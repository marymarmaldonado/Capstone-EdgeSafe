import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  function handleLogin(e: any) {
    e.preventDefault();

    // temporary mock user auth (will be replaced)
    if (username === "admin" && password === "admin") {
      localStorage.setItem("isAuthenticated", "true");
      navigate("/home");
    } else {
      setError("Invalid credentials");
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>EdgeSafe Login</h1>
        <p className="login-subtitle">
          Authorized access to detection dashboard
        </p>

        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && <p className="login-error">{error}</p>}

          <button type="submit">Sign In</button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;