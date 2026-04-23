import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [budget, setBudget] = useState("");
  const [goal, setGoal] = useState("");
  const [priority, setPriority] = useState("");
  const [result, setResult] = useState("");

  const handleSubmit = async () => {
    const response = await fetch("http://127.0.0.1:8000/decision", {
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

    const data = await response.json();
    setResult(data.result);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Decision Assistant 🚀</h1>

      <input
        placeholder="Your question"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Budget"
        value={budget}
        onChange={(e) => setBudget(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Goal"
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Priority"
        value={priority}
        onChange={(e) => setPriority(e.target.value)}
      />
      <br /><br />

      <button onClick={handleSubmit}>Get Decision</button>

      <h2>Result:</h2>
      <pre>{result}</pre>
    </div>
  );
}

export default App;