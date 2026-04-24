import { useState } from "react";
import './App.css'
function App() {
  const [query, setQuery] = useState("");
  const [budget, setBudget] = useState("");
  const [goal, setGoal] = useState("");
  const [priority, setPriority] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/decision", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
        budget: budget ? parseInt(budget) : null,
        goal,
        priority,
      }),
    });

    const data = await res.json();
    setResult(data.result);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center p-6">

      <div className="backdrop-blur-lg bg-white/10 border border-white/20 shadow-2xl rounded-3xl p-8 w-full max-w-xl text-white">

        <h1 className="text-3xl font-bold text-center mb-6">
          AI Decision Assistant 🚀
        </h1>

        <div className="space-y-4">
          <input
            className="w-full p-3 rounded-lg bg-white/20 placeholder-gray-200 focus:outline-none"
            placeholder="What do you want to decide?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <input
            className="w-full p-3 rounded-lg bg-white/20 placeholder-gray-200 focus:outline-none"
            placeholder="Budget"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
          />

          <input
            className="w-full p-3 rounded-lg bg-white/20 placeholder-gray-200 focus:outline-none"
            placeholder="Goal (e.g., programming)"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
          />

          <input
            className="w-full p-3 rounded-lg bg-white/20 placeholder-gray-200 focus:outline-none"
            placeholder="Priority (e.g., battery)"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
          />
        </div>

        <button
          onClick={handleSubmit}
          className="mt-6 w-full bg-white text-purple-700 font-semibold py-3 rounded-xl hover:scale-105 transition transform"
        >
          {loading ? "Thinking..." : "Get Decision"}
        </button>

        {result && (
          <div className="mt-6 bg-white/20 p-4 rounded-xl whitespace-pre-wrap text-sm">
            {result}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;