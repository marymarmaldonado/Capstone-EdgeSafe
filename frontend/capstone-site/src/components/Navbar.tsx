import { Link, useNavigate } from "react-router-dom";
import { isAuthenticated, logout } from "../api";

function Navbar() {
  const navigate = useNavigate();
  const loggedIn = isAuthenticated();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav style={styles.nav}>
      <h2 style={styles.title}>EdgeSafe</h2>
      <div style={styles.links}>
        <Link to="/home" style={styles.link}>Home</Link>
        <Link to="/results" style={styles.link}>Results</Link>
        <Link to="/logs" style={styles.link}>Logs</Link>
        {loggedIn && (
          <button onClick={handleLogout} style={styles.logoutBtn}>
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}

const styles: Record<string, React.CSSProperties> = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "1.5rem 3rem",
    borderBottom: "1px solid rgba(0, 0, 0, 0.2)",
    backgroundColor: "white",
  },
  title: {
    margin: 0,
    color: "#111827",
  },
  links: {
    display: "flex",
    gap: "2rem",
    alignItems: "center",
  },
  link: {
    color: "#111827",
    textDecoration: "none",
  },
  logoutBtn: {
    background: "none",
    border: "1px solid #e5e7eb",
    borderRadius: "6px",
    padding: "0.3rem 0.8rem",
    cursor: "pointer",
    fontSize: "0.9rem",
    color: "#111827",
  },
};

export default Navbar;