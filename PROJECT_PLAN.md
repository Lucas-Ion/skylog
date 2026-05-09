# SkyLog

Written By: Lucas Ion

## What I'm building

SkyLog is a backend service for tracking flights and computing analytics over them. By the end it should be a real running system: an API, a worker that ingests live flight data from OpenSky Network, a Postgres database, Redis caching, structured logs, Prometheus metrics, and a deployment that survives me closing my desktop.

The reason I picked aviation is that the data is genuinely diverse and available. Flights have schedules, real positions, delays, routes, aircraft, airports, weather. It also has free public data sources (OpenSky, OurAirports CSV, Aviation Weather Center), so I'm never blocked on data.

## Books I'm working from

- Fluent Python (Ramalho) for Python depth
- Designing Data-Intensive Applications (Kleppmann) for system design and database thinking
- Clean Code (Martin) for readability and craft
- The Pragmatic Programmer (Hunt, Thomas) for engineering mindset
- Architecture Patterns with Python (Percival, Gregory) for the structural patterns I'll apply directly to SkyLog

## The shape of the project

The system grows in capability roughly like this:

In the first phase I will develop a clean CRUD API over Postgres. Tests, migrations, layered architecture.

In the second phase I will introduce real complexity. Async ingestion from the OpenSky API, Redis caching, structured logging, Prometheus metrics

In the third phase I will split the system into multiple processes. A separate worker, a message queue, event-driven persistence, idempotency. Then a followed by increasing database depth: indexes, query plans, materialised views.

In the final phase I will be focused on deployment and refactoring. Multi-stage Docker, GitHub Actions CI/CD, deployed to a real URL.

## Phase by phase

### Phase 1: Foundation

A FastAPI service over a Postgres database, exposing CRUD for airports, aircraft, and flights. SQLAlchemy 2.0 async, Alembic migrations, Pydantic v2 schemas, and pytest with a real test database. The architecture will aim to be layered (routers, services, repositories) and there are 30+ tests including integration tests.

Reading: Pragmatic Programmer chapters 1-2, Clean Code chapters 2-4, Architecture Patterns chapters 1-2.

### Phase 2: Async, external data, caching

A background async task pulls live aircraft positions from OpenSky every 60 seconds. Positions are persisted into a time-series-friendly schema. Reads are cached in Redis with a deliberate invalidation strategy that I write down before implementing. Structured logs with trace IDs. Prometheus metrics on request latency, ingestion success/failure, and cache hit ratio.

Reading: Fluent Python chapter 21 (async), DDIA chapter 1, DDIA chapter 2, Architecture Patterns chapter 3.

### Phase 3: Distributed and database depth

The ingestion worker becomes a separate process. A message broker sits between the API and the worker. Domain events (`FlightPositionRecorded`) are published and consumed idempotently. An analytics consumer updates aggregate tables from those events.

Then a focus on the database itself. EXPLAIN ANALYZE on every important query. Composite indexes. BRIN indexes for the time-series data. A materialised view or summary table for "busiest airports today". Connection pool tuning.

Reading: Architecture Patterns chapters 8-9, DDIA chapter 11 (first half), DDIA chapter 3 (full), DDIA chapter 7.

### Phase 4: Deployment and Pythonic refactor

Multi-stage Dockerfile, docker-compose for local dev, GitHub Actions running lint, typecheck, tests, build, and image push. Deployed to a real URL on Hetzner or Fly.io. HTTPS, env-based config, secrets handled properly.

I refactor the entire codebase using what I've absorbed from Fluent Python. Protocols instead of ABCs where it makes sense. Proper dataclasses for value objects. `__repr__` and `__eq__` on domain entities. `mypy --strict` clean. Audit async code for places where `asyncio.gather` or `TaskGroup` clarifies intent.

Reading Goals: Fluent Python chapters 5, 8, 11, 13, 15. Clean Code chapter 17.

## Final Phase

I'll focus on improve the proiject with 2-3 themes from this list rather than trying to do all of them:

- Replication and failover with read replicas, with documented RTO/RPO
- Partitioning the flight position data by date range and measuring impact
- Deliberately introducing eventual consistency somewhere and measuring the user-facing effect
- Load testing until something breaks, fixing it, repeating
- Practising zero-downtime schema migrations
- Distributed tracing across api → worker → database with OpenTelemetry

Reading: DDIA chapters 5, 6, 9, plus re-reading my own Week 1 code, which I expect to be horrified by.

## Tracking

I'll keep a `LEARNING_LOG.md` in the repo. Every working day I'll write 2-3 sentences: what I built, what surprised me, what I don't yet understand.

## What success looks like

End the phases: a deployed running system at a real URL, a clean GitHub repo with tests passing in CI, a learning log full of dated entries, and the ability to talk through any part of the system without notes.
