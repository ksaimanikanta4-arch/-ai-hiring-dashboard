"""
Growth Potential Explainer - Interactive Streamlit Dashboard
Making hiring scores ALIVE through interactive visualizations and what-if scenarios
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from groq import Groq
from candidate_data import (
    CANDIDATES,
    get_candidate_scores,
    get_all_candidates_summary,
    GrowthPotentialScorer,
    CareerTrajectoryAnalyzer
)

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Growth Potential Explainer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .score-excellent {
        color: #10b981;
        font-weight: 700;
    }
    .score-good {
        color: #3b82f6;
        font-weight: 700;
    }
    .score-developing {
        color: #f59e0b;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_radar_chart(sub_scores, candidate_name):
    """Create a radar chart for sub-factor scores"""
    categories = [k.replace('_', ' ').title() for k in sub_scores.keys()]
    values = list(sub_scores.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=candidate_name,
        fillcolor='rgba(102, 126, 234, 0.5)',
        line=dict(color='rgba(102, 126, 234, 1)', width=2)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=80, r=80, t=40, b=40)
    )

    return fig


def create_timeline_chart(timeline_data):
    """Create an interactive timeline of candidate's career progression"""
    df = pd.DataFrame(timeline_data)

    # Color mapping for event types
    color_map = {
        'role': '#667eea',
        'certification': '#10b981',
        'achievement': '#f59e0b'
    }

    df['color'] = df['type'].map(color_map)

    fig = go.Figure()

    for event_type in df['type'].unique():
        df_type = df[df['type'] == event_type]
        fig.add_trace(go.Scatter(
            x=df_type['year'],
            y=[event_type] * len(df_type),
            mode='markers+text',
            name=event_type.title(),
            marker=dict(
                size=20,
                color=color_map[event_type],
                symbol='circle',
                line=dict(width=2, color='white')
            ),
            text=df_type['event'],
            textposition="top center",
            textfont=dict(size=9),
            hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
        ))

    fig.update_layout(
        title="Career Growth Timeline",
        xaxis_title="Year",
        yaxis=dict(
            tickmode='array',
            tickvals=['role', 'certification', 'achievement'],
            ticktext=['Role Changes', 'Certifications', 'Achievements']
        ),
        height=350,
        hovermode='closest',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def create_comparison_chart(candidates_data):
    """Create comparison chart for multiple candidates"""
    df = pd.DataFrame(candidates_data)

    fig = go.Figure()

    # Create grouped bar chart
    fig.add_trace(go.Bar(
        x=df['name'],
        y=df['score'],
        marker=dict(
            color=df['score'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Score")
        ),
        text=df['score'],
        textposition='outside',
        texttemplate='<b>%{text:.1f}</b>',
        hovertemplate='<b>%{x}</b><br>Growth Potential: %{y:.1f}/100<extra></extra>'
    ))

    fig.update_layout(
        title="Growth Potential Comparison",
        xaxis_title="Candidate",
        yaxis_title="Growth Potential Score",
        yaxis=dict(range=[0, 110]),
        height=400,
        showlegend=False
    )

    return fig


def create_factor_breakdown_chart(sub_scores):
    """Create horizontal bar chart showing factor contributions"""
    scorer = GrowthPotentialScorer()

    factors = list(sub_scores.keys())
    scores = list(sub_scores.values())
    weights = [scorer.WEIGHTS[f] for f in factors]
    contributions = [s * (w/100) for s, w in zip(scores, weights)]

    labels = [f.replace('_', ' ').title() for f in factors]

    df = pd.DataFrame({
        'Factor': labels,
        'Score': scores,
        'Weight': [f"{w}%" for w in weights],
        'Contribution': contributions
    })

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df['Factor'],
        x=df['Contribution'],
        orientation='h',
        marker=dict(
            color=df['Score'],
            colorscale='RdYlGn',
            showscale=False,
            line=dict(color='white', width=1)
        ),
        text=[f"{s:.0f} (×{w})" for s, w in zip(df['Score'], df['Weight'])],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Score: %{text}<br>Contribution: %{x:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title="Score Breakdown by Factor",
        xaxis_title="Weighted Contribution to Overall Score",
        yaxis_title="",
        height=350,
        xaxis=dict(range=[0, max(contributions) * 1.2])
    )

    return fig


def create_seniority_progression_chart(progression, candidate_name):
    """Create line chart showing seniority level progression over time"""
    if not progression:
        return None

    years = [p['year'] for p in progression]
    levels = [p['level'] for p in progression]
    events = [p['event'] for p in progression]

    fig = go.Figure()

    # Line chart with markers
    fig.add_trace(go.Scatter(
        x=years,
        y=levels,
        mode='lines+markers',
        name=candidate_name,
        line=dict(color='#667eea', width=3),
        marker=dict(
            size=12,
            color='#667eea',
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        text=events,
        hovertemplate='<b>%{text}</b><br>Year: %{x}<br>Level: %{y}<extra></extra>'
    ))

    # Add shaded regions for different seniority levels
    fig.add_hrect(y0=0.5, y1=1.5, fillcolor="rgba(254, 226, 226, 0.3)", line_width=0)
    fig.add_hrect(y0=1.5, y1=2.5, fillcolor="rgba(219, 234, 254, 0.3)", line_width=0)
    fig.add_hrect(y0=2.5, y1=3.5, fillcolor="rgba(209, 250, 229, 0.3)", line_width=0)
    fig.add_hrect(y0=3.5, y1=4.5, fillcolor="rgba(254, 249, 195, 0.3)", line_width=0)
    fig.add_hrect(y0=4.5, y1=5.5, fillcolor="rgba(233, 213, 255, 0.3)", line_width=0)

    fig.update_layout(
        title=f"Seniority Progression: {candidate_name}",
        xaxis_title="Year",
        yaxis_title="Seniority Level",
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=list(CareerTrajectoryAnalyzer.SENIORITY_LABELS.values()),
            range=[0.5, 5.5]
        ),
        height=400,
        hovermode='closest'
    )

    return fig


def create_trajectory_comparison_chart(candidates_data):
    """Create comparison chart showing seniority progression for multiple candidates"""
    fig = go.Figure()

    colors = ['#667eea', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

    for idx, (name, progression) in enumerate(candidates_data.items()):
        if not progression:
            continue

        years = [p['year'] for p in progression]
        levels = [p['level'] for p in progression]

        fig.add_trace(go.Scatter(
            x=years,
            y=levels,
            mode='lines+markers',
            name=name,
            line=dict(color=colors[idx % len(colors)], width=3),
            marker=dict(size=10, line=dict(width=2, color='white')),
            hovertemplate=f'<b>{name}</b><br>Year: %{{x}}<br>Level: %{{y}}<extra></extra>'
        ))

    fig.update_layout(
        title="Career Trajectory Comparison",
        xaxis_title="Year",
        yaxis_title="Seniority Level",
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=list(CareerTrajectoryAnalyzer.SENIORITY_LABELS.values()),
            range=[0.5, 5.5]
        ),
        height=500,
        hovermode='closest',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )

    return fig


# ============================================================================
# INTERACTIVE FEATURES
# ============================================================================

def what_if_simulator():
    """Interactive what-if scenario simulator"""
    st.subheader("🔮 What-If Scenario Simulator")
    st.markdown("Adjust the parameters below to see how they affect the Growth Potential score in real-time.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Learning Agility")
        certifications = st.slider("Certifications Earned", 0, 10, 3, key="cert")
        courses = st.slider("Courses Completed (12 months)", 0, 20, 8, key="courses")
        learning_vel = st.slider("Learning Velocity (months between skills)", 1, 12, 4, key="vel",
                                 help="Lower is better - how many months between acquiring new skills")

        st.markdown("#### Skill Progression")
        role_trans = st.slider("Role Transitions", 0, 5, 2, key="roles")
        tech_stack = st.slider("Tech Stack Breadth", 0, 20, 10, key="tech")
        seniority = st.slider("Years to Current Level", 1, 15, 5, key="sen",
                             help="Lower is better - faster progression")

    with col2:
        st.markdown("#### Adaptability")
        industry_sw = st.slider("Industry Switches", 0, 5, 1, key="ind")
        domain_piv = st.slider("Domain Pivots", 0, 5, 1, key="pivot")
        challenge = st.slider("Challenge Response (Interview)", 0, 10, 7, key="chal")

        st.markdown("#### Innovation & Feedback")
        projects = st.slider("Side Projects", 0, 10, 3, key="proj")
        contributions = st.slider("Team Contributions", 0, 15, 5, key="contrib")
        patents = st.slider("Patents/Publications", 0, 10, 2, key="pat")
        improvements = st.slider("Performance Improvements", 0, 10, 3, key="imp")
        mentorship = st.slider("Mentorship Seeking (0-10)", 0, 10, 6, key="ment")
        self_aware = st.slider("Self-Awareness (0-10)", 0, 10, 7, key="aware")

    # Calculate scores based on user input
    scorer = GrowthPotentialScorer()

    sim_scores = {
        'learning_agility': scorer.calculate_learning_agility(certifications, courses, learning_vel),
        'skill_progression': scorer.calculate_skill_progression(role_trans, tech_stack, seniority),
        'adaptability': scorer.calculate_adaptability(industry_sw, domain_piv, challenge),
        'innovation_mindset': scorer.calculate_innovation_mindset(projects, contributions, patents),
        'feedback_integration': scorer.calculate_feedback_integration(improvements, mentorship, self_aware)
    }

    sim_overall = scorer.calculate_overall_score(sim_scores)
    sim_explanation = scorer.get_score_explanation(sim_scores, sim_overall)

    # Display results
    st.markdown("---")
    st.markdown("### 📊 Simulated Results")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Score gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=sim_overall,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Score", 'font': {'size': 24}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "#667eea"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 60], 'color': '#fee2e2'},
                    {'range': [60, 75], 'color': '#dbeafe'},
                    {'range': [75, 100], 'color': '#d1fae5'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        st.markdown(sim_explanation)

    # Radar chart
    st.plotly_chart(create_radar_chart(sim_scores, "Simulated Candidate"), use_container_width=True)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_candidate_context(candidate_name):
    """Build comprehensive context about a candidate for the AI assistant"""
    candidate = CANDIDATES[candidate_name]
    sub_scores, overall_score, explanation = get_candidate_scores(candidate_name)

    context = f"""
CANDIDATE PROFILE: {candidate_name}
Role: {candidate['role']}
Experience: {candidate['experience_years']} years
Background: {candidate['background']}

GROWTH POTENTIAL SCORE: {overall_score}/100

SUB-FACTOR SCORES:
"""
    for factor, score in sub_scores.items():
        factor_name = factor.replace('_', ' ').title()
        weight = GrowthPotentialScorer.WEIGHTS[factor]
        context += f"- {factor_name}: {score:.1f}/100 (Weight: {weight}%)\n"

    context += "\nDETAILED METRICS:\n"
    for factor_key, metrics in candidate['metrics'].items():
        factor_name = factor_key.replace('_', ' ').title()
        context += f"\n{factor_name}:\n"
        for metric, value in metrics.items():
            context += f"  - {metric.replace('_', ' ').title()}: {value}\n"

    context += "\nCAREER TIMELINE:\n"
    for item in sorted(candidate['timeline'], key=lambda x: x['year']):
        context += f"- {item['year']}: {item['event']} ({item['type']})\n"

    return context


def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract text content"""
    try:
        file_type = uploaded_file.type
        file_name = uploaded_file.name

        # Handle different file types
        if file_type == "text/plain" or file_name.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
            return f"FILE: {file_name}\n\n{content}"

        elif file_type == "application/json" or file_name.endswith('.json'):
            import json
            content = json.loads(uploaded_file.read().decode('utf-8'))
            return f"FILE: {file_name}\n\n{json.dumps(content, indent=2)}"

        elif file_type == "text/csv" or file_name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            return f"FILE: {file_name}\n\nCSV Data Preview (first 50 rows):\n{df.head(50).to_string()}\n\nTotal Rows: {len(df)}\nColumns: {', '.join(df.columns)}"

        elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            df = pd.read_excel(uploaded_file)
            return f"FILE: {file_name}\n\nExcel Data Preview (first 50 rows):\n{df.head(50).to_string()}\n\nTotal Rows: {len(df)}\nColumns: {', '.join(df.columns)}"

        elif file_type == "application/pdf" or file_name.endswith('.pdf'):
            # For PDF, we'll provide a basic message
            # You can add PyPDF2 or pdfplumber for actual PDF parsing
            return f"FILE: {file_name}\n\nPDF file uploaded. Note: Full PDF text extraction requires additional libraries (PyPDF2/pdfplumber)."

        else:
            return f"FILE: {file_name}\n\nUnsupported file type: {file_type}"

    except Exception as e:
        return f"Error processing file: {str(e)}"


# ============================================================================
# AI ASSISTANT & RESUME MATCHER
# ============================================================================

def gpt_assistant():
    """AI-powered chat assistant to explain candidate scores"""
    st.subheader("🤖 AI Assistant")

    # Try to load API key from environment variable first
    api_key = os.getenv("GROQ_API_KEY")

    # If not in environment, show input field
    if not api_key:
        api_key = st.text_input(
            "Enter your Groq API Key",
            type="password",
            help="Get your free API key from https://console.groq.com/keys (or add to .env file)"
        )
    else:
        st.success("✅ API key loaded from environment variable")

    if not api_key:
        st.info("👆 Please enter your Groq API key to start chatting. Get a free key at https://console.groq.com/keys")
        st.markdown("""
        **What you can do:**
        - 📊 Ask about candidate Growth Potential scores
        - 🎯 Match resumes to job descriptions
        - 📈 Compare candidates
        - 💡 Get hiring insights

        **Tip:** You can also create a `.env` file with `GROQ_API_KEY=your_key_here`
        """)
        return

    # Initialize Groq client
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {str(e)}")
        return

    # Create tabs for different modes
    mode_tab1, mode_tab2 = st.tabs(["💬 Chat Assistant", "🎯 Resume-JD Matcher"])

    with mode_tab1:
        st.markdown("Ask me anything about the candidates, their scores, or how the Growth Potential assessment works!")

        # File uploader
        uploaded_file = st.file_uploader(
            "📎 Upload a file (optional)",
            type=['txt', 'csv', 'json', 'xlsx', 'xls', 'pdf'],
            help="Upload candidate data, resumes, or any relevant document to discuss with the AI",
            key="chat_file_upload"
        )

        # Initialize file content in session state
        if "uploaded_file_content" not in st.session_state:
            st.session_state.uploaded_file_content = None

        # Process uploaded file
        if uploaded_file is not None:
            with st.spinner("Processing uploaded file..."):
                file_content = process_uploaded_file(uploaded_file)
                st.session_state.uploaded_file_content = file_content
                st.success(f"✅ File '{uploaded_file.name}' processed successfully!")

                # Show preview in expander
                with st.expander("📄 View uploaded file preview"):
                    st.text(file_content[:1000] + ("..." if len(file_content) > 1000 else ""))

        # Option to clear uploaded file
        if st.session_state.uploaded_file_content is not None:
            if st.button("🗑️ Clear uploaded file", key="clear_chat_file"):
                st.session_state.uploaded_file_content = None
                st.rerun()

        st.markdown("---")

        # Candidate selector (in Chat Assistant tab)
        candidate_name = st.selectbox(
            "Select a candidate to discuss (or ask general questions)",
            ["All Candidates"] + list(CANDIDATES.keys())
        )

        # Build context
        if candidate_name == "All Candidates":
            context = "OVERVIEW OF ALL CANDIDATES:\n\n"
            for name in CANDIDATES.keys():
                sub_scores, overall_score, _ = get_candidate_scores(name)
                context += f"\n{name}:\n"
                context += f"- Overall Score: {overall_score}/100\n"
                context += f"- Role: {CANDIDATES[name]['role']}\n"
                for factor, score in sub_scores.items():
                    context += f"- {factor.replace('_', ' ').title()}: {score:.1f}/100\n"
        else:
            context = get_candidate_context(candidate_name)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask me anything about the candidates..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Build messages for Groq
                        system_message = f"""You are an expert hiring analyst explaining Growth Potential scores for candidates.
You have access to detailed candidate data and scoring metrics.

{context}

SCORING METHODOLOGY:
The Growth Potential score is calculated using 5 weighted factors:
1. Learning Agility (30%): Speed of skill acquisition, certifications, courses
2. Skill Progression (25%): Career trajectory, role transitions, tech stack breadth
3. Adaptability (20%): Industry switches, domain pivots, challenge response
4. Innovation Mindset (15%): Side projects, contributions, patents/publications
5. Feedback Integration (10%): Performance improvements, mentorship, self-awareness

Provide clear, insightful explanations. Use specific numbers and examples from the candidate data.
Be conversational but professional. If asked to compare, provide balanced analysis."""

                        # Add uploaded file content to system message if available
                        if st.session_state.uploaded_file_content:
                            system_message += f"\n\nADDITIONAL UPLOADED DOCUMENT:\n{st.session_state.uploaded_file_content}"

                        messages = [{"role": "system", "content": system_message}]

                        # Add conversation history (last 5 messages)
                        for msg in st.session_state.messages[-5:]:
                            messages.append({"role": msg["role"], "content": msg["content"]})

                        # Call Groq API
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=messages,
                            temperature=0.7,
                            max_tokens=1000
                        )

                        assistant_message = response.choices[0].message.content
                        st.markdown(assistant_message)

                        # Save assistant response
                        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")

        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    with mode_tab2:
        st.markdown("Upload a resume and paste a job description to get an AI-powered match analysis with scoring!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📄 Resume")
            resume_file = st.file_uploader(
                "Upload Resume",
                type=['txt', 'pdf', 'doc', 'docx'],
                help="Upload the candidate's resume",
                key="resume_upload"
            )

            if resume_file:
                resume_content = process_uploaded_file(resume_file)
                with st.expander("👀 View resume preview"):
                    st.text(resume_content[:500] + ("..." if len(resume_content) > 500 else ""))

        with col2:
            st.markdown("#### 📋 Job Description")
            job_description = st.text_area(
                "Paste Job Description",
                height=200,
                placeholder="Paste the full job description here...",
                key="jd_input"
            )

        # Match button
        if st.button("🎯 Analyze Match", type="primary", use_container_width=True):
            if not resume_file:
                st.error("Please upload a resume first!")
            elif not job_description:
                st.error("Please paste a job description!")
            else:
                with st.spinner("Analyzing resume-job match..."):
                    try:
                        resume_content = process_uploaded_file(resume_file)

                        # Build matching prompt
                        matching_prompt = f"""You are an expert technical recruiter and hiring analyst. Analyze the match between this resume and job description.

RESUME:
{resume_content}

JOB DESCRIPTION:
{job_description}

Please provide a comprehensive match analysis with the following structure:

1. OVERALL MATCH SCORE: Provide a score out of 100 with justification

2. KEY STRENGTHS (matching points):
   - List specific skills, experiences, and qualifications from the resume that match the JD
   - Explain why each is relevant

3. GAPS & WEAKNESSES (missing requirements):
   - List requirements from the JD that are not clearly present in the resume
   - Assess the severity of each gap

4. DETAILED SCORING BREAKDOWN:
   - Technical Skills Match: X/100
   - Experience Level Match: X/100
   - Domain/Industry Match: X/100
   - Education/Certifications Match: X/100
   - Soft Skills/Culture Fit: X/100

5. RECOMMENDATION:
   - Strong Match (75-100): Proceed to interview
   - Moderate Match (50-74): Consider with reservations
   - Weak Match (0-49): Not recommended

6. SUGGESTED INTERVIEW QUESTIONS:
   - 3-5 specific questions to ask based on gaps or areas needing clarification

Be specific, use bullet points, and reference concrete examples from both documents."""

                        messages = [
                            {"role": "system", "content": "You are an expert technical recruiter and hiring analyst."},
                            {"role": "user", "content": matching_prompt}
                        ]

                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=messages,
                            temperature=0.5,
                            max_tokens=2000
                        )

                        match_analysis = response.choices[0].message.content

                        # Store in session state for follow-up questions
                        st.session_state.match_analysis = match_analysis
                        st.session_state.match_resume_content = resume_content
                        st.session_state.match_jd_content = job_description
                        st.session_state.match_resume_filename = resume_file.name

                    except Exception as e:
                        st.error(f"Error analyzing match: {str(e)}")

        # Display match analysis if it exists
        if "match_analysis" in st.session_state and st.session_state.match_analysis:
            st.markdown("---")
            st.markdown("### 📊 Match Analysis Results")
            st.markdown(st.session_state.match_analysis)

            # Add download button for the analysis
            st.download_button(
                label="📥 Download Analysis",
                data=st.session_state.match_analysis,
                file_name=f"match_analysis_{st.session_state.match_resume_filename}.txt",
                mime="text/plain",
                key="download_analysis"
            )

            # Follow-up questions section
            st.markdown("---")
            st.markdown("### 💬 Ask Follow-up Questions")
            st.markdown("Have questions about the match analysis? Ask away!")

            # Initialize matcher chat history
            if "matcher_chat_messages" not in st.session_state:
                st.session_state.matcher_chat_messages = []

            # Display matcher chat history
            for message in st.session_state.matcher_chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Chat input for follow-up questions
            if followup_prompt := st.chat_input("Ask a follow-up question about this match...", key="matcher_chat_input"):
                # Add user message
                st.session_state.matcher_chat_messages.append({"role": "user", "content": followup_prompt})
                with st.chat_message("user"):
                    st.markdown(followup_prompt)

                # Generate AI response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            # Build context-aware system message
                            followup_system_message = f"""You are an expert technical recruiter and hiring analyst. You previously analyzed a resume-job description match.

RESUME:
{st.session_state.match_resume_content}

JOB DESCRIPTION:
{st.session_state.match_jd_content}

PREVIOUS MATCH ANALYSIS:
{st.session_state.match_analysis}

The user has follow-up questions about this match analysis. Answer their questions with specific references to the resume, job description, and your previous analysis. Be helpful, detailed, and actionable."""

                            followup_messages = [{"role": "system", "content": followup_system_message}]

                            # Add conversation history (last 10 messages for context)
                            for msg in st.session_state.matcher_chat_messages[-10:]:
                                followup_messages.append({"role": msg["role"], "content": msg["content"]})

                            # Call Groq API
                            followup_response = client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=followup_messages,
                                temperature=0.6,
                                max_tokens=1500
                            )

                            assistant_message = followup_response.choices[0].message.content
                            st.markdown(assistant_message)

                            # Save assistant response
                            st.session_state.matcher_chat_messages.append({"role": "assistant", "content": assistant_message})

                        except Exception as e:
                            st.error(f"Error generating response: {str(e)}")

            # Clear conversation button
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("🗑️ Clear Chat", key="clear_matcher_chat"):
                    st.session_state.matcher_chat_messages = []
                    st.rerun()
            with col2:
                if st.button("🔄 New Analysis", key="reset_matcher"):
                    st.session_state.match_analysis = None
                    st.session_state.match_resume_content = None
                    st.session_state.match_jd_content = None
                    st.session_state.match_resume_filename = None
                    st.session_state.matcher_chat_messages = []
                    st.rerun()

        else:
            st.markdown("---")
            st.info("💡 **Tip:** The AI will analyze technical skills, experience, education, and provide a detailed scoring breakdown with actionable recommendations.")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point with navigation and routing"""

    # Header
    st.markdown('<h1 class="main-header">📈 Growth Potential Explainer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Making hiring scores come alive through interactive explainability</p>',
                unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["🏠 Dashboard", "👥 Candidate Deep Dive", "🔍 Compare Candidates", "🔮 What-If Simulator", "🤖 AI Assistant"],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 About Growth Potential")
    st.sidebar.markdown("""
    Growth Potential measures a candidate's ability to:
    - **Learn & Adapt** quickly
    - **Progress** in their career
    - **Innovate** and contribute
    - **Integrate feedback** effectively
    """)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚖️ Factor Weights")
    weights = GrowthPotentialScorer.WEIGHTS
    for factor, weight in weights.items():
        st.sidebar.markdown(f"**{factor.replace('_', ' ').title()}:** {weight}%")

    # Page routing
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "👥 Candidate Deep Dive":
        show_candidate_details()
    elif page == "🔍 Compare Candidates":
        show_comparison()
    elif page == "🔮 What-If Simulator":
        what_if_simulator()
    elif page == "🤖 AI Assistant":
        gpt_assistant()


# ============================================================================
# PAGE RENDERING FUNCTIONS
# ============================================================================

def show_dashboard():
    """Show overview dashboard"""
    st.header("Candidate Rankings")

    # Get all candidates
    summary = get_all_candidates_summary()

    # Display ranking cards
    cols = st.columns(3)
    for idx, candidate in enumerate(summary):
        with cols[idx]:
            score_class = "score-excellent" if candidate['score'] >= 75 else \
                         "score-good" if candidate['score'] >= 60 else "score-developing"

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                <div style='font-size: 3rem;'>{candidate['photo']}</div>
                <h3>{candidate['name']}</h3>
                <p>{candidate['role']}</p>
                <h1 style='font-size: 3rem; margin: 1rem 0;'>{candidate['score']}</h1>
                <p style='font-size: 0.9rem;'>Growth Potential Score</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Comparison chart
    st.plotly_chart(create_comparison_chart(summary), use_container_width=True)

    # Quick insights
    st.subheader("💡 Quick Insights")
    col1, col2, col3 = st.columns(3)

    top_candidate = summary[0]
    avg_score = np.mean([c['score'] for c in summary])

    with col1:
        st.metric("Top Candidate", top_candidate['name'], f"{top_candidate['score']}/100")
    with col2:
        st.metric("Average Score", f"{avg_score:.1f}", "")
    with col3:
        st.metric("Candidates Evaluated", len(summary), "")


def show_candidate_details():
    """Show detailed analysis for a specific candidate"""
    candidate_name = st.selectbox("Select Candidate", list(CANDIDATES.keys()))

    candidate = CANDIDATES[candidate_name]
    sub_scores, overall_score, explanation = get_candidate_scores(candidate_name)

    # Header with photo and basic info
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"<div style='font-size: 8rem; text-align: center;'>{candidate['photo']}</div>",
                   unsafe_allow_html=True)
    with col2:
        st.title(candidate_name)
        st.subheader(candidate['role'])
        st.markdown(f"**Experience:** {candidate['experience_years']} years")
        st.markdown(candidate['background'])

    st.markdown("---")

    # Score overview
    col1, col2 = st.columns([1, 2])

    with col1:
        # Gauge chart for overall score
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Growth Potential", 'font': {'size': 20}},
            number={'font': {'size': 60}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#667eea"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 60], 'color': '#fee2e2'},
                    {'range': [60, 75], 'color': '#dbeafe'},
                    {'range': [75, 100], 'color': '#d1fae5'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_gauge.update_layout(height=400, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        st.markdown(explanation)

    st.markdown("---")

    # Get trajectory metrics
    trajectory = CareerTrajectoryAnalyzer.get_trajectory_metrics(candidate_name)

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Factor Breakdown", "🚀 Career Trajectory", "📈 Career Timeline", "🔬 Deep Metrics"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_radar_chart(sub_scores, candidate_name), use_container_width=True)
        with col2:
            st.plotly_chart(create_factor_breakdown_chart(sub_scores), use_container_width=True)

    with tab2:
        # Career Trajectory Analysis
        st.markdown(trajectory['narrative'])

        st.markdown("---")

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Trajectory Pattern",
                trajectory['pattern'],
                help="Classification based on career progression pattern"
            )

        with col2:
            st.metric(
                "Velocity",
                f"{trajectory['velocity']} levels/year",
                help="Rate of seniority progression"
            )

        with col3:
            st.metric(
                "Levels Gained",
                trajectory['levels_gained'],
                help="Total seniority levels advanced"
            )

        with col4:
            current_level_label = CareerTrajectoryAnalyzer.SENIORITY_LABELS.get(trajectory['current_level'], "Unknown")
            st.metric(
                "Current Level",
                current_level_label,
                help="Current seniority level"
            )

        st.markdown("---")

        # Seniority Progression Chart
        progression_chart = create_seniority_progression_chart(trajectory['progression'], candidate_name)
        if progression_chart:
            st.plotly_chart(progression_chart, use_container_width=True)

        # Promotion Timeline
        if trajectory['promotions']:
            st.subheader("📊 Promotion History Details")

            promo_data = []
            for promo in trajectory['promotions']:
                from_label = CareerTrajectoryAnalyzer.SENIORITY_LABELS.get(promo['from_level'], "Unknown")
                to_label = CareerTrajectoryAnalyzer.SENIORITY_LABELS.get(promo['to_level'], "Unknown")
                promo_data.append({
                    'Year': f"{promo['from_year']} → {promo['to_year']}",
                    'Promotion': f"{from_label} → {to_label}",
                    'Time (Years)': promo['years'],
                    'From Role': promo['from_role'],
                    'To Role': promo['to_role']
                })

            promo_df = pd.DataFrame(promo_data)
            st.dataframe(promo_df, use_container_width=True, hide_index=True)

            # Average promotion time
            avg_time = np.mean([p['years'] for p in trajectory['promotions']])
            st.info(f"⏱️ **Average time between promotions:** {avg_time:.1f} years")

    with tab3:
        st.plotly_chart(create_timeline_chart(candidate['timeline']), use_container_width=True)

        # Timeline details
        st.subheader("Career Milestones")
        for item in sorted(candidate['timeline'], key=lambda x: x['year'], reverse=True):
            icon = "🎯" if item['type'] == 'role' else "🎓" if item['type'] == 'certification' else "⭐"
            st.markdown(f"**{item['year']}** {icon} {item['event']}")

    with tab4:
        st.subheader("Detailed Metrics Breakdown")

        for factor_key, metrics in candidate['metrics'].items():
            factor_name = factor_key.replace('_', ' ').title()
            score = sub_scores[factor_key]

            with st.expander(f"{factor_name} - Score: {score:.0f}/100"):
                for metric, value in metrics.items():
                    st.markdown(f"**{metric.replace('_', ' ').title()}:** {value}")


def show_comparison():
    """Show side-by-side comparison of all candidates"""
    st.header("🔍 Candidate Comparison")

    # Create tabs for different comparison views
    comp_tab1, comp_tab2 = st.tabs(["📊 Growth Potential Scores", "🚀 Career Trajectory"])

    with comp_tab1:
        # Calculate all scores
        comparison_data = []
        for name in CANDIDATES.keys():
            sub_scores, overall_score, _ = get_candidate_scores(name)
            comparison_data.append({
                'Candidate': name,
                'Overall': overall_score,
                **{k.replace('_', ' ').title(): v for k, v in sub_scores.items()}
            })

        df = pd.DataFrame(comparison_data)

        # Heatmap
        st.subheader("Score Heatmap")

        fig_heatmap = go.Figure(data=go.Heatmap(
            z=df.iloc[:, 1:].values.T,
            x=df['Candidate'],
            y=df.columns[1:],
            colorscale='RdYlGn',
            text=df.iloc[:, 1:].values.T,
            texttemplate='%{text:.0f}',
            textfont={"size": 14},
            colorbar=dict(title="Score")
        ))

        fig_heatmap.update_layout(
            height=500,
            xaxis_title="Candidate",
            yaxis_title="Factor"
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Detailed comparison table
        st.subheader("Detailed Scores")

        # Style the dataframe
        def highlight_max(s):
            is_max = s == s.max()
            return ['background-color: #d1fae5' if v else '' for v in is_max]

        styled_df = df.style.apply(highlight_max, subset=df.columns[1:])
        st.dataframe(styled_df, use_container_width=True)

        # Factor-by-factor comparison
        st.subheader("Factor-by-Factor Comparison")

        factor_cols = df.columns[2:]  # Skip 'Candidate' and 'Overall'
        selected_factor = st.selectbox("Select Factor to Compare", factor_cols)

        fig_factor = go.Figure()

        fig_factor.add_trace(go.Bar(
            x=df['Candidate'],
            y=df[selected_factor],
            marker=dict(
                color=df[selected_factor],
                colorscale='Viridis',
                showscale=True
            ),
            text=df[selected_factor],
            texttemplate='%{text:.1f}',
            textposition='outside'
        ))

        fig_factor.update_layout(
            title=f"{selected_factor} Comparison",
            xaxis_title="Candidate",
            yaxis_title="Score",
            yaxis=dict(range=[0, 110]),
            height=400
        )

        st.plotly_chart(fig_factor, use_container_width=True)

    with comp_tab2:
        st.subheader("Career Trajectory Comparison")

        # Get trajectory data for all candidates
        trajectory_data = {}
        trajectory_metrics = {}

        for name in CANDIDATES.keys():
            metrics = CareerTrajectoryAnalyzer.get_trajectory_metrics(name)
            trajectory_data[name] = metrics['progression']
            trajectory_metrics[name] = metrics

        # Trajectory comparison chart
        st.plotly_chart(create_trajectory_comparison_chart(trajectory_data), use_container_width=True)

        st.markdown("---")

        # Trajectory metrics comparison table
        st.subheader("Trajectory Metrics Comparison")

        metrics_data = []
        for name, metrics in trajectory_metrics.items():
            current_level_label = CareerTrajectoryAnalyzer.SENIORITY_LABELS.get(metrics['current_level'], "Unknown")
            avg_promo_time = np.mean([p['years'] for p in metrics['promotions']]) if metrics['promotions'] else 0

            metrics_data.append({
                'Candidate': name,
                'Pattern': metrics['pattern'],
                'Current Level': current_level_label,
                'Levels Gained': metrics['levels_gained'],
                'Velocity (levels/year)': metrics['velocity'],
                'Avg Promotion Time (years)': f"{avg_promo_time:.1f}" if avg_promo_time > 0 else "N/A",
                'Acceleration': metrics['acceleration'].title()
            })

        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Individual candidate trajectories
        st.subheader("Individual Trajectory Details")

        selected_candidate = st.selectbox("Select candidate to view detailed trajectory", list(CANDIDATES.keys()), key="traj_select")

        if selected_candidate:
            selected_metrics = trajectory_metrics[selected_candidate]
            st.markdown(selected_metrics['narrative'])


if __name__ == "__main__":
    main()
