# Part 14: Real-World Project Development with the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this fourteenth and final installment, we're exploring one of the most exciting aspects of software development: **Real-World Project Development**.

In our previous posts, we've covered [the basics of Air](01-introduction-to-air-framework.md), [mastered Air Tags](02-mastering-air-tags.md), learned about [routing and HTTP methods](03-routing-and-http-methods.md), explored [forms and validation](04-forms-and-validation.md), understood [templates and Jinja integration](05-templates-and-jinja-integration.md), enhanced our applications with [Tailwind CSS styling](06-styling-with-tailwind-css.md), made our apps more interactive with [HTMX integration](07-htmx-integration.md), implemented [database integration](08-database-integration.md), secured our applications with [authentication and security](09-authentication-and-security.md), ensured quality through [testing and debugging](10-testing-and-debugging.md), prepared our applications for production with [deployment and performance optimization](11-deployment-and-performance.md), integrated with modern [React frontend applications](12-react-frontend-integration.md), and developed [Expo React Native mobile apps](13-expo-react-native-mobile-app.md). Now it's time to bring all these concepts together in a comprehensive real-world project that showcases the full power of the Air framework.

## Project Planning

Before diving into implementation, proper planning is essential for successful project development. Let's explore the key aspects of project planning for a real-world Air application.

### Requirements Gathering

The first step in any successful project is understanding what needs to be built. For our example project, let's build a task management application with the following requirements:

1. **User Management**: User registration, authentication, and profile management
2. **Task Management**: Create, read, update, and delete tasks with due dates and priorities
3. **Project Organization**: Group tasks into projects with team collaboration features
4. **Real-time Updates**: Live notifications and status updates
5. **File Attachments**: Upload and manage files associated with tasks
6. **Search and Filter**: Advanced search and filtering capabilities
7. **Admin Dashboard**: Administrative interface for managing users and system settings
8. **Mobile Support**: Full functionality on mobile devices
9. **API Access**: RESTful API for third-party integrations

### Architecture Design

A well-designed architecture is crucial for maintainable and scalable applications. Let's design a modern full-stack architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │   Web Frontend  │    │   Admin Panel   │
│   (Expo RN)     │    │    (React)      │    │   (FastAdmin)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      API Gateway        │
                    │    (Air Framework)      │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼────────┐      ┌────────▼────────┐      ┌────────▼────────┐
│ Authentication │      │   Task Service  │      │  Project Service│
│    Service     │      │                 │      │                 │
└────────────────┘      └─────────────────┘      └─────────────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      Data Layer         │
                    │  (PostgreSQL + Redis)   │
                    └─────────────────────────┘
```

### Technology Stack Selection

For our real-world project, we'll select the following technology stack:

**Backend (Air Framework):**
- Air (built on FastAPI, Starlette, Pydantic)
- SQLModel for database ORM
- PostgreSQL for primary database
- Redis for caching and real-time messaging
- JWT for authentication
- Celery for background tasks

**Frontend (Web):**
- React with Vite
- Tailwind CSS for styling
- React Router for navigation
- React Query for data fetching
- Socket.IO for real-time communication

**Mobile:**
- Expo React Native
- NativeWind for Tailwind CSS
- Expo Router for navigation
- Expo Notifications for push notifications

**Infrastructure:**
- Docker for containerization
- Docker Compose for multi-service orchestration
- Nginx as reverse proxy
- Let's Encrypt for SSL certificates
- GitHub Actions for CI/CD

## Implementation

Now let's dive into the implementation of our real-world project, covering backend, frontend, and mobile development.

### Backend Development with Air

Let's start by implementing the core backend services with Air:

```python
# main.py
import air
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
import redis
import asyncio

# Database setup
DATABASE_URL = "postgresql://user:password@localhost/taskmanager"
engine = create_engine(DATABASE_URL)

# Redis setup for caching and real-time messaging
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Create tables
from models import User, Task, Project
SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: air.Air):
    # Startup
    print("Starting up Task Manager application...")
    yield
    # Shutdown
    print("Shutting down Task Manager application...")

