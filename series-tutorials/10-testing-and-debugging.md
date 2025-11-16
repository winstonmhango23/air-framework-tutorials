# Part 10: Testing and Debugging in the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this tenth installment, we're diving into one of the most critical aspects of software development: **Testing and Debugging**.

In our previous posts, we've covered [the basics of Air](01-introduction-to-air-framework.md), [mastered Air Tags](02-mastering-air-tags.md), learned about [routing and HTTP methods](03-routing-and-http-methods.md), explored [forms and validation](04-forms-and-validation.md), understood [templates and Jinja integration](05-templates-and-jinja-integration.md), enhanced our applications with [Tailwind CSS styling](06-styling-with-tailwind-css.md), made our apps more interactive with [HTMX integration](07-htmx-integration.md), implemented [database integration](08-database-integration.md), and secured our applications with [authentication and security](09-authentication-and-security.md). Now it's time to ensure our Air applications are reliable, performant, and bug-free through comprehensive testing and debugging practices.

## Introduction to Testing and Debugging with Air

Testing and debugging are essential practices that ensure your Air applications function correctly, perform well, and remain maintainable as they grow in complexity. While Air, built on top of FastAPI, provides excellent tools for building web applications, it's equally important to establish robust testing and debugging workflows.

### Why Testing and Debugging Matter

1. **Quality Assurance**: Catch bugs before they reach production
2. **Confidence**: Ensure changes don't break existing functionality
3. **Documentation**: Tests serve as living documentation of expected behavior
4. **Refactoring Safety**: Make changes with confidence that existing functionality remains intact
5. **Performance Optimization**: Identify bottlenecks and optimize critical paths

## Testing Air Applications

Air applications can be tested using the same tools and techniques as FastAPI applications, with the added benefit of Air's conveniences for web development.

### Unit Testing with pytest

Unit tests focus on testing individual functions or components in isolation. For Air applications, this typically means testing service layer functions, utility functions, and business logic.

First, let's set up our testing environment:

```bash
# Install testing dependencies
pip install pytest httpx pytest-cov
# Or with uv
uv add pytest httpx pytest-cov
```

Let's create a simple utility function and test it:

```
# utils.py
def calculate_reading_time(text: str) -> int:
    """
    Calculate estimated reading time in minutes.
    Assumes average reading speed of 200 words per minute.
    """
    words_per_minute = 200
    word_count = len(text.split())
    reading_time = word_count / words_per_minute
    return max(1, round(reading_time))

def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.
    """
    import re
    # Convert to lowercase and replace spaces/underscores with hyphens
    slug = re.sub(r'[_\s]+', '-', text.lower())
    # Remove non-alphanumeric characters except hyphens
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    # Replace multiple hyphens with single hyphen
    slug = re.sub(r'-+', '-', slug)
    return slug
```

```python
# test_utils.py
import pytest
from utils import calculate_reading_time, slugify

def test_calculate_reading_time():
    # Test short text
    assert calculate_reading_time("Hello world") == 1
    
    # Test longer text (400 words should be 2 minutes)
    long_text = "word " * 400
    assert calculate_reading_time(long_text) == 2
    
    # Test empty text
    assert calculate_reading_time("") == 1

def test_slugify():
    # Test basic conversion
    assert slugify("Hello World") == "hello-world"
    
    # Test with special characters
    assert slugify("Hello, World!") == "hello-world"
    
    # Test with underscores
    assert slugify("Hello_World_Test") == "hello-world-test"
    
    # Test with multiple spaces
    assert slugify("Hello    World") == "hello-world"
    
    # Test edge cases
    assert slugify("") == ""
    assert slugify("   ") == ""
    assert slugify("123") == "123"
```

### Testing HTTP Endpoints

For testing HTTP endpoints in Air applications, we use the `TestClient` from FastAPI:

```
# main.py
import air
from pydantic import BaseModel

app = air.Air()

class Item(BaseModel):
    id: int
    name: str
    description: str = None

# In-memory storage for demo purposes
items_db = {}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Air Testing Demo"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise air.HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items/")
def create_item(item: Item):
    if item.id in items_db:
        raise air.HTTPException(status_code=409, detail="Item already exists")
    items_db[item.id] = item
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise air.HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise air.HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return deleted_item
```

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app, items_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    """Clear the database before each test."""
    items_db.clear()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Air Testing Demo"}

