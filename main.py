from pathlib import Path
from frontmatter import Frontmatter
import markdown
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from air import Air, AirForm, AirField, RedirectResponse
import secrets
import hashlib
import fastapi
import air

def get_articles() -> list[dict]:
    """Read all markdown files in the articles directory and return their content."""
    articles = []
    for path in Path("articles").glob("*.md"):
        articles.append(Frontmatter.read_file(path))
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


def get_article(slug: str) -> dict | None:
    """Get a specific article by its slug."""
    for article in get_articles():
        if article["attributes"]["slug"] == slug:
            return article
    return None


def get_article_by_id(article_id: int) -> dict | None:
    """Get an article by its index (ID)."""
    articles = get_articles()
    if 0 <= article_id < len(articles):
        return articles[article_id]
    return None


def get_article_index_by_slug(slug: str) -> int | None:
    """Get the index of an article by its slug."""
    articles = get_articles()
    for i, article in enumerate(articles):
        if article["attributes"]["slug"] == slug:
            return i
    return None


# Initialize Air app with session support
app = Air()
app.add_middleware(
    air.SessionMiddleware,
    secret_key=secrets.token_urlsafe(32)
)
api = fastapi.FastAPI()


@app.page
def index():
    """Home page with latest articles."""
    title = "My Personal Blog"
    articles = get_articles()

    # Check if user is logged in
    is_admin = False  # In a real app, check session here

    return air.layouts.mvpcss(
        air.Title(title),
        air.Header(
            air.Nav(
                air.A("My Personal Blog", href="/", style="font-size: 1.5em; font-weight: bold;"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Contact", href="/contact"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("API Docs", href="/docs", target="_blank") if app.docs_url else "",
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Admin", href="/admin") if is_admin else air.A("Login", href="/login")
            )
        ),
        air.H1(title),
        air.P("Welcome to my personal blog!"),
        air.H2("Latest Articles"),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                        style="font-size: 1.2em; font-weight: bold; display: block;"
                    ),
                    air.Small(
                        f"{article['attributes']['description']} - "
                        f"Published: {article['attributes']['date']} by {article['attributes']['author']}"
                    ),
                    air.Div(
                        *[air.Span(f"#{tag}", style="margin-right: 0.5rem; color: #666;") 
                          for tag in article['attributes']['tags']],
                        style="margin-top: 0.25rem;"
                    )
                )
                for article in articles
            ]
        )
    )


