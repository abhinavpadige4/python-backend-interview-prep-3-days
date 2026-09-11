"""
Design Patterns Solution

Common design patterns relevant to backend development for interview preparation.
Covers:
- Creational Patterns: Singleton, Factory, Builder
- Structural Patterns: Adapter, Decorator, Facade
- Behavioral Patterns: Observer, Strategy, Command
- Pattern selection guidelines
- Anti-patterns to avoid
"""

# Creational Patterns
CREATIONAL_PATTERNS = '''
Creational Patterns deal with object creation mechanisms.

1. Singleton Pattern
    - Ensure a class has only one instance
    - Provide global point of access to it
    - Use cases: Configuration managers, logging, database connections

2. Factory Pattern
    - Define interface for creating objects
    - Let subclasses decide which class to instantiate
    - Use cases: Object creation based on configuration, plugin systems

3. Abstract Factory Pattern
    - Provide interface for creating families of related objects
    - Without specifying their concrete classes
    - Use cases: GUI toolkits, database vendors

4. Builder Pattern
    - Separate construction of complex object from its representation
    - Allow same construction process to create different representations
    - Use cases: Complex object construction, immutable objects

5. Prototype Pattern
    - Create new objects by copying existing prototype
    - Useful when creation is expensive
    - Use cases: Object cloning, configuration templates
'''

# Singleton Pattern Examples
SINGLETON_EXAMPLES = '''
import threading
from abc import ABC, abstractmethod

# Method 1: Classic Singleton (thread-safe)
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Double-check locking
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    """Singleton database connection."""
    
    def __init__(self, connection_string="sqlite:///:memory:"):
        self.connection_string = connection_string
        self.connected = False
        print(f"DatabaseConnection initialized with {connection_string}")
    
    def connect(self):
        if not self.connected:
            print(f"Connecting to {self.connection_string}")
            self.connected = True
        return self.connected
    
    def disconnect(self):
        if self.connected:
            print(f"Disconnecting from {self.connection_string}")
            self.connected = False

# Method 2: Module-level Singleton (Pythonic)
# database.py
"""
DATABASE_CONNECTION = None

def get_database_connection():
    global DATABASE_CONNECTION
    if DATABASE_CONNECTION is None:
        DATABASE_CONNECTION = DatabaseConnection()
    return DATABASE_CONNECTION
"""

# Method 3: Borg Pattern (Shared State)
class Borg:
    """Borg pattern - all instances share state."""
    _shared_state = {}
    
    def __init__(self):
        self.__dict__ = self._shared_state

class Logger(Borg):
    """Logger using Borg pattern."""
    
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'initialized'):
            self.log_level = "INFO"
            self.handlers = []
            self.initialized = True
    
    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")

# Usage Examples
def singleton_examples():
    """Demonstrate singleton usage."""
    print("=== Singleton Pattern Examples ===")
    
    # Test DatabaseConnection singleton
    db1 = DatabaseConnection("postgresql://localhost/mydb")
    db2 = DatabaseConnection("mysql://localhost/mydb")  # Same instance!
    
    print(f"db1 is db2: {db1 is db2}")  # True
    print(f"db1.connection_string: {db1.connection_string}")
    print(f"db2.connection_string: {db2.connection_string}")  # First one wins
    
    db1.connect()
    print(f"db2.connected: {db2.connected}")  # True (same instance)
    
    # Test Logger (Borg pattern)
    logger1 = Logger()
    logger2 = Logger()
    
    print(f"\nlogger1 is logger2: {logger1 is logger2}")  # False (different instances)
    print(f"logger1.__dict__ is logger2.__dict__: {logger1.__dict__ is logger2.__dict__}")  # True (shared state)
    
    logger1.log("First message")
    logger2.log("Second message")  # Shares same state
    
    print("Singleton examples completed.")
'''

