import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import Alert from "../components/Alert";
import { getProfile } from "../api/authApi";
import { clearSession, getApiError } from "../utils/auth";

export default function Profile() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadProfile() {
      try {
        const response = await getProfile();
        setUser(response.data);
        localStorage.setItem("user", JSON.stringify(response.data));
      } catch (err) {
        setError(getApiError(err));
        if (err?.response?.status === 401) {
          clearSession();
          navigate("/login", { replace: true });
        }
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, [navigate]);

  return (
    <AuthCard
      eyebrow="PROTECTED AREA"
      title="Your profile"
      description="This data is loaded from the protected Django REST API."
    >
      <Alert>{error}</Alert>

      {loading ? (
        <div className="loading">Loading profile...</div>
      ) : user ? (
        <div className="profile-grid">
          <ProfileItem label="Full name" value={`${user.first_name} ${user.last_name}`} />
          <ProfileItem label="Email" value={user.email} />
          <ProfileItem label="Mobile" value={user.mobile} />
          <ProfileItem label="Date of birth" value={user.dob} />
          <ProfileItem label="Age" value={user.age} />
          <ProfileItem label="Gender" value={user.gender} />
          <ProfileItem label="Hobby" value={user.hobby} />
          <ProfileItem label="Mobile verified" value={user.is_mobile_verified ? "Yes" : "No"} />
          <ProfileItem label="Account active" value={user.is_active ? "Yes" : "No"} />
          <ProfileItem label="User ID" value={user.id} full />
        </div>
      ) : null}
    </AuthCard>
  );
}

function ProfileItem({ label, value, full }) {
  return (
    <div className={`profile-item ${full ? "full" : ""}`}>
      <span>{label}</span>
      <strong>{value || "—"}</strong>
    </div>
  );
}