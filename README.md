# Multimodal Hospitality Creator

Multimodal Hospitality Creator is a Streamlit-based Generative AI application for hospitality concept creation. It transforms a single user prompt into:

- a descriptive hospitality concept using Google Gemini
- a matching concept image using Hugging Face Stable Diffusion

The enhanced version also includes:

- user signup and login
- SQLite-based design history
- downloadable saved images
- lightweight personal RAG using each user's previous saved concepts

## Overview

This project is designed for hospitality ideation and visualization use cases such as:

- luxury resorts
- boutique hotels
- destination retreats
- premium cafes and restaurants
- themed travel venues

Users can generate new concepts, maintain their own saved design history, and use earlier preferences as contextual guidance for newer outputs.

## Key Features

- Prompt-based text and image generation
- Gemini-powered hospitality concept descriptions
- Hugging Face Stable Diffusion image generation
- User account signup and login
- SQLite database for user-specific generation history
- Saved image download support
- Personal RAG over previous saved concepts
- Modular multi-file project structure

## Technology Stack

- Python
- Streamlit
- Google Gemini API via `google-genai`
- Hugging Face Inference API
- SQLite
- `requests`

## Project Structure

```text
multimodal-hospitality-creator/
|-- app/
|   |-- __init__.py
|   `-- main.py
|-- services/
|   |-- __init__.py
|   |-- gemini_service.py
|   `-- image_service.py
|-- database/
|   |-- __init__.py
|   `-- db.py
|-- config/
|   |-- __init__.py
|   `-- config.py
|-- utils/
|   |-- __init__.py
|   `-- utils.py
|-- docs/
|   |-- HLD_REPORT_NOTES.md
|   `-- PROJECT_OVERVIEW.md
|-- storage/
|   |-- app.db
|   `-- images/
|-- requirements.txt
|-- .env.example
|-- .gitignore
`-- README.md
```

## Module Description

### `app/main.py`

Main Streamlit application entrypoint.

- renders login and signup screens
- manages session state
- triggers generation workflow
- displays current outputs
- displays previous saved designs
- supports image download

### `services/gemini_service.py`

Handles text generation using Google Gemini.

- reads API key from environment variables or Streamlit secrets
- accepts personal retrieval context
- generates grounded hospitality concept descriptions

### `services/image_service.py`

Handles image generation using Hugging Face.

- reads API key from environment variables or Streamlit secrets
- calls Stable Diffusion inference endpoint
- returns image bytes for display and storage

### `database/db.py`

Handles persistence and retrieval.

- creates SQLite tables
- stores user accounts
- authenticates login
- stores generations per user
- retrieves user history
- retrieves relevant history for personal RAG

### `config/config.py`

Stores configuration values such as:

- model names
- API endpoint
- database path
- local image storage path

### `utils/utils.py`

Contains helper utilities such as prompt validation.

## System Architecture

The application follows a modular service-based architecture with four main layers.

### 1. Presentation Layer

Implemented in Streamlit.

- login/signup UI
- concept generation UI
- user history UI
- image download UI

### 2. Service Layer

Implemented in Python service modules.

- Gemini text generation service
- Hugging Face image generation service

### 3. Persistence Layer

Implemented with SQLite and local file storage.

- users stored in SQLite
- generations stored in SQLite
- generated images stored in `storage/images/`

### 4. Personal RAG Layer

Implemented over user generation history.

- retrieves similar previous prompts and descriptions
- passes them as context to Gemini
- improves continuity across a user's concepts

## Architecture Flow

```text
User
  |
  v
Streamlit UI (app/main.py)
  |
  +--> SQLite (database/db.py) --> Users / Saved Generations
  |
  +--> Personal Retrieval --> Relevant User History
  |
  +--> Gemini Service --> Google Gemini API
  |
  +--> Image Service --> Hugging Face Stable Diffusion API
  |
  v
Generated Text + Generated Image
  |
  v
Saved to User History + Rendered in UI
```

## Process Flow

1. User signs up or logs in.
2. User enters a hospitality prompt.
3. The application validates the prompt.
4. The database retrieves relevant previous saved generations for that user.
5. The prompt and retrieved history are sent to Gemini.
6. Gemini generates a text concept description.
7. The same prompt is sent to Hugging Face for image generation.
8. The generated image is saved locally.
9. Prompt, generated text, and image path are stored in SQLite.
10. The app displays the results in the UI.
11. The user can view and download previous saved images from `My Designs`.

## Personal RAG

This project includes a lightweight personal RAG mechanism.

Instead of retrieving from external documents, the system retrieves from:

- a user's previous prompts
- a user's previous generated text outputs

This allows the app to:

- maintain stylistic continuity
- reflect user preferences over time
- produce more context-aware text generation

The image generation flow remains unchanged and continues to use the current prompt directly.

## API Integration Details

### Google Gemini

- SDK: `google-genai`
- Model: `gemini-2.5-flash`
- Purpose: hospitality text generation
- Authentication: `GEMINI_API_KEY`

### Hugging Face Stable Diffusion

- Access method: HTTP POST
- Model: `stabilityai/stable-diffusion-xl-base-1.0`
- Purpose: image generation
- Authentication: `HUGGINGFACE_API_KEY`

## Database Design

### `users` table

- `id`
- `username`
- `password_hash`
- `created_at`

### `generations` table

- `id`
- `user_id`
- `prompt`
- `generated_text`
- `image_path`
- `created_at`

## Error Handling

The application handles:

- empty prompt input
- missing API keys
- invalid login credentials
- duplicate usernames
- Gemini API errors
- Hugging Face API errors
- missing saved image files

## Security Notes

- API keys are read from environment variables or Streamlit secrets
- passwords are stored as SHA-256 hashes
- secrets are not intended to be committed to source control

## Local Run Instructions

Open PowerShell in the project folder and run:

```powershell
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
$env:GEMINI_API_KEY="your_gemini_api_key"
$env:HUGGINGFACE_API_KEY="your_huggingface_api_key"
venv\Scripts\python.exe -m streamlit run app/main.py --server.address 127.0.0.1 --server.port 8501
```

Then open:

```text
http://127.0.0.1:8501
```

## Streamlit Cloud Deployment

This project can be deployed on Streamlit Community Cloud for project presentation use.

### Deployment Steps

1. Push the project to GitHub
2. Go to `https://share.streamlit.io/`
3. Sign in with GitHub
4. Click `Create app`
5. Choose your repository and branch
6. Set the main file path to `app/main.py`
7. Add secrets in `Advanced settings`

```toml
GEMINI_API_KEY="your_gemini_api_key"
HUGGINGFACE_API_KEY="your_huggingface_api_key"
```

8. Click `Deploy`

### Deployment Note

SQLite and local file storage are suitable for short-term academic presentation use, but should not be treated as permanent production storage in hosted environments.

## Example Prompt

```text
Luxury beach resort with sunset view
```

## References

- Streamlit Documentation
- Google Gemini Python SDK Documentation
- Hugging Face Inference API Documentation
- Python Requests Documentation
