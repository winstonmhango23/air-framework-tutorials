import air
import uvicorn


# Air Tags Implementation
def create_blog_post(title, author, date, content):
    return air.Article(
        air.Header(
            air.H1(title, class_="post-title"),
            air.Div(
                air.Span(f"By {author}", class_="post-author"),
                air.Time(date, class_="post-date")
            ),
            class_="post-header"
        ),
        air.Div(
            air.P(content),
            class_="post-content"
        ),
        class_="blog-post"
    )


def create_page_with_air_tags():
    return air.Html(
        air.Head(
            air.Title("My Blog"),
            air.Meta(charset="utf-8"),
            air.Link(rel="stylesheet", href="/static/css/style.css")
        ),
        air.Body(
            air.Header(
                air.H1("My Personal Blog"),
                air.Nav(
                    air.Ul(
                        air.Li(air.A("Home", href="/")),
                        air.Li(air.A("About", href="/about")),
                        air.Li(air.A("Archive", href="/archive"))
                    )
                )
            ),
            air.Main(
                create_blog_post(
                    "Understanding Air Tags",
                    "Winston Mhango",
                    "2025-10-24",
                    "Today we're exploring the powerful Air Tags system..."
                ),
                create_blog_post(
                    "Building REST APIs with Air",
                    "Winston Mhango",
                    "2025-10-17",
                    "Learn how to build modern REST APIs using Air framework..."
                )
            ),
            air.Footer(
                air.P("© 2025 My Blog. All rights reserved.")
            )
        )
    )


# Jinja2 Implementation
# Initialize the Jinja renderer
jinja = air.JinjaRenderer(directory="templates")


def create_page_with_jinja2(request: air.Request):
    # Data to pass to the template
    blog_posts = [
        {
            "title": "Understanding Air Tags",
            "author": "Winston Mhango",
            "date": "2025-10-24",
            "content": "Today we're exploring the powerful Air Tags system..."
        },
        {
            "title": "Building REST APIs with Air",
            "author": "Winston Mhango",
            "date": "2025-10-17",
            "content": "Learn how to build modern REST APIs using Air framework..."
        }
    ]
    
    # Render the template with the data
    return jinja(
        request,
        name="blog.html",
        context={"blog_posts": blog_posts}
    )


# Initialize Air app
app = air.Air()


# Routes
@app.get("/")
def index():
    return air.Html(
        air.Head(air.Title("Air Framework Blog Example")),
        air.Body(
            air.H1("Air Framework Blog Example"),
            air.P("Welcome to the Air Framework blog example!"),
            air.Ul(
                air.Li(air.A("Air Tags Implementation", href="/blog/air-tags")),
                air.Li(air.A("Jinja2 Implementation", href="/blog/jinja2"))
            )
        )
    )


@app.get("/blog/air-tags")
def blog_with_air_tags():
    return create_page_with_air_tags()


@app.get("/blog/jinja2")
def blog_with_jinja2(request: air.Request):
    return create_page_with_jinja2(request)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)