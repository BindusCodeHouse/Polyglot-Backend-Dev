export function saveSession(data) {
  localStorage.setItem("access_token", data.tokens.access);
  localStorage.setItem("refresh_token", data.tokens.refresh);
  localStorage.setItem("user", JSON.stringify(data.user));
}

export function clearSession() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
}

export function getStoredUser() {
  try {
    return JSON.parse(localStorage.getItem("user") || "null");
  } catch {
    return null;
  }
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem("access_token"));
}

export function getApiError(error) {
  const data = error?.response?.data;

  if (!data) return "Unable to connect to the server.";

  if (typeof data === "string") return data;
  if (data.detail) return data.detail;
  if (data.message) return data.message;

  const messages = [];
  Object.entries(data).forEach(([field, value]) => {
    const values = Array.isArray(value) ? value : [value];
    values.forEach((message) => {
      if (typeof message === "string") {
        messages.push(field === "non_field_errors" ? message : `${field}: ${message}`);
      }
    });
  });

  return messages.join(" ") || "Something went wrong.";
}