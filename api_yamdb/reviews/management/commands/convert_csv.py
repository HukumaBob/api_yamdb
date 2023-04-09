import logging
from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

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
        for model, csv in TABLES.items():
            with open(f"./static/data/{csv}", encoding="utf-8") as file:
                reader = DictReader(file)
                for data in reader:
                    obj, created = model.objects.get_or_create(**data)
                    if created:
                        logging.info(self.style.SUCCESS(f"Created {obj}"))
                    else:
                        logging.warning(f"{obj} already exists")
