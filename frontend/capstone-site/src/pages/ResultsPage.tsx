import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import { apiFetch } from "../api";
import "../styles/dashboard.css";

type DetectionEvent = {
  id: number;
  model_name: string;
  inference_ms: number;
  timestamp: string;
  confidence: number;
  detected: boolean;
  source: string;
  image_path: string;
};

function ResultsPage() {
  const [events, setEvents] = useState<DetectionEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await apiFetch("/events");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: DetectionEvent[] = await response.json();
        setEvents(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const totalRecentEvents = events.length;
  const avgInferenceMs =
    totalRecentEvents > 0
      ? Math.round(
          events.reduce((sum, event) => sum + event.inference_ms, 0) /
            totalRecentEvents
        )
      : 0;

  const latestDetectedEvent = events.find((event) => event.detected);

  if (loading) {
    return (
      <div>
        <Navbar />
        <main style={{ padding: "2rem" }}>
          <p>Loading detection results...</p>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <Navbar />
        <main style={{ padding: "2rem" }}>
          <p>Error loading data: {error}</p>
        </main>
      </div>
    );
  }

  return (
    <div>
      <Navbar />

      <main className="dashboard-page">
        <section className="dashboard-header">
          <div>
            <h1 className="dashboard-title">Detection Results</h1>
            <p className="dashboard-subtitle">
              Review recent firearm detection activity, detection metadata, and performance metrics.
            </p>
          </div>
        </section>

        <section className="stats-grid">
          <article className="dashboard-card stat-card">
            <p className="stat-label">Recent Events</p>
            <h2 className="stat-value">{totalRecentEvents}</h2>
            <p className="stat-helper">Latest processed records</p>
          </article>

          <article className="dashboard-card stat-card">
            <p className="stat-label">Average Inference</p>
            <h2 className="stat-value">{avgInferenceMs} ms</h2>
            <p className="stat-helper">Recent processing latency</p>
          </article>

          <article className="dashboard-card stat-card">
            <p className="stat-label">Latest Detection</p>
            <h2 className="stat-value small-text">
              {latestDetectedEvent
                ? formatTimestamp(latestDetectedEvent.timestamp)
                : "No detections"}
            </h2>
            <p className="stat-helper">
              {latestDetectedEvent
                ? `${latestDetectedEvent.source} • ${Math.round(
                    latestDetectedEvent.confidence * 100
                  )}% confidence`
                : "No recent high-risk event"}
            </p>
          </article>
        </section>

        <section className="dashboard-grid">
          <article className="dashboard-card">
            <div className="section-header">
              <div>
                <h2>Recent Detection of Events</h2>
              </div>
            </div>

            <div className="table-wrapper">
              <table className="events-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Timestamp</th>
                    <th>Source</th>
                    <th>Model</th>
                    <th>Inference</th>
                    <th>Confidence</th>
                    <th>Status</th>
                    <th>Image Ref</th>
                  </tr>
                </thead>
                <tbody>
                  {events.map((event) => (
                    <tr key={event.id}>
                      <td>#{event.id}</td>
                      <td>{formatTimestamp(event.timestamp)}</td>
                      <td>{event.source}</td>
                      <td>{event.model_name}</td>
                      <td>{event.inference_ms} ms</td>
                      <td>{Math.round(event.confidence * 100)}%</td>
                      <td>
                        <span
                          className={`status-badge ${
                            event.detected
                              ? "status-detected"
                              : "status-not-detected"
                          }`}
                        >
                          {event.detected ? "Detected" : "Not Detected"}
                        </span>
                      </td>
                      <td>{event.image_path}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </article>
 
        </section>
      </main>
    </div>
  );
}

function formatTimestamp(timestamp: string) {
  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return timestamp;
  }

  return date.toLocaleString();
}

export default ResultsPage;