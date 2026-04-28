import { useState } from "react";
import { useEffect } from "react";
import Login from "./Login";
import Register from "./Register";

function App() {
  const [conversations, setConversations] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [isLoginPage, setIsLoginPage] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );
  console.log("isLoggedIn:", isLoggedIn);
  localStorage.getItem("token")
  

  const currentChat = conversations.find(c => c.id === currentChatId);
  const messages = currentChat ? currentChat.messages : [];


  useEffect(() => {
    const loadChats = async () => {
      const token = localStorage.getItem("token");
  
      if (!token) return;
  
      try {
        const res = await fetch("http://127.0.0.1:8000/chats", {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
        });
  
        if (!res.ok) {
          console.log("fetch failed");
          return;
        }
  
        const data = await res.json();
  
        console.log("CHATS:", data); // 🔥 مهم
  
        if (data.length > 0) {
          setConversations(data);
          setCurrentChatId(data[data.length - 1].id);
        }
  
        setLoaded(true); // 🔥 لازم تكون هون
      } catch (err) {
        console.log("ERROR:", err);
      }
    };
  
    loadChats();
  }, []);



  useEffect(() => {
    if (!loaded) return;
  
    localStorage.setItem("chats", JSON.stringify(conversations));
    localStorage.setItem("currentChatId", currentChatId);
  }, [conversations, currentChatId, loaded]);

  const sendMessage = async () => {
    if (!input) return;
  
    const userMsg = {
      id: Date.now(),
      role: "user",
      content: input,
    };
  
    let chatId = currentChatId;
  
    // 🆕 إذا ما في شات → أنشئ واحد
    if (!chatId) {
      chatId = Date.now();
  
      const newChat = {
        id: chatId,
        title: input.slice(0, 20),
        messages: [userMsg],
      };
  
      setConversations(prev => [...prev, newChat]);
      setCurrentChatId(chatId);
    } else {
      // ➕ ضيف على الشات الحالي
      setConversations((prev) =>
        prev.map((chat) =>
          chat.id === chatId
            ? { ...chat, messages: [...chat.messages, userMsg] }
            : chat
        )
      );
    }
  
    setInput("");
    setLoading(true);
    const token = localStorage.getItem("token");
    if (!token) return;
    // 🔥 API
    const res = await fetch("http://127.0.0.1:8000/decision", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        query: input,
      }),
    });
  
    const data = await res.json();
  
    const aiMsg = {
      id: Date.now() + 1,
      role: "ai",
      content: data.result,
    };
  
    // ➕ ضيف رد AI
    setConversations((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? { ...chat, messages: [...chat.messages, aiMsg] }
          : chat
      )
    );
  
    setLoading(false);
  };
  useEffect(() => {
    if (!loaded || conversations.length === 0) return; 
  
    const saveChats = async () => {
      const token = localStorage.getItem("token");
      if (!token) return;
      await fetch("http://127.0.0.1:8000/chats", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          conversations,
        }),
      });
    };
  
    saveChats();
  }, [conversations, loaded]);


  if (!isLoggedIn) {
    return isLoginPage ? (
      <Login
        setIsLoggedIn={setIsLoggedIn}
        setIsLoginPage={setIsLoginPage}
      />
    ) : (
      <Register setIsLoginPage={setIsLoginPage} />
    );
  }

  return (
    <div className="h-screen flex bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500">
  
      {/* Sidebar */}
      <div className="w-72 bg-black/30 backdrop-blur-xl p-4 flex flex-col">
  
        <h2 className="text-white text-xl font-bold mb-4">
          AI Assistant
        </h2>
  
        {/* New Chat */}
        <button
          onClick={() => setCurrentChatId(null)}
          className="bg-white text-purple-700 rounded-xl p-2 mb-3 font-semibold hover:opacity-90"
        >
          + New Chat
        </button>
  
        {/* Logout */}
        <button
          onClick={() => {
            localStorage.removeItem("token");
            setIsLoggedIn(false);
          }}
          className="bg-red-500 text-white rounded-xl p-2 mb-4 font-semibold hover:bg-red-600"
        >
          Logout
        </button>
  
        {/* Chats List */}
        <div className="flex-1 overflow-y-auto space-y-2">
  
          {conversations.map((chat) => (
            <div
              key={chat.id}
              onClick={() => setCurrentChatId(chat.id)}
              className={`flex justify-between items-center p-3 rounded-xl cursor-pointer transition ${
                chat.id === currentChatId
                  ? "bg-white text-black"
                  : "bg-white/10 text-white hover:bg-white/20"
              }`}
            >
              {/* Title */}
              <span className="truncate">
                {chat.title.length > 20
                  ? chat.title.slice(0, 20) + "..."
                  : chat.title}
              </span>
  
              {/* Delete Button */}
              <button
                onClick={async (e) => {
                  e.stopPropagation();
  
                  const token = localStorage.getItem("token");
  
                  await fetch(`http://127.0.0.1:8000/chats/${chat.id}`, {
                    method: "DELETE",
                    headers: {
                      Authorization: `Bearer ${token}`,
                    },
                  });
  
                  setConversations(prev =>
                    prev.filter(c => c.id !== chat.id)
                  );
  
                  if (currentChatId === chat.id) {
                    setCurrentChatId(null);
                  }
                }}
                className="ml-2 text-red-400 hover:text-red-600"
              >
                ❌
              </button>
            </div>
          ))}
  
        </div>
      </div>
  
      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
  
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
  
          {messages.map((msg) => (
            <div
              key={msg.id}
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
            className="bg-white text-purple-700 px-6 rounded-xl font-semibold hover:opacity-90"
          >
            Send
          </button>
        </div>
  
      </div>
    </div>
  );
}

export default App;