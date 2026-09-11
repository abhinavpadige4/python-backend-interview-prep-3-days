"""
Testing Fundamentals Solution

Testing concepts and implementations for backend interview preparation.
Covers:
- Unit testing with unittest and pytest
- Test organization and structure
- Mocking and patching
- Test-driven development (TDD)
- Fixtures and setup/teardown
- Integration testing concepts
- Code coverage and test quality
"""

# Testing Frameworks Overview
TESTING_FRAMEWORKS = '''
Testing Frameworks in Python:

1. unittest (built-in)
    - Part of Python standard library
    - Inspired by JUnit
    - Uses test classes and methods
    - Requires boilerplate code
    - Good for simple testing needs

2. pytest (most popular)
    - Third-party framework
    - More concise and readable syntax
    - Powerful fixture system
    - Excellent plugin ecosystem
    - Automatic test discovery
    - Better error reporting

3. doctest
    - Tests embedded in docstrings
    - Good for documentation testing
    - Limited for complex testing scenarios

4. nose2
    - Extension of unittest
    - Plugin-based architecture
    - Less commonly used now

Recommendation: Use pytest for most backend testing scenarios
'''

# Basic Unit Testing Examples
UNIT_TESTING_EXAMPLES = '''
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest

# Example class to test
class UserService:
    """Example service class for testing."""
    
    def __init__(self, database=None):
        self.database = database or MockDatabase()
    
    def get_user_by_id(self, user_id):
        """Get user by ID."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
        return self.database.get_user(user_id)
    
    def create_user(self, name, email):
        """Create a new user."""
        if not name or not email:
            raise ValueError("Name and email are required")
        if "@" not in email:
            raise ValueError("Invalid email format")
        
        user_id = self.database.get_next_id()
        user = {
            'id': user_id,
            'name': name,
            'email': email,
            'created_at': '2024-01-01T00:00:00Z'
        }
        self.database.save_user(user)
        return user
    
    def update_user_email(self, user_id, new_email):
        """Update user's email."""
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email format")
        
        user = self.get_user_by_id(user_id)
        user['email'] = new_email
        self.database.update_user(user)
        return user
    
    def is_valid_email(self, email):
        """Simple email validation."""
        return "@" in email and "." in email.split("@")[-1]

class MockDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def save_user(self, user):
        self.users[user['id']] = user
    
    def update_user(self, user):
        self.users[user['id']] = user
    
    def get_next_id(self):
        current_id = self.next_id
        self.next_id += 1
        return current_id

# unittest Examples
class TestUserServiceUnittest(unittest.TestCase):
    """Unit tests using unittest framework."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.service = UserService()
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def test_get_user_by_id_valid(self):
        """Test getting a valid user."""
        # Arrange
        test_user = {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}
        self.service.database.users[1] = test_user
        
        # Act
        result = self.service.get_user_by_id(1)
        
        # Assert
        self.assertEqual(result, test_user)
        self.assertIn('name', result)
        self.assertEqual(result['email'], 'john@example.com')
    
    def test_get_user_by_id_invalid(self):
        """Test getting user with invalid ID."""
        # Test various invalid inputs
        invalid_ids = [0, -1, 'abc', None]
        
        for invalid_id in invalid_ids:
            with self.subTest(invalid_id=invalid_id):
                with self.assertRaises(ValueError):
                    self.service.get_user_by_id(invalid_id)
    
    def test_create_user_success(self):
        """Test successful user creation."""
        # Act
        result = self.service.create_user('Jane Smith', 'jane@example.com')
        
        # Assert
        self.assertEqual(result['name'], 'Jane Smith')
        self.assertEqual(result['email'], 'jane@example.com')
        self.assertEqual(result['id'], 1)
        self.assertIn('created_at', result)
        
        # Verify user was saved
        self.assertIn(1, self.service.database.users)
        self.assertEqual(self.service.database.users[1]['name'], 'Jane Smith')
    
    def test_create_user_validation(self):
        """Test user creation validation."""
        # Test missing name
        with self.assertRaises(ValueError) as context:
            self.service.create_user('', 'test@example.com')
        self.assertIn('Name and email are required', str(context.exception))
        
        # Test missing email
        with self.assertRaises(ValueError) as context:
            self.service.create_user('John Doe', '')
        self.assertIn('Name and email are required', str(context.exception))
        
        # Test invalid email
        with self.assertRaises(ValueError) as context:
            self.service.create_user('John Doe', 'invalid-email')
        self.assertIn('Invalid email format', str(context.exception))
    
    def test_update_user_email(self):
        """Test updating user email."""
        # Arrange
        test_user = {'id': 1, 'name': 'John Doe', 'email': 'old@example.com'}
        self.service.database.users[1] = test_user
        
        # Act
        result = self.service.update_user_email(1, 'new@example.com')
        
        # Assert
        self.assertEqual(result['email'], 'new@example.com')
        self.assertEqual(self.service.database.users[1]['email'], 'new@example.com')
    
    def test_update_user_email_invalid(self):
        """Test updating user with invalid email."""
        # Arrange
        test_user = {'id': 1, 'name': 'John Doe', 'email': 'test@example.com'}
        self.service.database.users[1] = test_user
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.update_user_email(1, 'invalid-email')
        self.assertIn('Invalid email format', str(context.exception))

# pytest Examples
class TestUserServicePytest:
    """Unit tests using pytest framework."""
    
    def setup_method(self):
        """Set up before each test method."""
        self.service = UserService()
    
    def teardown_method(self):
        """Clean up after each test method."""
        pass
    
    def test_get_user_by_id_valid(self):
        """Test getting a valid user."""
        # Arrange
        test_user = {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}
        self.service.database.users[1] = test_user
        
        # Act
        result = self.service.get_user_by_id(1)
        
        # Assert
        assert result == test_user
        assert 'name' in result
        assert result['email'] == 'john@example.com'
    
    def test_get_user_by_id_invalid(self):
        """Test getting user with invalid ID."""
        invalid_ids = [0, -1, 'abc', None]
        
        for invalid_id in invalid_ids:
            with pytest.raises(ValueError):
                self.service.get_user_by_id(invalid_id)
    
    def test_create_user_success(self):
        """Test successful user creation."""
        # Act
        result = self.service.create_user('Jane Smith', 'jane@example.com')
        
        # Assert
        assert result['name'] == 'Jane Smith'
        assert result['email'] == 'jane@example.com'
        assert result['id'] == 1
        assert 'created_at' in result
        
        # Verify user was saved
        assert 1 in self.service.database.users
        assert self.service.database.users[1]['name'] == 'Jane Smith'
    
    def test_create_user_validation(self):
        """Test user creation validation."""
        # Test missing name
        with pytest.raises(ValueError, match='Name and email are required'):
            self.service.create_user('', 'test@example.com')
        
        # Test missing email
        with pytest.raises(ValueError, match='Name and email are required'):
            self.service.create_user('John Doe', '')
        
        # Test invalid email
        with pytest.raises(ValueError, match='Invalid email format'):
            self.service.create_user('John Doe', 'invalid-email')
    
    @pytest.mark.parametrize("name,email,expected_error", [
        ("", "test@example.com", "Name and email are required"),
        ("John Doe", "", "Name and email are required"),
        ("John Doe", "invalid-email", "Invalid email format"),
    ])
    def test_create_user_validation_parametrized(self, name, email, expected_error):
        """Parametrized test for user creation validation."""
        with pytest.raises(ValueError, match=expected_error):
            self.service.create_user(name, email)
    
    def test_update_user_email(self):
        """Test updating user email."""
        # Arrange
        test_user = {'id': 1, 'name': 'John Doe', 'email': 'old@example.com'}
        self.service.database.users[1] = test_user
        
        # Act
        result = self.service.update_user_email(1, 'new@example.com')
        
        # Assert
        assert result['email'] == 'new@example.com'
        assert self.service.database.users[1]['email'] == 'new@example.com'
    
    def test_update_user_email_invalid(self):
        """Test updating user with invalid email."""
        # Arrange
        test_user = {'id': 1, 'name': 'John Doe', 'email': 'test@example.com'}
        self.service.database.users[1] = test_user
        
        # Act & Assert
        with pytest.raises(ValueError, match='Invalid email format'):
            self.service.update_user_email(1, 'invalid-email')

# Fixtures Examples
FIXTURES_EXAMPLES = '''
import pytest

