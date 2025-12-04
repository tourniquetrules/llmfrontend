# OpenRouter Chat Frontend

A simple web-based chat interface for interacting with OpenRouter models (defaulting to `amazon/nova-2-lite-v1:free`).

## Prerequisites

- Python 3.8+
- An OpenRouter API Key (get one at [openrouter.ai](https://openrouter.ai))

## Installation

1. Clone the repository (if applicable) or download the files.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and paste your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here...
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```
3. Type your message in the chat input.
4. You can change the model by editing the "Model" field in the header.

## Dependencies

- **Flask**: Web framework.
- **requests**: For making HTTP requests to OpenRouter.
- **python-dotenv**: For loading environment variables.
