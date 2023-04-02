from csv import DictReader
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from user.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if User.objects.exists():
            print('user data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading users data")

        # Code to load the data into database
        for row in DictReader(open('./static/data/users.csv')):
            user = User(
                id=row['id'], username=row['username'],
                email=row['email'], role=row['role'],
                bio=row['bio'], first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()
