# AI-Powered Job & Internship Scam Detector

A complete full-stack web application that uses AI and NLP to detect fraudulent job offers and internship scams. Built with Flask (Python), MongoDB, and vanilla JavaScript.

## 🎯 Features

- **User Authentication**: Secure signup/login system with JWT tokens
- **File Upload**: Support for PDF, DOC, DOCX, and TXT files
- **Text Analysis**: Paste job descriptions directly
- **AI Scam Detection**: 
  - Keyword detection for scam patterns
  - Urgency and emotional language analysis
  - Grammar quality checks
  - Financial red flag detection
  - Free email domain detection
- **Company Verification**:
  - Website existence and HTTPS verification
  - Email domain vs website domain matching
- **Trust Scoring**: 0-100 trust score with risk levels (Safe/Suspicious/High Risk)
- **Dashboard**: View analysis history and statistics
- **Modern UI**: Clean, responsive design with gradient backgrounds

## 📁 Project Structure

```
scam-detector/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore file
├── backend/
│   ├── __init__.py
│   ├── database.py      # MongoDB configuration
│   ├── auth.py          # Authentication endpoints
│   ├── auth_utils.py    # JWT token utilities
│   ├── analysis.py      # Analysis endpoints
│   ├── dashboard.py     # Dashboard endpoints
│   ├── scam_detector.py # AI/NLP detection engine
│   └── file_utils.py    # File upload and text extraction
├── frontend/
│   ├── index.html       # Landing page
│   ├── login.html       # Login page
│   ├── signup.html      # Signup page
│   ├── dashboard.html   # User dashboard
│   ├── analyze.html     # Analysis form
│   ├── result.html      # Analysis results page
│   ├── styles.css       # All CSS styles
│   ├── auth.js          # Authentication JavaScript
│   ├── dashboard.js     # Dashboard JavaScript
│   ├── analyze.js       # Analysis form JavaScript
│   └── result.js        # Results display JavaScript
└── uploads/             # Uploaded files directory
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)

### Step 1: Install MongoDB

**Option A: Local MongoDB**
- Download and install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community)
- Start MongoDB service:
  ```bash
  # Windows
  net start MongoDB
  
  # Linux/Mac
  sudo systemctl start mongod
  ```

**Option B: MongoDB Atlas (Cloud)**
- Create a free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Create a cluster and get your connection string

### Step 2: Clone/Download Project

Navigate to the project directory:
```bash
cd scam-detector
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=job_scam_detector

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# File Upload Configuration
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=pdf,doc,docx,txt
```

**For MongoDB Atlas**, update `MONGODB_URI`:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

### Step 6: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 7: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### 1. Create an Account
- Click "Get Started" on the landing page
- Sign up with your email and password (minimum 6 characters)

### 2. Analyze a Job Offer

**Option A: Upload a File**
- Go to "Analyze" page
- Click "Upload File" tab
- Upload PDF, DOC, DOCX, or TXT file
- Optionally add company email and website
- Click "Analyze Job Offer"

**Option B: Paste Text**
- Go to "Analyze" page
- Paste job description in the text area
- Optionally add company email and website
- Click "Analyze Job Offer"

### 3. View Results
- See trust score (0-100)
- Review risk level (Safe/Suspicious/High Risk)
- Check detailed findings and explanations
- View keyword detections and red flags

### 4. Dashboard
- View all past analyses
- See statistics (total analyses, safe/suspicious/high risk counts)
- Delete old analyses
- View detailed results

## 🔧 Technical Details

### Backend Architecture

- **Flask**: Web framework
- **MongoDB**: Database for users, analyses, and files
- **JWT**: Token-based authentication
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction

### Frontend Architecture

- **Vanilla JavaScript**: No frameworks, pure JS
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Fetch API**: For API calls

### AI Detection Features

1. **Keyword Detection**: Scans for scam-related keywords
2. **Urgency Analysis**: Detects pressure tactics and urgency language
3. **Grammar Check**: Identifies common scam grammar patterns
4. **Financial Flags**: Detects payment requests and financial red flags
5. **Email Domain Check**: Verifies if company uses free email domains
6. **Website Verification**: Checks if company website exists and uses HTTPS
7. **Domain Matching**: Verifies email domain matches website domain

### Trust Score Calculation

- Starts at 100 points
- Deducts points for:
  - Suspicious keywords (max -30)
  - Urgency language (max -20)
  - Grammar issues (max -15)
  - Financial red flags (max -20)
  - Free email domain (-10)
  - Unverified website (-15)
  - Domain mismatch (-10)

**Risk Levels:**
- 80-100: Safe (Green)
- 50-79: Suspicious (Yellow)
- 0-49: High Risk (Red)

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Input validation and sanitization
- File type and size validation
- Secure file upload handling
- CORS protection
- Protected API routes

## 🐛 Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running
- Check `MONGODB_URI` in `.env`
- For Atlas, verify connection string includes credentials

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or stop the process using port 5000

### File Upload Fails
- Check file size (max 10MB)
- Verify file type (PDF, DOC, DOCX, TXT only)
- Ensure `uploads/` directory exists

### Module Not Found
- Activate virtual environment
- Run `pip install -r requirements.txt` again

## 📝 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/verify` - Verify token
- `POST /api/auth/logout` - Logout

### Analysis
- `POST /api/analysis/analyze` - Analyze job offer
- `GET /api/analysis/result/<id>` - Get analysis result

### Dashboard
- `GET /api/dashboard/analyses` - Get user analyses
- `DELETE /api/dashboard/analyses/<id>` - Delete analysis
- `GET /api/dashboard/stats` - Get user statistics

## 🚧 Future Enhancements

- Machine learning model integration (Naive Bayes/Logistic Regression)
- WHOIS API integration for domain age checking
- LinkedIn company verification
- Email sending for analysis reports
- Batch analysis for multiple offers
- Export results as PDF
- Multi-language support

## 📄 License

This project is open source and available for educational purposes.

---

**Built with ❤️ to protect job seekers from scams**
