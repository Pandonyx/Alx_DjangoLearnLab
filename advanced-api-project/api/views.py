from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .filters import BookFilter, AuthorFilter


class BookListView(generics.ListAPIView):
    """
    Enhanced ListView for retrieving all books with comprehensive filtering, searching, and ordering.
    
    Filtering Options:
    - Basic: ?author=1&publication_year=2020
    - Text search: ?title=harry&author_name=rowling
    - Date ranges: ?year_from=2000&year_to=2023
    - Recent books: ?recent_books=true
    
    Search Options:
    - Global search: ?search=Harry Potter
    - Searches across title and author name fields
    
    Ordering Options:
    - Single field: ?ordering=title or ?ordering=-publication_year
    - Multiple fields: ?ordering=author__name,publication_year
    - Available fields: title, publication_year, author__name, id
    
    Example Queries:
    - /api/books/?search=Harry&ordering=-publication_year
    - /api/books/?author_name=tolkien&year_from=1950&year_to=1970
    - /api/books/?recent_books=true&ordering=title
    """
    queryset = Book.objects.select_related('author')  # Optimize database queries
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configure filter backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Use custom FilterSet for advanced filtering
    filterset_class = BookFilter
    
    # Search functionality - searches across multiple fields
    search_fields = [
        'title',           # Search in book title
        'author__name',    # Search in author name
        '=title',          # Exact match for title (prefix with =)
        '@title',          # Full-text search for title (PostgreSQL only)
    ]
    
    # Ordering functionality
    ordering_fields = [
        'title',
        'publication_year', 
        'author__name',
        'id'
    ]
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """
        Optionally restricts the returned books to a given subset,
        by filtering against a query parameter in the URL.
        """
        queryset = super().get_queryset()
        
        # Additional custom filtering can be added here
        # For example, filtering by current user's preferences
        
        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single book by ID.
    
    Provides GET endpoint to retrieve a specific book by its primary key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Customized CreateView for adding a new book.
    
    Provides POST endpoint to create a new book instance with:
    - Authentication required
    - Custom validation handling
    - Custom response formatting
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom method to handle additional logic during book creation.
        This method is called after validation but before saving.
        """
        # You can add custom logic here, such as:
        # - Setting additional fields
        # - Logging the creation
        # - Sending notifications
        print(f"Creating new book: {serializer.validated_data['title']}")
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle form submission and provide custom responses.
        """
        serializer = self.get_serializer(data=request.data)
        
        # Perform validation
        if serializer.is_valid():
            # Custom validation passed
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            # Custom success response
            return Response({
                'message': 'Book created successfully',
                'book': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            # Validation failed - return custom error response
            return Response({
                'message': 'Failed to create book',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class BookUpdateView(generics.UpdateAPIView):
    """
    Customized UpdateView for modifying an existing book.
    
    Provides PUT and PATCH endpoints to update an existing book with:
    - Authentication required
    - Custom validation handling
    - Custom response formatting
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        """
        Custom method to handle additional logic during book update.
        This method is called after validation but before saving.
        """
        # You can add custom logic here, such as:
        # - Logging the update
        # - Checking permissions for specific fields
        # - Updating related models
        print(f"Updating book: {serializer.instance.title}")
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method to handle form submission and provide custom responses.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        # Perform validation
        if serializer.is_valid():
            # Custom validation passed
            self.perform_update(serializer)
            
            # Custom success response
            return Response({
                'message': 'Book updated successfully',
                'book': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            # Validation failed - return custom error response
            return Response({
                'message': 'Failed to update book',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        """
        Custom queryset method to add additional filtering.
        For example, users might only be able to update certain books.
        """
        queryset = Book.objects.all()
        
        # Example: Filter by publication year if provided in query params
        year = self.request.query_params.get('year')
        if year is not None:
            queryset = queryset.filter(publication_year=year)
        
        return queryset


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for removing a book with authentication required.
    
    Provides DELETE endpoint to remove a book from the database.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom delete method to provide custom response.
        """
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Book "{book_title}" deleted successfully'
        }, status=status.HTTP_200_OK)


# Author Views with filtering capabilities
class AuthorListView(generics.ListAPIView):
    """
    Enhanced ListView for retrieving all authors with filtering and searching.
    
    Filtering Options:
    - Filter by name: ?name=tolkien
    - Filter authors with books: ?has_books=true
    
    Search Options:
    - Search by name: ?search=rowling
    
    Ordering Options:
    - Order by name: ?ordering=name or ?ordering=-name
    
    Example Queries:
    - /api/authors/?search=tolkien&ordering=name
    - /api/authors/?has_books=true
    """
    queryset = Author.objects.prefetch_related('books')  # Optimize for nested books
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configure filter backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Use custom FilterSet
    filterset_class = AuthorFilter
    
    # Search functionality
    search_fields = ['name']
    
    # Ordering functionality
    ordering_fields = ['name', 'id']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single author by ID.
    
    Provides GET endpoint to retrieve a specific author with their books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]