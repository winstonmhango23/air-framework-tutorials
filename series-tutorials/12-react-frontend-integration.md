# Part 12: React Frontend Integration with the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this twelfth installment, we're exploring one of the most exciting aspects of modern web development: **React Frontend Integration**.

In our previous posts, we've covered [the basics of Air](01-introduction-to-air-framework.md), [mastered Air Tags](02-mastering-air-tags.md), learned about [routing and HTTP methods](03-routing-and-http-methods.md), explored [forms and validation](04-forms-and-validation.md), understood [templates and Jinja integration](05-templates-and-jinja-integration.md), enhanced our applications with [Tailwind CSS styling](06-styling-with-tailwind-css.md), made our apps more interactive with [HTMX integration](07-htmx-integration.md), implemented [database integration](08-database-integration.md), secured our applications with [authentication and security](09-authentication-and-security.md), ensured quality through [testing and debugging](10-testing-and-debugging.md), and prepared our applications for production with [deployment and performance optimization](11-deployment-and-performance.md). Now it's time to take our Air applications to the next level by integrating them with modern React frontend applications.

## Introduction to React Integration with Air

React has become the de facto standard for building interactive user interfaces on the web. By integrating React with Air, we can leverage the best of both worlds: Air's powerful backend capabilities and React's component-based frontend architecture. This separation of concerns allows teams to work more efficiently and enables better scalability for complex applications.

### Why Integrate React with Air?

1. **Separation of Concerns**: Clear division between backend logic and frontend presentation
2. **Developer Experience**: Modern development workflows with hot reloading and component-based architecture
3. **Performance**: React's virtual DOM provides efficient UI updates
4. **Ecosystem**: Access to a vast library of React components and tools
5. **Scalability**: Easier to scale frontend and backend independently

## Setting Up the React Project

Let's start by creating a new React project using Vite, which provides an excellent development experience with fast hot module replacement.

### Creating a React App with Vite

```bash
# Create a new React project with Vite
npm create vite@latest air-react-frontend -- --template react

# Navigate to the project directory
cd air-react-frontend

# Install dependencies
npm install

# Install additional dependencies we'll need
npm install axios react-router-dom @tailwindcss/vite
```

### Project Structure

A typical React project with Vite follows this structure:

```
air-react-frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── utils/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

### Environment Configuration

Create environment files for different environments:

```bash
# .env.development
VITE_API_URL=http://localhost:8000

# .env.production
VITE_API_URL=https://your-production-api.com
```

### Proxy Setup for Development

To avoid CORS issues during development, configure a proxy in Vite:

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
```

## Building the React Frontend

Let's build a complete React frontend that integrates with our Air backend.

### Component Architecture

A well-structured React application follows a component-based architecture:

```jsx
// src/App.jsx
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import PostsPage from './pages/PostsPage'
import PostDetailPage from './pages/PostDetailPage'
import CreatePostPage from './pages/CreatePostPage'
import Navbar from './components/Navbar'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/posts" element={<PostsPage />} />
            <Route path="/posts/:id" element={<PostDetailPage />} />
            <Route path="/create-post" element={<CreatePostPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
```

### State Management with useState and useContext

Let's implement state management using React's built-in hooks:

```jsx
// src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in (from localStorage or API)
    const token = localStorage.getItem('token')
    if (token) {
      // Validate token and set user
      validateToken(token)
        .then(userData => {
          setUser(userData)
          setLoading(false)
        })
        .catch(() => {
          localStorage.removeItem('token')
          setLoading(false)
        })
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (credentials) => {
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      })
      
      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('token', data.token)
        setUser(data.user)
        return { success: true }
      } else {
        const error = await response.json()
        return { success: false, error: error.detail }
      }
    } catch (error) {
      return { success: false, error: 'Network error' }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  const value = {
    user,
    login,
    logout,
    loading,
    isAuthenticated: !!user,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
```

### Routing with React Router

Implement navigation between different pages:

```jsx
// src/components/Navbar.jsx
import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth()
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <Link to="/" className="text-xl font-bold text-blue-600">
              Air Blog
            </Link>
            <div className="hidden md:flex space-x-4">
              <Link
                to="/"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/') 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Home
              </Link>
              <Link
                to="/posts"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/posts') 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Posts
              </Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-sm text-gray-700">
                  Welcome, {user.username}
                </span>
                <button
                  onClick={logout}
                  className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                to="/login"
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
              >
                Login
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
```

### Form Handling with React Hook Form

For complex form handling, we can use React Hook Form:

