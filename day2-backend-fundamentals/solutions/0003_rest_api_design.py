"""
REST API Design Solution

RESTful API design principles and examples for backend interview preparation.
Covers:
- REST principles and constraints
- Resource modeling
- HTTP methods and status codes
- API versioning
- Error handling
- Pagination, filtering, sorting
- Security considerations
"""

# REST API Design Principles
REST_PRINCIPLES = '''
REST (Representational State Transfer) Principles:

1. Client-Server Architecture
   - Separation of concerns between client and server
   - Client handles UI, server handles data storage and business logic

2. Statelessness
   - Each request contains all information needed to understand it
   - Server does not store client context between requests
   - Improves scalability and reliability

3. Cacheability
   - Responses must define themselves as cacheable or not
   - Clients can cache responses to improve performance

4. Uniform Interface
   - Resource identification through URLs
   - Manipulation of resources through representations
   - Self-descriptive messages
   - Hypermedia as the engine of application state (HATEOAS)

5. Layered System
   - Client cannot tell if connected directly to server or through intermediaries
   - Allows for load balancing, shared caches, etc.

6. Code on Demand (optional)
   - Servers can temporarily extend client functionality by transferring code
'''

# HTTP Methods and Their Usage
HTTP_METHODS = '''
HTTP Methods in REST APIs:

GET:
    - Retrieve resource(s)
    - Safe and idempotent
    - Examples: 
        GET /users          # Get all users
        GET /users/123      # Get specific user
        GET /users?role=admin  # Get users with filter

POST:
    - Create new resource
    - Not safe, not idempotent
    - Examples:
        POST /users         # Create new user
        POST /orders        # Create new order

PUT:
    - Update existing resource (replace entire resource)
    - Idempotent
    - Examples:
        PUT /users/123      # Replace user completely
        PUT /products/456   # Replace product completely

PATCH:
    - Partially update resource
    - Not necessarily idempotent
    - Examples:
        PATCH /users/123    # Update specific fields of user
        PATCH /orders/789   # Update order status only

DELETE:
    - Remove resource
    - Idempotent
    - Examples:
        DELETE /users/123   # Delete user
        DELETE /orders/456  # Delete order

HEAD:
    - Same as GET but without response body
    - Used for checking metadata, availability

OPTIONS:
    - Describe communication options for resource
    - Used for CORS preflight requests
'''

# HTTP Status Codes
HTTP_STATUS_CODES = '''
HTTP Status Codes by Category:

1xx Informational
    100 Continue
    101 Switching Protocols

2xx Success
    200 OK                    # Standard successful response
    201 Created               # Resource successfully created
    202 Accepted              # Request accepted for processing
    204 No Content            # Successful but no response body

3xx Redirection
    301 Moved Permanently     # Resource moved permanently
    302 Found                 # Resource temporarily moved
    304 Not Modified          # Resource not modified (for caching)

4xx Client Errors
    400 Bad Request           # Invalid request syntax or parameters
    401 Unauthorized          # Authentication required
    403 Forbidden             # Authenticated but insufficient permissions
    404 Not Found             # Resource not found
    405 Method Not Allowed    # HTTP method not supported for resource
    409 Conflict              # Request conflicts with current state
    422 Unprocessable Entity  # Semantic errors (validation failures)
    429 Too Many Requests     # Rate limiting exceeded

5xx Server Errors
    500 Internal Server Error # Generic server error
    502 Bad Gateway           # Invalid response from upstream server
    503 Service Unavailable   # Server temporarily unavailable
    504 Gateway Timeout       # Upstream server timeout
'''

# Resource Modeling Examples
RESOURCE_MODELING = '''
REST Resource Modeling Examples:

Good Resource Names (nouns, not verbs):
    ✓ /users                    # Collection of users
    ✓ /users/123                # Specific user
    ✓ /orders                   # Collection of orders
    ✓ /orders/123/items         # Items in specific order
    ✓ /products                 # Collection of products
    ✓ /categories/5/products    # Products in specific category

Avoid Verb-based URLs:
    ✗ /getUsers                 # Use GET /users instead
    ✗ /createUser               # Use POST /users instead
    ✗ /deleteOrder/123          # Use DELETE /orders/123 instead

Collection vs Resource URLs:
    GET    /users               # Get all users
    POST   /users               # Create new user
    GET    /users/123           # Get specific user
    PUT    /users/123           # Update specific user
    PATCH  /users/123           # Partially update specific user
    DELETE /users/123           # Delete specific user

Nested Resources:
    GET    /users/123/orders    # Get orders for specific user
    POST   /users/123/orders    # Create order for specific user
    GET    /orders/123/items    # Get items for specific order
'''

