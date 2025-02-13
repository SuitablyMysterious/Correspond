#[tauri::command]
fn send_message(message: String) -> String {
    // Handle the message here
    format!("Received message: {}", message)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![send_message])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}