# Part 3: Routing and HTTP Methods in the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this third installment, we're diving deep into one of the most fundamental aspects of any web framework: **routing and HTTP methods**.

In our previous posts, we've explored [the basics of Air](01-introduction-to-air-framework.md) and [mastered Air Tags](02-mastering-air-tags.md). Now it's time to understand how Air handles routing - the mechanism that directs incoming requests to the appropriate handler functions.

## Understanding Routing in Air

Routing is the process of mapping URLs to specific functions that handle requests. Air, being built on top of FastAPI, inherits FastAPI's powerful and intuitive routing system while adding its own conveniences.

In Air, routing works similarly to FastAPI, using decorators to associate URL paths with handler functions:

```python
import air

app = air.Air()

@app.get("/")
def home():
    return air.layouts.mvpcss(
        air.H1("Welcome to My Site"),
        air.P("This is the home page.")
    )
```

## Basic HTTP Method Routing

Air supports all standard HTTP methods through corresponding decorators. Let's explore each one:

### GET Requests

GET is the most common HTTP method, used for retrieving data:

```python
@app.get("/")
def home():
    return air.layouts.mvpcss(
        air.H1("Home Page"),
        air.P("Welcome to our website!")
    )

@app.get("/about")
def about():
    return air.layouts.mvpcss(
        air.H1("About Us"),
        air.P("Learn more about our company.")
    )
```

### POST Requests

POST is used for submitting data, typically from forms:

```python
@app.post("/contact")
async def contact_form(request: air.Request):
    form_data = await request.form()
    name = form_data.get("name")
    email = form_data.get("email")
    message = form_data.get("message")
    
    # Process the form data (save to database, send email, etc.)
    
    return air.layouts.mvpcss(
        air.H1("Thank You!"),
        air.P(f"Thanks for your message, {name}!")
    )
```

### PUT Requests

PUT is used for updating resources:

```python
@app.put("/api/users/{user_id}")
async def update_user(user_id: int, request: air.Request):
    # Get JSON data from request
    user_data = await request.json()
    
    # Update user in database
    # ...
    
    return {"message": f"User {user_id} updated successfully"}
```

### DELETE Requests

DELETE is used for removing resources:

```python
@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    # Delete user from database
    # ...
    
    return {"message": f"User {user_id} deleted successfully"}
```

### PATCH Requests

PATCH is used for partial updates:

```python
@app.patch("/api/users/{user_id}")
async def partial_update_user(user_id: int, request: air.Request):
    # Get partial data from request
    update_data = await request.json()
    
    # Apply partial update to user
    # ...
    
    return {"message": f"User {user_id} partially updated"}
```

## Route Parameters

Air supports both path parameters and query parameters for dynamic routing.

### Path Parameters

Path parameters are defined in the route path using curly braces:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    # The user_id parameter is automatically converted to an integer
    return air.layouts.mvpcss(
        air.H1(f"User Profile: {user_id}"),
        air.P(f"Details for user #{user_id}")
    )

@app.get("/posts/{year}/{month}/{day}")
def get_post_by_date(year: int, month: int, day: int):
    return air.layouts.mvpcss(
        air.H1(f"Posts from {year}-{month:02d}-{day:02d}"),
        air.P(f"All posts published on {year}-{month:02d}-{day:02d}")
    )
```

### Query Parameters

Query parameters are automatically extracted from the URL and passed as function arguments:

```python
@app.get("/search")
def search_posts(query: str, page: int = 1, limit: int = 10):
    # query is required, page and limit have default values
    return air.layouts.mvpcss(
        air.H1(f"Search Results for: {query}"),
        air.P(f"Page {page}, showing {limit} results per page")
    )

# This would handle URLs like:
# /search?query=python&page=2&limit=20
```

### Optional Parameters

You can make parameters optional by providing default values:

```python
@app.get("/products")
def list_products(category: str = None, min_price: float = 0.0, max_price: float = 1000.0):
    filters = []
    if category:
        filters.append(f"Category: {category}")
    filters.append(f"Price range: ${min_price} - ${max_price}")
    
    return air.layouts.mvpcss(
        air.H1("Product List"),
        air.P("Active filters: " + ", ".join(filters))
    )
```

## The @app.page Decorator

Air introduces a special `@app.page` decorator that simplifies creating web pages. This decorator automatically converts function names to URL paths:

```python
@app.page
def index():
    # Maps to "/"
    return air.layouts.mvpcss(air.H1("Home"))

@app.page
def about_us():
    # Maps to "/about-us"
    return air.layouts.mvpcss(air.H1("About Us"))

@app.page
def contact_info():
    # Maps to "/contact-info"
    return air.layouts.mvpcss(air.H1("Contact Information"))
