from django.urls import path
from .views import grade_turma

urlpatterns = [
    path("grade/<int:turma_id>/", grade_turma, name="grade_turma"),
]