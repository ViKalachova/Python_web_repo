from django.db import models

# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=150, null=False, unique=True)
    born_date = models.DateField(null=True)
    born_location = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return f"{self.fullname}"

class Tag(models.Model):
    tag_name = models.CharField(max_length=150, null=False, unique=True)

    def __str__(self):
        return f"{self.tag_name}"

class Quote(models.Model):
    artist = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote}"