# Part 5: Templates and Jinja Integration in the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this fifth installment, we're exploring one of the most powerful features of Air: **templates and Jinja integration**.

In our previous posts, we've covered [the basics of Air](01-introduction-to-air-framework.md), [mastered Air Tags](02-mastering-air-tags.md), learned about [routing and HTTP methods](03-routing-and-http-methods.md), and explored [forms and validation](04-forms-and-validation.md). Now it's time to understand how Air seamlessly integrates with Jinja, the popular templating engine, to provide flexible and powerful template rendering capabilities.

## Understanding Templates in Air

While Air Tags provide a powerful way to generate HTML directly in Python, there are times when you might want to use traditional templates. Air provides excellent support for Jinja templates, allowing you to leverage the full power of Jinja while still benefiting from Air's other features.

## Setting Up JinjaRenderer

To use Jinja templates in Air, you first need to set up a `JinjaRenderer`:

```python
import air

app = air.Air()

# Set up Jinja renderer
jinja = air.JinjaRenderer(directory="templates")

@app.page
def index(request: air.Request):
    return jinja(
        request,
        name="home.html",
        title="Welcome to My Site",
        message="Hello from Jinja!"
    )
```

This setup creates a renderer that looks for templates in the `templates` directory. The `JinjaRenderer` automatically handles converting the response to HTML, making it seamless to use in your Air applications.

## Creating Template Directory Structure

Let's create a proper directory structure for our templates:

```
my_air_app/
├── main.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   └── contact.html
```

## Basic Jinja Templates

Let's start with a simple base template:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Air App{% endblock %}</title>
    <link rel="stylesheet" href="https://unpkg.com/mvp.css">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2025 My Air App</p>
    </footer>
</body>
</html>
```

And a child template that extends it:

```html
<!-- templates/home.html -->
{% extends "base.html" %}

