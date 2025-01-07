from django.db import models

class FAQs(models.Model):
    id=models.AutoField(primary_key=True)
    question=models.CharField(max_length=255)
    answer=models.TextField()
    
    def __str__(self):
        return self.question