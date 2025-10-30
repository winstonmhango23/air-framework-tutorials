from pathlib import Path
from frontmatter import Frontmatter
import markdown
from datetime import datetime
from typing import List
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


app = air.Air()
api = fastapi.FastAPI()

@app.page
def index():
    title = "My Personal Blog"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Header(
            air.Nav(
                air.A("My Personal Blog", href="/", style="font-size: 1.5em; font-weight: bold;"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Contact", href="/contact"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("API", href="/api/docs", target="_blank")
            )
        ),
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Welcome to my personal blog!"),
        air.H2("Latest Articles"),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                        style="font-size: 1.2em; font-weight: bold;"
                    ),
                    air.Br(),
                    air.Small(article["attributes"]["description"]),
                    air.Br(),
                    air.Time(
                        f'Published: {article["attributes"]["date"]}', 
                        datetime=str(article["attributes"]["date"]),
                        style="color: #666;"
                    )
                )
                for article in articles
            ]
        )
    )


@app.get("/{slug}")
def article_detail(slug: str):
    """Display a single article."""
    article = get_article(slug)
    if not article:
        return air.layouts.mvpcss(
            air.H1("Article not found"),
            air.P("The requested article could not be found.")
        )

    # Convert markdown content to HTML
    html_content = markdown.markdown(article["body"])

    return air.layouts.mvpcss(
        air.Title(article["attributes"]["title"]),
        air.Article(
            air.H1(article["attributes"]["title"]),
            air.Time(
                f'Published: {article["attributes"]["date"]}',
                datetime=str(article["attributes"]["date"])
            ),
            air.P(f"By {article['attributes']['author']}"),
            air.Div(air.Raw(html_content))
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.page
def contact():
    """Contact form page."""
    return air.layouts.mvpcss(
        air.Title("Contact Us"),
        air.H1("Contact Us"),
        air.Form(
            air.Div(
                air.Label("Name", for_="name"),
                air.Input(type="text", name="name", required=True),
            ),
            air.Div(
                air.Label("Email", for_="email"),
                air.Input(type="email", name="email", required=True),
            ),
            air.Div(
                air.Label("Message", for_="message"),
                air.Textarea(name="message", required=True, rows="5"),
            ),
            air.Button("Submit", type="submit"),
            method="POST",
            action="/contact",
            style="display: flex; flex-direction: column; gap: 1rem;"
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/contact")
async def contact_handler(request: air.Request):
    """Handle form submission."""
    form_data = await request.form()

    name = form_data.get("name")
    email = form_data.get("email")
    message = form_data.get("message")

    return air.layouts.mvpcss(
        air.H1("Thank You!"),
        air.P(f"We have received your message, {name}!"),
        air.P("We'll get back to you soon."),
        air.Nav(
            air.A("← Back to Home", href="/"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("Send Another Message", href="/contact")
        )
    )

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