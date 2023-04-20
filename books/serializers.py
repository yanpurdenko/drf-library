from rest_framework import serializers

from books.models import Genre, Book


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "description",
            "genres",
            "cover",
            "inventory",
            "daily_fee",
            "image",
        )
