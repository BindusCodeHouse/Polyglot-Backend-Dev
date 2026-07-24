# Secure Authentication Frontend

React + Vite frontend for the uploaded Django REST Framework authentication backend.

## Backend APIs implemented

- `POST /myApp/register/`
- `POST /myApp/verify-otp/`
- `POST /myApp/set-password/`
- `POST /myApp/login/`
- `GET /myApp/profile/`
- `POST /myApp/logout/`

## User flow

```text
Register
   ↓
OTP Verification
   ↓
Password Setup Link from Email
   ↓
Set Password + Accept Terms/Privacy
   ↓
Login
   ↓
Protected Profile
   ↓
Logout
```

If the user enters the wrong OTP 3 times, the backend deletes the pending user. The frontend sends the user back to Register.

## Setup

1. Install Node.js.
2. Open this frontend folder.
3. Create `.env` from `.env.example`.
4. Set:

```env
VITE_API_BASE_URL=http://localhost:8000/myApp
```

5. Install dependencies:

```bash
npm install
```

6. Start:

```bash
npm run dev
```

Frontend normally runs at:

```text
http://localhost:5173
```

## Important: password setup email URL

Your Django backend sends a URL containing `uid` and `token`. This frontend supports:

```text
http://localhost:5173/set-password/<uidb64>/<token>
```

It also supports query parameters:

```text
http://localhost:5173/set-password?uidb64=<uid>&token=<token>
```

Your Django email should point to the React frontend, not the Django API endpoint. The React page then calls:

```text
POST http://localhost:8000/myApp/set-password/
```

with:

```json
{
  "uidb64": "<uid>",
  "token": "<token>",
  "password": "StrongPassword@123",
  "confirm_password": "StrongPassword@123",
  "accepted_terms_and_conditions": true,
  "accepted_privacy_policy": true
}
```

## CORS

Because React and Django run on different ports during development, Django must allow the frontend origin.

Example:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

Make sure `corsheaders` middleware is configured before Django's common middleware.

## JWT note

The current backend has access + refresh token generation and refresh-token blacklisting on logout, but the uploaded backend does **not** expose a refresh-token endpoint.

The frontend therefore sends the access token on protected requests, but it cannot automatically renew an expired 5-minute access token.

Recommended backend endpoint:

```text
POST /myApp/token/refresh/
```

Then the frontend can automatically refresh access tokens with an Axios interceptor.

## Project structure

```text
SecureAuthenticationFrontend/
├── src/
│   ├── api/
│   │   ├── client.js
│   │   └── authApi.js
│   ├── components/
│   │   ├── Alert.jsx
│   │   ├── AuthCard.jsx
│   │   ├── Layout.jsx
│   │   ├── PasswordStrength.jsx
│   │   └── ProtectedRoute.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── NotFound.jsx
│   │   ├── Profile.jsx
│   │   ├── Register.jsx
│   │   ├── SetPassword.jsx
│   │   └── VerifyOtp.jsx
│   ├── utils/
│   │   ├── auth.js
│   │   └── validation.js
│   ├── App.jsx
│   ├── main.jsx
│   └── styles.css
├── .env.example
├── index.html
├── package.json
├── vite.config.js
└── README.md
```
