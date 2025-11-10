"""
Candidate data model and scoring logic for Growth Potential assessment
"""
import numpy as np
from datetime import datetime, timedelta

class GrowthPotentialScorer:
    """Calculates Growth Potential score based on multiple sub-factors"""

    # Weights for each sub-factor (must sum to 100)
    WEIGHTS = {
        'learning_agility': 30,
        'skill_progression': 25,
        'adaptability': 20,
        'innovation_mindset': 15,
        'feedback_integration': 10
    }

    @staticmethod
    def calculate_learning_agility(certifications, courses_completed, learning_velocity):
        """
        Learning Agility: How quickly they acquire new skills
        - certifications: number of certifications earned
        - courses_completed: courses in last 12 months
        - learning_velocity: months between skill acquisitions (lower is better)
        """
        cert_score = min(certifications * 15, 40)
        course_score = min(courses_completed * 5, 30)
        velocity_score = max(30 - learning_velocity * 3, 0)
        return min((cert_score + course_score + velocity_score) / 100 * 100, 100)

    @staticmethod
    def calculate_skill_progression(role_transitions, tech_stack_breadth, seniority_growth):
        """
        Skill Progression: Career trajectory and skill development
        - role_transitions: number of meaningful role changes
        - tech_stack_breadth: number of technologies mastered
        - seniority_growth: years to reach current level
        """
        transition_score = min(role_transitions * 20, 40)
        breadth_score = min(tech_stack_breadth * 4, 40)
        # Lower seniority_growth is better (faster progression)
        growth_score = max(30 - seniority_growth * 2, 10)
        return (transition_score + breadth_score + growth_score) / 110 * 100

    @staticmethod
    def calculate_adaptability(industry_switches, domain_pivots, challenge_response):
        """
        Adaptability: Ability to thrive in changing environments
        - industry_switches: times switched industries/domains
        - domain_pivots: major technology/role pivots
        - challenge_response: score from behavioral interviews (0-10)
        """
        switch_score = min(industry_switches * 25, 50)
        pivot_score = min(domain_pivots * 15, 30)
        response_score = challenge_response * 2
        return (switch_score + pivot_score + response_score) / 100 * 100

    @staticmethod
    def calculate_innovation_mindset(side_projects, contributions, patents_publications):
        """
        Innovation Mindset: Creative problem-solving and initiative
        - side_projects: personal/open-source projects
        - contributions: meaningful contributions to teams
        - patents_publications: patents, papers, or technical blogs
        """
        project_score = min(side_projects * 15, 45)
        contribution_score = min(contributions * 8, 35)
        ip_score = min(patents_publications * 10, 20)
        return (project_score + contribution_score + ip_score) / 100 * 100

    @staticmethod
    def calculate_feedback_integration(performance_improvements,
                                       mentorship_sought,
                                       self_awareness):
        """
        Feedback Integration: How well they learn from feedback
        - performance_improvements: documented improvements after feedback
        - mentorship_sought: actively seeks mentorship (0-10)
        - self_awareness: demonstrated self-awareness (0-10)
        """
        improvement_score = min(performance_improvements * 15, 40)
        mentorship_score = mentorship_sought * 3
        awareness_score = self_awareness * 3
        return (improvement_score + mentorship_score + awareness_score) / 100 * 100

    @classmethod
    def calculate_overall_score(cls, sub_scores):
        """Calculate weighted overall Growth Potential score"""
        total = 0
        for factor, weight in cls.WEIGHTS.items():
            total += sub_scores[factor] * (weight / 100)
        return round(total, 1)

    @classmethod
    def get_score_explanation(cls, sub_scores, overall_score):
        """Generate natural language explanation of the score"""
        strengths = []
        improvements = []

        for factor, score in sub_scores.items():
            factor_name = factor.replace('_', ' ').title()
            if score >= 75:
                strengths.append(f"{factor_name} ({score:.0f}/100)")
            elif score < 60:
                improvements.append(f"{factor_name} ({score:.0f}/100)")

        explanation = f"**Overall Growth Potential: {overall_score}/100**\n\n"

        if overall_score >= 75:
            explanation += "**Exceptional Growth Potential** - This candidate demonstrates outstanding ability to learn, adapt, and evolve.\n\n"
        elif overall_score >= 60:
            explanation += "**Strong Growth Potential** - This candidate shows solid potential for development and advancement.\n\n"
        else:
            explanation += "**Developing Growth Potential** - This candidate has room to strengthen their growth trajectory.\n\n"

        if strengths:
            explanation += "**Key Strengths:**\n"
            for s in strengths:
                explanation += f"- {s}\n"
            explanation += "\n"

        if improvements:
            explanation += "**Areas for Development:**\n"
            for i in improvements:
                explanation += f"- {i}\n"

        return explanation


