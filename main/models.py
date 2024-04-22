from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BookFormat(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.description}"


class Type(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.description}"


class BookClub(models.Model):
    """
    Represents a book club entity.
    """
    club_name = models.CharField(max_length=64)
    date_created = models.DateField()
    club_description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2)
    types = models.ManyToManyField(Type)

    def __str__(self):
        return f"{self.id}: {self.club_name}"


class Reading(models.Model):
    """
    Represents a reading session within a book club.
    """
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    cover_edition_key = models.CharField(max_length=64)
    book_name = models.CharField(max_length=200)
    publish_year = models.IntegerField()
    author = models.CharField(max_length=100)
    status = models.CharField(max_length=2)
    date_finished = models.DateField(null=True)

    def __str__(self):
        return f"Book: {self.book_name}, Club ID: {self.club.id}, Status: {self.status}"


class Question(models.Model):
    """
    Represents a discussion question related to a book reading session.
    """
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE)
    date = models.DateField()


class Response(models.Model):
    """
    Represents a response to a discussion question.
    """
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateField()


class Shelf(models.Model):
    """
    Represents a book added to user's bookshelf.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_edition_key = models.CharField(max_length=64)
    book_name = models.CharField(max_length=200)
    publish_year = models.IntegerField()
    author = models.CharField(max_length=100)
    format = models.ForeignKey(BookFormat, on_delete=models.CASCADE)
    status = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.format.description}: {self.book_name}"


class JoinClub(models.Model):
    """
    Represents a user's membership status in a book club.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    status = models.CharField(max_length=2)
