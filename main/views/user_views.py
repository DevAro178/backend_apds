import requests,base64,os,json
from bs4 import BeautifulSoup
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from main.models import Attachments, Category, Emails, FAQs, Links, ReportAttributes, Reports
from main.serializers import (
    AttachmentsSerializer, CategorySerializer, EmailsSerializer, FAQsSerializer,
    LinksSerializer, ReportAttributesSerializer, ReportsSerializer
)
from rest_framework.decorators import action, permission_classes
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Ensure the user is authenticated
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist


        
        
# **Emails ViewSet** - Handles CRUD operations for Emails
class EmailsViewSet(viewsets.ModelViewSet):
    serializer_class = EmailsSerializer
    permission_classes = [IsAuthenticated]

    # Get all emails for the logged-in user
    def get_queryset(self):
        return Emails.objects.filter(user_id=self.request.user)

    # Create a new email with attachments and links
    def create(self, request, *args, **kwargs):
        
        email_data = request.data
        attachments_data = email_data.pop('attachments', [])
        links_data = email_data.pop('links', [])
        
        # Set the user_id field to the authenticated user
        email_data['user_id'] = request.user.id

        email_serializer = self.get_serializer(data=email_data)
        email_serializer.is_valid(raise_exception=True)
        email = email_serializer.save(user_id=request.user)

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

        return Response(email_serializer.data, status=status.HTTP_201_CREATED)

    # Update email with attachments and links
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        email_data = request.data
        attachments_data = email_data.pop('attachments', [])
        links_data = email_data.pop('links', [])

        email_serializer = self.get_serializer(instance, data=email_data, partial=True)
        email_serializer.is_valid(raise_exception=True)
        email_serializer.save()

        # Handle attachments
        for attachment in attachments_data:
            attachment['email_id'] = instance.id
            attachment_serializer = AttachmentsSerializer(data=attachment)
            attachment_serializer.is_valid(raise_exception=True)
            attachment_serializer.save()

        # Handle links
        for link in links_data:
            link['email_id'] = instance.id
            link_serializer = LinksSerializer(data=link)
            link_serializer.is_valid(raise_exception=True)
            link_serializer.save()

        return Response(email_serializer.data)

    # Delete email and related attachments and links
    def destroy(self, request, *args, **kwargs):
        email = self.get_object()
        email_id = email.id

        # Delete related attachments and links
        Attachments.objects.filter(email_id=email_id).delete()
        Links.objects.filter(email_id=email_id).delete()

        return super().destroy(request, *args, **kwargs)


# **Reports ViewSet** - Handles CRUD operations for Reports
class ReportsViewSet(viewsets.ModelViewSet):
    serializer_class = ReportsSerializer
    permission_classes = [IsAuthenticated]

    # Get reports filtered by email_id (requesting user's reports)
    def get_queryset(self):
        email_id = self.request.query_params.get('email_id')
        if email_id:
            return Reports.objects.filter(email_id=email_id)
        return Reports.objects.none()

    # Create a new report with associated reportAttributes
    def create(self, request, *args, **kwargs):
        report_data = request.data
        report_attributes_data = report_data.pop('attributes', [])

        report_serializer = self.get_serializer(data=report_data)
        report_serializer.is_valid(raise_exception=True)
        report = report_serializer.save()

        # Handle reportAttributes
        for attribute in report_attributes_data:
            attribute['report_id'] = report.id
            attribute_serializer = ReportAttributesSerializer(data=attribute)
            attribute_serializer.is_valid(raise_exception=True)
            attribute_serializer.save()

        return Response(report_serializer.data, status=status.HTTP_201_CREATED)

    # Update report with reportAttributes
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        report_data = request.data
        report_attributes_data = report_data.pop('attributes', [])

        report_serializer = self.get_serializer(instance, data=report_data, partial=True)
        report_serializer.is_valid(raise_exception=True)
        report_serializer.save()

        # Handle reportAttributes
        for attribute in report_attributes_data:
            attribute['report_id'] = instance.id
            attribute_serializer = ReportAttributesSerializer(data=attribute)
            attribute_serializer.is_valid(raise_exception=True)
            attribute_serializer.save()

        return Response(report_serializer.data)

    # Delete report and related reportAttributes
    def destroy(self, request, *args, **kwargs):
        report = self.get_object()
        report_id = report.id

        # Delete related reportAttributes
        ReportAttributes.objects.filter(report_id=report_id).delete()

        return super().destroy(request, *args, **kwargs)


# **FAQs ViewSet** - Handles CRUD operations for FAQs (accessible by anyone)
class FAQsViewSet(viewsets.ModelViewSet):
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    permission_classes = [AllowAny]  # Open access to FAQs
    
    # Permission control based on HTTP method
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            # Public access for GET (list and retrieve) actions
            return [AllowAny()]
        return [IsAuthenticated()]  # Authenticated access for POST, PUT, DELETE


