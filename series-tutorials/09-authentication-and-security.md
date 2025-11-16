# Part 9: Authentication and Security in the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this ninth installment, we're exploring one of the most critical aspects of web application development: **Authentication and Security**.

In our previous posts, we've covered [the basics of Air](01-introduction-to-air-framework.md), [mastered Air Tags](02-mastering-air-tags.md), learned about [routing and HTTP methods](03-routing-and-http-methods.md), explored [forms and validation](04-forms-and-validation.md), understood [templates and Jinja integration](05-templates-and-jinja-integration.md), enhanced our applications with [Tailwind CSS styling](06-styling-with-tailwind-css.md), made our apps more interactive with [HTMX integration](07-htmx-integration.md), and implemented [database integration](08-database-integration.md). Now it's time to secure our Air applications with robust authentication and security measures.

## Introduction to Authentication and Security with Air

Authentication and security are fundamental to any web application that handles user data or provides personalized experiences. Without proper security measures, applications are vulnerable to various attacks that can compromise user data, application integrity, and business reputation.

The Air framework, built on top of FastAPI, inherits FastAPI's robust security features while providing its own conveniences for implementing authentication in web applications. In this post, we'll explore how to implement secure authentication systems in Air applications.

### Why Authentication and Security Matter

1. **Data Protection**: Safeguard sensitive user information and application data
2. **Access Control**: Ensure only authorized users can access specific resources
3. **Compliance**: Meet regulatory requirements for data protection
4. **Trust**: Build user confidence in your application
5. **Prevention**: Protect against common web vulnerabilities

## Authentication Fundamentals

Before diving into implementation, let's understand the core concepts of authentication and the approaches available in Air applications.

### Session Management

Session management is one of the traditional approaches to maintaining user authentication state. With sessions, the server stores user information and associates it with a session identifier sent to the client.

```python
import air
from datetime import datetime, timedelta
from typing import Optional
import secrets

# Simple in-memory session store (use Redis or database in production)
sessions = {}

class SessionManager:
    @staticmethod
    def create_session(user_id: int) -> str:
        session_id = secrets.token_urlsafe(32)
        sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        }
        return session_id
    
    @staticmethod
    def get_session(session_id: str) -> Optional[dict]:
        session = sessions.get(session_id)
        if session and session["expires_at"] > datetime.utcnow():
            return session
        return None
    
    @staticmethod
    def destroy_session(session_id: str):
        if session_id in sessions:
            del sessions[session_id]

# Session dependency
def get_current_user(request: air.Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    
    session = SessionManager.get_session(session_id)
    if not session:
        return None
    
    # In a real app, you'd fetch user from database
    return {"id": session["user_id"], "username": f"user_{session['user_id']}"}
```

### Token-Based Authentication

Token-based authentication, particularly JWT (JSON Web Tokens), has become the standard for modern web applications. Tokens contain encoded user information and are verified using cryptographic signatures.

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Token dependency
async def get_current_user_from_token(token: str = air.Header(None)):
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        # In a real app, you'd fetch user from database
        return {"id": user_id, "username": f"user_{user_id}"}
    except JWTError:
        return None
