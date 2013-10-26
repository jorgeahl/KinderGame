from django.db import models
# Create your models here.
class Group(models.Model):
        level = models.CharField(max_length=100)
        group = models.CharField(max_length=100)
        semester = models.CharField(max_length=100)
        year = models.CharField(max_length=100)
        #def __unicode__(self):
         #       return self.group

class Student(models.Model):
	name = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	#group = models.ForeignKey(Group)
	level = models.CharField(max_length=100)
	

