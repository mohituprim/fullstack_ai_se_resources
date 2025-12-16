Are you familar with server side rendering  
- Yes: render HTML on the server, send it to the client for first paint; improves TTFB and SEO, shifts compute to server; client then hydrates to make it interactive. Use for content-heavy/public pages, avoid for highly dynamic dashboards unless needed.

How dependency injection is different in fast api than traditional system  
- FastAPI uses function parameters with type hints + `Depends` for declarative DI; no container config files. Dependencies can be per-request, cached within request scope, and can yield for teardown. Traditional DI often uses classes/containers configured separately; FastAPI keeps it inline and async-aware.

When fast api could be slower with async  
- If work is CPU-bound (e.g., heavy JSON parsing, ML inference) and starves the event loop. If async code awaits blocking libraries (DB drivers, HTTP clients) without threads, causing serialization. Too many tasks causing context-switch overhead vs a simple threaded sync app.

What happens when we recieves html and css in browser till painting  
- HTML parse -> DOM; CSS download/parse -> CSSOM; combine into render tree; layout; paint; composites layers. JS can block parsing/execution if not deferred/async. Fonts/images may trigger reflow/repaint when loaded.

what is hyderation  
- Taking server-rendered HTML and attaching client-side event listeners/state to make it interactive, reusing existing DOM instead of re-rendering from scratch.

Which project are you most proud of it and why  
- Pick one with measurable impact, e.g., “Built a multi-tenant workflow service that cut onboarding from weeks to days and handled 10x traffic with zero downtime—owned architecture, observability, and rollout.”

How you would rollout new api version in fastapi without writing duplicate model for database changes?  
- Add versioned routers (`/v1`, `/v2`) with shared Pydantic models where possible; evolve models via optional fields and defaults. Use DB migrations to add new columns as nullable, backfill, then enforce. Introduce adapters/transform layers instead of duplicating ORM models. Deprecate old routes with headers and remove after adoption.