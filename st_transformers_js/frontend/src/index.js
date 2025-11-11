import { Streamlit } from "streamlit-component-lib"

let logEl;
let resultEl;

function log(message, type = 'info') {
  if (logEl) {
    const entry = document.createElement('div');
    entry.className = `log-entry log-${type}`;
    entry.textContent = `${new Date().toLocaleTimeString()} - ${message}`;
    logEl.appendChild(entry);
    logEl.scrollTop = logEl.scrollHeight;
  }
}

function displayResult(data) {
  if (resultEl) {
    resultEl.textContent = JSON.stringify(data, null, 2);
  }
}

async function runPipeline(config) {
  try {
    if (typeof transformers === 'undefined') {
      throw new Error('Transformers.js not loaded');
    }

    log('Loading pipeline...', 'progress');

    const pipeline = await transformers.pipeline(
      config.pipeline_type,
      config.model_name,
      {
        progress_callback: (progress) => {
          if (progress.status === 'downloading') {
            const percent = ((progress.loaded / progress.total) * 100).toFixed(1);
            log(`Downloading ${progress.file}: ${percent}%`, 'progress');
          } else if (progress.status === 'loading') {
            log(`Loading ${progress.file}...`, 'progress');
          }
        }
      }
    );

    log('Pipeline loaded successfully ✓', 'success');

    let processedInputs = config.inputs;
    if (typeof processedInputs === 'string' && processedInputs.length > 100) {
        processedInputs = `data:image/jpeg;base64,${processedInputs}`;
        log('Processing image input...', 'progress');
    }

    log('Running inference...', 'progress');

    const result = await pipeline(processedInputs, config.config);

    log('Inference complete ✓', 'success');
    displayResult(result);

    Streamlit.setComponentValue(result);

  } catch (error) {
    log(`Error: ${error.message}`, 'error');
    console.error('Pipeline error:', error);
    Streamlit.setComponentValue({ error: error.message });
  }
}

function onRender(event) {
  const data = event.detail;

  if (data.theme) {
    Streamlit.setFrameHeight(400);
  }

  if (data.args.config) {
    const config = data.args.config;
    document.body.innerHTML = `
      <div id="container">
        <div id="log">
          <div class="log-entry log-info">🚀 Component initialized...</div>
        </div>
        <pre id="result"></pre>
      </div>
    `;
    logEl = document.getElementById('log');
    resultEl = document.getElementById('result');
    runPipeline(config);
  }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
