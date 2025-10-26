from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="books")
    authors = models.ManyToManyField(Author, related_name="books")
    publish_date = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.title