def test_create_item():
    item_data = {
        "id": 1,
        "name": "Test Item",
        "description": "A test item"
    }
    
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json() == item_data

def test_create_duplicate_item():
    # First create an item
    item_data = {"id": 1, "name": "Test Item"}
    client.post("/items/", json=item_data)
    
    # Try to create the same item again
    response = client.post("/items/", json=item_data)
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}

def test_read_item():
    # First create an item
    item_data = {"id": 1, "name": "Test Item", "description": "A test item"}
    client.post("/items/", json=item_data)
    
    # Read the item
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == item_data

def test_read_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_update_item():
    # First create an item
    item_data = {"id": 1, "name": "Test Item", "description": "A test item"}
    client.post("/items/", json=item_data)
    
    # Update the item
    updated_data = {"id": 1, "name": "Updated Item", "description": "Updated description"}
    response = client.put("/items/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data

def test_delete_item():
    # First create an item
    item_data = {"id": 1, "name": "Test Item", "description": "A test item"}
    client.post("/items/", json=item_data)
    
    # Delete the item
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == item_data
    
    # Verify item is deleted
    response = client.get("/items/1")
    assert response.status_code == 404
```

### Testing Database Interactions

When testing database interactions, it's important to use a separate test database and mock external dependencies where possible:

```
# database.py
from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    is_active: bool = Field(default=True)

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, echo=True)

def create_test_db():
    SQLModel.metadata.create_all(test_engine)

def get_test_session():
    with Session(test_engine) as session:
        yield session
```

```python
# user_service.py
from sqlmodel import select
from database import User, get_test_session

def create_user(username: str, email: str) -> User:
    user = User(username=username, email=email)
    with get_test_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

def get_user_by_username(username: str) -> User:
    with get_test_session() as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        return user
```

```python
# test_user_service.py
import pytest
from user_service import create_user, get_user_by_username
from database import create_test_db

@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    """Create test database tables."""
    create_test_db()

@pytest.fixture(autouse=True)
def clear_users():
    """Clear users table before each test."""
    # Implementation depends on your database setup
    pass

def test_create_user():
    user = create_user("testuser", "test@example.com")
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True

def test_get_user_by_username():
    # First create a user
    created_user = create_user("testuser", "test@example.com")
    
    # Then retrieve the user
    retrieved_user = get_user_by_username("testuser")
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"

def test_get_nonexistent_user():
    user = get_user_by_username("nonexistent")
    assert user is None
```

### Integration Testing

Integration tests verify that different parts of your application work together correctly:

```
# test_integration.py
import pytest
from fastapi.testclient import TestClient
from main import app
from database import create_test_db

@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    """Create test database tables."""
    create_test_db()

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

def test_full_user_flow(client):
    # 1. Create a user via API
    user_data = {
        "username": "integration_test_user",
        "email": "integration@test.com"
    }
    
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]
    
    # 2. Retrieve the user via API
    response = client.get(f"/users/{created_user['id']}")
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user["username"] == user_data["username"]
    
    # 3. Update the user via API
    updated_data = {
        "username": "updated_user",
        "email": "updated@test.com"
    }
    
    response = client.put(f"/users/{created_user['id']}", json=updated_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["username"] == updated_data["username"]
    
    # 4. Delete the user via API
    response = client.delete(f"/users/{created_user['id']}")
    assert response.status_code == 200
    
    # 5. Verify user is deleted
    response = client.get(f"/users/{created_user['id']}")
    assert response.status_code == 404
```

## Debugging Techniques

Effective debugging is crucial for identifying and resolving issues in your Air applications.

### Logging Configuration

Proper logging is essential for debugging production applications:

```
# logging_config.py
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'app.log', 
        maxBytes=1024*1024*5,  # 5MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Configure specific loggers
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

# In your main application
import logging
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

@app.get("/debug-example")
def debug_example():
    logger.info("Debug endpoint called")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    
    try:
        # Some operation that might fail
        result = 1 / 0
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise air.HTTPException(status_code=500, detail="Internal server error")
```

### Debugging Tools

Several tools can help with debugging Air applications:

```
# Using the Python debugger (pdb)
@app.get("/debug-with-pdb")
def debug_with_pdb():
    import pdb
    
    x = 10
    y = 20
    pdb.set_trace()  # Execution will pause here
    result = x + y
    return {"result": result}

# Using breakpoint() (Python 3.7+)
@app.get("/debug-with-breakpoint")
def debug_with_breakpoint():
    x = 10
    y = 20
    breakpoint()  # Execution will pause here
    result = x + y
    return {"result": result}

# Custom debugging middleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

class DebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url}")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            logger.info(f"Response: {response.status_code} in {process_time:.4f}s")
            return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            raise

