import logging
from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

# Dictionary mapping models to their corresponding CSV files
TABLES = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv",
    Title.genre.through: "genre_title.csv",
}


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from user.csv"

    def handle(self, *args, **kwargs):
        # Iterate over the models and their respective CSV files
        for model, csv in TABLES.items():
            # Open the CSV file
            with open(f"./static/data/{csv}", encoding="utf-8") as file:
                # Create a dictionary reader for the CSV file
                reader = DictReader(file)
                # Iterate over each row in the CSV file
                for data in reader:
                    # Get or create an object of the current model using the row data
                    obj, created = model.objects.get_or_create(**data)
                    # Check if the object was newly created or already existed
                    if created:
                        logging.info(self.style.SUCCESS(f"Created {obj}"))
                    else:
                        logging.warning(f"{obj} already exists")
