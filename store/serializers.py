from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


class BookSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField() #Новое поле Сериалайзера
    annotated_likes = serializers.IntegerField(read_only=True) #Новое поле Сериалайзера
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    discount_price = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True) #Цеа со скидкой

    class Meta:
        model = Book
        #fields = '__all__'
        fields = ('id' ,'name',  'author_name', 'price', 'discount', 'discount_price', 'likes_count','annotated_likes', 'rating')

    # self - Самм сериализатор, instance то что сериализуем
    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()

class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = '__all__'
