
# DevOps-ready Microservice (Student Project)

This project was created to fulfill the following requirements:
- Microservice API (FastAPI) with at least 4 endpoints: 2 GET, 2 POST.
- A call to an external microservice (/external endpoint).
- Unit tests (pytest/unittest).
- Simple frontend to interact with the API.
- Dockerized: the app runs in a container; docker-compose orchestrates app, Prometheus, Grafana, Jenkins and JMeter.
- Jenkinsfile to build, run tests and deploy using docker-compose.
- Prometheus metrics and Grafana ready to visualize metrics.
- Playwright test scaffold for UI testing.

## How to run locally (developer machine)

Requirements: Docker & docker-compose installed.

1. Build and start all services:
   ```
   docker-compose up -d --build
   ```
   This will start:
   - app on port 8000
   - prometheus on port 9090
   - grafana on port 3000
   - jenkins on port 8080
   - jmeter (idle) container

2. Open the minimal frontend:
   - http://localhost:8000/frontend/index.html

3. Prometheus metrics:
   - http://localhost:8000/metrics (app)
   - Prometheus UI: http://localhost:9090
   - Grafana UI: http://localhost:3000

4. Jenkins:
   - http://localhost:8080
   - The container will initialize Jenkins (first-run password in logs).

## Tests
- Unit tests: run locally with pytest inside the app folder:
  ```
  docker run --rm -v $PWD/app:/app -w /app python:3.11-slim bash -c "pip install -r requirements.txt pytest && pytest -q"
  ```
- Playwright: See `app/playwright-requirements.txt` to set up Playwright and run tests.

## Notes & Limitations
- The `/external` endpoint calls https://httpbin.org/get as an example external microservice. If you run in an offline environment, it will return a graceful error message.
- Jenkins is provided as a container. For automatic triggers on Git push, configure your Git repo webhook to Jenkins (or use GitHub/GitLab integration).
- JMeter: add .jmx plans to `tests/jmeter` and execute them with the jmeter container.
- Container auto-reload on git push: typical setups use webhooks from your Git provider to Jenkins; Jenkinsfile is provided to run build/test/deploy pipeline.

## What I added
- FastAPI microservice with endpoints: /health (GET), /items/{id} (GET), /external (GET), /items (POST), /compute (POST)
- Prometheus metrics supported.
- Dockerfile and docker-compose orchestration including Prometheus/Grafana/Jenkins/JMeter.
- Unit tests and Playwright test scaffold.
- Jenkinsfile for CI pipeline.
