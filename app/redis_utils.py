import json

def get_scheduler_data(client):
    keys = client.keys("*:sc")
    song_data = []
    for key in keys:
        data = client.get(key)
        if data:
            try:
                scheduler_info = json.loads(data.decode('utf-8'))
                song_data.append(scheduler_info)
            except json.JSONDecodeError:
                continue
    return song_data


def get_video(client, song_name):
    key = f"1:{song_name}:vi"
    video_data = client.get(key)
    if video_data:
        return video_data
    return None


def get_all_songs(client):
    keys = client.keys("*:sc")
    songs = []
    for key in keys:
        data = client.get(key)
        if data:
            try:
                song_info = json.loads(data.decode('utf-8'))
                song_name = song_info.get('song_name')
                if song_name and song_name not in [s['song_name'] for s in songs]:
                    songs.append({"song_name": song_name})
            except json.JSONDecodeError:
                continue
    return songs