```

### Password Hashing

Never store passwords in plain text. Always hash passwords using secure algorithms like bcrypt:

```python
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a hash for a password."""
    return pwd_context.hash(password)

# Example usage
hashed_password = get_password_hash("my_secure_password")
is_valid = verify_password("my_secure_password", hashed_password)
```

### User Registration Flows

A complete authentication system requires user registration functionality:

```
from sqlmodel import Field, SQLModel, Session
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

@app.page("/register")
def register_form():
    return air.layouts.mvpcss(
        air.H1("Register", class_="text-3xl font-bold mb-6"),
        air.Form(
            air.Div(
                air.Label("Username", for_="username", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="text",
                    id="username",
                    name="username",
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Label("Email", for_="email", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="email",
                    id="email",
                    name="email",
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Label("Password", for_="password", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="password",
                    id="password",
                    name="password",
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Label("Confirm Password", for_="confirm_password", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="password",
                    id="confirm_password",
                    name="confirm_password",
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-6"
            ),
            air.Button(
                "Register",
                type="submit",
                class_="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            ),
            hx_post="/register",
            hx_target="#result",
            hx_swap="innerHTML",
            class_="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto"
        ),
        air.Div(id="result", class_="mt-6")
    )

@app.post("/register")
async def register_user(request: air.Request, session: Session = Depends(get_session)):
    form_data = await request.form()
    
    username = form_data.get("username")
    email = form_data.get("email")
    password = form_data.get("password")
    confirm_password = form_data.get("confirm_password")
    
    # Validation
    if not username or not email or not password:
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("All fields are required.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    if password != confirm_password:
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Passwords do not match.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.username == username)).first()
    if existing_user:
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Username already exists.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    existing_email = session.exec(select(User).where(User.email == email)).first()
    if existing_email:
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Email already registered.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    # Create new user
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return air.Div(
        air.Div(
            air.H3("Success!", class_="text-lg font-medium text-green-800"),
            air.P("Account created successfully. You can now log in.", class_="text-green-600"),
            air.A(
                "Login",
                href="/login",
                class_="mt-2 inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded text-sm"
            ),
            class_="bg-green-50 p-4 rounded-lg"
        )
    )
```

## Implementing Authentication in Air

Now let's implement a complete authentication system in Air with login, logout, and protected routes.

### User Models

First, let's define our user model with proper security considerations:

```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, max_length=100)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Relationships
    posts: List["Post"] = Relationship(back_populates="author")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
```

### Login and Logout Views

Let's implement the login and logout functionality:

```python
@app.page("/login")
def login_form():
    return air.layouts.mvpcss(
        air.H1("Login", class_="text-3xl font-bold mb-6"),
        air.Form(
            air.Div(
                air.Label("Username or Email", for_="identifier", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="text",
                    id="identifier",
                    name="identifier",
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Label("Password", for_="password", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="password",
                    id="password",
                    name="password",
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-6"
            ),
            air.Div(
                air.Button(
                    "Login",
                    type="submit",
                    class_="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                ),
                air.A(
                    "Register",
                    href="/register",
                    class_="mt-2 block text-center text-blue-600 hover:text-blue-800"
                ),
                class_="mb-4"
            ),
            hx_post="/login",
            hx_target="#result",
            hx_swap="innerHTML",
            class_="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto"
        ),
        air.Div(id="result", class_="mt-6")
    )

@app.post("/login")
async def login_user(request: air.Request, session: Session = Depends(get_session)):
    form_data = await request.form()
    
    identifier = form_data.get("identifier")
    password = form_data.get("password")
    
    if not identifier or not password:
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Both username/email and password are required.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    # Find user by username or email
    user = session.exec(
        select(User).where(
            (User.username == identifier) | (User.email == identifier)
        )
    ).first()
    
    if not user or not verify_password(password, user.hashed_password):
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Invalid username/email or password.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    session.add(user)
    session.commit()
    
    # Create session or token
    session_id = SessionManager.create_session(user.id)
    
    # Return success with redirect
    return air.Div(
        air.Script("document.cookie = 'session_id=" + session_id + "; path=/'; window.location.href = '/dashboard';"),
        air.Div(
            air.H3("Success!", class_="text-lg font-medium text-green-800"),
            air.P("Login successful. Redirecting...", class_="text-green-600"),
            class_="bg-green-50 p-4 rounded-lg"
        )
    )

@app.page("/logout")
def logout_user(request: air.Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        SessionManager.destroy_session(session_id)
    
    # Clear cookie and redirect
    response = air.RedirectResponse(url="/", status_code=303)
    response.set_cookie("session_id", "", expires=0)
    return response

# Protected route example
@app.page("/dashboard")
def dashboard(request: air.Request, current_user: dict = Depends(get_current_user)):
    if not current_user:
        return air.RedirectResponse(url="/login", status_code=303)
    
    return air.layouts.mvpcss(
        air.H1(f"Welcome, {current_user['username']}!", class_="text-3xl font-bold mb-6"),
        air.Div(
            air.P("This is your dashboard. Only authenticated users can see this page.", class_="text-gray-700"),
            air.A(
                "Logout",
                href="/logout",
                class_="mt-4 inline-block bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            ),
            class_="bg-white p-6 rounded-lg shadow-md"
        )
    )
```

### Session Middleware

For session-based authentication, we need middleware to handle session management:

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Add session information to request state
        session_id = request.cookies.get("session_id")
        if session_id:
            session = SessionManager.get_session(session_id)
            if session:
                request.state.user = {"id": session["user_id"], "username": f"user_{session['user_id']}"}
            else:
                request.state.user = None
        else:
            request.state.user = None
        
        response = await call_next(request)
        return response

# Add middleware to app
app.add_middleware(SessionMiddleware)
```

### Protected Routes

Creating protected routes is essential for securing parts of your application:

```python
from functools import wraps

def require_auth(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        request = kwargs.get('request') or args[0]  # Assuming request is first arg
        if not hasattr(request.state, 'user') or not request.state.user:
            return air.RedirectResponse(url="/login", status_code=303)
        return view_func(*args, **kwargs)
    return wrapper

# Using the decorator
@app.page("/profile")
@require_auth
def profile_page(request: air.Request):
    user = request.state.user
    return air.layouts.mvpcss(
        air.H1(f"Profile: {user['username']}", class_="text-3xl font-bold mb-6"),
        air.Div(
            air.P(f"User ID: {user['id']}", class_="text-gray-700"),
            air.A(
                "Back to Dashboard",
                href="/dashboard",
                class_="mt-4 inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            ),
            class_="bg-white p-6 rounded-lg shadow-md"
        )
    )
```

## Security Best Practices

Implementing authentication is just the beginning. Let's explore essential security best practices for Air applications.

### CSRF Protection

Cross-Site Request Forgery (CSRF) protection is crucial for form submissions:

```python
import secrets

def generate_csrf_token():
    return secrets.token_urlsafe(32)

def validate_csrf_token(request: air.Request, token: str):
    session_token = request.cookies.get("csrf_token")
    return session_token and session_token == token

# Include CSRF token in forms
@app.page("/protected-form")
def protected_form(request: air.Request):
    csrf_token = generate_csrf_token()
    # Store in session or cookie
    response = air.layouts.mvpcss(
        air.H1("Protected Form", class_="text-3xl font-bold mb-6"),
        air.Form(
            air.Input(type="hidden", name="csrf_token", value=csrf_token),
            # ... form fields ...
            air.Button("Submit", type="submit"),
            # ... rest of form ...
        )
    )
    response.set_cookie("csrf_token", csrf_token, httponly=True, samesite="strict")
    return response
```

### XSS Prevention

Cross-Site Scripting (XSS) prevention involves proper output escaping:

```python
# Air Tags automatically escape content by default
# But be careful with raw HTML
@app.page("/user-content")
def user_content(user_input: str):
    # Safe - automatic escaping
    return air.layouts.mvpcss(
        air.H1("User Content"),
        air.P(user_input)  # Automatically escaped
    )

# If you need to render HTML, be explicit about it
@app.page("/render-html")
def render_html_safe(user_html: str):
    # Only use this if you've sanitized the HTML
    from markupsafe import Markup
    return air.layouts.mvpcss(
        air.H1("Rendered HTML"),
        air.Div(Markup(user_html))  # Explicitly mark as safe
    )
```

### SQL Injection Prevention

SQL injection is prevented by using parameterized queries through SQLModel:

```python
# Safe - using SQLModel's parameterized queries
@app.get("/posts/{post_id}")
def get_post(post_id: int, session: Session = Depends(get_session)):
    # SQLModel automatically handles parameterization
    post = session.get(Post, post_id)
    return post

# Also safe - using select with parameters
@app.get("/posts/search")
def search_posts(query: str, session: Session = Depends(get_session)):
    statement = select(Post).where(Post.title.contains(query))
    posts = session.exec(statement).all()
    return posts

# Avoid - raw SQL concatenation (dangerous)
# DON'T DO THIS:
# posts = session.exec(f"SELECT * FROM post WHERE title LIKE '%{query}%'")
```

### Rate Limiting

Rate limiting prevents abuse of your authentication endpoints:

```python
from collections import defaultdict
from datetime import datetime, timedelta

# Simple in-memory rate limiter (use Redis in production)
rate_limits = defaultdict(list)

def is_rate_limited(ip: str, limit: int = 5, window: int = 300) -> bool:
    now = datetime.utcnow()
    # Clean old entries
    rate_limits[ip] = [timestamp for timestamp in rate_limits[ip] 
                      if now - timestamp < timedelta(seconds=window)]
    
    # Check if limit exceeded
    if len(rate_limits[ip]) >= limit:
        return True
    
    # Add current request
    rate_limits[ip].append(now)
    return False

@app.post("/login")
async def login_user(request: air.Request, session: Session = Depends(get_session)):
    client_ip = request.client.host
    
    if is_rate_limited(client_ip):
        return air.Div(
            air.Div(
                air.H3("Too Many Requests", class_="text-lg font-medium text-red-800"),
                air.P("Please wait before trying again.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    # ... rest of login logic ...
```

## OAuth Integration

For modern applications, OAuth integration allows users to sign in with their existing accounts from providers like Google, GitHub, or Facebook.

### Social Login Providers

```python
from authlib.integrations.starlette_client import OAuth

# OAuth configuration
oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

@app.page("/login/google")
async def login_google(request: air.Request):
    redirect_uri = request.url_for("auth_google")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.route("/auth/google", name="auth_google")
async def auth_google(request: air.Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        
        if user_info:
            # Check if user exists, create if not
            # Log user in
            session_id = SessionManager.create_session(user_info["sub"])
            
            response = air.RedirectResponse(url="/dashboard", status_code=303)
            response.set_cookie("session_id", session_id, httponly=True, samesite="strict")
            return response
        
    except Exception as e:
        return air.layouts.mvpcss(
            air.H1("Authentication Error", class_="text-3xl font-bold mb-6"),
            air.P(f"Failed to authenticate: {str(e)}", class_="text-red-600")
        )
    
    return air.RedirectResponse(url="/login", status_code=303)
```

### API Token Management

For API access, token-based authentication is preferred:

```python
from datetime import datetime, timedelta

class APIToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    
    user: User = Relationship()

def create_api_token(user_id: int, name: str, expires_in_days: int = 365) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    api_token = APIToken(
        token=token,
        user_id=user_id,
        name=name,
        expires_at=expires_at
    )
    
    # Save to database
    with Session(engine) as session:
        session.add(api_token)
        session.commit()
    
    return token

# API token dependency
async def get_current_user_from_api_token(request: air.Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split(" ")[1]
    
    with Session(engine) as session:
        api_token = session.exec(
            select(APIToken).where(APIToken.token == token)
        ).first()
        
        if not api_token or api_token.expires_at < datetime.utcnow():
            return None
        
        # Update last used
        api_token.last_used = datetime.utcnow()
        session.add(api_token)
        session.commit()
        
        # Get user
        user = session.get(User, api_token.user_id)
        return user
```

### Role-Based Access Control

Implementing role-based access control (RBAC):

```python
class UserRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    role: str  # "admin", "moderator", "user", etc.
    assigned_at: datetime = Field(default_factory=datetime.utcnow)

def require_role(required_role: str):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            request = kwargs.get('request') or args[0]
            user = getattr(request.state, 'user', None)
            
            if not user:
                return air.RedirectResponse(url="/login", status_code=303)
            
            # Check user role
            with Session(engine) as session:
                user_role = session.exec(
                    select(UserRole).where(UserRole.user_id == user["id"])
                ).first()
                
                if not user_role or user_role.role != required_role:
                    return air.layouts.mvpcss(
                        air.H1("Access Denied", class_="text-3xl font-bold mb-6"),
                        air.P("You don't have permission to access this page.", class_="text-red-600")
                    )
            
            return view_func(*args, **kwargs)
        return wrapper
    return decorator

# Using role-based access control
@app.page("/admin")
@require_role("admin")
def admin_dashboard(request: air.Request):
    return air.layouts.mvpcss(
        air.H1("Admin Dashboard", class_="text-3xl font-bold mb-6"),
        air.P("Welcome to the admin panel.", class_="text-gray-700")
    )
```

### Multi-Factor Authentication

Implementing multi-factor authentication (MFA):

```python
import pyotp
import qrcode
from io import BytesIO
import base64

class UserMFA(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    secret: str  # TOTP secret
    enabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

def generate_mfa_secret() -> str:
    return pyotp.random_base32()

def verify_mfa_token(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

@app.page("/setup-mfa")
@require_auth
def setup_mfa(request: air.Request):
    user = request.state.user
    
    # Generate secret for user
    secret = generate_mfa_secret()
    
    # Save to database (temporarily)
    with Session(engine) as session:
        user_mfa = UserMFA(user_id=user["id"], secret=secret)
        session.add(user_mfa)
        session.commit()
    
    # Generate QR code
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user["username"],
        issuer_name="Your App Name"
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_b64 = base64.b64encode(buffer.getvalue()).decode()
    
    return air.layouts.mvpcss(
        air.H1("Setup Multi-Factor Authentication", class_="text-3xl font-bold mb-6"),
        air.Div(
            air.P("Scan this QR code with your authenticator app:", class_="text-gray-700 mb-4"),
            air.Img(src=f"data:image/png;base64,{qr_code_b64}", class_="mx-auto"),
            air.P(f"Or enter this code manually: {secret}", class_="text-center text-sm text-gray-600 mt-4"),
            air.Form(
                air.Div(
                    air.Label("Enter 6-digit code:", for_="mfa_code", class_="block text-sm font-medium text-gray-700 mb-1"),
                    air.Input(
                        type="text",
                        id="mfa_code",
                        name="mfa_code",
                        maxlength=6,
                        required=True,
                        class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    ),
                    class_="mb-4"
                ),
                air.Input(type="hidden", name="secret", value=secret),
                air.Button(
                    "Verify and Enable MFA",
                    type="submit",
                    class_="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                ),
                hx_post="/verify-mfa",
                hx_target="#result",
                hx_swap="innerHTML",
                class_="mt-6"
            ),
            class_="bg-white p-6 rounded-lg shadow-md text-center"
        ),
        air.Div(id="result", class_="mt-6")
    )

@app.post("/verify-mfa")
@require_auth
async def verify_mfa(request: air.Request):
    form_data = await request.form()
    secret = form_data.get("secret")
    mfa_code = form_data.get("mfa_code")
    
    if verify_mfa_token(secret, mfa_code):
        # Enable MFA for user
        user = request.state.user
        with Session(engine) as session:
            user_mfa = session.exec(
                select(UserMFA).where(UserMFA.user_id == user["id"])
            ).first()
            
            if user_mfa:
                user_mfa.enabled = True
                session.add(user_mfa)
                session.commit()
        
        return air.Div(
            air.Div(
                air.H3("Success!", class_="text-lg font-medium text-green-800"),
                air.P("Multi-factor authentication has been enabled.", class_="text-green-600"),
                class_="bg-green-50 p-4 rounded-lg"
            )
        )
    else:
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Invalid code. Please try again.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
```

## Best Practices for Authentication and Security

### 1. Use HTTPS in Production

Always use HTTPS in production environments:

```python
# In production, run with HTTPS
# uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### 2. Secure Cookie Settings

Set secure cookie attributes:

```python
# Secure cookie settings
response.set_cookie(
    "session_id", 
    session_id,
    httponly=True,      # Prevent XSS
    secure=True,        # HTTPS only
    samesite="strict",  # CSRF protection
    max_age=3600*24     # 24 hours
)
```

### 3. Implement Proper Logging

Log security events without exposing sensitive data:

```python
import logging

logger = logging.getLogger("security")

@app.post("/login")
async def login_user(request: air.Request):
    # ... authentication logic ...
    
    if success:
        logger.info(f"Successful login for user {user_id}")
    else:
        client_ip = request.client.host
        logger.warning(f"Failed login attempt from {client_ip}")
```

### 4. Regular Security Updates

Keep dependencies updated:

```bash
# Regularly update dependencies
pip list --outdated
pip install --upgrade air passlib bcrypt jose pyotp qrcode authlib

# Or with uv
uv pip list --outdated
uv pip install --upgrade air passlib bcrypt python-jose pyotp qrcode[pil] authlib
```

### 5. Environment Variables for Secrets

Never hardcode secrets:

```python
# .env file
SECRET_KEY=your-very-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# In your code
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
```

## What's Coming Next

In our next post, we'll explore testing and debugging, covering:

1. Unit testing Air applications with pytest
2. Integration testing strategies
3. Debugging techniques and tools
4. Performance profiling and optimization

## Conclusion

Authentication and security are critical components of any production web application. The Air framework, built on FastAPI, provides excellent tools and patterns for implementing secure authentication systems.

Key takeaways from this post:

1. **Authentication Fundamentals**: Understand session management, token-based authentication, and password hashing
2. **Implementation in Air**: Create login/logout flows, protected routes, and session management
3. **Security Best Practices**: Implement CSRF protection, prevent XSS and SQL injection, and apply rate limiting
4. **Advanced Features**: Integrate OAuth, implement API tokens, and add multi-factor authentication
5. **Production Considerations**: Use HTTPS, secure cookies, proper logging, and environment variables

With a solid authentication and security foundation, your Air applications will be well-protected against common threats while providing a smooth user experience. Remember that security is an ongoing process, not a one-time implementation.

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for weekly updates. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

See you in the next post where we'll dive into testing and debugging!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [Database Integration](08-database-integration.md)*

## Quiz: Test Your Knowledge

1. What is the primary method Air uses for session management?
   a) JWT tokens
   b) OAuth
   c) Server-side sessions with cookies
   d) Local storage

2. Which library is commonly used for password hashing in Air applications?
   a) hashlib
   b) bcrypt
   c) cryptography
   d) passlib

3. What HTTP header is checked to detect HTMX requests in Air?
   a) X-Requested-With
   b) hx-request
   c) X-HTMX-Request
   d) HTMX-Request

4. True or False: You should store sensitive information like API keys and database passwords directly in your source code.

5. True or False: CSRF protection is automatically handled by Air's SessionMiddleware.

6. Explain the difference between authentication and authorization, and how both are implemented in Air applications.

### Answers:
1. c) Server-side sessions with cookies
2. d) passlib
3. b) hx-request
4. False - Sensitive information should be stored in environment variables, not in source code
5. False - While Air's SessionMiddleware provides a foundation, CSRF protection requires additional implementation like the double-submit cookie pattern or custom headers
6. Authentication is the process of verifying who a user is (typically through login credentials), while authorization is the process of determining what resources or actions an authenticated user is allowed to access. In Air applications, authentication is typically implemented through session management with login/logout endpoints and password hashing, while authorization is implemented through route dependencies that check user roles or permissions before allowing access to protected resources.
