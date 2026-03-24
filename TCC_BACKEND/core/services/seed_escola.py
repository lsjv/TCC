from core.models import (
    Escola,
    Professor,
    Disciplina,
    Turma,
    TurmaDisciplina,
    Slot
)


def seed():

    print("Criando escola...")
    escola, _ = Escola.objects.get_or_create(nome="Escola Teste")

    print("Criando professores...")
    carga_maxima_por_professor = {
        "Ana":      19,
        "Pedro":    19,
        "Carlos":   19,
        "Fernanda": 23,
        "Mariana":  18,
        "Juliana":  18,
        "Roberto":  16,
        "Lucas":    18,
    }

    for nome, carga in carga_maxima_por_professor.items():
        Professor.objects.get_or_create(
            nome=nome,
            defaults={'carga_maxima_semana': carga}
        )

    print("Criando disciplinas...")
    disciplinas = [
        "Matemática",
        "Língua Portuguesa",
        "História",
        "Geografia",
        "Ciências",
        "Língua Inglesa",
        "Educação Física",
        "Artes",
    ]

    for nome in disciplinas:
        Disciplina.objects.get_or_create(nome=nome)

    print("Criando turmas...")
    turmas_data = [
        ("6A", "manha"),
        ("6B", "manha"),
        ("7A", "manha"),
        ("7B", "manha"),
        ("8A", "manha"),
        ("9A", "manha"),
    ]

    for nome, turno in turmas_data:
        Turma.objects.get_or_create(
            nome=nome,
            escola=escola,
            defaults={'turno': turno}
        )

    print("Criando slots...")
    for dia in range(5):
        for aula in range(1, 6):
            Slot.objects.get_or_create(
                escola=escola,
                dia_semana=dia,
                numero_aula=aula,
                turno="manha"
            )

    print("Criando relações turma-disciplina...")

    aulas_semanais = {
        "Matemática":        5,
        "Língua Portuguesa": 5,
        "História":          3,
        "Geografia":         3,
        "Ciências":          3,
        "Língua Inglesa":    2,
        "Educação Física":   2,
        "Artes":             2,
    }

    professor_por_turma_disciplina = {
        # Matemática
        ("6A", "Matemática"): "Ana",
        ("6B", "Matemática"): "Ana",
        ("7A", "Matemática"): "Ana",
        ("7B", "Matemática"): "Pedro",
        ("8A", "Matemática"): "Pedro",
        ("9A", "Matemática"): "Pedro",

        # Língua Portuguesa
        ("6A", "Língua Portuguesa"): "Carlos",
        ("6B", "Língua Portuguesa"): "Carlos",
        ("7A", "Língua Portuguesa"): "Carlos",
        ("7B", "Língua Portuguesa"): "Fernanda",
        ("8A", "Língua Portuguesa"): "Fernanda",
        ("9A", "Língua Portuguesa"): "Fernanda",

        # História
        ("6A", "História"): "Mariana",
        ("6B", "História"): "Mariana",
        ("7A", "História"): "Mariana",
        ("7B", "História"): "Mariana",
        ("8A", "História"): "Mariana",
        ("9A", "História"): "Mariana",

        # Geografia
        ("6A", "Geografia"): "Juliana",
        ("6B", "Geografia"): "Juliana",
        ("7A", "Geografia"): "Juliana",
        ("7B", "Geografia"): "Juliana",
        ("8A", "Geografia"): "Juliana",
        ("9A", "Geografia"): "Juliana",

        # Ciências — Roberto: 6A/6B/7A/7B | Lucas: 8A/9A
        ("6A", "Ciências"): "Roberto",
        ("6B", "Ciências"): "Roberto",
        ("7A", "Ciências"): "Roberto",
        ("7B", "Ciências"): "Roberto",
        ("8A", "Ciências"): "Lucas",
        ("9A", "Ciências"): "Lucas",

        # Língua Inglesa
        ("6A", "Língua Inglesa"): "Lucas",
        ("6B", "Língua Inglesa"): "Lucas",
        ("7A", "Língua Inglesa"): "Lucas",
        ("7B", "Língua Inglesa"): "Lucas",
        ("8A", "Língua Inglesa"): "Lucas",
        ("9A", "Língua Inglesa"): "Lucas",

        # Educação Física
        ("6A", "Educação Física"): "Ana",
        ("6B", "Educação Física"): "Ana",
        ("7A", "Educação Física"): "Pedro",
        ("7B", "Educação Física"): "Pedro",
        ("8A", "Educação Física"): "Carlos",
        ("9A", "Educação Física"): "Carlos",

        # Artes — Fernanda: 6A/6B/7A/7B | Roberto: 8A/9A
        ("6A", "Artes"): "Fernanda",
        ("6B", "Artes"): "Fernanda",
        ("7A", "Artes"): "Fernanda",
        ("7B", "Artes"): "Fernanda",
        ("8A", "Artes"): "Roberto",
        ("9A", "Artes"): "Roberto",
    }

    turmas = Turma.objects.filter(escola=escola)
    disciplinas_qs = Disciplina.objects.all()

    for turma in turmas:
        for disciplina in disciplinas_qs:
            nome_prof = professor_por_turma_disciplina[(turma.nome, disciplina.nome)]
            professor = Professor.objects.get(nome=nome_prof)

            TurmaDisciplina.objects.get_or_create(
                turma=turma,
                disciplina=disciplina,
                defaults={
                    'professor': professor,
                    'aulas_semanais': aulas_semanais[disciplina.nome]
                }
            )

    print("Seed finalizado!")