{% block title %}{{ title }} - My Air App{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    
    {% if user %}
        <p>Welcome back, {{ user.name }}!</p>
    {% else %}
        <p><a href="/login">Login</a> to access your account.</p>
    {% endif %}
{% endblock %}
```

## Context Passing to Templates

Air makes it easy to pass context data to your Jinja templates. You can pass data in two ways:

### 1. Individual Keyword Arguments

```python
@app.page
def index(request: air.Request):
    user = {"name": "Alice", "email": "alice@example.com"}
    return jinja(
        request,
        name="home.html",
        title="Welcome Home",
        message="This is the home page",
        user=user
    )
```

### 2. Context Dictionary

```python
@app.page
def index(request: air.Request):
    context = {
        "title": "Welcome Home",
        "message": "This is the home page",
        "user": {"name": "Alice", "email": "alice@example.com"},
        "posts": [
            {"title": "First Post", "content": "This is the first post"},
            {"title": "Second Post", "content": "This is the second post"}
        ]
    }
    
    return jinja(
        request,
        name="home.html",
        context=context
    )
```

## Template Inheritance

One of Jinja's most powerful features is template inheritance, which allows you to create a base template and extend it in child templates:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Air App{% endblock %}</title>
    {% block head %}{% endblock %}
</head>
<body>
    <header>
        {% block header %}
            <h1>My Air App</h1>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        {% endblock %}
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        {% block footer %}
            <p>&copy; 2025 My Air App</p>
        {% endblock %}
    </footer>
</body>
</html>
```

```html
<!-- templates/about.html -->
{% extends "base.html" %}

{% block title %}About Us - My Air App{% endblock %}

{% block content %}
    <h1>About Us</h1>
    <p>This is the about page. Learn more about our company.</p>
    
    <h2>Our Team</h2>
    <ul>
        {% for member in team_members %}
            <li>{{ member.name }} - {{ member.role }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```

## Working with Template Filters and Functions

Jinja provides a rich set of built-in filters and functions, and you can also create custom ones:

```python
# Custom filter
def datetime_format(value, format='%Y-%m-%d'):
    return value.strftime(format)

# Custom function
def get_user_avatar(user_id):
    return f"/static/avatars/{user_id}.jpg"

# Configure Jinja with custom filters and functions
jinja = air.JinjaRenderer(
    directory="templates",
    env=jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
)

# Add custom filters and functions
jinja.env.filters['datetime'] = datetime_format
jinja.env.globals['get_avatar'] = get_user_avatar
```

Then use them in your templates:

```html
<!-- Using custom filter -->
<p>Published on {{ post.published_date|datetime('%B %d, %Y') }}</p>

<!-- Using custom function -->
<img src="{{ get_avatar(user.id) }}" alt="{{ user.name }}">
```

## Combining Jinja and Air Tags

One of Air's unique strengths is the ability to seamlessly combine Jinja templates with Air Tags. This allows you to use Jinja for overall page structure while leveraging Air Tags for dynamic content:

```python
@app.get("/profile/{user_id}")
def profile(request: air.Request, user_id: int):
    # Create Air Tags for dynamic content
    user_info = air.Div(
        air.H2(f"User Profile: {user_id}"),
        air.P(f"This is the profile page for user #{user_id}"),
        class_="user-profile"
    )
    
    # Pass Air Tags to Jinja template
    return jinja(
        request,
        name="profile.html",
        title=f"Profile - User {user_id}",
        user_content=user_info  # Air Tags can be passed directly
    )
```

```html
<!-- templates/profile.html -->
{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>
    
    <!-- Render Air Tags using the safe filter -->
    {{ user_content|safe }}
    
    <p>Additional static content can go here.</p>
{% endblock %}
```

## Advanced Template Features

### Template Macros

Jinja macros are like functions in templates:

```
<!-- templates/macros.html -->
{% macro render_form_field(field_name, field_label, field_type="text", required=false) %}
    <div class="form-group">
        <label for="{{ field_name }}">{{ field_label }}{% if required %} *{% endif %}</label>
        <input type="{{ field_type }}" id="{{ field_name }}" name="{{ field_name }}" 
               {% if required %}required{% endif %}>
    </div>
{% endmacro %}

{% macro render_button(button_text, button_type="submit", button_class="btn") %}
    <button type="{{ button_type }}" class="{{ button_class }}">{{ button_text }}</button>
{% endmacro %}
```

```html
<!-- templates/contact.html -->
{% extends "base.html" %}
{% from "macros.html" import render_form_field, render_button %}

{% block title %}Contact Us - My Air App{% endblock %}

{% block content %}
    <h1>Contact Us</h1>
    
    <form method="POST" action="/contact">
        {{ render_form_field("name", "Name", "text", true) }}
        {{ render_form_field("email", "Email", "email", true) }}
        {{ render_form_field("subject", "Subject", "text", true) }}
        
        <div class="form-group">
            <label for="message">Message *</label>
            <textarea id="message" name="message" rows="5" required></textarea>
        </div>
        
        {{ render_button("Send Message") }}
    </form>
{% endblock %}
```

### Template Includes

You can include other templates within your templates:

```
<!-- templates/sidebar.html -->
<aside class="sidebar">
    <h3>Recent Posts</h3>
    <ul>
        {% for post in recent_posts %}
            <li><a href="/posts/{{ post.id }}">{{ post.title }}</a></li>
        {% endfor %}
    </ul>
</aside>
```

```
<!-- templates/blog.html -->
{% extends "base.html" %}

{% block content %}
    <div class="content-wrapper">
        <main class="main-content">
            {% block main_content %}{% endblock %}
        </main>
        
        {% include "sidebar.html" %}
    </div>
{% endblock %}
```

## Practical Example: Blog Application with Templates

Let's create a more comprehensive example that demonstrates templates in action:

```
import air
from datetime import datetime
from typing import Optional

app = air.Air()
jinja = air.JinjaRenderer(directory="templates")

# Sample data (in a real app, this would come from a database)
posts = [
    {
        "id": 1,
        "title": "Getting Started with Air",
        "content": "Air is a modern Python web framework...",
        "author": "Alice",
        "published_date": datetime(2025, 10, 1),
        "tags": ["python", "web-framework"]
    },
    {
        "id": 2,
        "title": "Mastering Air Tags",
        "content": "Air Tags provide a powerful way to generate HTML...",
        "author": "Bob",
        "published_date": datetime(2025, 10, 15),
        "tags": ["html", "python"]
    }
]

@app.page
def index(request: air.Request):
    return jinja(
        request,
        name="index.html",
        title="Home",
        posts=posts
    )

@app.get("/posts/{post_id}")
def post_detail(request: air.Request, post_id: int):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return jinja(
            request,
            name="404.html",
            title="Post Not Found"
        )
    
    return jinja(
        request,
        name="post.html",
        title=post["title"],
        post=post
    )

@app.page
def about(request: air.Request):
    team_members = [
        {"name": "Alice Johnson", "role": "Lead Developer"},
        {"name": "Bob Smith", "role": "UI/UX Designer"},
        {"name": "Carol Williams", "role": "Content Writer"}
    ]
    
    return jinja(
        request,
        name="about.html",
        title="About Us",
        team_members=team_members
    )

# API endpoint for dynamic content
@app.get("/api/latest-posts")
def latest_posts():
    # Return the 3 most recent posts
    sorted_posts = sorted(posts, key=lambda x: x["published_date"], reverse=True)
    return sorted_posts[:3]
```

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block title %}{{ title }} - My Blog{% endblock %}

