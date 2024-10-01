from django.db import models

# Create your models here.

LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("c", "C"),
    ("cpp", "C++"),
    ("js", "Javascript")
]

class CodeSubmission(models.Model):
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, null=True, blank=True)
    code = models.TextField(null=True,blank=True)
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    error_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)