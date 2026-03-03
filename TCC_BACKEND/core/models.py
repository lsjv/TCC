from django.db import models

# Create your models here.
class Escola(models.Model):
    nome = models.CharField(max_length=100)
      
    def __str__(self):
        return self.nome

class Professor(models.Model):
    nome = models.CharField(max_length=100)

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

class Turmas(models.model):
    nome = models.CharField(max_length=100)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

class Aulas(models.Model):
    nome = models.CharField(max_length=100)
    turmas = models.ForeignKey(Turmas, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    dias = models.IntegerField()
    horarios = models.IntegerField()