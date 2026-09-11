"""
System Design Basics Solution

Fundamental system design concepts for backend interview preparation.
Covers:
- Scalability concepts
- Availability and reliability
- Consistency models
- Caching strategies
- Database scaling
- Message queues
- Load balancing
- Microservices vs monolith
- CAP theorem
- System design interview approach
"""

# Scalability Concepts
SCALABILITY_CONCEPTS = '''
Scalability: Ability of system to handle growing amounts of work
Types of Scalability:

1. Vertical Scaling (Scaling Up)
    - Add more resources to existing server (CPU, RAM, Storage)
    - Pros: Simple, no code changes needed
    - Cons: Hardware limits, single point of failure, expensive
    - Limits: Diminishing returns, cost becomes prohibitive

2. Horizontal Scaling (Scaling Out)
    - Add more servers to distribute load
    - Pros: Theoretically unlimited, better fault tolerance
    - Cons: Increased complexity, need for load balancing
    - Requirements: Stateless services, shared nothing architecture

3. Load Distribution Strategies:
    - Round Robin: Distribute requests evenly in sequence
    - Least Connections: Send to server with fewest active connections
    - IP Hash: Same client IP always goes to same server
    - Weighted: Assign weights based on server capacity

4. Bottleneck Identification:
    - CPU-bound: Processing power limits throughput
    - Memory-bound: Available RAM limits concurrent operations
    - I/O-bound: Disk/network speed limits data transfer
    - Network-bound: Bandwidth limits communication
'''

# Availability and Reliability
AVAILABILITY_RELIABILITY = '''
Availability: Percentage of time system is operational and accessible
Reliability: Probability system will perform without failure over time

Key Metrics:
- Uptime: Percentage of time system is available
- MTBF: Mean Time Between Failures
- MTTR: Mean Time To Recovery
- RTO: Recovery Time Objective
- RPO: Recovery Point Objective

Availability Classes:
- 90% ("one nine"): 36.5 days downtime/year
- 99% ("two nines"): 3.65 days downtime/year
- 99.9% ("three nines"): 8.76 hours downtime/year
- 99.99% ("four nines"): 52.6 minutes downtime/year
- 99.999% ("five nines"): 5.26 minutes downtime/year
- 99.9999% ("six nines"): 31.5 seconds downtime/year

Strategies for High Availability:
1. Redundancy: Duplicate critical components
2. Failover: Automatic switch to backup systems
3. Load Distribution: Spread load across multiple instances
4. Health Checks: Monitor component health
5. Graceful Degradation: Reduce functionality during issues
6. Circuit Breaker: Prevent cascading failures
'''

# Consistency Models
CONSISTENCY_MODELS = '''
Consistency: How up-to-date and synchronized data is across system

Strong Consistency:
    - All nodes see same data at same time
    - ACID transactions guarantee
    - Pros: Simple to reason about
    - Cons: Higher latency, lower availability
    - Use cases: Financial transactions, user accounts

Eventual Consistency:
    - System will become consistent over time
    - High availability and partition tolerance
    - Pros: Better performance, higher availability
    - Cons: Temporary inconsistencies, complex conflict resolution
    - Use cases: Social media feeds, analytics, caching

Consistency Levels:
    - Strict Consistency: Strongest form
    - Sequential Consistency: Operations appear in program order
    - Causal Consistency: Causally related operations ordered
    - Read Your Writes: Client sees its own writes
    - Monotonic Reads: Successive reads return same or newer data
    - Monotonic Writes: Writes from same process ordered
    - Write Follows Reads: Write follows previous read

Implementing Consistency:
    - Quorum Reads/Writes: Require majority agreement
    - Vector Clocks: Track causality between events
    - Conflict Resolution: Last-write-wins, merge functions
    - Read Repair: Fix inconsistencies during read operations
'''