# Dummy candidate data
CANDIDATES = {
    "Sarah Chen": {
        "role": "Senior Software Engineer",
        "experience_years": 6,
        "photo": "👩‍💻",
        "background": "Full-stack developer with focus on cloud architecture. Started as frontend developer, transitioned to backend, now leading microservices initiatives.",
        "metrics": {
            "learning_agility": {
                "certifications": 5,  # AWS, Kubernetes, etc.
                "courses_completed": 8,
                "learning_velocity": 4  # New skill every 4 months
            },
            "skill_progression": {
                "role_transitions": 3,  # Junior → Mid → Senior → Tech Lead
                "tech_stack_breadth": 12,
                "seniority_growth": 5  # Reached senior level in 5 years
            },
            "adaptability": {
                "industry_switches": 2,  # Finance → Healthcare
                "domain_pivots": 2,  # Frontend → Backend → DevOps
                "challenge_response": 9
            },
            "innovation_mindset": {
                "side_projects": 4,
                "contributions": 6,  # Led 6 major initiatives
                "patents_publications": 3  # Technical blogs
            },
            "feedback_integration": {
                "performance_improvements": 4,
                "mentorship_sought": 8,
                "self_awareness": 9
            }
        },
        "timeline": [
            {"year": 2019, "event": "Joined as Junior Frontend Dev", "type": "role", "seniority_level": 1},
            {"year": 2020, "event": "AWS Certified Solutions Architect", "type": "certification", "seniority_level": 1},
            {"year": 2020, "event": "Transitioned to Full-Stack", "type": "role", "seniority_level": 2},
            {"year": 2021, "event": "Led migration to microservices", "type": "achievement", "seniority_level": 2},
            {"year": 2022, "event": "Promoted to Senior Engineer", "type": "role", "seniority_level": 3},
            {"year": 2023, "event": "Kubernetes CKA certified", "type": "certification", "seniority_level": 3},
            {"year": 2024, "event": "Leading cloud architecture team", "type": "achievement", "seniority_level": 4}
        ]
    },
    "Marcus Rodriguez": {
        "role": "Product Manager",
        "experience_years": 8,
        "photo": "👨‍💼",
        "background": "Started as software engineer, pivoted to product management. Specialized in B2B SaaS products with focus on data analytics.",
        "metrics": {
            "learning_agility": {
                "certifications": 2,
                "courses_completed": 12,  # MBA courses, PM certifications
                "learning_velocity": 6
            },
            "skill_progression": {
                "role_transitions": 2,  # Engineer → Associate PM → Senior PM
                "tech_stack_breadth": 8,
                "seniority_growth": 7
            },
            "adaptability": {
                "industry_switches": 3,  # E-commerce → EdTech → FinTech
                "domain_pivots": 1,  # Engineering to Product
                "challenge_response": 8
            },
            "innovation_mindset": {
                "side_projects": 2,
                "contributions": 8,  # Product launches
                "patents_publications": 1
            },
            "feedback_integration": {
                "performance_improvements": 3,
                "mentorship_sought": 7,
                "self_awareness": 7
            }
        },
        "timeline": [
            {"year": 2017, "event": "Software Engineer at E-commerce startup", "type": "role", "seniority_level": 2},
            {"year": 2018, "event": "Transitioned to Associate PM", "type": "role", "seniority_level": 2},
            {"year": 2019, "event": "Launched mobile analytics platform", "type": "achievement", "seniority_level": 2},
            {"year": 2020, "event": "Switched to EdTech", "type": "role", "seniority_level": 2},
            {"year": 2021, "event": "Product Management Certification", "type": "certification", "seniority_level": 2},
            {"year": 2022, "event": "Senior PM at FinTech", "type": "role", "seniority_level": 3},
            {"year": 2024, "event": "Led $5M ARR product line", "type": "achievement", "seniority_level": 3}
        ]
    },
    "Aisha Patel": {
        "role": "Data Scientist",
        "experience_years": 4,
        "photo": "👩‍🔬",
        "background": "PhD in Machine Learning, now applying research to production systems. Focus on NLP and recommendation systems.",
        "metrics": {
            "learning_agility": {
                "certifications": 3,
                "courses_completed": 15,  # Continuous learner
                "learning_velocity": 3  # Very fast learner
            },
            "skill_progression": {
                "role_transitions": 2,  # Researcher → Data Scientist → Senior DS
                "tech_stack_breadth": 10,
                "seniority_growth": 3  # Fast progression
            },
            "adaptability": {
                "industry_switches": 1,
                "domain_pivots": 1,  # Research to Applied ML
                "challenge_response": 7
            },
            "innovation_mindset": {
                "side_projects": 6,  # Active in open source
                "contributions": 4,
                "patents_publications": 8  # Academic papers + patents
            },
            "feedback_integration": {
                "performance_improvements": 2,
                "mentorship_sought": 6,
                "self_awareness": 6
            }
        },
        "timeline": [
            {"year": 2020, "event": "PhD in Machine Learning", "type": "certification", "seniority_level": 2},
            {"year": 2021, "event": "Research Scientist at AI Lab", "type": "role", "seniority_level": 2},
            {"year": 2021, "event": "Published 3 papers at NeurIPS", "type": "achievement", "seniority_level": 2},
            {"year": 2022, "event": "Joined as Data Scientist", "type": "role", "seniority_level": 2},
            {"year": 2023, "event": "Patent for recommendation algorithm", "type": "achievement", "seniority_level": 3},
            {"year": 2023, "event": "Promoted to Senior Data Scientist", "type": "role", "seniority_level": 3},
            {"year": 2024, "event": "Leading ML Platform team", "type": "achievement", "seniority_level": 4}
        ]
    }
}


