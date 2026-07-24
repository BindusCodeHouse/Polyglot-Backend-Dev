export default function AuthCard({ eyebrow, title, description, children }) {
  return (
    <section className="auth-card">
      <div className="auth-card-header">
        {eyebrow && <div className="eyebrow">{eyebrow}</div>}
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>
      {children}
    </section>
  );
}