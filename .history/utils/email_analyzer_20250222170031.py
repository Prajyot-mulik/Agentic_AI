import ollama

class EmailAnalyzer:
    def __init__(self):
        self.model = "deepseek-r1:7b"

    def analyze_email(self, email):
        prompt = f"Analyze this email and summarize its intent:\n\nSubject: {email['subject']}\nBody: {email['body']}"
        response = ollama.generate(model=self.model, prompt=prompt)
        return response['response']