class CareerTrajectoryAnalyzer:
    """Analyzes career trajectory and seniority progression"""

    # Seniority level mapping
    SENIORITY_LABELS = {
        1: "Junior",
        2: "Mid-Level",
        3: "Senior",
        4: "Lead/Staff",
        5: "Principal/Director"
    }

    @staticmethod
    def get_seniority_progression(timeline):
        """Extract seniority progression from timeline"""
        # Get role changes only and sort by year
        role_changes = [item for item in timeline if item['type'] == 'role']
        role_changes.sort(key=lambda x: x['year'])

        progression = []
        for item in role_changes:
            progression.append({
                'year': item['year'],
                'level': item.get('seniority_level', 2),
                'event': item['event']
            })

        return progression

    @staticmethod
    def calculate_time_between_promotions(progression):
        """Calculate time between each promotion"""
        promotions = []
        for i in range(len(progression) - 1):
            if progression[i+1]['level'] > progression[i]['level']:
                time_diff = progression[i+1]['year'] - progression[i]['year']
                promotions.append({
                    'from_level': progression[i]['level'],
                    'to_level': progression[i+1]['level'],
                    'years': time_diff,
                    'from_year': progression[i]['year'],
                    'to_year': progression[i+1]['year'],
                    'from_role': progression[i]['event'],
                    'to_role': progression[i+1]['event']
                })
        return promotions

    @staticmethod
    def calculate_trajectory_velocity(progression, experience_years):
        """Calculate trajectory velocity (levels per year)"""
        if not progression or experience_years == 0:
            return 0

        start_level = progression[0]['level']
        end_level = progression[-1]['level']
        levels_gained = end_level - start_level

        velocity = levels_gained / experience_years
        return round(velocity, 2)

    @staticmethod
    def calculate_trajectory_acceleration(progression):
        """Calculate if trajectory is accelerating or decelerating"""
        promotions = CareerTrajectoryAnalyzer.calculate_time_between_promotions(progression)

        if len(promotions) < 2:
            return "stable"

        # Compare recent promotion speed to earlier ones
        recent_avg = np.mean([p['years'] for p in promotions[-2:]])
        earlier_avg = np.mean([p['years'] for p in promotions[:-2]]) if len(promotions) > 2 else recent_avg

        if recent_avg < earlier_avg * 0.8:
            return "accelerating"
        elif recent_avg > earlier_avg * 1.2:
            return "decelerating"
        else:
            return "stable"

    @staticmethod
    def classify_trajectory_pattern(progression, experience_years, promotions):
        """Classify trajectory into patterns"""
        if not progression or not promotions:
            return "Early Career"

        velocity = CareerTrajectoryAnalyzer.calculate_trajectory_velocity(progression, experience_years)
        avg_promotion_time = np.mean([p['years'] for p in promotions]) if promotions else float('inf')
        total_levels = progression[-1]['level'] - progression[0]['level']

        # Fast Riser: High velocity, quick promotions
        if velocity >= 0.4 and avg_promotion_time <= 2.5:
            return "Fast Riser 🚀"

        # Steady Climber: Consistent progression
        elif 0.25 <= velocity < 0.4 and 2 <= avg_promotion_time <= 4:
            return "Steady Climber 📈"

        # Lateral Explorer: Multiple switches, slower vertical growth
        elif total_levels <= 1 and len(progression) >= 3:
            return "Lateral Explorer 🔄"

        # Specialist: Stayed at similar level, deepening expertise
        elif total_levels == 0:
            return "Specialist 🎯"

        # Late Bloomer: Recent acceleration
        elif CareerTrajectoryAnalyzer.calculate_trajectory_acceleration(progression) == "accelerating":
            return "Late Bloomer 🌟"

        # Plateaued: Slowing progression
        elif CareerTrajectoryAnalyzer.calculate_trajectory_acceleration(progression) == "decelerating":
            return "Plateaued ⏸️"

        else:
            return "Developing 🌱"

    @staticmethod
    def generate_trajectory_narrative(candidate_name, progression, promotions, pattern, velocity, experience_years):
        """Generate natural language narrative about career trajectory"""
        if not progression:
            return "Insufficient career history data."

        start_level = CareerTrajectoryAnalyzer.SENIORITY_LABELS.get(progression[0]['level'], "Unknown")
        current_level = CareerTrajectoryAnalyzer.SENIORITY_LABELS.get(progression[-1]['level'], "Unknown")
        levels_gained = progression[-1]['level'] - progression[0]['level']

        narrative = f"**Career Trajectory: {pattern}**\n\n"
        narrative += f"{candidate_name} started as a **{start_level}** professional and is currently at the **{current_level}** level, "
        narrative += f"advancing **{levels_gained} level{'s' if levels_gained != 1 else ''}** over **{experience_years} years**.\n\n"

        # Velocity analysis
        if velocity >= 0.4:
            narrative += f"With a trajectory velocity of **{velocity} levels/year**, this represents **exceptional career acceleration** - significantly faster than industry averages.\n\n"
        elif velocity >= 0.25:
            narrative += f"With a trajectory velocity of **{velocity} levels/year**, this shows **solid career progression** at a healthy pace.\n\n"
        else:
            narrative += f"With a trajectory velocity of **{velocity} levels/year**, this indicates **steady, measured growth** with focus on skill deepening.\n\n"

        # Promotion details
        if promotions:
            narrative += "**Promotion History:**\n"
            for promo in promotions:
                from_label = CareerTrajectoryAnalyzer.SENIORITY_LABELS.get(promo['from_level'], "Unknown")
                to_label = CareerTrajectoryAnalyzer.SENIORITY_LABELS.get(promo['to_level'], "Unknown")
                narrative += f"- **{promo['from_year']} → {promo['to_year']}** ({promo['years']} {'year' if promo['years'] == 1 else 'years'}): "
                narrative += f"{from_label} to {to_label}\n"

            avg_time = np.mean([p['years'] for p in promotions])
            narrative += f"\n**Average time between promotions:** {avg_time:.1f} years\n"

            if avg_time <= 2:
                narrative += "⚡ This is exceptionally fast - well above market pace.\n"
            elif avg_time <= 3:
                narrative += "✨ This is faster than typical industry standards.\n"
            elif avg_time <= 5:
                narrative += "✓ This aligns with standard career progression timelines.\n"
            else:
                narrative += "⏳ This suggests a focus on mastery before advancement.\n"

        return narrative

    @staticmethod
    def get_trajectory_metrics(candidate_name):
        """Get all trajectory metrics for a candidate"""
        candidate = CANDIDATES[candidate_name]
        timeline = candidate['timeline']
        experience_years = candidate['experience_years']

        progression = CareerTrajectoryAnalyzer.get_seniority_progression(timeline)
        promotions = CareerTrajectoryAnalyzer.calculate_time_between_promotions(progression)
        velocity = CareerTrajectoryAnalyzer.calculate_trajectory_velocity(progression, experience_years)
        acceleration = CareerTrajectoryAnalyzer.calculate_trajectory_acceleration(progression)
        pattern = CareerTrajectoryAnalyzer.classify_trajectory_pattern(progression, experience_years, promotions)
        narrative = CareerTrajectoryAnalyzer.generate_trajectory_narrative(
            candidate_name, progression, promotions, pattern, velocity, experience_years
        )

        return {
            'progression': progression,
            'promotions': promotions,
            'velocity': velocity,
            'acceleration': acceleration,
            'pattern': pattern,
            'narrative': narrative,
            'current_level': progression[-1]['level'] if progression else 0,
            'levels_gained': progression[-1]['level'] - progression[0]['level'] if progression else 0
        }


