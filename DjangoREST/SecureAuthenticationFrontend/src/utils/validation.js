export function calculateAge(dob) {
  if (!dob) return "";
  const birth = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const month = today.getMonth() - birth.getMonth();
  if (month < 0 || (month === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  return age >= 0 ? age : "";
}

export function validateMobile(mobile) {
  return /^\+\d{10,15}$/.test(mobile);
}

export function validatePassword(password) {
  return password.length >= 8;
}