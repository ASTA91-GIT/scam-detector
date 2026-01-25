// analyze.js
// API_BASE_URL & getAuthHeaders() come from auth.js

const form = document.getElementById('analysisForm');
const fileInput = document.getElementById('fileInput');
const fileUploadArea = document.getElementById('fileUploadArea');
const fileName = document.getElementById('fileName');
const resultContainer = document.getElementById('resultContainer');
/* =========================
   TAB SWITCHING (REQUIRED)
   ========================= */

const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.dataset.tab;

        // Update buttons
        tabButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update tabs
        tabContents.forEach(tab => tab.classList.remove('active'));
        document.getElementById(`${target}Tab`).classList.add('active');
    });
});

/* =========================
   FILE UPLOAD UI HANDLING
   ========================= */

// Click upload area → open file picker
fileUploadArea.addEventListener('click', () => {
    fileInput.click();
});

// Show file name
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileName.style.display = 'block';
        fileName.innerText = `Selected file: ${fileInput.files[0].name}`;
    }
});

// Drag & drop
fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.classList.add('drag-over');
});

fileUploadArea.addEventListener('dragleave', () => {
    fileUploadArea.classList.remove('drag-over');
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.classList.remove('drag-over');

    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileName.style.display = 'block';
        fileName.innerText = `Selected file: ${e.dataTransfer.files[0].name}`;
    }
});

/* =========================
   FORM SUBMIT
   ========================= */

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const analyzeBtnText = document.getElementById('analyzeBtnText');
    const analyzeSpinner = document.getElementById('analyzeSpinner');

    hideError('errorMessage');

    const jobText = document.getElementById('jobText').value.trim();
    const companyEmail = document.getElementById('companyEmail').value.trim();
    const companyWebsite = document.getElementById('companyWebsite').value.trim();
    const file = fileInput.files[0];

    if (!jobText && !file) {
        showError('errorMessage', 'Please paste text OR upload a file');
        return;
    }

    analyzeBtnText.style.display = 'none';
    analyzeSpinner.style.display = 'inline-block';

    try {
        let response;

        // ✅ FILE PATH
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            if (companyEmail) formData.append('company_email', companyEmail);
            if (companyWebsite) formData.append('company_website', companyWebsite);

            response = await fetch(`${API_BASE_URL}/analysis/analyze`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                },
                body: formData
            });

        // ✅ TEXT PATH
        } else {
            response = await fetch(`${API_BASE_URL}/analysis/analyze`, {
                method: 'POST',
                headers: getAuthHeaders(true),
                body: JSON.stringify({
                    text: jobText,
                    company_email: companyEmail,
                    company_website: companyWebsite
                })
            });
        }

        // Guard JSON
        const contentType = response.headers.get('content-type') || '';
        if (!contentType.includes('application/json')) {
            throw new Error('Backend did not return JSON');
        }

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        const result = data.result;
        const explanations = Array.isArray(result.explanations)
            ? result.explanations
            : [];

        resultContainer.classList.remove('hidden');

        resultContainer.innerHTML = `
            <div class="result-header">
                <h2>Analysis Result</h2>
            </div>

            <div class="trust-score-display">
                <div class="score-circle ${
                    result.risk_level === 'Safe'
                        ? 'success'
                        : result.risk_level === 'Suspicious'
                        ? 'warning'
                        : 'danger'
                }">
                    ${result.trust_score}
                </div>
            </div>

            <div style="text-align:center; margin-top:1rem;">
                <span class="risk-badge ${
                    result.risk_level === 'Safe'
                        ? 'badge-success'
                        : result.risk_level === 'Suspicious'
                        ? 'badge-warning'
                        : 'badge-danger'
                }">
                    ${result.risk_level}
                </span>
            </div>

            <p style="text-align:center; margin-top:1rem;">
                Analysis completed
            </p>

            ${
                explanations.length > 0
                    ? `<div class="explanations-list">
                        ${explanations.map(e => `
                            <div class="explanation-item">${e}</div>
                        `).join('')}
                       </div>`
                    : `<p style="text-align:center; color:#666;">
                        No specific scam indicators detected
                       </p>`
            }
        `;

    } catch (error) {
        console.error('Analysis error:', error);
        showError('errorMessage', error.message);
    } finally {
        analyzeBtnText.style.display = 'inline';
        analyzeSpinner.style.display = 'none';
    }
});
