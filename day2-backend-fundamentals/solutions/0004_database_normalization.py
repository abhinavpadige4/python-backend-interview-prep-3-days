"""
Database Normalization Solution

Database normalization concepts and examples for backend interview preparation.
Covers:
- Normalization forms (1NF, 2NF, 3NF, BCNF)
- Denormalization trade-offs
- Functional dependencies
- Anomalies (insertion, update, deletion)
- Practical normalization examples
"""

# Normalization Concepts
NORMALIZATION_CONCEPTS = '''
Database Normalization:

Purpose: Organize data to minimize redundancy and dependency
Goals:
- Eliminate redundant data
- Ensure data dependencies make sense
- Protect data integrity
- Make database more flexible

Normal Forms:
1NF (First Normal Form): Atomic values, no repeating groups
2NF (Second Normal Form): 1NF + no partial dependencies
3NF (Third Normal Form): 2NF + no transitive dependencies
BCNF (Boyce-Codd Normal Form): Stronger version of 3NF

Anomalies that normalization prevents:
- Insertion anomalies: Cannot add data without unrelated data
- Update anomalies: Need to update same data in multiple places
- Deletion anomalies: Losing related data when deleting records
'''

# Functional Dependencies
FUNCTIONAL_DEPENDENCIES = '''
Functional Dependencies:

Definition: Attribute B is functionally dependent on attribute A 
if each value of A is associated with exactly one value of B.
Notation: A → B

Types:
- Trivial dependency: A → A (always true)
- Non-trivial dependency: A → B where B is not subset of A
- Full functional dependency: A → B and no subset of A determines B
- Partial dependency: A → B but some subset of A also determines B
- Transitive dependency: A → B and B → C, therefore A → C

Examples:
- StudentID → StudentName, Major (full dependency)
- {StudentID, Course} → Grade (full dependency)
- Course → InstructorName (might be partial if Course determines Department which determines Instructor)
'''

# Normal Forms Explained
NORMAL_FORMS = '''
1NF (First Normal Form):
    - Each column contains atomic (indivisible) values
    - Each row is unique (no duplicate rows)
    - No repeating groups or arrays
    - Example violation: Storing multiple phone numbers in one column

2NF (Second Normal Form):
    - Must be in 1NF
    - No partial dependencies: No non-key attribute depends on 
      only part of a composite primary key
    - Example violation: In table (StudentID, Course, InstructorName, Grade),
      if InstructorName depends only on Course (not StudentID)

3NF (Third Normal Form):
    - Must be in 2NF
    - No transitive dependencies: No non-key attribute depends on 
      another non-key attribute
    - Example violation: Employee → Department → DepartmentLocation
      (Employee determines Department, Department determines Location)

BCNF (Boyce-Codd Normal Form):
    - Stronger than 3NF
    - For every dependency A → B, A must be a superkey
    - Addresses certain anomalies that 3NF doesn't handle
'''

# Denormalization
DENORMALIZATION = '''
Denormalization:

Intentional introduction of redundancy to improve performance
Trade-offs:
    Pros: 
        - Improved query performance (fewer JOINs)
        - Simpler queries
        - Better read performance
    Cons:
        - Increased storage requirements
        - Risk of data inconsistency
        - More complex update logic
        - Need to maintain redundancy

When to denormalize:
    - Heavy read workloads with infrequent writes
    - Reporting and analytics workloads
    - When JOIN performance becomes bottleneck
    - Caching frequently accessed computed values

Examples:
    - Storing total order amount in Orders table (instead of calculating from OrderItems)
    - Storing user name in Comments table (instead of JOINing with Users)
    - Pre-computed aggregates for dashboards
'''

