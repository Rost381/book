from store.models import Book


def operation():
    book1 = Book.objects.get(pk='1')
    book2 = Book.objects.get(pk='2')
    book3 = Book.objects.get(pk='3')
    print(book1, book2, book3)