# Factory Pattern Examples
FACTORY_PATTERNS = '''
from abc import ABC, abstractmethod
from enum import Enum

# Product Interface
class NotificationSender(ABC):
    """Abstract product interface."""
    
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass

# Concrete Products
class EmailSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Sending email to {recipient}: {message}")
        # Simulate email sending
        return True

class SMSSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Sending SMS to {recipient}: {message}")
        # Simulate SMS sending
        return True

class PushNotificationSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Sending push notification to {recipient}: {message}")
        # Simulate push notification
        return True

# Creator Interface
class NotificationSenderFactory(ABC):
    """Abstract factory interface."""
    
    @abstractmethod
    def create_sender(self, notification_type: str) -> NotificationSender:
        pass

# Concrete Factory
class NotificationSenderFactoryImpl(NotificationSenderFactory):
    """Factory that creates notification senders."""
    
    def create_sender(self, notification_type: str) -> NotificationSender:
        senders = {
            'email': EmailSender(),
            'sms': SMSSender(),
            'push': PushNotificationSender()
        }
        
        sender = senders.get(notification_type.lower())
        if sender is None:
            raise ValueError(f"Unknown notification type: {notification_type}")
        
        return sender

# Factory Method Pattern (subclasses decide)
class BaseNotificationFactory(ABC):
    """Factory method pattern - subclasses implement creation."""
    
    @abstractmethod
    def create_sender(self) -> NotificationSender:
        pass
    
    def send_notification(self, recipient: str, message: str) -> bool:
        sender = self.create_sender()
        return sender.send(recipient, message)

class EmailNotificationFactory(BaseNotificationFactory):
    def create_sender(self) -> NotificationSender:
        return EmailSender()

class SMSNotificationFactory(BaseNotificationFactory):
    def create_sender(self) -> NotificationSender:
        return SMSSender()

# Simple Factory (not a formal pattern but common)
class NotificationFactory:
    """Simple factory for creating notification senders."""
    
    @staticmethod
    def create_sender(notification_type: str) -> NotificationSender:
        """Static factory method."""
        if notification_type == 'email':
            return EmailSender()
        elif notification_type == 'sms':
            return SMSSender()
        elif notification_type == 'push':
            return PushNotificationSender()
        else:
            raise ValueError(f"Unsupported notification type: {notification_type}")

# Usage Examples
def factory_examples():
    """Demonstrate factory pattern usage."""
    print("\n=== Factory Pattern Examples ===")
    
    # Abstract Factory
    factory = NotificationSenderFactoryImpl()
    
    email_sender = factory.create_sender('email')
    sms_sender = factory.create_sender('sms')
    push_sender = factory.create_sender('push')
    
    email_sender.send("user@example.com", "Welcome!")
    sms_sender.send("+1234567890", "Your code is 1234")
    push_sender.send("device_token_123", "New message!")
    
    # Factory Method
    email_factory = EmailNotificationFactory()
    sms_factory = SMSNotificationFactory()
    
    email_factory.send_notification("user@example.com", "Factory method email")
    sms_factory.send_notification("+1234567890", "Factory method SMS")
    
    # Simple Factory
    simple_sender = NotificationFactory.create_sender('email')
    simple_sender.send("test@example.com", "Simple factory email")
    
    print("Factory pattern examples completed.")
'''

