from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255)
    # Владелец related_name -
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              related_name='my_books')

   #Читатель through UserBookRelation- Через какую модель идет связь ManyToManyField
    #У читателя есть книгИ, у книги есть читателИ
    readers = models.ManyToManyField(User, through='UserBookRelation',
                                     related_name='books')
    discount =models.DecimalField(max_digits=2, decimal_places=0, null=True)


    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
    
    def __str__(self):
        return f'Id: {self.id} {self.name},  {self.author_name}, Владелец: {self.owner}' \
               f' Цена: {self.price} Скидка: {self.author_name} процентов'


class UserBookRelation(models.Model):
    '''
    Промежутичная модель ManyToManyField
    для User и Book
    '''
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    class Meta:
        verbose_name = 'Лайки, закладки, рейтинг'
        verbose_name_plural = 'Лайки, закладки, рейтинг'

    def __str__(self):
        return f'{self.user.username}: {self.book.name}, Like: {self.like}, ' \
               f' in_bookmarks {self.in_bookmarks}, RATE: {self.rate}'



