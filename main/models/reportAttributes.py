from django.db import models

class ReportAttributes(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    report_id = models.ForeignKey('Reports', on_delete=models.CASCADE, to_field='id')
    
    def __str__(self):
        return self.name