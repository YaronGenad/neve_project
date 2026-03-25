# Production-Ready System Plan for Al-Hashadeh Educational Material Generator

## Overview
This document outlines the plan to transform the current proof-of-concept (POC) system into a production-ready service that generates educational materials using the Al-Hashadeh methodology, with caching, user authentication, and a React frontend.

## System Architecture

### Backend Service (Python/FastAPI)
- **Authentication**: Email/password with JWT tokens
- **Database**: PostgreSQL for persistent storage of users, queries, and generated materials
- **Caching**: Redis for storing recent queries and generated materials (LRU eviction policy)
- **Similarity Search**: BM25 implementation using the `rank-bm25` library for finding similar teacher queries
- **Generation Pipeline**: Integrated existing generation pipeline as a service
- **API Endpoints**:
  - Auth: `/auth/register`, `/auth/login`, `/auth/refresh`
  - Queries: `/queries/submit`, `/queries/history`, `/queries/{id}`
  - Materials: `/materials/generate`, `/materials/{id}`, `/materials/download/{id}`
  - Health: `/health`

### Frontend (React)
- **Framework**: React with TypeScript
- **State Management**: React Context or Redux Toolkit
- **UI Library**: Material-UI (MUI) or Ant Design
- **Pages**:
  - Login/Register
  - Dashboard (query history)
  - Query Form (subject, topic, grade, rounds)
  - Results Viewer (preview generated materials)
  - Download Center (PDF downloads)
- **Features**:
  - Real-time similarity search suggestions as teacher types
  - Material preview before download
  - History of generated materials with search/filter
  - Responsive design for desktop/tablet use

### Data Models

#### User Table
- id (UUID, PK)
- email (string, unique)
- password_hash (string)
- full_name (string)
- created_at (timestamp)
- updated_at (timestamp)

#### Query Table
- id (UUID, PK)
- user_id (UUID, FK)
- subject (string)
- topic (string)
- grade (string)
- rounds (integer)
- query_text (string, normalized for search)
- created_at (timestamp)

#### Material Table
- id (UUID, PK)
- query_id (UUID, FK)
- content_json (JSONB, stores the generated content structure)
- file_paths (JSONB, paths to generated HTML/PDF files)
- version (integer, for tracking iterations)
- created_at (timestamp)

### Caching Strategy
- **Redis Keys**:
  - `query:{hash}`: Recent query results (TTL: 24 hours)
  - `material:{id}`: Generated material content (TTL: 7 days)
  - `user:{id}:history`: User's recent queries (TTL: 30 days)
- **Cache Warming**: Pre-populate with common queries during off-peak hours
- **Cache Invalidation**: On new material generation for similar queries

### BM25 Implementation
- **Library**: `rank-bm25` (Python)
- **Indexing**: 
  - Build index from all stored queries in PostgreSQL
  - Rebuild index periodically (every hour) or when new queries exceed threshold
  - Store index in Redis for fast lookup
- **Search Process**:
  1. Normalize incoming query (remove extra whitespace, lowercase)
  2. Search Redis cache for exact match
  3. If not found, use BM25 to find top-k similar queries
  4. Return cached materials for similar queries if similarity > threshold
  5. If no similar queries or teacher requests new generation, generate fresh material

### Security Considerations
- **Authentication**: 
  - Password hashing with bcrypt (cost factor 12)
  - JWT tokens with short expiration (15 min) and refresh tokens
  - HTTPS enforcement in production
- **Data Protection**:
  - SQL injection prevention via ORM/parameterized queries
  - Input validation and sanitization
  - Rate limiting on API endpoints
  - CORS restrictions to trusted domains
- **File Security**:
  - Sanitize file names to prevent path traversal
  - Serve generated files through secure endpoints
  - Regular cleanup of temporary files

### Error Handling & Logging
- **Logging**: Structured JSON logging to stdout/stderr
- **Error Types**:
  - Validation errors (400)
  - Authentication errors (401, 403)
  - Resource not found (404)
  - Generation failures (500)
  - Rate limit exceeded (429)
- **Monitoring**: 
  - Health check endpoints
  - Metrics collection (Prometheus compatible)
  - Error tracking (Sentry or similar)

### Testing Strategy
- **Unit Tests**: 
  - Backend: Pytest for API endpoints, utilities, BM25 logic
  - Frontend: Jest + React Testing Library for components
- **Integration Tests**:
  - Database interactions
  - API endpoint chains
  - Cache invalidation scenarios
- **End-to-End Tests**:
  - Cypress for critical user journeys (login → query → download)
- **Performance Tests**:
  - Load testing with Locust or k6
  - BM25 search performance benchmarks

### Deployment Considerations
- **Containerization**: Docker images for backend and frontend
- **Orchestration**: Docker Compose for development, Kubernetes for production
- **Environment Variables**:
  - Database connection strings
  - Redis connection
  - JWT secret keys
  - LLM API keys (Gemini/NVIDIA)
  - File storage paths
- **Scaling**:
  - Horizontal scaling of backend services
  - Redis clustering for cache
  - Read replicas for PostgreSQL
  - CDN for serving static assets (if needed)

## Implementation Roadmap

### Phase 1: Core Infrastructure
1. Set up PostgreSQL and Redis
2. Implement authentication system
3. Create basic API structure with FastAPI
4. Design database schemas

### Phase 2: Generation Pipeline Integration
1. Wrap existing generation pipeline as a service
2. Implement material storage and retrieval
3. Add file generation and PDF creation endpoints

### Phase 3: Caching and Search
1. Implement Redis caching layer
2. Develop BM25 similarity search
3. Add query normalization and caching logic

### Phase 4: Frontend Development
1. Create React application structure
2. Implement authentication flows
3. Build query submission and results interfaces
4. Add material preview and download functionality

### Phase 5: Security and Testing
1. Implement security measures (hashing, validation, rate limiting)
2. Write comprehensive test suite
3. Perform penetration testing and security audit
4. Optimize performance

### Phase 6: Deployment and Monitoring
1. Create Docker containers
2. Set up CI/CD pipeline
3. Configure monitoring and logging
4. Load testing and capacity planning

## Open Questions for Discussion
1. Should we store generated files in the filesystem or in the database (as BLOBs)?
2. What should be the similarity threshold for BM25 matches to trigger cache reuse?
3. How long should we cache generated materials before considering them stale?
4. Should we allow teachers to edit and regenerate materials based on existing versions?
5. What file naming convention should we use for generated materials?

## Next Steps
Review this plan with stakeholders and gather feedback. Once approved, begin implementation with Phase 1.