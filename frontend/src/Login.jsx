import { useState } from "react";

function Login({  setIsLoggedIn, setIsLoginPage }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const res = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (data.error) {
      alert("Invalid credentials");
      return;
    }

    // 🔥 خزّن user_id
    localStorage.setItem("token", data.token);

    setIsLoggedIn(true);
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500">
      <div className="bg-white/20 p-6 rounded-xl backdrop-blur-lg w-80">
        <h2 className="text-white text-xl mb-4">Login</h2>

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
  onClick={handleLogin}
  className="w-full bg-white text-purple-700 py-2 rounded"
>
  Login
</button>

<p
  onClick={() => setIsLoginPage(false)}
  className="text-white mt-3 text-sm cursor-pointer"
>
  Don't have an account? Register
</p>
      </div>
    </div>
  );
}

export default Login;