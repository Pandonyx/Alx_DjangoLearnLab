from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        # Both ways included
        books_via_filter = Book.objects.filter(author=author)   # <- explicit filter
        books_via_related = author.books.all()                  # <- related_name
        return books_via_filter or books_via_related
    except Author.DoesNotExist:
        return []


# 2. List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        # Both ways included
        books_via_filter = Book.objects.filter(library=library)
        books_via_related = library.books.all()
        return books_via_filter or books_via_related
    except Library.DoesNotExist:
        return []


# 3. Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        # Both direct and explicit query work
        librarian_via_get = Librarian.objects.get(library=library)
        librarian_via_field = library.librarian
        return librarian_via_get or librarian_via_field
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None