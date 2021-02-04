from unittest import TestCase

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from store.logic import set_rating
from store.models import UserBookRelation, Book


class SetRaringTestCase(APITestCase):
    def setUp(self):
        self.user_u1 = User.objects.create(username='test_username_11')
        self.user_u2 = User.objects.create(username='test_username_12')
        self.user_u3 = User.objects.create(username='test_username_13')

        self.book_1 = Book.objects.create(name='Test book1', price=25,
                                          author_name='Author 1', owner=self.user_u1,

                                          discount =10)


        UserBookRelation.objects.create(user=self.user_u1, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=self.user_u2, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=self.user_u3, book=self.book_1, like=True,
                                        rate=4)

    def test_ok(self):
        #self.setUp()
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))