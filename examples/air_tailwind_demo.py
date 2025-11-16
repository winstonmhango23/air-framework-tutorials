"""
Air Framework with Tailwind CSS Integration Demo

This example demonstrates various ways to integrate Tailwind CSS with the Air framework,
including CDN approach, static files approach, and advanced features like dark mode.
"""

import air
import uvicorn

# Create Air app instance
app = air.Air()

# Mount static files directory for serving CSS, JS, and images
# Note: You need to create a 'static' directory with your compiled Tailwind CSS
try:
    app.mount("/static", air.StaticFiles(directory="static"), name="static")
    STATIC_FILES_AVAILABLE = True
except RuntimeError:
    # Static directory doesn't exist, we'll use CDN approach
    STATIC_FILES_AVAILABLE = False
    print("Static directory not found. Using CDN approach for Tailwind CSS.")

@app.page
def index():
    """Main demo page showcasing Tailwind CSS integration with Air"""
    
    # Choose CSS approach based on static files availability
    if STATIC_FILES_AVAILABLE:
        css_link = air.Link(rel="stylesheet", href="/static/css/output.css")
        title_text = "Air Framework + Tailwind CSS (Static Files)"
    else:
        css_link = air.Script(src="https://cdn.tailwindcss.com")
        title_text = "Air Framework + Tailwind CSS (CDN)"
    
    return air.Html(
        air.Head(
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            air.Title(title_text),
            css_link,
        ),
        air.Body(
            # Main container with responsive padding
            air.Div(
                # Header section
                air.Header(
                    air.Div(
                        air.H1("Air Framework + Tailwind CSS", 
                              class_="text-3xl md:text-4xl font-bold text-indigo-700"),
                        air.P("A powerful combination for modern web development", 
                              class_="mt-2 text-gray-600"),
                        class_="text-center"
                    ),
                    class_="bg-gradient-to-r from-indigo-50 to-purple-50 py-8 mb-8"
                ),
                
                # Main content grid
                air.Div(
                    # Card 1: Introduction
                    air.Div(
                        air.H2("About This Demo", class_="text-xl font-bold text-gray-800 mb-3"),
                        air.P("This page demonstrates how to integrate Tailwind CSS with the Air framework. "
                              "You can see both CDN and static file approaches in action.", 
                              class_="text-gray-600 mb-4"),
                        air.Ul(
                            air.Li("Responsive design with Tailwind's utility classes", class_="mb-2"),
                            air.Li("Dynamic components with Air Tags", class_="mb-2"),
                            air.Li("Dark mode support", class_="mb-2"),
                            class_="list-disc pl-5 text-gray-600"
                        ),
                        class_="bg-white rounded-lg shadow-md p-6 mb-6"
                    ),
                    
                    # Card 2: Features showcase
                    air.Div(
                        air.H2("Tailwind CSS Features", class_="text-xl font-bold text-gray-800 mb-3"),
                        air.Div(
                            air.Button("Primary Button", 
                                      class_="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg mr-2 mb-2"),
                            air.Button("Secondary Button", 
                                      class_="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-lg mr-2 mb-2"),
                            air.Button("Success Button", 
                                      class_="bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-lg mb-2"),
                            class_="flex flex-wrap"
                        ),
                        air.Div(
                            air.Span("Badge", class_="inline-block bg-red-100 text-red-800 text-xs font-semibold px-2.5 py-0.5 rounded mr-2"),
                            air.Span("Pill", class_="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full mr-2"),
                            air.Span("Large", class_="inline-block bg-yellow-100 text-yellow-800 text-sm font-semibold px-3 py-1 rounded mr-2"),
                            class_="mt-4"
                        ),
                        class_="bg-white rounded-lg shadow-md p-6 mb-6"
                    ),
                    
                    # Card 3: Responsive grid
                    air.Div(
                        air.H2("Responsive Grid", class_="text-xl font-bold text-gray-800 mb-3"),
                        air.P("Resize your browser to see how the grid adapts to different screen sizes.", 
                              class_="text-gray-600 mb-4"),
                        air.Div(
                            air.Div("Column 1", class_="bg-indigo-100 p-4 rounded text-center"),
                            air.Div("Column 2", class_="bg-purple-100 p-4 rounded text-center"),
                            air.Div("Column 3", class_="bg-pink-100 p-4 rounded text-center"),
                            class_="grid grid-cols-1 md:grid-cols-3 gap-4"
                        ),
                        class_="bg-white rounded-lg shadow-md p-6 mb-6"
                    ),
                    
                    # Card 4: Dark mode toggle
                    air.Div(
                        air.H2("Dark Mode", class_="text-xl font-bold text-gray-800 mb-3"),
                        air.P("Click the button below to toggle dark mode. This demonstrates how to implement "
                              "dark mode with Tailwind CSS and JavaScript.", 
                              class_="text-gray-600 mb-4"),
                        air.Button("Toggle Dark Mode", 
                                  id="dark-mode-toggle",
                                  class_="bg-gray-800 hover:bg-gray-900 text-white font-medium py-2 px-4 rounded-lg"),
                        air.Script("""
                            document.getElementById('dark-mode-toggle').addEventListener('click', function() {
                                document.documentElement.classList.toggle('dark');
                            });
                        """),
                        class_="bg-white rounded-lg shadow-md p-6 dark:bg-gray-800 dark:text-white"
                    ),
                    
                    class_="container mx-auto px-4 pb-8 max-w-4xl"
                ),
                
                # Footer
                air.Footer(
                    air.Div(
                        air.P("Built with Air Framework and Tailwind CSS", 
                              class_="text-center text-gray-600 dark:text-gray-400"),
                        air.P(f"CSS Approach: {'Static Files' if STATIC_FILES_AVAILABLE else 'CDN'}", 
                              class_="text-center text-sm text-gray-500 dark:text-gray-500"),
                        class_="py-6"
                    ),
                    class_="bg-gray-100 dark:bg-gray-900 mt-8"
                ),
                
                class_="min-h-screen bg-gray-50 dark:bg-gray-900"
            )
        )
    )

