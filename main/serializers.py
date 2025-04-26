from rest_framework import serializers
from .models import Attachments, Category, Emails, FAQs, Links, ReportAttributes, Reports

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

    class Meta:
        model = Emails
        fields = ['id', 'user_id', 'title', 'body', 'category_id', 'attachments', 'links']


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


class ReportsSerializer(serializers.ModelSerializer):
    attributes = ReportAttributesSerializer(many=True, read_only=True, source='reportattributes_set')
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Reports
        fields = ['id', 'email_id', 'confidence_score', 'attributes', 'category_name']

    def get_category_name(self, obj):
        try:
            return obj.email_id.category_id.name  # Traverses: Report → Email → Category → name
        except AttributeError:
            return None