```jsx
// src/pages/CreatePostPage.jsx
import React from 'react'
import { useForm } from 'react-hook-form'
import { useAuth } from '../context/AuthContext'

const CreatePostPage = () => {
  const { user } = useAuth()
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm()

  const onSubmit = async (data) => {
    try {
      const response = await fetch('/api/posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(data),
      })

      if (response.ok) {
        reset()
        alert('Post created successfully!')
        // Redirect to posts page
        window.location.href = '/posts'
      } else {
        const error = await response.json()
        alert(`Error: ${error.detail}`)
      }
    } catch (error) {
      alert('Network error occurred')
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Create New Post</h1>
      
      <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-6 rounded-lg shadow-md">
        <div className="mb-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title
          </label>
          <input
            id="title"
            {...register('title', { 
              required: 'Title is required',
              minLength: {
                value: 5,
                message: 'Title must be at least 5 characters'
              }
            })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
          )}
        </div>

        <div className="mb-4">
          <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-1">
            Content
          </label>
          <textarea
            id="content"
            rows={6}
            {...register('content', { 
              required: 'Content is required',
              minLength: {
                value: 10,
                message: 'Content must be at least 10 characters'
              }
            })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.content && (
            <p className="mt-1 text-sm text-red-600">{errors.content.message}</p>
          )}
        </div>

        <div className="flex items-center">
          <input
            id="published"
            type="checkbox"
            {...register('published')}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label htmlFor="published" className="ml-2 block text-sm text-gray-700">
            Publish immediately
          </label>
        </div>

        <div className="mt-6">
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {isSubmitting ? 'Creating...' : 'Create Post'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default CreatePostPage
```

## Connecting React to Air API

Now let's connect our React frontend to the Air backend API.

### Fetching Data with useEffect

```jsx
// src/pages/PostsPage.jsx
import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const PostsPage = () => {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('/api/posts')
        if (response.ok) {
          const data = await response.json()
          setPosts(data)
        } else {
          throw new Error('Failed to fetch posts')
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchPosts()
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-700">Error: {error}</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Blog Posts</h1>
        <Link
          to="/create-post"
          className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
        >
          Create Post
        </Link>
      </div>

      {posts.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No posts found.</p>
        </div>
      ) : (
        <div className="grid gap-6">
          {posts.map((post) => (
            <div key={post.id} className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-2">
                <Link 
                  to={`/posts/${post.id}`} 
                  className="text-blue-600 hover:text-blue-800"
                >
                  {post.title}
                </Link>
              </h2>
              <p className="text-gray-600 text-sm mb-4">
                By {post.author} • {new Date(post.created_at).toLocaleDateString()}
              </p>
              <p className="text-gray-700 mb-4">
                {post.content.substring(0, 150)}...
              </p>
              <div className="flex items-center">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  post.published 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {post.published ? 'Published' : 'Draft'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default PostsPage
```

### POST/PUT/DELETE Operations

```jsx
// src/services/postService.js
const API_BASE_URL = '/api'

class PostService {
  async getAllPosts() {
    const response = await fetch(`${API_BASE_URL}/posts`)
    if (!response.ok) {
      throw new Error('Failed to fetch posts')
    }
    return response.json()
  }

  async getPostById(id) {
    const response = await fetch(`${API_BASE_URL}/posts/${id}`)
    if (!response.ok) {
      throw new Error('Failed to fetch post')
    }
    return response.json()
  }

  async createPost(postData) {
    const response = await fetch(`${API_BASE_URL}/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(postData),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create post')
    }
    
    return response.json()
  }

  async updatePost(id, postData) {
    const response = await fetch(`${API_BASE_URL}/posts/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(postData),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to update post')
    }
    
    return response.json()
  }

  async deletePost(id) {
    const response = await fetch(`${API_BASE_URL}/posts/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to delete post')
    }
    
    return response.json()
  }
}

export default new PostService()
```

### Error Handling

Implement comprehensive error handling:

```jsx
// src/hooks/useApi.js
import { useState, useEffect } from 'react'

export const useApi = (apiFunction, dependencies = []) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)
        const result = await apiFunction()
        setData(result)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, dependencies)

  return { data, loading, error }
}
```

### Loading States

Create reusable loading components:

```jsx
// src/components/LoadingSpinner.jsx
import React from 'react'

const LoadingSpinner = ({ size = 'md' }) => {
  const sizeClasses = {
    sm: 'h-6 w-6',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
  }

  return (
    <div className="flex justify-center items-center">
      <div className={`${sizeClasses[size]} animate-spin rounded-full border-b-2 border-blue-500`}></div>
    </div>
  )
}

export default LoadingSpinner
```

## Tailwind CSS in React

Integrate Tailwind CSS for styling React components:

### Installing Tailwind in React

```bash
# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Component Styling

Create reusable styled components:

```jsx
// src/components/Button.jsx
import React from 'react'

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  disabled = false, 
  className = '',
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2'
  
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-blue-500',
  }
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  }
  
  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed' : ''
  
  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabledClasses} ${className}`

  return (
    <button 
      className={classes}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  )
}

export default Button
```

### Responsive Design

Implement responsive design patterns:

```jsx
// src/components/ResponsiveGrid.jsx
import React from 'react'

