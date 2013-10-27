from django.db import models
# Create your models here.
class Group(models.Model):
        level = models.PositiveIntegerField()
        group = models.PositiveIntegerField()
        semester = models.PositiveIntegerField()
        year = models.PositiveIntegerField()
        def __unicode__(self):  # Python 3: def __str__(self):
                return self.group
        # def __str__(self):
        #     return "%s %r" % (self.level,self.group)

class Student(models.Model):
	name = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	group = models.PositiveIntegerField()
	level = models.PositiveIntegerField()
	

