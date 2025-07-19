# Agents Manifest

This file provides a manifest of the tools, configurations, and environments used in this project.

## Project Structure

- `frontend/`: Contains the client-side application (HTML, CSS, JavaScript).
- `backend/`: Contains the server-side application (Python with Flask).
- `config/`: Contains configuration files, such as `tools.json`.

## Tooling

### Frontend

- **Linter:** ESLint
- **Testing:** No testing framework is currently in place.

### Backend

- **Linter:** Pylint
- **Testing:** No testing framework is currently in place.

## Build and Deployment

- A basic CI pipeline is configured in `.github/workflows/ci.yml`. This pipeline lints the Python and JavaScript code on every push.
- No Dockerfile or other containerization is set up.
