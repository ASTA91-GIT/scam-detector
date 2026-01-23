"""
AI/NLP Scam Detection Engine
Implements keyword detection, urgency analysis, and risk scoring
"""
import re
import requests
from urllib.parse import urlparse
import socket

# Scam keyword patterns
SCAM_KEYWORDS = {
    'urgent': ['urgent', 'immediately', 'asap', 'right away', 'hurry', 'limited time', 'act now'],
    'payment': ['pay', 'fee', 'deposit', 'payment', 'money', 'wire transfer', 'western union', 'moneygram', 'bitcoin', 'cryptocurrency'],
    'suspicious_email': ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'protonmail.com'],
    'too_good': ['guaranteed', 'no experience needed', 'work from home', 'easy money', 'get rich quick', 'high salary', 'no interview'],
    'grammar_issues': ['congratulation', 'congratulation you', 'kindly', 'revert back', 'do the needful'],
    'personal_info': ['ssn', 'social security', 'bank account', 'credit card', 'passport number'],
    'remote_work_scam': ['work from home', 'online job', 'data entry', 'typing job', 'no experience'],
}

# Free email domains
FREE_EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
    'protonmail.com', 'icloud.com', 'mail.com', 'yandex.com', 'zoho.com'
]

def detect_scam_keywords(text):
    """Detect scam-related keywords in text"""
    text_lower = text.lower()
    detected_keywords = {}
    total_score = 0
    
    for category, keywords in SCAM_KEYWORDS.items():
        found = []
        for keyword in keywords:
            if keyword in text_lower:
                found.append(keyword)
                total_score += 1
        
        if found:
            detected_keywords[category] = found
    
    return detected_keywords, total_score

def analyze_urgency_language(text):
    """Analyze urgency and emotional manipulation in text"""
    urgency_patterns = [
        r'\b(urgent|immediately|asap|right away|hurry|limited time|act now)\b',
        r'\b(must|need to|required to|you must)\b',
        r'\b(deadline|expires|expiring|last chance)\b',
        r'!{2,}',  # Multiple exclamation marks
        r'\b(guaranteed|promise|assure)\b'
    ]
    
    urgency_score = 0
    matches = []
    
    for pattern in urgency_patterns:
        found = re.findall(pattern, text.lower())
        if found:
            urgency_score += len(found)
            matches.extend(found)
    
    return urgency_score, matches

def analyze_grammar_quality(text):
    """Heuristic grammar quality check"""
    # Check for common scam grammar patterns
    grammar_issues = [
        r'\b(congratulation[^s])\b',  # Missing 's'
        r'\b(kindly)\b',  # Common in scam emails
        r'\b(revert back)\b',  # Redundant
        r'\b(do the needful)\b',  # Scam phrase
        r'\b(am [a-z]+ing)\b',  # "am writing", "am contacting"
    ]
    
    issues_found = 0
    for pattern in grammar_issues:
        if re.search(pattern, text.lower()):
            issues_found += 1
    
    # Basic grammar check: sentence structure
    sentences = re.split(r'[.!?]+', text)
    avg_sentence_length = len(text) / max(len(sentences), 1)
    
    # Very short or very long sentences might indicate issues
    if avg_sentence_length < 20 or avg_sentence_length > 200:
        issues_found += 1
    
    return issues_found

def detect_financial_red_flags(text):
    """Detect financial red flags"""
    financial_patterns = [
        r'\b(pay|payment|fee|deposit|money|cost|charge)\b',
        r'\b(wire transfer|western union|moneygram|bitcoin|cryptocurrency|paypal)\b',
        r'\b(bank account|credit card|debit card)\b',
        r'\$\d+',  # Dollar amounts
        r'\b(refund|reimbursement|advance payment)\b'
    ]
    
    flags = []
    for pattern in financial_patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            flags.extend(matches)
    
    return len(flags), flags

def check_email_domain(email):
    """Check if email uses free email domain"""
    if not email or '@' not in email:
        return False, None
    
    domain = email.split('@')[1].lower()
    is_free = domain in FREE_EMAIL_DOMAINS
    
    return is_free, domain

def verify_website_exists(url):
    """Check if website exists and is accessible"""
    try:
        # Parse URL
        parsed = urlparse(url)
        if not parsed.scheme:
            url = 'https://' + url
            parsed = urlparse(url)
        
        domain = parsed.netloc or parsed.path.split('/')[0]
        
        # Check DNS resolution
        try:
            socket.gethostbyname(domain)
        except socket.gaierror:
            return False, "Domain does not resolve"
        
        # Check HTTPS
        is_https = parsed.scheme == 'https' or url.startswith('https://')
        
        # Try to connect
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            status_code = response.status_code
            return True, f"Website accessible (Status: {status_code}, HTTPS: {is_https})"
        except:
            return True, f"Domain exists but connection failed (HTTPS: {is_https})"
            
    except Exception as e:
        return False, f"Error checking website: {str(e)}"

