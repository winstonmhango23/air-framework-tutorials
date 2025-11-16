"""
Setup script for Tailwind CSS integration with Air framework

This script helps set up the necessary files and directories for integrating 
Tailwind CSS with the Air framework using the static files approach.
"""

import os
import json
import subprocess
import sys

def create_directory_structure():
    """Create the recommended directory structure for Air + Tailwind CSS"""
    directories = [
        "static",
        "static/css",
        "static/js",
        "static/images",
        "templates"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_tailwind_config():
    """Create tailwind.config.js file"""
    config_content = """/** @type {import('tailwindcss').Config} */
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
"""
    
    with open("tailwind.config.js", "w") as f:
        f.write(config_content)
    
    print("Created tailwind.config.js")

def create_postcss_config():
    """Create postcss.config.js file"""
    config_content = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}
"""
    
    with open("postcss.config.js", "w") as f:
        f.write(config_content)
    
    print("Created postcss.config.js")

def create_input_css():
    """Create the input CSS file with Tailwind directives"""
    css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

/* Add your custom CSS here */
"""
    
    with open("static/css/input.css", "w") as f:
        f.write(css_content)
    
    print("Created static/css/input.css")

def create_package_json():
    """Create package.json with Tailwind CSS dependencies"""
    package_content = {
        "name": "air-tailwind-setup",
        "version": "1.0.0",
        "description": "Tailwind CSS setup for Air framework",
        "main": "index.js",
        "scripts": {
            "build": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css",
            "watch": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
        },
        "keywords": ["air", "tailwindcss"],
        "author": "Air Developer",
        "license": "MIT",
        "devDependencies": {
            "tailwindcss": "^3.4.0",
            "autoprefixer": "^10.4.0",
            "postcss": "^8.4.0"
        }
    }
    
    with open("package.json", "w") as f:
        json.dump(package_content, f, indent=2)
    
    print("Created package.json")

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_dependencies():
    """Install npm dependencies"""
    if not check_node_installed():
        print("Node.js is not installed. Please install Node.js first.")
        print("Visit https://nodejs.org/ to download and install Node.js")
        return False
    
    try:
        print("Installing Tailwind CSS and related dependencies...")
        subprocess.run(["npm", "install"], check=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please make sure npm is working correctly.")
        return False

def create_example_template():
    """Create an example HTML template"""
    template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Air + Tailwind CSS</title>
    <link href="/static/css/output.css" rel="stylesheet">
</head>
<body>
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold text-indigo-600">Hello, Tailwind CSS!</h1>
        <p class="mt-4 text-gray-700">This is an example template using Tailwind CSS with Air framework.</p>
        <button class="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
            Click Me
        </button>
    </div>
</body>
</html>
"""
    
    with open("templates/example.html", "w") as f:
        f.write(template_content)
    
    print("Created templates/example.html")

def print_instructions():
    """Print setup instructions"""
    instructions = """
Setup Complete!

To start using Tailwind CSS with your Air framework:

1. Build the CSS file:
   npm run build

2. Or watch for changes during development:
   npm run watch

3. In your Air application, mount the static directory:
   app.mount("/static", air.StaticFiles(directory="static"), name="static")

4. Include the CSS in your HTML templates:
   <link href="/static/css/output.css" rel="stylesheet">

5. Use Tailwind classes in your HTML:
   <h1 class="text-3xl font-bold text-blue-600">Hello World</h1>

For more information, check out:
- Tailwind CSS Documentation: https://tailwindcss.com/docs
- Air Framework Documentation: https://feldroy.github.io/air/
"""
    print(instructions)

def main():
    """Main setup function"""
    print("Setting up Tailwind CSS for Air framework...")
    
    # Create directory structure
    create_directory_structure()
    
    # Create configuration files
    create_tailwind_config()
    create_postcss_config()
    create_input_css()
    create_package_json()
    create_example_template()
    
    # Install dependencies
    if install_dependencies():
        print("\nSetup completed successfully!")
        print_instructions()
    else:
        print("\nSetup completed with manual installation required.")
        print("\nPlease run 'npm install' manually to install dependencies.")
        print_instructions()

if __name__ == "__main__":
    main()