# Builder Pattern Examples
BUILDER_PATTERNS = '''
from typing import Optional, List
from dataclasses import dataclass, field

# Product: Complex object to build
@dataclass
class HTTPRequest:
    """Complex HTTP request object."""
    method: str
    url: str
    headers: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    data: Optional[dict] = None
    timeout: int = 30
    verify_ssl: bool = True
    
    def __str__(self):
        return f"{self.method} {self.url}"

# Builder Interface
class HTTPRequestBuilder(ABC):
    """Abstract builder interface."""
    
    @abstractmethod
    def set_method(self, method: str) -> 'HTTPRequestBuilder':
        pass
    
    @abstractmethod
    def set_url(self, url: str) -> 'HTTPRequestBuilder':
        pass
    
    @abstractmethod
    def add_header(self, key: str, value: str) -> 'HTTPRequestBuilder':
        pass
    
    @abstractmethod
    def add_param(self, key: str, value: str) -> 'HTTPRequestBuilder':
        pass
    
    @abstractmethod
    def set_data(self, data: dict) -> 'HTTPRequestBuilder':
        pass
    
    @abstractmethod
    def set_timeout(self, timeout: int) -> 'HTTPRequestBuilder':
        pass
    
    @abstractmethod
    def set_verify_ssl(self, verify_ssl: bool) -> 'HTTPRequestBuilder':
        pass
    
    @abstractmethod
    def build(self) -> HTTPRequest:
        pass

# Concrete Builder
class ConcreteHTTPRequestBuilder(HTTPRequestBuilder):
    """Concrete builder for HTTPRequest objects."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset builder to initial state."""
        self._method = "GET"
        self._url = ""
        self._headers = {}
        self._params = {}
        self._data = None
        self._timeout = 30
        self._verify_ssl = True
    
    def set_method(self, method: str) -> 'HTTPRequestBuilder':
        self._method = method.upper()
        return self
    
    def set_url(self, url: str) -> 'HTTPRequestBuilder':
        self._url = url
        return self
    
    def add_header(self, key: str, value: str) -> 'HTTPRequestBuilder':
        self._headers[key] = value
        return self
    
    def add_param(self, key: str, value: str) -> 'HTTPRequestBuilder':
        self._params[key] = value
        return self
    
    def set_data(self, data: dict) -> 'HTTPRequestBuilder':
        self._data = data
        return self
    
    def set_timeout(self, timeout: int) -> 'HTTPRequestBuilder':
        self._timeout = timeout
        return self
    
    def set_verify_ssl(self, verify_ssl: bool) -> 'HTTPRequestBuilder':
        self._verify_ssl = verify_ssl
        return self
    
    def build(self) -> HTTPRequest:
        """Build and return the final HTTPRequest object."""
        if not self._url:
            raise ValueError("URL is required")
        
        request = HTTPRequest(
            method=self._method,
            url=self._url,
            headers=self._headers.copy(),
            params=self._params.copy(),
            data=self._data.copy() if self._data else None,
            timeout=self._timeout,
            verify_ssl=self._verify_ssl
        )
        
        # Reset for next build
        self.reset()
        return request

# Director (optional) - controls the building process
class HTTPRequestDirector:
    """Director that uses builder to create specific requests."""
    
    def __init__(self, builder: HTTPRequestBuilder):
        self.builder = builder
    
    def construct_get_request(self, url: str, params: dict = None) -> HTTPRequest:
        """Construct a GET request."""
        self.builder.reset()
        self.builder.set_method("GET")
        self.builder.set_url(url)
        if params:
            for key, value in params.items():
                self.builder.add_param(key, str(value))
        return self.builder.build()
    
    def construct_post_request(self, url: str, data: dict = None, headers: dict = None) -> HTTPRequest:
        """Construct a POST request."""
        self.builder.reset()
        self.builder.set_method("POST")
        self.builder.set_url(url)
        if data:
            self.builder.set_data(data)
        if headers:
            for key, value in headers.items():
                self.builder.add_header(key, value)
        return self.builder.build()

# Usage Examples
def builder_examples():
    """Demonstrate builder pattern usage."""
    print("\n=== Builder Pattern Examples ===")
    
    # Using builder directly
    builder = ConcreteHTTPRequestBuilder()
    
    request1 = (builder
                .set_method("POST")
                .set_url("https://api.example.com/users")
                .add_header("Content-Type", "application/json")
                .add_header("Authorization", "Bearer token123")
                .set_data({"name": "John", "email": "john@example.com"})
                .set_timeout(10)
                .build())
    
    print(f"Built request: {request1}")
    print(f"Headers: {request1.headers}")
    print(f"Data: {request1.data}")
    
    # Using director
    director = HTTPRequestDirector(ConcreteHTTPRequestBuilder())
    
    get_request = director.construct_get_request(
        "https://api.example.com/search",
        {"q": "python", "limit": "10"}
    )
    
    post_request = director.construct_post_request(
        "https://api.example.com/posts",
        {"title": "Hello World", "body": "This is a test post"},
        {"Content-Type": "application/json", "X-API-Key": "secret"}
    )
    
    print(f"GET request: {get_request}")
    print(f"POST request: {post_request}")
    
    print("Builder pattern examples completed.")
'''

