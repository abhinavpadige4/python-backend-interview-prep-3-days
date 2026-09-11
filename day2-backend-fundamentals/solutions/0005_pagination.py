"""
API Pagination and Filtering Solution

Implementation examples and concepts for API pagination, filtering, and sorting
for backend interview preparation.
Covers:
- Different pagination strategies
- Filtering implementation
- Sorting mechanisms
- Performance considerations
- Best practices
"""

# Pagination Strategies
PAGINATION_STRATEGIES = '''
Pagination Strategies Comparison:

1. Offset-Based (LIMIT/OFFSET)
    SQL: SELECT * FROM table LIMIT 20 OFFSET 40
    Pros:
        - Simple to understand and implement
        - Works with all SQL databases
        - Easy to calculate total pages
    Cons:
        - Poor performance on large offsets (O(n) complexity)
        - Inconsistent results when data changes between requests
        - No guarantee of seeing all items exactly once

2. Cursor-Based (Keyset Pagination)
    SQL: SELECT * FROM table WHERE id > 100 ORDER BY id LIMIT 20
    Pros:
        - Consistent performance regardless of page size
        - Stable results even with data modifications
        - No duplicate or missing items
    Cons:
        - More complex implementation
        - No random access to pages
        - Requires sortable, unique column(s)

3. Seek Method (Advanced Cursor-Based)
    SQL: SELECT * FROM table 
         WHERE (created_at, id) > ('2024-01-15 10:30:00', 100) 
         ORDER BY created_at, id LIMIT 20
    Pros:
        - Handles duplicate values in sort column
        - Excellent performance
        - Stable pagination
    Cons:
        - Most complex to implement
        - Requires composite cursor

4. Page-Based (Offset-based with page numbers)
    SQL: Same as offset-based but with page parameter
    Pros:
        - Familiar interface for users
        - Easy to calculate: offset = (page - 1) * limit
    Cons:
        - Inherits all offset-based limitations
'''

# Offset-Based Pagination Implementation
OFFSET_PAGINATION = '''
def get_users_offset_pagination(db_session, page=1, page_size=20):
    """
    Offset-based pagination implementation.
    
    Args:
        db_session: Database session
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Tuple of (items, total_count, has_next, has_prev)
    """
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get total count for pagination info
    total_count = db_session.query(User).count()
    
    # Get paginated results
    users = db_session.query(User)\
        .order_by(User.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()
    
    # Calculate pagination metadata
    total_pages = (total_count + page_size - 1) // page_size  # Ceiling division
    has_next = page < total_pages
    has_prev = page > 1
    
    return users, total_count, has_next, has_prev

# Alternative: Return dict with pagination info
def get_users_offset_pagination_dict(db_session, page=1, page_size=20):
    """
    Offset-based pagination returning dictionary format.
    """
    offset = (page - 1) * page_size
    
    total_count = db_session.query(User).count()
    users = db_session.query(User)\
        .order_by(User.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()
    
    return {
        'items': [user.to_dict() for user in users],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_items': total_count,
            'total_pages': (total_count + page_size - 1) // page_size,
            'has_next': page < ((total_count + page_size - 1) // page_size),
            'has_prev': page > 1
        }
    }
'''

