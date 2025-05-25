from django.core.management.base import BaseCommand
from main.models import FAQs

class Command(BaseCommand):
    help = 'Seed FAQ data for phishing emails'

    def handle(self, *args, **options):
        faqs = [
            {
                "question": "What is a phishing email?",
                "answer": "A phishing email is a fraudulent message that appears to come from a legitimate source. It attempts to trick recipients into revealing sensitive information like passwords, credit card numbers, or installing malware."
            },
            {
                "question": "How can I identify a phishing email?",
                "answer": "Look for poor grammar, urgent language, suspicious links, unfamiliar senders, and requests for personal information. Always verify the sender’s email address and avoid clicking unknown links."
            },
            {
                "question": "What happens if I click a phishing link?",
                "answer": "Clicking a phishing link may lead you to a fake website that captures your information or may install malware on your device that can steal data or spy on your activity."
            },
            {
                "question": "How does your system detect phishing emails?",
                "answer": "Our system uses content analysis, domain reputation checks, link scanning, and machine learning to identify suspicious patterns associated with phishing attempts."
            },
            {
                "question": "Can phishing emails look exactly like real ones?",
                "answer": "Yes, some phishing emails are designed to perfectly mimic legitimate messages, including logos, names, and layout. Always verify URLs and sender details."
            },
            {
                "question": "What should I do if I suspect a phishing email?",
                "answer": "Do not click any links or download attachments. Report the email to your IT department or email provider and delete it immediately."
            },
            {
                "question": "Can your system block phishing emails before they reach my inbox?",
                "answer": "Yes, we aim to identify and filter phishing emails using real-time detection techniques before they reach the user’s inbox."
            },
            {
                "question": "What is domain reputation and how does it help?",
                "answer": "Domain reputation refers to the trustworthiness of a website. If a domain has been associated with malicious activity, our system flags it to help detect phishing."
            },
            {
                "question": "Are phishing emails always from strangers?",
                "answer": "Not necessarily. Attackers can spoof trusted contacts or companies. That’s why it's crucial to verify the authenticity of the message, even if it looks familiar."
            },
            {
                "question": "What data is typically targeted by phishing emails?",
                "answer": "Phishing emails often target login credentials, credit card numbers, personal identity details, and sometimes install malware for long-term exploitation."
            },
            {
                "question": "How often should I check my email for phishing signs?",
                "answer": "Always stay vigilant. Check each suspicious email carefully before taking any action, especially if it seems unexpected or asks for personal info."
            },
            {
                "question": "Does opening a phishing email compromise my system?",
                "answer": "Simply opening an email is usually not harmful, but clicking links or downloading attachments can expose you to risks."
            },
            {
                "question": "What should I do if I entered my credentials on a phishing site?",
                "answer": "Immediately change your password, enable two-factor authentication, and notify your security team or service provider."
            },
            {
                "question": "Can phishing emails be personalized?",
                "answer": "Yes, attackers often use personal information (from social media or data breaches) to craft more convincing and targeted messages."
            },
            {
                "question": "What role does machine learning play in detecting phishing?",
                "answer": "Machine learning helps identify patterns and anomalies in email structure, content, and links to detect phishing more effectively."
            },
            {
                "question": "Are all suspicious links phishing?",
                "answer": "Not necessarily, but it's better to err on the side of caution. Our system evaluates the destination, domain history, and behavior to decide."
            },
            {
                "question": "Can phishing affect my organization?",
                "answer": "Absolutely. A single compromised account can lead to data breaches, financial loss, and damage to reputation."
            },
            {
                "question": "How can I protect myself from phishing?",
                "answer": "Use strong, unique passwords, enable multi-factor authentication, and stay educated about phishing tactics."
            },
            {
                "question": "Is your detection system updated regularly?",
                "answer": "Yes, our system continuously evolves by learning from new threats, reports, and behavioral patterns across millions of emails."
            },
            {
                "question": "What should I do if I’m unsure whether an email is real?",
                "answer": "Verify by contacting the sender through official channels, and report the email to your security team or provider."
            },
        ]

        for faq in faqs:
            obj, created = FAQs.objects.get_or_create(
                question=faq["question"],
                defaults={"answer": faq["answer"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added FAQ: {faq['question']}"))
            else:
                self.stdout.write(f"Skipped existing FAQ: {faq['question']}")
