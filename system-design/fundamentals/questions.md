# Interview Questions for Software Architects

## 1. How do you decide between a monolith, modular monolith, and microservices for a new system?

**Decision Framework:**

**Start with Monolith when:**
- Small team (2-5 developers)
- Limited domain knowledge
- Need to move fast and validate product-market fit
- Simple domain with clear boundaries
- Low traffic/scale requirements initially
- Team lacks distributed systems experience

**Choose Modular Monolith when:**
- Team size: 5-15 developers
- Domain is moderately complex but still manageable
- Need clear module boundaries but want to avoid distributed system complexity
- Want to prepare for future microservices migration
- Single deployment unit is acceptable
- Need better organization than monolith but not full microservices overhead

**Choose Microservices when:**
- Large team (15+ developers) or multiple teams
- Clear bounded contexts (Domain-Driven Design)
- Different scaling requirements per service
- Need independent deployment and technology choices
- High availability requirements (fault isolation)
- Team has distributed systems expertise
- Organization can handle operational complexity

**Key Considerations:**
- Team size and structure (Conway's Law)
- Domain complexity and boundaries
- Operational maturity
- Scale requirements
- Time-to-market constraints
- Long-term maintenance costs

**Anti-pattern:** Starting with microservices "because it's modern" without clear justification.

---

## 2. What are the trade-offs between layered, vertical slice, and hexagonal architectures?

**Layered Architecture (Traditional N-Tier):**
- **Pros:**
  - Simple, familiar structure
  - Clear separation of concerns (Presentation → Business → Data)
  - Easy to understand for junior developers
- **Cons:**
  - Tight coupling between layers
  - Changes ripple across layers
  - Hard to test in isolation
  - Can lead to "anemic domain model"
  - Database becomes the center of the universe

**Vertical Slice Architecture:**
- **Pros:**
  - Features are self-contained (UI → Business Logic → Data)
  - Changes are localized to a slice
  - Better alignment with business features
  - Easier to understand feature flow
  - Reduces coupling between features
- **Cons:**
  - Potential code duplication
  - Requires discipline to maintain boundaries
  - Can be harder to share common logic

**Hexagonal Architecture (Ports & Adapters):**
- **Pros:**
  - Business logic is isolated from infrastructure
  - Easy to test (mock ports/adapters)
  - Technology-agnostic core
  - Flexible: swap databases, UIs, external services
  - Clear dependency direction (inward)
- **Cons:**
  - More abstraction overhead
  - Steeper learning curve
  - Can be over-engineered for simple apps
  - Requires discipline to maintain boundaries

**When to Use:**
- **Layered:** Simple CRUD apps, small teams, rapid prototyping
- **Vertical Slice:** Feature-rich applications, domain-driven design, when features are independent
- **Hexagonal:** Complex business logic, need for testability, multiple integration points, long-term maintainability

---

## 3. How do you apply the Principle of Least Surprises when designing components?

**Core Principle:** Components should behave in ways that users and developers expect, based on conventions, naming, and established patterns.

**Application Strategies:**

1. **Naming Conventions:**
   - Use domain language consistently
   - Follow established patterns (e.g., `get*` returns value, `is*` returns boolean)
   - Avoid abbreviations unless universally understood
   - Method names should clearly indicate side effects

2. **Consistent Interfaces:**
   - Similar operations should have similar signatures
   - Follow language/framework conventions
   - Maintain consistent error handling patterns
   - Use standard return types (e.g., `Optional<T>`, `Result<T, E>`)

3. **Predictable Behavior:**
   - No hidden side effects
   - Immutability where appropriate
   - Fail fast with clear error messages
   - Idempotent operations where expected

4. **Follow Established Patterns:**
   - Use well-known design patterns consistently
   - Follow framework conventions (e.g., REST, GraphQL)
   - Adhere to language idioms

5. **Documentation:**
   - Clear API documentation
   - Examples for common use cases
   - Document any non-obvious behavior

**Example:**
```python
# Surprising (bad)
def process(data):  # What does it return? Does it mutate data?
    ...

# Least surprise (good)
def process_user_data(user_data: UserData) -> ProcessedUserData:
    """Processes user data and returns a new processed instance."""
    ...
```

---

## 4. How do you avoid accidental complexity when scaling a system?

**Accidental Complexity:** Complexity introduced by the solution, not inherent to the problem.

**Strategies:**

1. **Start Simple:**
   - Begin with the simplest solution that works
   - Avoid premature optimization
   - Don't solve problems you don't have yet

2. **Measure Before Optimizing:**
   - Profile and identify actual bottlenecks
   - Use metrics to guide decisions
   - Avoid optimizing based on assumptions

3. **Incremental Complexity:**
   - Add complexity only when needed
   - Refactor when patterns emerge
   - Don't build for hypothetical scale

4. **Use Managed Services:**
   - Leverage cloud services (databases, queues, caches)
   - Reduce operational overhead
   - Focus on business logic

5. **Standard Patterns:**
   - Use proven patterns (circuit breakers, retries, caching)
   - Avoid custom solutions when standard ones exist
   - Learn from industry best practices

6. **Clear Abstractions:**
   - Hide complexity behind simple interfaces
   - Use facades for complex subsystems
   - Document why complexity exists

7. **Team Communication:**
   - Code reviews to catch over-engineering
   - Regular architecture reviews
   - Share knowledge and patterns

**Red Flags:**
- Building distributed systems before needing them
- Custom implementations of standard algorithms
- Over-abstraction without clear benefit
- Solving for 10x scale when current is 1x

---

## 5. How do you choose between synchronous and asynchronous communication?

**Synchronous Communication:**
- **Use when:**
  - Need immediate response/confirmation
  - Request-response pattern is natural
  - Low latency is critical
  - Simple error handling (try/catch)
  - Tight coupling is acceptable
  - Low volume, high-value operations

- **Examples:**
  - User authentication
  - Real-time queries
  - Payment processing (immediate confirmation)
  - API calls between services

**Asynchronous Communication:**
- **Use when:**
  - Operations are long-running
  - Decoupling is important
  - Can tolerate eventual consistency
  - Need to handle bursts/spikes
  - Different services have different processing times
  - Fire-and-forget operations

- **Examples:**
  - Email notifications
  - Image processing
  - Data synchronization
  - Event-driven architectures
  - Background jobs

**Decision Matrix:**

| Factor | Synchronous | Asynchronous |
|--------|------------|--------------|
| Response Time | Immediate | Eventual |
| Coupling | Tight | Loose |
| Error Handling | Simple | Complex (retries, DLQ) |
| Throughput | Limited by slowest | Higher (queues buffer) |
| Complexity | Lower | Higher |
| Consistency | Strong | Eventual |

**Hybrid Approach:**
- Synchronous for critical path, async for everything else
- Request-response with async processing (return job ID)
- Event sourcing with synchronous reads

---

## 6. How do you design idempotent operations for systems with retries?

**Idempotency:** Performing an operation multiple times has the same effect as performing it once.

**Design Patterns:**

1. **Idempotency Keys:**
   - Client generates unique key per operation
   - Server stores key → result mapping
   - Return cached result if key seen before
   ```python
   def process_payment(idempotency_key: str, amount: float):
       if key_exists(idempotency_key):
           return get_cached_result(idempotency_key)
       result = execute_payment(amount)
       store_result(idempotency_key, result)
       return result
   ```

2. **Natural Idempotency:**
   - Use operations that are naturally idempotent
   - `PUT /users/123` (replace) vs `POST /users` (create)
   - Upsert operations (INSERT ... ON CONFLICT)

3. **Version Numbers/ETags:**
   - Include version in update requests
   - Reject if version mismatch (optimistic locking)
   - Prevents lost updates

4. **State Machines:**
   - Operations only valid in certain states
   - Transition guards prevent duplicate processing
   - Example: Order can only be "confirmed" once

5. **Idempotency at Database Level:**
   - Unique constraints
   - Transactions with proper isolation
   - Upsert semantics

**Implementation Considerations:**
- **Storage:** Redis/Memcached for short TTL, database for long-term
- **TTL:** Match idempotency key TTL to operation validity window
- **Scope:** Per-user or global idempotency keys
- **Cleanup:** Expire old keys to prevent storage bloat

**Example:**
```python
class PaymentService:
    def process_payment(self, idempotency_key: str, amount: float):
        # Check if already processed
        cached = self.cache.get(idempotency_key)
        if cached:
            return cached
        
        # Process payment (with database transaction)
        with self.db.transaction():
            payment = self.db.create_payment(amount, idempotency_key)
            self.cache.set(idempotency_key, payment, ttl=3600)
            return payment
```

---

## 7. How would you prevent race conditions in a high-throughput workflow?

**Race Condition:** When outcome depends on timing of concurrent operations.

**Prevention Strategies:**

1. **Database-Level Locking:**
   - **Pessimistic Locking:** `SELECT ... FOR UPDATE`
   - **Optimistic Locking:** Version numbers, compare-and-swap
   - **Unique Constraints:** Prevent duplicate entries
   - **Transactions:** ACID guarantees with proper isolation levels

2. **Distributed Locks:**
   - Redis with SETNX (SET if Not eXists)
   - ZooKeeper/etcd for coordination
   - Database advisory locks
   - **TTL:** Always set expiration to prevent deadlocks

3. **Message Queue Ordering:**
   - Single consumer per partition/topic
   - Partition by entity ID (same ID → same partition)
   - Sequential processing within partition

4. **Idempotency:**
   - Idempotency keys (see Question 6)
   - Natural idempotent operations
   - State machines with guards

5. **Compare-and-Swap (CAS):**
   - Atomic updates with condition checks
   - Redis: `WATCH` + `MULTI` + `EXEC`
   - Database: `UPDATE ... WHERE version = expected_version`

6. **Event Sourcing:**
   - Append-only event log
   - Events are immutable
   - Replay to rebuild state

7. **Saga Pattern:**
   - Compensating transactions
   - Each step is idempotent
   - Can retry safely

**Example - Inventory Deduction:**
```python
def deduct_inventory(item_id: str, quantity: int):
    # Option 1: Pessimistic lock
    with db.transaction():
        item = db.query("SELECT * FROM inventory WHERE id = ? FOR UPDATE", item_id)
        if item.stock >= quantity:
            db.execute("UPDATE inventory SET stock = stock - ? WHERE id = ?", 
                      quantity, item_id)
    
    # Option 2: Optimistic lock with version
    version = get_current_version(item_id)
    updated = db.execute(
        "UPDATE inventory SET stock = stock - ?, version = version + 1 "
        "WHERE id = ? AND version = ? AND stock >= ?",
        quantity, item_id, version, quantity
    )
    if updated == 0:
        raise ConcurrentModificationError()
    
    # Option 3: Atomic operation
    db.execute(
        "UPDATE inventory SET stock = stock - ? WHERE id = ? AND stock >= ?",
        quantity, item_id, quantity
    )
```

**Best Practices:**
- Minimize lock duration
- Use appropriate isolation levels
- Design for failure (timeouts, retries)
- Monitor for deadlocks
- Use idempotency where possible

---

## 8. How do you decide when to use queues, streams, or direct calls?

**Direct Calls (Synchronous):**
- **Use when:**
  - Need immediate response
  - Tight coupling is acceptable
  - Low latency critical
  - Simple request-response
  - Low volume
- **Example:** User authentication, real-time queries

**Message Queues (Point-to-Point):**
- **Use when:**
  - One producer, one consumer per message
  - Need guaranteed delivery
  - Work distribution (load balancing)
  - Decoupling producer and consumer
  - Can tolerate some delay
- **Examples:**
  - Task queues (Celery, Sidekiq)
  - Job processing
  - Email sending
  - Image processing

**Message Streams (Pub/Sub):**
- **Use when:**
  - One producer, multiple consumers
  - Event-driven architecture
  - Need event replay
  - Different consumers process at different rates
  - Event sourcing
- **Examples:**
  - User activity events
  - Order status changes
  - Real-time analytics
  - Audit logs
  - Kafka, RabbitMQ topics

**Decision Matrix:**

| Requirement | Direct Calls | Queues | Streams |
|------------|--------------|--------|--------|
| Latency | Low | Medium | Medium |
| Coupling | Tight | Loose | Loose |
| Consumers | 1 | 1 per message | Multiple |
| Replay | No | No | Yes |
| Ordering | N/A | Per queue | Per partition |
| Throughput | Limited | High | Very High |
| Complexity | Low | Medium | High |

**Hybrid Approaches:**
- **Request-Response over Queue:** Request queue + response queue
- **Streams with Direct Calls:** Critical path synchronous, events async
- **Event Sourcing:** Streams for events, direct calls for queries

**Example Scenarios:**
- **E-commerce Order Processing:**
  - Direct call: Payment processing (immediate confirmation)
  - Queue: Email notifications, inventory updates
  - Stream: Order events for analytics, recommendations

---

## 9. What's the role of sagas in long-running workflows?

**Saga Pattern:** Manages distributed transactions across multiple services using a sequence of local transactions with compensating actions.

**Problem:** Distributed transactions (2PC) are slow, block resources, and don't scale well.

**Solution:** Break transaction into steps, each with a compensating action.

**Types of Sagas:**

1. **Choreography (Event-Driven):**
   - Each service knows what to do next
   - Services publish events
   - Other services react
   - **Pros:** Loose coupling, no central coordinator
   - **Cons:** Hard to track, complex error handling

2. **Orchestration (Centralized):**
   - Central coordinator (orchestrator) manages workflow
   - Orchestrator calls services in sequence
   - **Pros:** Easy to understand, centralized error handling
   - **Cons:** Single point of failure, tighter coupling

**Example - Order Processing Saga:**

**Choreography:**
```
Order Service → OrderCreated event
  ↓
Inventory Service → ReserveInventory → InventoryReserved event
  ↓
Payment Service → ChargeCard → PaymentProcessed event
  ↓
Shipping Service → CreateShipment → OrderCompleted event
```

**Orchestration:**
```
Orchestrator:
  1. Call Order Service → Create Order
  2. Call Inventory Service → Reserve Inventory
  3. Call Payment Service → Charge Card
  4. Call Shipping Service → Create Shipment
```

**Compensating Actions:**
- If payment fails after inventory reserved → Release inventory
- If shipping fails after payment → Refund payment
- Each step has a corresponding undo operation

**Key Properties:**
- **Idempotent:** Steps can be retried safely
- **Compensatable:** Each step has a compensating action
- **Observable:** Track saga state for debugging
- **Timeout Handling:** Set timeouts for each step

**When to Use:**
- Long-running business processes
- Multiple services involved
- Need eventual consistency
- Cannot use distributed transactions

**Example Implementation:**
```python
class OrderSaga:
    def execute(self, order_data):
        try:
            order = self.order_service.create(order_data)
            inventory = self.inventory_service.reserve(order.items)
            payment = self.payment_service.charge(order.total)
            shipment = self.shipping_service.create(order.id)
            return {"status": "completed", "order_id": order.id}
        except PaymentFailed:
            self.inventory_service.release(inventory.id)  # Compensate
            self.order_service.cancel(order.id)
            raise
        except ShippingFailed:
            self.payment_service.refund(payment.id)  # Compensate
            self.inventory_service.release(inventory.id)
            self.order_service.cancel(order.id)
            raise
```

---

## 10. How do you design for exactly-once or effectively-once processing guarantees?

**Processing Semantics:**
- **At-least-once:** Messages may be processed multiple times (need idempotency)
- **At-most-once:** Messages may be lost (no retries)
- **Exactly-once:** Each message processed exactly once (ideal but hard)
- **Effectively-once:** Achieved through idempotency (practical approach)

**Exactly-Once Challenges:**
- Network failures
- Process crashes
- Retries
- Duplicate messages

**Design Strategies:**

1. **Idempotent Processing:**
   - Make operations idempotent (see Question 6)
   - Use idempotency keys
   - Natural idempotent operations (UPSERT, SET)
   - **This is the practical approach (effectively-once)**

2. **Transactional Outbox Pattern:**
   - Write to database and outbox in same transaction
   - Separate process reads outbox and publishes events
   - Prevents lost messages
   - Still need idempotency for duplicates

3. **Deduplication:**
   - Track processed message IDs
   - Check before processing
   - Store in fast lookup (Redis)
   - TTL based on processing window

4. **Kafka Exactly-Once Semantics:**
   - Idempotent producers (deduplicate by producer ID + sequence)
   - Transactional producers (atomic writes to multiple partitions)
   - Consumer: read committed, idempotent processing

5. **Database Transactions:**
   - Process message in transaction
   - Commit only after successful processing
   - On failure, message remains in queue
   - **Risk:** Poison messages block processing

6. **Two-Phase Processing:**
   - **Phase 1:** Validate and prepare (idempotent)
   - **Phase 2:** Execute (idempotent)
   - Can retry either phase safely

**Example - Effectively-Once Processing:**
```python
class MessageProcessor:
    def process(self, message_id: str, payload: dict):
        # Check if already processed
        if self.processed_cache.exists(message_id):
            return self.processed_cache.get(message_id)
        
        # Process idempotently
        try:
            result = self.process_payment(
                idempotency_key=message_id,
                amount=payload['amount']
            )
            
            # Mark as processed
            self.processed_cache.set(message_id, result, ttl=86400)
            return result
        except DuplicatePaymentError:
            # Already processed (race condition)
            return self.processed_cache.get(message_id)
```

**Best Practices:**
- **Prefer effectively-once** over exactly-once (more practical)
- Use idempotency keys derived from message content
- Store processing state (Redis, database)
- Set appropriate TTLs
- Monitor for duplicate processing
- Use idempotent operations everywhere

**Trade-offs:**
- Exactly-once: Complex, performance overhead
- Effectively-once: Simpler, requires idempotency design
- At-least-once: Simplest, requires idempotency

---

## 11. How do you handle partial failures in distributed systems?

**Partial Failure:** Some components fail while others continue operating.

**Failure Types:**
- Network partitions
- Service crashes
- Slow services (timeouts)
- Database failures
- External API failures

**Handling Strategies:**

1. **Circuit Breaker Pattern:**
   - Monitor failure rate
   - Open circuit after threshold
   - Fail fast when open
   - Half-open state for recovery testing
   - **Prevents cascading failures**

2. **Retries with Exponential Backoff:**
   - Retry transient failures
   - Exponential backoff to avoid thundering herd
   - Jitter to spread retries
   - Max retry limit
   - **Only for idempotent operations**

3. **Timeouts:**
   - Set reasonable timeouts
   - Fail fast, don't wait indefinitely
   - Different timeouts for different operations
   - **Prevent resource exhaustion**

4. **Bulkheads:**
   - Isolate resources (thread pools, connections)
   - Failure in one area doesn't affect others
   - **Prevent cascading failures**

5. **Graceful Degradation:**
   - Return cached/stale data when service down
   - Disable non-critical features
   - Show partial results
   - **Maintain user experience**

6. **Health Checks:**
   - Monitor service health
   - Remove unhealthy instances from load balancer
   - Automatic recovery when healthy
   - **Enable self-healing**

7. **Fallback Mechanisms:**
   - Default values
   - Cached responses
   - Alternative data sources
   - **Provide continuity**

8. **Dead Letter Queues (DLQ):**
   - Move failed messages to DLQ
   - Manual inspection and retry
   - **Prevent poison messages**

9. **Saga Pattern:**
   - Compensating transactions
   - Rollback on partial failure
   - **Maintain consistency**

**Example Implementation:**
```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def call_external_api(data):
    try:
        response = requests.post(
            "https://external-api.com/process",
            json=data,
            timeout=5  # Fail fast
        )
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        # Retry with exponential backoff
        raise RetryableError()
    except requests.HTTPError as e:
        if e.status_code >= 500:
            raise RetryableError()  # Server error, retry
        else:
            raise PermanentError()  # Client error, don't retry

def process_with_fallback(data):
    try:
        return call_external_api(data)
    except CircuitBreakerOpen:
        # Circuit open, use fallback
        return get_cached_response(data) or default_response()
    except PermanentError:
        # Don't retry, log and alert
        logger.error(f"Permanent error: {e}")
        raise
```

**Best Practices:**
- **Fail fast:** Don't wait indefinitely
- **Retry wisely:** Only idempotent operations, with limits
- **Monitor everything:** Metrics, logs, alerts
- **Test failures:** Chaos engineering
- **Design for failure:** Assume everything will fail
- **Isolate failures:** Bulkheads, circuit breakers

---

## 12. What patterns help maintain consistency across multiple services?

**Challenge:** Maintaining data consistency without distributed transactions.

**Patterns:**

1. **Saga Pattern:**
   - Sequence of local transactions
   - Compensating actions for rollback
   - Eventual consistency
   - **Best for:** Long-running workflows

2. **Event Sourcing:**
   - Store events, not current state
   - Replay events to rebuild state
   - Events are source of truth
   - **Best for:** Audit trails, time travel

3. **CQRS (Command Query Responsibility Segregation):**
   - Separate read and write models
   - Write model: commands, events
   - Read model: optimized queries
   - **Best for:** Different read/write patterns

4. **Transactional Outbox:**
   - Write to database and outbox in transaction
   - Separate process publishes events
   - Ensures at-least-once delivery
   - **Best for:** Reliable event publishing

5. **Two-Phase Commit (2PC):**
   - Coordinator manages commit
   - Prepare phase, then commit/abort
   - **Pros:** Strong consistency
   - **Cons:** Slow, blocks, doesn't scale
   - **Avoid in:** High-throughput systems

6. **Compensating Transactions:**
   - Each operation has compensating action
   - Rollback by executing compensations
   - Part of Saga pattern
   - **Best for:** Business operations with undo

7. **Eventual Consistency with Conflict Resolution:**
   - Accept temporary inconsistency
   - Resolve conflicts (last-write-wins, merge, CRDTs)
   - **Best for:** High availability, partition tolerance

8. **Distributed Locks:**
   - Coordinate access to shared resources
   - Redis, ZooKeeper, etcd
   - **Best for:** Critical sections, leader election

9. **Idempotency:**
   - Operations can be safely retried
   - Prevents duplicate processing
   - **Best for:** Retry scenarios

**Example - Order Processing with Saga:**
```python
class OrderSaga:
    def process_order(self, order_data):
        # Step 1: Create order (idempotent)
        order = self.order_service.create(order_data)
        
        # Step 2: Reserve inventory (idempotent)
        reservation = self.inventory_service.reserve(
            order.items, 
            idempotency_key=f"order-{order.id}"
        )
        
        # Step 3: Charge payment (idempotent)
        payment = self.payment_service.charge(
            order.total,
            idempotency_key=f"order-{order.id}"
        )
        
        # If any step fails, compensate previous steps
        try:
            shipment = self.shipping_service.create(order.id)
        except ShippingError:
            # Compensate
            self.payment_service.refund(payment.id)
            self.inventory_service.release(reservation.id)
            self.order_service.cancel(order.id)
            raise
```

**Choosing a Pattern:**

| Requirement | Pattern |
|------------|---------|
| Strong consistency | 2PC (if acceptable performance) |
| Long workflows | Saga |
| Audit trail | Event Sourcing |
| High throughput | Eventual consistency |
| Read optimization | CQRS |
| Reliable events | Transactional Outbox |

**Best Practices:**
- **Prefer eventual consistency** where possible
- Use **idempotency** everywhere
- **Design for failure** (compensating actions)
- **Monitor consistency** (eventual consistency monitors)
- **Document consistency guarantees** (strong vs eventual)

---

## 13. How do you design a resilient system that survives external dependency failures?

**Resilience:** System's ability to handle and recover from failures.

**Design Strategies:**

1. **Circuit Breaker:**
   - Open circuit after failure threshold
   - Fail fast when open
   - Half-open for recovery testing
   - **Prevents cascading failures**

2. **Retries with Backoff:**
   - Exponential backoff + jitter
   - Max retry limit
   - Only for idempotent operations
   - **Handle transient failures**

3. **Timeouts:**
   - Set reasonable timeouts
   - Fail fast, don't hang
   - **Prevent resource exhaustion**

4. **Fallbacks:**
   - Cached responses
   - Default values
   - Alternative data sources
   - **Maintain functionality**

5. **Bulkheads:**
   - Isolate resources per dependency
   - Thread pools, connection pools
   - **Prevent one failure from affecting others**

6. **Health Checks:**
   - Monitor dependency health
   - Remove unhealthy instances
   - Automatic recovery
   - **Enable self-healing**

7. **Rate Limiting:**
   - Protect dependencies from overload
   - Client-side rate limiting
   - **Prevent dependency failures**

8. **Caching:**
   - Cache dependency responses
   - Serve stale data when dependency down
   - TTL-based invalidation
   - **Reduce dependency load**

9. **Async Processing:**
   - Queue requests to dependencies
   - Process asynchronously
   - **Decouple from dependency availability**

10. **Multiple Providers:**
    - Fallback to alternative providers
    - Load balance across providers
    - **Reduce single point of failure**

**Example Implementation:**
```python
from circuitbreaker import circuit
import time
import random

class ResilientExternalService:
    def __init__(self):
        self.cache = {}
        self.circuit_open = False
        self.failure_count = 0
    
    @circuit(failure_threshold=5, recovery_timeout=60)
    def call_external_api(self, endpoint, data, use_cache=True):
        # Check cache first
        cache_key = f"{endpoint}:{hash(str(data))}"
        if use_cache and cache_key in self.cache:
            cached_response, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 300:  # 5 min TTL
                return cached_response
        
        # Call with timeout and retries
        for attempt in range(3):
            try:
                response = requests.post(
                    endpoint,
                    json=data,
                    timeout=5,
                    headers={"X-Idempotency-Key": str(uuid.uuid4())}
                )
                response.raise_for_status()
                
                # Cache successful response
                self.cache[cache_key] = (response.json(), time.time())
                self.failure_count = 0
                return response.json()
                
            except requests.Timeout:
                if attempt < 2:
                    time.sleep(2 ** attempt + random.uniform(0, 1))  # Backoff + jitter
                    continue
                raise
            except requests.HTTPError as e:
                if e.status_code >= 500 and attempt < 2:
                    time.sleep(2 ** attempt + random.uniform(0, 1))
                    continue
                raise
    
    def call_with_fallback(self, endpoint, data, fallback_value):
        try:
            return self.call_external_api(endpoint, data)
        except (CircuitBreakerOpen, requests.RequestException):
            # Return fallback or cached value
            return fallback_value or self.get_cached_value(endpoint, data)
```

**Best Practices:**
- **Assume dependencies will fail**
- **Fail fast** with timeouts
- **Degrade gracefully** with fallbacks
- **Monitor everything** (circuit states, retry rates)
- **Test failure scenarios** (chaos engineering)
- **Document fallback behavior**

---

## 14. What's your approach to detecting and isolating slow services?

**Detection Strategies:**

1. **Metrics & Monitoring:**
   - **Latency percentiles** (p50, p95, p99, p999)
   - **Request rate** and **error rate**
   - **Response time** distribution
   - **Time-series databases** (Prometheus, InfluxDB)
   - **Dashboards** (Grafana)

2. **Distributed Tracing:**
   - **OpenTracing/OpenTelemetry**
   - Trace requests across services
   - Identify slow spans
   - **Pinpoint bottlenecks**

3. **Health Checks:**
   - **Liveness probes:** Is service running?
   - **Readiness probes:** Is service ready?
   - **Startup probes:** Is service started?
   - **Response time thresholds**

4. **Synthetic Monitoring:**
   - **Canary deployments**
   - **A/B testing** with performance metrics
   - **Load testing** before production

5. **Alerting:**
   - **SLA violations** (p95 > threshold)
   - **Error rate spikes**
   - **Anomaly detection** (sudden latency increase)

**Isolation Strategies:**

1. **Circuit Breaker:**
   - Open circuit when latency exceeds threshold
   - Fail fast, don't wait
   - **Prevent cascading slowness**

2. **Timeouts:**
   - Set per-service timeouts
   - Fail fast on timeout
   - **Don't let slow service block others**

3. **Bulkheads:**
   - **Separate thread pools** per service
   - **Connection pools** per service
   - **Isolate resources**
   - **One slow service doesn't block others**

4. **Load Balancer Health Checks:**
   - Remove slow instances from rotation
   - Automatic recovery when healthy
   - **Traffic routing**

5. **Rate Limiting:**
   - **Protect slow services** from overload
   - **Client-side rate limiting**
   - **Queue requests** if needed

6. **Service Mesh:**
   - **Automatic retries** with timeouts
   - **Circuit breaking**
   - **Load balancing**
   - **Observability** (metrics, tracing)

**Example Implementation:**
```python
import time
from prometheus_client import Histogram, Counter

# Metrics
request_duration = Histogram('http_request_duration_seconds', 'Request duration')
request_errors = Counter('http_request_errors_total', 'Request errors')

class ServiceMonitor:
    def __init__(self, service_name, timeout=5):
        self.service_name = service_name
        self.timeout = timeout
        self.circuit_open = False
        self.slow_request_count = 0
    
    def call_service(self, func, *args, **kwargs):
        start_time = time.time()
        
        try:
            with request_duration.time():
                result = func(*args, **kwargs)
            
            duration = time.time() - start_time
            
            # Track slow requests
            if duration > self.timeout * 0.8:  # 80% of timeout
                self.slow_request_count += 1
                logger.warning(f"Slow request to {self.service_name}: {duration}s")
            
            # Reset on success
            if duration < self.timeout * 0.5:
                self.slow_request_count = 0
                self.circuit_open = False
            
            return result
            
        except TimeoutError:
            request_errors.inc()
            self.slow_request_count += 1
            
            if self.slow_request_count > 5:
                self.circuit_open = True
                logger.error(f"Circuit opened for {self.service_name}")
            
            raise
```

**Best Practices:**
- **Monitor percentiles**, not just averages
- **Set SLAs** and alert on violations
- **Use distributed tracing** to find bottlenecks
- **Implement circuit breakers** with latency thresholds
- **Isolate resources** with bulkheads
- **Fail fast** with timeouts
- **Automate remediation** where possible

---

## 15. How do you design caching layers (L1/L2) to avoid stale data and thundering herds?

**Cache Layers:**
- **L1 Cache:** Fast, small (CPU cache, in-memory)
- **L2 Cache:** Slower, larger (Redis, Memcached)
- **L3:** Database/disk

**Stale Data Prevention:**

1. **TTL (Time-To-Live):**
   - Set appropriate expiration times
   - Balance freshness vs performance
   - **Simple but may serve stale data**

2. **Cache Invalidation:**
   - **Write-through:** Update cache on write
   - **Write-behind:** Update cache asynchronously
   - **Invalidate on update:** Delete cache entry
   - **Event-driven invalidation**

3. **Versioning:**
   - Include version in cache key
   - Invalidate by incrementing version
   - **Precise invalidation**

4. **Cache-Aside Pattern:**
   - Application manages cache
   - Read: Check cache → DB → Update cache
   - Write: Update DB → Invalidate cache
   - **Most common pattern**

5. **Read-Through Pattern:**
   - Cache library handles reads
   - Automatically fetches from DB on miss
   - **Simpler application code**

**Thundering Herd Prevention:**

**Problem:** Many requests miss cache simultaneously, all hit database.

**Solutions:**

1. **Locking:**
   - **Distributed lock** (Redis SETNX)
   - First request acquires lock, fetches data
   - Other requests wait or get stale data
   - **Prevents duplicate fetches**

2. **Probabilistic Early Expiration:**
   - Expire cache slightly before TTL
   - Spread refreshes over time
   - **Reduce simultaneous misses**

3. **Background Refresh:**
   - Refresh cache before expiration
   - Serve stale data during refresh
   - **Always have data available**

4. **Semaphore/Queue:**
   - Limit concurrent database queries
   - Queue requests if limit reached
   - **Control load**

5. **Stale-While-Revalidate:**
   - Serve stale data immediately
   - Refresh in background
   - **Best user experience**

**Example Implementation:**
```python
import redis
import time
import threading
from functools import wraps

class CacheManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.local_cache = {}  # L1 cache
        self.locks = {}
    
    def get_with_fallback(self, key, fetch_func, ttl=300, stale_ttl=600):
        # L1: Check local cache
        if key in self.local_cache:
            data, timestamp = self.local_cache[key]
            if time.time() - timestamp < ttl:
                return data
        
        # L2: Check Redis
        cached = self.redis.get(key)
        if cached:
            data = json.loads(cached)
            # Populate L1
            self.local_cache[key] = (data, time.time())
            return data
        
        # Cache miss - prevent thundering herd
        lock_key = f"lock:{key}"
        lock_acquired = self.redis.set(lock_key, "1", nx=True, ex=10)
        
        if lock_acquired:
            # This request fetches data
            try:
                data = fetch_func()
                # Store in both caches
                self.redis.setex(key, stale_ttl, json.dumps(data))
                self.local_cache[key] = (data, time.time())
                return data
            finally:
                self.redis.delete(lock_key)
        else:
            # Another request is fetching, wait briefly
            time.sleep(0.1)
            # Retry or return stale data
            stale = self.redis.get(key)
            if stale:
                return json.loads(stale)
            # Last resort: fetch directly (should be rare)
            return fetch_func()
    
    def invalidate(self, key):
        """Invalidate cache on update"""
        self.local_cache.pop(key, None)
        self.redis.delete(key)
```

**Best Practices:**
- **Use multi-level caching** (L1 + L2)
- **Set appropriate TTLs** (balance freshness vs hits)
- **Implement locking** to prevent thundering herd
- **Invalidate on writes** (cache-aside pattern)
- **Monitor cache hit rates**
- **Use stale-while-revalidate** for better UX
- **Version cache keys** for precise invalidation

---

## 16. What are the signals that a system needs vertical scaling vs horizontal scaling?

**Vertical Scaling (Scale Up):**
- Add more resources to existing machine (CPU, RAM, disk)
- **Easier, but limited by hardware**

**Horizontal Scaling (Scale Out):**
- Add more machines/instances
- **More complex, but unlimited**

**Signals for Vertical Scaling:**

1. **Single Resource Bottleneck:**
   - CPU at 100% on single machine
   - Memory exhausted
   - Disk I/O saturated
   - **One machine can handle more**

2. **Stateful Applications:**
   - In-memory state
   - Local file storage
   - **Hard to distribute**

3. **Low Traffic:**
   - Current machine underutilized
   - **Cheaper to scale up**

4. **Licensing Costs:**
   - Per-instance licensing
   - **Fewer instances = lower cost**

5. **Simple Architecture:**
   - Monolith
   - **Easier to scale up than refactor**

6. **Database (Sometimes):**
   - Single database instance
   - **Vertical scaling can help**

**Signals for Horizontal Scaling:**

1. **High Availability Required:**
   - Need redundancy
   - **Multiple instances for failover**

2. **Traffic Growth:**
   - Beyond single machine capacity
   - **Need more machines**

3. **Geographic Distribution:**
   - Users in different regions
   - **Deploy closer to users**

4. **Stateless Services:**
   - Easy to replicate
   - **Horizontal scaling is natural**

5. **Cost Efficiency:**
   - Smaller instances often cheaper
   - **Better resource utilization**

6. **Elasticity:**
   - Variable traffic (peak hours)
   - **Auto-scaling**

7. **Microservices:**
   - Independent services
   - **Scale services independently**

**Decision Matrix:**

| Factor | Vertical | Horizontal |
|--------|----------|------------|
| Cost (low traffic) | Lower | Higher |
| Cost (high traffic) | Higher | Lower |
| Complexity | Lower | Higher |
| Limit | Hardware max | Unlimited |
| Availability | Single point of failure | High availability |
| Elasticity | Limited | High |
| Stateful apps | Easier | Harder |

**Hybrid Approach:**
- **Vertical scaling** for databases (initially)
- **Horizontal scaling** for application servers
- **Both** as needed

**Example Scenarios:**

**Vertical Scaling:**
- Small startup, single server, CPU bottleneck → Upgrade CPU/RAM
- Database with high memory needs → Larger instance
- Monolith with stateful sessions → Scale up

**Horizontal Scaling:**
- Web application with stateless API → Add more instances
- High traffic e-commerce → Load balancer + multiple app servers
- Microservices architecture → Scale services independently

**Best Practices:**
- **Start with vertical** if simple and low traffic
- **Plan for horizontal** from the start (stateless design)
- **Monitor metrics** to guide decisions
- **Consider cost** vs complexity trade-off
- **Design for both** (cloud instances can scale both ways)

---

## 17. How do you design read-heavy workloads for maximum throughput?

**Read-Heavy Workload Characteristics:**
- Many reads, few writes
- Examples: News sites, blogs, product catalogs, analytics dashboards

**Design Strategies:**

1. **Caching:**
   - **Multi-level caching** (L1: application, L2: Redis/Memcached)
   - **CDN** for static content
   - **Cache-aside pattern**
   - **Cache frequently accessed data**
   - **Long TTLs** for relatively static data

2. **Read Replicas:**
   - **Database read replicas**
   - Distribute read load
   - **Write to primary, read from replicas**
   - **Geographic distribution** for lower latency

3. **CQRS (Command Query Responsibility Segregation):**
   - **Separate read and write models**
   - **Optimized read models** (denormalized, materialized views)
   - **Event sourcing** for writes, optimized queries for reads

4. **Materialized Views:**
   - **Pre-computed query results**
   - **Refresh periodically** or on events
   - **Fast reads, slower writes**

5. **Denormalization:**
   - **Duplicate data** for faster reads
   - **Trade storage for read performance**
   - **Keep in sync** via events or triggers

6. **Connection Pooling:**
   - **Reuse database connections**
   - **Reduce connection overhead**
   - **Optimize pool size**

7. **Query Optimization:**
   - **Indexes** on frequently queried columns
   - **Composite indexes** for common query patterns
   - **Avoid N+1 queries**
   - **Use pagination**

8. **Content Delivery Network (CDN):**
   - **Cache static content** at edge
   - **Reduce origin server load**
   - **Lower latency** for users

9. **Sharding (Read):**
   - **Partition data** across shards
   - **Route reads to appropriate shard**
   - **Parallel reads**

10. **Async Processing:**
    - **Pre-compute** expensive queries
    - **Background jobs** for aggregations
    - **Serve pre-computed results**

**Example Architecture:**
```
User Request
    ↓
CDN (static assets)
    ↓
Load Balancer
    ↓
Application Servers (with L1 cache)
    ↓
Redis/Memcached (L2 cache)
    ↓
Read Replicas (if cache miss)
    ↓
Primary Database (writes only)
```

**Example Implementation:**
```python
class ReadOptimizedService:
    def __init__(self):
        self.cache = RedisCache()
        self.read_db = ReadReplicaConnection()
        self.write_db = PrimaryConnection()
    
    def get_product(self, product_id: str):
        # L1: Check cache
        cached = self.cache.get(f"product:{product_id}")
        if cached:
            return json.loads(cached)
        
        # L2: Read from replica
        product = self.read_db.query(
            "SELECT * FROM products WHERE id = ?",
            product_id
        )
        
        # Cache for future reads
        self.cache.setex(
            f"product:{product_id}",
            3600,  # 1 hour TTL
            json.dumps(product)
        )
        
        return product
    
    def update_product(self, product_id: str, data: dict):
        # Write to primary
        self.write_db.execute(
            "UPDATE products SET ... WHERE id = ?",
            product_id, data
        )
        
        # Invalidate cache
        self.cache.delete(f"product:{product_id}")
        
        # Optionally: Update cache with new data
        # self.cache.setex(f"product:{product_id}", 3600, json.dumps(updated_product))
```

**Best Practices:**
- **Cache aggressively** for read-heavy workloads
- **Use read replicas** to distribute load
- **Optimize queries** with proper indexes
- **Denormalize** where it makes sense
- **Use CDN** for static content
- **Monitor cache hit rates** and adjust TTLs
- **Pre-compute** expensive aggregations

---

## 18. What patterns help reduce database load without harming consistency?

**Problem:** Database is a bottleneck, but we need to maintain data consistency.

**Patterns:**

1. **Caching:**
   - **Cache read results** (Redis, Memcached)
   - **Cache-aside pattern:** App manages cache
   - **Read-through pattern:** Cache library handles it
   - **Write-through:** Update cache on write
   - **Trade-off:** Potential stale data (acceptable for some use cases)

2. **Read Replicas:**
   - **Distribute read load** across replicas
   - **Write to primary, read from replicas**
   - **Eventual consistency** (replication lag)
   - **Acceptable for:** Read-heavy workloads, non-critical reads

3. **Materialized Views:**
   - **Pre-computed query results**
   - **Refresh on schedule** or events
   - **Fast reads, slower writes**
   - **Maintains consistency** (eventual)

4. **Denormalization:**
   - **Duplicate data** for faster reads
   - **Update all copies** on write
   - **Trade storage for performance**
   - **Maintain consistency** via transactions or events

5. **Query Result Caching:**
   - **Cache query results** with appropriate keys
   - **Invalidate on data changes**
   - **Reduce repeated queries**

6. **Batch Operations:**
   - **Batch reads** (IN queries)
   - **Batch writes** (bulk inserts)
   - **Reduce round trips**

7. **Pagination:**
   - **Limit result sets**
   - **Cursor-based pagination** (more efficient than offset)
   - **Reduce data transfer**

8. **Connection Pooling:**
   - **Reuse connections**
   - **Reduce connection overhead**
   - **Optimize pool size**

9. **Write Optimization:**
   - **Batch writes**
   - **Async writes** for non-critical data
   - **Write-behind caching**

10. **Event Sourcing + CQRS:**
    - **Separate read and write models**
    - **Optimized read models**
    - **Eventual consistency**

**Consistency Levels:**

- **Strong Consistency:** All reads see latest write (primary database)
- **Eventual Consistency:** Reads may see stale data (replicas, caches)
- **Read-Your-Writes:** User sees their own writes immediately

**Example Implementation:**
```python
class DatabaseOptimizer:
    def __init__(self):
        self.cache = RedisCache()
        self.primary_db = PrimaryDB()
        self.read_replica = ReadReplicaDB()
    
    def get_user(self, user_id: str, require_fresh=False):
        """Get user with caching and read replica"""
        if not require_fresh:
            # Check cache first
            cached = self.cache.get(f"user:{user_id}")
            if cached:
                return json.loads(cached)
        
        # Read from replica (eventual consistency OK)
        user = self.read_replica.query(
            "SELECT * FROM users WHERE id = ?", user_id
        )
        
        # Cache result
        self.cache.setex(f"user:{user_id}", 300, json.dumps(user))
        return user
    
    def update_user(self, user_id: str, data: dict):
        """Update with cache invalidation"""
        # Write to primary (strong consistency)
        self.primary_db.execute(
            "UPDATE users SET ... WHERE id = ?", user_id, data
        )
        
        # Invalidate cache
        self.cache.delete(f"user:{user_id}")
        
        # Optionally: Update cache with new data
        updated_user = self.get_user(user_id, require_fresh=True)
        self.cache.setex(f"user:{user_id}", 300, json.dumps(updated_user))
    
    def batch_get_users(self, user_ids: list):
        """Batch read to reduce queries"""
        # Check cache first
        cached_users = {}
        uncached_ids = []
        
        for user_id in user_ids:
            cached = self.cache.get(f"user:{user_id}")
            if cached:
                cached_users[user_id] = json.loads(cached)
            else:
                uncached_ids.append(user_id)
        
        # Batch query for uncached
        if uncached_ids:
            users = self.read_replica.query(
                "SELECT * FROM users WHERE id IN (?)", uncached_ids
            )
            for user in users:
                cached_users[user['id']] = user
                self.cache.setex(f"user:{user['id']}", 300, json.dumps(user))
        
        return [cached_users[uid] for uid in user_ids]
```

**Best Practices:**
- **Use caching** for frequently accessed, relatively static data
- **Read replicas** for read-heavy workloads
- **Invalidate cache** on writes to maintain freshness
- **Accept eventual consistency** where appropriate
- **Monitor replication lag** for read replicas
- **Use strong consistency** only when necessary
- **Batch operations** to reduce round trips

---

## 19. How do you approach hot partition problems?

**Hot Partition:** One partition receives significantly more traffic than others, causing bottlenecks.

**Causes:**
- Skewed data distribution
- Popular entities (celebrity accounts, trending items)
- Time-based partitioning (current day/hour)
- Poor partition key selection

**Solutions:**

1. **Better Partition Key Selection:**
   - **Distribute load evenly**
   - **Avoid time-based keys** (unless necessary)
   - **Use composite keys** (user_id + timestamp)
   - **Hash-based partitioning** for even distribution

2. **Salting:**
   - **Add random suffix** to partition key
   - **Distribute across multiple partitions**
   - **Example:** `user_id:123` → `user_id:123:0`, `user_id:123:1`
   - **Trade-off:** Need to query multiple partitions

3. **Caching:**
   - **Cache hot partition data**
   - **Reduce database load**
   - **CDN for static content**

4. **Read Replicas:**
   - **Distribute read load**
   - **Multiple replicas for hot partitions**

5. **Throttling/Rate Limiting:**
   - **Limit requests** to hot partitions
   - **Queue requests** if needed
   - **Protect from overload**

6. **Pre-partitioning:**
   - **Pre-split popular entities**
   - **Distribute across partitions** proactively

7. **Dynamic Rebalancing:**
   - **Monitor partition load**
   - **Automatically split hot partitions**
   - **Rebalance data**

8. **Separate Hot Data:**
   - **Separate storage** for hot data
   - **Different scaling strategy**
   - **Example:** Hot items in Redis, others in database

**Example - Hot User Problem:**
```python
class HotPartitionHandler:
    def __init__(self):
        self.cache = RedisCache()
        self.db_shards = [DBShard(i) for i in range(10)]
        self.hot_user_cache = {}
    
    def get_shard(self, user_id: str):
        """Distribute users across shards"""
        # Hash-based sharding
        shard_index = hash(user_id) % len(self.db_shards)
        return self.db_shards[shard_index]
    
    def get_user_with_salting(self, user_id: str):
        """Handle hot users with salting"""
        # Check if hot user (high traffic)
        if self.is_hot_user(user_id):
            # Query all salt partitions
            user_data = {}
            for salt in range(3):  # 3 salt partitions
                salted_key = f"{user_id}:{salt}"
                shard = self.get_shard(salted_key)
                data = shard.get_user(salted_key)
                if data:
                    user_data.update(data)
            return user_data
        else:
            # Normal user, single partition
            shard = self.get_shard(user_id)
            return shard.get_user(user_id)
    
    def is_hot_user(self, user_id: str):
        """Detect hot users based on request rate"""
        request_count = self.cache.incr(f"requests:{user_id}", ex=60)
        return request_count > 1000  # Threshold
    
    def handle_hot_partition(self, partition_key: str):
        """Mitigate hot partition"""
        # 1. Cache aggressively
        cached = self.cache.get(f"hot:{partition_key}")
        if cached:
            return json.loads(cached)
        
        # 2. Throttle if needed
        if self.get_request_rate(partition_key) > threshold:
            raise RateLimitError("Partition overloaded")
        
        # 3. Use read replica
        data = self.read_replica.get(partition_key)
        
        # 4. Cache result
        self.cache.setex(f"hot:{partition_key}", 60, json.dumps(data))
        return data
```

**Best Practices:**
- **Choose partition keys** that distribute evenly
- **Monitor partition load** and detect hot partitions
- **Use salting** for known hot entities
- **Cache hot data** aggressively
- **Throttle** if necessary to protect system
- **Design for rebalancing** (can split partitions)
- **Separate hot and cold data** if possible

---

## 20. How do you handle high-volume write workloads?

**High-Volume Write Challenges:**
- Database write bottlenecks
- Lock contention
- Replication lag
- Disk I/O saturation

**Strategies:**

1. **Batch Writes:**
   - **Group multiple writes** into single transaction
   - **Reduce round trips**
   - **Example:** Bulk inserts instead of individual inserts

2. **Async Writes:**
   - **Queue writes** for async processing
   - **Return immediately** to user
   - **Process in background**
   - **Trade-off:** Eventual consistency

3. **Write-Behind Caching:**
   - **Write to cache first**
   - **Batch flush to database**
   - **Reduce database load**

4. **Sharding:**
   - **Partition data** across multiple databases
   - **Distribute write load**
   - **Horizontal scaling**

5. **Write-Optimized Storage:**
   - **Append-only logs** (write-optimized)
   - **LSM trees** (Log-Structured Merge trees)
   - **Columnar storage** for analytics

6. **Connection Pooling:**
   - **Reuse connections**
   - **Reduce connection overhead**

7. **Optimize Transactions:**
   - **Minimize transaction duration**
   - **Reduce lock contention**
   - **Use appropriate isolation levels**

8. **Event Sourcing:**
   - **Append events** (fast writes)
   - **Rebuild state** from events
   - **Write-optimized**

9. **CQRS:**
   - **Separate write and read models**
   - **Optimize write model** for writes
   - **Async read model updates**

10. **Compression:**
    - **Compress data** before writing
    - **Reduce I/O**

**Example Implementation:**
```python
import asyncio
from queue import Queue
from threading import Thread

class HighVolumeWriteHandler:
    def __init__(self, db, batch_size=100, flush_interval=5):
        self.db = db
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.write_queue = Queue()
        self.batch_buffer = []
        self.flush_thread = Thread(target=self._flush_loop, daemon=True)
        self.flush_thread.start()
    
    def write_async(self, data: dict):
        """Queue write for async processing"""
        self.write_queue.put(data)
        return {"status": "queued"}
    
    def write_sync(self, data: dict):
        """Synchronous write (for critical data)"""
        return self.db.insert(data)
    
    def write_batch(self, data_list: list):
        """Batch write multiple records"""
        if len(data_list) == 0:
            return
        
        # Group by table/collection if needed
        grouped = {}
        for item in data_list:
            table = item.get('table', 'default')
            if table not in grouped:
                grouped[table] = []
            grouped[table].append(item)
        
        # Batch insert per table
        for table, items in grouped.items():
            self.db.bulk_insert(table, items)
    
    def _flush_loop(self):
        """Background thread to flush queued writes"""
        while True:
            try:
                # Collect batch
                batch = []
                timeout = 0.1
                
                # Wait for first item
                item = self.write_queue.get(timeout=timeout)
                batch.append(item)
                
                # Collect more items up to batch_size or timeout
                end_time = time.time() + self.flush_interval
                while len(batch) < self.batch_size and time.time() < end_time:
                    try:
                        item = self.write_queue.get(timeout=0.1)
                        batch.append(item)
                    except:
                        break
                
                # Flush batch
                if batch:
                    try:
                        self.write_batch(batch)
                    except Exception as e:
                        logger.error(f"Batch write failed: {e}")
                        # Optionally: Move to dead letter queue
                        
            except Exception as e:
                logger.error(f"Flush loop error: {e}")
                time.sleep(1)
    
    def write_with_retry(self, data: dict, max_retries=3):
        """Write with exponential backoff retry"""
        for attempt in range(max_retries):
            try:
                return self.db.insert(data)
            except TransientError as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
```

**Best Practices:**
- **Batch writes** to reduce round trips
- **Use async writes** for non-critical data
- **Shard data** to distribute load
- **Optimize database** (indexes, connection pooling)
- **Monitor write throughput** and latency
- **Use write-optimized storage** (LSM trees, append logs)
- **Implement backpressure** to prevent overload

---

## 21. How do you pick between relational vs document database?

**Relational Database (SQL):**
- **Structured data** with relationships
- **ACID transactions**
- **Normalized schema**
- **SQL queries**
- **Examples:** PostgreSQL, MySQL, SQL Server

**Document Database (NoSQL):**
- **Semi-structured data** (JSON, BSON)
- **Flexible schema**
- **Horizontal scaling**
- **Document-oriented queries**
- **Examples:** MongoDB, CouchDB, DynamoDB

**Decision Factors:**

1. **Data Structure:**
   - **Relational:** Structured, normalized data with relationships
   - **Document:** Hierarchical, nested data (JSON-like)

2. **Schema Flexibility:**
   - **Relational:** Fixed schema, migrations needed
   - **Document:** Flexible schema, easy to evolve

3. **Relationships:**
   - **Relational:** Strong support for joins, foreign keys
   - **Document:** Embedding or references (no joins)

4. **Transactions:**
   - **Relational:** ACID transactions across tables
   - **Document:** Limited transactions (single document or eventual consistency)

5. **Scaling:**
   - **Relational:** Primarily vertical scaling (some horizontal with sharding)
   - **Document:** Built for horizontal scaling

6. **Query Patterns:**
   - **Relational:** Complex SQL queries, aggregations, joins
   - **Document:** Simple queries, limited joins

7. **Consistency:**
   - **Relational:** Strong consistency
   - **Document:** Often eventual consistency (configurable)

**When to Use Relational:**

- **Complex relationships** between entities
- **Need ACID transactions** across multiple entities
- **Complex queries** with joins and aggregations
- **Structured, normalized data**
- **Strong consistency** required
- **Examples:**
  - Financial systems (transactions)
  - E-commerce (orders, products, users)
  - Content management (related content)

**When to Use Document:**

- **Hierarchical data** (user profiles, product catalogs)
- **Flexible schema** (user-generated content)
- **High write throughput**
- **Horizontal scaling** required
- **Simple queries** on single documents
- **Examples:**
  - User profiles
  - Product catalogs
  - Content management (blog posts)
  - Real-time analytics
  - IoT data

**Hybrid Approach:**
- **Use both** for different use cases
- **Relational** for transactional data
- **Document** for content, logs, analytics
- **Polyglot persistence**

**Example Scenarios:**

**E-commerce Platform:**
- **Relational:** Orders, payments, inventory (transactions, relationships)
- **Document:** Product catalogs (flexible attributes, variants)

**Social Media:**
- **Relational:** User accounts, relationships (friends, followers)
- **Document:** Posts, comments (nested, flexible)

**Analytics Platform:**
- **Relational:** User metadata, configurations
- **Document:** Event logs, time-series data

**Best Practices:**
- **Choose based on data model**, not trends
- **Consider query patterns** before choosing
- **Don't force relational** into document model
- **Don't force document** into relational model
- **Use polyglot persistence** when appropriate
- **Consider migration path** if needs change

---

## 22. When would you use distributed transactions vs eventual consistency?

**Distributed Transactions (2PC - Two-Phase Commit):**
- **Strong consistency** across services
- **All-or-nothing** atomicity
- **Coordinator** manages commit/abort
- **Blocking** (locks resources)

**Eventual Consistency:**
- **Temporary inconsistency** allowed
- **Converges to consistency** over time
- **No global coordinator**
- **Non-blocking**

**When to Use Distributed Transactions:**

1. **Strong Consistency Required:**
   - **Financial transactions** (money transfers)
   - **Inventory management** (stock updates)
   - **Critical business operations**

2. **Simple Operations:**
   - **Few services** involved (2-3)
   - **Fast operations**
   - **Low latency** acceptable

3. **ACID Properties Needed:**
   - **Atomicity:** All or nothing
   - **Consistency:** Data remains valid
   - **Isolation:** Concurrent transactions isolated
   - **Durability:** Committed changes persist

4. **Low Throughput:**
   - **Not high-volume** system
   - **Can tolerate blocking**

**When to Use Eventual Consistency:**

1. **High Availability:**
   - **Partition tolerance** (CAP theorem)
   - **System must remain available**
   - **Can tolerate temporary inconsistency**

2. **High Throughput:**
   - **High-volume** system
   - **Need non-blocking** operations
   - **Performance critical**

3. **Long-Running Operations:**
   - **Operations take time**
   - **Can't block** for long periods
   - **Saga pattern** better fit

4. **Geographic Distribution:**
   - **Services in different regions**
   - **Network latency** makes 2PC impractical
   - **Eventual consistency** natural fit

5. **Independent Services:**
   - **Services can operate** independently
   - **Loose coupling** desired
   - **Microservices architecture**

**Trade-offs:**

| Aspect | Distributed Transactions | Eventual Consistency |
|--------|------------------------|---------------------|
| Consistency | Strong | Eventual |
| Availability | Lower (blocks on failure) | Higher |
| Performance | Slower (blocking) | Faster (non-blocking) |
| Complexity | Medium | High (conflict resolution) |
| Scalability | Limited | High |
| Latency | Higher | Lower |

**Hybrid Approach:**

- **Use 2PC** for critical, low-volume operations
- **Use eventual consistency** for high-volume, non-critical operations
- **Saga pattern** for long-running workflows

**Example - Money Transfer:**

**Distributed Transaction (2PC):**
```python
def transfer_money(from_account, to_account, amount):
    coordinator = TransactionCoordinator()
    
    try:
        # Phase 1: Prepare
        coordinator.prepare(from_account, "debit", amount)
        coordinator.prepare(to_account, "credit", amount)
        
        # Phase 2: Commit
        coordinator.commit_all()
        return {"status": "success"}
    except:
        coordinator.abort_all()
        raise
```

**Eventual Consistency (Saga):**
```python
def transfer_money_saga(from_account, to_account, amount):
    saga = MoneyTransferSaga()
    
    try:
        # Step 1: Debit (idempotent)
        debit_result = saga.debit_account(from_account, amount)
        
        # Step 2: Credit (idempotent)
        credit_result = saga.credit_account(to_account, amount)
        
        return {"status": "success"}
    except:
        # Compensate
        saga.compensate_debit(debit_result.id)
        raise
```

**Best Practices:**
- **Prefer eventual consistency** for high-scale systems
- **Use 2PC** only when strong consistency is critical
- **Design for idempotency** in eventual consistency systems
- **Monitor consistency** (eventual consistency monitors)
- **Document consistency guarantees** (strong vs eventual)
- **Use Saga pattern** for long-running workflows

---

## 23. How do you design an audit-friendly system without killing performance?

**Audit Requirements:**
- Track all changes (who, what, when, why)
- Immutable audit log
- Queryable audit trail
- Compliance (SOX, GDPR, etc.)

**Performance Challenges:**
- Additional writes for every operation
- Storage overhead
- Query performance on audit logs

**Design Strategies:**

1. **Event Sourcing:**
   - **Store events**, not current state
   - **Events are audit log** by nature
   - **Append-only** (fast writes)
   - **Rebuild state** from events

2. **Async Audit Logging:**
   - **Write audit logs asynchronously**
   - **Don't block main transaction**
   - **Queue audit events**
   - **Trade-off:** Potential loss if system crashes before flush

3. **Separate Audit Database:**
   - **Dedicated database** for audit logs
   - **Don't impact** main database performance
   - **Optimized for writes** (append-only)
   - **Can use different technology** (time-series DB)

4. **Change Data Capture (CDC):**
   - **Capture changes** at database level
   - **No application code** changes needed
   - **Low overhead**
   - **Examples:** Debezium, AWS DMS

5. **Audit Table with Partitioning:**
   - **Partition by time** (monthly/yearly)
   - **Archive old partitions**
   - **Fast writes** to current partition
   - **Efficient queries** on recent data

6. **Optimized Audit Schema:**
   - **Minimal columns** (id, entity_id, action, timestamp, user_id, changes)
   - **JSON column** for flexible change data
   - **Indexes** on frequently queried columns
   - **Compression** for old data

7. **Batch Audit Writes:**
   - **Batch multiple audit entries**
   - **Reduce write overhead**
   - **Flush periodically**

8. **Read Replicas for Audit Queries:**
   - **Query audit logs** from replica
   - **Don't impact** main database
   - **Separate read load**

**Example Implementation:**
```python
import asyncio
from queue import Queue
from threading import Thread
import json

class AuditLogger:
    def __init__(self, audit_db, batch_size=100, flush_interval=5):
        self.audit_db = audit_db
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.audit_queue = Queue()
        self.flush_thread = Thread(target=self._flush_loop, daemon=True)
        self.flush_thread.start()
    
    def log_async(self, entity_type: str, entity_id: str, action: str, 
                  user_id: str, changes: dict, metadata: dict = None):
        """Async audit logging (non-blocking)"""
        audit_event = {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": action,  # CREATE, UPDATE, DELETE
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "changes": json.dumps(changes),  # Before/after or delta
            "metadata": json.dumps(metadata or {})
        }
        self.audit_queue.put(audit_event)
    
    def log_sync(self, entity_type: str, entity_id: str, action: str,
                 user_id: str, changes: dict):
        """Synchronous audit logging (for critical operations)"""
        self.audit_db.insert("audit_logs", {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": action,
            "user_id": user_id,
            "timestamp": datetime.utcnow(),
            "changes": json.dumps(changes)
        })
    
    def _flush_loop(self):
        """Background thread to flush audit logs"""
        while True:
            try:
                batch = []
                end_time = time.time() + self.flush_interval
                
                # Collect batch
                while len(batch) < self.batch_size and time.time() < end_time:
                    try:
                        event = self.audit_queue.get(timeout=0.1)
                        batch.append(event)
                    except:
                        break
                
                # Batch insert
                if batch:
                    self.audit_db.bulk_insert("audit_logs", batch)
                    
            except Exception as e:
                logger.error(f"Audit flush error: {e}")
                time.sleep(1)

class AuditableService:
    def __init__(self, db, audit_logger):
        self.db = db
        self.audit = audit_logger
    
    def update_user(self, user_id: str, changes: dict, user_id_audit: str):
        # Get current state (for audit)
        current_user = self.db.get_user(user_id)
        
        # Update user
        updated_user = self.db.update_user(user_id, changes)
        
        # Audit log (async, non-blocking)
        self.audit.log_async(
            entity_type="user",
            entity_id=user_id,
            action="UPDATE",
            user_id=user_id_audit,
            changes={
                "before": current_user,
                "after": updated_user
            }
        )
        
        return updated_user
```

**Optimized Audit Schema:**
```sql
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(255) NOT NULL,
    action VARCHAR(20) NOT NULL,  -- CREATE, UPDATE, DELETE
    user_id VARCHAR(255),
    timestamp TIMESTAMP NOT NULL,
    changes JSONB,  -- Flexible change data
    metadata JSONB,
    -- Partition by month
    created_month DATE GENERATED ALWAYS AS (DATE_TRUNC('month', timestamp)) STORED
) PARTITION BY RANGE (created_month);

-- Indexes for common queries
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
```

**Best Practices:**
- **Use async audit logging** for non-critical operations
- **Separate audit database** to avoid impacting main DB
- **Partition audit tables** by time
- **Optimize schema** (JSON columns, minimal indexes)
- **Use CDC** if possible (low overhead)
- **Batch writes** to reduce overhead
- **Archive old audit logs** to separate storage
- **Monitor audit log performance**

---

## 24. What's your strategy for schema evolution without downtime?

**Schema Evolution:** Changing database schema while system is running (zero-downtime deployments).

**Strategies:**

1. **Backward-Compatible Changes:**
   - **Add columns** with default values (nullable or with defaults)
   - **Don't remove columns** immediately (deprecate first)
   - **Add indexes** (non-blocking in most databases)
   - **No application changes** required initially

2. **Dual-Write Pattern:**
   - **Write to both old and new schema**
   - **Read from old schema** initially
   - **Migrate data** in background
   - **Switch reads** to new schema
   - **Remove old schema** after migration

3. **Expand-Contract Pattern:**
   - **Expand:** Add new schema (new columns, tables)
   - **Migrate:** Move data to new schema
   - **Contract:** Remove old schema
   - **Gradual migration**

4. **Versioned Schema:**
   - **Version columns** (schema_version)
   - **Support multiple versions** simultaneously
   - **Application handles** different versions
   - **Gradually migrate** to new version

5. **Feature Flags:**
   - **Toggle new schema** with feature flags
   - **Rollback easily** if issues
   - **Gradual rollout**

6. **Database Migrations:**
   - **Idempotent migrations**
   - **Rollback scripts**
   - **Test in staging** first
   - **Run during low traffic** if possible

7. **Read Replicas:**
   - **Apply migration to replica** first
   - **Test with replica**
   - **Switch traffic** to replica
   - **Apply to primary**

8. **Blue-Green Deployment:**
   - **Two identical environments**
   - **Migrate green** environment
   - **Switch traffic** from blue to green
   - **Blue becomes new green**

**Example - Adding a New Column:**

**Step 1: Add Column (Backward Compatible)**
```sql
-- Add nullable column (safe)
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) NULL;

-- Or with default (safe)
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';
```

**Step 2: Deploy Application (Dual-Write)**
```python
class UserService:
    def create_user(self, user_data: dict):
        user = {
            "name": user_data["name"],
            "email": user_data["email"],
            "phone_number": user_data.get("phone_number"),  # New field
            "status": user_data.get("status", "active")  # New field
        }
        
        # Write to database (new schema)
        return self.db.create_user(user)
    
    def get_user(self, user_id: str):
        user = self.db.get_user(user_id)
        # Handle missing phone_number for old records
        if "phone_number" not in user:
            user["phone_number"] = None
        return user
```

**Step 3: Backfill Data (Optional)**
```python
def backfill_phone_numbers():
    """Backfill phone numbers for existing users"""
    users = db.query("SELECT id FROM users WHERE phone_number IS NULL")
    for user in users:
        # Get phone from external source or set default
        phone = get_phone_from_external_source(user.id)
        db.execute(
            "UPDATE users SET phone_number = ? WHERE id = ?",
            phone, user.id
        )
```

**Example - Removing a Column:**

**Step 1: Stop Writing to Column**
```python
# Application no longer writes to old_column
# But still reads it for backward compatibility
```

**Step 2: Migrate Data (if needed)**
```python
# Copy data to new column or table if needed
```

**Step 3: Remove Column (After All Instances Updated)**
```sql
-- Remove column (after ensuring no code uses it)
ALTER TABLE users DROP COLUMN old_column;
```

**Example - Renaming a Column:**

**Step 1: Add New Column**
```sql
ALTER TABLE users ADD COLUMN new_name VARCHAR(255);
```

**Step 2: Dual-Write**
```python
def update_user(user_id: str, data: dict):
    # Write to both columns
    db.execute(
        "UPDATE users SET old_name = ?, new_name = ? WHERE id = ?",
        data["name"], data["name"], user_id
    )
```

**Step 3: Backfill**
```python
# Copy old_name to new_name for existing records
db.execute("UPDATE users SET new_name = old_name WHERE new_name IS NULL")
```

**Step 4: Switch Reads**
```python
# Application now reads from new_name
```

**Step 5: Remove Old Column**
```sql
ALTER TABLE users DROP COLUMN old_name;
```

**Best Practices:**
- **Make changes backward compatible** when possible
- **Use feature flags** for gradual rollout
- **Test migrations** in staging first
- **Have rollback plan** for every migration
- **Monitor** during and after migration
- **Communicate changes** to team
- **Document migration steps**
- **Use database migration tools** (Alembic, Flyway, Liquibase)
- **Run during low traffic** if possible
- **Support multiple schema versions** during transition