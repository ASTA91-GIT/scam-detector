# Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install MongoDB
- **Windows**: Download from [mongodb.com](https://www.mongodb.com/try/download/community) and install
- **Mac**: `brew install mongodb-community`
- **Linux**: `sudo apt-get install mongodb`

Start MongoDB:
```bash
# Windows
net start MongoDB

# Mac/Linux
sudo systemctl start mongod
# or
mongod
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env and update MongoDB URI if needed
```

### 4. Run Application
```bash
python app.py
```

### 5. Open Browser
Navigate to: `http://localhost:5000`

## ✅ Verify Installation

1. **Check MongoDB**: Open MongoDB Compass or run `mongosh` to verify connection
2. **Check Python**: Run `python --version` (should be 3.8+)
3. **Check Dependencies**: Run `pip list` to verify all packages installed

## 🎯 First Use

1. Click "Get Started" on landing page
2. Sign up with email and password
3. Go to "Analyze" page
4. Paste a job description or upload a file
5. Click "Analyze Job Offer"
6. View results!

## 🐛 Common Issues

**MongoDB Connection Error**
- Ensure MongoDB is running
- Check `MONGODB_URI` in `.env`
- Default: `mongodb://localhost:27017/`

**Port 5000 Already in Use**
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

**Module Not Found**
- Activate virtual environment
- Run `pip install -r requirements.txt` again

## 📚 Next Steps

- Read full README.md for detailed documentation
- Explore the dashboard to see analysis history
- Try analyzing different types of job offers
- Check the AI detection features

Happy analyzing! 🎉
