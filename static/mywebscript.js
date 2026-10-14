const form = document.getElementById('emotion-form');
const textarea = document.getElementById('text-to-analyze');
const result = document.getElementById('result');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    result.textContent = 'Analyzing...';

    const params = new URLSearchParams({ textToAnalyze: textarea.value });
    const response = await fetch(`/emotionDetector?${params.toString()}`);
    result.textContent = await response.text();
});
