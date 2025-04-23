from main.serializers import (ReportAttributesSerializer, ReportsSerializer)

def post(report_data):
    report_attributes_data = report_data.pop('attributes', [])

    report_serializer = ReportsSerializer(data=report_data)
    report_serializer.is_valid(raise_exception=True)
    report = report_serializer.save()

    # Handle reportAttributes
    for attribute in report_attributes_data:
        attribute['report_id'] = report.id
        attribute_serializer = ReportAttributesSerializer(data=attribute)
        attribute_serializer.is_valid(raise_exception=True)
        attribute_serializer.save()
        
    return report_serializer