# 🖼️ ImageFlow Pro - Advanced Image Processing Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A full-stack image processing platform with modern web interface**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Usage](#-usage) • [Troubleshooting](#-troubleshooting)

</div>

## 📋 Overview

ImageFlow Pro is a comprehensive image processing application featuring a Streamlit frontend and FastAPI backend. It provides professional-grade image manipulation tools with real-time preview and advanced analytics.

### ✨ Key Highlights
- **Real-time Processing**: Instant preview of all operations
- **Modular Architecture**: Clean separation of concerns with domain-driven design
- **Comprehensive Image Processing**: Full suite of filters and transformations including cropping
- **Advanced Analytics**: Interactive histograms and statistical analysis
- **Modern UI**: Beautiful, responsive Streamlit interface
- **RESTful API**: Well-documented FastAPI endpoints with automatic OpenAPI documentation
- **Session Management**: Persistent state and processing history tracking
- **Image Cropping**: Interactive cropping tool with preset aspect ratios

## 🏗️ Project Structure
```
App_Web_Image/
│
├── 📦 pyproject.toml                 # Project dependencies & metadata
├── 📄 README.md                      # Documentation (this file)
├── 📄 SUMMARY.txt                    # Project summary & implementation details
├── 🔒 .gitignore                     # Git ignore rules
├── 🐍 .python-version                # Python version specification
│
├── 🔧 backend/                       # FastAPI Backend Server
│   ├── __init__.py
│   └── app/
│       ├── 🏃 main.py                # FastAPI application entry point
│       ├── 📋 requirements.txt       # Backend dependencies
│       ├── __init__.py
│       │
│       ├── 🔌 api/                   # API Layer
│       │   ├── __init__.py
│       │   ├── 🎯 preprocess.py      # Image processing endpoints
│       │   │   ├─ POST /preprocess   # Main image processing
│       │   │   ├─ POST /crop         # Image cropping endpoint
│       │   │   └─ Filters & transforms
│       │   └── ⚙️ dependencies.py    # Dependency injection & middleware
│       │
│       ├── 📊 domain/                # Domain Layer (DDD principles)
│       │   ├── __init__.py
│       │   ├── 📜 interfaces.py      # Abstract interfaces & contracts
│       │   │   └─ IImageProcessor
│       │   └── 📦 models.py          # Data models & schemas
│       │       ├─ ImageProcessingParams
│       │       ├─ ProcessingResult
│       │       └─ Filter configurations
│       │
│       ├── 🏗️ infrastructure/        # Infrastructure Layer
│       │   ├── __init__.py
│       │   └── 🖼️ image_processor.py # Core image processing logic
│       │       ├─ crop_image()       # Cropping implementation
│       │       ├─ apply_filters()    # Filter application
│       │       ├─ apply_blur()
│       │       ├─ apply_edge_detection()
│       │       ├─ color_space_conversion()
│       │       ├─ geometric_transform()
│       │       └─ adjust_brightness_contrast()
│       │
│       └── 🎯 core/                  # Core Module
│           └── __init__.py           # Shared kernel code
│
├── 🎨 frontend/                      # Streamlit Frontend Application
│   ├── 🏃 app.py                     # Main Streamlit application
│   ├── 📋 requirements.txt           # Frontend dependencies
│   │
│   ├── 🧩 components/                # Reusable UI Components
│   │   ├── __init__.py
│   │   ├── 📤 upload_image.py        # Image upload interface
│   │   ├── 🖼️ image_view.py          # Image display & preview tabs
│   │   │   ├─ Image display
│   │   │   ├─ Filters tab
│   │   │   ├─ Cropping tab ✂️
│   │   │   ├─ Transformations tab
│   │   │   └─ Analytics tab
│   │   ├── ✂️ crop.py                # Cropping component
│   │   │   ├─ render_crop_preview()
│   │   │   ├─ Sliders (X, Y, Width, Height)
│   │   │   ├─ Preset buttons (1:1, 16:9, 9:16, 4:3)
│   │   │   └─ Apply/Reset actions
│   │   ├── 🎨 sidebar.py             # Sidebar controls
│   │   ├── 📚 gallery.py             # Image gallery display
│   │   └── ⏱️ history.py             # Processing history & undo/redo
│   │
│   ├── 🔗 services/                  # Backend Communication
│   │   ├── __init__.py
│   │   └── 🌐 api_client.py          # Backend API client
│   │       ├─ API_BASE_URL
│   │       ├─ API_ENDPOINTS
│   │       ├─ preprocess_image()
│   │       ├─ crop_image()
│   │       └─ Error handling
│   │
│   ├── 🎨 styles/                    # UI Styling & Theming
│   │   ├── __init__.py
│   │   └── 🖌️ styles.py              # CSS styling
│   │       ├─ Custom colors
│   │       ├─ Component styling
│   │       ├─ Responsive design
│   │       └─ Animations
│   │
│   └── 🛠️ utils/                     # Utility Functions
│       ├── __init__.py
│       ├── 🔧 helpers.py             # Helper functions
│       ├── 💾 state.py               # Session state management
│       │   └─ init_session_state()
│       └── 📊 visualization.py       # Data visualization utilities
│           └─ Histogram, charts, etc.
│
└── 📁 .venv/                         # Virtual environment (auto-managed by uv)
```
##  Architecture

