import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input) return;

    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);

    setInput("");
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/decision", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: input,
      }),
    });

    const data = await res.json();

    const aiMsg = { role: "ai", content: data.result };

    setMessages((prev) => [...prev, aiMsg]);
    setLoading(false);
  };

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500">

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-xl p-4 rounded-2xl ${
              msg.role === "user"
                ? "ml-auto bg-white text-black"
                : "mr-auto bg-white/20 text-white"
            }`}
          >
            {msg.content}
          </div>
        ))}

        {loading && (
          <div className="text-white opacity-70">Thinking...</div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 bg-black/20 backdrop-blur-lg flex gap-2">
        <input
          className="flex-1 p-3 rounded-xl bg-white/20 text-white placeholder-gray-300 focus:outline-none"
          placeholder="Ask anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button
          onClick={sendMessage}
          className="bg-white text-purple-700 px-6 rounded-xl font-semibold"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;