# Add middleware to app
app.add_middleware(DebugMiddleware)
```

### Performance Profiling

Identifying performance bottlenecks is crucial for optimizing Air applications:

```
# Using cProfile for CPU profiling
import cProfile
import pstats
from io import StringIO

@app.get("/profile-example")
def profile_example():
    def cpu_intensive_function():
        # Simulate CPU-intensive work
        result = 0
        for i in range(1000000):
            result += i * i
        return result
    
    # Profile the function
    pr = cProfile.Profile()
    pr.enable()
    result = cpu_intensive_function()
    pr.disable()
    
    # Get profiling results
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    
    logger.info(f"Profiling results:\n{s.getvalue()}")
    return {"result": result}

# Custom timing decorator
import functools
import time

def timing_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@app.get("/timed-endpoint")
@timing_decorator
async def timed_endpoint():
    # Simulate some work
    await asyncio.sleep(0.1)
    return {"message": "This endpoint was timed"}
```

### Memory Profiling

Monitoring memory usage helps identify memory leaks and optimize resource consumption:

```
# Using tracemalloc for memory profiling
import tracemalloc

@app.get("/memory-profile")
def memory_profile():
    # Start tracing
    tracemalloc.start()
    
    # Perform some operations
    data = [i for i in range(100000)]
    processed_data = [x * 2 for x in data]
    
    # Get memory statistics
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    logger.info(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
    logger.info(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
    
    return {
        "current_memory_mb": current / 1024 / 1024,
        "peak_memory_mb": peak / 1024 / 1024
    }

# Memory monitoring middleware
class MemoryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if tracemalloc.is_tracing():
            snapshot1 = tracemalloc.take_snapshot()
        
        response = await call_next(request)
        
        if tracemalloc.is_tracing():
            snapshot2 = tracemalloc.take_snapshot()
            top_stats = snapshot2.compare_to(snapshot1, 'lineno')
            
            logger.info("Top 3 memory allocations:")
            for stat in top_stats[:3]:
                logger.info(stat)
        
        return response
```

## Testing with Tailwind CSS

When using Tailwind CSS with Air, there are specific considerations for testing visual aspects of your application.

### Visual Regression Testing

Visual regression testing ensures that UI changes don't introduce unintended visual differences:

```python
# test_visual_regression.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_homepage_visual_regression():
    """Test that the homepage renders as expected."""
    response = client.get("/")
    assert response.status_code == 200
    
    # For visual regression testing, you would typically:
    # 1. Capture a screenshot of the rendered page
    # 2. Compare it with a baseline image
    # 3. Report any differences
    
    # This is a simplified example - in practice you would use
    # tools like Playwright, Selenium, or Percy for visual testing
    
    # Check that essential elements are present
    html_content = response.text
    assert "Welcome" in html_content
    assert "class=" in html_content  # Ensure Tailwind classes are present

def test_responsive_design():
    """Test responsive design elements."""
    # Test different viewport sizes
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Desktop view
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    
    # You would typically use browser automation tools
    # to test actual responsive behavior
```

### Responsive Design Testing

Testing responsive design ensures your application works well on different screen sizes:

```python
# test_responsive.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_mobile_viewport():
    """Test that mobile-specific elements are present."""
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)",
        "Accept": "text/html"
    }
    
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    
    # Check for mobile-specific classes or elements
    # This would depend on your specific implementation

