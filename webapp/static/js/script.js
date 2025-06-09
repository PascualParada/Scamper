document.addEventListener('DOMContentLoaded', () => {
    const scamperForm = document.getElementById('scamper-form');
    const resultsSection = document.getElementById('results-section');
    const scamperOutput = document.getElementById('scamper-output');
    const summarySection = document.getElementById('summary-section');
    const summaryText = document.getElementById('summary-text');
    const loadingIndicator = document.getElementById('loading-indicator');
    const errorMessageContainer = document.getElementById('error-message'); // Corrected variable name

    const techniqueDisplayNames = {
        "substitute": "Sustituir - Reemplazar elementos",
        "combine": "Combinar - Fusionar ideas",
        "adapt": "Adaptar - Aplicar de otros contextos",
        "modify": "Modificar - Amplificar o reducir",
        "put_to_other_uses": "Otros Usos - Nuevas aplicaciones", // Corrected key from Python
        "eliminate": "Eliminar - Simplificar",
        "reverse": "Invertir - Reorganizar o hacer al revés"
    };

    scamperForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        resultsSection.style.display = 'block';
        scamperOutput.innerHTML = ''; // Clear previous results
        summarySection.style.display = 'none';
        summaryText.textContent = '';
        errorMessageContainer.style.display = 'none'; // Use correct variable
        loadingIndicator.style.display = 'block';

        const problem = document.getElementById('problem').value;
        const context = document.getElementById('context').value;

        if (!problem.trim()) {
            // More user-friendly error display
            displayError('Por favor, describe tu problema o idea central.');
            loadingIndicator.style.display = 'none';
            return;
        }

        if (problem.trim().length < 5) {
            displayError('El problema debe tener al menos 5 caracteres.');
            loadingIndicator.style.display = 'none';
            return;
        }


        try {
            const response = await fetch('/api/scamper', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ problem: problem.trim(), context: context.trim() }),
            });

            const data = await response.json(); // Attempt to parse JSON regardless of response.ok

            if (!response.ok) {
                // Use error message from API if available, otherwise a generic one
                const errorMsg = data && data.error ? data.error : \`Error del servidor: \${response.status}\`;
                throw new Error(errorMsg);
            }

            displayResults(data);

        } catch (error) {
            console.error('Error fetching SCAMPER results:', error);
            displayError(error.message || 'No se pudo conectar al servidor o procesar la solicitud.');
        } finally {
            loadingIndicator.style.display = 'none';
        }
    });

    function displayError(message) {
        scamperOutput.innerHTML = ''; // Clear any partial results
        summarySection.style.display = 'none';
        errorMessageContainer.innerHTML = \`<p>\${message}</p>\`;
        errorMessageContainer.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function displayResults(data) {
        scamperOutput.innerHTML = ''; // Clear loading/previous error messages
        errorMessageContainer.style.display = 'none';


        if (data.original_problem) {
            const problemAnalyzedContainer = document.createElement('div');
            problemAnalyzedContainer.classList.add('problem-analyzed-container'); // For styling if needed

            const problemTitle = document.createElement('h3');
            problemTitle.textContent = 'Problema Analizado:';

            const problemParagraph = document.createElement('p');
            problemParagraph.textContent = data.original_problem;

            problemAnalyzedContainer.appendChild(problemTitle);
            problemAnalyzedContainer.appendChild(problemParagraph);
            scamperOutput.appendChild(problemAnalyzedContainer);
        }

        if (data.results && Array.isArray(data.results)) {
            data.results.forEach(result => {
                if (result && result.technique && result.explanation && Array.isArray(result.ideas)) {
                    const techniqueDiv = document.createElement('div');
                    techniqueDiv.classList.add('result-technique');

                    // Use .value if technique is an enum-like object, or direct access if it's a string
                    const techniqueKey = (result.technique && typeof result.technique === 'string' ? result.technique.toLowerCase() : result.technique.value.toLowerCase());
                    const techniqueName = techniqueDisplayNames[techniqueKey] || techniqueKey.toUpperCase();


                    let ideasHtml = '<ul class="ideas-list">'; // Added class for styling
                    result.ideas.forEach(idea => {
                        ideasHtml += \`<li>\${idea}</li>\`;
                    });
                    ideasHtml += '</ul>';

                    techniqueDiv.innerHTML = \`
                        <h4>\${techniqueName}</h4>
                        <p class="explanation">\${result.explanation}</p>
                        <div class="ideas-section">
                            <h5>💡 Ideas Generadas:</h5>
                            \${ideasHtml}
                        </div>
                    \`;
                    scamperOutput.appendChild(techniqueDiv);
                }
            });
        } else {
             displayError("La respuesta del servidor no contiene resultados válidos.");
             return; // Stop further processing if results are not as expected
        }


        if (data.summary) {
            summaryText.textContent = data.summary;
            summarySection.style.display = 'block';
        } else {
            summarySection.style.display = 'none';
        }

        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
});
