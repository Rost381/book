from django.db.models import Count, Case, When, Avg, F
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.utils import json

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(APITestCase):

    def setUP(self):
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')
        self.user_3 = User.objects.create(username='user_3')

        self.book_1 = Book.objects.create(name='Test book1', price=25,
                                          author_name='Author 1',
                                          discount =10)
        self.book_2 = Book.objects.create(name='Test book2', price=55,
                                          author_name='Author 5',
                                          discount =50)

        UserBookRelation.objects.create(user=self.user_1, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=self.user_2, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=self.user_3, book=self.book_1, like=True,
                                        rate=4)

        UserBookRelation.objects.create(user=self.user_1, book=self.book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=self.user_2, book=self.book_2, like=True,
                                        rate=4)
        UserBookRelation.objects.create(user=self.user_3, book=self.book_2, like=False)

    def test_ok(self):
        self.setUP()

        books =  Book.objects.all().annotate(annotated_likes=Count(Case#В случае
                                                                  (When #Когда
                                                                   (userbookrelation__like=True,
                                                                    then=1 #Возвращаем 1
                                                                    ))),
                                             rating = Avg('userbookrelation__rate')#Avg -среднее
                                             ).order_by('id') #Сортируем

        data = BookSerializer(books, many=True).data

        print(data)
        expected_data= [
                                {
                                'Id': self.book_1.id,
                                'name': 'Test book1',
                                'price': '25.00',
                                'author_name': 'Author 1',
                                'likes_count' : 3,
                                'annotated_likes': 3,
                                'rating' : 4.67
                                },
                                {
                                'id': self.book_2.id,
                                'name': 'Test book2',
                                'price': '55.00',
                                'author_name': 'Author 5',
                                'likes_count': 2,
                                'annotated_likes': 2,
                                'rating' : 3.50
                                }

                                ]

        self.assertEqual(data,expected_data)

    def test_query(self):
        self.setUP()


        books = Book.objects.all().annotate(annotated_likes=Count(Case  # В случае
                                                                  (When  # Когда
                                                                   (userbookrelation__like=True,
                                                                    then=1  # Возвращаем 1
                                                                    ))),
                                            rating=Avg('userbookrelation__rate'),  # Avg -среднее
                                            discount_price= F('price')-((F('discount'))*(F('price'))/100)
                                            ).order_by('id')  # Сортируем

        data = BookSerializer(books, many=True).data

        print(data)
        #discount_price = F('userbookrelation__price') - F('userbookrelation__discount')
