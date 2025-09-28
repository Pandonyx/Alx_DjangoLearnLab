from django.db import models


class Author(models.Model):
    """
    Model representing an author.
    
    This model stores basic information about authors and establishes
    the "one" side of a one-to-many relationship with books.
    """
    # Store the author's full name
    name = models.CharField(max_length=200)
    
    def __str__(self):
        """Return string representation of the author (their name)."""
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Model representing a book.
    
    This model stores book information and establishes the "many" side
    of a one-to-many relationship with authors (each book has one author,
    but an author can have multiple books).
    """
    # Store the book's title
    title = models.CharField(max_length=300)
    
    # Store the year the book was published
    publication_year = models.IntegerField()
    
    # Foreign key to Author model - establishes one-to-many relationship
    # CASCADE means if an author is deleted, all their books are deleted too
    # related_name='books' allows reverse lookup: author.books.all()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    
    def __str__(self):
        """Return string representation of the book (title and year)."""
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        ordering = ['title']