from core.models import (
    Escola,
    Professor,
    Disciplina,
    Turma,
    TurmaDisciplina,
    Slot
)

# ============================================
# FUNÇÕES DE CRIAÇÃO/POPULAÇÃO DO BANCO DE DADOS
# ============================================

def criar_escola():
    """
    Cria ou obtém a escola principal do sistema.
    
    O método get_or_create retorna uma tupla (objeto, booleano_criado)
    Usamos _ para ignorar o booleano, pois só precisamos do objeto escola.
    
    Returns:
        Escola: Objeto da escola criada ou existente
    """
    escola, _ = Escola.objects.get_or_create(nome="Escola Modelo")
    return escola


def criar_professores():
    """
    Cria uma lista pré-definida de professores no banco de dados.
    
    A lista contém 17 professores com nomes variados para distribuir
    pelas diferentes disciplinas e turmas.
    
    O método get_or_create evita duplicatas caso a função seja executada
    múltiplas vezes.
    """
    nomes = [
        "Carlos Alberto", "Ana Beatriz", "Carla Souza", "Joaquim Antonio",
        "Mariana Costa", "Roberto Mendes", "Pedro Henrique",
        "Ricardo Lopes", "Fernanda Costa", "Juliana Martins",
        "André Santos", "Paulo Cesar", "Teresa Alves",
        "Simone Rocha", "Patricia Oliveira", "Lucia Fernandes",
        "Marcos Paulo"
    ]

    for nome in nomes:
        Professor.objects.get_or_create(nome=nome)


def criar_disciplinas():
    """
    Cria uma lista completa de disciplinas escolares.
    
    Inclui disciplinas do ensino fundamental e médio:
    - Fundamental: Matemática, Português, Ciências, etc.
    - Médio: Biologia, Física, Química, Filosofia, etc.
    """
    disciplinas = [
        "Matemática", "Português", "Ciências", "História", "Geografia",
        "Inglês", "Artes", "Educação Física", "Ensino Religioso",
        "Literatura", "Biologia", "Física", "Química",
        "Filosofia", "Sociologia"
    ]

    for nome in disciplinas:
        Disciplina.objects.get_or_create(nome=nome)


def criar_turmas(escola):
    """
    Cria turmas para ensino fundamental (tarde) e ensino médio (manhã).
    
    Args:
        escola: Objeto Escola ao qual as turmas pertencem
    
    Turmas criadas:
        - Fundamental (tarde): 6A, 6B, 7A, 7B, 8A, 9A
        - Médio (manhã): 1A, 1B, 2A, 2B, 3A, 3B
    """
    turmas_fundamental = ["6A", "6B", "7A", "7B", "8A", "9A"]
    turmas_medio = ["1A", "1B", "2A", "2B", "3A", "3B"]

    # Cria turmas do fundamental com turno = "tarde"
    for nome in turmas_fundamental:
        Turma.objects.get_or_create(
            nome=nome,
            escola=escola,
            turno="tarde"
        )

    # Cria turmas do médio com turno = "manha"
    for nome in turmas_medio:
        Turma.objects.get_or_create(
            nome=nome,
            escola=escola,
            turno="manha"
        )


def criar_slots(escola):
    """
    Cria todos os slots de horário disponíveis na escola.
    
    Args:
        escola: Objeto Escola para o qual os slots serão criados
    
    Estrutura criada:
        - 2 turnos (manhã e tarde)
        - 5 dias por semana (segunda a sexta)
        - 5 aulas por dia
        Total: 2 × 5 × 5 = 50 slots
    
    Cada slot representa um horário único: (turno, dia, número_aula)
    Exemplo: (manhã, segunda, 1ª aula) é um slot diferente de (tarde, segunda, 1ª aula)
    """
    dias = range(5)      # 0=segunda, 1=terça, 2=quarta, 3=quinta, 4=sexta
    aulas = range(1, 6)  # números das aulas: 1, 2, 3, 4, 5

    # Cria slots para cada turno
    for turno in ["manha", "tarde"]:
        # Para cada dia da semana
        for dia in dias:
            # Para cada número de aula
            for numero in aulas:
                Slot.objects.get_or_create(
                    escola=escola,
                    dia_semana=dia,
                    numero_aula=numero,
                    turno=turno
                )