const ResponsiveGrid = ({ children, columns = 3 }) => {
  const gridClasses = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
  }

  return (
    <div className={`grid ${gridClasses[columns]} gap-6`}>
      {children}
    </div>
  )
}

export default ResponsiveGrid
```

## Advanced React Patterns

### Custom Hooks

Create custom hooks for common functionality:

```jsx
// src/hooks/useLocalStorage.js
import { useState, useEffect } from 'react'

export const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      return initialValue
    }
  })

  const setValue = (value) => {
    try {
      setStoredValue(value)
      window.localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error('Error saving to localStorage:', error)
    }
  }

  return [storedValue, setValue]
}
```

### Context Providers

Use context providers for global state:

```jsx
// src/context/ThemeContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react'

const ThemeContext = createContext()

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light')

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light'
    setTheme(savedTheme)
    document.documentElement.classList.toggle('dark', savedTheme === 'dark')
  }, [])

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
    localStorage.setItem('theme', newTheme)
    document.documentElement.classList.toggle('dark', newTheme === 'dark')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}
```

### Performance Optimization

Implement performance optimization techniques:

```jsx
// src/components/OptimizedPostList.jsx
import React, { memo, useMemo } from 'react'
import PostItem from './PostItem'

const OptimizedPostList = memo(({ posts, onDelete }) => {
  // Memoize expensive calculations
  const sortedPosts = useMemo(() => {
    return [...posts].sort((a, b) => 
      new Date(b.created_at) - new Date(a.created_at)
    )
  }, [posts])

  return (
    <div className="space-y-4">
      {sortedPosts.map(post => (
        <PostItem 
          key={post.id} 
          post={post} 
          onDelete={onDelete} 
        />
      ))}
    </div>
  )
})

export default OptimizedPostList
```

## Testing React Components

Set up testing for React components:

```bash
# Install testing dependencies
npm install -D @testing-library/react @testing-library/jest-dom jest-environment-jsdom
```

```jsx
// src/__tests__/Button.test.jsx
import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import Button from '../components/Button'

describe('Button', () => {
  test('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  test('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  test('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)
    expect(screen.getByText('Click me')).toBeDisabled()
  })
})
```

## What's Coming Next

In our next post, we'll explore Expo React Native mobile app development, covering:

1. Introduction to Expo and its benefits
2. Creating mobile apps with React Native
3. Connecting mobile apps to Air backends
4. Mobile UI with Tailwind CSS
5. Publishing and distribution strategies

## Conclusion

Integrating React with the Air framework creates a powerful full-stack development experience. By separating frontend and backend concerns, you can leverage the strengths of both technologies while maintaining a clean, scalable architecture.

Key takeaways from this post:

1. **Project Setup**: Create React applications with Vite for fast development
2. **Component Architecture**: Build reusable, well-structured React components
3. **State Management**: Use useState, useContext, and custom hooks for effective state management
4. **API Integration**: Connect React frontend to Air backend APIs with proper error handling
5. **Styling**: Implement responsive design with Tailwind CSS
6. **Advanced Patterns**: Leverage custom hooks, context providers, and performance optimization techniques

With React frontend integration mastered, you can now build modern, interactive web applications that communicate seamlessly with your Air backend. The combination of Air's Python-based approach and React's component-based architecture provides an efficient workflow for building full-stack applications.

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for weekly updates. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

See you in the next post where we'll dive into Expo React Native mobile app development!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [Deployment and Performance Optimization](11-deployment-and-performance.md)*

## Quiz: Test Your Knowledge

1. Which tool is recommended for creating React applications in the tutorial?
   a) Create React App
   b) Next.js
   c) Vite
   d) Webpack

2. What is the correct way to fetch data from an Air API in a React component?
   a) Using XMLHttpRequest directly
   b) Using the fetch API or Axios
   c) Using jQuery AJAX
   d) Using Air's built-in fetch function

3. What React hook is used for managing local component state?
   a) useEffect
   b) useContext
   c) useState
   d) useMemo

4. True or False: You can use Tailwind CSS for styling React components when integrating with Air applications.

5. True or False: React components must be written in JavaScript, not TypeScript.

6. Explain the benefits of separating the frontend (React) and backend (Air) into separate applications, and how they communicate with each other.

### Answers:
1. c) Vite
2. b) Using the fetch API or Axios
3. c) useState
4. True
5. False - React components can be written in either JavaScript or TypeScript
6. Separating frontend and backend applications provides several benefits: 1) Independent development and deployment cycles, 2) Technology specialization (JavaScript/React for frontend, Python/Air for backend), 3) Better scalability (frontend and backend can be scaled independently), 4) Improved security (separation of concerns), and 5) Team specialization (frontend and backend developers can work independently). They communicate through REST APIs or GraphQL endpoints, where the React frontend makes HTTP requests to the Air backend, which responds with JSON data that the frontend can then render in the UI.