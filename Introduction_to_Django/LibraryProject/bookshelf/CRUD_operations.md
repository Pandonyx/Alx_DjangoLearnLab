# Django Shell CRUD Example

This document demonstrates performing **CRUD (Create, Retrieve, Update, Delete)** operations on the `Book` model in **one continuous Django shell session**.

---

## Full CRUD Session

```python
>>> from bookshelf.models import Book

# Create a Book instance
>>> book = Book.objects.create(
...     title="1984",
...     author="George Orwell",
...     published_year=1949
... )
>>> print(book.id, book.title, book.author, book.published_year)
1 1984 George Orwell 1949

# Retrieve the created book
>>> book = Book.objects.get(id=1)
>>> print(book.id, book.title, book.author, book.published_year)
1 1984 George Orwell 1949

# Update the book's title
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> print(book.id, book.title, book.author, book.published_year)
1 Nineteen Eighty-Four George Orwell 1949

# Delete the book
>>> book.delete()
(1, {'bookshelf.Book': 1})

# Confirm deletion
>>> print(Book.objects.all())
<QuerySet []>
```
