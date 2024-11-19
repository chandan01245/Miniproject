from django.db import models

# Create your models here.

class register(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    mail = models.EmailField(max_length=30,blank=True)
    Date = models.DateField(max_length=8)
    Reason = models.TextField(max_length=80,default="Sick",blank=True)

    def __str__(self):
        return f'{self.name}, {self.Date}, {self.phone}'
    
class medicine(models.Model):
    email = models.EmailField(max_length=30)
    Medication = models.CharField(max_length=100)
    Dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=35)
    additional_notes = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.Medication

class appointment(models.Model):
    name= models.CharField(max_length=20)
    date = models.DateField(max_length=8)
    phone = models.CharField(max_length=10,default=0000000000)
    Reason = models.CharField(max_length=80,default="Sick")

    def __str__(self):
        return self.name