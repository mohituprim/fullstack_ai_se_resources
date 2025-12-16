Round 1
- Introduction
- How do you implement multi-tenant architecture
    Multi-tenant architecture: choose per-tenant schema when tenants need isolation and easier export; 
    choose shared schema with tenant_id for simpler ops and many small tenants.
     Use a tenant resolver middleware, scoped DB sessions, row-level security, tenant-aware caches/queues/object storage prefixes, and per-tenant config/feature flags.
- How do you handle millions of records inside flow
Handling millions of records in a flow: paginate/stream (cursor-based), push heavy work to async workers, batch DB writes/reads, add proper indexes, avoid N+1 with joins or prefetch, and use backpressure/reties with idempotent jobs.
- Are you using redis
Redis usage: great for caching hot reads, distributed locks, rate limiting, pub/sub or streams for lightweight queues, and storing session or feature flags with TTL. Use key namespacing per tenant.
- How do you handle flow update
Flow updates: version your flows; store immutable versions and mark active version per tenant. Migrate running instances via compatibility shims or only apply new versions to new runs. Keep schema contracts stable or add adapters.
- How do organize fastapi or django project
Organizing FastAPI/Django: domain/module structure (e.g., api/routes, services/use-cases, repositories, schemas, models, jobs). Keep settings via Pydantic or Django settings modules with env-specific overrides. Separate dependencies, auth, and middleware. Use alembic/migrations in migrations/.
- How do you handle authentication 
Authentication handling: JWT or opaque tokens with short TTL + refresh; store passwords with bcrypt/argon2; enforce MFA/SSO (OIDC/SAML) when possible; per-tenant auth configs; role/permission model checked in services; protect cookies with HttpOnly/SameSite; rate-limit and log auth events.
- How you will secure data from llm
Securing data from LLM: apply data minimization and redaction before sending; PII detection; tenancy-aware access checks; use prompt templates with strict context windows; store prompts/completions with audit trails; consider self-hosted models for sensitive data; encrypt in transit and at rest; allow tenant-level opt-out.
- How do you optimize query in postgress
Optimizing Postgres queries: create the right indexes (including partial and composite), analyze plans with EXPLAIN ANALYZE, avoid SELECT *, batch writes, use connection pooling, tune work_mem/shared_buffers, and vacuum/analyze regularly. Partition large tables by tenant/date if warranted.
- How did you implemented pdf automation
PDF automation implementation: use templating (HTML+CSS with WeasyPrint/wkhtmltopdf) or programmatic libs (ReportLab/PyPDF); separate data mapping from rendering; support async generation via a worker queue; store outputs in object storage with pre-signed URLs; include tests for templates.
- are you comfertable build ci/cd pipeline in github
CI/CD pipeline on GitHub: GitHub Actions with workflows for lint/test/build on PR, security scans (SAST/Dependabot), caching (pip/npm), matrix for versions, and deploy steps (e.g., to AWS via OIDC, Terraform/CDK). Protect main with required checks.
- about aws services
AWS services: typical stack—ECS/Fargate or EKS for services, RDS/Aurora for DB, ElastiCache for Redis, S3 for storage, CloudFront for CDN, SQS/SNS/EventBridge for async, Lambda for event-driven, API Gateway/ALB for ingress, Cognito/SSO for auth, Secrets Manager/SSM Parameter Store for secrets, CloudWatch/X-Ray for observability, WAF/Shield for edge security.
