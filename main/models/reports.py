from django.db import models

class Reports(models.Model):
    id=models.AutoField(primary_key=True)
    email_id = models.OneToOneField('Emails', on_delete=models.CASCADE, to_field='id')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.confidence_score