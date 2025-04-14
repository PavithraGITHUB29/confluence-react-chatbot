import { useState } from "react";
import axios from "axios";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I'm your Confluence Assistant 🤖. Ask me anything about the documentation." }
  ]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", content: input };
    setMessages([...messages, userMsg]);
    setInput("");

    try {
      const res = await axios.post("http://localhost:5000/api/chat", { query: input });
      const response = res.data.answer || "Sorry, no answer found.";
      const page = res.data.title ? `**From page:** *${res.data.title}*\n\n` : "";

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `${page}${response}` }
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Error fetching response from server." }
      ]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-md p-6 space-y-4">
        <h1 className="text-2xl font-semibold">📘 Confluence Chatbot</h1>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`p-3 rounded-lg ${msg.role === "user" ? "bg-green-100 text-right" : "bg-blue-50 text-left border-l-4 border-blue-500"}`}
            >
              <div className="whitespace-pre-wrap">{msg.content}</div>
            </div>
          ))}
        </div>
        <div className="flex space-x-2">
          <input
            className="flex-1 border rounded-md px-4 py-2"
            value={input}
            placeholder="Type your question here..."
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