```

This is particularly useful for quickly prototyping web pages without having to manually specify routes.

## Advanced Routing Features

### Route Dependencies

Air supports dependencies that can be injected into route handlers:

```python
from fastapi import Depends

def get_current_user():
    # Simulate getting current user
    return {"username": "alice", "role": "admin"}

@app.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return air.layouts.mvpcss(
        air.H1(f"Profile for {current_user['username']}"),
        air.P(f"Role: {current_user['role']}")
    )
```

### Request Validation with Pydantic

You can use Pydantic models for request validation:

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

@app.post("/api/users")
async def create_user(user: UserCreate):
    # user is automatically validated and converted to UserCreate instance
    return {
        "message": "User created successfully",
        "user": {
            "name": user.name,
            "email": user.email,
            "age": user.age
        }
    }
```

### Response Models

You can also specify response models for better API documentation:

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user_api(user_id: int):
    # Return data that matches UserResponse model
    return {
        "id": user_id,
        "name": "Alice",
        "email": "alice@example.com"
    }
```

## Combining REST APIs with Web Pages

One of Air's strengths is its ability to serve both web pages and REST APIs from the same application:

```python
import air
from fastapi import FastAPI

# Create Air app for web pages
app = air.Air()

# Create FastAPI app for REST API
api = FastAPI()

# Web page routes
@app.get("/")
def home():
    return air.layouts.mvpcss(
        air.H1("My Website"),
        air.P(air.A("API Documentation", href="/api/docs"))
    )

# REST API routes
@api.get("/users")
def get_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@api.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Alice"}

# Mount the API app under /api
app.mount("/api", api)
```

## Route Organization with Routers

For larger applications, you can organize routes using routers:

```python
import air

app = air.Air()

# Create a router for user-related routes
user_router = air.AirRouter(prefix="/users", tags=["users"])

@user_router.get("/")
def list_users():
    return air.layouts.mvpcss(air.H1("User List"))

@user_router.get("/{user_id}")
def get_user(user_id: int):
    return air.layouts.mvpcss(air.H1(f"User {user_id}"))

# Include the router in the main app
app.include_router(user_router)

# Create a router for admin routes
admin_router = air.AirRouter(prefix="/admin", tags=["admin"])

@admin_router.get("/")
def admin_dashboard():
    return air.layouts.mvpcss(air.H1("Admin Dashboard"))

# Include with additional prefix
app.include_router(admin_router, prefix="/admin")
```

## Practical Example: Blog Application

Let's put everything together with a practical blog application example:

```python
import air
from typing import Optional
from pydantic import BaseModel

app = air.Air()

# Pydantic models
class PostCreate(BaseModel):
    title: str
    content: str
    author: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    published: bool = True

# In-memory storage (in a real app, you'd use a database)
posts = [
    {"id": 1, "title": "First Post", "content": "This is the first post.", "author": "Alice"},
    {"id": 2, "title": "Second Post", "content": "This is the second post.", "author": "Bob"}
]

# Web page routes
@app.page
def index():
    """Home page showing all blog posts"""
    post_list = air.Ul(
        *[air.Li(
            air.A(post["title"], href=f"/posts/{post['id']}"),
            f" by {post['author']}"
        ) for post in posts]
    )
    
    return air.layouts.mvpcss(
        air.H1("My Blog"),
        air.P(air.A("Create New Post", href="/create-post")),
        post_list
    )

@app.page
def create_post_page():
    """Page for creating new blog posts"""
    return air.layouts.mvpcss(
        air.H1("Create New Post"),
        air.Form(
            air.Label("Title:", for_="title"),
            air.Input(type="text", id="title", name="title", required=True),
            
            air.Label("Author:", for_="author"),
            air.Input(type="text", id="author", name="author", required=True),
            
            air.Label("Content:", for_="content"),
            air.Textarea(id="content", name="content", rows=10, required=True),
            
            air.Button("Create Post", type="submit"),
            method="POST",
            action="/create-post"
        )
    )

# API routes
@app.get("/api/posts", response_model=list[PostResponse])
def get_posts_api():
    """API endpoint to get all posts"""
    return posts

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post_api(post_id: int):
    """API endpoint to get a specific post"""
    for post in posts:
        if post["id"] == post_id:
            return post
    return {"error": "Post not found"}, 404

@app.post("/api/posts", response_model=PostResponse)
async def create_post_api(post: PostCreate):
    """API endpoint to create a new post"""
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "content": post.content,
        "author": post.author
    }
    posts.append(new_post)
    return new_post

