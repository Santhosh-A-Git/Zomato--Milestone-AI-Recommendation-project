# Zomato AI-Powered Restaurant Recommendation System

An AI-powered restaurant recommendation service inspired by Zomato. This system intelligently suggests restaurants based on user preferences by combining structured data with a Large Language Model (LLM).

## Features

- **Personalized Recommendations**: Takes user preferences such as location, budget, cuisine, and minimum ratings.
- **LLM Integration**: Leverages Groq LLM API to rank options and generate human-like explanations for why each restaurant fits the user's criteria.
- **Real-World Dataset**: Built on top of a Zomato dataset from Hugging Face.
- **Decoupled Architecture**: 
  - **Backend**: FastAPI-powered Python service for data processing, filtering, and LLM orchestration.
  - **Frontend**: Lightweight frontend using Vite.

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn, Pandas, PyArrow, Groq Python SDK
- **Frontend**: HTML, JavaScript, Vite
- **Deployment**: Railway (Backend), Vercel (Frontend)

## Project Structure

```
├── data/                  # Dataset and processing scripts
├── docs/                  # Documentation and deployment plans
├── frontend/              # Frontend source code (Vite)
├── src/                   # Backend API source code
│   ├── api/               # FastAPI routes and main application
│   ├── engine/            # Recommendation and orchestration logic
│   ├── filters/           # Data filtering logic
│   ├── llm/               # Groq LLM integration
│   └── models/            # Pydantic models for data validation
├── predict.py             # Script for local predictions
├── Procfile               # Production startup command for backend
├── pyproject.toml         # Python project metadata
└── requirements.txt       # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js (for the frontend)
- [Groq API Key](https://console.groq.com/keys)

### Backend Setup

1. **Clone the repository** (if you haven't already).
2. **Navigate to the project root**:
   ```bash
   cd "Zomoto Recommendation system"
   ```
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   - Copy `.env.example` to `.env`
   - Add your Groq API key:
     ```env
     GROQ_API_KEY=your_actual_groq_api_key_here
     ```
5. **Run the FastAPI server**:
   ```bash
   python -m uvicorn src.api.main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```
2. **Install Node dependencies**:
   ```bash
   npm install
   ```
3. **Run the Vite development server**:
   ```bash
   npm run dev
   ```
   The frontend will be available at the URL provided by Vite (usually `http://localhost:5173`).

## Deployment

Detailed deployment instructions for hosting the backend on Railway and the frontend on Vercel can be found in `docs/deployment-plan.md`.

## Dataset

The system uses the [Zomato Restaurant Recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) dataset from Hugging Face. Data processing scripts are included in the `data/` directory to ingest and format the data.
