from django.db import models
from django.urls import reverse
# Create your models here.

class EntryPage(models.Model):
    title = models.CharField(max_length=100)
    entry_text = models.TextField
    def get_absolute_url(self): 
        return reverse('encyclopedia:entry', kwargs={'title':self.title})