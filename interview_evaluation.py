import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Tuple


@dataclass
class CandidateEvaluation:
    candidate_name: str
    candidate_email: str
    role_applied: str
    interview_date: str
    scores: Dict[str, float]


class InterviewPerformanceEvaluationSystem:
    def __init__(self, db_path: str = "interview_evaluations.db") -> None:
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_name TEXT NOT NULL,
                    candidate_email TEXT NOT NULL,
                    role_applied TEXT NOT NULL,
                    interview_date TEXT NOT NULL,
                    scores_json TEXT NOT NULL,
                    overall_score REAL NOT NULL,
                    performance_classification TEXT NOT NULL,
                    strengths_json TEXT NOT NULL,
                    improvements_json TEXT NOT NULL,
                    generated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    @staticmethod
    def calculate_overall_score(scores: Dict[str, float]) -> float:
        if not scores:
            raise ValueError("At least one evaluation parameter score is required.")
        return round(sum(scores.values()) / len(scores), 2)

    @staticmethod
    def classify_performance(overall_score: float) -> str:
        if overall_score >= 8.5:
            return "Excellent"
        if overall_score >= 7.0:
            return "Good"
        if overall_score >= 5.0:
            return "Average"
        return "Needs Improvement"

    @staticmethod
    def identify_strengths_and_improvements(scores: Dict[str, float]) -> Tuple[List[str], List[str]]:
        strengths = [metric for metric, score in scores.items() if score >= 8.0]
        improvements = [metric for metric, score in scores.items() if score < 6.0]

        if not strengths:
            strengths = ["No major strengths identified yet"]
        if not improvements:
            improvements = ["No critical improvement areas identified"]

        return strengths, improvements

    def evaluate(self, candidate: CandidateEvaluation) -> Dict[str, object]:
        overall_score = self.calculate_overall_score(candidate.scores)
        classification = self.classify_performance(overall_score)
        strengths, improvements = self.identify_strengths_and_improvements(candidate.scores)

        return {
            "candidate_name": candidate.candidate_name,
            "candidate_email": candidate.candidate_email,
            "role_applied": candidate.role_applied,
            "interview_date": candidate.interview_date,
            "scores": candidate.scores,
            "overall_score": overall_score,
            "performance_classification": classification,
            "strengths": strengths,
            "improvement_areas": improvements,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def save_evaluation(self, evaluation_report: Dict[str, object]) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO evaluations (
                    candidate_name,
                    candidate_email,
                    role_applied,
                    interview_date,
                    scores_json,
                    overall_score,
                    performance_classification,
                    strengths_json,
                    improvements_json,
                    generated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    evaluation_report["candidate_name"],
                    evaluation_report["candidate_email"],
                    evaluation_report["role_applied"],
                    evaluation_report["interview_date"],
                    json.dumps(evaluation_report["scores"]),
                    evaluation_report["overall_score"],
                    evaluation_report["performance_classification"],
                    json.dumps(evaluation_report["strengths"]),
                    json.dumps(evaluation_report["improvement_areas"]),
                    evaluation_report["generated_at"],
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    @staticmethod
    def generate_summary_text(evaluation_report: Dict[str, object]) -> str:
        return (
            "\nInterview Performance Summary\n"
            "--------------------------------\n"
            f"Candidate: {evaluation_report['candidate_name']} ({evaluation_report['candidate_email']})\n"
            f"Role: {evaluation_report['role_applied']}\n"
            f"Interview Date: {evaluation_report['interview_date']}\n"
            f"Overall Score: {evaluation_report['overall_score']} / 10\n"
            f"Classification: {evaluation_report['performance_classification']}\n"
            f"Strengths: {', '.join(evaluation_report['strengths'])}\n"
            f"Improvement Areas: {', '.join(evaluation_report['improvement_areas'])}\n"
        )


def _collect_candidate_input() -> CandidateEvaluation:
    name = input("Candidate name: ").strip()
    email = input("Candidate email: ").strip()
    role = input("Role applied for: ").strip()
    interview_date = input("Interview date (YYYY-MM-DD): ").strip()

    metrics = [
        "Technical Skills",
        "Communication",
        "Problem Solving",
        "Confidence",
        "Cultural Fit",
    ]
    scores: Dict[str, float] = {}
    for metric in metrics:
        while True:
            try:
                value = float(input(f"{metric} score (0-10): ").strip())
                if 0 <= value <= 10:
                    scores[metric] = value
                    break
            except ValueError:
                pass
            print("Invalid score. Please enter a number between 0 and 10.")

    return CandidateEvaluation(
        candidate_name=name,
        candidate_email=email,
        role_applied=role,
        interview_date=interview_date,
        scores=scores,
    )


def main() -> None:
    system = InterviewPerformanceEvaluationSystem()
    candidate = _collect_candidate_input()
    report = system.evaluate(candidate)
    record_id = system.save_evaluation(report)
    print(system.generate_summary_text(report))
    print(f"Saved evaluation record ID: {record_id}")


if __name__ == "__main__":
    main()
