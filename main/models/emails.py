from django.db import models

class Emails(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title