import air

app = air.Air()


@app.page
def index():
    title = "My Blog"  # TODO: Change this to your own blog title!
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Welcome to my awesome Air-powered blog."),
    )