def criar_relacoes():
    """
    Cria as relações TurmaDisciplina (que disciplina cada turma estuda,
    com qual professor e quantas aulas por semana).
    
    Cada tupla em 'dados' representa:
        (nome_da_turma, nome_da_disciplina, nome_do_professor, aulas_semanais)
    
    OBSERVAÇÃO: Este conjunto de dados está INCOMPLETO! Muitas turmas e disciplinas
    não foram relacionadas. Isso provavelmente é intencional para testes ou
    para ser expandido posteriormente.
    """
    dados = [
        # ===== TURMAS 6º ANO (FUNDAMENTAL) =====
        # Turma 6A - bastante completa
        ("6A", "Matemática", "Carlos Alberto", 5),
        ("6A", "Português", "Ana Beatriz", 5),
        ("6A", "Ciências", "Mariana Costa", 4),
        ("6A", "História", "Roberto Mendes", 3),
        ("6A", "Geografia", "Roberto Mendes", 3),  # Mesmo professor para História e Geografia
        ("6A", "Inglês", "Patricia Oliveira", 2),
        ("6A", "Artes", "Lucia Fernandes", 2),
        ("6A", "Educação Física", "Marcos Paulo", 2),
        ("6A", "Ensino Religioso", "Lucia Fernandes", 1),  # Mesmo professor para Artes e Ensino Religioso

        # Turma 6B - incompleta (faltam várias disciplinas)
        ("6B", "Matemática", "Carlos Alberto", 5),
        ("6B", "Português", "Ana Beatriz", 5),
        ("6B", "Ciências", "Mariana Costa", 4),
        ("6B", "História", "Roberto Mendes", 3),
        ("6B", "Geografia", "Roberto Mendes", 3),
        # Faltam: Inglês, Artes, Educação Física, Ensino Religioso

        # ===== TURMAS 7º ANO (FUNDAMENTAL) =====
        # Turma 7A - muito incompleta
        ("7A", "Matemática", "Carla Souza", 5),      # Professora diferente do 6º ano
        ("7A", "Português", "Joaquim Antonio", 5),   # Professor diferente do 6º ano
        ("7A", "Ciências", "Mariana Costa", 4),      # Mesma professora de Ciências
        # Faltam: História, Geografia, Inglês, Artes, Educação Física, Ensino Religioso

        # ===== TURMAS 1º ANO (MÉDIO) =====
        # Turma 1A - foco em disciplinas do médio
        ("1A", "Matemática", "Ricardo Lopes", 3),     # Menos aulas (3 vs 5 no fundamental)
        ("1A", "Português", "Fernanda Costa", 3),
        ("1A", "Literatura", "Fernanda Costa", 2),    # Mesma professora para Português e Literatura
        ("1A", "Biologia", "Juliana Martins", 2),
        ("1A", "Física", "André Santos", 2),
        # Faltam: Química, História, Geografia, Inglês, Artes, Educação Física, Filosofia, Sociologia
    ]

    # Itera sobre os dados e cria cada relação TurmaDisciplina
    for turma_nome, disc_nome, prof_nome, aulas in dados:
        # Busca os objetos relacionados no banco de dados
        turma = Turma.objects.get(nome=turma_nome)
        disciplina = Disciplina.objects.get(nome=disc_nome)
        professor = Professor.objects.get(nome=prof_nome)

        # Cria a relação (ou obtém se já existir)
        # O parâmetro 'defaults' é usado para definir campos adicionais
        # quando o objeto é criado (não quando já existe)
        TurmaDisciplina.objects.get_or_create(
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            defaults={"aulas_semanais": aulas}
        )


def seed():
    """
    Função principal que orquestra toda a população do banco de dados.
    
    Ordem de execução é importante devido às dependências entre os modelos:
    1. Escola (independente)
    2. Professores (independente)
    3. Disciplinas (independente)
    4. Turmas (depende de Escola)
    5. Slots (depende de Escola)
    6. Relações TurmaDisciplina (depende de Turma, Disciplina e Professor)
    
    Esta função é tipicamente chamada por um comando personalizado do Django
    ou diretamente no shell para popular o banco com dados iniciais.
    """
    escola = criar_escola()      # Passo 1: Cria a escola

    criar_professores()          # Passo 2: Cria os professores
    criar_disciplinas()          # Passo 3: Cria as disciplinas
    criar_turmas(escola)         # Passo 4: Cria as turmas (precisa da escola)
    criar_slots(escola)          # Passo 5: Cria os slots (precisa da escola)
    criar_relacoes()             # Passo 6: Cria as relações (precisa de turmas, disciplinas e professores)

    print("Banco populado com sucesso.")  # Mensagem de confirmação


# ============================================
# PONTO DE ENTRADA DO SCRIPT
# ============================================
# Se este arquivo for executado diretamente (python seed.py),
# a função seed() será chamada automaticamente.
if __name__ == "__main__":
    seed()