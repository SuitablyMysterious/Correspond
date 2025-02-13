import { useState } from 'react'
import { invoke } from '@tauri-apps/api/tauri'

function App() {
    const [message, setMessage] = useState('')

    async function sendMessage() {
        // Example of invoking a Rust command
        try {
            const response = await invoke('send_message', { message })
            console.log('Response:', response)
        } catch (error) {
            console.error('Error:', error)
        }
    }

    return (
        <div className="h-screen bg-gray-100 p-4">
            <div className="max-w-4xl mx-auto">
                <header className="mb-6">
                    <h1 className="text-3xl font-bold text-gray-800">Correspond</h1>
                    <p className="text-gray-600">Your messaging platform</p>
                </header>

                <main className="bg-white rounded-lg shadow p-6">
                    <div className="space-y-4">
                        <div className="flex flex-col">
                            <label htmlFor="message" className="text-sm font-medium text-gray-700 mb-1">
                                Message
                            </label>
                            <textarea
                                id="message"
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                className="border rounded-md p-2 h-32"
                                placeholder="Type your message here..."
                            />
                        </div>

                        <button
                            onClick={sendMessage}
                            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600
                       transition-colors duration-200"
                        >
                            Send Message
                        </button>
                    </div>
                </main>
            </div>
        </div>
    )
}

export default App