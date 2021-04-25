from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Book, UserBookRelation


#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('id', 'name', "author_name", 'price', 'rating', )
    search_fields = ('id', 'name', 'author_name',)
    list_filter = ("author_name", 'rating', )
    list_display_links = ('name', 'author_name')
    ordering = ('id',)

@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    pass
