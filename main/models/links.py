from django.db import models

class Links(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email_id = models.ForeignKey('Emails', on_delete=models.CASCADE, to_field='id')
    
    def __str__(self):
        return self.name