# Contacts Manager

I built this as part of the Nology DevOps accelerator to practice containerizing an app and building a full CI/CD pipeline. It's a simple contacts manager, you can add people, assign them to a group, and delete them.

**Live app:** https://contacts-manager-theta.vercel.app
**Backend API:** https://contacts-manager-production-7a2c.up.railway.app

## Stack

- Backend: FastAPI and SQLAlchemy, tested with pytest
- Database: MySQL 8
- Frontend: React and TypeScript, built with Vite
- Local dev: Docker Compose
- CI/CD: GitHub Actions
- Hosting: Railway for the backend and database, Vercel for the frontend

## Running it locally

You need Docker installed. Nothing else.

```bash
git clone https://github.com/jordanjoseph95/contacts-manager.git
cd contacts-manager
docker compose up
```

That starts three containers, the database, the backend on port 8000, and the frontend on port 5173. Go to http://localhost:5173 once it's up.

The backend waits for MySQL to pass its healthcheck before it starts, so you don't need to worry about startup order. Both the backend and frontend hot reload, so you can edit code and see changes without rebuilding anything. The database data lives in a named volume, so it's still there if you run `docker compose down` and bring it back up.

## Branches and protection

I work on `develop` and merge into `main` for production. Both branches require the `Backend Tests` check to pass before you can merge a PR. I haven't turned on "Include administrators" yet, so as the repo owner I can still push straight to a protected branch and skip the check. Everything should go through a PR anyway.

## The pipeline

### Backend Tests

Runs my pytest suite against a real MySQL container. Triggers on:
- PRs into develop
- PRs into main
- pushes to develop or main

This is the check that has to pass before anything merges.

### Lint

Runs ESLint on the frontend through Reviewdog and leaves comments on the PR. This one's advisory only, it never blocks a merge, it's just there to flag things.

### Deploy Backend

Fires once Backend Tests passes on main, so it only runs after an actual merge, not when a PR is opened. It deploys the backend to Railway using their CLI, authenticated with a `RAILWAY_TOKEN` I stored as a GitHub Actions secret. If the deploy fails, the workflow shows red in the Actions tab, so I'd know straight away.

The frontend deploys on its own through Vercel's GitHub integration, which redeploys automatically whenever main changes.

## Why Railway and Vercel

I picked Railway for the backend and database because it was quick to set up and has MySQL hosting built in, plus a CLI I could wire straight into GitHub Actions. I set the actual deploy trigger up through Actions rather than Railway's own auto-deploy, so there's one clear path for deploys instead of two things fighting over it.

I picked Vercel for the frontend because it just works with Vite out of the box and deploys automatically on push.

### Manual steps I had to do outside the code

**Railway:**
1. Created a project with MySQL from Railway's template.
2. Added a backend service pointed at the `backend` folder in this repo.
3. Set the backend's environment variables, pointing at the MySQL service using Railway's `${{ServiceName.VAR}}` syntax.
4. Generated a public domain for the backend under Networking.
5. Created a project token and saved it as `RAILWAY_TOKEN` in the repo's Actions secrets.
6. Turned off Railway's own "Auto deploys when pushed to GitHub" and "Wait for CI," since GitHub Actions already handles both of those.
7. Cleared the backend service's Root Directory setting, because the Actions workflow already scopes the deploy to the backend folder before it uploads.

**Vercel:**
1. Imported the repo.
2. Set Root Directory to `frontend`.
3. Added `VITE_API_URL` as an environment variable, pointing at the Railway backend URL.

**CORS:**
The backend only accepts requests from `http://localhost:5173` and the live Vercel URL.

## Evidence

- Green CI run: https://github.com/jordanjoseph95/contacts-manager/actions/runs/36924834655
- Successful deploy: https://github.com/jordanjoseph95/contacts-manager/actions/runs/36925100064
- Live app: https://contacts-manager-theta.vercel.app