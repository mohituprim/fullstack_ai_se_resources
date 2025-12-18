## Tecra – Round 1 Notes (Refined with Examples)

### 1. Multi-tenant Architecture

**How I approach it**
- **Shared schema (single DB, `tenant_id` column)**  
  - Pros: simple to manage, good for many small tenants.  
  - Cons: weaker isolation, noisy neighbors.
- **Schema-per-tenant**  
  - Pros: better isolation, easier per-tenant backup/export.  
  - Cons: migrations/ops more complex at high tenant counts.
- **DB-per-tenant**  
  - Pros: strongest isolation; good for large enterprise tenants.  
  - Cons: operational overhead, many connections.

**When to pick what (example answer)**  
> “For a SaaS with thousands of small tenants, I’d start with a shared schema and a `tenant_id` column with strict row-level security. If we onboard a few very large tenants, we can move them to schema-per-tenant or DB-per-tenant for stronger isolation and performance tuning.”

**Implementation example (FastAPI + SQLAlchemy)**
- Tenant resolution middleware:
  - Use `X-Tenant-Id` header / subdomain / JWT claim.
  - Put tenant id into `request.state.tenant_id` or a `ContextVar`.
- DB layer:
  - All queries filter by `tenant_id` (or use Postgres RLS).
- Caching / queues / storage:
  - Prefix keys/paths with tenant id: `f\"{tenant_id}:user:{user_id}\"` or `s3://bucket/{tenant_id}/...`.

```python
from starlette.middleware.base import BaseHTTPMiddleware

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        tenant_id = request.headers.get(\"X-Tenant-Id\")
        request.state.tenant_id = tenant_id
        response = await call_next(request)
        return response
```

---

### 2. Handling Millions of Records in a Flow

**Key points**
- **Stream / paginate**, don’t load all records into memory.
- Use **cursor/keyset pagination**, not only `OFFSET/LIMIT`.
- Move heavy processing to **async workers** (queues).
- **Batch** DB writes/reads and external calls.
- Ensure good **indexes** and avoid N+1 queries.

**Example answer**  
> “For millions of records, I’d never do `SELECT *` and load them all into memory. I’d page or stream them, pushing each batch onto a queue processed by workers. I’d add proper indexes and avoid N+1 by using joins or prefetching.”

**Code sketch – processing in batches**

```python
def process_large_table(conn, batch_size=10_000):
    last_id = 0
    while True:
        rows = conn.execute(
            \"\"\"SELECT id, payload
                   FROM events
                  WHERE id > %s
                  ORDER BY id
                  LIMIT %s\"\"\",\n            (last_id, batch_size),
        ).fetchall()
\n        if not rows:
            break

        for row in rows:
            enqueue_job(row.id, row.payload)  # send to async worker

        last_id = rows[-1].id
```

---

### 3. Redis Usage

**What I’d say I use Redis for**
- Caching hot reads (e.g., user profiles, feature flags).
- Distributed locks (e.g., to ensure one job runs at a time).
- Rate limiting (IP/user/tenant based).
- Pub/sub or streams for lightweight queues.
- Short-lived session storage.

**Example – per-tenant cache key**

```python
import json
import redis

r = redis.Redis(host=\"localhost\", port=6379)

def get_user_profile(user_id, tenant_id):
    key = f\"{tenant_id}:user:{user_id}\"
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    profile = load_user_from_db(user_id, tenant_id)
    r.setex(key, 3600, json.dumps(profile))  # 1 hour TTL
    return profile
```

---

### 4. Handling Flow Updates (Versioning)

**Concept**
- Treat a “flow” (workflow/state machine) as a **versioned definition**.
- Store each version as immutable, and mark one as **active**.

**Answer style**  
> “We version our flows. We store flow definitions with a version number and mark an active version per tenant. Running instances usually complete on their old version, while new runs start on the latest version. That keeps deployments safe without breaking running flows.”

**Sketch**

```sql
CREATE TABLE flows (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  version INT NOT NULL,
  definition JSONB NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT FALSE
);
```

---

### 5. Organizing FastAPI or Django Projects

**FastAPI typical structure**

```text
app/
  main.py
  api/
    routes/
      users.py
      auth.py
  core/
    config.py
    security.py
  services/
    user_service.py
  repositories/
    user_repository.py
  models/
    user.py
  schemas/
    user.py
  migrations/
```

