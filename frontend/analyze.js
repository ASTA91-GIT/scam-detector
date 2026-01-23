// Analysis JavaScript
const API_BASE_URL = 'http://localhost:5000/api';

// Tab switching
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        
        // Update buttons
        tabButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update content
        tabContents.forEach(c => c.classList.remove('active'));
        document.getElementById(`${targetTab}Tab`).classList.add('active');
    });
});

// File upload handling
const fileInput = document.getElementById('fileInput');
const fileUploadArea = document.getElementById('fileUploadArea');
const fileName = document.getElementById('fileName');

fileUploadArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = `Selected: ${file.name}`;
        fileName.style.display = 'block';
    }
});

// Drag and drop
fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.style.borderColor = 'var(--primary-color)';
    fileUploadArea.style.background = 'var(--light-bg)';
});

fileUploadArea.addEventListener('dragleave', () => {
    fileUploadArea.style.borderColor = 'var(--border-color)';
    fileUploadArea.style.background = 'transparent';
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.style.borderColor = 'var(--border-color)';
    fileUploadArea.style.background = 'transparent';
    
    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files;
        fileName.textContent = `Selected: ${file.name}`;
        fileName.style.display = 'block';
    }
});

// Analysis form submission
document.getElementById('analysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const analyzeBtnText = document.getElementById('analyzeBtnText');
    const analyzeSpinner = document.getElementById('analyzeSpinner');
    const errorMessage = document.getElementById('errorMessage');
    
    hideError('errorMessage');
    
    analyzeBtnText.style.display = 'none';
    analyzeSpinner.style.display = 'inline-block';
    
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = 'login.html';
            return;
        }
        
        const formData = new FormData();
        
        // Get text input
        const jobText = document.getElementById('jobText').value;
        const companyEmail = document.getElementById('companyEmail').value;
        const companyWebsite = document.getElementById('companyWebsite').value;
        
        // Check if file is uploaded
        const file = fileInput.files[0];
        
        if (file) {
            formData.append('file', file);
        }
        
        if (jobText) {
            formData.append('text', jobText);
        }
        
        if (companyEmail) {
            formData.append('company_email', companyEmail);
        }
        
        if (companyWebsite) {
            formData.append('company_website', companyWebsite);
        }
        
        // Validate input
        if (!jobText && !file) {
            showError('errorMessage', 'Please provide job description text or upload a file');
            analyzeBtnText.style.display = 'inline';
            analyzeSpinner.style.display = 'none';
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/analysis/analyze`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Redirect to result page
            window.location.href = `result.html?id=${data.result.analysis_id}`;
        } else {
            showError('errorMessage', data.error || 'Analysis failed');
            analyzeBtnText.style.display = 'inline';
            analyzeSpinner.style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error);
        showError('errorMessage', 'Network error. Please try again.');
        analyzeBtnText.style.display = 'inline';
        analyzeSpinner.style.display = 'none';
    }
});

// Helper functions
function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }
}

function hideError(elementId) {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.style.display = 'none';
    }
}
