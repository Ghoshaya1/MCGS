"""
Project templates for different programming languages and project types.
"""

from typing import Dict, Any


def get_template_files(language: str, project_type: str = "basic") -> Dict[str, str]:
    """Get template files for a specific language and project type"""
    templates = {
        'python': get_python_templates,
        'javascript': get_javascript_templates,
        'typescript': get_typescript_templates,
        'csharp': get_csharp_templates,
        'java': get_java_templates,
        'go': get_go_templates,
        'rust': get_rust_templates,
        'php': get_php_templates,
        'ruby': get_ruby_templates,
    }
    
    if language in templates:
        return templates[language](project_type)
    
    return get_generic_templates(language, project_type)


def get_python_templates(project_type: str = "basic") -> Dict[str, str]:
    """Python project templates"""
    if project_type == "fastapi":
        return {
            "main.py": '''from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

# In-memory storage (replace with database)
items: List[Item] = []

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    item.id = len(items) + 1
    items.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
            "requirements.txt": '''fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
''',
            "test_main.py": '''import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_and_get_item():
    # Create item
    item_data = {"name": "Test Item", "description": "Test Description"}
    response = client.post("/items", json=item_data)
    assert response.status_code == 200
    created_item = response.json()
    assert created_item["name"] == "Test Item"
    assert created_item["id"] == 1
    
    # Get item
    response = client.get(f"/items/{created_item['id']}")
    assert response.status_code == 200
    assert response.json() == created_item

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
''',
            "README.md": '''# FastAPI Project

A modern, fast web API built with FastAPI.

## Features

- Fast API with automatic interactive documentation
- CORS support
- Data validation with Pydantic
- RESTful endpoints for items management
- Health check endpoint

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

## API Documentation

Once running, visit:
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

## Testing

```bash
pytest test_main.py -v
```

## Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /items` - Get all items
- `POST /items` - Create new item
- `GET /items/{id}` - Get specific item
'''
        }
    elif project_type == "flask":
        return {
            "app.py": '''from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from typing import List, Dict, Any

app = Flask(__name__)
CORS(app)

# In-memory storage (replace with database)
items: List[Dict[str, Any]] = []

@app.route('/')
def root():
    return jsonify({"message": "Welcome to the Flask API"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    item = {
        "id": len(items) + 1,
        "name": data['name'],
        "description": data.get('description', '')
    }
    items.append(item)
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int):
    for item in items:
        if item['id'] == item_id:
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''',
            "requirements.txt": '''Flask==3.0.0
Flask-CORS==4.0.0
''',
            "test_app.py": '''import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Welcome to the Flask API"

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == "healthy"

def test_create_and_get_item(client):
    # Create item
    item_data = {"name": "Test Item", "description": "Test Description"}
    response = client.post('/items', 
                          data=json.dumps(item_data),
                          content_type='application/json')
    assert response.status_code == 201
    created_item = json.loads(response.data)
    assert created_item['name'] == "Test Item"
    
    # Get item
    response = client.get(f"/items/{created_item['id']}")
    assert response.status_code == 200
    item = json.loads(response.data)
    assert item == created_item
''',
            "README.md": '''# Flask Project

A simple web API built with Flask.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

## Testing

```bash
pytest test_app.py -v
```

## Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /items` - Get all items
- `POST /items` - Create new item
- `GET /items/<id>` - Get specific item
'''
        }
    else:  # basic Python project
        return {
            "main.py": '''#!/usr/bin/env python3
"""
Main application module.
"""

def main():
    """Main function"""
    print("Hello, World!")
    print("This is a basic Python project.")

if __name__ == "__main__":
    main()
''',
            "requirements.txt": '''# Add your dependencies here
''',
            "test_main.py": '''import pytest
from main import main

def test_main():
    """Test the main function"""
    # This is a basic test - modify as needed
    assert main is not None

def test_basic_functionality():
    """Test basic functionality"""
    result = main()
    assert result is None  # main() doesn't return anything by default
''',
            "README.md": '''# Python Project

A basic Python project.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Testing

```bash
pytest test_main.py -v
```
'''
        }


def get_javascript_templates(project_type: str = "basic") -> Dict[str, str]:
    """JavaScript/Node.js project templates"""
    if project_type == "express":
        return {
            "app.js": '''const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage (replace with database)
let items = [];

// Routes
app.get('/', (req, res) => {
    res.json({ message: 'Welcome to the Express API' });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.get('/items', (req, res) => {
    res.json(items);
});

app.post('/items', (req, res) => {
    const { name, description } = req.body;
    
    if (!name) {
        return res.status(400).json({ error: 'Name is required' });
    }
    
    const item = {
        id: items.length + 1,
        name,
        description: description || ''
    };
    
    items.push(item);
    res.status(201).json(item);
});

app.get('/items/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const item = items.find(item => item.id === id);
    
    if (!item) {
        return res.status(404).json({ error: 'Item not found' });
    }
    
    res.json(item);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
''',
            "package.json": '''{
  "name": "express-api",
  "version": "1.0.0",
  "description": "Express API project",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "supertest": "^6.3.3",
    "nodemon": "^3.0.2"
  },
  "jest": {
    "testEnvironment": "node"
  }
}''',
            "app.test.js": '''const request = require('supertest');
const app = require('./app');

describe('Express API', () => {
    test('GET / should return welcome message', async () => {
        const response = await request(app)
            .get('/')
            .expect(200);
        
        expect(response.body.message).toBe('Welcome to the Express API');
    });

    test('GET /health should return healthy status', async () => {
        const response = await request(app)
            .get('/health')
            .expect(200);
        
        expect(response.body.status).toBe('healthy');
    });

    test('POST /items should create a new item', async () => {
        const itemData = { name: 'Test Item', description: 'Test Description' };
        
        const response = await request(app)
            .post('/items')
            .send(itemData)
            .expect(201);
        
        expect(response.body.name).toBe('Test Item');
        expect(response.body.id).toBe(1);
    });

    test('GET /items should return all items', async () => {
        const response = await request(app)
            .get('/items')
            .expect(200);
        
        expect(Array.isArray(response.body)).toBe(true);
    });
});
''',
            "README.md": '''# Express API Project

A RESTful API built with Express.js.

## Installation

```bash
npm install
```

## Running

Development mode:
```bash
npm run dev
```

Production mode:
```bash
npm start
```

## Testing

```bash
npm test
```

## Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /items` - Get all items
- `POST /items` - Create new item
- `GET /items/:id` - Get specific item
'''
        }
    else:  # basic Node.js project
        return {
            "index.js": '''#!/usr/bin/env node

console.log('Hello, World!');
console.log('This is a basic Node.js project.');

// Example function
function greet(name) {
    return `Hello, ${name}!`;
}

// Export for testing
module.exports = { greet };
''',
            "package.json": '''{
  "name": "nodejs-project",
  "version": "1.0.0",
  "description": "Basic Node.js project",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  },
  "devDependencies": {
    "jest": "^29.7.0"
  },
  "jest": {
    "testEnvironment": "node"
  }
}''',
            "index.test.js": '''const { greet } = require('./index');

describe('Basic functionality', () => {
    test('greet function should return greeting', () => {
        const result = greet('World');
        expect(result).toBe('Hello, World!');
    });

    test('greet function should handle different names', () => {
        const result = greet('Alice');
        expect(result).toBe('Hello, Alice!');
    });
});
''',
            "README.md": '''# Node.js Project

A basic Node.js project.

## Installation

```bash
npm install
```

## Running

```bash
npm start
```

## Testing

```bash
npm test
```
'''
        }


def get_typescript_templates(project_type: str = "basic") -> Dict[str, str]:
    """TypeScript project templates"""
    if project_type == "react" or project_type == "react-app":
        return {
            "src/index.tsx": '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''',
            "src/App.tsx": '''import React, { useState, useEffect } from 'react';
import './App.css';
import UserDashboard from './components/UserDashboard';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setUser({
        id: 1,
        name: 'John Doe',
        email: 'john.doe@example.com',
        role: 'Admin'
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>User Dashboard</h1>
      </header>
      <main>
        {user && <UserDashboard user={user} />}
      </main>
    </div>
  );
};

export default App;
''',
            "src/components/UserDashboard.tsx": '''import React from 'react';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface UserDashboardProps {
  user: User;
}

const UserDashboard: React.FC<UserDashboardProps> = ({ user }) => {
  return (
    <div className="user-dashboard">
      <div className="user-card">
        <h2>Welcome, {user.name}!</h2>
        <div className="user-info">
          <p><strong>ID:</strong> {user.id}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Role:</strong> {user.role}</p>
        </div>
      </div>
      
      <div className="dashboard-actions">
        <button className="btn btn-primary">Edit Profile</button>
        <button className="btn btn-secondary">View Settings</button>
        <button className="btn btn-info">Help & Support</button>
      </div>
      
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Active Sessions</h3>
          <p>2</p>
        </div>
        <div className="stat-card">
          <h3>Last Login</h3>
          <p>Today, 2:30 PM</p>
        </div>
        <div className="stat-card">
          <h3>Account Status</h3>
          <p>Active</p>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
''',
            "src/App.css": '''.App {
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
  margin-bottom: 20px;
  border-radius: 8px;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 18px;
}

.user-dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.user-card {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info p {
  margin: 8px 0;
  text-align: left;
}

.dashboard-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-info {
  background-color: #17a2b8;
  color: white;
}

.btn:hover {
  opacity: 0.8;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.stat-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}

.stat-card p {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
  color: #007bff;
}
''',
            "src/index.css": '''body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f8f9fa;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}

* {
  box-sizing: border-box;
}
''',
            "public/index.html": '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="TypeScript React User Dashboard" />
    <title>User Dashboard</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
''',
            "package.json": '''{
  "name": "typescript-react-dashboard",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^4.9.5"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^14.4.3",
    "react-scripts": "5.0.1"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}''',
            "tsconfig.json": '''{
  "compilerOptions": {
    "target": "es5",
    "lib": [
      "dom",
      "dom.iterable",
      "es6"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": [
    "src"
  ]
}''',
            "src/components/UserDashboard.test.tsx": '''import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import UserDashboard from './UserDashboard';

const mockUser = {
  id: 1,
  name: 'John Doe',
  email: 'john.doe@example.com',
  role: 'Admin'
};

describe('UserDashboard', () => {
  test('renders user information correctly', () => {
    render(<UserDashboard user={mockUser} />);
    
    expect(screen.getByText('Welcome, John Doe!')).toBeInTheDocument();
    expect(screen.getByText('john.doe@example.com')).toBeInTheDocument();
    expect(screen.getByText('Admin')).toBeInTheDocument();
  });

  test('renders dashboard actions', () => {
    render(<UserDashboard user={mockUser} />);
    
    expect(screen.getByText('Edit Profile')).toBeInTheDocument();
    expect(screen.getByText('View Settings')).toBeInTheDocument();
    expect(screen.getByText('Help & Support')).toBeInTheDocument();
  });

  test('renders dashboard stats', () => {
    render(<UserDashboard user={mockUser} />);
    
    expect(screen.getByText('Active Sessions')).toBeInTheDocument();
    expect(screen.getByText('Last Login')).toBeInTheDocument();
    expect(screen.getByText('Account Status')).toBeInTheDocument();
  });
});
''',
            "README.md": '''# TypeScript React User Dashboard

A modern user dashboard application built with React and TypeScript.

## Features

- User profile display
- Dashboard statistics
- Responsive design
- TypeScript for type safety
- Testing with Jest and React Testing Library

## Installation

```bash
npm install
```

## Development

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Testing

```bash
npm test
```

## Building

```bash
npm run build
```

## Project Structure

```
src/
  components/          # React components
    UserDashboard.tsx  # Main dashboard component
  App.tsx             # Main App component
  index.tsx           # Application entry point
  App.css             # App styles
  index.css           # Global styles
public/
  index.html          # HTML template
```

## Technologies Used

- React 18
- TypeScript
- CSS3
- Jest & React Testing Library
'''
        }
    
    return {
        "src/index.ts": '''#!/usr/bin/env node

interface Person {
    name: string;
    age: number;
}

function greet(person: Person): string {
    return `Hello, ${person.name}! You are ${person.age} years old.`;
}

function main(): void {
    console.log('Hello, TypeScript World!');
    
    const person: Person = { name: 'Alice', age: 30 };
    console.log(greet(person));
}

// Export for testing
export { greet, Person };

// Run if this is the main module
if (require.main === module) {
    main();
}
''',
        "package.json": '''{
  "name": "typescript-project",
  "version": "1.0.0",
  "description": "TypeScript project",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "test": "jest",
    "clean": "rm -rf dist"
  },
  "devDependencies": {
    "@types/jest": "^29.5.8",
    "@types/node": "^20.9.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.1",
    "ts-node": "^10.9.1",
    "typescript": "^5.2.2"
  },
  "jest": {
    "preset": "ts-jest",
    "testEnvironment": "node",
    "roots": ["<rootDir>/src", "<rootDir>/tests"]
  }
}''',
        "tsconfig.json": '''{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}''',
        "tests/index.test.ts": '''import { greet, Person } from '../src/index';

describe('TypeScript functionality', () => {
    test('greet function should return proper greeting', () => {
        const person: Person = { name: 'Bob', age: 25 };
        const result = greet(person);
        expect(result).toBe('Hello, Bob! You are 25 years old.');
    });

    test('greet function should handle different persons', () => {
        const person: Person = { name: 'Alice', age: 30 };
        const result = greet(person);
        expect(result).toBe('Hello, Alice! You are 30 years old.');
    });
});
''',
        "README.md": '''# TypeScript Project

A basic TypeScript project with proper build setup.

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Building

```bash
npm run build
```

## Running

```bash
npm start
```

## Testing

```bash
npm test
```

## Structure

- `src/` - TypeScript source files
- `dist/` - Compiled JavaScript files
- `tests/` - Test files
'''
    }


def get_csharp_templates(project_type: str = "basic") -> Dict[str, str]:
    """C# project templates"""
    if project_type == "webapi":
        return {
            "Program.cs": '''using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;

namespace WebApiProject
{
    public class Program
    {
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}
''',
            "Startup.cs": '''using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace WebApiProject
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllers();
            services.AddCors(options =>
            {
                options.AddDefaultPolicy(builder =>
                {
                    builder.AllowAnyOrigin()
                           .AllowAnyMethod()
                           .AllowAnyHeader();
                });
            });
        }

        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseRouting();
            app.UseCors();
            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}
''',
            "Controllers/ItemsController.cs": '''using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Linq;

namespace WebApiProject.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ItemsController : ControllerBase
    {
        private static List<Item> _items = new List<Item>();

        [HttpGet]
        public ActionResult<IEnumerable<Item>> GetItems()
        {
            return Ok(_items);
        }

        [HttpGet("{id}")]
        public ActionResult<Item> GetItem(int id)
        {
            var item = _items.FirstOrDefault(x => x.Id == id);
            if (item == null)
            {
                return NotFound();
            }
            return Ok(item);
        }

        [HttpPost]
        public ActionResult<Item> CreateItem(CreateItemRequest request)
        {
            var item = new Item
            {
                Id = _items.Count + 1,
                Name = request.Name,
                Description = request.Description
            };
            
            _items.Add(item);
            return CreatedAtAction(nameof(GetItem), new { id = item.Id }, item);
        }
    }

    public class Item
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
    }

    public class CreateItemRequest
    {
        public string Name { get; set; }
        public string Description { get; set; }
    }
}
''',
            "WebApiProject.csproj": '''<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.App" />
  </ItemGroup>

