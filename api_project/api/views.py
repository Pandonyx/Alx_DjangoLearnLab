from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookList(generics.ListAPIView):
    """
    A read-only view that lists all books.
    Permissions are inherited from the project's default settings (IsAuthenticatedOrReadOnly).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for the Book model.

    Permissions are explicitly set to allow anyone to read (GET), but only
    authenticated users to write (POST, PUT, DELETE).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
