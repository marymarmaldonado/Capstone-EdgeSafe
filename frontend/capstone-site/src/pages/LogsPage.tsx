import Navbar from "../components/Navbar";

function LogsPage() {
  return (
    <div>
      <Navbar />
      <main style={{ padding: "2rem" }}>
        <h1>Event Logs</h1>
        <p>This page will show detection event logs.</p>
      </main>
    </div>
  );
}

export default LogsPage;