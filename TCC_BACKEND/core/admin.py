
# core/admin.py
from django.contrib import admin
from .models import Escola

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']  