def check_domain_age(domain):
    """Mock domain age check (in production, use WHOIS API)"""
    # This is a simplified version
    # In production, use a WHOIS API service
    return None, "Domain age check not available (requires API)"

def calculate_trust_score(keyword_score, urgency_score, grammar_issues, financial_flags, 
                         email_domain_suspicious, website_exists, company_match):
    """Calculate overall trust score (0-100)"""
    # Start with 100 points
    score = 100
    
    # Deduct points for various red flags
    score -= min(keyword_score * 5, 30)  # Keywords: max -30 points
    score -= min(urgency_score * 3, 20)  # Urgency: max -20 points
    score -= min(grammar_issues * 5, 15)  # Grammar: max -15 points
    score -= min(financial_flags * 4, 20)  # Financial: max -20 points
    
    # Email domain check
    if email_domain_suspicious:
        score -= 10
    
    # Website verification
    if not website_exists:
        score -= 15
    
    # Company email/website mismatch
    if not company_match:
        score -= 10
    
    # Ensure score is between 0 and 100
    score = max(0, min(100, score))
    
    return round(score, 2)

def get_risk_level(trust_score):
    """Get risk level based on trust score"""
    if trust_score >= 80:
        return "Safe", "success"
    elif trust_score >= 50:
        return "Suspicious", "warning"
    else:
        return "High Risk", "danger"

def analyze_job_offer(text, company_email=None, company_website=None):
    """
    Main analysis function
    Returns comprehensive scam detection results
    """
    # Keyword detection
    keywords, keyword_score = detect_scam_keywords(text)
    
    # Urgency analysis
    urgency_score, urgency_matches = analyze_urgency_language(text)
    
    # Grammar quality
    grammar_issues = analyze_grammar_quality(text)
    
    # Financial red flags
    financial_flags_count, financial_flags = detect_financial_red_flags(text)
    
    # Email domain check
    email_suspicious = False
    email_domain = None
    if company_email:
        email_suspicious, email_domain = check_email_domain(company_email)
    
    # Website verification
    website_exists = False
    website_status = None
    if company_website:
        website_exists, website_status = verify_website_exists(company_website)
    
    # Company match check (simplified)
    company_match = True
    if company_email and company_website:
        email_domain_check = company_email.split('@')[1] if '@' in company_email else None
        website_domain = urlparse(company_website).netloc if company_website else None
        if email_domain_check and website_domain:
            # Check if email domain matches website domain
            company_match = email_domain_check.lower() in website_domain.lower() or \
                          website_domain.lower() in email_domain_check.lower()
    
    # Calculate trust score
    trust_score = calculate_trust_score(
        keyword_score, urgency_score, grammar_issues, financial_flags_count,
        email_suspicious, website_exists, company_match
    )
    
    # Get risk level
    risk_level, risk_color = get_risk_level(trust_score)
    
    # Generate explanations
    explanations = []
    if keyword_score > 0:
        explanations.append(f"Found {keyword_score} suspicious keyword(s) related to scams")
    if urgency_score > 3:
        explanations.append("High urgency language detected - legitimate companies rarely use pressure tactics")
    if grammar_issues > 2:
        explanations.append("Multiple grammar issues found - professional companies typically have better communication")
    if financial_flags_count > 0:
        explanations.append(f"Financial red flags detected: requests for payment or personal financial information")
    if email_suspicious:
        explanations.append("Company email uses free email domain - legitimate companies typically use their own domain")
    if not website_exists:
        explanations.append("Company website could not be verified or does not exist")
    if not company_match:
        explanations.append("Email domain does not match company website domain")
    
    if not explanations:
        explanations.append("No major red flags detected. However, always verify independently.")
    
    return {
        'trust_score': trust_score,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'keyword_detections': keywords,
        'keyword_score': keyword_score,
        'urgency_score': urgency_score,
        'urgency_matches': urgency_matches[:10],  # Limit to 10 matches
        'grammar_issues': grammar_issues,
        'financial_flags': financial_flags[:10],  # Limit to 10 flags
        'financial_flags_count': financial_flags_count,
        'email_domain_suspicious': email_suspicious,
        'email_domain': email_domain,
        'website_exists': website_exists,
        'website_status': website_status,
        'company_match': company_match,
        'explanations': explanations,
        'text_length': len(text),
        'word_count': len(text.split())
    }
