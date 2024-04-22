from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from .forms import CreateClubForm, SearchBookForm, AddToShelfForm, ManageClubForm, QuestionForm, ResponseForm
from datetime import date
from .models import BookClub, Shelf, Reading, JoinClub, Question, Response
import requests
import urllib
from requests.exceptions import RequestException


@register.filter
def get_dict_value(dict, key):
    return dict[key]


@register.filter
def add_3_dots(str):
    dots = "..."
    limit = 15
    if len(str) > limit:
        return str[0:limit] + dots
    return str


# function to call API
def make_api_call(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except RequestException as e:
        # Handle network errors or invalid responses from the API
        print("Error occurred during API call:", e)
        return None

# Create your views here.


# landing page of website to show all active book clubs with current reading
def index(request):
    # find out all books clubs with current reading
    clubs_with_reading = Reading.objects.filter(status="A").values("club")
    # filter those clubs are still active
    active_club_with_reading = BookClub.objects.filter(
        status="A", id__in=clubs_with_reading)
    # Hash table to contain each active book club id and its current reading
    clubs_current_reading = {}
    for club in active_club_with_reading:
        current_reading = Reading.objects.get(
            status="A", club=club)
        clubs_current_reading[club.id] = current_reading.cover_edition_key

    return render(request, "main/index.html", {"active_clubs": active_club_with_reading, "clubs_current_reading": clubs_current_reading})


# webpage for functionality to add book to book shelf
@login_required(redirect_field_name=None)
def add_to_shelf(request):
    # django form for users to input book name and author to search for a book
    form = SearchBookForm()
    # django form for users to select the correct book from search results
    add_shelf_form = AddToShelfForm()

    ui_search_results = []

    # call API to get results based on users' input
    if request.method == "POST" and 'search_book' in request.POST:
        form = SearchBookForm(request.POST)
        api_url = "https://openlibrary.org/search.json"
        params = {
            'title': form["book_name"].value(),
            'page': 1,
            'limit': 9,
            'q': "first_publish_year:* AND cover_i:* AND author_name:*"
        }
        if form["author_name"].value():
            params['author'] = form["author_name"].value()

        try:
            api_result = make_api_call(api_url, params=params)
            if api_result:
                docs = api_result.get("docs", [])
                # Process the API response
                for item in docs:
                    book_info = {}
                    book_info["author_name"] = ", ".join(item["author_name"])
                    book_info["title"] = item["title"]
                    book_info["publish_year"] = item["first_publish_year"]
                    if "cover_i" in item:
                        book_info["cover_id"] = item["cover_i"]
                    ui_search_results.append(book_info)
            print(ui_search_results)
        except Exception as e:
            # Handle any other unexpected exceptions
            print("Error occurred:", e)

    return render(request, "main/add_to_shelf.html", {"form": form, "ui_search_results": ui_search_results, "add_shelf_form": add_shelf_form})


# when user selects a particular book from search results, this functionality adds the book to the shelf
@login_required(redirect_field_name=None)
def submit_shelf(request):
    if request.method == "POST":
        add_shelf_form = AddToShelfForm(request.POST)
        if add_shelf_form.is_valid():
            user = request.user
            cover_edition_key = add_shelf_form.cleaned_data["cover_edition_key"]
            book_name = add_shelf_form.cleaned_data["book_name"]
            publish_year = add_shelf_form.cleaned_data["publish_year"]
            author = add_shelf_form.cleaned_data["author"]
            format = add_shelf_form.cleaned_data["format"]
            status = 'A'
            new_shelf = Shelf.objects.create(
                cover_edition_key=cover_edition_key, book_name=book_name, publish_year=publish_year, author=author, format=format, user=user, status=status)
            new_shelf.save()
            return HttpResponseRedirect(reverse("main:shelf"))


# webpage to show information of a book club and option to manage, join or leave that club
def club_page(request, club_id):
    club = BookClub.objects.get(pk=club_id)
    # check if the club has current reading
    current_book = None
    if Reading.objects.filter(club=club, status="A").exists():
        current_book = Reading.objects.get(club=club, status="A")
    # check if the club has previous readings
    if Reading.objects.filter(club=club, status="D").exists():
        finish_books = Reading.objects.filter(club=club, status="D")
    else:
        finish_books = None

    # check if the user has created or joined the club
    is_joined = False
    is_creator = False
    if request.user.is_authenticated:
        user = request.user
        if JoinClub.objects.filter(user=user, club=club_id, status='A').exists():
            is_joined = True
        if BookClub.objects.filter(id=club_id, user=user).exists():
            is_creator = True
    return render(request, "main/club_page.html", {"club": club, "current_book": current_book, "finish_books": finish_books, "is_joined": is_joined, "is_creator": is_creator})


# functionality for users to join a book club
@login_required(redirect_field_name=None)
def join_club(request, club_id):
    if request.method == "POST":
        user = request.user
        club = BookClub.objects.get(pk=club_id)
        new_join = JoinClub.objects.create(user=user, club=club, status='A')
        new_join.save()
        return HttpResponseRedirect(reverse("main:club_page", args=[club_id]))


# functionality for users to leave a book club
@login_required(redirect_field_name=None)
def leave_club(request, club_id):
    if request.method == "POST":
        user = request.user
        club = BookClub.objects.get(pk=club_id)
        leave = JoinClub.objects.get(user=user, club=club, status="A")
        leave.status = "D"
        leave.save()
        return HttpResponseRedirect(reverse("main:club_page", args=[club_id]))


# webpage for users to create their own book club
@login_required(redirect_field_name=None)
def create_club(request):
    if request.method == "POST":
        # django form to require users to input information needed to create a book club
        form = CreateClubForm(request.POST)
        if form.is_valid():
            club_name = form.cleaned_data["club_name"]
            date_created = date.today()
            club_description = form.cleaned_data["club_description"]
            user = request.user
            status = 'A'
            types = form.cleaned_data["types"][:3]
            new_club = BookClub.objects.create(
                club_name=club_name, date_created=date_created, club_description=club_description, user=user, status=status)
            new_club.types.set(types)
            new_club.save()
            return HttpResponseRedirect(reverse("main:manage_club", args=[new_club.id]))

    form = CreateClubForm()
    return render(request, "main/create_club.html", {"form": form})


# functionality for book club owner to delete that club
@login_required(redirect_field_name=None)
def delete_club(request, club_id):
    user = request.user
    # check if the user is the owner of the book club
    is_creator = False
    if BookClub.objects.filter(pk=club_id, user=user).exists():
        is_creator = True
    if request.method == "POST" and is_creator:
        club = BookClub.objects.get(pk=club_id)
        club.status = "D"
        club.save()
        return HttpResponseRedirect(reverse("main:user_page"))


# functionality for book club owner to change the current reading for that club
@login_required(redirect_field_name=None)
def finish_book(request, reading_id, club_id):
    # check if the user is the owner of the club
    user = request.user
    is_creator = False
    if BookClub.objects.filter(pk=club_id, user=user).exists():
        is_creator = True
    # if they are the owner, they can perform the action to finish the current book
    if request.method == "POST" and is_creator:
        reading = Reading.objects.get(pk=reading_id)
        reading.status = "D"
        reading.date_finished = date.today()
        reading.save()
        return HttpResponseRedirect(reverse("main:manage_club", args=[club_id]))


# webpage serves as discussion area for owner and members of the club to discuss a book
@login_required(redirect_field_name=None)
def discussion(request, reading_id):
    # django form for users to input their questions regarding a book
    question_form = QuestionForm()
    # django form for others user to respond to the questions
    response_form = ResponseForm()

    reading = Reading.objects.get(pk=reading_id)
    club = reading.club

    # check if the book is the current reading for that club, users can only submit questions and responds for current reading
    if reading.status == 'A':
        current_book = True
    elif reading.status == 'D':
        current_book = False

    # check if the user is the owner or member of the club
    is_joined = False
    is_creator = False
    if request.user.is_authenticated:
        user = request.user
        if JoinClub.objects.filter(user=user, club=club, status='A').exists():
            is_joined = True
        if club.user.id == user.id:
            is_creator = True

    if request.method == "POST" and request.user.is_authenticated:
        # only owner and members of the club can take part in the discussion
        if current_book and (is_joined or is_creator):
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                description = question_form.cleaned_data["description"]
                date_posted = date.today()
                Question.objects.create(
                    description=description, user=user, reading=reading, date=date_posted)
                question_form = QuestionForm()

    if Question.objects.filter(reading=reading).exists():
        question_list = Question.objects.filter(reading=reading)
    else:
        question_list = None
        response_list = None

    # hash table to contains each question and its responds
    if question_list:
        response_list = {}
        for question in question_list:
            response_list[question.id] = Response.objects.filter(
                question=question)

    return render(request, "main/discussion.html", {"club": club, "reading": reading, "current_book": current_book, "question_form": question_form, "response_form": response_form, "question_list": question_list, "response_list": response_list, "is_joined": is_joined, "is_creator": is_creator})


# functionality to responds the questions in discussion area
@login_required(redirect_field_name=None)
def response(request, question_id):
    if request.method == "POST":
        user = request.user
        question = Question.objects.get(pk=question_id)
        reading = question.reading
        club = reading.club

        # only owner or members of the clubs can respond to questions
        is_joined = False
        if JoinClub.objects.filter(user=user, club=club, status='A').exists():
            is_joined = True
        is_creator = False
        if club.user.id == user.id:
            is_creator = True

        # only current reading accept further responds
        if reading.status == 'A':
            current_book = True
        elif reading.status == 'D':
            current_book = False

        if current_book and (is_joined or is_creator):
            response_form = ResponseForm(request.POST)
            if response_form.is_valid():
                description = response_form.cleaned_data["description"]
                date_response = date.today()
                Response.objects.create(
                    description=description, user=user, question=question, date=date_response)
                return HttpResponseRedirect(reverse("main:discussion", args=[reading.id]))


# webpage for the owner of the club to finish a current reading and select the new reading for the club
@login_required(redirect_field_name=None)
def manage_club(request, club_id):
    book_club = None
    user = request.user
    # check if the user is the owner of the club
    is_creator = False
    if BookClub.objects.filter(pk=club_id, user=user).exists():
        is_creator = True
    # only the owner can perform the action to select new reading for the club
    if request.method == "POST" and 'club_id' in request.POST and is_creator:
        manage_club_form = ManageClubForm(request.POST)
        if manage_club_form.is_valid():
            club_id = manage_club_form.cleaned_data["club_id"]
            book_club = BookClub.objects.get(pk=club_id)
            cover_edition_key = manage_club_form.cleaned_data["cover_edition_key"]
            book_name = manage_club_form.cleaned_data["book_name"]
            publish_year = manage_club_form.cleaned_data["publish_year"]
            author = manage_club_form.cleaned_data["author"]
            status = 'A'
            date_finished = None
            form = None
            Reading.objects.create(club=book_club,
                                   cover_edition_key=cover_edition_key, book_name=book_name, publish_year=publish_year, author=author, status=status, date_finished=date_finished)

    ui_search_results = []

    # django form for the owner to input book name and author name to search for a book
    if request.method == "GET":
        form = SearchBookForm()

    # call API to search for a book based on the input by owner
    if request.method == "POST" and 'search_book' in request.POST:
        form = SearchBookForm(request.POST)
        api_url = "https://openlibrary.org/search.json"
        params = {
            'title': form["book_name"].value(),
            'page': 1,
            'limit': 9,
            'q': "first_publish_year:* AND cover_i:* AND author_name:*"
        }
        if form["author_name"].value():
            params['author'] = form["author_name"].value()

        try:
            api_result = make_api_call(api_url, params=params)
            if api_result:
                docs = api_result.get("docs", [])
                # Process the API response
                for item in docs:
                    book_info = {}
                    book_info["author_name"] = ", ".join(item["author_name"])
                    book_info["title"] = item["title"]
                    book_info["publish_year"] = item["first_publish_year"]
                    if "cover_i" in item:
                        book_info["cover_id"] = item["cover_i"]
                    ui_search_results.append(book_info)
        except Exception as e:
            # Handle any other unexpected exceptions
            print("Error occurred:", e)

    manage_club_form = ManageClubForm()
    if book_club is None:
        book_club = BookClub.objects.get(pk=club_id)
    # if there is current reading, the owner has the option to finish it. Otherwise, manage club form will be shown
    if Reading.objects.filter(club=book_club, status="A").exists():
        current_book = Reading.objects.get(club=book_club, status="A")
    else:
        current_book = None
    return render(request, "main/manage_club.html", {"book_club": book_club, "form": form, "ui_search_results": ui_search_results, "manage_club_form": manage_club_form, "current_book": current_book})


# webpage to show all active books that have been added
@login_required()
def shelf(request):
    user = request.user
    # filter the physical books
    if Shelf.objects.filter(user=user, format=1, status='A').exists():
        physical_list = Shelf.objects.filter(user=user, format=1, status='A')
    else:
        physical_list = None
    # filter the Apple Books
    if Shelf.objects.filter(user=user, format=2, status='A').exists():
        apple_list = Shelf.objects.filter(user=user, format=2, status='A')
    else:
        apple_list = None
    # filter the Google books
    if Shelf.objects.filter(user=user, format=3, status='A').exists():
        google_list = Shelf.objects.filter(user=user, format=3, status='A')
    else:
        google_list = None
    # filter the Kindle books
    if Shelf.objects.filter(user=user, format=4, status='A').exists():
        kindle_list = Shelf.objects.filter(user=user, format=4, status='A')
    else:
        kindle_list = None

    return render(request, "main/shelf.html", {"physical_list": physical_list, "apple_list": apple_list, "google_list": google_list, "kindle_list": kindle_list})


# functionality to delete a book from the user's shelf
@login_required(redirect_field_name=None)
def shelf_del_book(request, shelf_id):
    validated = False
    if Shelf.objects.filter(pk=shelf_id, user=request.user).exists():
        validated = True
    if request.method == "POST" and validated:
        book = Shelf.objects.get(pk=shelf_id)
        book.status = "D"
        book.save()
        return HttpResponseRedirect(reverse("main:shelf"))


# webpage to show which book clubs are created or joined by the user
@login_required()
def user_page(request):
    if BookClub.objects.filter(user=request.user, status="A").exists():
        ui_user_book_clubs = BookClub.objects.filter(
            user=request.user, status="A")
    else:
        ui_user_book_clubs = None
    if JoinClub.objects.filter(user=request.user).exists():
        joined_clubs = JoinClub.objects.filter(user=request.user, status='A')
    else:
        joined_clubs = None

    return render(request, "main/user_page.html", {"ui_user_book_clubs": ui_user_book_clubs, "joined_clubs": joined_clubs})
