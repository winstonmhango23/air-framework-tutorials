import air
import uvicorn

# Create Air app instance
app = air.Air()

# Mount static files directory for serving CSS, JS, and images
app.mount("/static", air.StaticFiles(directory="static"), name="static")

# Homepage route
@app.page
def home(request: air.Request):
    """Main homepage route that renders the homepage template"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="home/home_page.html",
        title="PremiumShop - Elevate Your Style"
    )

# Explicit route for root path
@app.get("/")
def root():
    """Redirect root path to home page"""
    return air.RedirectResponse(url="/home")

# Products page
@app.page
def products(request: air.Request):
    """Products listing page"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="products/products_page.html",
        title="Products - PremiumShop"
    )

# Product detail page
@app.page
def product_detail(request: air.Request, product_id: int):
    """Product detail page"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="products/product_detail.html",
        title=f"Product {product_id} - PremiumShop"
    )

# Categories page
@app.page
def categories(request: air.Request):
    """Categories listing page"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="categories/categories_page.html",
        title="Categories - PremiumShop"
    )

# Category detail page
@app.page
def category_detail(request: air.Request, category_id: int):
    """Category detail page"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="base.html",
        title=f"Category {category_id} - PremiumShop"
    )

# About page
@app.page
def about(request: air.Request):
    """About us page"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="about/about_page.html",
        title="About Us - PremiumShop"
    )

# Contact page
@app.page
def contact(request: air.Request):
    """Contact page"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="contact/contact_page.html",
        title="Contact - PremiumShop"
    )

# Cart page
@app.page
def cart(request: air.Request):
    """Shopping cart page"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="cart/cart_page.html",
        title="Shopping Cart - PremiumShop"
    )

# Checkout page
@app.page
def checkout(request: air.Request):
    """Checkout page"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="checkout/checkout_page.html",
        title="Checkout - PremiumShop"
    )

if __name__ == "__main__":
    print("Starting PremiumShop E-commerce Application...")
    print("Open http://localhost:8003 in your browser")
    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)