# Caching Strategies
CACHING_STRATEGIES = '''
Caching: Store frequently accessed data in fast access layer

Cache Types:
1. Local Cache (In-process)
    - Stored in application memory
    - Pros: Fastest access, no network overhead
    - Cons: Limited by JVM/process memory, not shared
    - Examples: HashMap, LRU cache, Guava Cache

2. Distributed Cache
    - Shared across multiple instances
    - Pros: Shared state, survives restarts
    - Cons: Network overhead, consistency challenges
    - Examples: Redis, Memcached, Hazelcast

3. CDN (Content Delivery Network)
    - Geographically distributed static content
    - Pros: Global low latency, offloads origin
    - Cons: Cost, cache invalidation complexity
    - Examples: CloudFront, Cloudflare, Akamai

Cache Strategies:
1. Cache-Aside (Lazy Loading)
    - Application loads data into cache on cache miss
    - Pros: Simple, cache only requested data
    - Cons: Cache miss penalty, potential stale data
    - Pattern: Try cache → if miss, load from DB → store in cache → return

2. Write-Through
    - Write to cache and database synchronously
    - Pros: Consistent cache, good read performance
    - Cons: Higher write latency, complex failure handling
    - Pattern: Write to cache → write to DB → return success

3. Write-Behind (Write-Back)
    - Write to cache first, async write to database
    - Pros: Fast writes, batching opportunities
    - Cons: Risk of data loss, complex failure recovery
    - Pattern: Write to cache → acknowledge → async write to DB

4. Refresh-Ahead
    - Proactively refresh cache before expiration
    - Pros: Reduced cache miss penalty
    - Cons: Wasted resources if data not accessed
    - Pattern: Background refresh based on access patterns

Cache Eviction Policies:
    - LRU (Least Recently Used): Remove oldest accessed items
    - LFU (Least Frequently Used): Remove least used items
    - FIFO (First In, First Out): Remove oldest inserted items
    - Random: Random selection for removal
    - TTL (Time To Live): Expire after fixed time

Cache Considerations:
    - Cache Invalidation: Knowing when to update/remove cached data
    - Cache Warming: Pre-loading cache with expected data
    - Cache Size: Balancing memory usage vs hit rate
    - Serialization: Converting objects to/from storable format
    - Network Partition Handling: What happens when cache is unreachable
'''

# Database Scaling
DATABASE_SCALING = '''
Database Scaling Strategies:

1. Replication
    - Master-Slave: One write master, multiple read slaves
    - Master-Master: Multiple nodes can accept writes
    - Pros: Read scaling, fault tolerance, geographic distribution
    - Cons: Replication lag, conflict resolution, complexity
    - Use cases: Read-heavy workloads, disaster recovery

2. Sharding (Horizontal Partitioning)
    - Split data across multiple databases based on shard key
    - Pros: Write scaling, improved query performance, fault isolation
    - Cons: Complex joins, rebalancing difficulty, operational overhead
    - Shard Key Strategies:
        * Range-based: IDs 1-1000 on shard A, 1001-2000 on shard B
        * Hash-based: Hash(shard_key) % number_of_shards
        * Directory-based: Lookup table mapping keys to shards
        * Entity-based: Keep related data together (user_id for user data)

3. Vertical Partitioning
    - Split tables by columns (vertical slicing)
    - Pros: Reduce I/O for frequently accessed columns
    - Cons: Join complexity, null value handling
    - Use cases: Separating frequently vs infrequently accessed columns

4. Denormalization
    - Intentional redundancy for performance
    - Pros: Reduced JOINs, improved read performance
    - Cons: Storage overhead, update complexity, inconsistency risk
    - Examples: Pre-computed aggregates, cached user names in comments

5. Read Replicas
    - Asynchronous copies for read scaling
    - Pros: Simple setup, good for reporting/analytics
    - Cons: Replication lag, not suitable for real-time reads
    - Use cases: Dashboards, analytics, background processing

6. Connection Pooling
    - Reuse database connections instead of creating new ones
    - Pros: Reduced connection overhead, better resource utilization
    - Cons: Pool exhaustion, connection leaks
    - Implementation: HikariCP, pgBouncer, built-in pool managers
'''