# Structural Patterns
STRUCTURAL_PATTERNS = '''
Structural Patterns deal with object composition and relationships.

1. Adapter Pattern
    - Convert interface of a class into another interface clients expect
    - Lets classes work together that couldn't otherwise
    - Use cases: Integrating with legacy systems, third-party libraries

2. Decorator Pattern
    - Attach additional responsibilities to object dynamically
    - Provide flexible alternative to subclassing
    - Use cases: Adding features to objects, middleware patterns

3. Facade Pattern
    - Provide unified interface to a set of interfaces
    - Make subsystem easier to use
    - Use cases: Simplifying complex APIs, library interfaces

4. Proxy Pattern
    - Provide surrogate or placeholder for another object
    - Control access to it
    - Use cases: Lazy loading, access control, logging

5. Bridge Pattern
    - Decouple abstraction from implementation
    - Allow both to vary independently
    - Use cases: Device drivers, platform abstraction layers
'''

# Adapter Pattern Examples
ADAPTER_PATTERNS = '''
from abc import ABC, abstractmethod

# Target Interface (what client expects)
class PaymentProcessor(ABC):
    """Target interface that client code uses."""
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str = "USD") -> bool:
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        pass

# Adaptee (existing interface that needs adapting)
class LegacyPaymentGateway:
    """Legacy payment gateway with different interface."""
    
    def charge_card(self, card_number: str, amount: float, expiry: str) -> dict:
        """Process payment using legacy system."""
        print(f"Legacy gateway: Charging ${amount} to card ending in {card_number[-4:]}")
        # Simulate processing
        return {
            'success': True,
            'transaction_id': f"leg_txn_{hash(card_number) % 10000:04d}",
            'amount': amount
        }
    
    def refund_transaction(self, transaction_id: str, amount: float) -> bool:
        """Refund transaction in legacy system."""
        print(f"Legacy gateway: Refunding ${amount} for transaction {transaction_id}")
        return True

# Adapter (makes legacy interface conform to target interface)
class LegacyPaymentAdapter(PaymentProcessor):
    """Adapter that makes LegacyPaymentGateway work as PaymentProcessor."""
    
    def __init__(self, legacy_gateway: LegacyPaymentGateway):
        self.legacy_gateway = legacy_gateway
    
    def process_payment(self, amount: float, currency: str = "USD") -> bool:
        """Adapt process_payment to legacy gateway's charge_card."""
        # In real implementation, we'd need card details
        # This is simplified for demonstration
        dummy_card = "4111111111111111"  # Test card
        dummy_expiry = "12/25"
        
        result = self.legacy_gateway.charge_card(dummy_card, amount, dummy_expiry)
        return result.get('success', False)
    
    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        """Adapt refund_payment to legacy gateway's refund_transaction."""
        return self.legacy_gateway.refund_transaction(transaction_id, amount)

# Usage Examples
def adapter_examples():
    """Demonstrate adapter pattern usage."""
    print("\n=== Adapter Pattern Examples ===")
    
    # Legacy system
    legacy_gateway = LegacyPaymentGateway()
    
    # Adapter to make it conform to new interface
    payment_processor = LegacyPaymentAdapter(legacy_gateway)
    
    # Client code uses the target interface
    success = payment_processor.process_payment(99.99, "USD")
    print(f"Payment processed: {success}")
    
    refund_success = payment_processor.refund_payment("leg_txn_1234", 50.00)
    print(f"Refund processed: {refund_success}")
    
    print("Adapter pattern examples completed.")
'''

