"""
AI/NLP Scam Detection Engine
Implements keyword detection, urgency analysis, red flags, and risk scoring
"""

import re
import requests
from urllib.parse import urlparse
import socket

# -----------------------------
# CONFIG
# -----------------------------

SCAM_KEYWORDS = {
    'urgent': ['urgent', 'immediately', 'asap', 'right away', 'hurry', 'limited time', 'act now'],
    'payment': ['pay', 'fee', 'deposit', 'payment', 'money', 'bitcoin', 'cryptocurrency'],
    'too_good': ['guaranteed', 'no experience needed', 'easy money', 'high salary', 'no interview'],
    'grammar_issues': ['kindly', 'revert back', 'do the needful'],
    'personal_info': ['bank account', 'credit card', 'passport', 'ssn'],
}

FREE_EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
    'aol.com', 'protonmail.com', 'icloud.com'
]

# -----------------------------
# DETECTION HELPERS
# -----------------------------

def detect_scam_keywords(text):
    text = text.lower()
    detected = {}
    score = 0

    for category, keywords in SCAM_KEYWORDS.items():
        hits = [k for k in keywords if k in text]
        if hits:
            detected[category] = hits
            score += len(hits)

    return detected, score


def analyze_urgency_language(text):
    patterns = [
        r'\b(urgent|immediately|asap|hurry|act now)\b',
        r'\b(deadline|expires|last chance)\b',
        r'!{2,}'
    ]

    matches = []
    for p in patterns:
        matches += re.findall(p, text.lower())

    return len(matches), matches


def analyze_grammar_quality(text):
    issues = 0
    patterns = [r'\bkindly\b', r'\brevert back\b', r'\bdo the needful\b']
    for p in patterns:
        if re.search(p, text.lower()):
            issues += 1
    return issues


def detect_financial_red_flags(text):
    patterns = [
        r'\b(pay|payment|fee|deposit|charges)\b',
        r'\b(bitcoin|crypto|wire transfer)\b',
        r'\b(bank account|credit card)\b'
    ]

    matches = []
    for p in patterns:
        matches += re.findall(p, text.lower())

    return len(matches), matches


def check_email_domain(email):
    if not email or '@' not in email:
        return False, None
    domain = email.split('@')[1].lower()
    return domain in FREE_EMAIL_DOMAINS, domain


def verify_website_exists(url):
    try:
        parsed = urlparse(url if url.startswith('http') else 'https://' + url)
        domain = parsed.netloc
        socket.gethostbyname(domain)
        return True, "Website reachable"
    except:
        return False, "Website not reachable"

# -----------------------------
# SCORING
# -----------------------------

def calculate_trust_score(keyword_score, urgency, grammar, financial, email_free, website_ok, company_match):
    score = 100
    score -= min(keyword_score * 5, 30)
    score -= min(urgency * 5, 20)
    score -= min(grammar * 5, 15)
    score -= min(financial * 6, 25)

    if email_free:
        score -= 10
    if not website_ok:
        score -= 15
    if not company_match:
        score -= 10

    return max(0, min(100, score))


def get_risk_level(score):
    if score >= 80:
        return "Safe"
    elif score >= 50:
        return "Suspicious"
    return "High Risk"

def get_risk_color(risk_level):
    if risk_level == "Safe":
        return "success"
    elif risk_level == "Suspicious":
        return "warning"
    return "danger"


# -----------------------------
# 🚩 RED FLAGS & RECOMMENDATIONS
# -----------------------------

def generate_red_flags_and_recommendations(analysis):
    red_flags = []
    recommendations = []

    if analysis['financial_flags_count'] > 0:
        red_flags.append("Advance payment or registration fee requested")
        recommendations.append("Do NOT make any payments before verification")

    if analysis['urgency_score'] > 2:
        red_flags.append("Urgency or pressure tactics detected")
        recommendations.append("Take time to verify the offer independently")

    if analysis['email_domain_suspicious']:
        red_flags.append("Recruiter is using a free email domain")
        recommendations.append("Contact the company via its official website")

    if not analysis['website_exists']:
        red_flags.append("Company website could not be verified")
        recommendations.append("Verify the company’s online presence")

    if analysis['grammar_issues'] > 1:
        red_flags.append("Unprofessional or suspicious language detected")
        recommendations.append("Be cautious of poor-quality communication")

    if not analysis['company_match']:
        red_flags.append("Email domain does not match company website")
        recommendations.append("Verify company contact details carefully")

    if not red_flags:
        recommendations.append("No major risks detected, but continue standard verification")

    return red_flags, recommendations

# -----------------------------
# MAIN ANALYSIS FUNCTION
# -----------------------------

def analyze_job_offer(text, company_email=None, company_website=None):
    keywords, keyword_score = detect_scam_keywords(text)
    urgency_score, urgency_matches = analyze_urgency_language(text)
    grammar_issues = analyze_grammar_quality(text)
    financial_count, financial_matches = detect_financial_red_flags(text)

    email_suspicious, email_domain = check_email_domain(company_email) if company_email else (False, None)
    website_exists, website_status = verify_website_exists(company_website) if company_website else (False, None)

    company_match = True
    if company_email and company_website:
        email_dom = company_email.split('@')[1]
        web_dom = urlparse(company_website).netloc
        company_match = email_dom in web_dom

    trust_score = calculate_trust_score(
        keyword_score,
        urgency_score,
        grammar_issues,
        financial_count,
        email_suspicious,
        website_exists,
        company_match
    )

    risk_level = get_risk_level(trust_score)
    risk_color = get_risk_color(risk_level)


    explanations = []
    if keyword_score:
        explanations.append("Suspicious scam-related keywords detected")
    if urgency_score:
        explanations.append("Urgent or pressure-based language detected")
    if financial_count:
        explanations.append("Financial requests detected in the offer")
    if email_suspicious:
        explanations.append("Free email domain reduces credibility")
    if not website_exists:
        explanations.append("Company website could not be verified")

    if not explanations:
        explanations.append("No obvious scam indicators found")

    result = {
        "trust_score": trust_score,
        "risk_level": risk_level,
        "risk_color": risk_color,  
        "keyword_score": keyword_score,
        "explanations": explanations,
        "keyword_detections": keywords,
        "urgency_score": urgency_score,
        "grammar_issues": grammar_issues,
        "financial_flags_count": financial_count,
        "email_domain_suspicious": email_suspicious,
        "website_exists": website_exists,
        "company_match": company_match
    }

    red_flags, recommendations = generate_red_flags_and_recommendations(result)
    result["red_flags"] = red_flags
    result["recommendations"] = recommendations

    return result
