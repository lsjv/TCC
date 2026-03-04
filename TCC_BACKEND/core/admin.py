
# core/admin.py
from django.contrib import admin
from .models import (
    Escola,
    Professor,
    Disciplina,
    Turmas,
    Aulas
)

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']  
    search_fields = [ 'nome']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['id',  'nome']
    search_fields = [ 'nome']

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['id' , 'nome']
    search_fields = [ 'nome']
