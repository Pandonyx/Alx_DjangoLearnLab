import django_filters
from django_filters import rest_framework as filters
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Custom FilterSet for Book model with advanced filtering options.
    
    Provides comprehensive filtering capabilities including:
    - Text searches with case-insensitive matching
    - Date range filtering for publication years
    - Author-based filtering with multiple options
    - Combined filters for complex queries
    """
    
    # Title filtering with case-insensitive contains
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text='Filter by title (case-insensitive, partial matches allowed)'
    )
    
    # Author filtering by ID
    author = django_filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        help_text='Filter by specific author ID'
    )
    
    # Author name filtering with case-insensitive contains
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text='Filter by author name (case-insensitive, partial matches allowed)'
    )
    
    # Publication year exact match
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        help_text='Filter by exact publication year'
    )
    
    # Publication year range filtering
    year_from = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text='Filter books published from this year onwards'
    )
    
    year_to = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text='Filter books published up to this year'
    )
    
    # Recent books filter (published in last 10 years)
    recent_books = django_filters.BooleanFilter(
        method='filter_recent_books',
        help_text='Filter recent books (published in last 10 years)'
    )
    
    def filter_recent_books(self, queryset, name, value):
        """
        Custom filter method to get books published in the last 10 years.
        """
        if value:
            from datetime import datetime
            current_year = datetime.now().year
            return queryset.filter(publication_year__gte=current_year - 10)
        return queryset
    
    class Meta:
        model = Book
        fields = {
            'title': ['icontains', 'exact'],
            'publication_year': ['exact', 'gte', 'lte', 'gt', 'lt'],
            'author': ['exact'],
            'author__name': ['icontains', 'exact'],
        }


class AuthorFilter(django_filters.FilterSet):
    """
    Custom FilterSet for Author model.
    
    Provides filtering capabilities for authors including:
    - Name-based searching
    - Filtering by number of books authored
    """
    
    # Author name filtering
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text='Filter by author name (case-insensitive, partial matches allowed)'
    )
    
    # Filter authors who have books
    has_books = django_filters.BooleanFilter(
        method='filter_has_books',
        help_text='Filter authors who have published books'
    )
    
    def filter_has_books(self, queryset, name, value):
        """
        Custom filter method to get authors who have published books.
        """
        if value:
            return queryset.filter(books__isnull=False).distinct()
        elif value is False:
            return queryset.filter(books__isnull=True)
        return queryset
    
    class Meta:
        model = Author
        fields = {
            'name': ['icontains', 'exact'],
        }