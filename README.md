# 📈 Growth Potential Explainer

An interactive Streamlit dashboard that makes hiring scores **come alive** through real-time explainability, visualizations, and what-if scenarios.

## 🌟 What Makes This Special

Instead of just showing a number, this dashboard lets you **see the score working**:

- **Interactive Radar Charts** - Visualize candidate strengths across 5 growth dimensions
- **Career Timeline Visualization** - See the candidate's journey come to life
- **Real-time What-If Simulator** - Adjust parameters and watch scores update instantly
- **AI-Powered Chat Assistant** - Ask questions and get intelligent explanations powered by Groq's Llama 3.1
- **Natural Language Explanations** - Understand exactly why someone scored the way they did
- **Side-by-Side Comparisons** - Compare candidates with interactive heatmaps and charts

## 🎯 The Four Factors (We chose Growth Potential)

This project focuses on **Growth Potential** - one of the most critical yet hardest-to-measure factors in hiring. We break it down into 5 explainable sub-factors:

### 1. **Learning Agility (30% weight)**
   - How quickly they acquire new skills
   - Certifications earned
   - Courses completed
   - Learning velocity

### 2. **Skill Progression (25% weight)**
   - Career trajectory and advancement
   - Role transitions
   - Technology stack breadth
   - Speed of seniority growth

### 3. **Adaptability (20% weight)**
   - Ability to thrive in changing environments
   - Industry switches
   - Domain pivots
   - Response to challenges

### 4. **Innovation Mindset (15% weight)**
   - Creative problem-solving and initiative
   - Side projects and open source
   - Team contributions
   - Patents and publications

### 5. **Feedback Integration (10% weight)**
   - How well they learn from feedback
   - Performance improvements
   - Mentorship seeking behavior
   - Self-awareness

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8 or higher
pip or conda
```

### Installation

**Quick Start (Recommended):**
```bash
./run.sh
```

The script will automatically:
- Create a Python virtual environment
- Install all dependencies
- Launch the dashboard

**Manual Installation:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

**Open your browser:**
The app will automatically open at `http://localhost:8501`

**Setup AI Assistant (Recommended):**
1. Open the `.env` file in the project root
2. Replace `your_groq_api_key_here` with your actual Groq API key
3. Your key should start with `gsk_`
4. Save the file and restart the app

Don't have a key? Get a free one at https://console.groq.com/keys (14,400 requests/day free tier)

## 📊 Features Walkthrough

### 🏠 Dashboard View
- See all 3 candidates ranked by Growth Potential
- Beautiful visual cards with scores
- Quick comparison chart
- At-a-glance insights

### 🤖 AI Assistant
- **Chat with AI** about candidate scores
- Ask questions like "Why did Sarah score higher?"
- Get personalized explanations for each candidate
- Compare candidates through natural conversation
- Free tier: 14,400 requests/day via Groq

### 👥 Candidate Deep Dive
- **Score Gauge** - Visual representation of overall growth potential
- **Natural Language Explanation** - Strengths and development areas
- **Factor Breakdown** - Radar chart + weighted contribution chart
- **Career Timeline** - Interactive timeline with roles, certifications, achievements
- **Deep Metrics** - Expandable sections showing all underlying data

### 🔍 Compare Candidates
- **Heatmap** - Color-coded comparison across all factors
- **Detailed Table** - Side-by-side numerical comparison
- **Factor Analysis** - Deep dive into specific factors

### 🔮 What-If Simulator
The most **interactive** feature:
- Adjust 13+ parameters with sliders
- Watch the score recalculate in real-time
- See how each change affects the radar chart
- Get instant natural language explanations
- Test scenarios like "What if they had 2 more certifications?"

### 🤖 AI Assistant (NEW!)
**Two powerful AI-powered tools:**

#### 💬 Chat Assistant
- Ask questions about any candidate in natural language
- Get AI-powered explanations of why candidates scored the way they did
- Compare candidates interactively
- Understand the scoring methodology through conversation
- Upload files (CSV, JSON, Excel, PDF) for additional context

#### 🎯 Resume-JD Matcher
- Upload candidate resumes (TXT, PDF, DOC, DOCX)
- Paste job descriptions
- Get comprehensive AI-powered match analysis with:
  - **Overall Match Score** (0-100)
  - **Detailed Breakdown** (Technical Skills, Experience, Domain, Education, Culture Fit)
  - **Key Strengths** - What matches well
  - **Gaps & Weaknesses** - What's missing
  - **Recommendation** - Hire, consider, or pass
  - **Interview Questions** - Based on identified gaps
  - **Follow-up Chat** - Ask questions about the analysis