def get_candidate_scores(candidate_name):
    """Calculate all scores for a candidate"""
    candidate = CANDIDATES[candidate_name]
    metrics = candidate['metrics']

    scorer = GrowthPotentialScorer()

    sub_scores = {
        'learning_agility': scorer.calculate_learning_agility(**metrics['learning_agility']),
        'skill_progression': scorer.calculate_skill_progression(**metrics['skill_progression']),
        'adaptability': scorer.calculate_adaptability(**metrics['adaptability']),
        'innovation_mindset': scorer.calculate_innovation_mindset(**metrics['innovation_mindset']),
        'feedback_integration': scorer.calculate_feedback_integration(**metrics['feedback_integration'])
    }

    overall_score = scorer.calculate_overall_score(sub_scores)
    explanation = scorer.get_score_explanation(sub_scores, overall_score)

    return sub_scores, overall_score, explanation


def get_all_candidates_summary():
    """Get summary scores for all candidates"""
    summary = []
    for name in CANDIDATES.keys():
        _, overall_score, _ = get_candidate_scores(name)
        summary.append({
            'name': name,
            'role': CANDIDATES[name]['role'],
            'score': overall_score,
            'photo': CANDIDATES[name]['photo']
        })
    return sorted(summary, key=lambda x: x['score'], reverse=True)
