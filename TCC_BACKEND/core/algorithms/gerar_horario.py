import random
from core.models import Turma, TurmaDisciplina,Slot,Aula

def gerar_horario_turma(turma_id):
    turma = Turma.objects.get(id=turma_id)

    #primeiro pegar as disciplinas das turmas
    turma_disciplinas= TurmaDisciplina.objects.filter(turma=turma)
    
    #criar lista de aulas
    aulas_nescessarias = []

    for td in turma_disciplinas:
        for _ in range(td.aulas_semanais):
            aulas_nescessarias.append(td)


    #embaralhar ordem
    random.shuffle(aulas_nescessarias)

    #agora pegar os slots disponiveis pra gerar o horario


    slots = list(Slot.objects.all())
    random.shuffle(slots)
    
    aulas_criadas = 0

    for slot in slots:
        
        if not aulas_nescessarias:
            break
        
        td = aulas_nescessarias.pop()

        #verificar conflit?

        conflito = Aula.objects.filter(
              turma_disciplina__professor=td.professor,
              slot=slot
              ).exists()

        if conflito:
            aulas_nescessarias.insert(0,td)
            continue
        Aula.objects.create(
              turma_disciplina=td,
              slot=slot
            )
        aulas_criadas += 1

    print(f"{aulas_criadas}aulas criadas para{turma.nome}")