# Cursor-Based Pagination Implementation
CURSOR_PAGINATION = '''
def get_users_cursor_pagination(db_session, cursor=None, limit=20):
    """
    Cursor-based pagination implementation using ID as cursor.
    
    Args:
        db_session: Database session
        cursor: Cursor value (ID of last item from previous page)
        limit: Number of items per page
        
    Returns:
        Tuple of (items, next_cursor, has_next)
    """
    # Build query
    query = db_session.query(User).order_by(User.id.asc())
    
    # Apply cursor filter if provided
    if cursor is not None:
        query = query.filter(User.id > cursor)
    
    # Get results + 1 to check if there's a next page
    users = query.limit(limit + 1).all()
    
    # Determine if there's a next page
    has_next = len(users) > limit
    if has_next:
        users = users[:-1]  # Remove the extra item
        next_cursor = users[-1].id
    else:
        next_cursor = None
    
    return users, next_cursor, has_next

# Advanced Cursor-Based with Timestamp (handles duplicates)
def get_users_advanced_cursor_pagination(db_session, cursor_timestamp=None, cursor_id=None, limit=20):
    """
    Advanced cursor-based pagination using timestamp and ID to handle duplicates.
    
    Args:
        db_session: Database session
        cursor_timestamp: Timestamp cursor from previous page
        cursor_id: ID cursor from previous page (for tie-breaking)
        limit: Number of items per page
        
    Returns:
        Tuple of (items, next_timestamp_cursor, next_id_cursor, has_next)
    """
    # Build base query
    query = db_session.query(User).order_by(User.updated_at.desc(), User.id.desc())
    
    # Apply cursor filters
    if cursor_timestamp is not None and cursor_id is not None:
        # For descending order: get items where (timestamp, id) < (cursor_timestamp, cursor_id)
        query = query.filter(
            db_session.or_(
                User.updated_at < cursor_timestamp,
                db_session.and_(
                    User.updated_at == cursor_timestamp,
                    User.id < cursor_id
                )
            )
        )
    elif cursor_timestamp is not None:
        query = query.filter(User.updated_at < cursor_timestamp)
    
    # Get results + 1 to check for next page
    users = query.limit(limit + 1).all()
    
    # Determine next page info
    has_next = len(users) > limit
    if has_next:
        users = users[:-1]  # Remove extra item
        next_timestamp_cursor = users[-1].updated_at
        next_id_cursor = users[-1].id
    else:
        next_timestamp_cursor = None
        next_id_cursor = None
    
    return users, next_timestamp_cursor, next_id_cursor, has_next
'''

# Filtering Implementation
FILTERING_IMPLEMENTATION = '''
def filter_users(db_session, filters=None):
    """
    Filter users based on various criteria.
    
    Args:
        db_session: Database session
        filters: Dictionary of filter criteria
                Example: {
                    'is_active': True,
                    'role': 'admin',
                    'created_after': '2024-01-01',
                    'created_before': '2024-12-31',
                    'name_contains': 'John',
                    'email_domain': 'example.com'
                }
    
    Returns:
        Query object with filters applied
    """
    query = db_session.query(User)
    
    if filters is None:
        filters = {}
    
    # Boolean filters
    if 'is_active' in filters:
        query = query.filter(User.is_active == filters['is_active'])
    
    # Equality filters
    if 'role' in filters:
        query = query.filter(User.role == filters['role'])
    
    # Date range filters
    if 'created_after' in filters:
        query = query.filter(User.created_at >= filters['created_after'])
    
    if 'created_before' in filters:
        query = query.filter(User.created_at <= filters['created_before'])
    
    # String matching filters
    if 'name_contains' in filters:
        query = query.filter(User.name.contains(filters['name_contains']))
    
    if 'name_starts_with' in filters:
        query = query.filter(User.name.startswith(filters['name_starts_with']))
    
    if 'email_domain' in filters:
        query = query.filter(User.email.like(f'%@{filters["email_domain"]}'))
    
    # Numerical range filters
    if 'age_min' in filters:
        query = query.filter(User.age >= filters['age_min'])
    
    if 'age_max' in filters:
        query = query.filter(User.age <= filters['age_max'])
    
    return query

# Usage example with pagination
def get_filtered_paginated_users(db_session, page=1, page_size=20, filters=None, sort_by='created_at', sort_order='desc'):
    """
    Get filtered, sorted, and paginated users.
    
    Args:
        db_session: Database session
        page: Page number
        page_size: Items per page
        filters: Filter criteria dictionary
        sort_by: Field to sort by
        sort_order: 'asc' or 'desc'
        
    Returns:
        Dictionary with items and pagination info
    """
    # Apply filters
    query = filter_users(db_session, filters)
    
    # Apply sorting
    if hasattr(User, sort_by):
        sort_column = getattr(User, sort_by)
        if sort_order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    total_count = query.count()
    users = query.offset(offset).limit(page_size).all()
    
    # Calculate pagination info
    total_pages = (total_count + page_size - 1) // page_size
    
    return {
        'items': [user.to_dict() for user in users],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_items': total_count,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1,
            'has_filters': bool(filters),
            'sort_by': sort_by,
            'sort_order': sort_order
        },
        'filters_applied': filters or {}
    }
'''

