# Python-Project-

## Interview Performance Evaluation System

This repository contains a Python-based prototype that:

- Accepts candidate details and interview scores
- Stores evaluation parameters and ratings in SQLite
- Calculates overall performance score
- Classifies performance (`Excellent`, `Good`, `Average`, `Needs Improvement`)
- Identifies strengths and improvement areas
- Generates a structured performance summary report

## Run the application

```bash
python interview_evaluation.py
```

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
