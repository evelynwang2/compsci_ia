from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    numAllowed = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name
    
class Race(models.Model):
    race = models.CharField(max_length=30)

    def __str__(self):
        return self.race
    
class State(models.Model):
    stateNameLong = models.CharField(max_length=20)
    stateNameShort = models.CharField(max_length=2)

    def __str__(self):
        return self.stateNameLong
    
class Delegate(models.Model):
    firstName = models.CharField(max_length=20, null=False, blank=False)
    lastName = models.CharField(max_length=20, null=False, blank=False)
    gender = models.CharField(max_length=1)
    streetAddr = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=20, null=False, blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    zip = models.IntegerField(null=False, blank=False)
    mobilePhone = models.CharField(max_length=15, null=False, blank=False)
    grade = models.SmallIntegerField(null=False, blank=False)
    parentName = models.CharField(max_length=50, null=False, blank=False)
    parentEmail = models.CharField(max_length=100, null=False, blank=False)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=False, blank=False)
    yearAtMun = models.SmallIntegerField(null=True)
    role=models.CharField(max_length=20, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now_add=True)
    parentPhone= models.CharField(max_length=15, null=False, blank=False)
    
class Team(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    delegate1 = models.ForeignKey(Delegate, related_name='delegate1', on_delete=models.CASCADE)
    delegate2 = models.ForeignKey(Delegate, related_name='delegate2', on_delete=models.CASCADE, null=True)
    delegate3 = models.ForeignKey(Delegate, related_name='delegate3', on_delete=models.CASCADE, null=True)
    delegate4 = models.ForeignKey(Delegate, related_name='delegate4', on_delete=models.CASCADE, null=True)

class Delegation(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, unique=True)
    assignedCountry = models.ForeignKey(Country, on_delete=models.CASCADE, default=None)
    
class Registry(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    choiceRank = models.SmallIntegerField(default=1)
    registryTime = models.DateTimeField(auto_now_add=True)

class Advisor(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    isActive = models.BooleanField(default=True)