app = air.Air(lifespan=lifespan)

# Dependency injection for database session
def get_session():
    with Session(engine) as session:
        yield session

# Dependency injection for Redis client
def get_redis():
    return redis_client

# Import routers
from routers import auth, tasks, projects, users

# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(tasks.router, prefix="/api/tasks")
app.include_router(projects.router, prefix="/api/projects")
app.include_router(users.router, prefix="/api/users")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```python
# models.py
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    full_name: str
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="assignee")
    projects: List["Project"] = Relationship(back_populates="owner")

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    owner_id: int = Field(foreign_key="user.id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    owner: User = Relationship(back_populates="projects")
    tasks: List["Task"] = Relationship(back_populates="project")

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    project_id: int = Field(foreign_key="project.id")
    assignee_id: Optional[int] = Field(default=None, foreign_key="user.id")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    project: Project = Relationship(back_populates="tasks")
    assignee: Optional[User] = Relationship(back_populates="tasks")

class FileAttachment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    filename: str
    file_path: str
    file_size: int
    content_type: str
    uploaded_by_id: int = Field(foreign_key="user.id")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
```

```python
# routers/auth.py
import air
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from models import User
from services import auth_service
from schemas import UserCreate, UserLogin, Token

router = air.APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    db_user = auth_service.create_user(user, session)
    return db_user

@router.post("/login", response_model=Token)
async def login_user(credentials: UserLogin, session: Session = Depends(get_session)):
    user = auth_service.authenticate_user(
        credentials.email, credentials.password, session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
```

### Frontend Development with React

Let's implement the web frontend with React:

``jsx
// src/App.jsx
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { AuthProvider } from './contexts/AuthContext'
import { SocketProvider } from './contexts/SocketContext'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import ProjectDetail from './pages/ProjectDetail'
import Tasks from './pages/Tasks'
import TaskDetail from './pages/TaskDetail'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Register from './pages/Register'
import ProtectedRoute from './components/ProtectedRoute'
import './App.css'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <SocketProvider>
          <Router>
            <div className="min-h-screen bg-gray-50">
              <Navbar />
              <main className="container mx-auto px-4 py-8">
                <Routes>
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route element={<ProtectedRoute />}>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/projects" element={<Projects />} />
                    <Route path="/projects/:id" element={<ProjectDetail />} />
                    <Route path="/tasks" element={<Tasks />} />
                    <Route path="/tasks/:id" element={<TaskDetail />} />
                    <Route path="/profile" element={<Profile />} />
                  </Route>
                </Routes>
              </main>
            </div>
          </Router>
        </SocketProvider>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
```

```jsx
// src/pages/Dashboard.jsx
import React from 'react'
import { useQuery } from 'react-query'
import { useAuth } from '../contexts/AuthContext'
import { useSocket } from '../contexts/SocketContext'
import TaskCard from '../components/TaskCard'
import StatCard from '../components/StatCard'
import { fetchDashboardData } from '../services/api'

