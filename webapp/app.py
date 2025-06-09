import sys
import os
from flask import Flask, render_template, request, jsonify

# Add project root to Python path to allow imports from agents, models etc.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.schemas import UserInput, ScamperResponse
from agents.orchestrator import orchestrator # This assumes orchestrator can be imported
                                          # and has process_user_input method.

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scamper', methods=['POST'])
async def scamper_api():
    try:
        data = request.get_json()
        if not data or 'problem' not in data:
            return jsonify({"error": "El campo 'problem' es obligatorio."}), 400

        problem = data['problem']
        context = data.get('context') # Context is optional

        if not isinstance(problem, str) or len(problem.strip()) < 5:
            return jsonify({"error": "El problema debe ser un texto de al menos 5 caracteres."}), 400
        if context is not None and not isinstance(context, str):
            return jsonify({"error": "El contexto debe ser un texto."}), 400

        user_input = UserInput(problem=problem.strip(), context=context.strip() if context else None)

        # Call the SCAMPER orchestrator
        # Assuming process_user_input is an async function as in the chatbot
        scamper_result: ScamperResponse = await orchestrator.process_user_input(user_input)

        # Convert Pydantic model to dict for JSON response
        return jsonify(scamper_result.model_dump())

    except Exception as e:
        print(f"Error in /api/scamper: {e}") # Log to server console
        # Consider more specific error handling for production
        return jsonify({"error": "Ocurrió un error procesando tu solicitud."}), 500

if __name__ == '__main__':
    # Note: For async routes with Flask, 'app.run(debug=True)' is fine for development.
    # For production, a proper ASGI server (like Hypercorn or Uvicorn with Gunicorn) would be needed.
    app.run(debug=True, port=5000) # Using port 5000