@pytest.fixture
def user_service():
    """Fixture providing a UserService instance."""
    return UserService()

@pytest.fixture
def mock_database():
    """Fixture providing a mock database."""
    class MockDatabase:
        def __init__(self):
            self.users = {}
            self.next_id = 1
        
        def get_user(self, user_id):
            return self.users.get(user_id)
        
        def save_user(self, user):
            self.users[user['id']] = user
        
        def update_user(self, user):
            self.users[user['id']] = user
        
        def get_next_id(self):
            current_id = self.next_id
            self.next_id += 1
            return current_id
    
    return MockDatabase()

@pytest.fixture
def user_service_with_mock(mock_database):
    """Fixture providing UserService with mock database."""
    return UserService(database=mock_database)

@pytest.fixture
def sample_user_data():
    """Fixture providing sample user data."""
    return {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com',
        'created_at': '2024-01-01T00:00:00Z'
    }

# Using fixtures in tests
def test_get_user_with_fixture(user_service_with_mock, sample_user_data):
    """Test using fixtures."""
    # Arrange
    user_service_with_mock.database.users[1] = sample_user_data
    
    # Act
    result = user_service_with_mock.get_user_by_id(1)
    
    # Assert
    assert result == sample_user_data

def test_create_user_with_fixture(user_service_with_mock):
    """Test user creation with fixtures."""
    # Act
    result = user_service_with_mock.create_user('Jane Smith', 'jane@example.com')
    
    # Assert
    assert result['name'] == 'Jane Smith'
    assert result['email'] == 'jane@example.com'
    assert result['id'] == 1
