import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import Alert from "../components/Alert";
import { registerUser } from "../api/authApi";
import { getApiError } from "../utils/auth";
import { calculateAge, validateMobile } from "../utils/validation";

const initialForm = {
  first_name: "",
  last_name: "",
  age: "",
  dob: "",
  email: "",
  mobile: "",
  hobby: "",
  gender: ""
};

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  function update(e) {
    const { name, value } = e.target;
    if (name === "dob") {
      setForm((old) => ({ ...old, dob: value, age: calculateAge(value) }));
    } else {
      setForm((old) => ({ ...old, [name]: value }));
    }
  }

  async function submit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!validateMobile(form.mobile)) {
      setError("Mobile must start with + and contain 10 to 15 digits.");
      return;
    }

    setLoading(true);
    try {
      const response = await registerUser({
        ...form,
        age: Number(form.age)
      });

      sessionStorage.setItem("pending_mobile", response.data.mobile);
      setSuccess(response.data.message);
      setTimeout(() => navigate("/verify-otp"), 800);
    } catch (err) {
      setError(getApiError(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthCard
      eyebrow="STEP 01 · CREATE ACCOUNT"
      title="Create your account"
      description="Enter your profile details. We will send a one-time password to your mobile number."
    >
      <Alert>{error}</Alert>
      <Alert type="success">{success}</Alert>

      <form className="form-grid" onSubmit={submit}>
        <div className="field">
          <label>First name</label>
          <input name="first_name" value={form.first_name} onChange={update} required />
        </div>
        <div className="field">
          <label>Last name</label>
          <input name="last_name" value={form.last_name} onChange={update} required />
        </div>

        <div className="field">
          <label>Date of birth</label>
          <input type="date" name="dob" value={form.dob} onChange={update} required />
        </div>
        <div className="field">
          <label>Age</label>
          <input type="number" name="age" value={form.age} readOnly className="readonly" />
        </div>

        <div className="field full">
          <label>Email address</label>
          <input type="email" name="email" value={form.email} onChange={update} required />
        </div>

        <div className="field full">
          <label>Mobile number</label>
          <input
            name="mobile"
            value={form.mobile}
            onChange={update}
            placeholder="+919876543210"
            required
          />
          <small>Include country code, for example +91.</small>
        </div>

        <div className="field">
          <label>Hobby</label>
          <input name="hobby" value={form.hobby} onChange={update} required />
        </div>

        <div className="field">
          <label>Gender</label>
          <select name="gender" value={form.gender} onChange={update} required>
            <option value="">Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>

        <button className="primary-button full" disabled={loading}>
          {loading ? "Creating account..." : "Register & Send OTP"}
        </button>
      </form>

      <div className="form-footer">
        Already have an account? <Link to="/login">Sign in</Link>
      </div>
    </AuthCard>
  );
}