</Project>
''',
            "README.md": '''# ASP.NET Core Web API Project

A RESTful API built with ASP.NET Core.

## Running

```bash
dotnet run
```

## Testing

```bash
dotnet test
```

## Endpoints

- `GET /api/items` - Get all items
- `GET /api/items/{id}` - Get specific item
- `POST /api/items` - Create new item
'''
        }
    else:  # basic console app
        return {
            "Program.cs": '''using System;

namespace ConsoleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, C# World!");
            
            var person = new Person("Alice", 30);
            Console.WriteLine(person.Greet());
        }
    }

    public class Person
    {
        public string Name { get; }
        public int Age { get; }

        public Person(string name, int age)
        {
            Name = name;
            Age = age;
        }

        public string Greet()
        {
            return $"Hello, my name is {Name} and I am {Age} years old.";
        }
    }
}
''',
            "ConsoleApp.csproj": '''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

</Project>
''',
            "README.md": '''# C# Console Application

A basic C# console application.

## Running

```bash
dotnet run
```

## Building

```bash
dotnet build
```
'''
        }


def get_java_templates(project_type: str = "basic") -> Dict[str, str]:
    """Java project templates"""
    if project_type == "spring":
        return {
            "src/main/java/com/example/Application.java": '''package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
''',
            "src/main/java/com/example/controller/ItemController.java": '''package com.example.controller;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api/items")
