"""Plex API class for constructing OCP-shaped search results"""
from typing import List

from plexapi.audio import Artist, Album, Track
from plexapi.video import Episode, Movie, Show
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.library import MovieSection, ShowSection, MusicSection


class PlexAPI:
    """Thinly wrapped plexapi library for OCP results"""
    def __init__(self, token: str):
        account = MyPlexAccount(token=token)
        servers = [r for r in account.resources() if "server" in r.provides]
        self.servers: List[PlexServer] = [account.resource(server.name).connect() for server in servers]
        self.movies, self.shows, self.music = [], [], []
        self.init_libraries()

    def init_libraries(self):
        """Load music, TV, and movie libraries from Plex servers"""
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
        """Search known music libraries for a specific query"""
        track_list = []
        for i, music in enumerate(self.music):
            results = music.hubSearch(query)  # Artist, Album, Track
            if not results:
                continue
            tracks = None
            best = results[0]
            if isinstance(best, Artist) or isinstance(best, Album):
                tracks = best.tracks()
            elif isinstance(best, Track):
                tracks = [best]
            if not tracks:
                continue
            track_list += [{
                    'image': self._get_plex_res(track.parentThumb, i) if track.parentThumb else None,
                    'bg_image': self._get_plex_res(track.grandparentArt, i) if track.grandparentArt else None,
                    'uri': track.getStreamURL(),
                    'title': track.title,
                    'album': track.parentTitle,
                    'artist': track.grandparentTitle,
                    'length': track.duration
                    } for track in tracks]
        return track_list

    def search_movies(self, query: str):
        """Search known movie libraries for a specific query"""
        movie_list = []
        for movies in self.movies:
            results = movies.hubSearch(query)
            if not results:
                continue
            movie_results = []
            best = results[0]
            if isinstance(best, Movie):
                movie_results.append(best)
            if not movie_results:
                continue
            movie_list += [{
                    'image': mov.thumbUrl if mov.thumbUrl else None,
                    'bg_image': mov.posterUrl if mov.posterUrl else None,
                    'uri': mov.getStreamURL(),
                    'title': mov.title,
                    'album': mov.title,
                    'artist': ", ".join([director.tag for director in mov.directors]) if mov.directors else None,
                    'length': mov.duration,
                    } for mov in movie_results]
        return movie_list

    def search_shows(self, query: str):
        """Search known TV libraries for a specific query"""
        show_list = []
        for shows in self.shows:
            results = shows.hubSearch(query)
            if not results:
                continue
            show_results = []
            best = results[0]
            if isinstance(best, Show):
                show_results += best.episodes()
            elif isinstance(best, Episode):
                show_results += [best]
            if not show_results:
                continue
            show_list += [{
                    'image': show.thumbUrl if show.thumbUrl else None,
                    'bg_image': show.posterUrl if show.posterUrl else None,
                    'uri': show.getStreamURL(),
                    'title': f"{show.seasonEpisode if show.seasonEpisode else ''} - {show.title}",
                    'album': f"{show.grandparentTitle if show.grandparentTitle else ''} - {show.parentTitle}",
                    'artist': ", ".join([director.tag for director in show.directors]) if show.directors else None,
                    'length': show.duration,
                    } for show in show_results]
        return show_list

    def _get_plex_res(self, resource: str, i: int) -> str:
        return self.servers[i].url(resource, True)
