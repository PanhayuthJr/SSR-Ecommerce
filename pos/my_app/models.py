from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,null=False,blank=False,unique=True)

class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)

class Teacher(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    address = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    address = models.TextField()
class Product(models.Model):
    product_name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    bar_code = models.BigIntegerField(null=False, blank=False, unique=True)
    sell_price = models.FloatField(null=False, blank=False)
    unit_in_stock = models.IntegerField(null=False, blank=False)
    photo = models.ImageField(upload_to="media/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)