# Complete Guide to Setting Up Tailwind CSS with the Air Framework

This guide provides a comprehensive walkthrough of setting up Tailwind CSS with the Air web framework, following the best practices and configuration used in this project.

## Table of Contents
- [Complete Guide to Setting Up Tailwind CSS with the Air Framework](#complete-guide-to-setting-up-tailwind-css-with-the-air-framework)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Prerequisites](#prerequisites)
  - [Directory Structure](#directory-structure)
  - [Installation](#installation)
  - [Configuration Files](#configuration-files)
    - [tailwind.config.js](#tailwindconfigjs)
    - [package.json](#packagejson)
    - [input.css](#inputcss)
  - [CSS Variable Theme System](#css-variable-theme-system)
  - [Building CSS](#building-css)
  - [Integrating with Air Framework](#integrating-with-air-framework)
  - [Using Tailwind Classes in Templates](#using-tailwind-classes-in-templates)
  - [Dark Mode Support](#dark-mode-support)
  - [Best Practices](#best-practices)
    - [1. Optimize CSS Output](#1-optimize-css-output)
    - [2. Use Semantic Class Names](#2-use-semantic-class-names)
    - [3. Leverage CSS Variables](#3-leverage-css-variables)
    - [4. Component Extraction](#4-component-extraction)
    - [5. Responsive Design](#5-responsive-design)
    - [6. Performance Considerations](#6-performance-considerations)
    - [7. Maintainability](#7-maintainability)
  - [Conclusion](#conclusion)

## Project Overview

This project demonstrates a professional setup of Tailwind CSS with the Air framework, featuring:
- A custom CSS variable-based theme system for consistent design
- Dark mode support with automatic OS preference detection
- Responsive design utilities
- Optimized CSS output with PurgeCSS
- Integration with Jinja2 templates

## Prerequisites

Before setting up Tailwind CSS with Air, ensure you have:
- Node.js (version 12 or higher)
- npm or yarn package manager
- Python 3.7+ with the Air framework installed

## Directory Structure

The recommended directory structure for an Air project with Tailwind CSS:

```
my-air-app/
├── main.py                 # Air application entry point
├── package.json            # Node.js dependencies and scripts
├── tailwind.config.js      # Tailwind CSS configuration
├── static/                 # Static assets directory
│   ├── css/
│   │   ├── input.css       # Tailwind directives and custom CSS
│   │   └── output.css      # Generated CSS (do not edit)
│   ├── js/
│   └── images/
├── templates/              # Jinja2 templates
│   ├── base.html
│   └── ...                 # Other template files
└── components/             # Optional: Reusable components
```

## Installation

1. Initialize your project with npm:
   ```bash
   npm init -y
   ```

2. Install Tailwind CSS and its dependencies:
   ```bash
   npm install -D tailwindcss
   ```

3. Initialize Tailwind CSS:
   ```bash
   npx tailwindcss init
   ```

## Configuration Files

### tailwind.config.js

The Tailwind configuration file defines content sources, theme extensions, and plugins:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}", 
    "./static/**/*.{html,js}",
    "./*.py",
    "./templates/**/*.py"
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        card: 'var(--card)',
        'card-foreground': 'var(--card-foreground)',
        popover: 'var(--popover)',
        'popover-foreground': 'var(--popover-foreground)',
        primary: 'var(--primary)',
        'primary-foreground': 'var(--primary-foreground)',
        secondary: 'var(--secondary)',
        'secondary-foreground': 'var(--secondary-foreground)',
        muted: 'var(--muted)',
        'muted-foreground': 'var(--muted-foreground)',
        accent: 'var(--accent)',
        'accent-foreground': 'var(--accent-foreground)',
        destructive: 'var(--destructive)',
        'destructive-foreground': 'var(--destructive-foreground)',
        border: 'var(--border)',
        input: 'var(--input)',
        ring: 'var(--ring)',
        'chart-1': 'var(--chart-1)',
        'chart-2': 'var(--chart-2)',
        'chart-3': 'var(--chart-3)',
        'chart-4': 'var(--chart-4)',
        'chart-5': 'var(--chart-5)',
        sidebar: 'var(--sidebar)',
        'sidebar-foreground': 'var(--sidebar-foreground)',
        'sidebar-primary': 'var(--sidebar-primary)',
        'sidebar-primary-foreground': 'var(--sidebar-primary-foreground)',
        'sidebar-accent': 'var(--sidebar-accent)',
        'sidebar-accent-foreground': 'var(--sidebar-accent-foreground)',
        'sidebar-border': 'var(--sidebar-border)',
        'sidebar-ring': 'var(--sidebar-ring)',
      },
      borderRadius: {
        DEFAULT: 'var(--radius)',
      }
    },
  },
  plugins: [
    function({ addUtilities }) {
      const newUtilities = {
        '.bg-background': {
          'background-color': 'var(--background)',
        },
        '.text-foreground': {
          'color': 'var(--foreground)',
        },
        // ... additional utility classes for all CSS variables
      }
      addUtilities(newUtilities, ['responsive', 'hover'])
    }
  ],
  darkMode: 'class'
}
```

### package.json

Define build scripts for Tailwind CSS:

```json
{
  "name": "helloair",
  "version": "1.0.0",
  "description": "A professional, modular e-commerce website built with the Air framework and Tailwind CSS.",
  "scripts": {
    "build": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css",
    "watch": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.18"
  }
}
```

### input.css

Create `static/css/input.css` with Tailwind directives and custom utilities:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom color utilities for our theme */
.bg-background {
  background-color: var(--background);
}

.text-foreground {
  color: var(--foreground);
}

/* ... additional custom utilities for all CSS variables */
```

## CSS Variable Theme System

The project uses CSS variables for theming, defined in `static/css/style.css`:

```css
:root {
  /* Minimalist light theme */
  --background: #fafafa;
  --foreground: #262626;
  --card: #ffffff;
  --card-foreground: #262626;
  --primary: #404040;
  /* ... other variables */
}

.dark {
  --background: #1f1f1f;
  --foreground: #f2f2f2;
  --card: #262626;
  --card-foreground: #f2f2f2;
  --primary: #f2f2f2;
  /* ... other variables */
}
```

This approach provides:
- Consistent color usage across the application
- Easy theme customization
- Seamless dark mode support
- Design system adherence

## Building CSS

Use the npm scripts defined in package.json to build your CSS:

1. One-time build:
   ```bash
   npm run build
   ```

2. Watch mode for development:
   ```bash
   npm run watch
   ```

The build process will:
- Process all Tailwind directives
- Generate utility classes based on actual usage in your templates
- Purge unused CSS for optimal file size
- Output the final CSS to `static/css/output.css`

## Integrating with Air Framework

In your `main.py`, mount the static files directory and reference the compiled CSS:

```python
import air

app = air.Air()

# Serve static files
app.mount("/static", air.StaticFiles(directory="static"), name="static")

@app.page
def home(request: air.Request):
    """Main homepage route that renders the homepage template"""
    return air.JinjaRenderer(directory="templates")(
        request,
        name="home/home_page.html",
        title="PremiumShop - Elevate Your Style"
    )
```

In your base template (`templates/base.html`):

```html
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}PremiumShop - Elevate Your Style{% endblock %}</title>
    
    <!-- Tailwind CSS -->
    <link href="/static/css/style.css" rel="stylesheet">
    <link href="/static/css/output.css" rel="stylesheet">
    
    {% block extra_head %}{% endblock %}
</head>
<body class="bg-background text-foreground font-sans antialiased transition-colors duration-300">
    {% block content %}{% endblock %}
</body>
</html>
```

## Using Tailwind Classes in Templates

Apply Tailwind classes directly in your HTML templates:

```html
<div class="max-w-7xl mx-auto px-4 py-12">
  <h1 class="text-3xl font-bold text-foreground mb-6">Welcome to Our Store</h1>
  <p class="text-lg text-muted-foreground mb-8">Discover our premium collection</p>
  
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="bg-card rounded-lg p-6 shadow-md">
      <h2 class="text-xl font-semibold text-card-foreground mb-3">Product 1</h2>
      <p class="text-muted-foreground">Description of product 1</p>
    </div>
    <!-- More product cards -->
  </div>
</div>
```

When using Air Tags in Python:

```python
import air

@app.page
def dashboard():
    return air.layouts.mvpcss(
        air.Div(
            air.H1("Dashboard", class_="text-3xl font-bold text-foreground mb-6"),
            air.Div(
                air.P("Statistics", class_="text-lg text-muted-foreground"),
                class_="bg-card rounded-lg p-6"
            ),
            class_="max-w-7xl mx-auto px-4 py-12"
        )
    )
```

Note: Use `class_` (with underscore) in Python instead of `class` due to Python keyword restrictions.

## Dark Mode Support

The project includes comprehensive dark mode support:

1. CSS variables for both light and dark themes
2. JavaScript for theme switching and persistence:

```html
<script>
    // Check for saved theme preference or respect OS preference
    if (localStorage.getItem('theme') === 'dark' || 
        (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    
    // Function to toggle dark mode
    function toggleDarkMode() {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        }
    }
</script>
```

3. Tailwind configuration with `darkMode: 'class'`
4. Utility classes that respect the dark mode context

## Best Practices

### 1. Optimize CSS Output
Ensure your `tailwind.config.js` content property correctly specifies all source files to enable proper purging of unused CSS:

```javascript
content: [
  "./templates/**/*.{html,js}", 
  "./static/**/*.{html,js}",
  "./*.py",
  "./templates/**/*.py"
]
```

### 2. Use Semantic Class Names
While Tailwind encourages utility-first CSS, maintain semantic meaning in your HTML structure:

```html
<!-- Good -->
<article class="product-card bg-card rounded-lg shadow-md">
  <h2 class="product-title text-xl font-semibold text-card-foreground">Product Name</h2>
</article>

<!-- Avoid -->
<div class="bg-white rounded-lg shadow-md">
  <h2 class="text-xl font-semibold text-gray-900">Product Name</h2>
</div>
```

### 3. Leverage CSS Variables
Use CSS variables for consistent theming:

```css
/* Define in style.css */
:root {
  --primary: #404040;
}

.dark {
  --primary: #f2f2f2;
}

/* Use in Tailwind config */
primary: 'var(--primary)',
```

### 4. Component Extraction
For repeated patterns, extract components using `@apply` in your CSS:

```css
@layer components {
  .btn-primary {
    @apply bg-primary text-primary-foreground font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity;
  }
  
  .card {
    @apply bg-card rounded-lg shadow-md overflow-hidden;
  }
}
```

### 5. Responsive Design
Use Tailwind's responsive prefixes consistently:

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  <!-- Content that adapts to screen size -->
</div>
```

### 6. Performance Considerations
- Always use the build process to purge unused CSS
- Minimize custom CSS in favor of Tailwind utilities
- Use `transition-colors` for smooth theme switching
- Leverage browser caching for static assets

### 7. Maintainability
- Keep your `tailwind.config.js` organized
- Document custom color names and their purposes
- Use consistent naming conventions for custom utilities
- Regularly update dependencies

## Conclusion

This setup provides a robust foundation for building modern web applications with the Air framework and Tailwind CSS. The combination offers:

- Rapid development with utility-first CSS
- Consistent design through a CSS variable-based theme system
- Dark mode support with user preference persistence
- Optimized production builds
- Seamless integration with Air's Python-based templating

By following this guide, you'll have a professional, maintainable setup that scales well for both small projects and large applications.