'''

# Mocking and Patching Examples
MOCKING_EXAMPLES = '''
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
import requests

# Example service that makes HTTP requests
class WeatherService:
    """Service that fetches weather data from external API."""
    
    BASE_URL = "https://api.weatherapi.com/v1"
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_current_weather(self, city):
        """Get current weather for a city."""
        url = f"{self.BASE_URL}/current.json"
        params = {
            'key': self.api_key,
            'q': city
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code}")
    
    def get_forecast(self, city, days=3):
        """Get weather forecast."""
        url = f"{self.BASE_URL}/forecast.json"
        params = {
            'key': self.api_key,
            'q': city,
            'days': days
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code}")

# Mocking Examples
class TestWeatherServiceMocking(unittest.TestCase):
    """Tests demonstrating various mocking techniques."""
    
    def setUp(self):
        self.service = WeatherService("test-api-key")
    
    @patch('requests.get')
    def test_get_current_weather_success(self, mock_get):
        """Test successful weather request using patch decorator."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'location': {'name': 'London'},
            'current': {'temp_c': 20, 'condition': {'text': 'Sunny'}}
        }
        mock_get.return_value = mock_response
        
        # Act
        result = self.service.get_current_weather('London')
        
        # Assert
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params']['q'], 'London')
        self.assertEqual(result['location']['name'], 'London')
        self.assertEqual(result['current']['temp_c'], 20)
    
    @patch('requests.get')
    def test_get_current_weather_failure(self, mock_get):
        """Test failed weather request."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.service.get_current_weather('NonexistentCity')
        self.assertIn('API request failed', str(context.exception))
    
    def test_get_current_weather_with_context_manager(self):
        """Test using patch as context manager."""
        with patch('requests.get') as mock_get:
            # Arrange
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'location': {'name': 'Paris'},
                'current': {'temp_c': 25, 'condition': {'text': 'Cloudy'}}
            }
            mock_get.return_value = mock_response
            
            # Act
            result = self.service.get_current_weather('Paris')
            
            # Assert
            mock_get.assert_called_once()
            assert result['location']['name'] == 'Paris'