{% block content %}
    <h1>Latest Posts</h1>
    
    {% for post in posts %}
        <article class="post-preview">
            <h2><a href="/posts/{{ post.id }}">{{ post.title }}</a></h2>
            <p class="post-meta">
                By {{ post.author }} on {{ post.published_date.strftime('%B %d, %Y') }}
            </p>
            <p>{{ post.content[:200] }}...</p>
            <div class="post-tags">
                {% for tag in post.tags %}
                    <span class="tag">{{ tag }}</span>
                {% endfor %}
            </div>
        </article>
    {% else %}
        <p>No posts available.</p>
    {% endfor %}
{% endblock %}
```

```html
<!-- templates/post.html -->
{% extends "base.html" %}

{% block title %}{{ title }} - My Blog{% endblock %}

{% block content %}
    <article class="post">
        <h1>{{ post.title }}</h1>
        <p class="post-meta">
            By {{ post.author }} on {{ post.published_date.strftime('%B %d, %Y') }}
        </p>
        <div class="post-content">
            {{ post.content }}
        </div>
        <div class="post-tags">
            {% for tag in post.tags %}
                <span class="tag">{{ tag }}</span>
            {% endfor %}
        </div>
    </article>
    
    <nav class="post-navigation">
        <a href="/">&larr; Back to Home</a>
    </nav>
{% endblock %}
```

```html
<!-- templates/about.html -->
{% extends "base.html" %}

{% block title %}{{ title }} - My Blog{% endblock %}

{% block content %}
    <h1>About Our Blog</h1>
    <p>Welcome to our blog where we share insights about Python web development and the Air framework.</p>
    
    <h2>Our Team</h2>
    <div class="team-members">
        {% for member in team_members %}
            <div class="team-member">
                <h3>{{ member.name }}</h3>
                <p>{{ member.role }}</p>
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

## Template Best Practices

### 1. Organize Templates Logically

```
templates/
├── base.html
├── partials/
│   ├── header.html
│   ├── footer.html
│   └── sidebar.html
├── pages/
│   ├── home.html
│   ├── about.html
│   └── contact.html
├── components/
│   ├── form_macros.html
│   └── navigation.html
└── emails/
    ├── welcome.html
    └── notification.html
```

### 2. Use Template Inheritance Consistently

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My App{% endblock %}</title>
    {% block extra_head %}{% endblock %}
</head>
<body>
    {% block body %}{% endblock %}
</body>
</html>
```

### 3. Handle Errors Gracefully

```html
<!-- templates/404.html -->
{% extends "base.html" %}

{% block title %}Page Not Found{% endblock %}

{% block body %}
    <h1>Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="/">Return to Home</a>
{% endblock %}
```

### 4. Use Custom Filters for Common Operations

```
# Custom filters
def truncate_text(text, length=100):
    if len(text) <= length:
        return text
    return text[:length] + "..."

def format_currency(amount):
    return f"${amount:,.2f}"

