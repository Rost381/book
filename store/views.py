from django.db.models import Count, When, Case, Avg, F
from django.shortcuts import render

# Create your views here.
#from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.logic import set_rating
from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer, UserBookRelationSerializer\


class BookViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    queryset = Book.objects.all().annotate(annotated_likes=Count(# Подсчет 1 возвращенных then=1
                                                                Case#В случае
                                                                  (When #Когда
                                                                   (userbookrelation__like=True,
                                                                    then=1 #Возвращаем 1
                                                                    ))),
                                       # rating = Avg('userbookrelation__rate'),#Avg -среднее
                                        discount_price=F('price') - ((F('discount')) * (F('price')) / 100),
                                        owner_name =F('owner__username')  #Сразу выбирает одного
                                            # ).select_related('owner' # Выбирает ОДНОГО owner из сериалайзерп
                    # если там owner_name = serializers.CharField(source= 'owner.username', default = "", read_only=True)
                                                    ).prefetch_related('readers' # Выбирает ВСЕХ
                                                             ).order_by('id') #Сортируем
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_field = ['price', 'author_name']


class UserBookRelationView(ModelViewSet): #, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['book', 'user']
    search_fields = ['book', 'user']
    ordering_field = ['book', 'user']
    #№ Для того, что бы передать вместо ID Relation ID Книги
    lookup_field = 'book'
    #
    # def mean_rate(self):
    #     '''
    #     Calculate mean rate
    #     '''
    #     books_relation = UserBookRelation.objects.filter(book=self.kwargs['book'])
    #     mean_rate = 0
    #     print(books_relation)
    #     for book in books_relation:
    #         mean_rate += book.rate
    #     print(mean_rate/len(books_relation))
    #     queryset = Book.objects.get(pk=self.kwargs['book'])
    #     print(queryset.price)
    #     # TODO Записать в поле BOOK
    #
    # def sum_likes(self):
    #     '''
    #     Calculate summary likes
    #     '''
    #
    #     likes_relation = UserBookRelation.objects.filter(book=self.kwargs['book'])
    #     likes_rate = 0
    #     print(likes_relation)
    #     for book in likes_relation:
    #         if (book.like):
    #             likes_rate+= 1
    #     print(likes_rate)
    #     queryset = Book.objects.get(pk=self.kwargs['book'])
    #     print(self.request.method)
    #     print(self.request.data)
    #     #TODO Записать в поле BOOK


    def get_object(self):
    # book_id=self.kwargs['book'] приходит из lookup_field = 'book' -эо ID Книги
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        #obj.save()
        print('get_object', self.request.data)
       # Расчитыват средний рейтинг и общин лайки
       #  if 'rate' in self.request.data:
       #      print("CALL VIEW ")
       #      set_rating(book=self.kwargs['book'])
       #  elif 'like' in self.request.data:
       #      self.sum_likes()
        return obj



def perform_create(self, serializer):
    serializer.validated_data['owner'] = self.request.user
    serializer.save()


#@csrf_exempt
def auth(request):
    return render(request, 'oauth.html', {})

