# routes.py
from flask import Blueprint, render_template, send_file, current_app, abort, Response
from app.redis_utils import get_scheduler_data, get_video, get_all_songs
import json
import os
import io

    
main = Blueprint('main', __name__)

def get_video_data(client, song_name):
    key = f"1:{song_name}:vi"
    video_binary = client.get(key)
    if not video_binary:
        raise FileNotFoundError(f"Video data for {song_name} not found in Redis.")
    return video_binary

@main.route("/video/<song_name>")
def serve_video(song_name):
    client = current_app.redis_client
    try:
        video_binary = get_video_data(client, song_name)
        return Response(video_binary, mimetype="video/mp4")
    except FileNotFoundError as e:
        return str(e), 404

# soll geändert werden !!
@main.route("/song/<song_name>")
def song_details(song_name):
    client = current_app.redis_client

    video_data = get_video(client, song_name)

    scheduler_data = get_scheduler_data(client)

    song_scheduler_info = next(
        (data for data in scheduler_data if data.get('song_name') == song_name),
        None
    )

    if not video_data:
        abort(404, description=f"Kein Video für {song_name} gefunden.")

    json_filename = save_song_data(song_name, client)

    return render_template("song.html",
                           song_name=song_name,
                           video_data=video_data,
                           song_scheduler_info=song_scheduler_info,
                           json_filename=json_filename)





def save_song_data(song_name, client):
    os.makedirs('saved_data', exist_ok=True)

    song_data = {
        "song_name": song_name,
        "scheduler_info": {},
        "video_info": {}
    }

    scheduler_keys = client.keys("*:sc")
    for key in scheduler_keys:
        data = client.get(key)
        if data:
            try:
                scheduler_info = json.loads(data.decode('utf-8'))
                song_data['scheduler_info'] = scheduler_info
            except json.JSONDecodeError:
                continue

    video_keys = client.keys(f"*:{song_name}:vi")
    if video_keys:
        video_key = video_keys[0]
        video_data = client.get(video_key)
        if video_data:
            video_filename = f"saved_data/{song_name}_video.bin"
            with open(video_filename, 'wb') as video_file:
                video_file.write(video_data)

            song_data['video_info'] = {
                "key": video_key.decode('utf-8'),
                "filename": video_filename,
                "size": len(video_data)
            }

    json_filename = f"saved_data/{song_name}_complete_info.json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(song_data, json_file, indent=4, ensure_ascii=False)

    return json_filename


@main.route("/")
def index():
    client = current_app.redis_client
    songs = get_all_songs(client)

    # Für jeden Song eine JSON-Datei erstellen
    for song in songs:
        save_song_data(song['song_name'], client)

    return render_template("index.html", songs=songs)