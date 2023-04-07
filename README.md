
## Description of the YaMDb project
The YaMDb project collects user feedback on works.
Produced by categories: "Books", "Films", "Music".
The list of categories can be extended by the administrator (for example,
you can add Fine Art or Jewelery changes).

The works themselves are not found in YaMDb, you cannot watch the movie or
listen to music.
In each category there are works: books, films or music. For example,
in the category "Books" there can be works "Winnie the Pooh and all-all-all" and
"Martian Chronicles", and in the category "Music" - the song "Davecha" of the group
"Insects" and Bach's second suite.

A work can be assigned a genre from the list of preset
(for example, "Fairy Tale", "Rock" or "Arthouse"). New genres can only be created
administrator.

Grateful or indignant users leave text messages for the works
reviews and rate the product in the range from one to ten
(integer); an average rating is formed from user ratings
works - rating. For one work, the user can
leave only one review.

### User registration algorithm
1. The user sends a POST request to add a new user with
email and username parameters to the /api/v1/auth/signup/ endpoint.
2. YaMDB sends an email with a confirmation code (confirmation_code) to the email address.
3. The user sends a POST request with the parameters username and
confirmation_code to the /api/v1/auth/token/ endpoint, in response to a request to it
comes token (JWT token). As a result, the user receives a token and can
work with the project's API by sending this token with each request.
4. To re-receive a letter with a confirmation code, the user sends
POST request with username and email parameters to the /api/v1/auth/remind/ endpoint.
5. Optionally, the user sends a PATCH request to the endpoint
/api/v1/users/me/ and fill in the fields in your profile.
6. If the user is created by an administrator, for example, via a POST request to
endpoint api/v1/users/ - a letter with a code also comes to his mail.

### Custom roles
- **Anonymous** - can view descriptions of works, read reviews and comments.
- **Authenticated user (user)** - can, like **Anonymous**, read everything,
in addition, he can publish reviews and rate works
(movies / books / songs), can comment on other people's reviews; can edit
and delete your reviews and comments. This role is assigned by default.
for every new user.
- **Moderator** - same rights as **Authenticated**
user plus the right to remove any reviews and comments.
- **Administrator (admin)** — full rights to manage all project content.
Can create and delete works, categories and genres. Can prescribe
user roles.
- **Django Superuser** - has administrator rights (admin). Even
change the user role of the superuser - this will not deprive him of administrative rights.
A superuser is always an administrator, but an administrator is not necessarily a superuser.

### YaMDb API resources
- Resource **auth**: authentication.
- Resource **users**: users.
- Resource **titles**: works to which they write reviews (a certain movie, book or song).
- Resource **categories**: categories (types) of works ("Films", "Books", "Music"). One work can only be assigned to one category.
- Resource **genres**: genres of works. One work can be tied to several genres.
- Resource **reviews**: reviews of works. The review is tied to a specific product.
- Resource **comments**: comments on reviews. The comment is tied to a specific review.

## Launch of the project

- Install and activate the virtual environment
- Install dependencies from requirements.txt file
```
python -m pip install --upgrade pip

pip install -r requirements.txt
```
- Run migrations:
```
python manage.py migrate
```

- In the folder with the manage.py file, run the command:
```
python manage.py runserver
```

## Management command that adds data to the database via Django ORM

- In the folder with the manage.py file, run the command:
```
python manage.py convert_csv
```