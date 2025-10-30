from pathlib import Path
from frontmatter import Frontmatter
import air


def get_articles() -> list[dict]:
    """Read all markdown files in the articles directory and return their content."""
    articles = []
    # Read all markdown files in the articles directory
    for path in Path("articles").glob("*.md"):
        # Parse the frontmatter and content of each file
        # then add it to the articles list
        articles.append(Frontmatter.read_file(path))
    # Sort articles by date in descending date order
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


app = air.Air()

@app.page
def index():
    title = "My First Air Framework Blog"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Welcome to my first Air framework blog!"),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                    ),
                    air.Br(),
                    air.Small(article["attributes"]["description"]),
                    air.Br(),
                    air.Time(
                        f'Published: {article["attributes"]["date"]}', 
                        datetime=str(article["attributes"]["date"])
                    )
                )
                for article in articles
            ]
        )
    )