# Decorator Pattern Examples
DECORATOR_PATTERNS = '''
from abc import ABC, abstractmethod
import time
import functools

# Component Interface
class Notification(ABC):
    """Component interface."""
    
    @abstractmethod
    def send(self, message: str) -> None:
        pass

# Concrete Component
class SimpleNotification(Notification):
    """Simple notification implementation."""
    
    def send(self, message: str) -> None:
        print(f"[SIMPLE] {message}")

# Base Decorator
class NotificationDecorator(Notification, ABC):
    """Base decorator class."""
    
    def __init__(self, notification: Notification):
        self._notification = notification
    
    @abstractmethod
    def send(self, message: str) -> None:
        pass

# Concrete Decorators
class TimestampDecorator(NotificationDecorator):
    """Decorator that adds timestamp."""
    
    def send(self, message: str) -> None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        decorated_message = f"[{timestamp}] {message}"
        self._notification.send(decorated_message)

class PriorityDecorator(NotificationDecorator):
    """Decorator that adds priority level."""
    
    def __init__(self, notification: Notification, priority: str = "NORMAL"):
        super().__init__(notification)
        self.priority = priority
    
    def send(self, message: str) -> None:
        decorated_message = f"[{self.priority}] {message}"
        self._notification.send(decorated_message)

class EncryptionDecorator(NotificationDecorator):
    """Decorator that simulates encryption."""
    
    def send(self, message: str) -> None:
        # Simple simulation - in reality would use proper encryption
        encrypted_message = f"[ENCRYPTED]{message}[ENCRYPTED]"
        self._notification.send(encrypted_message)

# Usage Examples
def decorator_examples():
    """Demonstrate decorator pattern usage."""
    print("\n=== Decorator Pattern Examples ===")
    
    # Simple notification
    simple = SimpleNotification()
    simple.send("Hello World")
    
    # Decorated notifications
    timestamped = TimestampDecorator(simple)
    timestamped.send("Message with timestamp")
    
    priority_notif = PriorityDecorator(simple, "HIGH")
    priority_notif.send("High priority message")
    
    encrypted = EncryptionDecorator(simple)
    encrypted.send("Encrypted message")
    
    # Stacking decorators
    fancy_notif = TimestampDecorator(
        PriorityDecorator(
            EncryptionDecorator(simple),
            "URGENT"
        )
    )
    fancy_notif.send("Fancy decorated message")
    
    # Using functools.wraps for function decorators
    def logger(func):
        """Decorator that logs function calls."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"{func.__name__} returned {result}")
            return result
        return wrapper
    
    @logger
    def calculate_tax(amount, rate=0.1):
        """Function decorated with logger."""
        return amount * rate
    
    tax = calculate_tax(100, 0.2)
    print(f"Calculated tax: {tax}")
    
    print("Decorator pattern examples completed.")
'''

# Facade Pattern Examples
FACADE_PATTERNS = '''
# Complex subsystem classes
class UserDatabase:
    def __init__(self):
        self.users = {}
    
    def create_user(self, username, email):
        user_id = len(self.users) + 1
        self.users[user_id] = {'id': user_id, 'username': username, 'email': email}
        return user_id
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def update_user(self, user_id, **kwargs):
        if user_id in self.users:
            self.users[user_id].update(kwargs)
            return True
        return False

class EmailService:
    def __init__(self):
        self.sent_emails = []
    
    def send_welcome_email(self, user_email):
        print(f"Sending welcome email to {user_email}")
        self.sent_emails.append({'to': user_email, 'type': 'welcome'})
        return True
    
    def send_notification_email(self, user_email, subject):
        print(f"Sending notification email to {user_email}: {subject}")
        self.sent_emails.append({'to': user_email, 'type': 'notification', 'subject': subject})
        return True

class AuditLogger:
    def __init__(self):
        self.logs = []
    
    def log_user_creation(self, user_id, username):
        entry = f"USER_CREATED: {user_id} ({username})"
        self.logs.append(entry)
        print(entry)
    
    def log_user_update(self, user_id, changes):
        entry = f"USER_UPDATED: {user_id} changed {changes}"
        self.logs.append(entry)
        print(entry)

# Facade - Simplified interface to complex subsystem
class UserManagementFacade:
    """Facade providing simplified interface to user management subsystem."""
    
    def __init__(self):
        self.database = UserDatabase()
        self.email_service = EmailService()
        self.audit_logger = AuditLogger()
    
    def create_user(self, username, email):
        """Create user with welcome email and audit logging."""
        # Use subsystem components
        user_id = self.database.create_user(username, email)
        self.email_service.send_welcome_email(email)
        self.audit_logger.log_user_creation(user_id, username)
        return user_id
    
    def update_user_email(self, user_id, new_email):
        """Update user email with notification and audit logging."""
        user = self.database.get_user(user_id)
        if not user:
            return False
        
        old_email = user['email']
        success = self.database.update_user(user_id, email=new_email)
        if success:
            self.email_service.send_notification_email(
                new_email, 
                f"Email updated from {old_email}"
            )
            self.audit_logger.log_user_update(
                user_id, 
                {'email': f'{old_email} -> {new_email}'}
            )
        return success
    
    def get_user_info(self, user_id):
        """Get user information."""
        return self.database.get_user(user_id)

# Usage Examples
def facade_examples():
    """Demonstrate facade pattern usage."""
    print("\n=== Facade Pattern Examples ===")
    
    # Using facade (simple interface)
    user_mgmt = UserManagementFacade()
    
    # Complex operations made simple
    user_id = user_mgmt.create_user("john_doe", "john@example.com")
    print(f"Created user with ID: {user_id}")
    
    email_updated = user_mgmt.update_user_email(user_id, "john.new@example.com")
    print(f"Email updated: {email_updated}")
    
    user_info = user_mgmt.get_user_info(user_id)
    print(f"User info: {user_info}")
    
    print("Facade pattern examples completed.")
'''

