import { useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import Alert from "../components/Alert";
import PasswordStrength from "../components/PasswordStrength";
import { setPassword } from "../api/authApi";
import { getApiError } from "../utils/auth";

export default function SetPassword() {
  const navigate = useNavigate();
  const params = useParams();
  const [searchParams] = useSearchParams();

  const uidb64 = params.uidb64 || searchParams.get("uidb64") || "";
  const token = params.token || searchParams.get("token") || "";

  const [password, setPasswordValue] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [terms, setTerms] = useState(false);
  const [privacy, setPrivacy] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!uidb64 || !token) {
      setError("Invalid password setup link. Please open the link sent to your email.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (!terms || !privacy) {
      setError("You must accept both Terms & Conditions and Privacy Policy.");
      return;
    }

    setLoading(true);
    try {
      const response = await setPassword({
        uidb64,
        token,
        password,
        confirm_password: confirmPassword,
        accepted_terms_and_conditions: terms,
        accepted_privacy_policy: privacy
      });
      setSuccess(response.data.message);
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      setError(getApiError(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthCard
      eyebrow="STEP 03 · SECURE ACCOUNT"
      title="Set your password"
      description="Create a strong password to activate your account."
    >
      <Alert>{error}</Alert>
      <Alert type="success">{success}</Alert>

      <form onSubmit={submit}>
        <div className="field">
          <label>New password</label>
          <input type="password" value={password} onChange={(e) => setPasswordValue(e.target.value)} required />
        </div>

        <PasswordStrength password={password} />

        <div className="field">
          <label>Confirm password</label>
          <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
        </div>

        <label className="checkbox">
          <input type="checkbox" checked={terms} onChange={(e) => setTerms(e.target.checked)} />
          <span>I accept the Terms & Conditions.</span>
        </label>

        <label className="checkbox">
          <input type="checkbox" checked={privacy} onChange={(e) => setPrivacy(e.target.checked)} />
          <span>I accept the Privacy Policy.</span>
        </label>

        <button className="primary-button" disabled={loading}>
          {loading ? "Activating account..." : "Set Password & Activate"}
        </button>
      </form>

      <div className="form-footer">
        Already activated? <Link to="/login">Go to login</Link>
      </div>
    </AuthCard>
  );
}