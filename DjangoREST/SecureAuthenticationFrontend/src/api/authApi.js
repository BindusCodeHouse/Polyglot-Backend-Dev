import api from "./client";

export const registerUser = (payload) =>
  api.post("/register/", payload);

export const verifyOtp = (payload) =>
  api.post("/verify-otp/", payload);

export const setPassword = (payload) =>
  api.post("/set-password/", payload);

export const loginUser = (payload) =>
  api.post("/login/", payload);

export const getProfile = () =>
  api.get("/profile/");

export const logoutUser = (refresh) =>
  api.post("/logout/", { refresh });