from django.db import models

# Create your models here.

class Escola(models.Model):
    """
    Modelo que representa uma unidade escolar (colégio).
    É a entidade principal do sistema, pois uma escola pode ter várias turmas
    e vários horários (slots) disponíveis.
    """
    nome = models.CharField(max_length=100)  # Nome da escola (ex: "Colégio São Paulo")
      
    def __str__(self):
        """Retorna o nome da escola como representação em string"""
        return self.nome


class Professor(models.Model):
    """
    Modelo que representa um professor.
    Cada professor pertence a uma escola e pode lecionar várias disciplinas para diferentes turmas.
    """
    escola = models.ForeignKey(
        'Escola',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='professores'
    )
    nome = models.CharField(max_length=100)
    carga_maxima_semana = models.IntegerField(default=20)
    max_aulas_consecutivas = models.IntegerField(default=4)  # 0 = sem restrição

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    """
    Modelo que representa uma disciplina/matéria escolar.
    Cada disciplina pertence a uma escola específica.
    """
    escola = models.ForeignKey(
        'Escola',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='disciplinas'
    )
    nome      = models.CharField(max_length=100)
    cor_bg    = models.CharField(max_length=7, default="#F1EFE8")
    cor_borda = models.CharField(max_length=7, default="#5F5E5A")
    cor_texto = models.CharField(max_length=7, default="#444441")

    def __str__(self):
        return self.nome


class Turma(models.Model):
    """
    Modelo que representa uma turma/classe de alunos.
    Cada turma pertence a uma escola específica e tem um turno definido.
    """
    nome = models.CharField(max_length=100)  # Nome/identificação da turma (ex: "3º Ano A", "5ª Série B")
    escola = models.ForeignKey(
        Escola, 
        on_delete=models.CASCADE  # Se a escola for deletada, todas as suas turmas também serão deletadas
    )
    turno = models.CharField(max_length=20)  # Turno de funcionamento: manhã, tarde ou noite

    def __str__(self):
        """Retorna o nome da turma como representação em string"""
        return self.nome


class TurmaDisciplina(models.Model):
    """
    Modelo de relacionamento entre Turma, Disciplina e Professor.
    É uma tabela intermediária que define:
    - Qual disciplina uma turma estuda
    - Qual professor leciona essa disciplina para essa turma
    - Quantas aulas semanais essa combinação possui
    
    Este é o modelo mais importante para a geração de horários!
    """
    turma = models.ForeignKey(
        Turma, 
        on_delete=models.CASCADE  # Se a turma for deletada, este relacionamento também é deletado
    )
    disciplina = models.ForeignKey(
        Disciplina, 
        on_delete=models.CASCADE  # Se a disciplina for deletada, este relacionamento também é deletado
    )
    professor = models.ForeignKey(
        Professor, 
        on_delete=models.CASCADE  # Se o professor for deletado, este relacionamento também é deletado
    )
    aulas_semanais = models.IntegerField()  # Quantidade de aulas desta combinação por semana (ex: 4 aulas de Matemática)

    def __str__(self):
        """Retorna uma string identificando a combinação turma-disciplina"""
        return f"{self.turma} - {self.disciplina}"
        

class Slot(models.Model):
    """
    Modelo que representa um horário disponível na grade da escola.
    Cada slot é um espaço de tempo que pode ser preenchido com uma aula.
    Exemplo: Segunda-feira, 1ª aula do turno da manhã.
    """
    escola = models.ForeignKey(
        Escola, 
        on_delete=models.CASCADE  # Se a escola for deletada, todos os seus slots também são deletados
    )
    dia_semana = models.IntegerField()  # Dia da semana: 0=segunda, 1=terça, 2=quarta, 3=quinta, 4=sexta
    numero_aula = models.IntegerField()  # Posição da aula no dia: 1ª aula, 2ª aula, 3ª aula, etc.
    turno = models.CharField(max_length=20)  # Turno deste slot (manhã/tarde/noite) - ajuda na filtragem

    def __str__(self):
        """Retorna uma string identificando o slot de horário"""
        return f"Dia {self.dia_semana} - Aula {self.numero_aula}"
    

class DisponibilidadeProfessor(models.Model):
    """
    Modelo que controla a disponibilidade dos professores.
    Define em quais dias e horários específicos cada professor pode dar aula.
    Se não houver registro para um professor, assume-se que ele está disponível em todos os horários.
    """
    professor = models.ForeignKey(
        Professor, 
        on_delete=models.CASCADE  # Se o professor for deletado, sua disponibilidade também é deletada
    )
    dia_semana = models.IntegerField()  # Dia da semana disponível (0-4)
    numero_aula = models.IntegerField()  # Número da aula disponível neste dia
    
    class Meta:
        # Garante que não haja registros duplicados de disponibilidade
        unique_together = ('professor', 'dia_semana', 'numero_aula')
    

class Aula(models.Model):
    """
    Modelo que representa uma aula efetivamente alocada na grade horária.
    Conecta um slot de horário com uma combinação turma-disciplina-professor.
    Quando o algoritmo de geração de horários executa, ele cria instâncias desta classe.
    """
    slot = models.ForeignKey(
        Slot, 
        on_delete=models.CASCADE  # Se o slot for deletado, a aula também é deletada
    )
    turma_disciplina = models.ForeignKey(
        TurmaDisciplina, 
        on_delete=models.CASCADE  # Se a turma-disciplina for deletada, suas aulas também são deletadas
    )

    class Meta:
        # Garante que não haja duas aulas no mesmo slot com a mesma turma-disciplina
        # Isso evita conflitos como a mesma turma tendo duas aulas no mesmo horário
        unique_together = ('slot', 'turma_disciplina')
    
    def __str__(self):
        """Retorna uma string identificando a aula alocada"""
        return f"{self.turma_disciplina} - {self.slot}"