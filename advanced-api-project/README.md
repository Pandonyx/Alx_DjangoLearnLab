# Advanced API Project Documentation

## Overview

This Django REST Framework API provides comprehensive CRUD operations for managing books and authors with advanced filtering, searching, ordering capabilities, custom permissions, and validation.

## Filtering, Searching, and Ordering Implementation

### 1. Filtering Capabilities

#### Basic Filtering

The API supports filtering through URL query parameters using Django Filter Backend:

```python
# In BookListView
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_class = BookFilter  # Custom FilterSet for advanced options
```

#### Available Filters

**Book Filters:**

- `author` - Filter by author ID: `/api/books/?author=1`
- `publication_year` - Exact year: `/api/books/?publication_year=2020`
- `year_from` - Books from year onwards: `/api/books/?year_from=2000`
- `year_to` - Books up to year: `/api/books/?year_to=2023`
- `title` - Case-insensitive title search: `/api/books/?title=harry`
- `author_name` - Case-insensitive author name: `/api/books/?author_name=rowling`
- `recent_books` - Books from last 10 years: `/api/books/?recent_books=true`

**Advanced Filtering Examples:**

```bash
# Combination filters
/api/books/?author_name=tolkien&year_from=1950&year_to=1970

# Range filtering
/api/books/?publication_year__gte=2000&publication_year__lte=2023

# Case-insensitive text filtering
/api/books/?title__icontains=lord&author__name__icontains=tolkien
```

#### Custom FilterSet Implementation

```python
class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    year_from = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    year_to = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    recent_books = django_filters.BooleanFilter(method='filter_recent_books')

    def filter_recent_books(self, queryset, name, value):
        if value:
            current_year = datetime.now().year
            return queryset.filter(publication_year__gte=current_year - 10)
        return queryset
```

### 2. Search Functionality

#### Global Search Configuration

```python
search_fields = [
    'title',           # Search in book title
    'author__name',    # Search in author name
    '=title',          # Exact match for title
    '@title',          # Full-text search (PostgreSQL only)
]
```

#### Search Usage Examples

```bash
# Global search across title and author
/api/books/?search=Harry Potter

# Partial matching (case-insensitive)
/api/books/?search=fantasy

# Exact search (using = prefix)
/api/books/?search==Harry Potter and the Philosopher's Stone
```

#### Search Features

- **Case-insensitive**: Searches ignore case differences
- **Partial matching**: Finds books with partial title/author matches
- **Cross-field search**: Single search term looks across multiple fields
- **Exact matching**: Use `=` prefix for exact matches

### 3. Ordering Configuration

#### Available Ordering Fields

```python
ordering_fields = [
    'title',
    'publication_year',
    'author__name',
    'id'
]
ordering = ['title']  # Default ordering
```

#### Ordering Usage Examples

```bash
# Single field ordering
/api/books/?ordering=title              # Ascending
/api/books/?ordering=-publication_year  # Descending

# Multiple field ordering
/api/books/?ordering=author__name,publication_year
/api/books/?ordering=-author__name,title

# Related field ordering
/api/books/?ordering=author__name
```

#### Ordering Features

- **Ascending/Descending**: Use `-` prefix for descending order
- **Multiple fields**: Comma-separated field names
- **Related fields**: Order by related model fields (author\_\_name)
- **Default ordering**: Falls back to title if no ordering specified

### 4. Combined Query Examples

#### Complex Filtering + Search + Ordering

```bash
# Search for fantasy books by Tolkien, published 1950-1970, ordered by year
/api/books/?search=fantasy&author_name=tolkien&year_from=1950&year_to=1970&ordering=publication_year

# Recent books with "magic" in title, ordered by author then title
/api/books/?recent_books=true&search=magic&ordering=author__name,title

# Books by specific author, ordered by publication year descending
/api/books/?author=1&ordering=-publication_year
```

## Performance Optimizations

### Database Query Optimization

```python
# In BookListView
queryset = Book.objects.select_related('author')  # Reduces database queries

# In AuthorListView
queryset = Author.objects.prefetch_related('books')  # Optimizes nested data
```

### Optimization Features

- **select_related**: Reduces queries for foreign key relationships
- **prefetch_related**: Optimizes reverse foreign key and many-to-many relationships
- **Efficient filtering**: Database-level filtering reduces data transfer
- **Indexed fields**: Ensure database indexes on commonly filtered fields

