# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from os.path import join, dirname
from typing import List

from .plex_api import PlexAPI
from ovos_plugin_common_play import MediaType, PlaybackType
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search
from ovos_utils.log import LOG


class PlexSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super(PlexSkill, self).__init__()
        self.skill_icon = join(dirname(__file__), "plex.png")
        self._plex_api = None
        self.supported_media = [
            MediaType.GENERIC,
            MediaType.MUSIC,
            MediaType.AUDIO,
            MediaType.MOVIE,
            MediaType.SHORT_FILM,
            MediaType.SILENT_MOVIE,
            MediaType.VIDEO,
            MediaType.DOCUMENTARY,
            MediaType.CARTOON,
            # MediaType.TV,
        ]

    @property
    def plex_api(self):
        if not self._plex_api:
            if not self.settings.get('token'):
                self._init_plex_api_key()
            api_key = self.settings.get('token')
            self._plex_api = PlexAPI(api_key)
        return self._plex_api

    def _init_plex_api_key(self):
        from plexapi.myplex import MyPlexPinLogin
        account = MyPlexPinLogin()
        account.run()
        self.gui.show_text(account.pin)
        account.waitForLogin()
        token = account.token
        self.settings['token'] = token
        self.settings.store()

    @ocp_search()
    def search_plex(self, phrase, media_type=MediaType.GENERIC) -> List[dict]:
        """
        OCP Search handler to return results for a user request
        :param phrase: search phrase from user
        :param media_type: user requested media type
        :returns: list of dict search results
        """
        # TODO: improved confidence calculation
        confidence = 75
        if self.voc_match(phrase, "plex"):
            confidence += 15
            phrase = self.remove_voc(phrase, "plex")
            self.extend_timeout(3)

        # Determine what kind of media to play
        movie_search = self.voc_match(phrase, "movie")
        # tv_search = self.voc_match(phrase, "tv")
        phrase = self.remove_voc(phrase, "movie")
        # phrase = self.remove_voc(phrase, "tv")
        self.log.info(f"Media type for search: {media_type}")
        self.log.info(f"Perform a movie search? {movie_search}")
        # self.log.info(f"Perform a tv search? {tv_search}")
        phrase = phrase.replace("on ", "").replace("in ", "")

        # Music search
        if media_type in (MediaType.MUSIC, MediaType.AUDIO, MediaType.GENERIC) and \
        ("soundtrack" not in phrase and not movie_search):
            self.log.info(f"Searching Plex Music for {phrase}")
            for r in self.plex_api.search_music(phrase):
                r['media_type'] = MediaType.MUSIC
                r['playback'] = PlaybackType.AUDIO
                if media_type != MediaType.GENERIC:
                    confidence += 10
                r['match_confidence'] = confidence
                yield r

        # Movie search
        if media_type in (
            MediaType.MOVIE,
            MediaType.SHORT_FILM,
            MediaType.SILENT_MOVIE,
            MediaType.VIDEO,
            MediaType.DOCUMENTARY,
            MediaType.CARTOON,
            MediaType.GENERIC
        ):
            self.log.info(f"Searching Plex Movies for {phrase}")
            for movie in self.plex_api.search_movies(phrase):
                movie['media_type'] = MediaType.MOVIE
                movie['playback'] = PlaybackType.VIDEO
                if media_type != MediaType.GENERIC:
                    confidence += 10
                movie['match_confidence'] = confidence
                yield movie

        # # TV search
        # for episode in self.plex_api.search_shows(phrase):
        #     self.log.info(f"Searching Plex TV for {phrase}")
        #     episode['media_type'] = MediaType.TV
        #     episode['playback'] = PlaybackType.VIDEO
        #     if media_type != MediaType.GENERIC:
        #         confidence += 10
        #     episode['match_confidence'] = confidence
        #     yield episode


def create_skill():
    return PlexSkill()