# Behavioral Patterns
BEHAVIORAL_PATTERNS = '''
Behavioral Patterns deal with communication between objects.

1. Observer Pattern
    - Define one-to-many dependency between objects
    - When one object changes state, all dependents are notified
    - Use cases: Event handling, MVC, publish-subscribe systems

2. Strategy Pattern
    - Define family of algorithms, encapsulate each one
    - Make them interchangeable
    - Use cases: Different sorting algorithms, payment strategies

3. Command Pattern
    - Encapsulate request as object
    - Allow parameterization of clients with different requests
    - Use cases: Undo/redo, job queues, transactional systems

4. Template Method Pattern
    - Define skeleton of algorithm in method
    - Defer some steps to subclasses
    - Use cases: Framework hooks, algorithm templates

5. Iterator Pattern
    - Provide way to access elements of aggregate object
    - Without exposing underlying representation
    - Use cases: Custom collections, traversal algorithms
'''

# Observer Pattern Examples
OBSERVER_PATTERNS = '''
from abc import ABC, abstractmethod
from typing import List, Callable

# Subject Interface
class Subject(ABC):
    """Subject that maintains list of observers."""
    
    @abstractmethod
    def attach(self, observer: 'Observer') -> None:
        pass
    
    @abstractmethod
    def detach(self, observer: 'Observer') -> None:
        pass
    
    @abstractmethod
    def notify(self) -> None:
        pass

# Observer Interface
class Observer(ABC):
    """Observer that receives updates from subject."""
    
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass

# Concrete Subject
class StockMarket(Subject):
    """Stock market that notifies observers of price changes."""
    
    def __init__(self):
        self._observers: List[Observer] = []
        self._stock_prices = {}
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)
    
    def set_stock_price(self, symbol: str, price: float) -> None:
        """Set stock price and notify observers."""
        old_price = self._stock_prices.get(symbol)
        self._stock_prices[symbol] = price
        print(f"Stock {symbol}: ${old_price} -> ${price}")
        self.notify()
    
    def get_stock_price(self, symbol: str) -> float:
        return self._stock_prices.get(symbol, 0.0)

# Concrete Observers
class MobileApp(Observer):
    """Mobile app that displays stock prices."""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.displayed_prices = {}
    
    def update(self, subject: Subject) -> None:
        # In reality, would get specific stock data
        # For demo, we'll show all prices
        print(f"[{self.app_name}] Updating stock prices...")
        for symbol, price in subject._stock_prices.items():
            self.displayed_prices[symbol] = price
            print(f"  {symbol}: ${price}")

class WebDashboard(Observer):
    """Web dashboard that shows stock alerts."""
    
    def __init__(self, dashboard_name: str):
        self.dashboard_name = dashboard_name
        self.alerts = []
    
    def update(self, subject: Subject) -> None:
        print(f"[{self.dashboard_name}] Checking for alerts...")
        for symbol, price in subject._stock_prices.items():
            if price > 100.0:  # Arbitrary threshold
                alert = f"HIGH PRICE ALERT: {symbol} at ${price}"
                self.alerts.append(alert)
                print(f"  {alert}")

class TradingAlgorithm(Observer):
    """Trading algorithm that makes decisions based on prices."""
    
    def __init__(self, name: str):
        self.name = name
        self.trades = []
    
    def update(self, subject: Subject) -> None:
        print(f"[{self.name}] Evaluating trading opportunities...")
        # Simple strategy: buy low, sell high
        for symbol, price in subject._stock_prices.items():
            if price < 50.0:  # Buy signal
                trade = f"BUY {symbol} at ${price}"
                self.trades.append(trade)
                print(f"  {trade}")
            elif price > 150.0:  # Sell signal
                trade = f"SELL {symbol} at ${price}"
                self.trades.append(trade)
                print(f"  {trade}")

# Usage Examples
def observer_examples():
    """Demonstrate observer pattern usage."""
    print("\n=== Observer Pattern Examples ===")
    
    # Create subject
    market = StockMarket()
    
    # Create observers
    mobile_app = MobileApp("TradingApp")
    web_dashboard = WebDashboard("FinanceDashboard")
    trading_algo = TradingAlgorithm("QuantBot")
    
    # Attach observers
    market.attach(mobile_app)
    market.attach(web_dashboard)
    market.attach(trading_algo)
    
    # Change stock prices - observers will be notified
    print("Setting stock prices...")
    market.set_stock_price("AAPL", 150.0)
    market.set_stock_price("GOOGL", 1200.0)
    market.set_stock_price("TSLA", 800.0)
    market.set_stock_price("AMZN", 3200.0)
    
    # Add another stock
    market.set_stock_price("MSFT", 300.0)
    
    # Detach one observer
    market.detach(web_dashboard)
    print("\nAfter detaching web dashboard:")
    market.set_stock_price("GME", 50.0)  # Only mobile app and trading algo notified
    
    print(f"\nMobile app displayed prices: {mobile_app.displayed_prices}")
    print(f"Web dashboard alerts: {web_dashboard.alerts}")
    print(f"Trading algorithm trades: {trading_algo.trades}")
    
    print("Observer pattern examples completed.")
'''