# Pytest Mocking Examples
class TestWeatherServicePytestMocking:
    """Pytest examples for mocking."""
    
    def setup_method(self):
        self.service = WeatherService("test-api-key")
    
    def test_get_current_weather_with_patch(self, mocker):
        """Test using pytest-mock plugin."""
        # Arrange
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'location': {'name': 'Tokyo'},
            'current': {'temp_c': 18, 'condition': {'text': 'Rainy'}}
        }
        mocker.patch('requests.get', return_value=mock_response)
        
        # Act
        result = self.service.get_current_weather('Tokyo')
        
        # Assert
        assert result['location']['name'] == 'Tokyo'
        assert result['current']['temp_c'] == 18
    
    def test_multiple_calls_with_side_effect(self, mocker):
        """Test using side_effect for multiple return values."""
        # Arrange
        mock_responses = [
            mocker.Mock(status_code=200, json=lambda: {'temp': 20}),
            mocker.Mock(status_code=200, json=lambda: {'temp': 25}),
            mocker.Mock(status_code=404)  # Error case
        ]
        mocker.patch('requests.get', side_effect=mock_responses)
        
        # Act & Assert
        result1 = self.service.get_current_weather('City1')
        result2 = self.service.get_current_weather('City2')
        
        assert result1['temp'] == 20
        assert result2['temp'] == 25
        
        # Third call should raise exception
        with pytest.raises(Exception):
            self.service.get_current_weather('City3')

# Test-Driven Development (TDD) Example
TDD_EXAMPLE = '''
# TDD Example: String Calculator
# Requirements:
# 1. Empty string returns 0
# 2. Single number returns the number
# 3. Two numbers separated by comma returns sum
# 4. Newlines instead of commas also work
# 5. Support different delimiters
# 6. Negative numbers throw exception

class StringCalculator:
    def add(self, numbers: str) -> int:
        """Add numbers from string format."""
        if not numbers:
            return 0
        
        # Handle custom delimiter
        delimiter = ","
        if numbers.startswith("//"):
            parts = numbers.split("\n", 1)
            delimiter = parts[0][2:]
            numbers = parts[1] if len(parts) > 1 else ""
        
        # Split by delimiter or newline
        if "\n" in numbers:
            # Replace newlines with delimiter for uniform splitting
            numbers = numbers.replace("\n", delimiter)
        
        # Split and filter empty strings
        num_list = [n.strip() for n in numbers.split(delimiter) if n.strip()]
        
        # Convert to integers and check for negatives
        integers = []
        negatives = []
        for num_str in num_list:
            try:
                num = int(num_str)
                if num < 0:
                    negatives.append(num)
                else:
                    integers.append(num)
            except ValueError:
                # Skip non-numeric values
                continue
        
        if negatives:
            raise ValueError(f"Negative numbers not allowed: {negatives}")
        
        return sum(integers)

# TDD Test Cases
class TestStringCalculator(unittest.TestCase):
    """TDD test cases for StringCalculator."""
    
    def setUp(self):
        self.calculator = StringCalculator()
    
    def test_empty_string_returns_zero(self):
        """Test that empty string returns 0."""
        self.assertEqual(self.calculator.add(""), 0)
    
    def test_single_number_returns_same(self):
        """Test that single number returns the same number."""
        self.assertEqual(self.calculator.add("5"), 5)
        self.assertEqual(self.calculator.add("0"), 0)
        self.assertEqual(self.calculator.add("123"), 123)
    
    def test_two_numbers_returns_sum(self):
        """Test that two numbers return their sum."""
        self.assertEqual(self.calculator.add("1,2"), 3)
        self.assertEqual(self.calculator.add("10,20"), 30)
    
    def test_newline_as_delimiter(self):
        """Test that newlines work as delimiters."""
        self.assertEqual(self.calculator.add("1\n2,3"), 6)
        self.assertEqual(self.calculator.add("1\n2\n3"), 6)
    
    def test_custom_delimiter(self):
        """Test custom delimiter format."""
        self.assertEqual(self.calculator.add("//;\n1;2"), 3)
        self.assertEqual(self.calculator.add("//|\n1|2|3"), 6)
    
    def test_negative_numbers_throw_exception(self):
        """Test that negative numbers throw exception."""
        with self.assertRaises(ValueError) as context:
            self.calculator.add("1,-2,3")
        self.assertIn("Negative numbers not allowed", str(context.exception))
        self.assertIn("-2", str(context.exception))
    
    def test_multiple_negatives(self):
        """Test multiple negative numbers."""
        with self.assertRaises(ValueError) as context:
            self.calculator.add("-1,2,-3")
        self.assertIn("Negative numbers not allowed", str(context.exception))
        self.assertIn("-1", str(context.exception))
        self.assertIn("-3", str(context.exception))
'''

