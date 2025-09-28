from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the conversion between Book model instances
    and JSON data. It includes all fields from the Book model and
    provides custom validation for the publication_year field.
    """
    class Meta:
        model = Book
        fields = '__all__'  # Serializes all fields: id, title, publication_year, author
    
    def validate_publication_year(self, value):
        """
        Custom validation method for publication_year field.
        
        Ensures that the publication year is not set to a future date,
        which would be invalid for published books.
        
        Args:
            value: The publication_year value to validate
            
        Returns:
            The validated value if it passes validation
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer handles the conversion between Author model instances
    and JSON data. It includes the author's name and dynamically serializes
    all related books using the BookSerializer.
    
    Relationship Handling:
    - Uses the 'books' related_name from the Author-Book relationship
    - The 'books' field is set to read_only=True to prevent creation/updates
      of books through the author serializer
    - When an Author instance is serialized, all related Book instances
      are automatically included in the response using BookSerializer
    """
    # Nested serializer field that uses the related_name 'books' from the ForeignKey
    # many=True because one author can have multiple books
    # read_only=True prevents creating/updating books through this serializer
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['name', 'books']  # Only include name and the nested books