# Strategy Pattern Examples
STRATEGY_PATTERNS = '''
from abc import ABC, abstractmethod
from typing import List

# Strategy Interface
class SortingStrategy(ABC):
    """Strategy interface for sorting algorithms."""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

# Concrete Strategies
class BubbleSortStrategy(SortingStrategy):
    def sort(self, data: List[int]) -> List[int]:
        """Bubble sort implementation."""
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class QuickSortStrategy(SortingStrategy):
    def sort(self, data: List[int]) -> List[int]:
        """Quick sort implementation."""
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)
    
    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)

class MergeSortStrategy(SortingStrategy):
    def sort(self, data: List[int]) -> List[int]:
        """Merge sort implementation."""
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self.merge_sort(data[:mid])
        right = self.merge_sort(data[mid:])
        return self._merge(left, right)
    
    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

# Context
class SortingContext:
    """Context that uses a sorting strategy."""
    
    def __init__(self, strategy: SortingStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortingStrategy):
        """Change the strategy at runtime."""
        self._strategy = strategy
    
    def sort_data(self, data: List[int]) -> List[int]:
        """Execute the strategy."""
        return self._strategy.sort(data)

# Usage Examples
def strategy_examples():
    """Demonstrate strategy pattern usage."""
    print("\n=== Strategy Pattern Examples ===")
    
    # Test data
    data = [64, 34, 25, 12, 22, 11, 90, 5]
    print(f"Original data: {data}")
    
    # Context with different strategies
    context = SortingContext(BubbleSortStrategy())
    bubble_sorted = context.sort_data(data)
    print(f"Bubble sort: {bubble_sorted}")
    
    context.set_strategy(QuickSortStrategy())
    quick_sorted = context.sort_data(data)
    print(f"Quick sort: {quick_sorted}")
    
    context.set_strategy(MergeSortStrategy())
    merge_sorted = context.sort_data(data)
    print(f"Merge sort: {merge_sorted}")
    
    # Verify all produce same result
    expected = sorted(data)
    print(f"Expected: {expected}")
    print(f"All strategies correct: {bubble_sorted == quick_sorted == merge_sorted == expected}")
    
    print("Strategy pattern examples completed.")
'''

