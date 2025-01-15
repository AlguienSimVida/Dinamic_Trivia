from django.urls import path
from .views import generate_trivia, show_question, next_question, show_results

urlpatterns = [
    path("generate_trivia/", generate_trivia, name="generate_trivia"),
    path("pregunta/", show_question, name="show_question"),
    path("siguiente/", next_question, name="next_question"),
    path("resultados/", show_results, name="show_results"),
]
