from main.serializers import (
    AttachmentsSerializer,EmailsSerializer
    ,LinksSerializer
)
import requests,base64,os,json
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model


def post(email_data,user_id):
    email_data['user_id'] = user_id
    attachments_data = email_data.pop('attachments', [])
    links_data = email_data.pop('links', [])
    email_serializer = EmailsSerializer(data=email_data)
    email_serializer.is_valid(raise_exception=True)

    User = get_user_model()
    user = User.objects.get(id=user_id)
    email = email_serializer.save(user_id=user)

    # Handle attachments
    for attachment in attachments_data:
        attachment['email_id'] = email.id
        attachment_serializer = AttachmentsSerializer(data=attachment)
        attachment_serializer.is_valid(raise_exception=True)
        attachment_serializer.save()

    # Handle links
    for link in links_data:
        link['email_id'] = email.id
        link_serializer = LinksSerializer(data=link)
        link_serializer.is_valid(raise_exception=True)
        link_serializer.save()

    return email_serializer



def getEmailBodyAgainstMessageID(messageID, access_token):
    
    def getEmailBodyFromResponse(data):
        """
        Extracts the email body (preferring text/html, fallback to text/plain)
        from Gmail API message response.
        """
        def decode_base64(data_str):
            try:
                return base64.urlsafe_b64decode(data_str).decode('utf-8')
            except Exception:
                return ''

        def text_from_html(html):
            soup = BeautifulSoup(html, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            lines = (line.strip() for line in soup.get_text().splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return '\n'.join(chunk for chunk in chunks if chunk)

        def extract_parts(payload):
            if 'parts' in payload:
                html_part = None
                plain_part = None
                for part in payload['parts']:
                    mime_type = part.get('mimeType', '')
                    if mime_type == 'text/html':
                        html_part = decode_base64(part['body'].get('data', ''))
                    elif mime_type == 'text/plain':
                        plain_part = decode_base64(part['body'].get('data', ''))
                    elif mime_type.startswith('multipart'):
                        nested = extract_parts(part)
                        if nested:
                            return nested  # Return nested html if found
                if html_part:
                    return html_part
                if plain_part:
                    return plain_part
            elif payload.get('body', {}).get('data'):
                return decode_base64(payload['body']['data'])
            return None
        try:
            body = extract_parts(data['payload'])            
            return body

        except Exception as e:
            print(f"Error while extracting email body: {str(e)}")
            return None


    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{messageID}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP error responses
        email_data = response.json()  # Parse the response JSON
        
        # Decode the Base64 URL-safe encoded data
        return getEmailBodyFromResponse(email_data)

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except KeyError:
        return {"error": "Invalid response format"}
