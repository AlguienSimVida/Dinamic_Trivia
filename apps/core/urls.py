from django.urls import path
from .views import generate_trivia, verify_answers

urlpatterns = [
    path("generate_trivia/", generate_trivia, name="generate_trivia"),
    path("verify_answers/", verify_answers, name="verify_answers")
]