# Practical Examples
PRACTICAL_EXAMPLES = '''
Example 1: Unnormalized Table (Violates 1NF)
-----------------------------------------
StudentCourses:
- StudentID
- StudentName
- Major
- Courses (contains comma-separated values like "Math,Physics,CS")
- Grades (contains comma-separated values like "A,B+,A-")

Problems:
    - Violates 1NF (non-atomic values)
    - Difficult to query specific course/grade
    - Update anomalies: Changing student name requires updating all rows
    - Insertion anomalies: Can't add course for new student without grades

Normalized Solution (1NF):
-----------------------------------------
Students:
- StudentID (PK)
- StudentName
- Major

Courses:
- CourseID (PK)
- CourseName
- Credits

Enrollments:
- EnrollmentID (PK)
- StudentID (FK)
- CourseID (FK)
- Grade

Example 2: Violating 2NF
-----------------------------------------
OrderDetails (with composite key OrderID, ProductID):
- OrderID (PK, part of composite)
- ProductID (PK, part of composite)
- ProductName
- Quantity
- UnitPrice
- TotalPrice

Problems:
    - ProductName depends only on ProductID (part of key) → Partial dependency
    - UnitPrice depends only on ProductID (part of key) → Partial dependency
    - TotalPrice depends on Quantity and UnitPrice (both non-key) → OK

Normalized Solution (2NF):
-----------------------------------------
Orders:
- OrderID (PK)
- OrderDate
- CustomerID

Products:
- ProductID (PK)
- ProductName
- UnitPrice

OrderDetails:
- OrderID (FK)
- ProductID (FK)
- Quantity
- TotalPrice (calculated or stored)

Example 3: Violating 3NF
-----------------------------------------
Employees:
- EmployeeID (PK)
- EmployeeName
- DepartmentID
- DepartmentName
- DepartmentLocation

Problems:
    - DepartmentName depends on DepartmentID (non-key → non-key)
    - DepartmentLocation depends on DepartmentID (non-key → non-key)
    - Transitive dependency: EmployeeID → DepartmentID → DepartmentName/Location

Normalized Solution (3NF):
-----------------------------------------
Employees:
- EmployeeID (PK)
- EmployeeName
- DepartmentID (FK)

Departments:
- DepartmentID (PK)
- DepartmentName
- DepartmentLocation

Example 4: Many-to-Many Relationship
-----------------------------------------
Unnormalized:
- StudentID
- StudentName
- Course1, Course2, Course3 (repeating groups)
- Grade1, Grade2, Grade3

Problems:
    - Violates 1NF (repeating groups)
    - Fixed number of courses limit
    - Difficult to query

Normalized Solution:
-----------------------------------------
Students:
- StudentID (PK)
- StudentName

Courses:
- CourseID (PK)
- CourseName

Enrollments:
- StudentID (FK)
- CourseID (FK)
- Grade
- EnrollmentDate
'''

# Normalization Process
NORMALIZATION_PROCESS = '''
Steps to Normalize a Database:

1. Identify all entities and their attributes
2. Determine primary keys for each entity
3. Identify functional dependencies
4. Apply normalization rules iteratively:
    - First achieve 1NF
    - Then achieve 2NF
    - Then achieve 3NF
    - Consider BCNF if needed
5. Validate the design:
    - Check for insert/update/delete anomalies
    - Verify all dependencies are correct
    - Ensure queries can be efficiently executed
6. Consider denormalization for performance if needed

Tools and Techniques:
- Entity-Relationship (ER) diagrams
- Functional dependency analysis
- Normalization algorithms
- Database design tools (MySQL Workbench, pgAdmin, etc.)
'''

# Interview Questions and Answers
INTERVIEW_QA = '''
Common Database Normalization Interview Questions:

Q: What is the difference between 2NF and 3NF?
A: 2NF eliminates partial dependencies (non-key attributes depending on 
   part of composite key). 3NF eliminates transitive dependencies 
   (non-key attributes depending on other non-key attributes).

Q: When would you denormalize a database?
A: Denormalize when read performance is critical and you can tolerate 
   some data redundancy. Common in reporting systems, data warehouses, 
   and applications with heavy read loads.

Q: What is a transitive dependency?
A: A transitive dependency occurs when A → B and B → C, therefore A → C.
   In normalization terms, this means a non-key attribute depends on 
   another non-key attribute.

Q: How do you handle many-to-many relationships in normalization?
A: Create a junction table (associative entity) with foreign keys 
   to both related tables. This eliminates repeating groups and 
   maintains referential integrity.

Q: What is BCNF and when is it needed?
A: BCNF (Boyce-Codd Normal Form) is a stronger version of 3NF where 
   every determinant must be a candidate key. It's needed when 
   3NF doesn't eliminate all anomalies due to overlapping candidate keys.
'''

def print_normalization_examples():
    """Print database normalization examples for reference."""
    print("=== NORMALIZATION CONCEPTS ===")
    print(NORMALIZATION_CONCEPTS.strip())
    print("\n=== FUNCTIONAL DEPENDENCIES ===")
    print(FUNCTIONAL_DEPENDENCIES.strip())
    print("\n=== NORMAL FORMS ===")
    print(NORMAL_FORMS.strip())
    print("\n=== DENORMALIZATION ===")
    print(DENORMALIZATION.strip())
    print("\n=== PRACTICAL EXAMPLES ===")
    print(PRACTICAL_EXAMPLES.strip())
    print("\n=== NORMALIZATION PROCESS ===")
    print(NORMALIZATION_PROCESS.strip())
    print("\n=== INTERVIEW Q&A ===")
    print(INTERVIEW_QA.strip())

if __name__ == "__main__":
    print_normalization_examples()
    
    # Normalization Interview Tips
    print("\n" + "="*50)
    print("DATABASE NORMALIZATION INTERVIEW TIPS:")
    print("="*50)
    print("1. Understand the purpose behind each normal form")
    print("2. Be able to identify violations in sample tables")
    print("3. Know how to decompose tables to achieve higher normal forms")
    print("4. Understand the trade-offs of normalization vs denormalization")
    print("5. Practice with real-world examples (orders, users, products)")
    print("6. Remember that normalization is about reducing redundancy")
    print("7. Know the difference between partial and transitive dependencies")
    print("8. Be ready to explain why we normalize (anomaly prevention)")
    print("9. Understand when denormalization makes sense")
    print("10. Practice drawing ER diagrams from requirements")