### Backend Architecture (Domain-Driven Design)
The backend follows **Domain-Driven Design (DDD)** principles with clear separation of concerns:

```
Request Flow: HTTP Request → API Layer → Domain Layer → Infrastructure Layer → Image Processing
```

- **`api/`** - HTTP layer handling requests and routing
  - `preprocess.py` - All image processing endpoints
  - `dependencies.py` - Dependency injection and middleware

- **`domain/`** - Business logic and contracts
  - `interfaces.py` - Abstract contracts (e.g., `IImageProcessor`)
  - `models.py` - Data models and request/response schemas

- **`infrastructure/`** - Implementation of business logic
  - `image_processor.py` - Core image processing functions using OpenCV, PIL, NumPy

- **`core/`** - Shared utilities and kernel code

### Frontend Architecture (Streamlit MVC-like)
The frontend is organized by functional domains:

```
User Interface → Components → Services → Backend API
```

- **`components/`** - Modular UI components
  - `upload_image.py` - Image upload interface
  - `image_view.py` - Main image viewer with multiple processing tabs
  - `crop.py` - Interactive image cropping tool
  - `sidebar.py` - Control panel
  - `gallery.py` - Processed images history
  - `history.py` - Undo/Redo management

- **`services/`** - Backend communication
  - `api_client.py` - HTTP client for FastAPI backend

- **`styles/`** - UI customization
  - `styles.py` - Custom CSS and theme configuration

- **`utils/`** - Helper functions and state management
  - `state.py` - Session state initialization
  - `helpers.py` - Utility functions
  - `visualization.py` - Chart and histogram rendering

## 🚀 Features

### Image Processing Capabilities
- **Image Cropping** ✂️
  - Interactive cropping with coordinate sliders
  - Preset aspect ratios (1:1, 16:9, 9:16, 4:3)
  - Real-time preview with selection overlay
  - Adjustable crop area and dimensions

- **Color Space Conversions**: RGB, Grayscale, HSV, and more
- **Filtering Operations**: Blur, Sharpen, Edge Detection, Morphological operations
- **Geometric Transformations**: Rotation, Scaling, Flipping, Perspective transforms
- **Enhancement**: Brightness, Contrast, Saturation, Sharpness, Gamma correction adjustments
- **Morphological Operations**: Erosion, Dilation, Opening, Closing
- **Thresholding**: Binary, Otsu, Adaptive threshold methods
- **Statistical Analysis**: Histogram generation, image statistics

### User Interface
- **Image Upload & Gallery**: Drag-and-drop interface with history
- **Real-time Preview**: Instant processing results with side-by-side comparison
- **Multiple Processing Tabs**:
  - 📊 Image Information (metadata, histograms)
  - ✂️ Cropping (interactive cropping tool)
  - 🎨 Filters (color, blur, edge detection)
  - 🔄 Transformations (rotation, scaling, flipping)
  - 📈 Analytics (statistical analysis and charts)
- **Processing History**: Track all operations with Undo/Redo functionality
- **Session State Management**: Persistent application state across interactions
- **Data Visualization**: Interactive histograms, charts, and statistical displays

##  Quick Installation

### Prerequisites
- **Python 3.8 or higher** (Python 3.10+ recommended)
- **Git** (for cloning the repository)
- **uv** (fast Python package manager - recommended)
  - Install on Windows: `pipx install uv` (or `pip install uv`)
  - Install on macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/EyaHaddad/app-web-image.git
cd app-web-image

# Create virtual environment and install dependencies
# uv automatically creates and manages .venv
uv sync
```

### 2. Launch the Application

You need **two terminal windows** for simultaneous execution:

**Terminal 1 - Start the Backend API Server:**
```bash
# Navigate to project directory
cd App_Web_Image

# Start FastAPI backend with auto-reload
uv run uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ API available at: **http://localhost:8000**
- Interactive API Docs (Swagger): **http://localhost:8000/docs**
- Alternative API Docs (ReDoc): **http://localhost:8000/redoc**

**Terminal 2 - Start the Frontend Application:**
```bash
# Navigate to project directory  
cd App_Web_Image

# Start Streamlit frontend
uv run streamlit run frontend/app.py
```
**Expected output:**
```
Local URL: http://localhost:8501
Network URL: http://xxx.xxx.x.x:8501
```

✅ Frontend available at: **http://localhost:8501**

### 3. Verify Installation

1. **Backend is running** if you can access:
   - http://localhost:8000/docs (Swagger UI should load)