- Download analysis reports
- Context-aware follow-up questions

**Powered by Groq's ultra-fast Llama 3.3 70B model**
**Requires free API key** from https://console.groq.com/keys (14,400 requests/day)

## 🎨 Screenshots

The dashboard includes:
- 📊 Interactive Plotly visualizations
- 🎨 Modern gradient design
- 📱 Responsive layout
- ⚡ Real-time updates

## 💡 Why This Approach Works

Traditional hiring platforms show you:
```
Candidate: Sarah Chen
Score: 78.4
```

This dashboard shows you:
```
Sarah Chen: 78.4/100

Exceptional Growth Potential - Outstanding ability to learn, adapt, and evolve

Key Strengths:
- Learning Agility (86/100)
- Feedback Integration (88/100)
- Adaptability (90/100)

[Interactive radar chart]
[Career timeline showing 7 milestones]
[Weighted contribution breakdown]

What if she had 1 more certification? → Score becomes 79.8
```

## 🗂️ Project Structure

```
.
├── app.py                  # Main Streamlit dashboard (1200+ lines)
├── candidate_data.py       # Scoring logic and candidate data
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── .env.example           # Template for .env
├── .gitignore             # Git ignore rules
├── run.sh                 # Quick start script
├── README.md              # This file
└── archive/               # Legacy React/Node.js version
```

## 📦 Code Organization

The codebase is organized into clear sections:
- **Visualization Functions** - All chart creation (radar, timeline, comparison, etc.)
- **Interactive Features** - What-If Simulator
- **Helper Functions** - Utility functions for data processing
- **AI Assistant & Resume Matcher** - AI-powered features
- **Page Rendering Functions** - Dashboard, Deep Dive, Comparison views
- **Main Application** - Navigation and routing

## 🔧 Customization

### Add New Candidates

Edit `candidate_data.py` and add to the `CANDIDATES` dictionary:

```python
CANDIDATES = {
    "New Candidate": {
        "role": "Software Engineer",
        "experience_years": 5,
        "photo": "👨‍💻",
        "background": "Description here...",
        "metrics": {
            # Add metrics for all 5 factors
        },
        "timeline": [
            # Add career milestones
        ]
    }
}
```

### Adjust Factor Weights

Modify the `WEIGHTS` dictionary in `candidate_data.py`:

```python
WEIGHTS = {
    'learning_agility': 30,      # Change these values
    'skill_progression': 25,     # Must sum to 100
    'adaptability': 20,
    'innovation_mindset': 15,
    'feedback_integration': 10
}
```

### Modify Scoring Algorithms

Each factor has its own calculation method in the `GrowthPotentialScorer` class. You can adjust the formulas in `candidate_data.py`.

## 🎯 Use Cases

1. **Hiring Teams** - Make data-driven decisions with transparent scoring
2. **Recruiters** - Explain candidate rankings to hiring managers
3. **Candidates** - Understand what's valued and how to improve
4. **Research** - Study the impact of different growth factors
5. **Education** - Teach explainable AI and scoring systems

## 📈 Sample Candidates

The dashboard includes 3 diverse candidates:

1. **Sarah Chen** - Senior Software Engineer (Score: 78.4)
   - Strong in learning agility and adaptability
   - Fast career progression in cloud architecture

2. **Marcus Rodriguez** - Product Manager (Score: 67.8)
   - Multiple industry pivots
   - Strong contribution record

3. **Aisha Patel** - Data Scientist (Score: 74.9)
   - PhD background with strong innovation
   - Excellent publication record

## 🚧 Future Enhancements

- [x] File upload support for resumes and data
- [x] Resume-JD matching with AI
- [x] Interview question suggestions based on gaps
- [x] Download analysis reports
- [ ] Export candidate reports as PDF
- [ ] Connect to real API/database
- [ ] Machine learning predictions
- [ ] Team composition analysis
- [ ] Historical trend tracking
- [ ] Batch resume processing
- [ ] Advanced analytics dashboard

## 👥 Team

**Development:**
- Sai - Full-stack development, AI integration, feature implementation

**Product & Strategy:**
- Ritwij Aryan Parmar - Product vision, ideation, strategic direction

## 🤝 Contributing

This is a demonstration project for explainable hiring platforms. Feel free to fork and adapt for your needs!

### Tech Stack
- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **AI/LLM**: Groq API (Llama 3.3 70B)
- **Language**: Python 3.8+

## 📄 License

MIT License - Use freely for educational and commercial purposes

---

**Built to make explainability feel alive** ✨

*Part of a hiring platform innovation challenge - reimagining how candidate scoring can be transparent, interactive, and trustworthy.*
