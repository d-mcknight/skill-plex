from plexapi.audio import Artist, Album, Track
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.library import MovieSection, ShowSection, MusicSection


class PlexAPI:
    def __init__(self, token: str):
        account = MyPlexAccount(token=token)
        self.server: PlexServer = account.resource(
            [r for r in account.resources()
             if "server" in r.provides][0].name).connect()
        self.movies, self.shows, self.music = None, None, None
        self.init_libraries()

    def init_libraries(self):
        lib = self.server.library.sections()
        for section in lib:
            if isinstance(section, MovieSection):
                self.movies = section
            elif isinstance(section, ShowSection):
                self.shows = section
            elif isinstance(section, MusicSection):
                self.music = section

    def search_music(self, query: str):
        results = self.music.hubSearch(query)  # Artist, Album, Track
        if not results:
            return None
        tracks = None
        best = results[0]
        if isinstance(best, Artist) or isinstance(best, Album):
            tracks = best.tracks()
        elif isinstance(best, Track):
            tracks = [best]
        if not tracks:
            return None
        return [{
                'image': self._get_plex_res(track.parentThumb) if track.parentThumb else None,
                'bg_image': self._get_plex_res(track.grandparentArt) if track.grandparentArt else None,
                'uri': track.getStreamURL(),
                'title': track.title,
                'album': track.parentTitle,
                'artist': track.grandparentTitle,
                'length': track.duration
                } for track in tracks]

    def _get_plex_res(self, resource: str) -> str:
        return self.server.url(resource, True)
