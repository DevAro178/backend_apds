import requests

def generate(mail_content,classification):
    prompt_template = """
    You are an email spam classifier, you'll give a few reasoning points for why the email is classified as spam or legitimate. Keep the reasoning points minimal - and don't add any unnecessary details.
    Follow a JSON format for your response first key (classification) should state if email is classified as spam or legitimate, in second key (reasons) should an array of reasoning points and in third key (confidence_score) give a confidence score for the analysed email.
    
    Below is the email classified as {classified_as}:
    
    {email_content}
    """
    
    # """
    #     You are an email spam classifier, you'll classify emails based on their content and context either they are spam or legitimate. I also need you to give me a few reasoning points for why the email is classified as spam or legitimate. Keep the reasoning points minimal - and don't add any unnecessary details.
    #     Follow a JSON format for your response first key (classification) should state if email is classified as spam or legitimate, in second key (reasons) should an array of reasoning points and in third key (confidence_score) give a confidence score for the analysed email.

    #     Below is the email:
    #     {email_content}
    # """
    
    
    final_prompt = prompt_template.replace("{email_content}", mail_content).replace("{classified_as}", classification)

    try:
        response = requests.post("http://35.154.25.253:11434/api/generate", json={"model": "mistral","prompt": final_prompt,"stream":False})
        return response.json()  
    except Exception as e:
        return None
        