# Message Queues
MESSAGE_QUEUES = '''
Message Queues: Asynchronous communication mechanism

Patterns:
1. Point-to-Point (Queue)
    - One producer, one consumer per message
    - Guaranteed delivery, ordered processing
    - Use cases: Job processing, email sending, file processing

2. Publish-Subscribe (Topic)
    - One producer, multiple consumers
    - Each consumer gets copy of message
    - Use cases: Event notifications, real-time updates, logging

3. Request-Reply
    - Synchronous-like communication over async medium
    - Use cases: RPC, service-to-service communication

Popular Message Queues:
1. RabbitMQ
    - Traditional message broker
    - Supports multiple protocols (AMQP, MQTT, STOMP)
    - Features: Routing, clustering, management UI
    - Use cases: Traditional enterprise messaging

2. Apache Kafka
    - Distributed streaming platform
    - High throughput, fault-tolerant, scalable
    - Features: Persistence, replayability, stream processing
    - Use cases: Event sourcing, log aggregation, stream processing

3. Amazon SQS
    - Managed queue service
    - Standard queues (at-least-once delivery)
    - FIFO queues (exactly-once ordering)
    - Features: Fully managed, scalable, integrates with AWS
    - Use cases: Decoupling microservices, batch processing

4. Redis Pub/Sub
    - Simple in-memory publish/subscribe
    - Pros: Fast, simple
    - Cons: No persistence, no guaranteed delivery
    - Use cases: Real-time notifications, simple broadcasting

Queue Design Considerations:
    - Message Ordering: FIFO vs priority-based
    - Delivery Guarantees: At-most-once, at-least-once, exactly-once
    - Durability: Persistent vs in-memory storage
    - Scalability: Horizontal scaling capabilities
    - Monitoring: Queue depth, processing rates, dead letter queues
    - Dead Letter Handling: Handling repeatedly failed messages
'''

# Load Balancing
LOAD_BALANCING = '''
Load Balancing: Distribute incoming network traffic across servers

Types:
1. Layer 4 (Transport Layer)
    - Works on TCP/UDP level
    - Based on IP address and port
    - Pros: Fast, simple
    - Cons: Limited intelligence, no content awareness
    - Examples: HAProxy (TCP mode), AWS Network Load Balancer

2. Layer 7 (Application Layer)
    - Works on HTTP level
    - Can inspect headers, cookies, URL paths
    - Pros: Intelligent routing, content-based decisions
    - Cons: More complex, higher latency
    - Examples: HAProxy (HTTP mode), NGINX, AWS Application Load Balancer

Algorithms:
    - Round Robin: Distribute evenly in rotation
    - Weighted Round Robin: Assign weights to servers
    - Least Connections: Send to server with fewest connections
    - Least Response Time: Send to fastest responding server
    - IP Hash: Same client IP to same server (session affinity)
    - URL Hash: Same URL to same server (cache friendly)
    - Random: Random distribution
    - Least Bandwidth: Send to server using least bandwidth

Health Checks:
    - Active: Periodically send test requests
    - Passive: Monitor actual request responses
    - Types: TCP connect, HTTP GET, HTTPS, custom scripts
    - Failure thresholds: Consecutive failures before marking down
    - Recovery: How soon to retry after failure

SSL/TLS Termination:
    - Offload encryption/decryption to load balancer
    - Pros: Reduced backend CPU usage, centralized certificate management
    - Cons: Additional point of failure, complexity
    - Options: Terminate at LB, passthrough to backend, re-encrypt

Sticky Sessions (Session Affinity):
    - Route same client to same server
    - Implementations: Cookie-based, IP-based, URL-based
    - Pros: Better caching, session state locality
    - Cons: Uneven load distribution, scalability limitations
'''

# Microservices vs Monolith
MICROSERVICES_VS_MONOLITH = '''
Monolithic Architecture:
    - Single deployable unit
    - All components tightly coupled
    - Pros: Simple development, testing, deployment
    - Cons: Scaling limitations, technology lock-in, long build times
    - Use cases: Simple applications, MVPs, small teams

Microservices Architecture:
    - Collection of small, independent services
    - Each service has single responsibility
    - Communicate via well-defined APIs (usually HTTP/REST or gRPC)
    - Pros: Independent scaling, technology diversity, fault isolation
    - Cons: Increased complexity, network latency, data consistency
    - Use cases: Complex applications, large teams, evolving requirements

Microservices Characteristics:
    - Service Independence: Deploy, scale, update independently
    - Bounded Contexts: Clear boundaries between services
    - API Contracts: Well-defined, versioned interfaces
    - Decentralized Data: Each service owns its data
    - Failure Isolation: Failures don't cascade uncontrollably
    - Technology Heterogeneity: Different services can use different tech

Communication Patterns:
    - Synchronous: HTTP/REST, gRPC (request-response)
    - Asynchronous: Message queues, event streaming
    - Service Discovery: Dynamic location of services
    - Load Balancing: Distribute requests across service instances

Data Management Challenges:
    - Distributed Transactions: ACID across services
    - Eventual Consistency: Accept temporary inconsistency
    - Saga Pattern: Compensating transactions for rollback
    - CQRS: Separate read and write models
    - Event Sourcing: Store events instead of current state

Infrastructure Needs:
    - Containerization: Docker, container orchestration
    - Service Mesh: Istio, Linkerd for traffic management
    - API Gateway: Entry point, authentication, rate limiting
    - Observability: Logging, monitoring, tracing
    - CI/CD: Automated testing and deployment
'''