# API Versioning Strategies
API_VERSIONING = '''
API Versioning Strategies:

1. URL Versioning (Most Common)
    GET /api/v1/users
    GET /api/v2/users
    Pros: Simple, visible, works with caching
    Cons: Can lead to duplication

2. Header Versioning
    GET /api/users
    Header: Accept-Version: v1
    Pros: Clean URLs
    Cons: Less visible, harder to test/cache

3. Query Parameter Versioning
    GET /api/users?version=1
    Pros: Simple to implement
    Cons: Can interfere with caching, less RESTful

4. Media Type Versioning
    GET /api/users
    Header: Accept: application/vnd.myapi.v1+json
    Pros: Clean URLs, content negotiation
    Cons: Complex to implement

Recommendation: Use URL versioning for simplicity and clarity
'''

# Error Handling Format
ERROR_HANDLING = '''
Standard Error Response Format:

{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {
                "field": "email",
                "message": "Email format is invalid"
            },
            {
                "field": "password",
                "message": "Password must be at least 8 characters"
            }
        ]
    }
}

HTTP Status Codes for Errors:
- 400 Bad Request: Validation errors, malformed requests
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Authenticated but insufficient permissions
- 404 Not Found: Resource doesn't exist
- 409 Conflict: Resource conflict (e.g., duplicate email)
- 422 Unprocessable Entity: Semantic errors (validation)
- 429 Too Many Requests: Rate limiting
'''

# Pagination Strategies
PAGINATION = '''
Pagination Strategies:

1. Offset-Based (LIMIT/OFFSET)
    GET /users?limit=20&offset=40
    Pros: Simple to understand and implement
    Cons: Poor performance on large datasets, inconsistent results with data changes

2. Cursor-Based (Keyset)
    GET /users?cursor=eyJpZCI6MTIzfQ==&limit=20
    Pros: Consistent performance, stable results with data changes
    Cons: More complex implementation, no random access

3. Page-Based
    GET /users?page=3&size=20
    Pros: Familiar to users, good UX
    Cons: Similar limitations to offset-based

Recommendation: Use cursor-based for large datasets, offset-based for small/admin APIs
'''

# Filtering, Sorting, and Searching
FILTERING_SORTING = '''
Filtering, Sorting, and Searching Parameters:

Filtering:
    GET /users?role=admin&is_active=true
    GET /products?category=electronics&price_min=100&price_max=500
    GET /orders?status=shipped&date_from=2024-01-01&date_to=2024-01-31

Sorting:
    GET /users?sort=name&order=asc
    GET /products?sort=price&order=desc
    GET /users?sort=-created_at  # Negative for descending (alternative)
    GET /users?sort=name,created_at  # Multiple sort fields

Searching:
    GET /users?q=john  # Search in name, email, etc.
    GET /products?q=laptop  # Full-text search
    GET /articles?q=python+django  # Search with multiple terms

Best Practices:
- Use consistent parameter names across endpoints
- Document all available filter/sort/search options
- Consider performance implications of filtering on non-indexed fields
- Use database-specific full-text search for complex search requirements
'''

# Security Considerations
SECURITY_CONSIDERATIONS = '''
Security Considerations for REST APIs:

1. Authentication & Authorization
   - Use industry standards (JWT, OAuth 2.0, API Keys)
   - Implement proper role-based access control (RBAC)
   - Validate tokens on protected endpoints
   - Use HTTPS exclusively in production

2. Input Validation
   - Validate all input data (type, format, length, range)
   - Use allowlists over blocklists when possible
   - Implement rate limiting to prevent abuse
   - Sanitize inputs to prevent injection attacks

3. Data Protection
   - Encrypt sensitive data at rest and in transit
   - Never expose passwords or tokens in responses
   - Use proper HTTP security headers
   - Implement CORS policies appropriately

4. API Specific Protections
   - Implement request size limits
   - Use timeout mechanisms for long-running requests
   - Log and monitor API usage for anomalies
   - Regular security testing and penetration testing
'''

