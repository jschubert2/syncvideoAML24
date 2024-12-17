from flask_socketio import emit
import json

def register_socketio_handlers(socketio, redis_client):
    @socketio.on("sync_request")
    def handle_sync_request():
        try:
            scheduler_data = redis_client.get("3:sc")
            if scheduler_data:
                scheduler_data = json.loads(scheduler_data.decode('utf-8'))
                emit("sync_state", scheduler_data)
            else:
                emit("sync_state", {"error": "No scheduler data found in Redis."})
        except Exception as e:
            emit("sync_state", {"error": str(e)})

    @socketio.on("update_state")
    def update_state(data):
        emit("test",data,broadcast=True)
        