**Example answer (FastAPI)**  
> “I organize FastAPI by domain: `api/routes` for endpoints, `schemas` for Pydantic models, `services` for business logic, `repositories` for DB access, `core` for config/security, and `migrations` for Alembic. Routes stay thin and call services; services call repositories.”

**Django**  
- Separate apps: `users`, `billing`, `projects`, etc.  
- Each app: `models.py`, `views.py` (or `api.py`), `serializers.py`, `urls.py`, `tests.py`.

---

### 6. Authentication Handling

**Key points to mention**
- Passwords: hash with **bcrypt/argon2**.
- Auth: JWT or opaque tokens (short-lived) + refresh tokens.
- Security:
  - HttpOnly/SameSite cookies.
  - Rate limiting and logging for login endpoints.
  - MFA/SSO (OIDC/SAML) for higher security tenants.

**Example answer**  
> “We store passwords with bcrypt, issue short-lived JWTs (or opaque tokens) plus refresh tokens, and keep user sessions in Redis or DB. We protect cookies with HttpOnly/SameSite, rate-limit login attempts, and log auth events for audit.”

---

### 7. Securing Data from LLMs

**What I’d highlight**
- **Data minimization**: only send what’s needed.
- **Redaction/PII detection** before sending text.
- **Tenant-aware access checks**: LLM only sees data the user is allowed to see.
- **Prompt hygiene**: templates, strict context, no raw concatenation of user text around secrets.
- **Auditing**: log prompts/responses (carefully) for security review.
- Use **self-hosted models** or private endpoints for highly sensitive data.

**Example**  
> “Before sending text to an LLM, we run PII detection and redact emails, phone numbers, and IDs. We also enforce tenant + permission checks at the service layer so only allowed data is in the prompt. For highly sensitive tenants we’d prefer a self-hosted or VPC-connected model.”

---

### 8. Optimizing Postgres Queries

**Checklist**
- Indexes: single, composite, partial.
- Use `EXPLAIN ANALYZE` to see real plan.
- Avoid `SELECT *` in hot paths.
- Batch writes, use connection pooling.
- Regular `VACUUM`/`ANALYZE`.
- Partition large tables by tenant/date if needed.

**Example answer**  
> “I use EXPLAIN ANALYZE to see whether Postgres is using indexes or doing seq scans. Then I design composite indexes on the columns used in WHERE and ORDER BY. For big tables, I’d consider partitioning by tenant or date.”

---

### 9. PDF Automation Implementation

**Pattern**
- Data → Template context → Render → PDF → Store.
- Use HTML+CSS → PDF (wkhtmltopdf/WeasyPrint) or direct PDF libs (ReportLab).
- Offload generation to background workers for large batches.

**Example answer**  
> “We used HTML templates rendered with Jinja2 and then wkhtmltopdf to generate PDFs. The API enqueues jobs to a worker, the worker renders the HTML, generates the PDF, stores it in S3, and we keep the URL in the DB.”

---

### 10. Comfortable Building CI/CD in GitHub

**What I’d say**
- Use **GitHub Actions**:
  - On PR: run lint, tests, type checks.
  - On main: build Docker image/artifact and deploy to environment (staging/prod).
- Use caching (pip/npm), matrix builds for versions.
- Use OIDC to deploy to AWS securely (no long-lived keys).
- Protect `main` with required checks.

**Mini example**

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: \"3.11\"
      - run: pip install -r requirements.txt
      - run: pytest
```

---

### 11. AWS Services

**Example answer structure**
- Compute: **ECS/Fargate or EKS** for services, **Lambda** for event-driven tasks.
- Data: **RDS/Aurora** for relational DB, **ElastiCache (Redis)** for caching, **S3** for file storage.
- Networking/Ingress: **API Gateway** or **ALB**, **CloudFront** as CDN.
- Async/Integration: **SQS/SNS/EventBridge** for messaging.
- Auth/Security: **Cognito/SSO**, **Secrets Manager/SSM** for secrets, **WAF/Shield** for edge.
- Observability: **CloudWatch** logs/metrics/alarms, X-Ray or other APM.

**Sample phrasing**  
> “In my previous project we used ECS on Fargate for services, RDS Postgres for the database, ElastiCache Redis for caching, S3 for file storage behind CloudFront, and SQS for async jobs. We managed secrets with Secrets Manager and used CloudWatch for logs and alarms.”