# CAP Theorem
CAP_THEOREM = '''
CAP Theorem: In distributed systems, you can only have two of three:
    Consistency: All nodes see same data at same time
    Availability: Every request receives response (success/failure)
    Partition Tolerance: System continues despite network partitions

Trade-offs:
    CA Systems (Consistency + Availability):
        - Not partition tolerant
        - Examples: Traditional RDBMS (when single node)
        - Use cases: Systems that can tolerate downtime

    CP Systems (Consistency + Partition Tolerance):
        - Not always available during partitions
        - Examples: MongoDB, HBase, Redis Cluster
        - Use cases: Financial systems, inventory management

    AP Systems (Availability + Partition Tolerance):
        - Not always consistent
        - Examples: Cassandra, DynamoDB, CouchDB
        - Use cases: Social media, analytics, content delivery

PACELC Theorem (Extension):
    If Partition exists:
        - Trade-off between Consistency and Latency
    Else:
        - Trade-off between Consistency and Latency

Practical Implications:
    - Network partitions are inevitable in distributed systems
    - Therefore, must choose between Consistency and Availability
    - Modern systems often tune consistency levels
    - Consider using multiple consistency levels for different data
'''

# System Design Interview Approach
SYSTEM_DESIGN_APPROACH = '''
Systematic Approach to System Design Interviews:

1. Clarify Requirements
    - Functional requirements: What the system should do
    - Non-functional requirements: Performance, scalability, availability
    - Constraints: Budget, timeline, technology limitations
    - Questions to ask:
        * Who are the users?
        * What are the main features?
        * What is the expected scale (users, requests per second)?
        * What are the performance requirements (latency, throughput)?
        * What are the availability requirements?

2. High-Level Design
    - Identify core components
    - Sketch basic architecture
    - Identify data flow
    - Consider bottlenecks
    - Draw component diagram

3. Deep Dive into Components
    - Detail each major component
    - Consider storage options
    - Think about APIs and interfaces
    - Address specific challenges
    - Consider edge cases and error handling

4. Identify and Address Bottlenecks
    - Where will the system struggle under load?
    - What are the single points of failure?
    - How will you scale each component?
    - What trade-offs are you making?

5. Review and Optimize
    - Walk through user journeys
    - Check if all requirements are met
    - Consider improvements and alternatives
    - Discuss trade-offs made
    - Summary of final design

Common System Design Questions:
    - Design URL shortener (like bit.ly)
    - Design Twitter/X
    - Design Instagram/Pinterest
    - Design Uber/Lyft ride sharing
    - Design Netflix/YouTube video streaming
    - Design Dropbox/Google Drive file storage
    - Design Chat/WhatsApp messaging system
    - Design Amazon/e-commerce platform
    - Design Twitter/X timeline/newsfeed
    - Design Google Docs real-time collaboration

Key Concepts to Remember:
    - Start simple, then iterate
    - Consider trade-offs explicitly
    - Think about failure scenarios
    - Plan for monitoring and observability
    - Think about data flow and storage
    - Consider security and privacy
    - Plan for evolution and future growth
'''

