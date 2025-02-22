import ollama

class EmailResponder:
    def __init__(self):
        self.model = "deepseek-r1:7b"

    def generate_response(self, email, analysis):
        prompt = f"""
        You are an AI email assistant. Your task is to respond to emails in a professional, friendly, and polished tone. 
        Correct any typos or grammatical errors in the original email, and ensure your response is concise, warm, and appropriate.

        Original Email:
        Subject: {email['subject']}
        Body: {email['body']}

        Analysis:
        {analysis}

        Instructions for your response:
        1. Start with a polite greeting.
        2. Acknowledge the sender's message and express gratitude or appreciation.
        3. Correct any typos or errors in the original email.
        4. Keep the tone professional yet friendly.
        5. End with a warm sign-off.

        Write the response:
        """
        response = ollama.generate(model=self.model, prompt=prompt)
        return response['response']