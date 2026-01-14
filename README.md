# SAM: Context-Aware Offline AI Companion

**Tagline:** A privacy-first, multi-persona local LLM orchestrator featuring scheduled check-ins and expressive TTS.

## Overview

AuraLocal (SAM) is a cross-platform desktop utility that acts as a proactive AI companion. It runs 100% locally, ensuring data sovereignty. Key features include:

- **Proactive Engagement:** Scheduled "How was your day?" check-ins.
- **Dynamic Persona Switching:** Switch between "Therapist", "Friend", etc.
- **Expressive TTS:** Emotional voice synthesis.

## Prerequisites

### 1. Install Ollama

This project requires [Ollama](https://ollama.com/) to run local LLMs.

**Windows:**

1. Download the Ollama installer from the [official website](https://ollama.com/download/windows).
2. Run the installer.
3. Open a terminal (PowerShell or Command Prompt) and verify installation:

    ```powershell
    ollama --version
    ```

### 2. Pull Required Models

We recommend `llama3.2` for balanced performance or `mistral-nemo` for better reasoning.

```powershell
ollama pull llama3.2
# OR
ollama pull mistral-nemo
```

Ensure the model is running (Ollama usually starts a background service):

```powershell
ollama serve
```

*Note: The default API port is 11434.*

## Project Setup

### 1. Clone/Open the Repository

Navigate to the project directory:

```powershell
cd e:/Codes/SAM/Sam
```

### 2. Create a Virtual Environment

It's recommended to use a Python virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Running the Application

### Backend

Start the FastAPI server:

```powershell
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`.
You can view the interactive testing docs at `http://localhost:8000/docs`.

### Extension

(Instructions coming in Phase 3)

## Architecture

- **Backend:** Python/FastAPI
- **LLM Engine:** Ollama (via API)
- **Frontend:** Chrome/Edge Extension
