from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Test route
@app.route('/ping')
def ping():
    return "OK"

# Analyze route
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['resume']

    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    except:
        return jsonify({"error": "Error reading PDF"})

    text = text.lower()

    skills_list = [
        "python", "java", "c", "c++", "html", "css",
        "javascript", "sql", "mongodb", "flask", "django"
    ]

    found_skills = [skill for skill in skills_list if skill in text]

    score = int((len(found_skills) / len(skills_list)) * 100)
    status = "Selected" if score >= 50 else "Rejected"

    return jsonify({
        "skills": found_skills,
        "score": score,
        "status": status
    })

if __name__ == '__main__':
    app.run(debug=True)
