# Part 8: Database Integration in the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this eighth installment, we're diving deep into one of the most critical aspects of web development: **Database Integration**.

In our previous posts, we've covered [the basics of Air](01-introduction-to-air-framework.md), [mastered Air Tags](02-mastering-air-tags.md), learned about [routing and HTTP methods](03-routing-and-http-methods.md), explored [forms and validation](04-forms-and-validation.md), understood [templates and Jinja integration](05-templates-and-jinja-integration.md), enhanced our applications with [Tailwind CSS styling](06-styling-with-tailwind-css.md), and made our apps more interactive with [HTMX integration](07-htmx-integration.md). Now it's time to give our Air applications persistent storage with database integration.

## Introduction to Database Integration with Air

Most real-world web applications require some form of data persistence. Whether it's user accounts, blog posts, product catalogs, or analytics data, databases are essential for storing and retrieving information. The Air framework, built on top of FastAPI, seamlessly integrates with popular Python database libraries, making it easy to add database functionality to your applications.

### Database Options Available with Air

Air supports multiple database integration options:

1. **SQLModel** - A library that combines SQLAlchemy and Pydantic, designed specifically for FastAPI
2. **SQLAlchemy** - The most popular Python SQL toolkit and Object Relational Mapper
3. **Tortoise ORM** - An easy-to-use asyncio ORM inspired by Django
4. **Databases** - An async database client for Python

For this tutorial, we'll focus on SQLModel as it's specifically designed for FastAPI-based frameworks like Air and provides the best integration experience.

### Installing Database Dependencies

To use SQLModel with Air, you'll need to install the required packages:

```bash
pip install sqlmodel
# Or if you're using uv
uv add sqlmodel
```

If you want to use Air's built-in SQLModel support, you can install it as an extra:

```bash
pip install "air[sqlmodel]"
# Or with uv
uv add "air[sqlmodel]"
```

## Creating Database Models

Database models define the structure of your data and how it maps to database tables. With SQLModel, you can create models that serve as both Pydantic models (for validation) and SQLAlchemy models (for database operations).

### Basic Model Definition

Let's start by creating a simple model for a blog application:

```python
from sqlmodel import Field, SQLModel, create_engine
from typing import Optional
from datetime import datetime

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: str
    author: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    published: bool = Field(default=False)
    
    def __repr__(self):
        return f"<Post(title='{self.title}', author='{self.author}')>"
```

Let's break down this model:

