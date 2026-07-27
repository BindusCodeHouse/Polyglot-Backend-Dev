import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <section className="not-found">
      <div className="eyebrow">404</div>
      <h1>Page not found</h1>
      <p>The page you requested does not exist.</p>
      <Link className="primary-button inline-button" to="/login">Return to Login</Link>
    </section>
  );
}