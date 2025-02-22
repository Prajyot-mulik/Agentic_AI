import time
from utils.gmail_client import GmailClient
from utils.email_analyzer import EmailAnalyzer
from utils.email_responder import EmailResponder

def main():
    # Initialize Gmail client
    gmail_client = GmailClient()

    # Initialize AI tools
    analyzer = EmailAnalyzer()
    responder = EmailResponder()

    # Main loop to check for new emails
    while True:
        print("Checking for new emails...")
        emails = gmail_client.fetch_unread_emails()

        for email in emails:
            print(f"Analyzing email: {email['subject']}")
            analysis = analyzer.analyze_email(email)
            print(f"Analysis: {analysis}")

            print("Generating response...")
            response = responder.generate_response(email, analysis)
            print(f"Generated response: {response}")

            print("Sending reply...")
            gmail_client.send_reply(email, response)
            print("Reply sent!")

        # Wait before checking again
        time.sleep(60)

if __name__ == "__main__":
    main()