#from django.contrib.auth.models import Group
from rest_framework import serializers
from rest.models import Student, Group

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('name', 'lastname', 'group')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('grade', 'semester', 'year', 'group')
