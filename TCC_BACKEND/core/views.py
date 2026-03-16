from django.shortcuts import render
from core.models import Turma, Aula

def grade_turma(request, turma_id):
    """
    View responsável por gerar e exibir a grade de horários de uma turma específica.
    Recebe uma requisição HTTP e o ID da turma, retorna uma página HTML com a grade.
    """
    
    # Busca a turma no banco de dados usando o ID fornecido na URL
    # Exemplo: /grade/1/ vai buscar a turma com id=1
    turma = Turma.objects.get(id=turma_id)

    # Cria uma matriz (lista de listas) 5x5 para representar a grade horária
    # Estrutura: grade[numero_aula][dia_semana]
    # [linha][coluna] - 5 linhas (aulas do dia) e 5 colunas (dias da semana)
    # grade = [
    #   [None, None, None, None, None],  # 1ª aula (índice 0)
    #   [None, None, None, None, None],  # 2ª aula (índice 1)
    #   [None, None, None, None, None],  # 3ª aula (índice 2)
    #   [None, None, None, None, None],  # 4ª aula (índice 3)
    #   [None, None, None, None, None]   # 5ª aula (índice 4)
    # ]
    # Cada posição da matriz começa como None (vazia)
    grade = [[None for _ in range(5)] for _ in range(5)]

    # Busca todas as aulas da turma no banco de dados
    # O filtro 'turma_disciplina__turma' usa o __ (duplo underscore) para
    # "atravessar" o relacionamento: Aula -> TurmaDisciplina -> Turma
    aulas = Aula.objects.filter(
        turma_disciplina__turma=turma  # Filtra aulas desta turma específica
    ).select_related(
        # select_related faz um JOIN no banco de dados para buscar dados relacionados
        # em uma única consulta, evitando consultas extras (problema N+1)
        "turma_disciplina__disciplina",  # Busca também os dados da disciplina
        "slot"                            # Busca também os dados do slot
    )

    # Preenche a matriz grade com as aulas encontradas
    for aula in aulas:
        # Pega o dia da semana do slot (0=segunda, 1=terça, ..., 4=sexta)
        dia = aula.slot.dia_semana  # Este valor já é um índice de 0 a 4
        
        # Pega o número da aula e ajusta para índice de lista (0-based)
        # numero_aula no banco é 1-based (1, 2, 3, 4, 5)
        # Nosso array é 0-based (0, 1, 2, 3, 4)
        # Então subtraímos 1 para converter
        numero = aula.slot.numero_aula - 1
        
        # Coloca o objeto aula na posição correta da matriz
        # grade[linha][coluna] = grade[numero_aula][dia_semana]
        grade[numero][dia] = aula

    # Prepara o contexto para enviar ao template
    context = {
        "turma": turma,           # Objeto turma para exibir informações
        "grade": grade,           # Matriz 5x5 com as aulas preenchidas
        "dias": ["SEG", "TER", "QUA", "QUI", "SEX"]  # Rótulos dos dias para o template
        # Os números das aulas (1ª, 2ª, etc.) serão tratados diretamente no template
        # usando o índice da linha (loop.index)
    }

    # Renderiza o template 'core/grade.html' passando o contexto
    # O template vai percorrer a matriz e exibir as aulas em formato de tabela
    return render(request, "core/grade.html", context)