@app.get("/{slug}")
def article_detail(slug: str):
    """Display a single article with full details."""
    article = get_article(slug)
    if not article:
        return air.layouts.mvpcss(
            air.H1("Article not found"),
            air.P("The requested article could not be found."),
            air.A("← Back to Home", href="/")
        )

    # Convert markdown content to HTML
    html_content = markdown.markdown(article["body"])

    return air.layouts.mvpcss(
        air.Title(article["attributes"]["title"]),
        air.Article(
            air.H1(article["attributes"]["title"]),
            air.Div(
                air.Time(
                    f'Published: {article["attributes"]["date"]}',
                    datetime=str(article["attributes"]["date"])
                ),
                air.P(f"By {article['attributes']['author']}"),
                style="color: #666; margin-bottom: 1rem;"
            ),
            air.Div(air.Raw(html_content), style="line-height: 1.6;"),
            air.Div(
                *[air.Span(f"#{tag}", style="margin-right: 0.5rem;") for tag in article['attributes']['tags']],
                style="margin-top: 1rem; color: #666;"
            )
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


# Contact Form
class ContactForm(AirForm):
    class model(BaseModel):
        name: str = Field(..., min_length=2, max_length=50, description="Your name")
        email: str = AirField(type="email", label="Email Address", required=True)
        subject: str = Field(..., min_length=5, max_length=100, description="Subject of your message")
        message: str = Field(..., min_length=10, max_length=1000, description="Your message")


contact_form = ContactForm()

@app.page
def contact():
    """Contact form page."""
    return air.layouts.mvpcss(
        air.Title("Contact Us"),
        air.H1("Contact Us"),
        air.P("Have questions or feedback? Get in touch!"),
        air.Form(
            contact_form.render(),  # Render the form with AirForm
            method="POST",
            action="/contact",
            style="display: flex; flex-direction: column; gap: 1rem; max-width: 500px;"
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/contact")
async def contact_handler(request: air.Request):
    """Handle contact form submission with validation."""
    form_data = await request.form()

    # Extract string values from form data
    form_dict = {}
    for key, value in form_data.items():
        # Handle both string values and UploadFile objects
        if hasattr(value, 'filename'):
            # This is an UploadFile object, skip it
            continue
        else:
            # This is a string value
            form_dict[key] = str(value)

    # Validate the form
    validation_result = contact_form.validate(form_dict)
    if validation_result is True:
        # Process valid data
        validated_data = contact_form.model(**form_dict)
        data_dict = validated_data.model_dump()

        # In a real application, you would send an email or save to database
        # print(f"Contact form submitted: {data_dict}")

        return air.layouts.mvpcss(
            air.H1("Thank You!"),
            air.P(f"Your message has been sent, {data_dict['name']}!"),
            air.P("We'll get back to you soon."),
            air.Nav(
                air.A("← Back to Home", href="/"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Send Another Message", href="/contact")
            )
        )
    else:
        # Form has errors, re-render with errors
        return air.layouts.mvpcss(
            air.Title("Contact Us - Error"),
            air.H1("Contact Us"),
            air.P("Please correct the errors below:"),
            air.Form(
                contact_form.render(),  # Renders form with errors
                method="POST",
                action="/contact",
                style="display: flex; flex-direction: column; gap: 1rem; max-width: 500px;"
            ),
            air.Nav(
                air.A("← Back to Home", href="/")
            )
        )


# API Endpoints
# API Endpoints
@api.get("/articles")
def api_articles():
    """Return all articles as JSON."""
    articles = get_articles()
    # Return only the attributes, not the full frontmatter object
    return {
        "articles": [
            {
                "title": article["attributes"]["title"],
                "slug": article["attributes"]["slug"],
                "description": article["attributes"]["description"],
                "date": article["attributes"]["date"],
                "author": article["attributes"]["author"],
                "tags": article["attributes"]["tags"]
            }
            for article in articles
        ]
    }


@api.get("/articles/{slug}")
def api_article_detail(slug: str):
    """Return a specific article as JSON."""
    article = get_article(slug)
    if not article:
        raise fastapi.exceptions.HTTPException(status_code=404)

    return {
        "title": article["attributes"]["title"],
        "slug": article["attributes"]["slug"],
        "description": article["attributes"]["description"],
        "date": article["attributes"]["date"],
        "author": article["attributes"]["author"],
        "tags": article["attributes"]["tags"],
        "content": article["body"]
    }

# Mounting the API into the APP
app.mount("/api", api)


# HTMX Interactive Features
@app.page
def htmx_demo():
    """Interactive HTMX demo page."""
    return air.layouts.mvpcss(
        air.Title("HTMX Demo"),
        air.H1("HTMX Interactive Demo"),
        air.H2("Dynamic Content Without JavaScript"),

        # Counter demo
        air.Div(
            air.H3("Counter Example:"),
            air.Button("Increment", 
                      hx_post="/api/increment", 
                      hx_target="#counter", 
                      hx_swap="innerHTML",
                      class_="button"),
            air.Button("Decrement", 
                      hx_post="/api/decrement", 
                      hx_target="#counter", 
                      hx_swap="innerHTML",
                      class_="button"),
            air.Button("Reset", 
                      hx_post="/api/reset", 
                      hx_target="#counter", 
                      hx_swap="innerHTML",
                      class_="button"),
            air.Div(0, id="counter", style="font-size: 2em; margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; display: inline-block;"),
        ),

        # Search demo
        air.Div(
            air.H3("Search Example:"),
            air.Form(
                air.Input(name="q", placeholder="Search articles...", 
                         hx_post="/api/search", 
                         hx_trigger="keyup changed delay:500ms", 
                         hx_target="#search-results", 
                         hx_swap="outerHTML"),
                method="POST",
                style="margin: 1rem 0;"
            ),
            air.Div(id="search-results", style="margin-top: 1rem;"),
        ),

        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


# Global counter for HTMX demo (in production, use database or Redis)
counter = 0

@app.post("/api/increment")
def increment_counter():
    global counter
    counter += 1
    return air.Div(counter, id="counter", style="font-size: 2em; margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; display: inline-block;")

@app.post("/api/decrement")
def decrement_counter():
    global counter
    counter = max(0, counter - 1)  # Don't go below 0
    return air.Div(counter, id="counter", style="font-size: 2em; margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; display: inline-block;")

@app.post("/api/reset")
def reset_counter():
    global counter
    counter = 0
    return air.Div(counter, id="counter", style="font-size: 2em; margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; display: inline-block;")

@app.post("/api/search")
async def search_articles(request: air.Request):
    """HTMX search endpoint."""
    form_data = await request.form()
    query_obj = form_data.get("q", "")
    # Convert to string if it's not already
    query = str(query_obj).lower() if query_obj else ""

    if not query:
        return air.Div("Enter a search term", id="search-results", style="margin-top: 1rem;")

    articles = get_articles()
    results = [
        article for article in articles 
        if query in article["attributes"]["title"].lower() 
        or query in article["attributes"]["description"].lower()
        or query in article["body"].lower()
    ]

    if not results:
        return air.Div("No results found", id="search-results", style="margin-top: 1rem; color: #666;")

    result_items = [
        air.Div(
            air.A(
                result["attributes"]["title"],
                href=f"/{result['attributes']['slug']}",
                style="display: block; margin-bottom: 0.5rem; font-weight: bold;"
            ),
            air.Small(result["attributes"]["description"]),
            style="padding: 0.5rem; border-bottom: 1px solid #eee;"
        )
        for result in results[:5]  # Limit to first 5 results
    ]

    return air.Div(*result_items, id="search-results", style="margin-top: 1rem; border: 1px solid #ccc; padding: 1rem;")

# Admin section with session protection
@app.page
def login():
    """Login page."""
    return air.layouts.mvpcss(
        air.Title("Admin Login"),
        air.H1("Admin Login"),
        air.Form(
            air.Div(
                air.Label("Username", for_="username"),
                air.Input(type="text", name="username", id="username"),
            ),
            air.Div(
                air.Label("Password", for_="password"),
                air.Input(type="password", name="password", id="password"),
            ),
            air.Button("Login", type="submit"),
            method="POST",
            action="/login",
            style="display: flex; flex-direction: column; gap: 1rem; max-width: 300px;"
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/login")
async def login_handler(request: air.Request):
    """Handle login."""
    form_data = await request.form()
    username_obj = form_data.get("username")
    password_obj = form_data.get("password")
    
    # Extract string values properly
    username = ""
    password = ""
    
    # Handle username
    if username_obj is not None:
        if hasattr(username_obj, 'filename'):
            # This is an UploadFile object, which is unexpected
            username = ""
        else:
            # This is a string value
            username = str(username_obj)
    
    # Handle password
    if password_obj is not None:
        if hasattr(password_obj, 'filename'):
            # This is an UploadFile object, which is unexpected
            password = ""
        else:
            # This is a string value
            password = str(password_obj)

    # Simple demo password check (use proper authentication in real app)
    # In a real app, hash passwords and verify against database
    if password:  # Check if password is not empty
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        hashed_admin = hashlib.sha256("admin".encode()).hexdigest()  # Demo password

        if username == "admin" and hashed_input == hashed_admin:
            request.session["user"] = username
            request.session["is_logged_in"] = True
            return RedirectResponse("/admin", status_code=303)
    
    return air.layouts.mvpcss(
        air.H1("Login Failed"),
        air.P("Invalid credentials. Please try again."),
        air.A("← Back to Home", href="/")
    )


def require_login(func):
    """Decorator to require login for routes."""
    def wrapper(*args, **kwargs):
        # In a real implementation, we'd access the request through FastAPI dependencies
        # This is just a basic example
        request = kwargs.get('request') or next((arg for arg in args if hasattr(arg, 'session')), None)

        # For this example, we'll skip this decorator functionality
        # In a real app, this would properly check sessions
        return func(*args, **kwargs)
    return wrapper


@app.page
@require_login  # Would require login in a real implementation
def admin():
    """Admin page for managing content."""
    articles = get_articles()

    return air.layouts.mvpcss(
        air.Title("Admin Dashboard"),
        air.Header(
            air.H1("Admin Dashboard"),
            air.Nav(
                air.A("← Back to Home", href="/"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Logout", href="/logout")
            )
        ),
        air.H2("Manage Articles"),
        air.Div(
            air.A("Add New Article", href="/admin/new", class_="button primary"),
            style="margin-bottom: 1rem;"
        ),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        f"{i+1}. {article['attributes']['title']} ({article['attributes']['slug']})",
                        href=f"/admin/edit/{article['attributes']['slug']}"
                    ),
                    air.Span(f" - {article['attributes']['date']} | ", style="color: #666;"),
                    air.A("View", href=f"/{article['attributes']['slug']}", target="_blank"),
                    style="margin-bottom: 0.5rem;"
                )
                for i, article in enumerate(articles)
            ]
        )
    )


@app.page
def admin_new():
    """Page to create new articles."""
    # Form for creating new articles
    return air.layouts.mvpcss(
        air.Title("Create New Article"),
        air.H1("Create New Article"),
        air.Form(
            # In a real implementation, you'd have a form for title, content, etc.
            air.Div(
                air.Label("Title", for_="title"),
                air.Input(type="text", name="title", id="title", required=True),
            ),
            air.Div(
                air.Label("Slug", for_="slug"),
                air.Input(type="text", name="slug", id="slug", required=True),
            ),
            air.Div(
                air.Label("Content", for_="content"),
                air.Textarea(name="content", id="content", required=True, rows="10"),
            ),
            air.Button("Create Article", type="submit"),
            method="POST",
            action="/admin/new",
            style="display: flex; flex-direction: column; gap: 1rem;"
        ),
        air.Nav(
            air.A("← Back to Admin", href="/admin"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/admin/new")
async def admin_new_handler(request: air.Request):
    """Handle new article creation."""
    # In a real app, this would create a new markdown file
    form_data = await request.form()
    title = form_data.get("title")
    slug = form_data.get("slug")
    content = form_data.get("content")

    # Create markdown content with frontmatter
    markdown_content = f"""---
title: {title}
description: {title}
slug: {slug}
published: true
date: {datetime.now().date()}
author: Admin
tags:

- new
---

{content}
"""

    # Write to file (in real app, you'd validate and sanitize input)
    file_path = Path("articles") / f"{slug}.md"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return air.layouts.mvpcss(
        air.H1("Article Created!"),
        air.P(f"Article '{title}' has been created successfully."),
        air.Div(
            air.A("View Article", href=f"/{slug}", class_="button primary"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("Back to Admin", href="/admin"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("← Back to Home", href="/")
        )
    )


@app.get("/logout")
def logout(request: air.Request):
    """Handle logout."""
    # Clear session
    request.session.clear()
    return RedirectResponse("/", status_code=303)


# Error handlers
@app.exception_handler(404)
async def not_found(request, exc):
    return air.layouts.mvpcss(
        air.H1("Page Not Found"),
        air.P("The requested page could not be found."),
        air.A("← Back to Home", href="/")
    )


@app.exception_handler(500)
async def server_error(request, exc):
    return air.layouts.mvpcss(
        air.H1("Server Error"),
        air.P("An internal server error occurred."),
        air.A("← Back to Home", href="/")
    )