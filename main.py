#!/usr/bin/env python3

import air

app = air.Air()

# Serve static files
app.mount("/static", air.StaticFiles(directory="static"), name="static")

# Route handlers
@app.get("/")
def root(request: air.Request):
    """Redirect root path to home page"""
    return air.RedirectResponse(url="/home")

@app.page
def home(request: air.Request):
    """Main homepage route that renders the homepage template"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="home/home_page.html",
        title="PremiumShop - Elevate Your Style"
    )

@app.page
def about(request: air.Request):
    """About page route"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="about/about_page.html",
        title="About Us - PremiumShop"
    )

@app.page
def contact(request: air.Request):
    """Contact page route"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="contact/contact_page.html",
        title="Contact Us - PremiumShop"
    )

@app.page
def products(request: air.Request):
    """Products page route"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="products/products_page.html",
        title="Our Products - PremiumShop"
    )

@app.page
def categories(request: air.Request):
    """Categories page route"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="categories/categories_page.html",
        title="Product Categories - PremiumShop"
    )

@app.page
def cart(request: air.Request):
    """Shopping cart page route"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="cart/cart_page.html",
        title="Your Cart - PremiumShop"
    )

@app.page
def checkout(request: air.Request):
    """Checkout page route"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="checkout/checkout_page.html",
        title="Checkout - PremiumShop"
    )

@app.page
def product_detail(request: air.Request, id: str):
    """Product detail page route"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="products/product_detail.html",
        title=f"Product Details - PremiumShop",
        product_id=id
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)