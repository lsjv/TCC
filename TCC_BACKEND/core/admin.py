from django.contrib import admin
from .models import (
    Escola,
    Professor,
    Disciplina,
    Turma,
    TurmaDisciplina,
    Slot,
    DisponibilidadeProfessor,
    Aula
)

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'carga_maxima_semana']
    search_fields = ['nome']


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'escola', 'turno']
    list_filter = ['escola', 'turno']
    search_fields = ['nome']


@admin.register(TurmaDisciplina)
class TurmaDisciplinaAdmin(admin.ModelAdmin):
    list_display = ['id', 'turma', 'disciplina', 'professor', 'aulas_semanais']
    list_filter = ['turma', 'professor']
    search_fields = ['turma__nome', 'disciplina__nome']


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'escola', 'dia_semana', 'numero_aula', 'turno']
    list_filter = ['escola', 'turno']


@admin.register(DisponibilidadeProfessor)
class DisponibilidadeProfessorAdmin(admin.ModelAdmin):
    list_display = ['id', 'professor', 'dia_semana', 'numero_aula']
    list_filter = ['professor']


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['id', 'slot', 'turma_disciplina']