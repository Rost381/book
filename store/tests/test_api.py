import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):

    def test_setUP(self):
        '''
        Создание пользователя и начальных книг
        '''
        self.user = User.objects.create(username='test_username')

        self.book1 = Book.objects.create(name='Test book1', price=25,
                                         author_name='Author 1', owner = self.user)
        self.book2 = Book.objects.create(name = 'Test book2', price = 55,
                                         author_name = 'Author 5', owner = self.user)
        self.book3 = Book.objects.create(name = 'Test book Author 1', price = 55,
                                         author_name = 'Author 2', owner = self.user)
        self.book4 = Book.objects.create(name='Test book4', price=27,
                                         author_name='Author 4',owner = self.user)

    def test_get(self):
        '''
        Проверка чтения списка всех книг
        '''
        self.test_setUP()
        url = reverse('book-list')
        print(url)
        response = self.client.get(url)
        print('response: ',response)
        print('response.data: ',response.data)
        #print(self.book1, self.book2,)
        serializer_data = BookSerializer([self.book1, self.book2,
                                          self.book3,self.book4], many = True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        '''
        Проверка фильтрации списка по цене
        '''
        self.test_setUP()
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url,data = {'price' : 55})
        # print('response: ',response)
        # print('response.data: ',response.data)
        #print(self.book1, self.book2,)
        serializer_data = BookSerializer([self.book2, self.book3], many = True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        '''
        Проверка поиска по автору
        '''
        self.test_setUP()
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url,data = {'search' :'Author 1'})
        # print('response: ',response)
        # print('response.data: ',response.data)
        #print(self.book1, self.book2,)
        serializer_data = BookSerializer([self.book1, self.book3], many = True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        '''
        Проверка сортировки
        '''
        self.test_setUP()
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url,data = {'ordering' :'price'})
        # print('response: ',response)
        # print('response.data: ',response.data)
        #print(self.book1, self.book2,)
        serializer_data = BookSerializer([self.book1,self.book4,
                                          self.book2, self.book3], many = True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        '''
        Проверка возможности создания
        '''
        self.test_setUP()
        self.user = User.objects.create(username='test_username2')
        print('Проверка  возможности   создания')
        self.assertEqual(4, Book.objects.all().count())
        url = reverse('book-list')
        data = {
    "name": "Programming in Python 3",
    "price": "150.00",
    "author_name": "Mark Sommerfeld-Junior",
        }
        json_data = json.dumps(data)
        #self.client.force_login(self.user)
        print('url',url)
        print('self.user', self.user)
        response = self.client.post(url, data=json_data,
                                   content_type='application/json')

        print('response: ',response)
        print('Book.objects.all(): ',Book.objects.all())

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)



    def test_update(self):
        '''
        Проверка возможности изменения Пользователем
        '''
        self.test_setUP()
        self.assertEqual(4, Book.objects.all().count())
        url = reverse('book-detail',args=(self.book1.id,))
        data = {
    "name": self.book1.name,
    "price": 575,
    "author_name": self.book1.author_name
}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        # print(url)

        response = self.client.put(url, data =json_data,
                                   content_type='application/json')
        # print('response: ',response)
        # print('response.data: ',response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #self.book1 = Book.objects.get(id=self.book1.id)
        self.book1.refresh_from_db() #Достает из базы
        self.assertEqual(575,self.book1.price)

    def test_update_not_owner(self):
        #self.user = User.objects.create(username='test_username')
        self.test_setUP()
        self.user2 = User.objects.create(username='test_username2')
        self.assertEqual(4, Book.objects.all().count())
        url = reverse('book-detail',args=(self.book1.id,))
        data = {
    "name": self.book1.name,
    "price": 575,
    "author_name": self.book1.author_name
}
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        print(url)

        response = self.client.put(url, data =json_data,
                                   content_type='application/json')
        # print('response: ',response)
        # print('response.data: ',response.data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual( {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')},response.data)
        #self.book1 = Book.objects.get(id=self.book1.id)
        self.book1.refresh_from_db() #Достает из базы
        self.assertEqual(25,self.book1.price)

    def test_update_not_owner_but_staff(self):
        '''
        Проверка возможности изменения Персоналом
        '''
        self.test_setUP()
        self.user2 = User.objects.create(username='test_username2',
                                             is_staff = True)
        self.assertEqual(4, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
                "name": self.book1.name,
                "price": 575,
                "author_name": self.book1.author_name
            }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        # print(url)
        response = self.client.put(url, data=json_data,
                                       content_type='application/json')
        # print('response: ', response)
        # print('response.data: ', response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book1 = Book.objects.get(id=self.book1.id)# Достает из базы
        self.book1.refresh_from_db()  # Достает из базы
        self.assertEqual(575, self.book1.price)

class BooksRelationTestCase(APITestCase):
    def test_setUP(self):
    #def __init__(self):
        '''
        Создание пользователя и начальных книг
        '''
        self.user = User.objects.create(username='test_username')
        self.book1 = Book.objects.create(name='Test book1', price=25,
                                         author_name='Author 1', owner = self.user)
        self.book2 = Book.objects.create(name = 'Test book2', price = 55,
                                         author_name = 'Author 5', owner = self.user)

    def test_like(self):
        '''
        Проверка 'like'
        '''
        self.test_setUP()
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        #Тest  like
        data = {
                "like": True
            }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                       content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                 book=self.book1)

        self.assertTrue(relation.like)

        # Тest Bookmarks
        data = {
                "in_bookmarks": True
            }
        json_data = json.dumps(data)

        response = self.client.patch(url, data=json_data,
                                       content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        '''
        Тest 'rate'
        '''
        self.test_setUP()
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
                "rate": 5,
            }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                       content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book1)
        self.assertEqual(5, relation.rate)

    def test_rate_wrong(self):
        '''
        Тest 'rate' with non-possible arg
        '''
        self.test_setUP()
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            "rate": 25,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
