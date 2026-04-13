// import Navbar from "../components/Navbar";

// function ResultsPage() {
//   return (
//     <div>
//       <Navbar />
//       <main style={{ padding: "2rem" }}>
//         <h1>Results</h1>
//         <p>This page will contain results, charts, and performance metrics.</p>
//       </main>
//     </div>
//   );
// }

// export default ResultsPage;

import Navbar from "../components/Navbar";
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

// mock data for recent detection events - in a real app this would come from an API call to the backend
const recentEvents: DetectionEvent[] = [
  {
    id: 12,
    model_name: "YOLOv8",
    inference_ms: 214,
    timestamp: "2026-04-13T10:24:18",
    confidence: 0.97,
    detected: true,
    source: "CAM 1",
    image_path: "images/test12.jpg",
  },
  {
    id: 11,
    model_name: "YOLOv8",
    inference_ms: 231,
    timestamp: "2026-04-13T10:12:43",
    confidence: 0.91,
    detected: true,
    source: "CAM 2",
    image_path: "images/test11.jpg",
  },
  {
    id: 10,
    model_name: "YOLOv8",
    inference_ms: 198,
    timestamp: "2026-04-13T09:58:07",
    confidence: 0.38,
    detected: false,
    source: "CAM 3",
    image_path: "images/test10.jpg",
  },
  {
    id: 9,
    model_name: "YOLOv8",
    inference_ms: 220,
    timestamp: "2026-04-13T09:44:56",
    confidence: 0.88,
    detected: true,
    source: "CAM 1",
    image_path: "images/test9.jpg",
  },
  {
    id: 8,
    model_name: "YOLOv8",
    inference_ms: 205,
    timestamp: "2026-04-13T09:31:14",
    confidence: 0.29,
    detected: false,
    source: "CAM 4",
    image_path: "images/test8.jpg",
  },
];

function ResultsPage() {
  const totalRecentEvents = recentEvents.length;
  const avgInferenceMs =
    totalRecentEvents > 0
      ? Math.round(
          recentEvents.reduce((sum, event) => sum + event.inference_ms, 0) /
            totalRecentEvents
        )
      : 0;

  const latestDetectedEvent = recentEvents.find((event) => event.detected);

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
                  {recentEvents.map((event) => (
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