const Dashboard = () => {
  const { user } = useAuth()
  const { socket } = useSocket()
  const { data: dashboardData, isLoading } = useQuery('dashboard', fetchDashboardData)

  React.useEffect(() => {
    if (socket) {
      socket.on('taskUpdated', (task) => {
        // Update UI in real-time
        console.log('Task updated:', task)
      })
    }

    return () => {
      if (socket) {
        socket.off('taskUpdated')
      }
    }
  }, [socket])

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Welcome back, {user?.full_name}</h1>
      
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard 
          title="Total Tasks" 
          value={dashboardData?.totalTasks || 0} 
          icon="📋"
        />
        <StatCard 
          title="Completed" 
          value={dashboardData?.completedTasks || 0} 
          icon="✅"
        />
        <StatCard 
          title="In Progress" 
          value={dashboardData?.inProgressTasks || 0} 
          icon="🔄"
        />
        <StatCard 
          title="Overdue" 
          value={dashboardData?.overdueTasks || 0} 
          icon="⏰"
        />
      </div>

      {/* Recent Tasks */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Tasks</h2>
        <div className="space-y-4">
          {dashboardData?.recentTasks?.map(task => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
```

### Mobile App with Expo

Let's implement the mobile app with Expo React Native:

``jsx
// app/(tabs)/index.jsx
import React from 'react'
import { View, Text, ScrollView } from 'react-native'
import { styled } from 'nativewind'
import { useQuery } from 'react-query'
import { useAuth } from '../../contexts/AuthContext'
import { fetchDashboardData } from '../../services/api'
import TaskCard from '../../components/TaskCard'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledScrollView = styled(ScrollView)

export default function HomeScreen() {
  const { user } = useAuth()
  const { data: dashboardData, isLoading } = useQuery('mobileDashboard', fetchDashboardData)

  if (isLoading) {
    return (
      <StyledView className="flex-1 justify-center items-center bg-gray-50">
        <StyledView className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></StyledView>
      </StyledView>
    )
  }

  return (
    <StyledScrollView className="flex-1 bg-gray-50 p-4">
      <StyledText className="text-2xl font-bold mb-6">
        Welcome back, {user?.full_name}
      </StyledText>
      
      <StyledView className="bg-white rounded-lg shadow-md p-4 mb-6">
        <StyledText className="text-lg font-semibold mb-3">Recent Tasks</StyledText>
        {dashboardData?.recentTasks?.map(task => (
          <TaskCard key={task.id} task={task} />
        ))}
      </StyledView>
    </StyledScrollView>
  )
}
```

### Shared Components and Utilities

Let's create shared components that can be used across web and mobile:

```jsx
// components/TaskCard.jsx
import React from 'react'
import { View, Text, TouchableOpacity } from 'react-native'
import { styled } from 'nativewind'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledTouchableOpacity = styled(TouchableOpacity)

const TaskCard = ({ task, onPress }) => {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 border-red-500'
      case 'high': return 'bg-orange-100 border-orange-500'
      case 'medium': return 'bg-yellow-100 border-yellow-500'
      case 'low': return 'bg-green-100 border-green-500'
      default: return 'bg-gray-100 border-gray-500'
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'done': return 'bg-green-500'
      case 'in_progress': return 'bg-blue-500'
      case 'review': return 'bg-purple-500'
      default: return 'bg-gray-500'
    }
  }

  return (
    <StyledTouchableOpacity 
      className="bg-white border border-gray-200 rounded-lg p-4 mb-3 shadow-sm"
      onPress={() => onPress && onPress(task)}
    >
      <StyledView className="flex-row justify-between items-start mb-2">
        <StyledText className="text-lg font-semibold text-gray-800 flex-1">
          {task.title}
        </StyledText>
        <StyledView className={`px-2 py-1 rounded-full border ${getPriorityColor(task.priority)}`}>
          <StyledText className="text-xs font-medium capitalize">
            {task.priority}
          </StyledText>
        </StyledView>
      </StyledView>
      
      {task.description && (
        <StyledText className="text-gray-600 mb-3" numberOfLines={2}>
          {task.description}
        </StyledText>
      )}
      
      <StyledView className="flex-row justify-between items-center">
        <StyledView className="flex-row items-center">
          <StyledView className={`w-3 h-3 rounded-full mr-2 ${getStatusColor(task.status)}`}></StyledView>
          <StyledText className="text-sm text-gray-500 capitalize">
            {task.status.replace('_', ' ')}
          </StyledText>
        </StyledView>
        
        {task.due_date && (
          <StyledText className="text-sm text-gray-500">
            Due: {new Date(task.due_date).toLocaleDateString()}
          </StyledText>
        )}
      </StyledView>
    </StyledTouchableOpacity>
  )
}

export default TaskCard
```

## Advanced Features

Now let's implement some advanced features that make our real-world project stand out.

### Real-time Updates with WebSockets

Let's implement real-time updates using WebSockets:

```python
# services/websocket_service.py
import json
import asyncio
from typing import Dict, Set
import websockets
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message)
                except:
                    # Remove broken connections
                    self.disconnect(connection, user_id)

    async def broadcast(self, message: str):
        for user_connections in self.active_connections.values():
            for connection in user_connections.copy():
                try:
                    await connection.send_text(message)
                except:
                    user_connections.discard(connection)

manager = ConnectionManager()

# routers/websocket.py
import air
from fastapi import WebSocket, Depends
from services import websocket_service, auth_service

router = air.APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    # Authenticate user
    user = auth_service.get_user_from_token(token)
    if not user:
        await websocket.close(code=1008)
        return

    await websocket_service.manager.connect(websocket, user.id)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages
            await websocket_service.manager.send_personal_message(
                f"You sent: {data}", user.id
            )
    except:
        websocket_service.manager.disconnect(websocket, user.id)
```

```javascript
// contexts/SocketContext.jsx
import React, { createContext, useContext, useEffect, useState } from 'react'
import { useAuth } from './AuthContext'

const SocketContext = createContext()

export const useSocket = () => {
  const context = useContext(SocketContext)
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider')
  }
  return context
}

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null)
  const { user, token } = useAuth()

  useEffect(() => {
    if (user && token) {
      const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`)
      
      ws.onopen = () => {
        console.log('WebSocket connected')
        setSocket(ws)
      }
      
      ws.onclose = () => {
        console.log('WebSocket disconnected')
        setSocket(null)
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      
      return () => {
        ws.close()
      }
    }
  }, [user, token])

  const sendMessage = (message) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message))
    }
  }

  return (
    <SocketContext.Provider value={{ socket, sendMessage }}>
      {children}
    </SocketContext.Provider>
  )
}
```

### File Upload and Management

Let's implement file upload and management functionality:

``python
# services/file_service.py
import os
import uuid
from pathlib import Path
from typing import Optional
from sqlmodel import Session
from models import FileAttachment

class FileService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
    
    def save_file(self, file, task_id: int, user_id: int, session: Session) -> FileAttachment:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = self.upload_dir / unique_filename
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Save file metadata to database
        file_attachment = FileAttachment(
            task_id=task_id,
            filename=file.filename,
            file_path=str(file_path),
            file_size=len(content),
            content_type=file.content_type,
            uploaded_by_id=user_id
        )
        
        session.add(file_attachment)
        session.commit()
        session.refresh(file_attachment)
        
        return file_attachment
    
    def get_file(self, file_id: int, session: Session) -> Optional[FileAttachment]:
        return session.get(FileAttachment, file_id)
    
    def delete_file(self, file_id: int, session: Session) -> bool:
        file_attachment = session.get(FileAttachment, file_id)
        if file_attachment:
            # Delete file from disk
            try:
                os.remove(file_attachment.file_path)
            except:
                pass
            
            # Delete from database
            session.delete(file_attachment)
            session.commit()
            return True
        return False

file_service = FileService()
```

