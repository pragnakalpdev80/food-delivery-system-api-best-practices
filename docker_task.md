## Containerize a Django Application Using Docker and Docker Compose

### 🎯 Objective

Your task is to containerize a Django application and make it accessible in a web browser using Docker and Docker Compose.

This assignment is designed to help you understand how Docker packages Python applications and their dependencies into portable containers that can run consistently across environments. 

---

## 📌 Problem Statement

You are given a standard Django project (or you may create a new one).

Your goal is to:

1. Create a Docker image for the Django application.
2. Configure Docker Compose to run the application.
3. Expose the Django development server on port `8000`.
4. Ensure that the application is accessible at:

   * `http://localhost:8000`
5. Use best practices such as:

   * `.dockerignore`
   * Dependency management with `requirements.txt`
   * Volume mounting for development

---

## 📋 Requirements

Your solution must include the following files:

* `Dockerfile`
* `docker-compose.yml`
* `.dockerignore`
* `requirements.txt`

The Docker container should:

* Use an official Python base image.
* Install all project dependencies.
* Copy the Django project into the container.
* Run the Django development server.
* Listen on `0.0.0.0:8000`.

The Docker Compose configuration should:

* Build the image from the local Dockerfile.
* Map port `8000` from the container to the host.
* Mount the project directory as a volume.
* Restart automatically unless stopped manually.

---

## 🌐 Expected Output

When the application is started successfully, opening the following URL in a browser should display the Django application:

```text
http://localhost:8000
```

If using a fresh Django project, the default Django welcome page should appear.

---

## 📦 Deliverables

Submit the following:

1. `Dockerfile`
2. `docker-compose.yml`
3. `.dockerignore`
4. `requirements.txt`
5. Screenshot of the application running in the browser
6. Output of the following commands:

   * `docker ps`
   * `docker images`
   * `docker compose ps`

---
