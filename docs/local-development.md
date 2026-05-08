# Local Development Guide

This guide covers setting up the Marketplace Platform for local development.

## Prerequisites

- Docker and Docker Compose
- GNU Make (optional, but recommended)

## Setup Instructions

1. **Clone the Repository**
2. **Initialize Environment:**
   ```bash
   cp .env.example .env
   ```
3. **Build and Start:**
   ```bash
   make init
   # or
   docker compose up --build -d
   ```
4. **Database Migrations:**
   ```bash
   make migrate
   ```
5. **Create Superuser:**
   ```bash
   make superuser
   ```

## Common Commands

Refer to the [Makefile](../Makefile) for a full list of commands:
- `make dev`: Start the development server and Celery worker.
- `make test`: Run the test suite.
- `make check`: Run Django checks and linting.
