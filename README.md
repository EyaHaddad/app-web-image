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
- **Comprehensive Image Processing**: Full suite of filters and transformations
- **Advanced Analytics**: Interactive histograms and statistical analysis
- **Modern UI**: Beautiful, responsive Streamlit interface
- **RESTful API**: Well-documented FastAPI endpoints with automatic OpenAPI documentation
- **Session Management**: Persistent state and processing history tracking

## 🏗️ Project Structure
```
app-web-image/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry point
│   │   ├── requirements.txt
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py       # API dependencies & middleware
│   │   │   └── preprocess.py         # Image preprocessing endpoints
│   │   ├── core/
│   │   │   └── __init__.py           # Core module initialization
│   │   ├── domain/
│   │   │   ├── interfaces.py         # Abstract interfaces & contracts
│   │   │   └── models.py             # Data models & schemas
│   │   └── infrastructure/
│   │       └── image_processor.py    # Core image processing logic
│   └── __pycache__/
├── frontend/                         # Streamlit Frontend
│   ├── app.py                        # Main Streamlit application
│   ├── requirements.txt
│   ├── components/
│   │   ├── gallery.py                # Image gallery component
│   │   ├── history.py                # Processing history component
│   │   ├── image_view.py             # Image display & preview
│   │   └── sidebar.py                # Sidebar UI component
│   ├── services/
│   │   └── api_client.py             # Backend API client
│   ├── styles/
│   │   └── styles.py                 # UI styling & theming
│   └── utils/
│       ├── helpers.py                # Utility functions
│       ├── state.py                  # Session state management
│       └── visualization.py          # Data visualization utilities
├── pyproject.toml                    # Project dependencies & metadata
└── README.md                         # This file
```
##  Architecture

### Backend Architecture
The backend follows **Domain-Driven Design (DDD)** principles:

- **`api/`**: Handles HTTP requests, routing, and preprocessing logic
- **`domain/`**: Contains core business logic and interfaces (contracts)
- **`infrastructure/`**: Implements the actual image processing using OpenCV and NumPy
- **`core/`**: Contains shared kernel code and utilities

### Frontend Architecture
The frontend is built with Streamlit and organized by functionality:

- **`components/`**: Reusable UI components (gallery, history, viewers)
- **`services/`**: Communicates with the backend API
- **`styles/`**: Centralized styling and theming configuration
- **`utils/`**: Helper functions, state management, and visualization tools

## 🚀 Features

### Image Processing Capabilities
- **Color Space Conversions**: RGB, Grayscale, HSV, and more
- **Filtering Operations**: Blur, Sharpen, Edge Detection, etc.
- **Geometric Transformations**: Rotation, Scaling, Perspective transforms
- **Enhancement**: Brightness, Contrast, Saturation adjustments
- **Morphological Operations**: Erosion, Dilation, Opening, Closing
- **Statistical Analysis**: Histogram generation and analysis

### User Interface
- **Image Upload & Gallery**: Drag-and-drop interface for images
- **Real-time Preview**: See processing results instantly
- **Processing History**: Track all operations performed
- **Session State Management**: Persistent application state
- **Data Visualization**: Interactive charts and statistical displays

##  Quick Installation

### Prerequisites
- Python 3.8 or higher
- uv (fast Python package manager)
	- Install on Windows: `pipx install uv` (recommended) or `pip install uv`

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/EyaHaddad/app-web-image.git
cd app-web-image

# Create the virtual environment and install dependencies (managed by uv)
uv sync
```

### 2. Launch the Application

**Terminal 1 - Start the Backend API:**
```bash
uv run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
- API available at: http://localhost:8000
- Interactive API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Terminal 2 - Start the Frontend:**
```bash
uv run streamlit run frontend/app.py
```
- Frontend available at: http://localhost:8501

### Notes
- `uv sync` creates and manages the `.venv` automatically
- Use `uv run <command>` to execute tools inside the managed environment
- Both backend and frontend must be running for full functionality
