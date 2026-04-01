import Navbar from "../components/Navbar";

function HomePage() {
  return (
    <div>
      <Navbar />
      <main style={styles.main}>
        <section style={styles.section}>
          <h1>Project Presentation</h1>
          <p>
            EdgeSafe is an edge-based firearm detection and secure event logging
            system designed for educational environments.
          </p>
        </section>

        <section style={styles.section}>
          <h2>Team</h2>
          <p>Include your team presentation here.</p>
        </section>

        <section style={styles.section}>
          <h2>Deliverables</h2>
          <p>Include the elevator pitch, presentation, GitHub, and tools here.</p>
        </section>
      </main>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  main: {
    maxWidth: "1000px",
    margin: "0 auto",
    padding: "2rem",
  },
  section: {
    backgroundColor: "#f9fafb",
    borderRadius: "12px",
    padding: "1.5rem",
    marginBottom: "1.5rem",
  },
};

export default HomePage;