// Result JavaScript
const API_BASE_URL = 'http://localhost:5000/api';

// Load result on page load
window.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const analysisId = urlParams.get('id');

    if (!analysisId) {
        document.getElementById('resultContent').innerHTML = `
            <div class="card">
                <div class="error-message">Analysis ID not provided</div>
                <a href="dashboard.html" class="btn btn-primary">Back to Dashboard</a>
            </div>
        `;
        return;
    }

    await loadResult(analysisId);
});

// Load analysis result
async function loadResult(analysisId) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = 'login.html';
            return;
        }

        const response = await fetch(`${API_BASE_URL}/analysis/result/${analysisId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayResult(data.analysis);
        } else {
            document.getElementById('resultContent').innerHTML = `
                <div class="card">
                    <div class="error-message">Failed to load analysis result</div>
                    <a href="dashboard.html" class="btn btn-primary">Back to Dashboard</a>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading result:', error);
        document.getElementById('resultContent').innerHTML = `
            <div class="card">
                <div class="error-message">Network error. Please try again.</div>
                <a href="dashboard.html" class="btn btn-primary">Back to Dashboard</a>
            </div>
        `;
    }
}

// Display result
function displayResult(analysis) {
    const resultContent = document.getElementById('resultContent');

    const riskBadgeClass = analysis.risk_color === 'success' ? 'badge-success' :
        analysis.risk_color === 'warning' ? 'badge-warning' : 'badge-danger';

    const date = new Date(analysis.created_at).toLocaleString();

    resultContent.innerHTML = `
        <div class="result-container">
            <div class="result-header">
                <h1>Analysis Result</h1>
                <p>Analyzed on ${date}</p>
            </div>
            
            <div class="trust-score-display">
                <div class="score-circle ${analysis.risk_color}">
                    ${analysis.trust_score}
                </div>
                <div class="risk-badge ${riskBadgeClass}">
                    ${analysis.risk_level}
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill ${analysis.risk_color}" style="width: ${analysis.trust_score}%"></div>
            </div>
            
            <div class="card">
                <h2>Key Findings</h2>
                <ul class="explanations-list">
                    ${analysis.explanations.map(exp => `<li>${exp}</li>`).join('')}
                </ul>
            </div>
            
            <div class="details-grid">
                <div class="detail-card">
                    <h4>Keyword Detections</h4>
                    <p>${analysis.keyword_score} suspicious keyword(s) found</p>
                    ${Object.keys(analysis.keyword_detections).length > 0 ?
            `<ul style="margin-top: 0.5rem; padding-left: 1.5rem;">
                            ${Object.entries(analysis.keyword_detections).map(([cat, keywords]) =>
                `<li><strong>${cat}:</strong> ${keywords.join(', ')}</li>`
            ).join('')}
                        </ul>` : '<p>No suspicious keywords detected</p>'}
                </div>
                
                <div class="detail-card">
                    <h4>Urgency Score</h4>
                    <p>${analysis.urgency_score} urgency indicators detected</p>
                </div>
                
                <div class="detail-card">
                    <h4>Grammar Issues</h4>
                    <p>${analysis.grammar_issues} grammar issue(s) found</p>
                </div>
                
                <div class="detail-card">
                    <h4>Financial Red Flags</h4>
                    <p>${analysis.financial_flags_count} financial red flag(s) detected</p>
                </div>
                
                ${analysis.company_email ? `
                <div class="detail-card">
                    <h4>Company Email</h4>
                    <p>${analysis.company_email}</p>
                    <p style="color: ${analysis.email_domain_suspicious ? 'var(--danger-color)' : 'var(--success-color)'}; margin-top: 0.5rem;">
                        ${analysis.email_domain_suspicious ? '⚠️ Free email domain detected' : '✓ Professional email domain'}
                    </p>
                </div>
                ` : ''}
                
                ${analysis.company_website ? `
                <div class="detail-card">
                    <h4>Company Website</h4>
                    <p><a href="${analysis.company_website}" target="_blank">${analysis.company_website}</a></p>
                    <p style="color: ${analysis.website_exists ? 'var(--success-color)' : 'var(--danger-color)'}; margin-top: 0.5rem;">
                        ${analysis.website_exists ? '✓ Website verified' : '⚠️ Website could not be verified'}
                    </p>
                </div>
                ` : ''}
                
                ${analysis.company_email && analysis.company_website ? `
                <div class="detail-card">
                    <h4>Domain Match</h4>
                    <p style="color: ${analysis.company_match ? 'var(--success-color)' : 'var(--danger-color)'};">
                        ${analysis.company_match ? '✓ Email domain matches website' : '⚠️ Email domain does not match website'}
                    </p>
                </div>
                ` : ''}
            </div>
            
            <div style="text-align: center; margin-top: 2rem;">
                <a href="analyze.html" class="btn btn-primary">Analyze Another</a>
                <a href="dashboard.html" class="btn btn-secondary">Back to Dashboard</a>
            </div>
        </div>
    `;
}
