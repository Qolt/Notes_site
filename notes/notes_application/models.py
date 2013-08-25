from django.db import models
from django.contrib.auth.models import User

class Notes (models.Model):
    title = models.CharField(max_length=1000)
    text = models.TextField()
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return '%s -- %s' % (self.owner, self.title)
