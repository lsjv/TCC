from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Escola
    path('escola/nova/',                       views.escola_create, name='escola_create'),
    path('escola/<int:escola_id>/',            views.escola_detail, name='escola_detail'),
    path('escola/<int:escola_id>/editar/',     views.escola_edit,   name='escola_edit'),
    path('escola/<int:escola_id>/excluir/',    views.escola_delete, name='escola_delete'),
    path('escola/<int:escola_id>/gerar/',      views.gerar_horario_view, name='gerar_horario'),

    # Slots
    path('escola/<int:escola_id>/slots/',          views.slot_list,         name='slot_list'),
    path('escola/<int:escola_id>/slots/excluir/',  views.slot_delete_turno, name='slot_delete_turno'),

    # Professor — escopado por escola
    path('escola/<int:escola_id>/professor/',          views.professor_list,   name='professor_list'),
    path('escola/<int:escola_id>/professor/novo/',     views.professor_create, name='professor_create'),
    path('professor/<int:professor_id>/editar/',       views.professor_edit,   name='professor_edit'),
    path('professor/<int:professor_id>/excluir/',      views.professor_delete, name='professor_delete'),
    path('professor/<int:professor_id>/disponibilidade/', views.professor_disponibilidade, name='professor_disponibilidade'),

    # Disciplina — escopada por escola
    path('escola/<int:escola_id>/disciplina/',         views.disciplina_list,   name='disciplina_list'),
    path('escola/<int:escola_id>/disciplina/nova/',    views.disciplina_create, name='disciplina_create'),
    path('disciplina/<int:disciplina_id>/editar/',     views.disciplina_edit,   name='disciplina_edit'),
    path('disciplina/<int:disciplina_id>/excluir/',    views.disciplina_delete, name='disciplina_delete'),

    # Turma
    path('escola/<int:escola_id>/turma/nova/',  views.turma_create, name='turma_create'),
    path('turma/<int:turma_id>/editar/',        views.turma_edit,   name='turma_edit'),
    path('turma/<int:turma_id>/excluir/',       views.turma_delete, name='turma_delete'),

    # TurmaDisciplina
    path('turma/<int:turma_id>/disciplinas/',           views.turma_disciplina_list,   name='turma_disciplina_list'),
    path('turma/<int:turma_id>/disciplina/nova/',       views.turma_disciplina_create, name='turma_disciplina_create'),
    path('turma-disciplina/<int:td_id>/editar/',        views.turma_disciplina_edit,   name='turma_disciplina_edit'),
    path('turma-disciplina/<int:td_id>/excluir/',       views.turma_disciplina_delete, name='turma_disciplina_delete'),

    # Grade
    path('grade/<int:turma_id>/',     views.grade_turma, name='grade_turma'),
    path('grade/<int:turma_id>/pdf/', views.grade_pdf,   name='grade_pdf'),
]
