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
from typing import List

from .plex_api import PlexAPI
from ovos_plugin_common_play import MediaType, PlaybackType
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search
from ovos_utils.log import LOG


class PlexSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super(PlexSkill, self).__init__()
        self._plex_api = None

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
        confidence = 75
        if media_type == MediaType.MUSIC:
            for r in self.plex_api.search_music(phrase):
                r['match_confidence'] = confidence
                confidence -= 5
                yield r


def create_skill():
    return PlexSkill()