# Example System Designs
EXAMPLE_DESIGNS = '''
Example 1: URL Shortener (bit.ly style)

Requirements:
    - Shorten long URLs
    - Redirect short URLs to original
    - Custom aliases optional
    - Analytics: click counts, geographic data
    - High availability and low latency

Components:
    - API Layer: Handle shorten and redirect requests
    - Application Logic: Generate short codes, validate URLs
    - Storage: Database for URL mappings
    - Cache: Frequently accessed mappings
    - Analytics: Separate service for tracking clicks

Data Model:
    - URL Mapping Table:
        * short_code (PK): e.g., "abc123"
        * original_url: The long URL
        * created_at: Timestamp
        * clicks: Integer counter
        * creator_id: Optional user ID

Algorithms:
    - Short Code Generation:
        * Base62 encoding (a-z, A-Z, 0-9)
        * Incremental ID → Base62
        * Random generation with collision detection
        * Hash-based approach

Scaling Considerations:
    - Read-heavy workload (more redirects than creations)
    - Cache hot URLs
    - Database sharding by short_code hash
    - CDN for static assets
    - Rate limiting to prevent abuse

Example 2: Twitter/X Timeline

Requirements:
    - Users can post tweets
    - Users can follow other users
    - Users see timeline of followed users' tweets
    - Real-time updates preferred
    - Handle celebrities with millions of followers

Approaches:
    1. Fan-out on Write:
        - When user posts tweet, push to all followers' timelines
        - Pros: Fast reads, real-time
        - Cons: Expensive for celebrities (fan-out problem)
        - Solution: Hybrid approach (celebrities vs regular users)

    2. Fan-out on Read:
        - When user requests timeline, fetch from followed users
        - Pros: Efficient writes
        - Cons: Slow reads, especially for users following many
        - Solution: Cache recent tweets, limit followees

    3. Mixed Approach:
        - Regular users: Fan-out on write
        - Celebrities: Fan-out on read with caching
        - Use tweet IDs for efficient sorting/pagination

Data Storage:
    - Tweets Table: tweet_id, user_id, content, timestamp
    - Follows Table: follower_id, followee_id
    - Timeline Cache: user_id → [recent_tweet_ids]
    - Redis Sorted Sets: For timeline with timestamps as scores

Example 3: Chat Application

Requirements:
    - One-to-one and group messaging
    - Online/offline status indicators
    - Message persistence
    - Typing indicators
    - Read receipts
    - Media sharing

Components:
    - WebSocket Servers: Handle persistent connections
    - Message Service: Store and retrieve messages
    - User Service: Manage user profiles and relationships
    - Presence Service: Track online/offline status
    - Notification Service: Push notifications for offline users
    - File Service: Handle media uploads/storage

Technologies:
    - WebSocket: Real-time bidirectional communication
    - Message Queue: For offline message delivery
    - Database: For persistent message storage
    - Cache: For online status and recent messages
    - CDN: For media file delivery

Scaling Considerations:
    - WebSocket connections are memory-intensive
    - Horizontal scaling with sticky sessions
    - Message partitioning by user ID or conversation ID
    - Read replicas for message history
    - Geographic distribution for global users
'''

def print_system_design_examples():
    """Print system design examples for reference."""
    print("=== SCALABILITY CONCEPTS ===")
    print(SCALABILITY_CONCEPTS.strip())
    print("\n=== AVAILABILITY AND RELIABILITY ===")
    print(AVAILABILITY_RELIABILITY.strip())
    print("\n=== CONSISTENCY MODELS ===")
    print(CONSISTENCY_MODELS.strip())
    print("\n=== CACHING STRATEGIES ===")
    print(CACHING_STRATEGIES.strip())
    print("\n=== DATABASE SCALING ===")
    print(DATABASE_SCALING.strip())
    print("\n=== MESSAGE QUEUES ===")
    print(MESSAGE_QUEUES.strip())
    print("\n=== LOAD BALANCING ===")
    print(LOAD_BALANCING.strip())
    print("\n=== MICROSERVICES VS MONOLITH ===")
    print(MICROSERVICES_VS_MONOLITH.strip())
    print("\n=== CAP THEOREM ===")
    print(CAP_THEOREM.strip())
    print("\n=== SYSTEM DESIGN INTERVIEW APPROACH ===")
    print(SYSTEM_DESIGN_APPROACH.strip())
    print("\n=== EXAMPLE SYSTEM DESIGNS ===")
    print(EXAMPLE_DESIGNS.strip())

if __name__ == "__main__":
    print_system_design_examples()
    
    # System Design Interview Tips
    print("\n" + "="*50)
    print("SYSTEM DESIGN INTERVIEW TIPS:")
    print("="*50)
    print("1. Start by clarifying requirements - don't make assumptions")
    print("2. Think about scale from the beginning (users, QPS, data volume)")
    print("3. Draw a simple high-level diagram first")
    print("4. Identify potential bottlenecks and single points of failure")
    print("5. Consider trade-offs explicitly (consistency vs availability, etc.)")
    print("6. Think about data flow: how data moves through your system")
    print("7. Consider storage options and access patterns")
    print("8. Plan for failure: what happens when components fail?")
    print("9. Think about monitoring, logging, and observability")
    print("10. Consider security aspects: authentication, authorization, data protection")
    print("11. Remember to discuss both functional and non-functional requirements")
    print("12. Practice explaining your thought process clearly")
    print("13. Know when to use SQL vs NoSQL databases")
    print("14. Understand caching strategies and when to apply them")
    print("15. Be ready to discuss alternatives and justify your choices")