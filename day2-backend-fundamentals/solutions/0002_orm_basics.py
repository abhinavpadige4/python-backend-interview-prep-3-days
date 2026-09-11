"""
ORM Basics Solution

Object-Relational Mapping examples using SQLAlchemy (most common Python ORM)
and Django ORM syntax for backend interview preparation.

Covers:
- Model definitions
- Relationships (One-to-Many, Many-to-Many, One-to-One)
- Field types and constraints
- Query examples
- Migration concepts
"""

# SQLAlchemy Examples
SQLALCHEMY_EXAMPLES = '''
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    posts = relationship("Post", back_populates="author")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# Order Model
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')  # pending, shipped, delivered, cancelled
    
    # Relationships
    user = relationship("User", back_populates="orders")
    
    def __repr__(self):
        return f"<Order(id={self.id}, product='{self.product_name}', total={self.total_price})>"

# Post Model (for many-to-many example)
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    published = Column(Boolean, default=False)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary="post_tags", back_populates="posts")

# Tag Model (for many-to-many)
class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    posts = relationship("Post", secondary="post_tags", back_populates="tags")

# Association table for many-to-many relationship
post_tags = Table('post_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

# Django ORM Examples
DJANGO_EXAMPLES = '''
from django.db import models
from django.contrib.auth.models import User as DjangoUser

class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Category(models.Model):
    """Product category"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Product model"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    """Order model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of purchase
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

# Query Examples
QUERY_EXAMPLES = '''
# SQLAlchemy Query Examples
def sqlalchemy_query_examples(session):
    """Examples of SQLAlchemy queries"""
    
    # Basic queries
    users = session.query(User).all()
    active_users = session.query(User).filter(User.is_active == True).all()
    user_by_email = session.query(User).filter(User.email == 'john@example.com').first()
    
    # Queries with relationships (eager loading)
    from sqlalchemy.orm import joinedload
    users_with_orders = session.query(User).options(
        joinedload(User.orders)
    ).filter(User.is_active == True).all()
    
    # Aggregation queries
    from sqlalchemy import func
    user_order_counts = session.query(
        User.username,
        func.count(Order.id).label('order_count')
    ).join(Order).group_by(User.id).all()
    
    # Filtering with related fields
    expensive_orders = session.query(Order).join(Product).filter(
        Product.price > 100.0
    ).all()
    
    # Ordering
    recent_users = session.query(User).order_by(
        User.created_at.desc()
    ).limit(10).all()
    
    # Count queries
    total_users = session.query(User).count()
    active_user_count = session.query(User).filter(
        User.is_active == True
    ).count()

# Django ORM Query Examples
def django_query_examples():
    """Examples of Django ORM queries"""
    
    # Basic queries
    all_users = User.objects.all()
    active_users = User.objects.filter(is_active=True)
    user_by_email = User.objects.get(email='john@example.com')
    
    # Related object queries
    user_orders = user.order_set.all()  # Reverse relationship
    user_orders_alt = user.orders.all()  # With related_name
    
    # Filtering with related fields
    expensive_products = Product.objects.filter(price__gt=100)
    user_expensive_orders = Order.objects.filter(
        user=user,
        product__price__gt=100
    )
    
    # Aggregation
    from django.db.models import Count, Sum, Avg
    user_stats = User.objects.annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__total_price')
    ).filter(order_count__gt=0)
    
    # Ordering
    recent_products = Product.objects.order_by('-created_at')[:10]
    
    # Complex filtering
    recent_active_users = User.objects.filter(
        is_active=True,
        date_joined__gte=timezone.now() - timedelta(days=30)
    )
    
    # Exists checks
    has_recent_orders = Order.objects.filter(
        user=user,
        order_date__gte=timezone.now() - timedelta(days=7)
    ).exists()

# Relationship Examples
RELATIONSHIP_EXAMPLES = '''
# One-to-Many (User -> Orders)
# One user can have many orders
# Access: user.orders (returns QuerySet/List of Order objects)
# Access: order.user (returns User object)

# Many-to-Many (Post <-> Tags)
# One post can have many tags, one tag can be on many posts
# Access: post.tags.all() 
# Access: tag.posts.all()

# One-to-One (User -> UserProfile)
# One user has exactly one profile
# Access: user.userprofile (returns UserProfile object or raises DoesNotExist)
# Access: userprofile.user (returns User object)

# Self-referential relationships (for hierarchical data)
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # Access: category.children.all() for subcategories
    # Access: category.parent for parent category
'''

def print_orm_examples():
    """Print ORM examples for reference."""
    print("=== SQLALCHEMY MODEL EXAMPLES ===")
    print(SQLALCHEMY_EXAMPLES.strip())
    print("\n=== DJANGO ORM MODEL EXAMPLES ===")
    print(DJANGO_EXAMPLES.strip())
    print("\n=== QUERY EXAMPLES ===")
    print(QUERY_EXAMPLES.strip())
    print("\n=== RELATIONSHIP EXAMPLES ===")
    print(RELATIONSHIP_EXAMPLES.strip())

if __name__ == "__main__":
    print_orm_examples()
    
    # ORM Interview Tips
    print("\n" + "="*50)
    print("ORM INTERVIEW TIPS:")
    print("="*50)
    print("1. Understand the three main relationship types:")
    print("   - One-to-Many (most common)")
    print("   - Many-to-Many (requires association table)")  
    print("   - One-to-One (for extending models)")
    print("")
    print("2. Always specify on_delete behavior for ForeignKeys")
    print("3. Use related_name to avoid reverse accessor conflicts")
    print("4. Understand lazy vs eager loading (N+1 query problem)")
    print("5. Know how to do aggregations and annotations")
    print("6. Understand transactions and when to use them")
    print("7. Be familiar with migration concepts")
    print("8. Know the difference between filter() and get()")
    print("9. Understand how to handle related object creation")
    print("10. Practice writing queries without looking at documentation")