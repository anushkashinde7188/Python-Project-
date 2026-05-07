import tempfile
import unittest

from interview_evaluation import CandidateEvaluation, InterviewPerformanceEvaluationSystem


class InterviewEvaluationTests(unittest.TestCase):
    def test_overall_score_and_classification(self):
        scores = {
            "Technical Skills": 9.0,
            "Communication": 8.0,
            "Problem Solving": 9.0,
            "Confidence": 8.0,
            "Cultural Fit": 7.0,
        }
        overall = InterviewPerformanceEvaluationSystem.calculate_overall_score(scores)
        classification = InterviewPerformanceEvaluationSystem.classify_performance(overall)
        self.assertEqual(overall, 8.2)
        self.assertEqual(classification, "Good")

    def test_strength_and_improvement_identification(self):
        scores = {
            "Technical Skills": 9.0,
            "Communication": 5.0,
            "Problem Solving": 8.0,
            "Confidence": 4.0,
            "Cultural Fit": 7.0,
        }
        strengths, improvements = InterviewPerformanceEvaluationSystem.identify_strengths_and_improvements(scores)
        self.assertIn("Technical Skills", strengths)
        self.assertIn("Problem Solving", strengths)
        self.assertIn("Communication", improvements)
        self.assertIn("Confidence", improvements)

    def test_report_generation_and_persistence(self):
        with tempfile.NamedTemporaryFile(suffix=".db") as temp_db:
            system = InterviewPerformanceEvaluationSystem(db_path=temp_db.name)
            candidate = CandidateEvaluation(
                candidate_name="Alex Doe",
                candidate_email="alex@example.com",
                role_applied="Python Developer",
                interview_date="2026-05-07",
                scores={
                    "Technical Skills": 8.5,
                    "Communication": 8.0,
                    "Problem Solving": 9.0,
                },
            )

            report = system.evaluate(candidate)
            record_id = system.save_evaluation(report)
            summary = system.generate_summary_text(report)

            self.assertGreater(record_id, 0)
            self.assertIn("Interview Performance Summary", summary)
            self.assertIn("Alex Doe", summary)
            self.assertEqual(report["performance_classification"], "Excellent")


if __name__ == "__main__":
    unittest.main()
