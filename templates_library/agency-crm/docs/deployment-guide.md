# Deployment Guide

## Supported Platforms
- **Vercel**: Optimized for static assets and serverless execution.
- **Railway**: Recommended for PostgreSQL and Redis hosting.
- **Render**: Great alternative for full-stack Django apps.

## Strategy
1. Configure production environment variables.
2. Set `DEBUG=False`.
3. Use a managed database service.
4. Configure S3 or Cloudflare R2 for media storage.