## API Response Format

### Successful Response with Pagination

```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/books/?page=2&search=harry",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Harry Potter and the Philosopher's Stone",
      "publication_year": 1997,
      "author": 1
    }
  ]
}
```

### Filter/Search with No Results

```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

## Error Handling

### Invalid Filter Values

- Invalid year formats are ignored or return validation errors
- Invalid author IDs return empty results
- Malformed query parameters are handled gracefully

### Invalid Ordering

- Invalid ordering fields are ignored
- API continues to function with default ordering
- No error responses for invalid ordering parameters

## View Configurations

### BookListView

**Endpoint**: `GET /api/books/`
**Features**: Comprehensive filtering, searching, and ordering

#### Configuration:

```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', '=title']
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['title']
```

### AuthorListView

**Endpoint**: `GET /api/authors/`
**Features**: Author filtering, searching, and ordering

#### Configuration:

```python
class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['name']
```

## Dependencies and Settings

### Required Packages

```bash
pip install djangorestframework django-filter
```

### Settings Configuration

```python
INSTALLED_APPS = [
    'rest_framework',
    'django_filters',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

## Best Practices Implemented

1. **Performance Optimization**

   - Use `select_related()` for foreign key relationships
   - Use `prefetch_related()` for reverse foreign keys
   - Implement database-level filtering to reduce data transfer
   - Add proper database indexes on filtered fields

2. **User Experience**

   - Case-insensitive search and filtering
   - Partial matching for text searches
   - Intuitive query parameter names
   - Consistent API response format

3. **Flexibility**

   - Multiple filter options per field (exact, contains, range)
   - Combinable filters for complex queries
   - Multiple ordering options
   - Both global search and specific field filtering

4. **Security**

   - Input validation through FilterSet
   - Safe handling of invalid parameters
   - No exposure of sensitive database structure

5. **Documentation**
   - Clear docstrings with examples
   - Comprehensive help text for filters
   - Example queries in comments

## Advanced Features

### Custom Filter Methods

```python
def filter_recent_books(self, queryset, name, value):
    """Custom method to filter books from last 10 years"""
    if value:
        current_year = datetime.now().year
        return queryset.filter(publication_year__gte=current_year - 10)
    return queryset
```

### Search Field Prefixes

- **No prefix**: Standard search (icontains)
- **=**: Exact match
- **@**: Full-text search (PostgreSQL)
- **^**: Starts with
- **$**: Regex search

### Filter Field Lookups

- **exact**: Exact match
- **icontains**: Case-insensitive contains
- **gte/lte**: Greater/less than or equal
- **gt/lt**: Greater/less than
- **in**: Value in list
- **range**: Value in range

## Testing Results

### Filter Testing

- ✅ Basic field filtering
- ✅ Range filtering (year_from, year_to)
- ✅ Custom boolean filters (recent_books)
- ✅ Related field filtering (author\_\_name)
- ✅ Multiple filter combinations

### Search Testing

- ✅ Global search across multiple fields
- ✅ Case-insensitive partial matching
- ✅ Exact search with = prefix
- ✅ Search combined with filters

### Ordering Testing

- ✅ Single field ordering (ascending/descending)
- ✅ Multiple field ordering
- ✅ Related field ordering
- ✅ Default ordering fallback

## Common Usage Patterns

### 1. Browse Books by Genre/Topic

```bash
# Search for fantasy books, ordered by publication year
/api/books/?search=fantasy&ordering=-publication_year
```

### 2. Find Books by Specific Author

```bash
# All books by Tolkien, ordered by title
/api/books/?author_name=tolkien&ordering=title
```

### 3. Discover Recent Publications

```bash
# Recent books with search term, ordered by newest first
/api/books/?recent_books=true&search=mystery&ordering=-publication_year
```

### 4. Academic Research

```bash
# Books in specific time period by publication year
/api/books/?year_from=1950&year_to=1970&ordering=publication_year
```

### 5. Library Management

```bash
# All books by specific author ID with exact year
/api/books/?author=1&publication_year=1997
```

## Frontend Integration Examples

### JavaScript/React Example

```javascript
// Build dynamic API URLs
const buildApiUrl = (baseUrl, filters = {}) => {
  const params = new URLSearchParams();

  Object.entries(filters).forEach(([key, value]) => {
    if (value !== null && value !== "") {
      params.append(key, value);
    }
  });

  return `${baseUrl}?${params.toString()}`;
};

// Usage
const apiUrl = buildApiUrl("/api/books/", {
  search: "harry potter",
  author_name: "rowling",
  ordering: "-publication_year",
});
// Result: /api/books/?search=harry+potter&author_name=rowling&ordering=-publication_year
```

### URL Builder for Complex Queries

```javascript
class BookApiClient {
  constructor(baseUrl = "/api/books/") {
    this.baseUrl = baseUrl;
    this.filters = {};
  }

  search(term) {
    this.filters.search = term;
    return this;
  }

  byAuthor(authorName) {
    this.filters.author_name = authorName;
    return this;
  }

  publishedBetween(yearFrom, yearTo) {
    this.filters.year_from = yearFrom;
    this.filters.year_to = yearTo;
    return this;
  }

  orderBy(field, descending = false) {
    this.filters.ordering = descending ? `-${field}` : field;
    return this;
  }

  recentOnly() {
    this.filters.recent_books = true;
    return this;
  }

  build() {
    const params = new URLSearchParams(this.filters);
    return `${this.baseUrl}?${params.toString()}`;
  }
}

// Usage
const url = new BookApiClient()
  .search("fantasy")
  .byAuthor("tolkien")
  .publishedBetween(1950, 1970)
  .orderBy("publication_year", true)
  .build();
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. No Results Returned

- Check filter values for typos
- Verify case sensitivity (use icontains filters)
- Test individual filters separately
- Check if data exists in database

#### 2. Slow Performance

- Add database indexes on filtered fields
- Use select_related/prefetch_related appropriately
- Consider pagination for large datasets
- Monitor database query count

#### 3. Unexpected Results

- Check filter logic (AND vs OR behavior)
- Verify related field paths (author\_\_name)
- Test with simplified queries first
- Check for data type mismatches

#### 4. Ordering Not Working

- Verify field names in ordering_fields
- Check for typos in ordering parameter
- Ensure related fields use double underscores
- Test with simple single-field ordering

## Future Enhancements

### Possible Improvements

1. **Full-text search** with PostgreSQL search features
2. **Faceted search** with result counts per filter
3. **Saved searches** for user preferences
4. **Advanced date filtering** with relative dates
5. **Geospatial filtering** if location data added
6. **Elasticsearch integration** for complex search
7. **Query result caching** for performance
8. **API versioning** for backward compatibility

### Additional Filter Ideas

- Genre/category filtering
- Language filtering
- Availability status
- Rating/review-based filtering
- Price range filtering (if applicable)
- Publisher filtering

This implementation provides a robust, flexible, and performant API with comprehensive filtering, searching, and ordering capabilities that can be easily extended as requirements grow.# Advanced API Project Documentation

## Overview

This Django REST Framework API provides CRUD operations for managing books and authors with custom permissions, filtering, and validation.

## View Configurations

### 1. BookListView

**Endpoint**: `GET /api/books/`
**Purpose**: Retrieve all books with advanced filtering capabilities

#### Configuration:

- **Base Class**: `generics.ListAPIView`
- **Permissions**: `IsAuthenticatedOrReadOnly` - Open read access
- **Serializer**: `BookSerializer`

#### Features:

- **Filtering**: Filter by `author` and `publication_year`
  - Example: `/api/books/?author=1&publication_year=2020`
- **Search**: Search in `title` and `author__name` fields
  - Example: `/api/books/?search=Harry`
- **Ordering**: Sort by `title` or `publication_year`
  - Example: `/api/books/?ordering=-publication_year`

#### Custom Settings:

```python
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_fields = ['author', 'publication_year']
search_fields = ['title', 'author__name']
ordering_fields = ['title', 'publication_year']
ordering = ['title']  # Default ordering
```

### 2. BookDetailView

**Endpoint**: `GET /api/books/<int:pk>/`
**Purpose**: Retrieve a specific book by ID

#### Configuration:

- **Base Class**: `generics.RetrieveAPIView`
- **Permissions**: `IsAuthenticatedOrReadOnly` - Open read access
- **Serializer**: `BookSerializer`

### 3. BookCreateView

**Endpoint**: `POST /api/books/create/`
**Purpose**: Create a new book with custom validation and response handling

#### Configuration:

- **Base Class**: `generics.CreateAPIView`
- **Permissions**: `IsAuthenticated` - Authentication required
- **Serializer**: `BookSerializer`

#### Custom Hooks:

1. **`perform_create(serializer)`**:
   - Called after validation but before saving
   - Used for logging and additional business logic
2. **`create(request, \*args, **kwargs)`\*\*:
   - Overridden for custom response formatting
   - Returns structured JSON with success/error messages

#### Custom Response Format:

```json
// Success
{
    "message": "Book created successfully",
    "book": { /* book data */ }
}

// Error
{
    "message": "Failed to create book",
    "errors": { /* validation errors */ }
}
```

### 4. BookUpdateView

**Endpoint**: `PUT/PATCH /api/books/<int:pk>/update/`
**Purpose**: Update existing books with custom validation and filtering

#### Configuration:

- **Base Class**: `generics.UpdateAPIView`
- **Permissions**: `IsAuthenticated` - Authentication required
- **Serializer**: `BookSerializer`

#### Custom Hooks:

1. **`perform_update(serializer)`**:

   - Called after validation but before saving
   - Used for logging and additional business logic

2. **`update(request, \*args, **kwargs)`\*\*:

   - Overridden for custom response formatting
   - Handles both PUT (full update) and PATCH (partial update)

3. **`get_queryset()`**:
   - Custom queryset filtering
   - Supports optional year filtering via query parameters
   - Example: `/api/books/1/update/?year=2020`

#### Custom Response Format:

```json
// Success
{
    "message": "Book updated successfully",
    "book": { /* updated book data */ }
}

// Error
{
    "message": "Failed to update book",
    "errors": { /* validation errors */ }
}
```

### 5. BookDeleteView

**Endpoint**: `DELETE /api/books/<int:pk>/delete/`
**Purpose**: Delete books with custom response

#### Configuration:

- **Base Class**: `generics.DestroyAPIView`
- **Permissions**: `IsAuthenticated` - Authentication required
- **Serializer**: `BookSerializer`

#### Custom Hooks:

1. **`destroy(request, \*args, **kwargs)`\*\*:
   - Overridden for custom response formatting
   - Returns confirmation message with deleted book title

#### Custom Response Format:

```json
{
  "message": "Book \"Title\" deleted successfully"
}
```

## Permission Classes

### IsAuthenticated

- **Applied to**: Create, Update, Delete operations
- **Behavior**: Requires user to be logged in
- **Error Response**: 401 Unauthorized if not authenticated

### IsAuthenticatedOrReadOnly

- **Applied to**: List, Detail operations
- **Behavior**:
  - Anonymous users: Read-only access (GET)
  - Authenticated users: Full access
- **Error Response**: 401 only for write operations

## Data Validation

### BookSerializer Validation

1. **Publication Year Validation**:
   - Must not be in the future
   - Error message: "Publication year cannot be in the future."
2. **Required Fields**:
   - `title`: Required string
   - `publication_year`: Required integer
   - `author`: Required foreign key to Author model

## URL Patterns

```python
urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]
```

## Dependencies

```python
# Required in settings.py
INSTALLED_APPS = [
    'rest_framework',
    'django_filters',
    # ... other apps
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

## Custom Extensions

### Logging Integration

- `perform_create()` and `perform_update()` methods include logging
- Can be extended to use Django's logging framework

### Custom Filtering

- `get_queryset()` in UpdateView supports query parameter filtering
- Easily extensible for additional filtering logic

### Response Formatting

- All write operations return structured JSON responses
- Consistent error message formatting
- Clear success confirmations

## Usage Examples

### Creating a Book

```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <credentials>" \
  -d '{
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
  }'
```

### Filtering Books

```bash
# Filter by author
curl "http://127.0.0.1:8000/api/books/?author=1"

# Search by title
curl "http://127.0.0.1:8000/api/books/?search=Django"

# Order by publication year (descending)
curl "http://127.0.0.1:8000/api/books/?ordering=-publication_year"
```

### Updating a Book

```bash
# Full update
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <credentials>" \
  -d '{
    "title": "Updated Title",
    "publication_year": 2024,
    "author": 1
  }'

# Partial update
curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <credentials>" \
  -d '{
    "title": "New Title Only"
  }'
```

## Error Handling

The API returns consistent error responses:

### 400 Bad Request (Validation Errors)

```json
{
  "message": "Failed to create book",
  "errors": {
    "publication_year": ["Publication year cannot be in the future."],
    "title": ["This field is required."]
  }
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```