# **Attachments ViewSet** - Handles CRUD operations for Attachments
class AttachmentsViewSet(viewsets.ModelViewSet):
    queryset = Attachments.objects.all()
    serializer_class = AttachmentsSerializer
    permission_classes = [IsAuthenticated]


# **Category ViewSet** - Handles CRUD operations for Categories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# **Links ViewSet** - Handles CRUD operations for Links
class LinksViewSet(viewsets.ModelViewSet):
    queryset = Links.objects.all()
    serializer_class = LinksSerializer
    permission_classes = [IsAuthenticated]


# **ReportAttributes ViewSet** - Handles CRUD operations for ReportAttributes
class ReportAttributesViewSet(viewsets.ModelViewSet):
    queryset = ReportAttributes.objects.all()
    serializer_class = ReportAttributesSerializer
    permission_classes = [IsAuthenticated]



class SpamClassifierView(APIView):
    model = None
    tokenizer = None
    model_path = None
    tokenizer_path = None

    permission_classes = [IsAuthenticated]  # Add this to require authentication
    # permission_classes = [AllowAny]  # Add this to require authentication

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define paths for model and tokenizer
        self.model_path = os.path.join(settings.BASE_DIR, 'main\\trainedModelFiles\\lstm_model.h5')
        self.tokenizer_path = os.path.join(settings.BASE_DIR, 'main\\trainedModelFiles\\tokenizer.json')
        
        # Load model and tokenizer once during initialization
        self.load_model_and_tokenizer()

    def load_model_and_tokenizer(self):
        try:
            # Load the trained LSTM model
            self.model = load_model(self.model_path)
            print(f"Model loaded from {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")

        try:
            # Load the tokenizer from the JSON file
            with open(self.tokenizer_path, 'r') as json_file:
                tokenizer_json = json.load(json_file)
            self.tokenizer = tokenizer_from_json(tokenizer_json)
            print(f"Tokenizer loaded from {self.tokenizer_path}")
        except Exception as e:
            print(f"Error loading tokenizer: {e}")

    def preprocessing(self, email_content):
        """Preprocess email content for prediction."""
        test_sequences = self.tokenizer.texts_to_sequences([email_content])
        return pad_sequences(test_sequences, padding='post', maxlen=100)
    
    # def get(self, request, *args, **kwargs):
    #     """Handle the GET request and return a sample string."""
    #     # sample_string = "Congratulations! You WON the Lottery!!!."
    #     sample_string = "How are you doing today? are you available for a call today?."
    #     processed_content = self.preprocessing(sample_string)
    #     # Predict with the model
    #     prediction_result = self.model.predict(processed_content)
    #     # Determine if the email is spam or legitimate
    #     result = "Spam Email" if prediction_result[0] > 0.5 else "Legitimate Email"
    #     return Response({'Result':result}, status=status.HTTP_200_OK)
      
    def getEmailBodyFromResponse(self, data):
        """
        Extracts the email body from the Gmail API response.
        If 'parts' is present, it selects the first part with mimeType 'text/plain'.
        If 'parts' is not present, it retrieves the body directly from 'payload.body.data'.
        """
        
        def textFromHtml(html):
            # Parse the decoded HTML content
            soup = BeautifulSoup(base64.urlsafe_b64decode(html).decode('utf-8'), 'html.parser')
            
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
        try:
            if 'parts' in data['payload']:
                print("@@@@@@@@@@@@@")
                for part in data['payload']['parts']:
                    if part['mimeType'] == 'text/html':
                        return textFromHtml(part['body']['data'])
            else:
                print("%%%%%%%%%%%%%%%%%%%")
                return textFromHtml(data['payload']['body']['data'])
        except KeyError:
            return None
        
    
    def getEmailBody(self, messageID, access_token):
        url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{messageID}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP error responses
            email_data = response.json()  # Parse the response JSON
            
            # Decode the Base64 URL-safe encoded data
            return self.getEmailBodyFromResponse(email_data)

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except KeyError:
            return {"error": "Invalid response format"}
    

    def post(self, request, *args, **kwargs):
        """Handle the POST request for spam classification."""
        result = None
        if request.method == "POST":
            # Get email content from the request body
            message_id = request.data.get('message_id')
            mail_content=self.getEmailBody(messageID=message_id,access_token=request.user.access_token)
            
            if mail_content:
                # Preprocess the email content
                processed_content = self.preprocessing(mail_content)
                
                # Predict with the model
                prediction_result = self.model.predict(processed_content)
                
                # Determine if the email is spam or legitimate
                result = "Spam Email" if prediction_result[0] > 0.5 else "Legitimate Email"
        
        return Response({"result": result})