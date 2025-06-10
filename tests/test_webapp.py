import sys
import os
import json
import unittest
import asyncio # Required for running async test methods manually if not using pytest-asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Add project root to Python path to allow imports from webapp, agents, models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from webapp.app import app
from models.schemas import ScamperResponse, ScamperResult # Assuming these are used
# Assuming Technique enum is part of models.schemas or accessible
# For the purpose of this test, let's define a mock Technique enum if not easily importable
# from models.schemas import Technique # Ideal case
try:
    from models.schemas import Technique
except ImportError:
    from enum import Enum
    class Technique(Enum):
        SUBSTITUTE = "substitute"
        COMBINE = "combine"
        ADAPT = "adapt"
        MODIFY = "modify"
        PUT_TO_OTHER_USES = "put_to_other_uses"
        ELIMINATE = "eliminate"
        REVERSE = "reverse"

class WebAppTests(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        # For async tests, it's good practice to set up an event loop if not using pytest-asyncio
        # self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.loop)

    # def tearDown(self):
    #     self.loop.close()

    @patch('webapp.app.orchestrator.process_user_input', new_callable=AsyncMock)
    def test_scamper_api_success(self, mock_process_user_input):
        async def run_test():
            mock_response_data = ScamperResponse(
                original_problem="Test problem",
                results=[
                    ScamperResult(
                        technique=Technique.SUBSTITUTE,
                        explanation="Substituted something.",
                        ideas=["Idea 1", "Idea 2"]
                    )
                ],
                summary="Test summary"
            )
            mock_process_user_input.return_value = mock_response_data

            payload = {"problem": "Test problem", "context": "Test context"}
            # Flask's test_client.post itself is not async, but the view function it calls is.
            # The test_client handles the async nature of the endpoint.
            response = self.client.post('/api/scamper', json=payload)

            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response_data['original_problem'], "Test problem")
            self.assertTrue(len(response_data['results']) > 0)
            self.assertEqual(response_data['results'][0]['technique'], Technique.SUBSTITUTE.value)
            self.assertEqual(response_data['summary'], "Test summary")
            mock_process_user_input.assert_called_once()
        asyncio.run(run_test())

    def test_scamper_api_missing_problem(self):
        async def run_test():
            payload = {"context": "Test context"}
            response = self.client.post('/api/scamper', json=payload)

            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data.decode('utf-8'))
            self.assertIn("El campo 'problem' es obligatorio", response_data['error'])
        asyncio.run(run_test())

    def test_scamper_api_short_problem(self):
        async def run_test():
            payload = {"problem": "abc"}
            response = self.client.post('/api/scamper', json=payload)

            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data.decode('utf-8'))
            self.assertIn("El problema debe ser un texto de al menos 5 caracteres", response_data['error'])
        asyncio.run(run_test())

    def test_scamper_api_invalid_context_type(self):
        async def run_test():
            payload = {"problem": "Valid problem", "context": 123}
            response = self.client.post('/api/scamper', json=payload)

            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data.decode('utf-8'))
            self.assertIn("El contexto debe ser un texto", response_data['error'])
        asyncio.run(run_test())

    @patch('webapp.app.orchestrator.process_user_input', new_callable=AsyncMock)
    def test_scamper_api_orchestrator_exception(self, mock_process_user_input):
        async def run_test():
            mock_process_user_input.side_effect = Exception("Orchestrator failed")

            payload = {"problem": "A valid problem for this test"}
            response = self.client.post('/api/scamper', json=payload)

            self.assertEqual(response.status_code, 500)
            response_data = json.loads(response.data.decode('utf-8'))
            self.assertIn("Ocurrió un error procesando tu solicitud", response_data['error'])
        asyncio.run(run_test())

if __name__ == '__main__':
    # This allows running 'python -m unittest tests.test_webapp'
    unittest.main()
