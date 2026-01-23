// Dashboard JavaScript
const API_BASE_URL = 'http://localhost:5000/api';

// Load dashboard data
async function loadDashboard() {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = 'login.html';
            return;
        }
        
        // Load stats
        await loadStats();
        
        // Load analyses
        await loadAnalyses();
    } catch (error) {
        console.error('Error loading dashboard:', error);
        document.getElementById('analysesList').innerHTML = 
            '<div class="error-message">Failed to load dashboard data</div>';
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/stats`, {
            headers: getAuthHeaders()
        });
        
        if (response.ok) {
            const data = await response.json();
            displayStats(data);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Display statistics
function displayStats(stats) {
    const statsContainer = document.getElementById('statsCards');
    statsContainer.innerHTML = `
        <div class="stat-card">
            <h3>Total Analyses</h3>
            <div class="stat-value">${stats.total_analyses}</div>
        </div>
        <div class="stat-card">
            <h3>Safe</h3>
            <div class="stat-value" style="color: var(--success-color);">${stats.safe_count}</div>
        </div>
        <div class="stat-card">
            <h3>Suspicious</h3>
            <div class="stat-value" style="color: var(--warning-color);">${stats.suspicious_count}</div>
        </div>
        <div class="stat-card">
            <h3>High Risk</h3>
            <div class="stat-value" style="color: var(--danger-color);">${stats.high_risk_count}</div>
        </div>
        <div class="stat-card">
            <h3>Avg Trust Score</h3>
            <div class="stat-value">${stats.average_trust_score}</div>
        </div>
    `;
}

// Load analyses
async function loadAnalyses() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/analyses?limit=20`, {
            headers: getAuthHeaders()
        });
        
        if (response.ok) {
            const data = await response.json();
            displayAnalyses(data.analyses);
        } else {
            document.getElementById('analysesList').innerHTML = 
                '<div class="error-message">Failed to load analyses</div>';
        }
    } catch (error) {
        console.error('Error loading analyses:', error);
        document.getElementById('analysesList').innerHTML = 
            '<div class="error-message">Network error. Please try again.</div>';
    }
}

// Display analyses list
function displayAnalyses(analyses) {
    const listContainer = document.getElementById('analysesList');
    
    if (analyses.length === 0) {
        listContainer.innerHTML = `
            <div class="card">
                <p style="text-align: center; color: var(--text-secondary);">
                    No analyses yet. <a href="analyze.html">Start analyzing</a> your first job offer!
                </p>
            </div>
        `;
        return;
    }
    
    listContainer.innerHTML = analyses.map(analysis => {
        const date = new Date(analysis.created_at).toLocaleDateString();
        const riskBadgeClass = analysis.risk_color === 'success' ? 'badge-success' : 
                              analysis.risk_color === 'warning' ? 'badge-warning' : 'badge-danger';
        
        return `
            <div class="analysis-item">
                <div class="analysis-item-info">
                    <h3>Analysis #${analysis._id.slice(-6)}</h3>
                    <p>Trust Score: ${analysis.trust_score}/100 | ${date}</p>
                    <span class="risk-badge ${riskBadgeClass}">${analysis.risk_level}</span>
                </div>
                <div class="analysis-item-actions">
                    <a href="result.html?id=${analysis._id}" class="btn btn-primary">View Details</a>
                    <button onclick="deleteAnalysis('${analysis._id}')" class="btn btn-outline">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

// Delete analysis
async function deleteAnalysis(analysisId) {
    if (!confirm('Are you sure you want to delete this analysis?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/analyses/${analysisId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (response.ok) {
            loadDashboard(); // Reload dashboard
        } else {
            alert('Failed to delete analysis');
        }
    } catch (error) {
        console.error('Error deleting analysis:', error);
        alert('Network error. Please try again.');
    }
}

// Get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Load dashboard on page load
if (document.getElementById('analysesList')) {
    loadDashboard();
}
