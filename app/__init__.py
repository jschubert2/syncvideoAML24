from flask import Flask
from flask_socketio import SocketIO
from app.config import Config
from app.routes import main
from app.socketio_handlers import register_socketio_handlers
import redis
import threading
import time
import json
import ntplib
from datetime import datetime, timedelta

socketio = SocketIO()

def create_app():
    app = Flask(__name__, static_folder='saved_data')
    app.config.from_object(Config)

    app.redis_client = redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        db=Config.REDIS_DB,
        password=Config.REDIS_PASSWORD
    )

    app.register_blueprint(main)

    socketio.init_app(app)

    register_socketio_handlers(socketio, app.redis_client)

    threading.Thread(target=sc_update, args=(app.redis_client,), daemon=True).start()

    return app

def sc_update(redis_client):
    while True:
        scheduler_data = redis_client.get("3:sc")
        if scheduler_data:
            scheduler_data = json.loads(scheduler_data.decode('utf-8'))
            if scheduler_data.get("isPlaying") == "true":
                scheduler_data["st"] = "Play"
            elif scheduler_data.get("isPlaying") == "false":
                scheduler_data["st"] = "Stop"

            socketio.emit("sync_state", scheduler_data)
        time.sleep(1)


def sct_update(redis_client):
    sched_old = "Start"
    adjusted_time = None

    while True:
        try:
            client = ntplib.NTPClient()

            response = client.request("pool.ntp.org", version=3)

            ntp_time = datetime.utcfromtimestamp(response.tx_time)
        except Exception as e:
            return f"Error fetching time: {e}"

        scheduler_data = redis_client.get("3:sc")
        if scheduler_data:
            scheduler_data = json.loads(scheduler_data.decode('utf-8'))
            print(scheduler_data)
            if scheduler_data.get("isPlaying") == "true":
                if sched_old != scheduler_data.get("st"):
                    # From pause to play switch, add 5 seconds
                    #adjusted_time = ntp_time + timedelta(seconds=5)
                    adjusted_time = scheduler_data.get("t")
                    print("continue to play at "+adjusted_time)
                    print("current time "+ntp_time)

            elif scheduler_data.get("isPlaying") == "false":
                scheduler_data["st"] = "Stop"


            if adjusted_time is None:
                adjusted_time = ntp_time

            if ntp_time >= adjusted_time:
                if scheduler_data.get("isPlaying") == "true":
                    scheduler_data["st"] = "Play"
                    print("---continue playing---")

            socketio.emit("sync_state", scheduler_data) #signal to start/stop video in html by using sockets
            sched_old = scheduler_data["st"]

        time.sleep(1)