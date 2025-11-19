# PremiumShop E-commerce Application

A professional, modular e-commerce website built with the Air framework and Tailwind CSS.

## Project Structure

```
.
├── main.py                 # Application entry point
├── templates/
│   ├── base.html           # Base template with Tailwind CSS
│   ├── home/
│   │   └── home_page.html  # Homepage template
│   ├── partials/
│   │   ├── navigation.html # Navigation component
│   │   └── footer.html     # Footer component
│   ├── blocks/
│   │   └── homepage_blocks/
│   │       ├── hero.html              # Hero section
│   │       ├── featured_categories.html # Categories section
│   │       ├── featured_products.html  # Products section
│   │       └── newsletter.html         # Newsletter section
│   ├── products/
│   │   ├── products_page.html    # Products listing
│   │   └── product_detail.html   # Product detail page
│   ├── categories/
│   │   └── categories_page.html  # Categories listing
│   ├── about/
│   │   └── about_page.html       # About page
│   ├── contact/
│   │   └── contact_page.html     # Contact page
│   ├── cart/
│   │   └── cart_page.html        # Shopping cart
│   └── checkout/
│       └── checkout_page.html    # Checkout page
├── static/
│   └── css/
│       ├── style.css      # Tailwind-like CSS classes
│       └── custom.css     # Custom styles
└── README.md              # This file
```

## Features

- **Modular Component Architecture**: Reusable UI components organized in a logical structure
- **Dark Mode Support**: Toggle between light and dark themes with persistent preferences
- **Responsive Design**: Mobile-first approach with responsive breakpoints
- **Professional UI**: Clean, modern, and elegant design suitable for enterprise applications
- **Component Reusability**: React-like component structure with template inheritance
- **Tailwind CSS Integration**: Utility-first styling approach for rapid development

## Key Components

### Layout Components
- **Base Template**: Core HTML structure with Tailwind CSS integration
- **Navigation**: Responsive header with mobile menu and dark mode toggle
- **Footer**: Comprehensive footer with links and payment options

### Homepage Blocks
- **Hero Section**: Eye-catching hero with call-to-action buttons
- **Featured Categories**: Category showcase with icons
- **Featured Products**: Product grid with pricing and ratings
- **Newsletter**: Email subscription section

### Product Components
- **Product Listing**: Grid layout with filtering and pagination
- **Product Detail**: Comprehensive product view with image gallery
- **Shopping Cart**: Cart management with quantity controls
- **Checkout**: Multi-step checkout process

## Getting Started

1. Install dependencies:
   ```bash
   pip install air-framework uvicorn
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Visit `http://localhost:8000` in your browser

## Design Principles

- **Minimalist Aesthetic**: Clean design with ample whitespace
- **Premium Feel**: High-quality visual elements and interactions
- **Dark Mode Ready**: Seamless theme switching with localStorage persistence
- **Mobile Optimized**: Fully responsive design for all device sizes
- **Accessible**: Semantic HTML and proper ARIA attributes
- **Performant**: Optimized assets and minimal JavaScript

## Technologies Used

- **Air Framework**: Python web framework built on FastAPI
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library
- **HTMX**: Dynamic interactions without complex JavaScript
- **LocalStorage**: Client-side theme persistence

This application demonstrates a professional-grade e-commerce implementation with a focus on modularity, reusability, and premium design quality.