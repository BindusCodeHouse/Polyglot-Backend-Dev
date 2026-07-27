import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { logoutUser } from "../api/authApi";
import { clearSession, isAuthenticated } from "../utils/auth";

export default function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [busy, setBusy] = useState(false);
  const loggedIn = isAuthenticated();

  async function handleLogout() {
    const refresh = localStorage.getItem("refresh_token");
    setBusy(true);
    try {
      if (refresh) await logoutUser(refresh);
    } catch {
      // Clear the client session even if the token is already invalid.
    } finally {
      clearSession();
      setBusy(false);
      navigate("/login", { replace: true });
    }
  }

  return (
    <div className="app-shell">
      <header className="navbar">
        <Link className="brand" to={loggedIn ? "/profile" : "/login"}>
          <span className="brand-mark">S</span>
          <span>SecureAuth</span>
        </Link>

        <nav>
          {!loggedIn ? (
            <>
              <Link className={location.pathname === "/login" ? "active" : ""} to="/login">Login</Link>
              <Link className={location.pathname === "/register" ? "active" : ""} to="/register">Register</Link>
            </>
          ) : (
            <>
              <Link className={location.pathname === "/profile" ? "active" : ""} to="/profile">Profile</Link>
              <button className="nav-button" onClick={handleLogout} disabled={busy}>
                {busy ? "Logging out..." : "Logout"}
              </button>
            </>
          )}
        </nav>
      </header>

      <main className="page-container">
        <Outlet />
      </main>

      <footer className="footer">Secure Authentication System · Django REST API + React</footer>
    </div>
  );
}