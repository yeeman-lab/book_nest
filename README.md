# Book Nest

Book Nest is a web application built using Django that facilitates book clubs and bookshelf management. Users can create or join book clubs, discuss books, add books to their personal bookshelves, and manage their reading lists.

## Features

- **Book Clubs:** Users can create their own book clubs, join existing ones, and manage club activities.
- **Discussions:** Each book club has a discussion section where members can post questions and responses related to the current reading.
- **Bookshelf:** Users can add books to their personal bookshelves categorised by format (physical, Apple Books, Google Books, Kindle, etc.).
- **Search:** Integration with Open Library API allows users to search for books by title and author.
- **User Authentication:** Secure user authentication and authorisation system using Django's built-in authentication system.

## Directory Tree (created or modified files)

- `book_nest\` - Contains the URL configuration for the whole project.
  - `urls.py` - Defines URL patterns for the book_nest app.
- `main\` - Represents the main Django app of the project.
  - `migrations\` - Directory storing database migration files for the main app.
  - `static\main\` - Holds static files specific to the main app, such as JavaScript and CSS files.
  - `templates\main\` - Contains HTML templates for the main app.
    - `add_to_shelf.html` - Template for adding a book to the shelf.
    - `club_page.html` - Template for displaying details of a book club.
    - `create_club.html` - Template for creating a new book club.
    - `discussion.html` - Template for displaying and taking part of discussions within a book club.
    - `index.html` - Main template for the main app, mainy for exploring all book clubs of the web app.
    - `layout.html` - Base template extended by other templates.
    - `manage_club.html` - Template for managing a book club, includes option to delete the book club or set up book reading for a club.
    - `shelf.html` - Template for displaying the user's bookshelf.
    - `user_page.html` - Template for displaying user-specific information, which book clubs have been created or joined by the user.
  - `admin.py` - Registers models to be managed via Django's admin interface.
  - `forms.py` - Contains forms used within the main app.
  - `models.py` - Defines database models for the `main` app, such as `BookClub`, `Reading`, and `Shelf`.
  - `tests.py` - Contains unit tests to ensure the functionality and integrity of the application's models and views.
  - `urls.py` - Defines URL patterns for the main app.
  - `views.py` - Contains view functions for handling HTTP requests and rendering responses.
- `users\` - Represents the Django app for user-related functionality.
  - `migrations\` - Directory storing database migration files for the users app.
  - `templates\users\` Contains HTML templates for user-related views, such as login and registration.
    - `login.html` - Template for user login.
    - `register.html` - Template for user registration.
  - `forms.py` - Contains forms used within the users app.
  - `urls.py` - Defines URL patterns for the users app.
  - `views.py` - Contains view functions for user-related actions, such as login and registration.
- `README.md` - Documentation file providing information about the project.
- `db.sqlite3` - SQLite database file.
- `manage.py` - Django's command-line utility for administrative tasks.
- `requirements.txt` - Contains the Python packages and versions needed for the project.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yeeman-lab/projects/book_nest.git
```

2. Navigate to the project directory:

```bash
cd book_nest
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Access the application in your web browser at http://localhost:8000/.

## Unit Test

Performing unit tests ensures that the Book Nest web application functions as expected and meets the desired specifications. After installation, run the following command to execute the unit tests:

```bash
python manage.py test
```

### Test Cases Overview

1.  BookClubModelTestCase

- Tests the creation of a `BookClub` model instance.
- Verifies attributes such as club name, description, and status.

2. ReadingModelTestCase

- Tests the creation of a `Reading` model instance associated with a `BookClub`.
- Verifies attributes such as book name, author, and status.

3. QuestionModelTestCase

- Tests the creation of a `Question` model instance related to a `Reading`.
- Verifies attributes such as description, user, and reading association.

4. LoginRequiredViewsTestCase

- Tests views that require authentication to access.
- Verifies that unauthenticated users are redirected to the login page.

5. ShelfTestCase

- Tests adding and deleting books from the user's shelf.
- Verifies that book records are correctly added and deleted from the shelf.

6. BookClubTestCase

- Tests creating, deleting, joining, and leaving book clubs.
- Verifies the functionality related to managing book clubs, including membership.

## Usage

### Without registration / login

#### Landing page

All users can see a list of active book clubs displayed as cards on the roof route of the web app. Users can click on the club names to access individual club pages.

![Index](./main/static/main/readme/index.png)

#### Club page

On the club page, users can view detailed information about the club, including its description, current reading, previous readings shown inside a carousel, and option to join the club which will redirect them to login process before they can join.

![Club Page](./main/static/main/readme/club_page.png)

#### Register / Login

To access the full functionality of the application, users need to create an account. This account enables users to:

- Create a book club or join existing ones.
- Participate in discussions about books within each club.
- Add books to their personal bookshelf.
- Manage readings in book clubs they've created.

Django's built-in authentication system is used to handle registration and login processes. If users enter incorrect values or leave fields blank in the registration or login forms, they'll see flash messages guiding them on the next steps.

![Register](./main/static/main/readme/register.png)

![Login](./main/static/main/readme/login.png)

### After registration / login

Once registered and logged in, users gain access to the full range of features offered by the Book Nest application:

#### Create or Join Book Clubs

Users can create their own book clubs or browse existing ones to join. Creating a book club allows users to define the club's description, select the types of books to be read, and manage the club's activities.

![Create Club](./main/static/main/readme/create_club.png)

#### Search and Select Current Reading

To set the current reading or add new books to the club's reading list, club administrators can search for books using the integrated search feature. Search results display relevant book information, including title, publication year, and cover image. Administrators can then select a book to add it to the club's reading list.

![Manage Club](./main/static/main/readme/manage_club.png)

Once a book is selected, it is displayed as the current reading in the redirect page and displays options to `Finish current reading` or `Delete the club`.

![Manage Club with reading](./main/static/main/readme/manage_club_2.png)

#### Participate in Discussions

Within each book club, users can engage in discussions about the books being read. They can post questions, share thoughts, and respond to others' contributions, fostering a vibrant community around literature.

![Discussion](./main/static/main/readme/discussion.png)

#### Manage Personal Bookshelf

Users have the ability to manage their personal bookshelf. This feature allows users to organise their collection of books across different formats, such as Physical Print, Apple Books, Google Books, and Kindle Books.

#### Adding Books to the Shelf

Users can add books to their shelf by clicking on the `Add book to shelf` button on the shelf page. This action redirects them to a search page where they can search for books by title and author. The search results display relevant book information, including the book cover, title, and publication year.

![Add book to shelf](./main/static/main/readme/add_to_shelf.png)

#### Viewing and Managing Books

Once books are added to the shelf, users can view them categorised by format on the shelf page. Each book entry includes the book cover, title, publication year, and an option to delete the book from the shelf.

![Shelf](./main/static/main/readme/shelf.png)

#### User Page

The user page serves as a central hub for users within the web application. It provides users with essential information about the book club they are currently engaged with and offers options for managing their participation.

![User page](./main/static/main/readme/user_page.png)

## Mobile-responsive

The Book Nest web application is designed to provide an optimal viewing and interaction experience across a wide range of devices, including desktops, tablets, and smartphones.
This was achieved by using grid system, components, and utilities provided by Bootstrap CSS framework, and custom CSS rules and media queries.

![Mobile](./main/static/main/readme/mobile.png)

# Acknowledgements

- The project utilises the [Open Library API](https://openlibrary.org/) for book search functionality.
- Built with [Django](https://www.djangoproject.com/) web framework.
