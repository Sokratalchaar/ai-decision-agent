import { useState } from "react";

function Register({ setIsLoginPage }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    const res = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (data.error) {
      alert(data.error);
      return;
    }

    alert("User created! Please login.");

    // 🔥 رجّع لصفحة login
    setIsLoginPage(true);
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500">
      <div className="bg-white/20 p-6 rounded-xl backdrop-blur-lg w-80">
        <h2 className="text-white text-xl mb-4">Register</h2>

        <input
          className="w-full mb-3 p-2 rounded bg-white/20 text-white"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="w-full mb-4 p-2 rounded bg-white/20 text-white"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleRegister}
          className="w-full bg-white text-purple-700 py-2 rounded"
        >
          Register
        </button>

        {/* 🔥 switch to login */}
        <p
          onClick={() => setIsLoginPage(true)}
          className="text-white mt-3 text-sm cursor-pointer"
        >
          Already have an account? Login
        </p>
      </div>
    </div>
  );
}

export default Register;