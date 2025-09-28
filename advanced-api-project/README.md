# Advanced API Project Documentation

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
