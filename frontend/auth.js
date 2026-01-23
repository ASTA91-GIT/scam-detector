// Authentication JavaScript
const API_BASE_URL = 'http://localhost:5000/api';

// Check if user is authenticated
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        // Redirect to login if not authenticated (except on auth pages)
        if (!window.location.pathname.includes('login.html') && 
            !window.location.pathname.includes('signup.html') &&
            !window.location.pathname.includes('index.html')) {
            window.location.href = 'login.html';
        }
        return null;
    }
    return token;
}

// Get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Show error message
function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }
}

// Hide error message
function hideError(elementId) {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.style.display = 'none';
    }
}

// Signup form handler
if (document.getElementById('signupForm')) {
    document.getElementById('signupForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        hideError('errorMessage');
        
        // Validation
        if (password !== confirmPassword) {
            showError('errorMessage', 'Passwords do not match');
            return;
        }
        
        if (password.length < 6) {
            showError('errorMessage', 'Password must be at least 6 characters');
            return;
        }
        
        const signupBtnText = document.getElementById('signupBtnText');
        const signupSpinner = document.getElementById('signupSpinner');
        
        signupBtnText.style.display = 'none';
        signupSpinner.style.display = 'inline-block';
        
        try {
            const response = await fetch(`${API_BASE_URL}/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            } else {
                showError('errorMessage', data.error || 'Signup failed');
                signupBtnText.style.display = 'inline';
                signupSpinner.style.display = 'none';
            }
        } catch (error) {
            showError('errorMessage', 'Network error. Please try again.');
            signupBtnText.style.display = 'inline';
            signupSpinner.style.display = 'none';
        }
    });
}

// Login form handler
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        hideError('errorMessage');
        
        const loginBtnText = document.getElementById('loginBtnText');
        const loginSpinner = document.getElementById('loginSpinner');
        
        loginBtnText.style.display = 'none';
        loginSpinner.style.display = 'inline-block';
        
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            } else {
                showError('errorMessage', data.error || 'Login failed');
                loginBtnText.style.display = 'inline';
                loginSpinner.style.display = 'none';
            }
        } catch (error) {
            showError('errorMessage', 'Network error. Please try again.');
            loginBtnText.style.display = 'inline';
            loginSpinner.style.display = 'none';
        }
    });
}

// Logout handler
if (document.getElementById('logoutBtn')) {
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'index.html';
    });
}

// Check authentication on page load (for protected pages)
if (window.location.pathname.includes('dashboard.html') || 
    window.location.pathname.includes('analyze.html') ||
    window.location.pathname.includes('result.html')) {
    if (!checkAuth()) {
        window.location.href = 'login.html';
    }
}