# Form handlers
@app.post("/create-post")
async def create_post_handler(request: air.Request):
    """Handle form submission for creating posts"""
    form_data = await request.form()
    title = form_data.get("title")
    author = form_data.get("author")
    content = form_data.get("content")
    
    # Create new post
    new_post = {
        "id": len(posts) + 1,
        "title": title,
        "content": content,
        "author": author
    }
    posts.append(new_post)
    
    # Redirect to the new post
    return air.RedirectResponse(f"/posts/{new_post['id']}", status_code=303)

@app.page
def post_detail(post_id: int):
    """Page showing a specific blog post"""
    for post in posts:
        if post["id"] == post_id:
            return air.layouts.mvpcss(
                air.H1(post["title"]),
                air.P(f"By {post['author']}"),
                air.P(post["content"]),
                air.A("← Back to Home", href="/")
            )
    
    return air.layouts.mvpcss(
        air.H1("Post Not Found"),
        air.P("The requested post could not be found."),
        air.A("← Back to Home", href="/")
    )

# API route for deleting posts
@app.delete("/api/posts/{post_id}")
async def delete_post_api(post_id: int):
    """API endpoint to delete a post"""
    global posts
    posts = [post for post in posts if post["id"] != post_id]
    return {"message": f"Post {post_id} deleted"}
```

## Best Practices for Routing

### 1. Use Descriptive Route Names

```python
# Good
@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int):
    pass

# Avoid
@app.get("/u/{id}/p")
def get_up(id: int):
    pass
```

### 2. Group Related Routes with Routers

```python
# Organize related functionality
user_router = air.AirRouter(prefix="/users", tags=["users"])
post_router = air.AirRouter(prefix="/posts", tags=["posts"])
admin_router = air.AirRouter(prefix="/admin", tags=["admin"])
```

### 3. Use Consistent Naming Conventions

```python
# Use nouns for resources
@app.get("/users")          # Good
@app.get("/users/{user_id}") # Good

# Avoid verbs in URLs for REST APIs
@app.get("/get-users")      # Avoid
```

### 4. Handle Errors Gracefully

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = find_user(user_id)
    if not user:
        # Return appropriate error response
        return air.layouts.mvpcss(
            air.H1("User Not Found"),
            air.P(f"No user found with ID {user_id}")
        ), 404
    return user
```

## What's Coming Next

In our next post, we'll explore forms and validation in depth, covering:

1. Creating HTML forms with Air Tags
2. Handling form submissions
3. Validating user input with Pydantic
4. The AirForm class for model-based forms
5. Error handling and user feedback

## Conclusion

Routing is a fundamental aspect of web development, and Air provides a powerful yet intuitive system for handling URLs and HTTP methods. By leveraging FastAPI's routing capabilities while adding conveniences like the `@app.page` decorator, Air makes it easy to build both traditional web applications and modern REST APIs.

Key takeaways from this post:

1. Air supports all standard HTTP methods with intuitive decorators
2. Path and query parameters are automatically extracted and validated
3. The `@app.page` decorator simplifies web page routing
4. You can combine web pages and REST APIs in the same application
5. Routers help organize complex applications

This routing system, combined with the Air Tags we learned about in the previous post, gives you a solid foundation for building web applications with Air.

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for weekly updates. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

See you in the next post where we'll dive into forms and validation!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [Mastering Air Tags](02-mastering-air-tags.md)*

## Quiz: Test Your Knowledge

1. Which HTTP method decorator would you use to handle form submissions in Air?
   a) @app.get
   b) @app.post
   c) @app.put
   d) @app.delete

2. How does Air automatically convert function names to URL paths with the @app.page decorator?
   a) By converting underscores to slashes
   b) By converting underscores to hyphens
   c) By removing all special characters
   d) By capitalizing each word

3. What is the correct way to define a path parameter in Air?
   a) @app.get("/users/:user_id")
   b) @app.get("/users/{user_id}")
   c) @app.get("/users/<user_id>")
   d) @app.get("/users/user_id")

4. True or False: Air only supports asynchronous route handlers and does not support synchronous functions.

5. True or False: Query parameters in Air are automatically extracted from the URL and passed as function arguments.

6. Explain the difference between path parameters and query parameters in Air routing, and provide an example of when you would use each.

### Answers:
1. b) @app.post
2. b) By converting underscores to hyphens
3. b) @app.get("/users/{user_id}")
4. False - Air supports both synchronous and asynchronous route handlers
5. True
6. Path parameters are defined in the route path using curly braces (e.g., /users/{user_id}) and are used for required identifiers that are part of the resource URL. Query parameters are automatically extracted from the URL query string (e.g., /search?query=python&page=1) and are used for optional parameters like filters or pagination.
