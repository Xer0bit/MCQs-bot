document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mcq-form');
    const topicInput = document.getElementById('topic');
    const numberInput = document.getElementById('number');
    const resultDiv = document.getElementById('result');
    const logPanel = document.getElementById('log-panel');
    const generateBtn = document.getElementById('generate-btn');

    function addLog(message, type = 'info') {
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        logPanel.appendChild(entry);
        logPanel.scrollTop = logPanel.scrollHeight;
    }

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        generateBtn.disabled = true;
        resultDiv.innerHTML = '';
        logPanel.innerHTML = '';
        
        const topic = topicInput.value;
        const number = numberInput.value;

        addLog(`Starting MCQ generation for topic: ${topic}`, 'info');
        addLog(`Requesting ${number} questions...`, 'info');

        try {
            const response = await fetch(`/api/generate_mcqs?topic=${topic}&number=${number}`);
            const data = await response.json();

            if (data.success) {
                addLog(`Successfully generated ${data.mcqs.length - 1} questions!`, 'success');
                resultDiv.innerHTML = generateDownloadButton(data.mcqs);
            } else {
                addLog('Failed to generate MCQs', 'error');
                resultDiv.innerHTML = 'Error generating MCQs. Please try again.';
            }
        } catch (error) {
            console.error('Error:', error);
            addLog(`Error: ${error.message}`, 'error');
            resultDiv.innerHTML = 'An error occurred. Please try again.';
        } finally {
            generateBtn.disabled = false;
        }
    });

    function generateDownloadButton(mcqs) {
        const csvContent = "data:text/csv;charset=utf-8," 
            + mcqs.map(row => 
                row.map(cell => 
                    cell.includes(',') || cell.includes('"') || cell.includes('\n') 
                        ? '"' + cell.replace(/"/g, '""') + '"' 
                        : cell
                ).join(",")
            ).join("\n");
        const encodedUri = encodeURI(csvContent);
        return `<a href="${encodedUri}" download="mcqs.csv" class="download-link">📥 Download MCQs as CSV</a>`;
    }

    // Clear logs button
    const clearLogsBtn = document.createElement('button');
    clearLogsBtn.textContent = 'Clear Logs';
    clearLogsBtn.style.marginTop = '10px';
    clearLogsBtn.onclick = () => logPanel.innerHTML = '';
    logPanel.parentElement.insertBefore(clearLogsBtn, logPanel);
});