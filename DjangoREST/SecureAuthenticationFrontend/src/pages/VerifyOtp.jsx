import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import Alert from "../components/Alert";
import { verifyOtp } from "../api/authApi";
import { getApiError } from "../utils/auth";

export default function VerifyOtp() {
  const navigate = useNavigate();
  const [mobile, setMobile] = useState(sessionStorage.getItem("pending_mobile") || "");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [attempts, setAttempts] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!mobile) setError("Mobile number is missing. Please register again.");
  }, [mobile]);

  async function submit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!/^\d{6}$/.test(otp)) {
      setError("Enter the 6-digit OTP.");
      return;
    }

    setLoading(true);
    try {
      const response = await verifyOtp({ mobile, otp });
      setSuccess(response.data.message);
      sessionStorage.removeItem("pending_mobile");
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      const data = err?.response?.data;
      if (data?.attempts_remaining !== undefined) {
        setAttempts(data.attempts_remaining);
      }
      setError(getApiError(err));
      if (data?.next_step === "/myApp/register/") {
        sessionStorage.removeItem("pending_mobile");
        setTimeout(() => navigate("/register"), 1800);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthCard
      eyebrow="STEP 02 · VERIFY MOBILE"
      title="Verify your mobile"
      description="Enter the 6-digit OTP sent to your registered mobile number."
    >
      <Alert>{error}</Alert>
      <Alert type="success">{success}</Alert>

      <form onSubmit={submit}>
        <div className="field">
          <label>Mobile number</label>
          <input value={mobile} onChange={(e) => setMobile(e.target.value)} required />
        </div>

        <div className="field otp-field">
          <label>6-digit OTP</label>
          <input
            inputMode="numeric"
            maxLength={6}
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
            placeholder="••••••"
            required
          />
        </div>

        {attempts !== null && (
          <div className="attempts">Attempts remaining: <strong>{attempts}</strong></div>
        )}

        <button className="primary-button" disabled={loading}>
          {loading ? "Verifying..." : "Verify OTP"}
        </button>
      </form>

      <div className="info-box">
        After 3 incorrect OTP attempts, your pending registration is deleted and you must register again.
      </div>

      <div className="form-footer">
        Wrong mobile number? <Link to="/register">Start again</Link>
      </div>
    </AuthCard>
  );
}