from django.db import models
from django.contrib.auth.models import User
from utils import TimeStampedModel

class Checklist(TimeStampedModel):
    name = models.CharField(max_length=256, null=False)
    description = models.TextField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shared = models.ManyToManyField(User, related_name='shared')

    def __unicode__(self):
        return unicode(self.name)

    def has_perm(self, user):
        return (self.owner == user or obj.shared.filter(shared=user))


class Task(TimeStampedModel):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return unicode(self.description)

    def has_perm(self, user):
        return (self.owner == user or self.checklist.has_perm(user))
