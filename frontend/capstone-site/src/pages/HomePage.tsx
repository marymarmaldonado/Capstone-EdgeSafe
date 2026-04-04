import Navbar from "../components/Navbar";
import image from "../../public/image.png";
import "../styles/home-page.css";

type TeamMember = {
  id: number;
  name: string;
  role: string;
  description: string;
  image: string;
};

const teamMembers: TeamMember[] = [
  {
    id: 1,
    name: "Andrea Seda",
    role: "Machine Learning & Edge Deployment",
    description:
      "Responsible for dataset preparation, YOLO model training, and deployment on the Jetson edge device.",
    image: image,
  },
  {
    id: 2,
    name: "Jessy Andújar",
    role: "Machine Learning & Edge Deployment",
    description:
      "Focused on model optimization, performance evaluation, and support for the live camera inference pipeline.",
    image: image,
  },
  {
    id: 3,
    name: "Jorge Marín",
    role: "Backend & Database",
    description:
      "Developed the backend API and local database for secure event logging, metadata storage, and retrieval.",
    image: image,
  },
  {
    id: 4,
    name: "Marymar Maldonado",
    role: "Frontend & Security",
    description:
      "Designed and implemented the dashboard UI, authentication flow, and secure access to project resources.",
    image: image,
  },
];

function HomePage() {
  return (
    <div>
      <Navbar />
      <main style={styles.main}>
        <h1>Project Presentation</h1>
        <section style={styles.section}>
          <h2 style={styles.heading}>Project Overview</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem", maxWidth: "750px", alignItems: "center", margin: "0 auto", fontSize: "0.9rem" }}>
            <div>
              <p>
                EdgeSafe is an edge-based firearm detection system designed for educational environments. It aims to improve safety by enabling real-time identification of firearms while reducing response time and preserving data privacy. Traditional security systems are reactive and rely on human monitoring, which can delay the detection of critical threats.
              </p>
            </div>
            <div>
              <p>
                EdgeSafe uses a YOLO-based object detection model deployed on a local edge device to analyze images and detect firearms. When a detection occurs, the system generates a structured event with metadata and stores it locally. Results are then displayed through a secure, authenticated web dashboard.
              </p>
            </div>
            <div>
              <p>
                Unlike cloud-based solutions, EdgeSafe performs all processing locally, reducing latency and eliminating dependence on internet connectivity. This approach improves reliability and protects sensitive data, making it more suitable for deployment in educational environments.
              </p>
            </div>
          </div>
        </section>

        <section style={styles.section}>
          <h2 className="team-heading">Meet the Team</h2>
          <div className="team-grid">
            {teamMembers.map((member) => (
              <article key={member.id} className="team-card">
                <img src={member.image} alt={member.name} className="team-image" />
                <h3 className="team-name">{member.name}</h3>
                <p className="team-role">{member.role}</p>
                <p className="team-description">{member.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section style={styles.section}>
          <h2 className="deliverables-heading">Project Deliverables</h2>

          <div className="deliverables-embed-grid">
            <div className="deliverable-panel">
              <h3 className="deliverable-title">Elevator Pitch Video</h3>
              <div className="video-wrapper">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/4C4HjbBjsyE?si=Ldzhk-10m0U0f5Y9" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
              </div>
            </div>

            <div className="deliverable-panel">
              <h3 className="deliverable-title">Final Presentation</h3>
              <div className="pdf-wrapper">
                <iframe
                  src="../public/capstone-proposal.pdf"
                  title="EdgeSafe Final Presentation"
                ></iframe>
              </div>
            </div>
          </div>

          <div className="deliverables-links-grid">
            <div className="deliverable-panel">
              <h3 className="deliverable-title">Project Links</h3>
              <ul className="deliverable-list">
                <li>
                  <a
                    href="https://github.com/marymarmaldonado/Capstone-EdgeSafe"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    GitHub Repository
                  </a>
                </li>
                <li>
                  <a
                    href="https://trello.com/b/uEwpHDVX/capstone-project"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Trello Board
                  </a>
                </li>
              </ul>
            </div>

            <div className="deliverable-panel">
              <h3 className="deliverable-title">Tools Used</h3>
              <ul className="deliverable-list">
                <li>YOLO</li>
                <li>PyTorch</li>
                <li>React</li>
                <li>SQLite</li>
                <li>NVIDIA Jetson Nano</li>
                <li>Git & GitHub</li>
              </ul>
            </div>

            <div className="deliverable-panel">
              <h3 className="deliverable-title">Sources</h3>
              <ul className="deliverable-list">
                <li>
                  <a
                    href="https://react.dev/"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    React Documentation
                  </a>
                </li>
                <li>
                  <a
                    href="https://www.sqlite.org/docs.html"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    SQLite Documentation
                  </a>
                </li>
                <li>
                  <a
                    href="https://docs.ultralytics.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Ultralytics YOLO Documentation
                  </a>
                </li>
                <li>
                  <a
                    href="https://developer.nvidia.com/embedded/jetson-nano-developer-kit"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Jetson Nano Documentation
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </section>
      </main>
    </div >
  );
}

const styles: Record<string, React.CSSProperties> = {
  main: {
    margin: "0 auto",
    padding: "2rem",
  },
  section: {
    padding: "2rem 0",
  },
  heading: {
    fontSize: "1.6rem",
    marginBottom: "1.5rem",
    color: "#111827",
    textAlign: "center",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "1.5rem",
  },
  card: {
    backgroundColor: "#ffffff",
    border: "1px solid #e5e7eb",
    borderRadius: "16px",
    padding: "1.5rem",
    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.05)",
    textAlign: "center",
  },
  image: {
    width: "120px",
    height: "120px",
    objectFit: "cover",
    borderRadius: "50%",
    marginBottom: "1rem",
    border: "3px solid #e5e7eb",
  },
  name: {
    margin: "0 0 0.5rem 0",
    fontSize: "0.95rem",
    color: "#111827",
  },
  role: {
    margin: "0 0 0.75rem 0",
    fontWeight: 600,
    color: "#4f46e5",
    fontSize: "0.8rem",
  },
  description: {
    margin: 0,
    color: "#4b5563",
    fontSize: "0.8rem",
    lineHeight: 1.5,
  },
};

export default HomePage;