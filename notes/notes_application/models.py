from django.db import models
from django.contrib.auth.models import User

class Notes (models.Model):
    title = models.CharField(max_length=1000)
    text = models.TextField()
    owner = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add = True)
    last_edit = models.DateTimeField(auto_now = True)
    shared_to = models.ManyToManyField(User, blank=True, null=True, related_name="shared")
    importance = models.TextField (choices = (
                    (u'Low', u'Low'),
                    (u'Normal', u'Normal'),
                    (u'High', u'High'),
                    (u'Very High', u'Very High'),
    ))

    def __unicode__(self):
        return '%s -- %s' % (self.owner, self.title)