2. **Frontend is running** if you can access:
   - http://localhost:8501 (Streamlit app should load)

3. **Both are working together** if you can:
   - Upload an image
   - Apply filters and see real-time results
   - Use the cropping tool with instant preview

### Important Notes
- `uv sync` creates and manages the `.venv` automatically
- Use `uv run <command>` to execute tools in the managed environment
- **Both backend and frontend must be running** for full functionality
- If ports 8000 or 8501 are in use, you can specify different ones:
  ```bash
  # Backend on different port
  uv run uvicorn backend.app.main:app --reload --port 8001
  
  # Frontend on different port
  uv run streamlit run frontend/app.py --server.port 8502
  ```

## 💡 Usage Guide

### Basic Workflow
1. **Upload Image**: Start with the upload interface on the home page
2. **Select Operation**: Choose from available tabs:
   - 📊 **Image Info** - View metadata and statistics
   - ✂️ **Cropping** - Crop image with interactive tools
   - 🎨 **Filters** - Apply color, blur, or edge detection
   - 🔄 **Transformations** - Rotate, scale, or flip
   - 📈 **Analytics** - Analyze image statistics
3. **Preview Results**: See real-time preview of changes
4. **Undo/Redo**: Use history to go back/forward
5. **Export**: Download processed image

### Cropping Tool Example
```
1. Upload an image
2. Go to "✂️ Cropping" tab
3. Adjust X, Y, Width, Height sliders OR use preset buttons:
   - 🟩 Square (1:1)
   - 🎬 Cinema (16:9)
   - 📱 Portrait (9:16)
   - 🖼️ Classic (4:3)
4. See preview with selection overlay
5. Click "Apply Crop" to execute
```

## 🔧 API Endpoints

### Main Endpoints
- **POST** `/preprocess` - Process image with various transformations
  ```json
  {
    "file": "image.jpg",
    "grayscale": false,
    "blur_type": "gaussian",
    "blur_kernel": 5,
    "brightness": 10,
    "contrast": 1.2
  }
  ```

- **POST** `/crop` - Crop image
  ```json
  {
    "file": "image.jpg",
    "x": 100,
    "y": 100,
    "width": 300,
    "height": 300
  }
  ```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing & Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port already in use | Change port with `--port 8001` flag |
| Module not found | Run `uv sync` to install dependencies |
| Backend not responding | Verify backend is running on http://localhost:8000/docs |
| Images not processing | Check image format (JPEG, PNG, BMP, etc.) |
| Out of memory | Reduce image size before upload |
| CORS errors | Ensure backend allows frontend origin |

### Verification Checklist
- [ ] Backend API running at `http://localhost:8000`
- [ ] Frontend app running at `http://localhost:8501`
- [ ] Can access Swagger docs at `/docs`
- [ ] Can upload an image successfully
- [ ] Can apply filters with real-time preview
- [ ] Cropping tool works with instant preview

## 📚 Project Files Reference

### Backend Structure
```
backend/app/
├── main.py                   # FastAPI app initialization
├── api/
│   ├── preprocess.py         # Image processing endpoints
│   └── dependencies.py       # Dependency injection
├── domain/
│   ├── interfaces.py         # Abstract contracts
│   └── models.py             # Data models & schemas
├── infrastructure/
│   └── image_processor.py    # Core image processing
└── core/                     # Shared utilities
```

### Frontend Structure
```
frontend/
├── app.py                    # Main Streamlit application
├── components/
│   ├── upload_image.py       # Image upload UI
│   ├── image_view.py         # Image viewer with tabs
│   ├── crop.py               # Cropping tool
│   ├── sidebar.py            # Control panel
│   ├── gallery.py            # Gallery display
│   └── history.py            # History & undo/redo
├── services/
│   └── api_client.py         # Backend HTTP client
├── styles/
│   └── styles.py             # CSS styling
└── utils/
    ├── state.py              # Session state
    ├── helpers.py            # Utility functions
    └── visualization.py      # Charts & histograms
```

## 📖 Additional Documentation
- `SUMMARY.txt` - Implementation summary and project details
- `pyproject.toml` - Dependencies and project metadata

## 🚀 Deployment

### Development Mode (Current)
- Both backend and frontend run locally
- Hot-reload enabled for development
- Perfect for testing and development

### Production Mode (Future)
- Deploy backend to server (e.g., AWS, Heroku)
- Deploy frontend separately
- Use environment variables for configuration
- Enable CORS properly for production

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License
This project is licensed under the MIT License.

## ✨ Acknowledgments
- **FastAPI** - Modern web framework for APIs
- **Streamlit** - Rapid web app development
- **OpenCV** - Computer vision library
- **PIL/Pillow** - Image processing
- **NumPy** - Numerical computing

## 📞 Support
For questions or issues:
1. Check `SUMMARY.txt` for implementation details
2. Review API docs at `http://localhost:8000/docs`
3. Verify both servers are running
4. Check browser console for errors