# Anti-Patterns to Avoid
ANTI_PATTERNS = '''
Common Anti-Patterns in Backend Development:

1. God Object
    - Single class that knows too much or does too much
    - Violates Single Responsibility Principle
    - Solution: Split into smaller, focused classes

2. Spaghetti Code
    - Complex, tangled control flow
    - Difficult to follow and maintain
    - Solution: Refactor into functions/methods with clear purposes

3. Magic Numbers/String Literals
    - Hard-coded values scattered throughout code
    - Solution: Use constants or configuration files

4. Copy-Paste Programming
    - Duplicating code instead of creating reusable functions
    - Solution: Extract common functionality into reusable components

5. Premature Optimization
    - Optimizing before identifying actual bottlenecks
    - Solution: Measure first, then optimize where needed

6. Boat Anchor
    - Keeping unused or obsolete code "just in case"
    - Solution: Remove dead code regularly

7. Golden Hammer
    - Using familiar tool/technology for every problem
    - Solution: Learn and use appropriate tools for each job

8. Poltergeists
    - Classes with very limited lifespan and effectiveness
    - Solution: Combine responsibilities or eliminate unnecessary classes

9. Race Conditions
    - Concurrent access to shared state without proper synchronization
    - Solution: Use locks, semaphores, or thread-safe data structures

10. N+1 Query Problem
    - Making N+1 database queries instead of using joins or batching
    - Solution: Use eager loading, joins, or batch queries
'''

def print_design_patterns_examples():
    """Print design patterns examples for reference."""
    print("=== CREATIONAL PATTERNS ===")
    print(CREATIONAL_PATTERNS.strip())
    print("\n=== SINGLETON PATTERN EXAMPLES ===")
    print(SINGLETON_EXAMPLES.strip())
    print("\n=== FACTORY PATTERN EXAMPLES ===")
    print(FACTORY_PATTERNS.strip())
    print("\n=== BUILDER PATTERN EXAMPLES ===")
    print(BUILDER_PATTERNS.strip())
    print("\n=== STRUCTURAL PATTERNS ===")
    print(STRUCTURAL_PATTERNS.strip())
    print("\n=== ADAPTER PATTERN EXAMPLES ===")
    print(ADAPTER_PATTERNS.strip())
    print("\n=== DECORATOR PATTERN EXAMPLES ===")
    print(DECORATOR_PATTERNS.strip())
    print("\n=== FACADE PATTERN EXAMPLES ===")
    print(FACADE_PATTERNS.strip())
    print("\n=== BEHAVIORAL PATTERNS ===")
    print(BEHAVIORAL_PATTERNS.strip())
    print("\n=== OBSERVER PATTERN EXAMPLES ===")
    print(OBSERVER_PATTERNS.strip())
    print("\n=== STRATEGY PATTERN EXAMPLES ===")
    print(STRATEGY_PATTERNS.strip())
    print("\n=== ANTI-PATTERNS TO AVOID ===")
    print(ANTI_PATTERNS.strip())

if __name__ == "__main__":
    print_design_patterns_examples()
    
    # Design Patterns Interview Tips
    print("\n" + "="*50)
    print("DESIGN PATTERNS INTERVIEW TIPS:")
    print("="*50)
    print("1. Understand the problem each pattern solves")
    print("2. Know the structural elements of each pattern")
    print("3. Be able to identify when to apply each pattern")
    print("4. Understand the trade-offs and drawbacks of patterns")
    print("5. Practice implementing patterns from scratch")
    print("6. Know the difference between similar patterns")
    print("7. Understand creational vs structural vs behavioral patterns")
    print("8. Be familiar with the most commonly used patterns")
    print("9. Know when NOT to use a pattern (simplicity over complexity)")
    print("10. Understand how patterns relate to SOLID principles")
    print("11. Be able to refactor code to use appropriate patterns")
    print("12. Know about dependency injection and its relation to patterns")
    print("13. Practice explaining patterns using real-world analogies")
    print("14. Understand language-specific implementations (Python vs Java)")