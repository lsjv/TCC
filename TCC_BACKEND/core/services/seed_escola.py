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
    professores = [
        "Ana",
        "Carlos",
        "Mariana",
        "Pedro",
        "Juliana",
        "Roberto",
        "Fernanda",
        "Lucas"
    ]

    for nome in professores:
        Professor.objects.get_or_create(nome=nome)


    print("Criando disciplinas...")
    disciplinas = [
        "Matemática",
        "Português",
        "História",
        "Geografia",
        "Ciências",
        "Inglês",
        "Educação Física",
        "Artes"
    ]

    for nome in disciplinas:
        Disciplina.objects.get_or_create(nome=nome)


    print("Criando turmas...")
    turmas = [
        ("6A", "manha"),
        ("6B", "manha"),
        ("7A", "manha"),
        ("7B", "manha"),
        ("8A", "manha"),
        ("9A", "manha"),
    ]

    for nome, turno in turmas:
        Turma.objects.get_or_create(
            nome=nome,
            escola=escola,
            turno=turno
        )


    print("Criando slots...")
    for dia in range(5):  # segunda a sexta
        for aula in range(1, 6):  # 5 aulas por dia

            Slot.objects.get_or_create(
                escola=escola,
                dia_semana=dia,
                numero_aula=aula,
                turno="manha"
            )


    print("Criando relações turma-disciplina...")

    aulas_semanais = {
        "Matemática": 5,
        "Português": 5,
        "História": 3,
        "Geografia": 3,
        "Ciências": 3,
        "Inglês": 2,
        "Educação Física": 2,
        "Artes": 2
    }

    turmas = Turma.objects.filter(escola=escola)
    disciplinas = Disciplina.objects.all()
    professores = list(Professor.objects.all())

    p_index = 0

    for turma in turmas:

        for disciplina in disciplinas:

            professor = professores[p_index % len(professores)]
            p_index += 1

            TurmaDisciplina.objects.get_or_create(
                turma=turma,
                disciplina=disciplina,
                professor=professor,
                aulas_semanais=aulas_semanais[disciplina.nome]
            )

    print("Seed finalizado!")