```python
# routers/files.py
import air
from fastapi import File, UploadFile, Depends
from sqlmodel import Session
from services import file_service
from models import FileAttachment

router = air.APIRouter(prefix="/files", tags=["files"])

@router.post("/upload/{task_id}", response_model=FileAttachment)
async def upload_file(
    task_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    file_attachment = file_service.save_file(file, task_id, current_user.id, session)
    return file_attachment

@router.get("/{file_id}")
async def download_file(
    file_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    file_attachment = file_service.get_file(file_id, session)
    if not file_attachment:
        raise HTTPException(status_code=404, detail="File not found")
    
    return air.FileResponse(
        file_attachment.file_path,
        media_type=file_attachment.content_type,
        filename=file_attachment.filename
    )

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    success = file_service.delete_file(file_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"message": "File deleted successfully"}
```

### Search Functionality

Let's implement advanced search functionality:

``python
# services/search_service.py
from sqlmodel import Session, select
from models import Task, Project, User
from typing import List, Optional

class SearchService:
    def search_tasks(
        self, 
        session: Session,
        query: str,
        project_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[int] = None
    ) -> List[Task]:
        statement = select(Task)
        
        # Text search
        if query:
            statement = statement.where(
                (Task.title.contains(query)) | 
                (Task.description.contains(query))
            )
        
        # Filter by project
        if project_id:
            statement = statement.where(Task.project_id == project_id)
        
        # Filter by status
        if status:
            statement = statement.where(Task.status == status)
        
        # Filter by priority
        if priority:
            statement = statement.where(Task.priority == priority)
        
        # Filter by assignee
        if assignee_id:
            statement = statement.where(Task.assignee_id == assignee_id)
        
        return session.exec(statement).all()
    
    def search_projects(
        self,
        session: Session,
        query: str
    ) -> List[Project]:
        statement = select(Project)
        
        if query:
            statement = statement.where(
                (Project.name.contains(query)) | 
                (Project.description.contains(query))
            )
        
        return session.exec(statement).all()

