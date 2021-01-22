from unittest import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ok(self):
        self.book1 = Book.objects.create(name='Test book1', price=25,
                                         author_name='Author 1')
        self.book2 = Book.objects.create(name='Test book2', price=55,
                                         author_name='Author 5')

        data = BookSerializer([self.book1, self.book2], many=True)
        print(data)
        expected_data= [
                                {
                                'Id': self.book1.id,
                                'name': 'Test book1',
                                'price': '25.00',
                                'author_name': 'Author 1'
                                },
                                {
                                'id': self.book2.id,
                                'name': 'Test book2',
                                'price': '55.00',
                                'author_name': 'Author 5'
                                }

                                ]
        self.assertEqual(data, expected_data)