# Test Organization Best Practices
TEST_ORGANIZATION = '''
Test Organization Best Practices:

1. Naming Conventions:
    - Test files: test_*.py or *_test.py
    - Test classes: Test* (unittest) or *Test (pytest)
    - Test methods: test_*_description_of_expected_behavior
    - Be descriptive but concise

2. Arrange-Act-Assert Pattern:
    - Arrange: Set up preconditions and inputs
    - Act: Execute the behavior being tested
    - Assert: Verify the expected outcomes

3. Test Independence:
    - Each test should be able to run independently
    - No test should depend on another test's state
    - Use setUp/tearDown or fixtures for shared state

4. Test Granularity:
    - Test one thing per test method
    - Keep tests focused and small
    - Prefer multiple specific tests over one complex test

5. Test Data Management:
    - Use factories or builders for test data
    - Consider fixtures for complex setup
    - Avoid hard-coded values when possible
    - Use meaningful test data that illustrates the scenario

6. Test Readability:
    - Tests should serve as documentation
    - Use clear, descriptive test names
    - Group related tests together
    - Use comments sparingly - good names should be self-explanatory

7. Test Maintenance:
    - Keep tests up-to-date with code changes
    - Remove or update obsolete tests
    - Refactor tests as needed for clarity
    - Treat test code with same respect as production code
'''

# Coverage and Quality
COVERAGE_QUALITY = '''
Test Coverage and Quality Metrics:

1. Line Coverage:
    - Percentage of executable lines covered by tests
    - Goal: 80%+ for backend applications
    - Remember: High coverage doesn't guarantee good tests

2. Branch Coverage:
    - Percentage of branches (if/else) covered
    - More meaningful than line coverage alone
    - Goal: 70%+ for critical paths

3. Path Coverage:
    - Percentage of possible paths covered
    - Most comprehensive but hardest to achieve
    - Usually impractical for complex code

4. Quality Indicators:
    - Tests fail when they should (catch regressions)
    - Tests pass when they should (no false positives)
    - Tests are fast (don't slow down development)
    - Tests are independent (can run in any order)
    - Tests are maintainable (easy to understand and update)
    - Tests are deterministic (same inputs produce same outputs)

5. Testing Pyramid:
    - Unit Tests: 70% (fast, isolated, test individual components)
    - Integration Tests: 20% (test component interactions)
    - End-to-End Tests: 10% (test full user journeys)

6. Mutation Testing:
    - Measures test effectiveness by introducing bugs
    - Higher mutation score = better tests
    - Tools: mutmut, cosmic-ray
'''

def print_testing_examples():
    """Print testing examples for reference."""
    print("=== TESTING FRAMEWORKS ===")
    print(TESTING_FRAMEWORKS.strip())
    print("\n=== UNIT TESTING EXAMPLES ===")
    print(UNIT_TESTING_EXAMPLES.strip())
    print("\n=== FIXTURES EXAMPLES ===")
    print(FIXTURES_EXAMPLES.strip())
    print("\n=== MOCKING EXAMPLES ===")
    print(MOCKING_EXAMPLES.strip())
    print("\n=== TDD EXAMPLE ===")
    print(TDD_EXAMPLE.strip())
    print("\n=== TEST ORGANIZATION BEST PRACTICES ===")
    print(TEST_ORGANIZATION.strip())
    print("\n=== COVERAGE AND QUALITY ===")
    print(COVERAGE_QUALITY.strip())

if __name__ == "__main__":
    print_testing_examples()
    
    # Testing Interview Tips
    print("\n" + "="*50)
    print("TESTING INTERVIEW TIPS:")
    print("="*50)
    print("1. Know the differences between unittest and pytest")
    print("2. Understand the Arrange-Act-Assert pattern")
    print("3. Be able to write clear, descriptive test names")
    print("4. Understand mocking and when to use it")
    print("5. Know the difference between Mock, MagicMock, and patch")
    print("6. Be familiar with pytest fixtures and their scopes")
    print("7. Understand test-driven development (TDD) principles")
    print("8. Know how to test edge cases and error conditions")
    print("9. Understand the testing pyramid concept")
    print("10. Be able to explain what makes a good unit test")
    print("11. Know how to handle dependencies in tests (mocks vs real)")
    print("12. Understand test isolation and why it's important")
    print("13. Practice writing tests for simple functions first")
    print("14. Know about test parametrization for testing multiple cases")
    print("15. Understand when to use integration vs unit tests")