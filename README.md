# Chirpy

A REST API for a small Twitter-like service, written in TypeScript with Express and PostgreSQL. Users can sign up, log in, post short messages ("chirps"), and upgrade to a premium tier through a payment-provider webhook.


## Features

- **User accounts** with passwords hashed using Argon2.
- **Authentication** with short-lived JWT access tokens (1 hour) and database-backed refresh tokens that can be revoked.
- **Chirps** of up to 140 characters, with a simple profanity filter, filtering by author and sorting by date.
- **Authorisation**: users can only update their own account and delete their own chirps.
- **Webhook** endpoint for a payment provider ("Polka"), protected by an API key, that upgrades users to the premium "Chirpy Red" tier.
- **Database migrations** with Drizzle ORM, applied automatically on startup.
- **Unit tests** with Vitest for password hashing, JWT creation and validation, and token extraction.

## API

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/healthz` | – | Readiness check |
| POST | `/api/users` | – | Create a user |
| PUT | `/api/users` | Access token | Update own email and password |
| POST | `/api/login` | – | Log in; returns an access token and a refresh token |
| POST | `/api/refresh` | Refresh token | Get a new access token |
| POST | `/api/revoke` | Refresh token | Revoke a refresh token |
| POST | `/api/chirps` | Access token | Post a chirp |
| GET | `/api/chirps` | – | List chirps; optional `?authorId=` and `?sort=asc\|desc` |
| GET | `/api/chirps/:chirpId` | – | Get one chirp |
| DELETE | `/api/chirps/:chirpId` | Access token | Delete own chirp |
| POST | `/api/polka/webhooks` | API key | Handle the `user.upgraded` event |
| GET | `/admin/metrics` | – | Page showing visit count for `/app` |
| POST | `/admin/reset` | – | Reset metrics and delete all users (dev only) |

Tokens and the API key are sent in the `Authorization` header (`Bearer <token>` or `ApiKey <key>`).

## Setup

Requires Node.js 21.7 or later (see `.nvmrc`) and PostgreSQL.

```bash
npm install
```

Create a `.env` file in the project root:

```
DB_URL=postgres://user:password@localhost:5432/chirpy?sslmode=disable
PLATFORM=dev
SECRET=<a long random string for signing JWTs>
POLKA_KEY=<API key expected from the webhook>
```

The server refuses to start if any of these is missing. `PLATFORM=dev` enables the `/admin/reset` endpoint.

Run the server (it listens on port 8080):

```bash
npm run dev
```

Run the tests:

```bash
npm test
```

## Project layout

```
src/index.ts           Express app, routes and error handling
src/auth.ts            password hashing, JWTs, refresh tokens, header parsing
src/config.ts          loads and validates environment variables
src/error.ts           custom HTTP error classes
src/db/schema.ts       Drizzle schema: users, chirps, refresh_tokens
src/db/queries/        database queries for users and chirps
src/db/migrations/     generated SQL migrations
src/auth.test.ts       unit tests
```

## Tech stack

TypeScript · Node.js · Express 5 · PostgreSQL · Drizzle ORM · Argon2 · JSON Web Tokens · Vitest

## License

MIT
