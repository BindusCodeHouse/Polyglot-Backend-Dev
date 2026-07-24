import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import Alert from "../components/Alert";
import { loginUser } from "../api/authApi";
import { getApiError, saveSession } from "../utils/auth";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await loginUser({ email, password });
      saveSession(response.data);
      const destination = location.state?.from?.pathname || "/profile";
      navigate(destination, { replace: true });
    } catch (err) {
      setError(getApiError(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthCard
      eyebrow="WELCOME BACK"
      title="Sign in to SecureAuth"
      description="Use your email and password to access your protected profile."
    >
      <Alert>{error}</Alert>

      <form onSubmit={submit}>
        <div className="field">
          <label>Email address</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>

        <div className="field">
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>

        <button className="primary-button" disabled={loading}>
          {loading ? "Signing in..." : "Sign In"}
        </button>
      </form>

      <div className="form-footer">
        New user? <Link to="/register">Create an account</Link>
      </div>
    </AuthCard>
  );
}