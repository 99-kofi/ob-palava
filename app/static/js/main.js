document.addEventListener('DOMContentLoaded', () => {
    const translateBtn = document.getElementById('translate-btn');
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const ttsBtn = document.getElementById('tts-btn');
    const directionSelect = document.getElementById('direction');
    const variantSelect = document.getElementById('variant');
    const audioPlayer = document.getElementById('audio-player');
    const loader = document.getElementById('loader');
    const statsDisplay = document.getElementById('stats-display');

    // Handle Splash Screen Transition
    const splash = document.getElementById('splash-screen');
    const mainApp = document.getElementById('app-main');

    setTimeout(() => {
        splash.classList.add('fade-out');
        mainApp.classList.add('fade-in-visible');
    }, 3500); // 3.5 seconds cinematic intro

    // Fetch stats on load
    fetchStats();

    translateBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        if (!text) return;

        // UI State
        translateBtn.disabled = true;
        loader.classList.remove('hidden');
        outputText.innerHTML = '<span class="placeholder">Translating...</span>';
        ttsBtn.disabled = true;

        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    direction: directionSelect.value,
                    variant: variantSelect.value
                })
            });

            if (!response.ok) {
                console.error("Server Error:", response.status);
                outputText.innerText = "Technical hitch. Abeg refresh or try again later.";
                return;
            }

            const data = await response.json();
            outputText.innerText = data.translated;
            ttsBtn.disabled = false;
            fetchStats(); // Update stats

        } catch (error) {
            outputText.innerText = "Connection failed. Please check if the server is running.";
            console.error(error);
        } finally {
            translateBtn.disabled = false;
            loader.classList.add('hidden');
        }
    });

    ttsBtn.addEventListener('click', async () => {
        const text = outputText.innerText;
        const variant = variantSelect.value;

        if (!text) return;

        ttsBtn.disabled = true;

        try {
            const response = await fetch('/tts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    variant: variant,
                    direction: directionSelect.value
                })
            });

            const data = await response.json();

            if (data.audio_url) {
                audioPlayer.src = data.audio_url;
                audioPlayer.play();
            } else {
                alert("Could not generate audio");
            }

        } catch (error) {
            console.error(error);
        } finally {
            ttsBtn.disabled = false;
        }
    });

    async function fetchStats() {
        try {
            const res = await fetch('/analytics/stats');
            const data = await res.json();
            if (data.visits !== undefined) {
                statsDisplay.innerText = `Visits: ${data.visits} | Translations: ${data.translations}`;
            }
        } catch (e) {
            console.log("Stats error", e);
        }
    }
});