@CrossOrigin(origins = "*")
public class ItemController {
    
    private List<Item> items = new ArrayList<>();
    private int nextId = 1;

    @GetMapping
    public List<Item> getAllItems() {
        return items;
    }

    @GetMapping("/{id}")
    public Item getItem(@PathVariable int id) {
        return items.stream()
                .filter(item -> item.getId() == id)
                .findFirst()
                .orElse(null);
    }

    @PostMapping
    public Item createItem(@RequestBody CreateItemRequest request) {
        Item item = new Item(nextId++, request.getName(), request.getDescription());
        items.add(item);
        return item;
    }
}

class Item {
    private int id;
    private String name;
    private String description;

    public Item(int id, String name, String description) {
        this.id = id;
        this.name = name;
        this.description = description;
    }

    // Getters and setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}

class CreateItemRequest {
    private String name;
    private String description;

    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
''',
            "pom.xml": '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>spring-boot-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
''',
            "README.md": '''# Spring Boot Application

A RESTful API built with Spring Boot.

## Running

```bash
mvn spring-boot:run
```

## Building

```bash
mvn clean package
```

## Testing

```bash
mvn test
```

## Endpoints

- `GET /api/items` - Get all items
- `GET /api/items/{id}` - Get specific item
- `POST /api/items` - Create new item
'''
        }
    else:  # basic Java app
        return {
            "src/main/java/Main.java": '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java World!");
        
        Person person = new Person("Alice", 30);
        System.out.println(person.greet());
    }
}

