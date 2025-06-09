# SCAMPER Multi-Agent System with Web Interface

This project implements the SCAMPER creativity technique using a multi-agent system. It now includes a web-based interface for easier interaction.

## Project Structure

- \`agents/\`: Contains the core logic for each SCAMPER technique agent and the orchestrator.
- \`config/\`: Configuration files (e.g., API keys, settings).
- \`interface/\`: Original command-line chatbot interface.
- \`models/\`: Pydantic schemas for data validation.
- \`utils/\`: Utility functions, including any API clients.
- \`webapp/\`: Contains the new Flask web application.
  - \`webapp/app.py\`: The main Flask application file with API endpoints.
  - \`webapp/static/\`: Static assets (CSS, JavaScript, images).
  - \`webapp/templates/\`: HTML templates for the web interface.
- \`tests/\`: Unit tests for the application.
  - \`tests/test_webapp.py\`: Unit tests for the Flask web API.
- \`main.py\`: Main script to run the command-line chatbot (if applicable).
- \`requirements.txt\`: Python dependencies.

## Features

- Application of 7 SCAMPER techniques: Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse.
- Generation of creative ideas based on user's problem/challenge.
- Interactive command-line interface (original).
- **New:** Modern web interface for a richer user experience.

## Web Interface

The web interface provides a user-friendly way to interact with the SCAMPER system.

### Prerequisites

- Python 3.8+
- Pip (Python package installer)

### Setup and Installation

1.  **Clone the repository (if you haven't already):**
    \`\`\`bash
    git clone <repository-url>
    cd <repository-directory>
    \`\`\`

2.  **Create a virtual environment (recommended):**
    \`\`\`bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    \`\`\`

3.  **Install dependencies:**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

4.  **Environment Variables:**
    Ensure you have a \`.env\` file in the project root if required by the application (e.g., for API keys used by \`config/settings.py\` or \`utils/gemini_client.py\`). A template might look like:
    \`\`\`
    # .env file
    GEMINI_API_KEY=your_api_key_here
    # Add other necessary environment variables
    \`\`\`
    *(Note: Actual required variables depend on the project's specific needs, especially for external API access like Google Gemini.)*

### Running the Web Application

1.  **Navigate to the webapp directory:**
    While the application can be run from the root due to \`sys.path\` modifications in \`webapp/app.py\`, it's often good practice to run it from its directory or ensure your Python path is set up if running from root.
    The current \`webapp/app.py\` is configured to be run directly.

2.  **Run the Flask development server:**
    \`\`\`bash
    python webapp/app.py
    \`\`\`
    The application will typically be available at \`http://127.0.0.1:5000/\`.

### Running Unit Tests

The project uses \`unittest\` for backend tests. \`pytest\` and \`pytest-asyncio\` are included in \`requirements.txt\` for a more convenient testing experience, especially with asynchronous code.

1.  **Ensure all development dependencies are installed:**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`
    *(This includes pytest and pytest-asyncio)*

2.  **Run tests using pytest (recommended for features like async support):**
    From the project root directory:
    \`\`\`bash
    pytest
    \`\`\`
    Pytest will automatically discover and run tests in the \`tests/\` directory.

3.  **Run tests using unittest:**
    From the project root directory:
    \`\`\`bash
    python -m unittest discover -s tests
    \`\`\`
    Or to run a specific file:
    \`\`\`bash
    python -m unittest tests.test_webapp
    \`\`\`

## Original Command-Line Interface

To run the original chatbot interface:
\`\`\`bash
python main.py
\`\`\`
*(This assumes \`main.py\` is set up to launch \`interface/chatbot.py\`)*

---
*This README was enhanced by Jules, your AI software engineering agent.*
