from django.db import models

# Create your models here.
class Escola(models.Model):
    nome = models.CharField(max_length=100)
      
    def __str__(self):
        return self.nome

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    carga_maxima_semana = models.IntegerField(default=20)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome0)

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    turno = models.CharField(max_length=20)  # manhã, tarde, noite

    def __str__(self):
        return self.nome

class Aula(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    turma_disciplina = models.ForeignKey(TurmaDisciplina, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('slot', 'turma_disciplina')

class TurmaDisciplina(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    aulas_semanais = models.IntegerField()

    def __str__(self):
        return f"{self.turma} - {self.disciplina}"
    
class Slot(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    dia_semana = models.IntegerField()  # 0-4
    numero_aula = models.IntegerField() # 1,2,3,4...
    turno = models.CharField(max_length=20)

    def __str__(self):
        return f"Dia {self.dia_semana} - Aula {self.numero_aula}"
    
class DisponibilidadeProfessor(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    dia_semana = models.IntegerField()
    numero_aula = models.IntegerField()