class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String greet() {
        return "Hello, my name is " + name + " and I am " + age + " years old.";
    }

    // Getters
    public String getName() { return name; }
    public int getAge() { return age; }
}
''',
            "pom.xml": '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>java-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
''',
            "README.md": '''# Java Application

A basic Java application.

## Running

```bash
mvn compile exec:java -Dexec.mainClass="Main"
```

## Building

```bash
mvn compile
```

## Testing

```bash
mvn test
```
'''
        }


def get_go_templates(project_type: str = "basic") -> Dict[str, str]:
    """Go project templates"""
    if project_type == "api":
        return {
            "main.go": '''package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
    Status  string `json:"status"`
}

func main() {
    // Set up routes
    http.HandleFunc("/", homeHandler)
    http.HandleFunc("/health", healthHandler)
    http.HandleFunc("/api/hello", helloHandler)
    
    fmt.Println("Go server starting on :8080")
    fmt.Println("Routes available:")
    fmt.Println("  GET  /          - Home page")
    fmt.Println("  GET  /health    - Health check")  
    fmt.Println("  GET  /api/hello - Hello API")
    
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    response := Response{
        Message: "Welcome to Go Web Server",
        Status:  "running",
    }
    json.NewEncoder(w).Encode(response)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    response := Response{
        Status: "healthy",
    }
    json.NewEncoder(w).Encode(response)
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    response := Response{
        Message: "Hello from Go API!",
        Status:  "success",
    }
    json.NewEncoder(w).Encode(response)
}
''',
            "go.mod": '''module go-server

go 1.21
''',
            "main_test.go": '''package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHomeHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(homeHandler)
    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }

    var response Response
    err = json.Unmarshal(rr.Body.Bytes(), &response)
    if err != nil {
        t.Fatal(err)
    }
    
    if response.Message != "Welcome to Go Web Server" {
        t.Errorf("handler returned unexpected message: got %v", response.Message)
    }
}

func TestHealthHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/health", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(healthHandler)
    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }
}
''',
            "README.md": '''# Go Web Server

A simple Go web server with routing using the standard library.

## Installation

```bash
go mod tidy
```

## Running

```bash
go run main.go
```

## Testing

```bash
go test -v
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /api/hello` - Hello API endpoint

## Example Usage

```bash
# Test the server
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/api/hello
```
'''
        }
    elif project_type == "web":
        return {
            "main.go": '''package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "strconv"

    "github.com/gorilla/mux"
)

type Item struct {
    ID          int    `json:"id"`
    Name        string `json:"name"`
    Description string `json:"description"`
}

type CreateItemRequest struct {
    Name        string `json:"name"`
    Description string `json:"description"`
}

var items []Item
var nextID = 1

func main() {
    r := mux.NewRouter()

    // Enable CORS
    r.Use(func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            w.Header().Set("Access-Control-Allow-Origin", "*")
            w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
            
            if r.Method == "OPTIONS" {
                return
            }
            
            next.ServeHTTP(w, r)
        })
    })

    r.HandleFunc("/", homeHandler).Methods("GET")
    r.HandleFunc("/health", healthHandler).Methods("GET")
    r.HandleFunc("/items", getItemsHandler).Methods("GET")
    r.HandleFunc("/items", createItemHandler).Methods("POST")
    r.HandleFunc("/items/{id}", getItemHandler).Methods("GET")

    fmt.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", r))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"message": "Welcome to the Go API"})
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}

func getItemsHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(items)
}

func createItemHandler(w http.ResponseWriter, r *http.Request) {
    var req CreateItemRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    if req.Name == "" {
        http.Error(w, "Name is required", http.StatusBadRequest)
        return
    }

    item := Item{
        ID:          nextID,
        Name:        req.Name,
        Description: req.Description,
    }
    nextID++
    items = append(items, item)

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(item)
}

func getItemHandler(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    id, err := strconv.Atoi(vars["id"])
    if err != nil {
        http.Error(w, "Invalid ID", http.StatusBadRequest)
        return
    }

    for _, item := range items {
        if item.ID == id {
            w.Header().Set("Content-Type", "application/json")
            json.NewEncoder(w).Encode(item)
            return
        }
    }

    http.Error(w, "Item not found", http.StatusNotFound)
}
''',
            "go.mod": '''module go-web-app

go 1.21

require (
    github.com/gorilla/mux v1.8.1
)
''',
            "main_test.go": '''package main

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/gorilla/mux"
)

func TestHomeHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(homeHandler)
    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }

    var response map[string]string
    json.Unmarshal(rr.Body.Bytes(), &response)
    
    if response["message"] != "Welcome to the Go API" {
        t.Errorf("handler returned unexpected body: got %v want %v", response["message"], "Welcome to the Go API")
    }
}

func TestHealthHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/health", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(healthHandler)
    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }
}
''',
            "README.md": '''# Go Web Application

A RESTful API built with Go and Gorilla Mux.

## Installation

```bash
go mod tidy
```

## Running

```bash
go run main.go
```

## Testing

```bash
go test
```

## Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /items` - Get all items
- `POST /items` - Create new item
- `GET /items/{id}` - Get specific item
'''
        }
    else:  # basic Go app
        return {
            "main.go": '''package main

import "fmt"

func main() {
    fmt.Println("Hello, Go World!")
    
    person := Person{Name: "Alice", Age: 30}
    fmt.Println(person.Greet())
}

type Person struct {
    Name string
    Age  int
}

func (p Person) Greet() string {
    return fmt.Sprintf("Hello, my name is %s and I am %d years old.", p.Name, p.Age)
}
''',
            "go.mod": '''module basic-go-app

go 1.21
''',
            "main_test.go": '''package main

import "testing"

func TestPersonGreet(t *testing.T) {
    person := Person{Name: "Bob", Age: 25}
    expected := "Hello, my name is Bob and I am 25 years old."
    
    if got := person.Greet(); got != expected {
        t.Errorf("Person.Greet() = %v, want %v", got, expected)
    }
}
''',
            "README.md": '''# Go Application

A basic Go application.

## Running

```bash
go run main.go
```

## Testing

```bash
go test
```

## Building

```bash
go build
```
'''
        }


