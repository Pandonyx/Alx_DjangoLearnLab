from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import datetime
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for Book API endpoints.
    
    Tests CRUD operations, filtering, searching, ordering, and permissions
    for the Book model API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data and authentication for each test.
        Creates test users, authors, books, and API client.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com', 
            password='adminpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='The Lord of the Rings',
            publication_year=1954,
            author=self.author3
        )
        
        # Set up API client
        self.client = APIClient()
        
        # URLs for testing
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.book_update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.book_delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})
    
    def authenticate_user(self, user=None):
        """Helper method to authenticate a user."""
        if user is None:
            user = self.user
        self.client.force_authenticate(user=user)
    
    def test_book_list_unauthenticated(self):
        """Test that unauthenticated users can view book list."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
    
    def test_book_list_authenticated(self):
        """Test that authenticated users can view book list."""
        self.authenticate_user()
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
    
    def test_book_detail_unauthenticated(self):
        """Test that unauthenticated users can view book details."""
        response = self.client.get(self.book_detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['author'], self.book1.author.pk)
    
    def test_book_detail_not_found(self):
        """Test 404 response for non-existent book."""
        response = self.client.get(self.book_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_book_create_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        book_data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_book_create_authenticated_valid_data(self):
        """Test successful book creation by authenticated user."""
        self.authenticate_user()
        book_data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Book created successfully')
        self.assertEqual(response.data['book']['title'], 'New Book')
        
        # Verify book was created in database
        new_book = Book.objects.get(title='New Book')
        self.assertEqual(new_book.publication_year, 2023)
        self.assertEqual(new_book.author, self.author1)
    
    def test_book_create_invalid_future_year(self):
        """Test validation for future publication year."""
        self.authenticate_user()
        current_year = datetime.now().year
        future_year = current_year + 1
        
        book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Failed to create book')
        self.assertIn('publication_year', response.data['errors'])
    
    def test_book_create_missing_required_fields(self):
        """Test validation for missing required fields."""
        self.authenticate_user()
        book_data = {
            'title': 'Incomplete Book'
            # Missing publication_year and author
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data['errors'])
        self.assertIn('author', response.data['errors'])
    
    def test_book_update_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        book_data = {
            'title': 'Updated Title',
            'publication_year': 2000,
            'author': self.author1.pk
        }
        response = self.client.put(self.book_update_url(self.book1.pk), book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_book_update_authenticated_valid_data(self):
        """Test successful book update by authenticated user."""
        self.authenticate_user()
        book_data = {
            'title': 'Updated Harry Potter',
            'publication_year': 1997,
            'author': self.author1.pk
        }
        response = self.client.put(self.book_update_url(self.book1.pk), book_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book updated successfully')
        self.assertEqual(response.data['book']['title'], 'Updated Harry Potter')
        
        # Verify book was updated in database
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Updated Harry Potter')
    
    def test_book_partial_update(self):
        """Test partial update (PATCH) of book."""
        self.authenticate_user()
        book_data = {'title': 'Partially Updated Title'}
        response = self.client.patch(self.book_update_url(self.book1.pk), book_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only title was updated
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Partially Updated Title')
        self.assertEqual(updated_book.publication_year, 1997)  # Should remain unchanged
    
    def test_book_delete_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        response = self.client.delete(self.book_delete_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_book_delete_authenticated(self):
        """Test successful book deletion by authenticated user."""
        self.authenticate_user()
        book_title = self.book1.title
        response = self.client.delete(self.book_delete_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'Book "{book_title}" deleted successfully')
        
        # Verify book was deleted from database
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book1.pk)


class BookFilteringTestCase(APITestCase):
    """
    Test suite for filtering, searching, and ordering functionality.
    """
    
    def setUp(self):
        """Set up test data for filtering tests."""
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books with varied data
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        
        self.book_list_url = reverse('book-list')
    
    def test_filter_by_author_id(self):
        """Test filtering books by author ID."""
        response = self.client.get(self.book_list_url, {'author': self.author2.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verify all returned books are by author2
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author2.pk)
    
    def test_filter_by_author_name(self):
        """Test filtering books by author name."""
        response = self.client.get(self.book_list_url, {'author_name': 'rowling'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.book1.title)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by exact publication year."""
        response = self.client.get(self.book_list_url, {'publication_year': 1949})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], '1984')
    
    def test_filter_by_year_range(self):
        """Test filtering books by publication year range."""
        response = self.client.get(self.book_list_url, {
            'year_from': 1945,
            'year_to': 1949
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verify all books are within the year range
        for book in response.data['results']:
            self.assertGreaterEqual(book['publication_year'], 1945)
            self.assertLessEqual(book['publication_year'], 1949)
    
    def test_filter_by_title(self):
        """Test filtering books by title."""
        response = self.client.get(self.book_list_url, {'title': 'harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Harry Potter', response.data['results'][0]['title'])
    
    def test_search_functionality(self):
        """Test global search across title and author name."""
        response = self.client.get(self.book_list_url, {'search': 'orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verify search found books by George Orwell
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author2.pk)
    
    def test_search_by_title(self):
        """Test search functionality with book title."""
        response = self.client.get(self.book_list_url, {'search': 'farm'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Animal Farm')
    
    def test_ordering_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        response = self.client.get(self.book_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_year_descending(self):
        """Test ordering books by publication year in descending order."""
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_ordering_by_author_name(self):
        """Test ordering books by author name."""
        response = self.client.get(self.book_list_url, {'ordering': 'author__name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should be ordered by author name: George Orwell, then J.K. Rowling
        first_book_author = response.data['results'][0]['author']
        last_book_author = response.data['results'][-1]['author']
        self.assertEqual(first_book_author, self.author2.pk)  # George Orwell
        self.assertEqual(last_book_author, self.author1.pk)   # J.K. Rowling
    
    def test_combined_filter_search_order(self):
        """Test combining filtering, searching, and ordering."""
        response = self.client.get(self.book_list_url, {
            'author_name': 'orwell',
            'ordering': 'publication_year'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Should be Orwell's books ordered by year: Animal Farm (1945), 1984 (1949)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, [1945, 1949])
    
    def test_no_results_filter(self):
        """Test filtering with no matching results."""
        response = self.client.get(self.book_list_url, {'author_name': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(response.data['count'], 0)


class AuthorAPITestCase(APITestCase):
    """
    Test suite for Author API endpoints.
    """
    
    def setUp(self):
        """Set up test data for author tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.author1 = Author.objects.create(name='Test Author 1')
        self.author2 = Author.objects.create(name='Test Author 2')
        
        # Create books for author1
        Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=self.author1
        )
        Book.objects.create(
            title='Book 2',
            publication_year=2021,
            author=self.author1
        )
        
        self.author_list_url = reverse('author-list')
        self.author_detail_url = lambda pk: reverse('author-detail', kwargs={'pk': pk})
    
    def test_author_list_view(self):
        """Test author list endpoint."""
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_author_detail_with_books(self):
        """Test author detail view includes nested books."""
        response = self.client.get(self.author_detail_url(self.author1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author 1')
        self.assertEqual(len(response.data['books']), 2)
    
    def test_author_detail_without_books(self):
        """Test author detail view for author without books."""
        response = self.client.get(self.author_detail_url(self.author2.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author 2')
        self.assertEqual(len(response.data['books']), 0)


class PermissionTestCase(APITestCase):
    """
    Test suite for API permissions and authentication.
    """
    
    def setUp(self):
        """Set up test users and data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        
        self.book_create_url = reverse('book-create')
        self.book_update_url = reverse('book-update', kwargs={'pk': self.book.pk})
        self.book_delete_url = reverse('book-delete', kwargs={'pk': self.book.pk})
    
    def test_read_permissions_unauthenticated(self):
        """Test that unauthenticated users can read but not write."""
        # Read operations should work
        list_response = self.client.get(reverse('book-list'))
        detail_response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))
        
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
    
    def test_write_permissions_unauthenticated(self):
        """Test that unauthenticated users cannot perform write operations."""
        book_data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        
        # Write operations should fail
        create_response = self.client.post(self.book_create_url, book_data)
        update_response = self.client.put(self.book_update_url, book_data)
        delete_response = self.client.delete(self.book_delete_url)
        
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_user_permissions(self):
        """Test that authenticated users can perform all operations."""
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        
        # All operations should work for authenticated users
        create_response = self.client.post(self.book_create_url, book_data)
        update_response = self.client.put(self.book_update_url, book_data)
        
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)


class SerializerTestCase(TestCase):
    """
    Test suite for model serializers.
    """
    
    def setUp(self):
        """Set up test data for serializer tests."""
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
    
    def test_book_serializer_valid_data(self):
        """Test BookSerializer with valid data."""
        serializer_data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        serializer = BookSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
    
    def test_book_serializer_invalid_future_year(self):
        """Test BookSerializer validation for future year."""
        current_year = datetime.now().year
        serializer_data = {
            'title': 'Future Book',
            'publication_year': current_year + 1,
            'author': self.author.pk
        }
        serializer = BookSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)
    
    def test_author_serializer_with_books(self):
        """Test AuthorSerializer includes nested books."""
        serializer = AuthorSerializer(self.author)
        self.assertEqual(serializer.data['name'], 'Test Author')
        self.assertEqual(len(serializer.data['books']), 1)
        self.assertEqual(serializer.data['books'][0]['title'], 'Test Book')