# Sorting Implementation
SORTING_IMPLEMENTATION = '''
def apply_sorting(query, model, sort_by=None, sort_order='asc'):
    """
    Apply sorting to a query with validation.
    
    Args:
        query: SQLAlchemy query object
        model: Model class to validate sort fields against
        sort_by: Field name to sort by
        sort_order: 'asc' or 'desc'
        
    Returns:
        Query with sorting applied
    """
    if sort_by is None or not hasattr(model, sort_by):
        # Default sorting if invalid field provided
        return query.order_by(model.id.asc())
    
    sort_column = getattr(model, sort_by)
    if sort_order.lower() == 'desc':
        return query.order_by(sort_column.desc())
    else:
        return query.order_by(sort_column.asc())

# Safe sorting with whitelist
def apply_safe_sorting(query, model, sort_by=None, sort_order='asc', allowed_fields=None):
    """
    Apply sorting with field validation using whitelist.
    
    Args:
        query: SQLAlchemy query object
        model: Model class
        sort_by: Field name to sort by
        sort_order: 'asc' or 'desc'
        allowed_fields: List of allowed field names for sorting
        
    Returns:
        Query with sorting applied
    """
    if allowed_fields is None:
        # Default to all model columns if no whitelist provided
        allowed_fields = [column.name for column in model.__table__.columns]
    
    # Validate sort field
    if sort_by not in allowed_fields:
        sort_by = allowed_fields[0]  # Default to first allowed field
    
    if not hasattr(model, sort_by):
        return query.order_by(model.id.asc())
    
    sort_column = getattr(model, sort_by)
    if sort_order.lower() == 'desc':
        return query.order_by(sort_column.desc())
    else:
        return query.order_by(sort_column.asc())
'''

# Performance Considerations
PERFORMANCE_CONSIDERATIONS = '''
Performance Considerations for Pagination and Filtering:

1. Indexing Strategy:
    - Index columns used in WHERE clauses (filters)
    - Index columns used in ORDER BY clauses (sorting)
    - Consider composite indexes for common filter combinations
    - For cursor pagination, ensure the cursor column is indexed

2. Query Optimization:
    - Avoid SELECT * when you only need specific columns
    - Use EXISTS instead of COUNT for existence checks when possible
    - Consider using LIMIT/OFFSET only for small datasets
    - For large datasets, strongly consider cursor-based pagination

3. Caching Strategies:
    - Cache frequently accessed pages (especially first few pages)
    - Use cache invalidation strategies when data changes
    - Consider caching filter results for expensive computations
    - Implement ETag/Last-Modified headers for client-side caching

4. Database-Specific Optimizations:
    - Use keyset pagination where supported natively
    - Consider materialized views for complex filtered views
    - Use partitioning for large tables with temporal data
    - Implement read replicas for read-heavy workloads

5. API Design Considerations:
    - Set reasonable maximum page sizes (e.g., 100 items max)
    - Provide total count only when needed (expensive operation)
    - Consider returning approximate counts for large datasets
    - Implement timeout mechanisms for long-running queries
'''