# Example API Endpoints for E-commerce Platform
EXAMPLE_ENDPOINTS = '''
# User Management
GET    /api/v1/users              # List users (with pagination/filtering)
POST   /api/v1/users              # Create new user
GET    /api/v1/users/{id}         # Get specific user
PUT    /api/v1/users/{id}         # Update user completely
PATCH  /api/v1/users/{id}         # Partially update user
DELETE /api/v1/users/{id}         # Delete user

# Authentication
POST   /api/v1/auth/login         # Login user
POST   /api/v1/auth/logout        # Logout user
POST   /api/v1/auth/refresh       # Refresh access token
POST   /api/v1/auth/register      # Register new user

# Product Management
GET    /api/v1/products           # List products
POST   /api/v1/products           # Create new product
GET    /api/v1/products/{id}      # Get specific product
PUT    /api/v1/products/{id}      # Update product
PATCH  /api/v1/products/{id}      # Partially update product
DELETE /api/v1/products/{id}      # Delete product

# Order Management
GET    /api/v1/orders             # List orders
POST   /api/v1/orders             # Create new order
GET    /api/v1/orders/{id}        # Get specific order
PUT    /api/v1/orders/{id}        # Update order
PATCH  /api/v1/orders/{id}        # Partially update order
DELETE /api/v1/orders/{id}        # Delete order
GET    /api/v1/orders/{id}/items  # Get order items
POST   /api/v1/orders/{id}/items  # Add item to order

# Cart Management
GET    /api/v1/cart               # Get current user's cart
POST   /api/v1/cart/items         # Add item to cart
PUT    /api/v1/cart/items/{id}    # Update cart item quantity
DELETE /api/v1/cart/items/{id}    # Remove item from cart
DELETE /api/v1/cart               # Clear cart

# Payment Processing
POST   /api/v1/payments           # Process payment
GET    /api/v1/payments/{id}      # Get payment details
'''

def print_rest_api_examples():
    """Print REST API design examples for reference."""
    print("=== REST PRINCIPLES ===")
    print(REST_PRINCIPLES.strip())
    print("\n=== HTTP METHODS ===")
    print(HTTP_METHODS.strip())
    print("\n=== HTTP STATUS CODES ===")
    print(HTTP_STATUS_CODES.strip())
    print("\n=== RESOURCE MODELING ===")
    print(RESOURCE_MODELING.strip())
    print("\n=== API VERSIONING ===")
    print(API_VERSIONING.strip())
    print("\n=== ERROR HANDLING ===")
    print(ERROR_HANDLING.strip())
    print("\n=== PAGINATION ===")
    print(PAGINATION.strip())
    print("\n=== FILTERING, SORTING, SEARCHING ===")
    print(FILTERING_SORTING.strip())
    print("\n=== SECURITY CONSIDERATIONS ===")
    print(SECURITY_CONSIDERATIONS.strip())
    print("\n=== EXAMPLE ENDPOINTS ===")
    print(EXAMPLE_ENDPOINTS.strip())

if __name__ == "__main__":
    print_rest_api_examples()
    
    # REST API Interview Tips
    print("\n" + "="*50)
    print("REST API DESIGN INTERVIEW TIPS:")
    print("="*50)
    print("1. Think in terms of resources (nouns), not actions (verbs)")
    print("2. Use proper HTTP methods for CRUD operations")
    print("3. Return appropriate HTTP status codes")
    print("4. Use consistent naming conventions and parameter styles")
    print("5. Implement proper error handling with meaningful messages")
    print("6. Consider versioning strategy from the beginning")
    print("7. Plan for pagination, filtering, and sorting")
    print("8. Think about security (authentication, authorization, validation)")
    print("9. Document your API properly (OpenAPI/Swagger)")
    print("10. Consider HATEOAS for discoverability (bonus points)")
    print("11. Understand trade-offs between different approaches")
    print("12. Practice designing APIs for common scenarios (e-commerce, social media, etc.)")