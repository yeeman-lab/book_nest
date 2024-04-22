from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_to_shelf", views.add_to_shelf, name="add_to_shelf"),
    path("submit_shelf", views.submit_shelf, name="submit_shelf"),
    path("club_page/<int:club_id>", views.club_page, name="club_page"),
    path("create_club", views.create_club, name="create_club"),
    path("discussion/<int:reading_id>",
         views.discussion, name="discussion"),
    path("manage_club/<int:club_id>", views.manage_club, name="manage_club"),
    path("shelf", views.shelf, name="shelf"),
    path("user_page", views.user_page, name="user_page"),
    path("delete_club/<int:club_id>", views.delete_club, name="delete_club"),
    path("finish_book/<int:reading_id>/<int:club_id>",
         views.finish_book, name="finish_book"),
    path("join_club/<int:club_id>", views.join_club, name="join_club"),
    path("leave_club/<int:club_id>", views.leave_club, name="leave_club"),
    path("response/<int:question_id>", views.response, name="response"),
    path("shelf_del_book/<int:shelf_id>",
         views.shelf_del_book, name="shelf_del_book"),
]
