from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Book, UserBookRelation


#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass

@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    pass