# Best Practices
BEST_PRACTICES = '''
Best Practices for API Pagination, Filtering, and Sorting:

1. Consistency:
    - Use consistent parameter names across all endpoints
    - Standardize response format for pagination metadata
    - Maintain consistent sorting behavior

2. Documentation:
    - Clearly document all available filter, sort, and pagination options
    - Provide examples for common use cases
    - Specify data types and formats for all parameters
    - Document default values and behaviors

3. Validation:
    - Validate all input parameters (type, range, format)
    - Provide meaningful error messages for invalid inputs
    - Reject unknown filter/sort parameters (or ignore with logging)
    - Validate that sort fields exist on the model

4. Security:
    - Implement rate limiting to prevent abuse
    - Set maximum limits for page_size parameter
    - Sanitize inputs to prevent injection attacks
    - Consider timing attacks on complex queries

5. Usability:
    - Provide navigation links (first, prev, next, last) in responses
    - Include current position information
    - Support both ascending and descending sort orders
    - Allow multiple sort criteria when useful
    - Provide clear empty state handling

6. Testing:
    - Test edge cases (empty results, single item, boundary conditions)
    - Test with various filter combinations
    - Test performance with large datasets
    - Test behavior when data changes during pagination
    - Test invalid parameter handling
'''

# Example API Response Formats
RESPONSE_FORMATS = '''
Standard API Response Formats:

1. Offset-Based Response:
{
    "items": [...],
    "pagination": {
        "page": 2,
        "page_size": 20,
        "total_items": 150,
        "total_pages": 8,
        "has_next": true,
        "has_prev": true
    }
}

2. Cursor-Based Response:
{
    "items": [...],
    "pagination": {
        "next_cursor": "eyJpZCI6MTUwfQ==",
        "has_next": true
    }
}

3. Links-Based Response (HATEOAS-inspired):
{
    "items": [...],
    "pagination": {
        "current_page": 2,
        "page_size": 20,
        "total_items": 150
    },
    "links": {
        "self": "/api/users?page=2&page_size=20",
        "next": "/api/users?page=3&page_size=20",
        "prev": "/api/users?page=1&page_size=20",
        "first": "/api/users?page=1&page_size=20",
        "last": "/api/users?page=8&page_size=20"
    }
}
'''

def print_pagination_examples():
    """Print pagination and filtering examples for reference."""
    print("=== PAGINATION STRATEGIES ===")
    print(PAGINATION_STRATEGIES.strip())
    print("\n=== OFFSET-BASED PAGINATION ===")
    print(OFFSET_PAGINATION.strip())
    print("\n=== CURSOR-BASED PAGINATION ===")
    print(CURSOR_PAGINATION.strip())
    print("\n=== FILTERING IMPLEMENTATION ===")
    print(FILTERING_IMPLEMENTATION.strip())
    print("\n=== SORTING IMPLEMENTATION ===")
    print(SORTING_IMPLEMENTATION.strip())
    print("\n=== PERFORMANCE CONSIDERATIONS ===")
    print(PERFORMANCE_CONSIDERATIONS.strip())
    print("\n=== BEST PRACTICES ===")
    print(BEST_PRACTICES.strip())
    print("\n=== RESPONSE FORMATS ===")
    print(RESPONSE_FORMATS.strip())

if __name__ == "__main__":
    print_pagination_examples()
    
    # Pagination Interview Tips
    print("\n" + "="*50)
    print("API PAGINATION & FILTERING INTERVIEW TIPS:")
    print("="*50)
    print("1. Know the trade-offs between different pagination strategies")
    print("2. Understand when to use offset-based vs cursor-based pagination")
    print("3. Be able to implement basic pagination from scratch")
    print("4. Understand the importance of indexing for query performance")
    print("5. Know how to handle sorting safely (whitelist validation)")
    print("6. Understand filtering implementation patterns")
    print("7. Be familiar with standard response formats")
    print("8. Know performance considerations and optimization techniques")
    print("9. Understand how to handle edge cases (empty results, etc.)")
    print("10. Practice explaining your pagination choice based on requirements")
    print("11. Know about cursor encoding (base64, etc.) for security")
    print("12. Understand the N+1 query problem and how to avoid it")