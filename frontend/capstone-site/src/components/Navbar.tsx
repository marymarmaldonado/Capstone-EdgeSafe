import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={styles.nav}>
      <h2 style={styles.title}>EdgeSafe</h2>
      <div style={styles.links}>
        <Link to="/home" style={styles.link}>Home</Link>
        <Link to="/results" style={styles.link}>Results</Link>
        <Link to="/logs" style={styles.link}>Logs</Link>
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
  },
  link: {
    color: "#111827",
    textDecoration: "none",
  },
};

export default Navbar;