export default function PasswordStrength({ password }) {
  if (!password) return null;

  const checks = [
    ["8+ characters", password.length >= 8],
    ["Uppercase letter", /[A-Z]/.test(password)],
    ["Lowercase letter", /[a-z]/.test(password)],
    ["Number", /\d/.test(password)],
    ["Special character", /[^A-Za-z0-9]/.test(password)]
  ];

  return (
    <div className="password-checks">
      {checks.map(([label, valid]) => (
        <span className={valid ? "check valid" : "check"} key={label}>
          {valid ? "✓" : "○"} {label}
        </span>
      ))}
    </div>
  );
}