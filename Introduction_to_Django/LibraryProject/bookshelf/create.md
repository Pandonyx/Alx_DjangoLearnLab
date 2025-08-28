> > > from bookshelf.models import Book
> > > from datetime import date
> > > book = Book.objects.create(title="1984", author="George Orwell", published_year="1949")
> > >
> > > print(book.id, book.title)
> > > 2 1984
