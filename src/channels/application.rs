use loco_rs::socketioxide::extract::{AckSender, Bin, Data, SocketRef};
use tracing::info;
use serde_json::Value;

pub async fn on_connect(socket: SocketRef) {
    info!("Socket.IO connected: {:?} {:?}", socket.ns(), socket.id);
    // socket.emit("auth", data).ok();

    socket.on(
        "message",
        |socket: SocketRef, Data::<Value>(data), Bin(bin)| {
            info!("Received event: {:?} {:?}", data, bin);
            socket.bin(bin).emit("message-back", data).ok();
        },
    );

    socket.on(
        "message-with-ack",
        |Data::<Value>(data), ack: AckSender, Bin(bin)| {
            info!("Received event: {:?} {:?}", data, bin);
            ack.bin(bin).send(data).ok();
        },
    );

    socket.on(
        "get-player-data",
        |socket: SocketRef, Data::<Value>(data)| {
            info!("Received get-player-data event: {:?}", data);
            // TODO: Fetch player data from database
            // This is a placeholder for the actual implementation
            let player_data = serde_json::json!({
                "name": "Player1",
                "level": 5,
                "score": 1000,
            });
            socket.emit("player-data", player_data).ok();
        },
    );
}