search_service = SearchService()
```

```python
# routers/search.py
import air
from fastapi import Depends
from sqlmodel import Session
from services import search_service
from models import Task, Project

router = air.APIRouter(prefix="/search", tags=["search"])

@router.get("/tasks", response_model=List[Task])
async def search_tasks(
    query: str = "",
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    tasks = search_service.search_tasks(
        session, query, project_id, status, priority, assignee_id
    )
    return tasks

@router.get("/projects", response_model=List[Project])
async def search_projects(
    query: str = "",
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    projects = search_service.search_projects(session, query)
    return projects
```

### Admin Dashboard

Let's implement an admin dashboard for system management:

```python
# routers/admin.py
import air
from fastapi import Depends
from sqlmodel import Session, select
from models import User, Task, Project

router = air.APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
async def get_admin_stats(
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_admin)
):
    # Get user count
    user_count = session.exec(select(User)).count()
    
    # Get task count
    task_count = session.exec(select(Task)).count()
    
    # Get project count
    project_count = session.exec(select(Project)).count()
    
    # Get recent activity
    recent_users = session.exec(
        select(User).order_by(User.created_at.desc()).limit(5)
    ).all()
    
    return {
        "user_count": user_count,
        "task_count": task_count,
        "project_count": project_count,
        "recent_users": recent_users
    }

@router.get("/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_admin)
):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_update: dict,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_admin)
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user
```

## Deployment

Finally, let's prepare our real-world project for production deployment.

### Production Deployment

Let's create Docker configurations for production deployment:

``dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/taskmanager
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: taskmanager
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
```

### CI/CD Pipeline

Let's set up a CI/CD pipeline with GitHub Actions:

``yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:6-alpine
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/postgres
        REDIS_URL: redis://localhost:6379/0
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to production
      run: |
        # Add your deployment commands here
        echo "Deploying to production..."
```

### Monitoring Setup

Let's implement monitoring and logging:

``python
# services/monitoring_service.py
import logging
import time
from functools import wraps
from typing import Callable
import psutil
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MonitoringService:
    def __init__(self):
        self.metrics = {}
    
    def track_execution_time(self, func_name: str):
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    logger.info(f"{func_name} executed in {execution_time:.4f} seconds")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(f"{func_name} failed after {execution_time:.4f} seconds: {str(e)}")
                    raise
            return wrapper
        return decorator
    
    def get_system_metrics(self):
        process = psutil.Process(os.getpid())
        return {
            "cpu_percent": process.cpu_percent(),
            "memory_mb": process.memory_info().rss / 1024 / 1024,
            "connections": len(process.connections()),
            "uptime_seconds": time.time() - process.create_time()
        }

monitoring_service = MonitoringService()
```

### Performance Optimization

Let's implement performance optimization techniques:

``python
# services/cache_service.py
import redis
import json
from typing import Optional, Any
from functools import wraps

