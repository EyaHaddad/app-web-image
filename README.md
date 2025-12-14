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
- **15+ Filters & Transformations**: Complete image processing toolkit
- **Batch Processing**: Handle multiple images simultaneously
- **Advanced Analytics**: Interactive histograms and statistical analysis
- **Modern UI**: Beautiful, responsive interface with dark/light themes

## 🏗️ Project Structure
```
app-web-image/
├── backend/ # FastAPI Backend
│ ├── app/
│ │ ├── init.py
│ │ ├── main.py # API entry point
│ │ ├── api/
│ │ │ ├── init.py
│ │ │ └── preprocess.py # All endpoints
│ │ └── core/
│ │ ├── init.py
│ │ └── image_utils.py # Processing logic (all fonctions)
│ └── requirements.txt
├── frontend/ # Streamlit Frontend
│ └── app.py # Main application
├
└── README.md # This file
 ```
##  Quick Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/EyaHaddad/app-web-image.git
cd app-web-image

# Create virtual environment for backend
python -m venv .venv

# Activate virtual environment

.venv\Scripts\activate



# Create virtual environment for backend
python -m venv .venv_frontend

# Activate virtual environment

.\.venv_frontend\Scripts\Activate # Create virtual environment for frontend


2. Install Dependencies 
bash
# Install all dependencies  (ven of the backend)
pip install -r backend/requirements.txt




bash
# Install all dependencies (.venv_frontend)
pip install -r frontend/requirements.txt


3. Launch the Application
bash
# Terminal 1 - Start the backend API
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
# API available at: http://localhost:8000
# API Docs: http://localhost:8000/docs

# Terminal 2 - Start the frontend
streamlit run frontend/app.py
# App available at: http://localhost:8501
