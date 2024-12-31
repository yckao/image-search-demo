# Image Search Demo

A text-to-image search service powered by OpenAI's CLIP model. This service allows users to search for images using natural language queries and provide feedback on search results.

## Features

- 🔍 Text-to-image search using CLIP embeddings
- 📊 User feedback collection on search results
- 🗄️ Vector similarity search with pgvector
- 🐳 Fully containerized with Docker
- 🚀 High-performance async API with FastAPI
- 📦 S3-compatible object storage support

## Architecture

The service consists of several components:

- **FastAPI Web Server**: Handles HTTP requests and coordinates between services
- **PostgreSQL + pgvector**: Stores image metadata and vector embeddings
- **MinIO**: S3-compatible object storage for image files
- **CLIP Model**: Generates embeddings for text queries and images

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yckao/image-search-demo.git
cd image-search-demo
```

2. Create environent file for development

```bash
cp .env.example .env
```

3. Start the services using Docker Compose:

```bash
docker compose -f hack/compose/docker-compose.yaml --profile dev up -d
```

4. [Opitional] Upload assets

```bash
docker compose -f hack/compose/docker-compose.yaml run dev-assets
```

5. Open the API documentation at http://localhost:8000/docs

## Future Work

- [ ] Add tests
- [ ] Add observability (metrics, tracing, logging)
