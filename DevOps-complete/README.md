
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
- The Jenkins pipeline automates the application lifecycle of the Currency Converter Microservice, including the stages of build, test, and deployment.
-  The pipeline is defined in the Jenkinsfile and orchestrates the following steps:
-  1. Checkout Stage
    Purpose: This stage checks out the source code from the version control system (e.g., GitHub, GitLab).
    Action:
    checkout scm: This command fetches the source code from the repository.
    It allows Jenkins to pull the latest changes made to the repository, ensuring that the pipeline runs with the most up-to-date codebase.
    Example:
    This stage fetches the code from the repository so that the pipeline can run subsequent stages on the latest version.

- 2. Build Stage
    Purpose: This stage is responsible for building the Docker image for the FastAPI application.
    Action:
    sh 'docker-compose -f ${DOCKER_COMPOSE_FILE} build --pull --no-cache ${IMAGE_NAME}':
    This command uses docker-compose to build the Docker image for the FastAPI application.
    The --pull option ensures that the latest version of the base images is pulled.
    The --no-cache flag forces a fresh build by not using cache layers, ensuring a clean image build every time.
    Example:
    After this stage, a Docker image is ready for deployment. It will contain the application code and all dependencies.

- 3. Linting Stage
    Purpose: This stage checks the source code for potential issues or coding standard violations (e.g., style guide issues).
    Action:
    sh 'docker run --rm -v $PWD/app:/app -w /app python:3.11-slim bash -c "pip install flake8 && flake8 ."':
    This runs a Python linter (flake8) in a Docker container, checking the code for style issues.
    The --rm option removes the container after the linting process is complete.
    Linting helps maintain code quality by enforcing style rules.
    Example:
    If the code does not follow the required coding standards, the pipeline will fail at this stage.

- 4. Unit Tests Stage
    Purpose: This stage runs unit tests to ensure that individual components of the FastAPI application work correctly.
    Action:
    sh 'docker run --rm -v $PWD/app:/app -w /app python:3.11-slim bash -c "pip install -r requirements.txt pytest && pytest -q"':
    This command runs pytest within a Python Docker container.
    The -q flag ensures a quiet output, making it easier to read the results.
    It installs dependencies from requirements.txt and runs all unit tests.
    Example:
    Unit tests verify that the core functionality of the FastAPI backend works as expected (e.g., ensuring API endpoints respond correctly).

5. Integration Tests Stage
    Purpose: This stage runs integration tests to verify the interaction between different parts of the system (e.g., database, external APIs).
    Action:
    sh 'docker run --rm -v $PWD/app:/app -w /app python:3.11-slim bash -c "pip install -r requirements.txt pytest && pytest tests/integration"':
    This command runs integration tests located in the tests/integration directory.
    These tests ensure that the backend interacts correctly with external services or APIs, such as a currency exchange service.
    Example:
    After this stage, any issues in how different parts of the application interact with each other will be identified.

- 6. Deploy Stage
    Purpose: This stage deploys the application to a containerized environment using Docker Compose.
    Action:
    sh 'docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --remove-orphans --build':
    This command brings up the containers using docker-compose, builds the images, and runs them in detached mode (-d).
    The --remove-orphans option ensures that any leftover containers from previous builds are removed.
    Example:
    At the end of this stage, the application should be running in containers, with all services deployed and ready to use.

- 7. Test Deployment Stage
    Purpose: This stage checks if the application is deployed successfully and is responding to requests (i.e., performs a health check).
    Action:
    sh 'curl -sS http://localhost:8000/health || exit 1':
    This uses curl to make a request to the FastAPI /health endpoint, verifying that the application is live and healthy.
    If the health check fails (i.e., the server is not running), the pipeline will exit with an error (exit 1).

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
