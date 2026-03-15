import { useAuth } from "../context/authcontext";
import { useNavigate } from "react-router-dom";

export default function DashboardPage() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const handleLogout = () => {
        logout();
        navigate("/login", { replace: true });
    };

    return (
        <div style={styles.container}>
            <header style={styles.header}>
                <h1 style={styles.title}>Dashboard</h1>
                <button onClick={handleLogout} style={styles.logoutBtn}>
                    Logout
                </button>
            </header>
            <main style={styles.main}>
                <div style={styles.welcomeCard}>
                    <h2>Welcome, {user?.name ?? "User"} ■</h2>
                    <p>Email: {user?.email}</p>
                    <p style={styles.badge}>■ Authenticated</p>
                </div>
                <p style={styles.hint}>
                    Only authenticated users can see this page.
                </p>
            </main>
        </div>
    );
}

const styles = {
    container: { minHeight: "100vh", background: "#f8fafc" },
    header: {
        display: "flex", justifyContent: "space-between",
        alignItems: "center", padding: "1rem 2rem",
        background: "#0f172a", color: "#fff"
    },
    title: { margin: 0 },
    logoutBtn: {
        padding: "0.5rem 1.2rem", background: "#ef4444",
        color: "#fff", border: "none", borderRadius: 6,
        cursor: "pointer", fontWeight: "bold"
    },
    main: { padding: "2rem" },
    welcomeCard: {
        background: "#fff", padding: "1.5rem", borderRadius: 10,
        boxShadow: "0 1px 4px rgba(0,0,0,.1)", marginBottom: "1rem"
    },
    badge: { color: "#16a34a", fontWeight: "bold" },
    hint: { color: "#64748b", fontStyle: "italic" },
};