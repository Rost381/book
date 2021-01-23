from django.shortcuts import render

# Create your views here.
#from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer, UserBookRelationSerializer\

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_field = ['price', 'author_name']



class UserBookRelationView(ModelViewSet, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['book', 'user']
    search_fields = ['book', 'user']
    ordering_field = ['book', 'user']

    lookup_field = 'book'

    def mean_rate(self):
        booksrelation = UserBookRelation.objects.filter(book=self.kwargs['book'])
        miean_rate = 0
        print(booksrelation)
        for book in booksrelation:
            miean_rate += book.rate
        print(miean_rate/len(booksrelation))
        queryset = Book.objects.get(pk=self.kwargs['book'])
        print(queryset)

    def get_object(self):

        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        self.mean_rate()
        return obj



def perform_create(self, serializer):
    serializer.validated_data['owner'] = self.request.user
    serializer.save()


#@csrf_exempt
def auth(request):
    return render(request, 'oauth.html', {})

