from django.db import migrations
from django.conf import settings
import os.path
import csv
from django.core.files import File
import datetime
from django.utils.text import slugify

def load_book_data(apps, schema_editor):
    """
    Read a CSV file full of books and insert them into the database.
    """

    Book = apps.get_model('core', 'Book')
    Author = apps.get_model('core', 'Author')
    Category = apps.get_model('core', 'Category')

    datapath = os.path.join(settings.BASE_DIR, 'initial_data')
    datafile = os.path.join(datapath, 'list_of_books.csv')
    with open(datafile, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            book_title = row['title']
            
            author, _ = Author.objects.get_or_create(name=row['author'])
            category, _ = Category.objects.get_or_create(name=row['title'])
           
            
            if Book.objects.filter(title=book_title).count():
                continue
            book = Book(
                title=row['title'],
                author=author
                description=row['description'],
                url=row['url'],
                date_added=datetime.datetime.now(),
                slug=slugify(row['title']),
                category=category,)
                
            author.save()
            book.save()
            category.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_book_data)
    ]