def get_rust_templates(project_type: str = "basic") -> Dict[str, str]:
    """Rust project templates"""
    return {
        "src/main.rs": '''fn main() {
    println!("Hello, Rust World!");
    
    let person = Person::new("Alice".to_string(), 30);
    println!("{}", person.greet());
}

struct Person {
    name: String,
    age: u32,
}

impl Person {
    fn new(name: String, age: u32) -> Self {
        Person { name, age }
    }
    
    fn greet(&self) -> String {
        format!("Hello, my name is {} and I am {} years old.", self.name, self.age)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_person_greet() {
        let person = Person::new("Bob".to_string(), 25);
        let expected = "Hello, my name is Bob and I am 25 years old.";
        assert_eq!(person.greet(), expected);
    }
}
''',
        "Cargo.toml": '''[package]
name = "rust-app"
version = "0.1.0"
edition = "2021"

[dependencies]
''',
        "README.md": '''# Rust Application

A basic Rust application.

## Running

```bash
cargo run
```

## Testing

```bash
cargo test
```

## Building

```bash
cargo build --release
```
'''
    }


def get_php_templates(project_type: str = "basic") -> Dict[str, str]:
    """PHP project templates"""
    return {
        "index.php": '''<?php

class Person {
    private $name;
    private $age;
    
    public function __construct($name, $age) {
        $this->name = $name;
        $this->age = $age;
    }
    
    public function greet() {
        return "Hello, my name is {$this->name} and I am {$this->age} years old.";
    }
}

echo "Hello, PHP World!\\n";

$person = new Person("Alice", 30);
echo $person->greet() . "\\n";

?>
''',
        "composer.json": '''{
    "name": "php-project",
    "description": "Basic PHP project",
    "type": "project",
    "require": {
        "php": ">=8.0"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0"
    },
    "autoload": {
        "psr-4": {
            "App\\\\": "src/"
        }
    }
}''',
        "README.md": '''# PHP Project

A basic PHP project.

## Installation

```bash
composer install
```

## Running

```bash
php index.php
```

## Testing

```bash
vendor/bin/phpunit
```
'''
    }


