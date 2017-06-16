from ...share import *

import googleapiclient.discovery as _googleapi

ytdevkey = apikeys["ytdevkey"]
youtube = _googleapi.build("youtube", "v3", developerKey=ytdevkey)


def get_ytvideos(query, ui_m=None):
    """Gets either a list of videos from a playlist or a single video, from the first result of a YouTube search

    Args:
        query (str): The YouTube search query
        ui_m (ui_embed.MusicPlayer): The embed UI to send updates to

    Returns:
        queue (list): The items obtained from the YouTube search
    """

    queue = []

    # Search YouTube
    search_result = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=1,
        type="video,playlist"
    ).execute()

    # Get video/playlist title
    title = search_result["items"][0]["snippet"]["title"]
    if ui_m:
        runcoro(ui_m.temp_update_status("Queueing {}".format(title)))

    # Queue video if video
    if search_result["items"][0]["id"]["kind"] == "youtube#video":
        # Get ID of video
        videoid = search_result["items"][0]["id"]["videoId"]

        # Append video to queue
        queue.append(["https://www.youtube.com/watch?v={}".format(videoid), title])

    # Queue playlist if playlist
    elif search_result["items"][0]["id"]["kind"] == "youtube#playlist":
        # Get ID of playlist
        playlistid = search_result["items"][0]["id"]["playlistId"]

        # Get items in playlist
        playlist = youtube.playlistItems().list(
            playlistId=playlistid,
            part="snippet",
            maxResults=50
        ).execute()

        # Append videos to queue
        for entry in playlist["items"]:
            videoid = entry["snippet"]["resourceId"]["videoId"]
            songname = entry["snippet"]["title"]
            queue.append(["https://www.youtube.com/watch?v={}".format(videoid), songname])

        # For playlists with more than 50 entries
        if "nextPageToken" in playlist:
            counter = 2

            while "nextPageToken" in playlist:
                if ui_m:
                    runcoro(ui_m.temp_update_status("Queueing {} (page {})".format(title, str(counter))))

                counter += 1

                # Get items in next page of playlist
                playlist = youtube.playlistItems().list(
                    playlistId=playlistid,
                    part="snippet",
                    maxResults=50,
                    pageToken=playlist["nextPageToken"]
                ).execute()

                # Append videos to queue
                for entry in playlist["items"]:
                    videoid = entry["snippet"]["resourceId"]["videoId"]
                    songname = entry["snippet"]["title"]
                    queue.append(["https://www.youtube.com/watch?v={}".format(videoid), songname])

    return queue