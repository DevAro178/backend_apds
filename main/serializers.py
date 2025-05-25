from rest_framework import serializers
from .models import Attachments, Category, Emails, FAQs, Links, ReportAttributes, Reports, domain

# Attachments Serializer
class AttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachments
        fields = '__all__'


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Emails Serializer
class EmailsSerializer(serializers.ModelSerializer):
    attachments = AttachmentsSerializer(many=True, read_only=True, source='attachments_set')  # Related attachments
    links = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='links_set')  # Related links
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Emails
        fields = ['id', 'user_id', 'title', 'body', 'category_id', 'attachments', 'links','message_id','category_name','created_at']
    
    def get_category_name(self, obj):
        try:
            return obj.category_id.name  # Traverses: Report → Email → Category → name
        except AttributeError:
            return None


# FAQs Serializer
class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = '__all__'


# Links Serializer
class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = '__all__'


# ReportAttributes Serializer
class ReportAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportAttributes
        fields = '__all__'


# class ReportsSerializer(serializers.ModelSerializer):
#     email = EmailsSerializer(read_only=True, source='email_id')
#     attributes = ReportAttributesSerializer(many=True, read_only=True, source='reportattributes_set')
    
#     class Meta:
#         model = Reports
#         fields = ['id', 'email', 'confidence_score', 'attributes']

class ReportsSerializer(serializers.ModelSerializer):
    email_id = serializers.PrimaryKeyRelatedField(queryset=Emails.objects.all())
    email = EmailsSerializer(read_only=True, source='email_id')
    attributes = ReportAttributesSerializer(many=True, read_only=True, source='reportattributes_set')

    class Meta:
        model = Reports
        fields = ['id', 'email_id', 'email', 'confidence_score', 'attributes']


class DomainSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = domain
        fields = ['name', 'category']