# Hospitality Concept Visualizer

Hospitality Concept Visualizer is a multimodal Generative AI application that transforms a single hospitality prompt into two outputs:

- a detailed textual concept description
- a visually aligned concept image

The project is designed for hospitality concept ideation, experience design visualization, and rapid presentation of venue ideas such as resorts, hotels, cafes, restaurants, and destination spaces.

## Overview

In hospitality planning, a concept usually needs both narrative and visual communication. This project brings both together in one workflow. A user enters a prompt such as `Luxury beach resort with sunset view`, and the system generates:

- a descriptive concept summary using Google Gemini
- a concept image using Hugging Face Stable Diffusion

The result is shown in a clean Streamlit web interface, making the project suitable for academic presentation, architectural explanation, and future product extension.

## Key Features

- Prompt-based concept generation
- Text generation using Google Gemini
- Image generation using Hugging Face Stable Diffusion
- Simple and clean Streamlit UI
- Side-by-side display of text and image outputs
- Input validation and API error handling
- Modular multi-file Python structure for maintainability

## Technology Stack

- Python
- Streamlit
- Google Gemini API via `google-genai`
- Hugging Face Inference API
- `requests`

## Project Structure

```text
team_handoff_demo/
|-- app.py
|-- config.py
|-- gemini_service.py
|-- image_service.py
|-- utils.py
|-- requirements.txt
|-- .env.example
|-- README.md
|-- PROJECT_OVERVIEW.md
|-- HLD_REPORT_NOTES.md
```

## Module Description

### `app.py`

Main Streamlit application file.

- renders the web interface
- accepts user prompt input
- triggers text and image generation
- displays outputs in separate columns
- handles user-facing errors

### `gemini_service.py`

Handles text generation using Google Gemini.

- reads `GEMINI_API_KEY`
- creates the Gemini client
- sends the prompt to `gemini-2.5-flash`
- returns generated text as a Python string

### `image_service.py`

Handles image generation using Hugging Face.

- reads `HUGGINGFACE_API_KEY`
- sends prompt to Stable Diffusion endpoint
- returns image bytes for rendering in Streamlit

### `config.py`

Stores shared configuration values.

- Gemini model name
- Hugging Face model name
- Hugging Face API endpoint

### `utils.py`

Contains lightweight helper logic.

- validates prompt input before API calls

## System Architecture

The application follows a simple service-based architecture with clear separation of concerns.

### Architecture Layers

#### 1. Presentation Layer

Implemented using Streamlit in `app.py`.

Responsibilities:

- accept user input
- trigger the generation workflow
- display text output
- display image output
- show spinner and error messages

#### 2. Application / Service Layer

Implemented using Python service files.

Responsibilities:

- call Gemini API for text generation
- call Hugging Face API for image generation
- keep integration logic separate from UI logic

#### 3. External AI Services Layer

Third-party AI services used by the application.

- Google Gemini for large language model based text generation
- Hugging Face Stable Diffusion inference endpoint for image generation

## Architecture Flow

```text
User
  |
  v
Streamlit UI (app.py)
  |
  +--> Gemini Service (gemini_service.py) --> Google Gemini API
  |
  +--> Image Service (image_service.py) --> Hugging Face Stable Diffusion API
  |
  v
Generated Text + Generated Image
  |
  v
Rendered Back in Streamlit UI
```

## Process Flow

1. User opens the Streamlit web application.
2. User enters a hospitality concept prompt.
3. User clicks the `Generate` button.
4. The application validates the prompt.
5. The prompt is sent to the Gemini service for text generation.
6. Gemini returns a descriptive hospitality concept response.
7. The same prompt is sent to the Hugging Face image service.
8. Hugging Face returns the generated image.
9. The application displays both outputs in the browser.
10. If any failure occurs, the application shows an error message instead of breaking the UI.

## Information Flow

### Input

- user prompt entered in Streamlit

### Internal Processing

- validation through `utils.py`
- text request through `gemini_service.py`
- image request through `image_service.py`

### Output

- generated concept description
- generated concept image

## API Integration Details

### Google Gemini

- SDK: `google-genai`
- Import: `from google import genai`
- Model: `gemini-2.5-flash`
- Purpose: text generation
- Authentication: `GEMINI_API_KEY`

### Hugging Face Stable Diffusion

- Access method: HTTP POST request
- Endpoint: Hugging Face router inference endpoint
- Model: `stabilityai/stable-diffusion-xl-base-1.0`
- Purpose: image generation
- Authentication: `HUGGINGFACE_API_KEY`

## Functional Workflow

### Text Generation

- receives prompt from UI
- sends prompt to Gemini API
- returns formatted descriptive text

### Image Generation

- receives same prompt from UI
- sends prompt to Hugging Face API
- returns generated image bytes

### User Presentation

- outputs are displayed in two columns
- text is shown under `Generated Text`
- image is shown under `Generated Image`

## Error Handling

The project includes simple but useful error handling for a stable user experience.

- empty prompt validation
- missing environment variables
- Gemini API errors
- Hugging Face API errors
- unexpected runtime errors

## Non-Functional Considerations

### Maintainability

- code is separated into focused modules
- configuration is centralized
- UI and API logic are kept separate

### Scalability

The project currently focuses on core multimodal generation, but its structure allows future extension such as:

- database integration
- prompt history
- user authentication
- caching
- deployment to cloud environments

### Security

- API keys are read from environment variables
- secrets are not stored directly in source files
- `.env.example` is included only as a reference template

## Setup Instructions

Open PowerShell in the project folder and run the following commands:

```powershell
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
$env:GEMINI_API_KEY="your_gemini_api_key"
$env:HUGGINGFACE_API_KEY="your_huggingface_api_key"
venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Then open:

```text
http://127.0.0.1:8501
```

## Example Prompt

```text
Luxury beach resort with sunset view
```

## Current Scope

The current version includes the complete multimodal generation pipeline with modular project structure, API integration, and interactive UI. The next enhancement phase can extend this foundation with persistence, analytics, and richer user workflows.

## References

- Streamlit Documentation
- Google Gemini Python SDK Documentation
- Hugging Face Inference API Documentation
- Python Requests Documentation
