import csv
import json

csv_file = 'exam_questions.csv'
json_file = 'practice_exam_data.json'

questions = []

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        question_data = {
            "question": row['Question'],
            "choices": [row['OptionA'], row['OptionB'], row['OptionC'], row['OptionD']],
            "correct": {
                'A': row['OptionA'],
                'B': row['OptionB'],
                'C': row['OptionC'],
                'D': row['OptionD']
            }[row['CorrectAnswer'].strip().upper()],
            "explanation": row['Explanation']
        }
        questions.append(question_data)

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2)

print(f"✅ {len(questions)} questions converted to {json_file}!")
