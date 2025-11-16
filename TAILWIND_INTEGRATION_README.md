# Tailwind CSS Integration with Air Framework

This repository contains comprehensive resources for integrating Tailwind CSS with the Air web framework. It includes guides, examples, and setup scripts to help you get started quickly.

## Contents

1. **[air-tailwindcss-integration-guide.md](series-tutorials/air-tailwindcss-integration-guide.md)** - A comprehensive guide explaining different approaches to integrate Tailwind CSS with Air
2. **[air_tailwind_demo.py](examples/air_tailwind_demo.py)** - A practical example demonstrating Tailwind CSS integration with Air
3. **[setup_tailwind.py](setup_tailwind.py)** - A setup script to create the necessary files and directories
4. **This README** - Instructions on how to use these resources

## Getting Started

### Option 1: Quick Setup with Setup Script

Run the setup script to automatically create the directory structure and configuration files:

```bash
python setup_tailwind.py
```

This script will:
- Create the recommended directory structure
- Generate configuration files (`tailwind.config.js`, `postcss.config.js`, etc.)
- Install necessary npm dependencies
- Create example files

### Option 2: Manual Setup

1. Create the directory structure:
   ```
   my-air-app/
   ├── static/
   │   ├── css/
   │   │   ├── input.css
   │   │   └── output.css (generated)
   │   ├── js/
   │   └── images/
   ├── templates/
   └── main.py
   ```

2. Install Tailwind CSS:
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. Configure `tailwind.config.js`:
   ```javascript
   /** @type {import('tailwindcss').Config} */
   module.exports = {
     content: [
       "./templates/**/*.{html,js}",
       "./static/**/*.{html,js}",
       "./*.py"
     ],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```

4. Create `static/css/input.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

5. Build the CSS:
   ```bash
   npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
   ```

## Using Tailwind CSS with Air

### In Your Air Application

```python
import air

app = air.Air()
app.mount("/static", air.StaticFiles(directory="static"), name="static")

@app.page
def index():
    return air.Html(
        air.Head(
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            air.Title("Air with Tailwind CSS"),
            air.Link(rel="stylesheet", href="/static/css/output.css"),
        ),
        air.Body(
            air.Div(
                air.H1("Hello, Tailwind!", class_="text-3xl font-bold text-blue-600"),
                air.P("This is a paragraph styled with Tailwind CSS.", 
                      class_="mt-4 text-gray-700"),
                class_="container mx-auto p-4"
            )
        )
    )
```

## Examples

### Run the Demo Application

```bash
python examples/air_tailwind_demo.py
```

Visit `http://localhost:8000` to see the demo in action.

## Integration Approaches

### 1. CDN Approach (Development Only)
```python
air.Script(src="https://cdn.tailwindcss.com")
```

### 2. Static Files Approach (Production)
```python
air.Link(rel="stylesheet", href="/static/css/output.css")
```

### 3. Advanced Features
- Dark mode support
- Responsive design
- Custom components with `@apply`
- JIT mode for faster builds

## Best Practices

1. **Use meaningful class names** that describe visual appearance
2. **Extract repeated patterns** into utility functions
3. **Leverage Tailwind's configuration** for custom colors and spacing
4. **Use responsive prefixes consistently**
5. **Purge unused CSS** for production builds

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Air Framework Documentation](https://feldroy.github.io/air/)
- [Tailwind CSS Cheat Sheet](https://nerdcave.com/tailwind-cheat-sheet)

## License

This project is open source and available under the MIT License.