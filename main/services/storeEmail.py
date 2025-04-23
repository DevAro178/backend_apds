from main.serializers import (
    AttachmentsSerializer,EmailsSerializer
    ,LinksSerializer
)
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