class CacheService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        try:
            ttl = ttl or self.default_ttl
            self.redis.setex(key, ttl, json.dumps(value))
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
    
    def delete(self, key: str):
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
    
    def cached(self, key_prefix: str, ttl: int = None):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = f"{key_prefix}:{hash(str(args) + str(kwargs))}"
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function and cache result
                result = await func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            return wrapper
        return decorator

# Usage example
cache_service = CacheService(redis_client)

@router.get("/tasks")
@cache_service.cached("tasks", ttl=300)  # Cache for 5 minutes
async def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks
```

## Conclusion

Congratulations! You've completed our comprehensive journey through the Air web framework. Throughout this series, we've explored everything from the basics of Air and Air Tags to advanced topics like real-world project development with full-stack implementations.

Key takeaways from this series:

1. **Foundation**: Understanding the Air framework built on FastAPI, Starlette, and Pydantic
2. **Core Concepts**: Mastering Air Tags, routing, forms, and validation
3. **Frontend Integration**: Styling with Tailwind CSS and enhancing with HTMX
4. **Data Management**: Database integration with SQLModel and SQLAlchemy
5. **Security**: Authentication, authorization, and security best practices
6. **Quality Assurance**: Testing and debugging techniques
7. **Production Readiness**: Deployment strategies and performance optimization
8. **Full-Stack Development**: React frontend and Expo mobile app integration
9. **Advanced Features**: Real-time updates, file management, and admin dashboards

With these skills, you're now equipped to build modern, scalable web applications that run on web and mobile platforms. The Air framework provides an excellent foundation for full-stack development, combining the power of Python with modern frontend technologies.

### Next Steps

To continue your journey with Air:

1. **Build Projects**: Start with small projects and gradually increase complexity
2. **Contribute**: Contribute to the Air framework or related open-source projects
3. **Stay Updated**: Follow the latest developments in the Air and FastAPI ecosystems
4. **Join Communities**: Participate in forums, conferences, and meetups
5. **Explore Advanced Topics**: Dive deeper into microservices, internationalization, and accessibility

### Resources

- [Official Air Documentation](https://feldroy.github.io/air/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [React Documentation](https://reactjs.org/)
- [Expo Documentation](https://docs.expo.dev/)

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for updates and additional content. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

Thank you for joining me on this journey through the Air framework. I hope you've found this series valuable and that you're excited to start building amazing applications with Air!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [Expo React Native Mobile App](13-expo-react-native-mobile-app.md)*

## Quiz: Test Your Knowledge

1. What is the primary benefit of using a task queue system like Celery in a web application?
   a) Faster database queries
   b) Handling long-running operations asynchronously
   c) Improved CSS styling
   d) Better HTML rendering

2. Which authentication method is most appropriate for API endpoints consumed by mobile apps?
   a) Session-based authentication
   b) JWT (JSON Web Tokens)
   c) Basic authentication
   d) OAuth 1.0

3. What is the main advantage of implementing database connection pooling?
   a) Reduced memory usage
   b) Improved security
   c) Better performance under high load
   d) Simpler code

4. True or False: Microservices architecture is always the best choice for web applications regardless of project size.

5. True or False: Caching should be implemented at multiple levels (browser, CDN, application, database) for optimal performance.

6. Explain the difference between horizontal and vertical scaling, and when you might choose each approach for a real-world Air application.

### Answers:
1. b) Handling long-running operations asynchronously
2. b) JWT (JSON Web Tokens)
3. c) Better performance under high load
4. False - Microservices add complexity and are best suited for large applications with multiple teams. Smaller applications often benefit from a monolithic architecture.
5. True
6. Horizontal scaling involves adding more servers/machines to distribute the load, while vertical scaling involves increasing the resources (CPU, RAM) of a single server. For a real-world Air application, you might choose horizontal scaling for handling variable traffic loads and improving fault tolerance, especially for stateless components. You might choose vertical scaling for simpler applications with predictable loads where adding more machines would be overkill, or when dealing with databases that don't scale well horizontally.