def test_tablet_viewport():
    """Test tablet viewport rendering."""
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X)",
        "Accept": "text/html"
    }
    
    response = client.get("/", headers=headers)
    assert response.status_code == 200

def test_desktop_viewport():
    """Test desktop viewport rendering."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept": "text/html"
    }
    
    response = client.get("/", headers=headers)
    assert response.status_code == 200
```

## Best Practices for Testing and Debugging

### 1. Test Organization

Organize your tests in a clear, maintainable structure:

```
# conftest.py - Shared test configuration
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Create a test client for each test."""
    return TestClient(app)

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com"
    }

# test_user_endpoints.py
class TestUserEndpoints:
    """Test user-related endpoints."""
    
    def test_create_user(self, client, sample_user):
        response = client.post("/users/", json=sample_user)
        assert response.status_code == 200
        
    def test_get_user(self, client, sample_user):
        # First create user
        client.post("/users/", json=sample_user)
        
        # Then get user
        response = client.get("/users/1")
        assert response.status_code == 200

# test_utils.py
class TestUtils:
    """Test utility functions."""
    
    def test_slugify(self):
        from utils import slugify
        assert slugify("Hello World") == "hello-world"
```

### 2. Test Data Management

Use factories or fixtures to manage test data:

```
# factories.py
import factory
from database import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    is_active = True

# test_with_factories.py
def test_user_creation_with_factory():
    user = UserFactory(username="testuser")
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
```

### 3. Continuous Integration

Set up continuous integration to run tests automatically:

```
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

### 4. Test Coverage

Monitor test coverage to ensure adequate testing:

```bash
# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Set coverage thresholds
pytest --cov=app --cov-fail-under=80
```

## What's Coming Next

In our next post, we'll explore deployment and performance optimization, covering:

1. Deployment options for Air applications
2. Containerization with Docker
3. Performance optimization strategies
4. Monitoring and maintenance best practices

## Conclusion

Testing and debugging are critical components of building reliable, maintainable Air applications. By implementing comprehensive testing strategies and effective debugging techniques, you can ensure your applications function correctly and perform well under various conditions.

Key takeaways from this post:

1. **Unit Testing**: Test individual functions and components in isolation using pytest
2. **HTTP Endpoint Testing**: Use TestClient to test API endpoints and web pages
3. **Database Testing**: Set up separate test databases and mock external dependencies
4. **Integration Testing**: Verify that different parts of your application work together
5. **Debugging Techniques**: Implement proper logging, use debugging tools, and profile performance
6. **Best Practices**: Organize tests effectively, manage test data, and set up continuous integration

With a solid testing and debugging foundation, your Air applications will be more reliable, easier to maintain, and less prone to bugs in production. Remember that testing is an investment in the long-term success of your application.

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for weekly updates. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

See you in the next post where we'll dive into deployment and performance optimization!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [Authentication and Security](09-authentication-and-security.md)*

## Quiz: Test Your Knowledge

1. Which testing framework is commonly used with Air applications?
   a) unittest
   b) nose
   c) pytest
   d) doctest

2. What is the correct way to create a test client for Air applications?
   a) air.TestClient(app)
   b) TestClient(app)
   c) app.test_client()
   d) air.test_client(app)

3. What is the primary purpose of mocking in unit tests?
   a) To speed up test execution
   b) To isolate the unit under test from its dependencies
   c) To reduce code duplication
   d) To improve test coverage

4. True or False: Integration tests verify that individual units of code work correctly in isolation.

5. True or False: You should test both successful and error cases in your unit tests.

6. Explain the difference between unit tests and integration tests, and when you would use each type in an Air application.

### Answers:
1. c) pytest
2. b) TestClient(app)
3. b) To isolate the unit under test from its dependencies
4. False - Unit tests verify individual units in isolation, while integration tests verify that different parts work together
5. True
6. Unit tests focus on testing individual functions, methods, or components in isolation to verify they work correctly on their own. They are fast, specific, and help identify exactly where bugs occur. Integration tests verify that different parts of an application work together correctly, such as testing the interaction between a route handler, database layer, and business logic. In Air applications, you would use unit tests to verify individual route handlers, utility functions, and model methods, while you would use integration tests to verify complete workflows like user registration, login processes, or API endpoint interactions with the database.