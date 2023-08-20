from typing import List, Optional

from plexapi.audio import Artist, Album, Track
from plexapi.video import Episode, Movie, Show
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.library import MovieSection, ShowSection, MusicSection
from ovos_utils.log import LOG


class PlexAPI:
    """Thinly wrapped plexapi library for OVOS Common Play results"""

    def __init__(self, token: str):
        self.servers: List[PlexServer] = []
        self.movies, self.shows, self.music: Optional[List[MusicSection]] = [], [], []
        self.connect_to_servers(token)
        self.init_libraries()

    def connect_to_servers(self, token: str):
        """Provide connections to all servers accessible from the provided token."""
        account = MyPlexAccount(token=token)
        servers = [r for r in account.resources() if "server" in r.provides]
        LOG.info("Found %s servers: %s", len(servers), ",".join([s.name for s in servers]))
        self.servers = [account.resource(server.name).connect() for server in servers]

    def init_libraries(self):
        """Initialize server libraries, specifically Movies, Shows, and Music."""
        for server in self.servers:
            lib = server.library.sections()
            for section in lib:
                if isinstance(section, MovieSection):
                    self.movies.append(section)
                elif isinstance(section, ShowSection):
                    self.shows.append(section)
                elif isinstance(section, MusicSection):
                    self.music.append(section)

    def search_music(self, query: str):
        """Search music libraries"""
        track_list = []
        for i, music in enumerate(self.music):
            results = music.hubSearch(query)
            for result in results:
                tracks = self._get_tracks_from_result(result)
                track_list += [self._construct_track_dict(track, i) for track in tracks]
        return track_list

    def _get_tracks_from_result(self, result):
        """Get music Tracks from search results"""
        if isinstance(result, Artist) or isinstance(result, Album):
            return result.tracks()
        elif isinstance(result, Track):
            return [result]
        return []

    def _construct_track_dict(self, track, i):
        """Construct a dictionary of Tracks for use with OVOS Common Play"""
        return {
            "image": track.thumbUrl if track.thumbUrl else "",
            "bg_image": track.artUrl if track.artUrl else "",
            "uri": track.getStreamURL(),
            "title": track.title,
            "album": track.parentTitle,
            "artist": track.grandparentTitle,
            "length": track.duration,
        }

    def search_movies(self, query: str):
        """Search movie libraries"""
        movie_list = []
        for movies in self.movies:
            results = movies.hubSearch(query)
            for result in results:
                if isinstance(result, Movie):
                    movie_list.append(self._construct_movie_dict(result))
        return movie_list

    def _construct_movie_dict(self, mov):
        """Construct a dictionary of Movies for use with OVOS Common Play"""
        return {
            "image": mov.thumbUrl if mov.thumbUrl else "",
            "bg_image": mov.posterUrl if mov.posterUrl else "",
            "uri": mov.getStreamURL(),
            "title": mov.title,
            "album": mov.title,
            "artist": ", ".join([director.tag for director in mov.directors]) if mov.directors else "",
            "length": mov.duration,
        }

    def search_shows(self, query: str):
        """Search TV Show libraries"""
        show_list = []
        for shows in self.shows:
            results = shows.hubSearch(query)
            for result in results:
                episodes = self._get_episodes_from_result(result)
                show_list += [self._construct_show_dict(show) for show in episodes]
        return show_list

    def _get_episodes_from_result(self, result):
        """Get TV Episodes from search results"""
        if isinstance(result, Show):
            return result.episodes()
        elif isinstance(result, Episode):
            return [result]
        return []

    def _construct_show_dict(self, show):
        """Construct a dictionary of Shows for use with OVOS Common Play"""
        return {
            "image": show.thumbUrl if show.thumbUrl else "",
            "bg_image": show.posterUrl if show.posterUrl else "",
            "uri": show.getStreamURL(),
            "title": f"{show.seasonEpisode if show.seasonEpisode else ''} - {show.title}",
            "album": f"{show.grandparentTitle if show.grandparentTitle else ''} - {show.parentTitle}",
            "artist": ", ".join([director.tag for director in show.directors]) if show.directors else "",
            "length": show.duration,
        }
