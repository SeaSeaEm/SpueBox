import spotipy
from spotipy import client
import config

import logging

def get_music_name(song):
    possible_author = None
    possible_song_name = None

    try:
        song = song.lower()
        # improve this parser
        if "-" not in song:
            # if there is no delimiter, how are we supposed to know which is the author or the track ?!
            possible_song_name = song.strip()
        else:
            possible_song_name = song.split('-')[1].strip()
            possible_author = song.split('-')[0].strip()

            if "ft" in song:
                possible_song_name = possible_song_name[:possible_song_name.index("ft")].strip()
            elif "feat" in song:
                possible_song_name = possible_song_name[:possible_song_name.index("feat")].strip()
            if "(" in song:
                possible_song_name = possible_song_name[:possible_song_name.index("(")].strip()
        
        
        if "official" in song:
            possible_song_name = possible_song_name[:possible_song_name.index("(official")]
    except Exception as e:
        logging.info(f"Unable to parse song name - {e}")
        pass
    
    # https://api.spotify.com/v1/search?query=track:a lot artist:21 Savage&type=track&market=BR&offset=0&limit=1
    if possible_author is None or possible_song_name is None:
        return

    logging.info("Author: " + possible_author)
    logging.info("Song: " + possible_song_name)

    from spotipy.oauth2 import SpotifyClientCredentials
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.client_id_spotify,
                                                                client_secret=config.client_secret_spotify))
    
    url = None

    if possible_author and possible_song_name:
        query = f'track:{possible_song_name} artist:{possible_author}'
    else:
        query = f'track:{possible_song_name}'
        
    logging.info(f"Query: {query}")
    logging.info(f'https://api.spotify.com/v1/search?query={query}&type=track&market=BR&offset=0&limit=1')
    try:
        results = sp.search(q=query, type='track', market='BR', limit='1')
        # import pprint

        try:
            # pprint.pprint(results["tracks"]["items"][0]["external_urls"]["spotify"])
            url = results["tracks"]["items"][0]["external_urls"]["spotify"]
        except Exception as e:
            logging.info(f"Unable to fetch track url - {e}")
            pass

        if url is None:
            # lets try fetching the album then
            try:
                # pprint.pprint(results["tracks"]["items"][0]["album"]["external_urls"]["spotify"])
                url = results["tracks"]["items"][0]["album"]["external_urls"]["spotify"]
            except Exception as e:
                logging.info(f"Unable to fetch album url - {e}")
                pass
            
        if url is None:
            # last shot, fetching the artist
            try:
                # pprint.pprint(results["tracks"]["items"][0]["artists"][0]["external_urls"]["spotify"])
                url = results["tracks"]["items"][0]["artists"][0]["external_urls"]["spotify"]
            except Exception as e:
                logging.info(f"Unable to fetch artist url - {e}")
                pass
    except:
        pass

    return url