# Add to Jinja environment
jinja.env.filters['truncate'] = truncate_text
jinja.env.filters['currency'] = format_currency
```

## Security Considerations

### 1. Autoescaping

Jinja automatically escapes HTML by default, which helps prevent XSS attacks:

```
# This is automatically escaped
user_input = "<script>alert('XSS')</script>"
# In template: {{ user_input }} renders as text, not HTML
```

### 2. Safe Filter Usage

When using the `|safe` filter with Air Tags, be careful about what content you're marking as safe:

```
# Good - Using safe filter with trusted Air Tags
content = air.Div(air.H1("Safe Content"))
return jinja(request, name="template.html", content=content)

# In template:
# {{ content|safe }}  # Safe because we control the Air Tags
```

### 3. Input Validation

Always validate and sanitize user input before passing it to templates:

```python
from pydantic import BaseModel, Field

class CommentModel(BaseModel):
    author: str = Field(max_length=50)
    content: str = Field(max_length=1000)

@app.post("/comments")
async def add_comment(request: air.Request):
    form_data = await request.form()
    try:
        comment = CommentModel(**dict(form_data))
        # Process validated comment
        # ...
    except Exception as e:
        # Handle validation errors
        pass
```

## Performance Considerations

### 1. Template Caching

Jinja automatically caches compiled templates, but you can configure caching behavior:

```
jinja = air.JinjaRenderer(
    directory="templates",
    env=jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
        cache_size=400  # Increase cache size for high-traffic sites
    )
)
```

### 2. Minimize Context Data

Only pass necessary data to templates:

```
# Good - Pass only what's needed
@app.page
def user_profile(request: air.Request, user_id: int):
    user = get_user_basic_info(user_id)  # Only basic info needed for template
    return jinja(request, name="profile.html", user=user)

# Avoid - Passing entire user objects with sensitive data
@app.page
def user_profile(request: air.Request, user_id: int):
    user = get_full_user_object(user_id)  # May include sensitive data
    return jinja(request, name="profile.html", user=user)
```

## What's Coming Next

In our next post, we'll explore styling with Tailwind CSS, covering:

1. Introduction to Tailwind CSS and its utility-first approach
2. Integrating Tailwind CSS with Air applications
3. Using Tailwind classes with Air Tags
4. Advanced Tailwind techniques and customization
5. Building responsive UI components

## Conclusion

Templates and Jinja integration are powerful features of the Air framework that provide flexibility in how you structure and render your web applications. By combining the traditional power of Jinja templates with Air's modern features like Air Tags, you can create sophisticated web applications with clean separation of concerns.

Key takeaways from this post:

1. Air provides seamless integration with Jinja templates through `JinjaRenderer`
2. Template inheritance allows for consistent page layouts
3. You can combine Jinja templates with Air Tags for maximum flexibility
4. Custom filters and functions extend Jinja's capabilities
5. Proper organization and security practices are essential for maintainable templates

With templates and Jinja integration mastered, you're well-equipped to build professional web applications with Air. The combination of Jinja's powerful templating features and Air's Python-based approach to web development makes for a robust and flexible development experience.

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for weekly updates. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

See you in the next post where we'll dive into styling with Tailwind CSS!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [Forms and Validation](04-forms-and-validation.md)*

## Quiz: Test Your Knowledge

1. What class does Air provide for integrating Jinja templates?
   a) JinjaTemplate
   b) JinjaRenderer
   c) TemplateEngine
   d) JinjaHandler

2. How do you pass context data to a Jinja template in Air?
   a) Through URL parameters
   b) As keyword arguments to the renderer
   c) Through global variables
   d) By embedding in HTML

3. What is the correct way to extend a base template in Jinja?
   a) {% include "base.html" %}
   b) {% extend "base.html" %}
   c) {% extends "base.html" %}
   d) {% import "base.html" %}

4. True or False: Jinja automatically escapes HTML by default to help prevent XSS attacks.

5. True or False: You cannot combine Air Tags with Jinja templates in the same application.

6. Explain how Air's JinjaRenderer handles Air Tags when they are passed as context data to templates.

### Answers:
1. b) JinjaRenderer
2. b) As keyword arguments to the renderer
3. c) {% extends "base.html" %}
4. True
5. False - Air Tags can be seamlessly integrated with Jinja templates
6. Air's JinjaRenderer automatically converts Air Tags to their HTML string representation when they are passed as context data to templates. This allows developers to create dynamic HTML content using Air Tags and then pass that content to Jinja templates for rendering.