@app.page
def components():
    """Page showcasing various UI components with Tailwind CSS"""
    
    # Choose CSS approach based on static files availability
    if STATIC_FILES_AVAILABLE:
        css_link = air.Link(rel="stylesheet", href="/static/css/output.css")
    else:
        css_link = air.Script(src="https://cdn.tailwindcss.com")
    
    return air.Html(
        air.Head(
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            air.Title("UI Components - Air + Tailwind CSS"),
            css_link,
        ),
        air.Body(
            air.Div(
                air.Header(
                    air.Div(
                        air.H1("UI Components", 
                              class_="text-3xl font-bold text-indigo-700"),
                        air.P("A showcase of various UI components styled with Tailwind CSS", 
                              class_="mt-2 text-gray-600"),
                        air.A("← Back to Home", href=index.url(), 
                             class_="inline-block mt-4 text-indigo-600 hover:text-indigo-800"),
                        class_="text-center"
                    ),
                    class_="bg-gradient-to-r from-indigo-50 to-purple-50 py-8 mb-8"
                ),
                
                air.Div(
                    # Alerts
                    air.Div(
                        air.H2("Alerts", class_="text-2xl font-bold text-gray-800 mb-4"),
                        air.Div(
                            air.Div(
                                air.Strong("Success!", class_="font-bold"),
                                " This is a success alert.",
                                class_="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative"
                            ),
                            air.Div(
                                air.Strong("Warning!", class_="font-bold"),
                                " This is a warning alert.",
                                class_="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative mt-4"
                            ),
                            air.Div(
                                air.Strong("Error!", class_="font-bold"),
                                " This is an error alert.",
                                class_="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4"
                            ),
                            class_="mb-8"
                        ),
                        
                        # Forms
                        air.H2("Forms", class_="text-2xl font-bold text-gray-800 mb-4 mt-8"),
                        air.Div(
                            air.Form(
                                air.Div(
                                    air.Label("Name", for_="name", class_="block text-gray-700 text-sm font-bold mb-2"),
                                    air.Input(type="text", id="name", placeholder="Your name", 
                                             class_="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline")
                                ),
                                air.Div(
                                    air.Label("Email", for_="email", class_="block text-gray-700 text-sm font-bold mb-2 mt-4"),
                                    air.Input(type="email", id="email", placeholder="Your email", 
                                             class_="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline")
                                ),
                                air.Div(
                                    air.Label("Message", for_="message", class_="block text-gray-700 text-sm font-bold mb-2 mt-4"),
                                    air.Textarea(id="message", rows="4", placeholder="Your message", 
                                                class_="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline")
                                ),
                                air.Div(
                                    air.Button("Submit", type="submit", 
                                              class_="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4"),
                                    class_="flex items-center justify-between"
                                ),
                                class_="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                            ),
                            
                            class_="mb-8"
                        ),
                        
                        # Cards
                        air.H2("Cards", class_="text-2xl font-bold text-gray-800 mb-4 mt-8"),
                        air.Div(
                            air.Div(
                                air.Img(src="https://via.placeholder.com/400x200", alt="Placeholder", 
                                       class_="w-full"),
                                air.Div(
                                    air.H3("Card Title", class_="text-xl font-bold mb-2"),
                                    air.P("This is a simple card component with an image, title, and description.", 
                                         class_="text-gray-700 text-base"),
                                    air.Button("Read More", 
                                              class_="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded"),
                                    class_="px-6 py-4"
                                ),
                                class_="max-w-sm rounded overflow-hidden shadow-lg bg-white"
                            ),
                            class_="flex justify-center"
                        ),
                        
                        class_="container mx-auto px-4 pb-8 max-w-4xl"
                    ),
                    
                    class_="bg-gray-50 dark:bg-gray-900 min-h-screen"
                )
            )
        )
    )

if __name__ == "__main__":
    print("Starting Air + Tailwind CSS Demo...")
    print("Open http://localhost:8000 in your browser")
    print("For static files approach, create a 'static/css/output.css' file")
    uvicorn.run("air_tailwind_demo:app", host="127.0.0.1", port=8000, reload=True)