1. **Inheritance**: Our [Post](file:///Users/macbookair/Documents/REACT%20BLOG%20APP/AIR%20PROJECTS/AIR%20TUTORIALS/helloair/venv/lib/python3.13/site-packages/pip/_vendor/rich/_export_format.py#L0-L1) class inherits from [SQLModel](file:///Users/macbookair/Documents/REACT%20BLOG%20APP/AIR%20PROJECTS/AIR%20TUTORIALS/helloair/venv/lib/python3.13/site-packages/sqlmodel/main.py#L107-L258) and uses `table=True` to indicate it should be mapped to a database table
2. **Fields**: Each attribute represents a column in the database table
3. **Primary Key**: The `id` field is marked as the primary key with auto-increment behavior
4. **Field Constraints**: We use `Field()` to add constraints like `max_length` and `default` values
5. **Default Values**: `created_at` uses `default_factory` to set the current timestamp when a record is created

### Advanced Model Features

Let's create a more complex example with relationships:

```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship - one user can have many posts
    posts: List["Post"] = Relationship(back_populates="author")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    published: bool = Field(default=False)
    
    # Foreign key relationship
    author_id: int = Field(foreign_key="user.id")
    author: User = Relationship(back_populates="posts")
    
    def __repr__(self):
        return f"<Post(title='{self.title}', author_id={self.author_id})>"
```

In this example:

1. **Unique Fields**: Both `username` and `email` are marked as unique
2. **Indexing**: `username` has an index for faster queries
3. **Foreign Keys**: `author_id` references the `id` field in the [User](file:///Users/macbookair/Documents/REACT%20BLOG%20APP/AIR%20PROJECTS/AIR%20TUTORIALS/helloair/venv/lib/python3.13/site-packages/pip/_vendor/rich/_export_format.py#L0-L1) table
4. **Relationships**: We establish bidirectional relationships between [User](file:///Users/macbookair/Documents/REACT%20BLOG%20APP/AIR%20PROJECTS/AIR%20TUTORIALS/helloair/venv/lib/python3.13/site-packages/pip/_vendor/rich/_export_format.py#L0-L1) and [Post](file:///Users/macbookair/Documents/REACT%20BLOG%20APP/AIR%20PROJECTS/AIR%20TUTORIALS/helloair/venv/lib/python3.13/site-packages/pip/_vendor/rich/_export_format.py#L0-L1) models

### Model Validation

Since SQLModel inherits from Pydantic, you get automatic validation:

```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    description: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Custom validator
    @property
    def is_in_stock(self) -> bool:
        return self.stock_quantity > 0
```

## Database Configuration and Connection

Before we can use our models, we need to configure the database connection.

### Setting Up the Database Engine

```python
from sqlmodel import create_engine, Session
import os

# For SQLite (development)
DATABASE_URL = "sqlite:///./blog.db"

# For PostgreSQL (production)
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

### Creating Tables

To create the database tables based on your models:

```python
from sqlmodel import SQLModel

# Create all tables
SQLModel.metadata.create_all(engine)
```

### Integrating with Air Application

Let's integrate database functionality into our Air application:

```python
import air
from sqlmodel import create_engine, Session, select
from contextlib import asynccontextmanager

# Database setup
DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create tables
from models import User, Post
SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: air.Air):
    # Startup: Create tables
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown: Cleanup if needed

app = air.Air(lifespan=lifespan)

# Dependency for getting database session
def get_session():
    with Session(engine) as session:
        yield session
```

## CRUD Operations with Air

Now let's implement Create, Read, Update, and Delete operations in our Air application.

### Creating Records

``python
from fastapi import Depends
from sqlmodel import Session, select

@app.page
def create_post_form():
    return air.layouts.mvpcss(
        air.H1("Create New Post", class_="text-3xl font-bold mb-6"),
        air.Form(
            air.Div(
                air.Label("Title", for_="title", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="text",
                    id="title",
                    name="title",
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Label("Author", for_="author", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="text",
                    id="author",
                    name="author",
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Label("Content", for_="content", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Textarea(
                    id="content",
                    name="content",
                    rows=6,
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Input(
                    type="checkbox",
                    id="published",
                    name="published",
                    value="on",
                    class_="mr-2"
                ),
                air.Label("Publish immediately", for_="published", class_="text-sm text-gray-700"),
                class_="mb-6"
            ),
            air.Button(
                "Create Post",
                type="submit",
                class_="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            ),
            hx_post="/posts",
            hx_target="#result",
            hx_swap="innerHTML",
            class_="bg-white p-6 rounded-lg shadow-md"
        ),
        air.Div(id="result", class_="mt-6")
    )

@app.post("/posts")
async def create_post(request: air.Request, session: Session = Depends(get_session)):
    form_data = await request.form()
    
    # Create new post
    new_post = Post(
        title=form_data.get("title", ""),
        content=form_data.get("content", ""),
        author=form_data.get("author", ""),
        published=form_data.get("published") == "on"
    )
    
    # Save to database
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    
    # Return success message
    return air.Div(
        air.Div(
            air.H3("Success!", class_="text-lg font-medium text-green-800"),
            air.P(f"Post '{new_post.title}' has been created successfully.", class_="text-green-600"),
            air.A(
                "View Post",
                href=f"/posts/{new_post.id}",
                class_="mt-2 inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded text-sm"
            ),
            class_="bg-green-50 p-4 rounded-lg"
        )
    )
```

### Reading Records

``python
@app.page
def list_posts(session: Session = Depends(get_session)):
    # Query all posts
    posts = session.exec(select(Post)).all()
    
    return air.layouts.mvpcss(
        air.H1("Blog Posts", class_="text-3xl font-bold mb-6"),
        air.Div(
            air.A(
                "Create New Post",
                href="/create-post",
                class_="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-6 inline-block"
            ),
            air.Div(
                *[air.Div(
                    air.H2(
                        air.A(post.title, href=f"/posts/{post.id}", class_="text-blue-600 hover:text-blue-800"),
                        class_="text-xl font-semibold"
                    ),
                    air.P(f"By {post.author}", class_="text-gray-600 text-sm"),
                    air.P(post.content[:150] + "...", class_="text-gray-700 mt-2"),
                    air.P(f"Created: {post.created_at.strftime('%Y-%m-%d')}", class_="text-gray-500 text-sm mt-2"),
                    air.Div(
                        air.Span(
                            "Published" if post.published else "Draft",
                            class_=f"text-xs px-2 py-1 rounded {'bg-green-100 text-green-800' if post.published else 'bg-yellow-100 text-yellow-800'}"
                        ),
                        class_="mt-2"
                    ),
                    class_="bg-white p-4 rounded-lg shadow mb-4"
                ) for post in posts],
                class_="mt-4"
            ) if posts else air.P("No posts found.", class_="text-gray-600"),
            class_="bg-white p-6 rounded-lg shadow-md"
        )
    )

@app.get("/posts/{post_id}")
def get_post(post_id: int, session: Session = Depends(get_session)):
    # Query specific post
    post = session.get(Post, post_id)
    
    if not post:
        return air.layouts.mvpcss(
            air.H1("Post Not Found", class_="text-3xl font-bold mb-6"),
            air.P("The requested post could not be found.", class_="text-gray-600"),
            air.A(
                "Back to Posts",
                href="/posts",
                class_="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded inline-block mt-4"
            )
        )
    
    return air.layouts.mvpcss(
        air.Article(
            air.H1(post.title, class_="text-3xl font-bold mb-2"),
            air.Div(
                air.Span(f"By {post.author}", class_="text-gray-600 mr-4"),
                air.Span(f"Published: {post.created_at.strftime('%Y-%m-%d')}", class_="text-gray-600"),
                class_="mb-6 text-sm"
            ),
            air.Div(
                air.P(post.content, class_="text-gray-700 leading-relaxed whitespace-pre-line"),
                class_="prose max-w-none"
            ),
            air.Div(
                air.Span(
                    "Published" if post.published else "Draft",
                    class_=f"text-xs px-2 py-1 rounded {'bg-green-100 text-green-800' if post.published else 'bg-yellow-100 text-yellow-800'}"
                ),
                class_="mt-6"
            ),
            class_="bg-white p-6 rounded-lg shadow-md"
        ),
        air.Div(
            air.A(
                "← Back to Posts",
                href="/posts",
                class_="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded inline-block mt-6"
            ),
            class_="mt-6"
        )
    )
```

### Updating Records

``python
@app.page("/posts/{post_id}/edit")
def edit_post_form(post_id: int, session: Session = Depends(get_session)):
    # Get the post to edit
    post = session.get(Post, post_id)
    
    if not post:
        return air.layouts.mvpcss(
            air.H1("Post Not Found", class_="text-3xl font-bold mb-6"),
            air.P("The requested post could not be found.", class_="text-gray-600")
        )
    
    return air.layouts.mvpcss(
        air.H1(f"Edit Post: {post.title}", class_="text-3xl font-bold mb-6"),
        air.Form(
            air.Div(
                air.Label("Title", for_="title", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="text",
                    id="title",
                    name="title",
                    value=post.title,
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Label("Author", for_="author", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Input(
                    type="text",
                    id="author",
                    name="author",
                    value=post.author,
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Label("Content", for_="content", class_="block text-sm font-medium text-gray-700 mb-1"),
                air.Textarea(
                    id="content",
                    name="content",
                    rows=6,
                    required=True,
                    class_="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Input(
                    type="checkbox",
                    id="published",
                    name="published",
                    value="on",
                    checked=post.published,
                    class_="mr-2"
                ),
                air.Label("Publish", for_="published", class_="text-sm text-gray-700"),
                class_="mb-6"
            ),
            air.Button(
                "Update Post",
                type="submit",
                class_="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            ),
            hx_put=f"/posts/{post_id}",
            hx_target="#result",
            hx_swap="innerHTML",
            class_="bg-white p-6 rounded-lg shadow-md"
        ),
        air.Div(
            air.A(
                "← Back to Post",
                href=f"/posts/{post_id}",
                class_="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded inline-block mt-4 mr-2"
            ),
            class_="mt-4"
        ),
        air.Div(id="result", class_="mt-6")
    )

@app.put("/posts/{post_id}")
async def update_post(post_id: int, request: air.Request, session: Session = Depends(get_session)):
    # Get the post to update
    post = session.get(Post, post_id)
    
    if not post:
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Post not found.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    # Get form data
    form_data = await request.form()
    
    # Update post fields
    post.title = form_data.get("title", post.title)
    post.content = form_data.get("content", post.content)
    post.author = form_data.get("author", post.author)
    post.published = form_data.get("published") == "on"
    
    # Save changes
    session.add(post)
    session.commit()
    session.refresh(post)
    
    # Return success message
    return air.Div(
        air.Div(
            air.H3("Success!", class_="text-lg font-medium text-green-800"),
            air.P("Post has been updated successfully.", class_="text-green-600"),
            air.A(
                "View Post",
                href=f"/posts/{post.id}",
                class_="mt-2 inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded text-sm"
            ),
            class_="bg-green-50 p-4 rounded-lg"
        )
    )
```

### Deleting Records

``python
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, session: Session = Depends(get_session)):
    # Get the post to delete
    post = session.get(Post, post_id)
    
    if not post:
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Post not found.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    
    # Delete the post
    session.delete(post)
    session.commit()
    
    # Return success message with redirect
    return air.Div(
        air.Script("window.location.href = '/posts';"),
        air.Div(
            air.H3("Success!", class_="text-lg font-medium text-green-800"),
            air.P("Post has been deleted successfully.", class_="text-green-600"),
            class_="bg-green-50 p-4 rounded-lg"
        )
    )

# Alternative: Delete with confirmation
@app.page("/posts/{post_id}/delete")
def delete_post_confirmation(post_id: int, session: Session = Depends(get_session)):
    # Get the post to delete
    post = session.get(Post, post_id)
    
    if not post:
        return air.layouts.mvpcss(
            air.H1("Post Not Found", class_="text-3xl font-bold mb-6"),
            air.P("The requested post could not be found.", class_="text-gray-600")
        )
    
    return air.layouts.mvpcss(
        air.H1("Delete Post", class_="text-3xl font-bold mb-6"),
        air.Div(
            air.H2(post.title, class_="text-xl font-semibold mb-2"),
            air.P("Are you sure you want to delete this post? This action cannot be undone.", class_="text-gray-700 mb-6"),
            air.Div(
                air.Button(
                    "Cancel",
                    hx_get=f"/posts/{post_id}",
                    hx_target="body",
                    hx_swap="innerHTML",
                    class_="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded mr-2"
                ),
                air.Button(
                    "Delete Post",
                    hx_delete=f"/posts/{post_id}",
                    hx_target="body",
                    hx_swap="innerHTML",
                    class_="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                ),
                class_="flex justify-end"
            ),
            class_="bg-white p-6 rounded-lg shadow-md"
        )
    )
```

## Advanced Database Patterns

### Pagination

When dealing with large datasets, pagination becomes essential:

```python
from sqlmodel import select
from math import ceil

@app.page("/posts")
def list_posts(page: int = 1, per_page: int = 5, session: Session = Depends(get_session)):
    # Calculate offset
    offset = (page - 1) * per_page
    
    # Query posts with pagination
    statement = select(Post).offset(offset).limit(per_page)
    posts = session.exec(statement).all()
    
    # Get total count for pagination calculation
    total_posts = session.exec(select(Post)).count()
    total_pages = ceil(total_posts / per_page)
    
    return air.layouts.mvpcss(
        air.H1("Blog Posts", class_="text-3xl font-bold mb-6"),
        air.Div(
            # Posts listing
            air.Div(
                *[air.Div(
                    air.H2(
                        air.A(post.title, href=f"/posts/{post.id}", class_="text-blue-600 hover:text-blue-800"),
                        class_="text-xl font-semibold"
                    ),
                    air.P(post.content[:150] + "...", class_="text-gray-700 mt-2"),
                    class_="bg-white p-4 rounded-lg shadow mb-4"
                ) for post in posts],
                class_="mt-4"
            ) if posts else air.P("No posts found.", class_="text-gray-600"),
            
            # Pagination controls
            air.Div(
                air.Div(
                    # Previous button
                    air.A(
                        "Previous",
                        href=f"/posts?page={page-1}" if page > 1 else "#",
                        class_=f"px-4 py-2 rounded-l-md {'bg-gray-300 cursor-not-allowed' if page <= 1 else 'bg-blue-500 hover:bg-blue-700 text-white'}"
                    ),
                    
                    # Page numbers
                    *[air.A(
                        str(i),
                        href=f"/posts?page={i}",
                        class_=f"px-4 py-2 {'bg-blue-500 text-white' if i == page else 'bg-white hover:bg-gray-100 border'}"
                    ) for i in range(max(1, page-2), min(total_pages+1, page+3))],
                    
                    # Next button
                    air.A(
                        "Next",
                        href=f"/posts?page={page+1}" if page < total_pages else "#",
                        class_=f"px-4 py-2 rounded-r-md {'bg-gray-300 cursor-not-allowed' if page >= total_pages else 'bg-blue-500 hover:bg-blue-700 text-white'}"
                    ),
                    class_="flex items-center justify-center space-x-1 mt-6"
                ),
                class_="mt-8"
            ) if total_pages > 1 else None,
            class_="bg-white p-6 rounded-lg shadow-md"
        )
    )
```

### Search and Filtering

Implementing search functionality:

```python
from sqlmodel import select, or_

@app.page("/posts/search")
def search_posts(query: str = "", session: Session = Depends(get_session)):
    posts = []
    
    if query:
        # Search in title, content, and author
        statement = select(Post).where(
            or_(
                Post.title.contains(query),
                Post.content.contains(query),
                Post.author.contains(query)
            )
        )
        posts = session.exec(statement).all()
    
    return air.layouts.mvpcss(
        air.H1("Search Posts", class_="text-3xl font-bold mb-6"),
        air.Form(
            air.Div(
                air.Div(
                    air.Input(
                        type="text",
                        name="query",
                        value=query,
                        placeholder="Search posts...",
                        class_="flex-1 px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    ),
                    air.Button(
                        "Search",
                        type="submit",
                        class_="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded-r-md"
                    ),
                    class_="flex"
                ),
                class_="mb-6"
            ),
            hx_get="/posts/search",
            hx_target="#search-results",
            hx_swap="innerHTML",
            hx_include="[name='query']",
            class_="mb-6"
        ),
        air.Div(
            air.H2(f"Search Results ({len(posts)} found)" if query else "Enter a search term", class_="text-xl font-semibold mb-4"),
            air.Div(
                *[air.Div(
                    air.H3(
                        air.A(post.title, href=f"/posts/{post.id}", class_="text-blue-600 hover:text-blue-800"),
                        class_="text-lg font-medium"
                    ),
                    air.P(f"By {post.author}", class_="text-gray-600 text-sm"),
                    air.P(post.content[:100] + "...", class_="text-gray-700 mt-1"),
                    class_="bg-gray-50 p-4 rounded-lg mb-4"
                ) for post in posts],
                class_="mt-4"
            ) if posts else (air.P("No posts found matching your search.", class_="text-gray-600") if query else None),
            id="search-results"
        )
    )
```

### Transactions

For operations that need to be atomic:

```python
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

@app.post("/posts/bulk-create")
async def bulk_create_posts(request: air.Request, session: Session = Depends(get_session)):
    try:
        # Begin transaction
        with session.begin():
            form_data = await request.form()
            titles = form_data.getlist("titles")
            authors = form_data.getlist("authors")
            
            # Create multiple posts in a single transaction
            created_posts = []
            for title, author in zip(titles, authors):
                if title and author:  # Skip empty entries
                    post = Post(title=title, content="", author=author)
                    session.add(post)
                    created_posts.append(post)
            
            # Commit all changes
            session.commit()
            
            # Refresh to get IDs
            for post in created_posts:
                session.refresh(post)
            
            return air.Div(
                air.Div(
                    air.H3("Success!", class_="text-lg font-medium text-green-800"),
                    air.P(f"Successfully created {len(created_posts)} posts.", class_="text-green-600"),
                    class_="bg-green-50 p-4 rounded-lg"
                )
            )
    except IntegrityError as e:
        session.rollback()
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P("Failed to create posts due to a database constraint violation.", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
    except Exception as e:
        session.rollback()
        return air.Div(
            air.Div(
                air.H3("Error", class_="text-lg font-medium text-red-800"),
                air.P(f"An unexpected error occurred: {str(e)}", class_="text-red-600"),
                class_="bg-red-50 p-4 rounded-lg"
            )
        )
```

## Best Practices for Database Integration

### 1. Use Dependency Injection for Sessions

Always use FastAPI's dependency injection system for database sessions:

```python
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        yield session

# Use as dependency
@app.get("/posts")
def list_posts(session: Session = Depends(get_session)):
    # Your code here
    pass
```

### 2. Handle Database Connections Properly

Use context managers and ensure connections are closed:

```python
# Good - Automatic cleanup
def get_session():
    with Session(engine) as session:
        yield session
    # Session is automatically closed

# Avoid - Manual cleanup that might be forgotten
def get_session_bad():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()  # Might be forgotten
```

### 3. Use Connection Pooling for Production

For production applications, configure connection pooling:

```python
from sqlmodel import create_engine

# Configure connection pool
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False  # Turn off in production
)
```

### 4. Implement Proper Error Handling

Handle database errors gracefully:

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

@app.post("/users")
async def create_user(user_data: dict, session: Session = Depends(get_session)):
    try:
        user = User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise air.HTTPException(status_code=400, detail="User already exists")
    except SQLAlchemyError:
        session.rollback()
        raise air.HTTPException(status_code=500, detail="Database error occurred")
```

### 5. Use Asynchronous Operations When Possible

For high-concurrency applications, consider async database operations:

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

# Async engine
async_engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

# Async session
async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session

# Async endpoint
@app.get("/async-posts")
async def list_posts_async(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    return posts
```

## What's Coming Next

In our next post, we'll explore authentication and security, covering:

1. User authentication fundamentals
2. Implementing login and logout functionality
3. Session management and security best practices
4. OAuth integration for social logins

## Conclusion

Database integration is a crucial component of any real-world web application, and the Air framework makes it remarkably straightforward. By leveraging SQLModel's combination of SQLAlchemy and Pydantic, you get the best of both worlds: powerful database ORM capabilities and robust data validation.

Key takeaways from this post:

1. Air integrates seamlessly with SQLModel, SQLAlchemy, and other database libraries
2. SQLModel models serve as both database tables and Pydantic validation models
3. CRUD operations in Air follow familiar patterns with proper error handling
4. Advanced patterns like pagination, search, and transactions enhance user experience
5. Following best practices ensures robust and maintainable database code

With database integration mastered, your Air applications can now persist and manage data effectively. The combination of Air's Python-based approach and SQLModel's elegant design provides an efficient workflow for building data-driven web applications.

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for weekly updates. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

See you in the next post where we'll dive into authentication and security!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [HTMX Integration](07-htmx-integration.md)*

## Quiz: Test Your Knowledge

1. Which library does Air primarily use for database integration?
   a) SQLAlchemy
   b) SQLModel
   c) Django ORM
   d) Peewee

2. What is the correct way to define a database model in Air using SQLModel?
   a) class User(BaseModel):
   b) class User(SQLModel, table=True):
   c) class User(Model):
   d) class User(DatabaseModel):

3. How do you handle database sessions in Air route handlers?
   a) Create a new session in each handler
   b) Use global session variables
   c) Use FastAPI dependency injection
   d) Manually manage connections

4. True or False: SQLModel models in Air serve as both database table definitions and Pydantic validation models.

5. True or False: You should always use synchronous database operations in Air applications for better performance.

6. Explain the benefits of using SQLModel over raw SQLAlchemy in Air applications, and how it integrates with Pydantic validation.

### Answers:
1. b) SQLModel
2. b) class User(SQLModel, table=True):
3. c) Use FastAPI dependency injection
4. True
5. False - For high-concurrency applications, asynchronous database operations should be used
6. SQLModel combines SQLAlchemy's powerful ORM capabilities with Pydantic's data validation features. This means you get both database mapping and data validation from a single model definition. In Air applications, this is particularly beneficial because it provides seamless integration with the framework's form validation and API response handling, reducing code duplication and ensuring consistent data handling throughout the application.
