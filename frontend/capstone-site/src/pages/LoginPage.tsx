import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "../styles/login.css";

type LocationState = { from?: { pathname?: string } } | null;

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as LocationState;
  const from = state?.from?.pathname || "/home";

  async function handleLogin(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.status === 401) {
        setError("Invalid credentials");
        return;
      }

      if (!response.ok) {
        setError("Login failed. Please try again.");
        return;
      }

      const data: { access_token: string; token_type: string } =
        await response.json();
      localStorage.setItem("token", data.access_token);
      navigate(from, { replace: true });
    } catch (err) {
      console.error("Login request failed:", err);
      setError("Could not reach the server. Please try again.");
    } finally {
      setLoading(false);
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
            disabled={loading}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />

          {error && <p className="login-error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
