
# Currency Converter – DevOps-ready Microservice

## Overview  
This project is a DevOps-ready microservice acting as a Currency Converter. The goal was to build a scalable and containerized application consisting of a **FastAPI backend**, a **simple frontend**, and a complete **CI/CD, monitoring, and testing environment**.  

The architecture is designed to enable efficient development and operations, combining modern DevOps tools like **Docker**, **Jenkins**, **Prometheus**, **Grafana**, and **JMeter** with a clean Python codebase.

---

## Architecture and Components  

### 1. Backend (FastAPI)
- Developed as a microservice with at least 4 endpoints:  
  - 2 **GET** routes to fetch data (e.g., current exchange rates).  
  - 2 **POST** routes to perform conversions and store data.  
- A dedicated **/external** endpoint calls an external service for data, e.g., live exchange rates.  
- **Unit tests** are implemented with `pytest` to ensure API functionality.

### 2. Frontend
- Lightweight HTML/JavaScript interface for interacting with the backend.  
- Accessible at `http://localhost:8000/frontend/index.html`.  
- Communicates with FastAPI via REST.

### 3. Containerization (Docker & docker-compose)
- All services run in containers, orchestrated using **docker-compose**.  
- Services include:
  - `app`: FastAPI backend (Port 8000)  
  - `prometheus`: Monitoring (Port 9090)  
  - `grafana`: Visualization (Port 3000)  
  - `jenkins`: CI/CD (Port 8080)  
  - `jmeter`: Load testing container  
- The entire system can be started with one command:
  ```bash
  docker-compose up -d --build
  ```

---

## DevOps Integration  

### Jenkins (CI/CD)
- Automated pipeline via **Jenkinsfile**:
  - Build Docker image  
  - Run unit tests  
  - Deploy using docker-compose  
- Jenkins initializes on first run; the password can be found in the container logs.

### Monitoring
- **Prometheus** collects metrics directly from the app (`/metrics` endpoint).  
- **Grafana** visualizes collected metrics on dashboards.  
- Example endpoints:
  - App metrics: `http://localhost:8000/metrics`
  - Prometheus UI: `http://localhost:9090`
  - Grafana: `http://localhost:3000`

### Testing
- **Unit tests** using `pytest`:
  ```bash
  docker run --rm -v $PWD/app:/app -w /app python:3.11-slim bash -c "pip install -r requirements.txt pytest && pytest -q"
  ```
- **Playwright** is set up for UI testing; configuration in `app/playwright-requirements.txt`.

---

## Local Usage
Requirements:  
- Docker  
- docker-compose  

Start services:
```bash
docker-compose up -d --build
```

Access:
- Frontend: `http://localhost:8000/frontend/index.html`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Jenkins: `http://localhost:8080`

---

## Conclusion
This project demonstrates how to set up a microservice with a complete DevOps toolchain. It covers the full lifecycle — from development, testing, and CI/CD to monitoring and visualization.  
It provides a solid foundation for more complex systems with multiple services or automated deployments.
