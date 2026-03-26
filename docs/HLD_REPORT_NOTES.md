# HLD Report Notes

These notes are organized to match the High Level Design table of contents and can be used directly by teammates while preparing the report.

## 1. Introduction

### 1.1 Scope of the document

This document describes the high-level design of a Streamlit-based multimodal Generative AI project for hospitality concept visualization. The system accepts a user prompt and generates both descriptive text and a concept image using external AI APIs.

### 1.2 Intended Audience

- Faculty or evaluators reviewing the architecture
- Project team members preparing presentation or report material
- Developers who want to understand the implementation
- Stakeholders interested in the solution approach

### 1.3 System overview

The system is a lightweight web application that runs locally on Streamlit. It integrates:

- Google Gemini API for text generation
- Hugging Face Stable Diffusion inference API for image generation

The application is designed for simple user interaction and clear multimodal output with a structure that is ready for future extension.

## 2. System Design

### 2.1 Application Design

The application uses a modular package structure:

- Presentation layer: Streamlit UI in `app/main.py`
- Service layer: Gemini and Hugging Face API integrations in `services/`
- Configuration and validation utilities in `config/` and `utils/`
- Database-ready package reserved in `database/`
- Documentation stored in `docs/`

### 2.2 Process Flow

1. User opens Streamlit app in browser.
2. User enters a hospitality concept prompt.
3. User clicks `Generate`.
4. Application validates the prompt.
5. Application sends prompt to Gemini API.
6. Gemini returns descriptive text.
7. Application sends same prompt to Hugging Face image API.
8. Hugging Face returns image bytes.
9. Application renders text and image in the UI.
10. If any issue occurs, the app displays an error message.

### 2.3 Information Flow

- Input source: User prompt entered in Streamlit UI
- Outbound API call 1: Prompt to Gemini text model
- Outbound API call 2: Prompt to Hugging Face Stable Diffusion model
- Inbound response 1: Generated descriptive text
- Inbound response 2: Generated image content
- Output destination: Browser UI rendered by Streamlit

### 2.4 Components Design

#### Component 1: Streamlit UI

- Collects prompt input
- Displays generate button
- Shows spinner during processing
- Displays text output
- Displays image output
- Displays error messages

#### Component 2: Gemini Text Generation Service

- Reads `GEMINI_API_KEY` from environment
- Creates Gemini client using `from google import genai`
- Calls `client.models.generate_content(...)`
- Returns generated text as string

#### Component 3: Hugging Face Image Generation Service

- Reads `HUGGINGFACE_API_KEY` from environment
- Sends HTTP POST request using `requests`
- Uses Stable Diffusion model endpoint
- Returns image bytes for display

#### Component 4: Config and Utilities

- Stores model names and endpoint constants
- Validates user input before making API calls

#### Component 5: Database Package

- Reserved for final-stage persistence integration
- Keeps the project structure prepared for future expansion

### 2.5 Key Design Considerations

- Simplicity with modularity
- Clear separation of UI, services, config, and utilities
- Easy presentation and maintainability
- Ready for future persistence and scaling improvements

### 2.6 API Catalogue

#### Google Gemini API

- Purpose: Generate hospitality concept description
- SDK: `google-genai`
- Method used: `client.models.generate_content`
- Model: `gemini-2.5-flash`
- Authentication: `GEMINI_API_KEY`

#### Hugging Face Inference API

- Purpose: Generate hospitality concept image
- Access method: HTTPS POST request
- Endpoint style: Hugging Face router inference endpoint
- Model: `stabilityai/stable-diffusion-xl-base-1.0`
- Authentication: `HUGGINGFACE_API_KEY`

## 3. Data Design

### 3.1 Data Model

The current version does not persist generation data. Runtime objects include:

- `prompt`
- `text_result`
- `image_result`

### 3.2 Data Access Mechanism

- Prompt is collected from Streamlit input widget
- External AI services are accessed through SDK/HTTP APIs
- Returned data is used in memory during request processing

### 3.3 Data Retention Policies

- No local persistence of prompts or outputs by default
- Data remains in process memory only for the active request/session

### 3.4 Data Migration

No migration is required in the current version.

## 4. Interfaces

- Browser-based UI through Streamlit
- Gemini API interface
- Hugging Face inference interface

## 5. State and Session Management

- Streamlit manages per-session UI state
- Each generation request is processed independently

## 6. Caching

- No explicit caching is implemented in the current version

## 7. Non-Functional Requirements

### 7.1 Security Aspects

- API keys are stored in environment variables
- Sensitive credentials should not be committed to version control
- HTTPS is used for external API communication

### 7.2 Performance Aspects

- Performance depends largely on external API latency
- Gemini text generation is typically faster than image generation
- The UI includes a spinner to indicate processing

## 8. References

- Streamlit documentation
- Google Gemini API Python SDK documentation
- Hugging Face Inference API documentation
- Python `requests` documentation
