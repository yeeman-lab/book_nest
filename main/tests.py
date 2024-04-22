from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import BookClub, BookFormat, Reading, Question, Response, Shelf, Type, JoinClub
from datetime import date


class BookClubModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='password123')
        self.book_club = BookClub.objects.create(
            club_name='Test Club',
            date_created=timezone.now(),
            club_description='Test description',
            user=self.user,
            status='A'
        )

    def test_book_club_creation(self):
        self.assertEqual(self.book_club.club_name, 'Test Club')
        self.assertEqual(self.book_club.club_description, 'Test description')
        self.assertEqual(self.book_club.status, 'A')
        self.assertEqual(self.book_club.user, self.user)


class ReadingModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='password123')
        self.book_club = BookClub.objects.create(
            club_name='Test Club',
            date_created=timezone.now(),
            club_description='Test description',
            user=self.user,
            status='A'
        )
        self.reading = Reading.objects.create(
            club=self.book_club,
            cover_edition_key='123',
            book_name='Test Book',
            publish_year=2020,
            author='Test Author',
            status='A'
        )

    def test_reading_creation(self):
        self.assertEqual(self.reading.book_name, 'Test Book')
        self.assertEqual(self.reading.status, 'A')
        self.assertEqual(self.reading.club, self.book_club)


class QuestionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='password123')
        self.book_club = BookClub.objects.create(
            club_name='Test Club',
            date_created=timezone.now(),
            club_description='Test description',
            user=self.user,
            status='A'
        )
        self.reading = Reading.objects.create(
            club=self.book_club,
            cover_edition_key='123',
            book_name='Test Book',
            publish_year=2020,
            author='Test Author',
            status='A'
        )
        self.question = Question.objects.create(
            description='Test question',
            user=self.user,
            reading=self.reading,
            date=timezone.now()
        )

    def test_question_creation(self):
        self.assertEqual(self.question.description, 'Test question')
        self.assertEqual(self.question.user, self.user)
        self.assertEqual(self.question.reading, self.reading)

# Add more test cases for other models if needed


class LoginRequiredViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_manage_club_view(self):
        response = self.client.get('/manage_club/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/users/login')

    def test_shelf_view(self):
        response = self.client.get('/shelf', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/users/login?next=/shelf')

    def test_user_page_view(self):
        response = self.client.get('/user_page', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/users/login?next=/user_page')


class ShelfTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        # Create a shelf record for testing delete book
        cover_edition_key = '30113'
        book_name = 'Harry Potter'
        publish_year = 2003
        author = 'J. K. Rowling'
        format = BookFormat.objects.get(pk=1)
        self.shelf = Shelf.objects.create(
            cover_edition_key=cover_edition_key, book_name=book_name, publish_year=publish_year, author=author, format=format, user=self.user, status='A')

    def test_add_book(self):
        before_shelf_size = len(Shelf.objects.filter(
            user=self.user, format=1, status='A'))
        cover_edition_key = '29596'
        book_name = 'Peter Pan'
        publish_year = 2003
        author = 'Namrata Tripathi'
        format = 1
        form_data = {'cover_edition_key': cover_edition_key,
                     'book_name': book_name, 'publish_year': publish_year, 'author': author, 'format': format}
        self.client.post("/submit_shelf", form_data)
        shelf_list = Shelf.objects.filter(
            user=self.user, format=1, status='A')
        after_shelf_size = len(shelf_list)

        find_shelf = [
            shelf for shelf in shelf_list if shelf.cover_edition_key == cover_edition_key and shelf.book_name == book_name and shelf.publish_year == publish_year and shelf.author == author and shelf.format == BookFormat.objects.get(pk=1)]

        self.assertEqual(before_shelf_size + 1, after_shelf_size)
        self.assertEqual(len(find_shelf), 1)

    def test_delete_book(self):
        before_shelf_size = len(Shelf.objects.filter(
            user=self.user, format=1, status='A'))
        self.client.post("/shelf_del_book/" + str(self.shelf.id))
        shelf_list = Shelf.objects.filter(
            user=self.user, format=1, status='A')
        after_shelf_size = len(shelf_list)
        find_shelf = [
            shelf for shelf in shelf_list if shelf.cover_edition_key == self.shelf.cover_edition_key and shelf.book_name == self.shelf.book_name and shelf.publish_year == self.shelf.publish_year and shelf.author == self.shelf.author and shelf.format == self.shelf.format]

        self.assertEqual(before_shelf_size - 1, after_shelf_size)
        self.assertEqual(len(find_shelf), 0)


class BookClubTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Create a Book Club for testing delele book club
        club_name = "Book Club A"
        date_created = date.today()
        club_description = "Testing Club A"
        status = 'A'
        types = [Type.objects.get(pk=1)]
        self.book_club_a = BookClub.objects.create(
            club_name=club_name, date_created=date_created, club_description=club_description, user=self.user, status=status)
        self.book_club_a.types.set(types)

        # Create a Book Club for testing join book club
        club_name = "Book Club B"
        date_created = date.today()
        club_description = "Testing Club B"
        status = 'A'
        types = [Type.objects.get(pk=2)]
        self.book_club_b = BookClub.objects.create(
            club_name=club_name, date_created=date_created, club_description=club_description, user=self.user, status=status)
        self.book_club_b.types.set(types)

        # Create a Book Club and Join for testing leave book club
        club_name = "Book Club C"
        date_created = date.today()
        club_description = "Testing Club C"
        status = 'A'
        types = [Type.objects.get(pk=2)]
        self.book_club_c = BookClub.objects.create(
            club_name=club_name, date_created=date_created, club_description=club_description, user=self.user, status=status)
        self.book_club_c.types.set(types)
        JoinClub.objects.create(
            user=self.user, club=self.book_club_c, status='A')

    def test_create_book_club(self):
        club_name = "Test Create Book Club"
        date_created = date.today()
        club_description = "Testing Create Club"
        status = 'A'
        types = [1, 2]
        before_number_of_created_club = len(BookClub.objects.filter(
            user=self.user, status='A'))
        form_data = {'club_name': club_name,
                     'date_created': date_created, 'club_description': club_description, 'status': status, 'types': types}
        self.client.post("/create_club", form_data)
        club_list = BookClub.objects.filter(
            user=self.user, status='A')
        after_number_of_created_club = len(club_list)

        find_book_club = [
            book_club for book_club in club_list if book_club.club_name == club_name and book_club.date_created == date_created and book_club.club_description == club_description]

        self.assertEqual(before_number_of_created_club +
                         1, after_number_of_created_club)
        self.assertEqual(len(find_book_club), 1)

    def test_delete_book_club(self):
        before_number_of_created_club = len(BookClub.objects.filter(
            user=self.user, status='A'))
        self.client.post("/delete_club/" + str(self.book_club_a.id))
        club_list = BookClub.objects.filter(
            user=self.user, status='A')
        after_number_of_created_club = len(club_list)

        find_book_club = [
            book_club for book_club in club_list if book_club.club_name == self.book_club_a.club_name and book_club.date_created == self.book_club_a.date_created and book_club.club_description == self.book_club_a.club_description]

        self.assertEqual(before_number_of_created_club -
                         1, after_number_of_created_club)
        self.assertEqual(len(find_book_club), 0)

    def test_join_book_club(self):
        before_no_of_joint_club = len(JoinClub.objects.filter(
            user=self.user, status='A'))
        self.client.post("/join_club/" + str(self.book_club_b.id))
        after_no_of_joint_club = len(JoinClub.objects.filter(
            user=self.user, status='A'))
        self.assertEqual(before_no_of_joint_club +
                         1, after_no_of_joint_club)
        self.assertTrue(JoinClub.objects.filter(
            user=self.user, club=self.book_club_b, status='A').exists())

    def test_leave_book_club(self):
        before_no_of_joint_club = len(JoinClub.objects.filter(
            user=self.user, status='A'))
        self.client.post("/leave_club/" + str(self.book_club_c.id))
        after_no_of_joint_club = len(JoinClub.objects.filter(
            user=self.user, status='A'))
        self.assertEqual(before_no_of_joint_club -
                         1, after_no_of_joint_club)
        self.assertFalse(JoinClub.objects.filter(
            user=self.user, club=self.book_club_c, status='A').exists())