def get_ruby_templates(project_type: str = "basic") -> Dict[str, str]:
    """Ruby project templates"""
    return {
        "main.rb": '''#!/usr/bin/env ruby

class Person
  attr_reader :name, :age
  
  def initialize(name, age)
    @name = name
    @age = age
  end
  
  def greet
    "Hello, my name is #{@name} and I am #{@age} years old."
  end
end

puts "Hello, Ruby World!"

person = Person.new("Alice", 30)
puts person.greet
''',
        "Gemfile": '''source 'https://rubygems.org'

ruby '3.0.0'

gem 'rspec', '~> 3.10', group: :test
''',
        "spec/main_spec.rb": '''require_relative '../main'

RSpec.describe Person do
  describe '#greet' do
    it 'returns a proper greeting' do
      person = Person.new('Bob', 25)
      expect(person.greet).to eq('Hello, my name is Bob and I am 25 years old.')
    end
  end
end
''',
        "README.md": '''# Ruby Project

A basic Ruby project.

## Installation

```bash
bundle install
```

## Running

```bash
ruby main.rb
```

## Testing

```bash
rspec
```
'''
    }


def get_generic_templates(language: str, project_type: str = "basic") -> Dict[str, str]:
    """Generic templates for unsupported languages"""
    return {
        "README.md": f'''# {language.title()} Project

A basic {language} project.

## Getting Started

This is a {language} project. Please refer to the {language} documentation for specific setup and build instructions.

## Project Type

This project is set up as a {project_type} {language} application.
''',
        "main.txt": f'''// This is a {language} project file
// Add your {language} code here

// Project type: {project_type}
// Language: {language}
'''
    }
