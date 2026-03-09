import random
from core.models import Turma, TurmaDisciplina,Slot,Aula

def gerar_horario_turma(turma_id):
    turma = Turma.objects.get(id=turma_id) #Recebe um ID de turma e busca no banco de dados o objeto Turma correspondente

    #primeiro pegar as disciplinas das turmas
    turma_disciplinas= TurmaDisciplina.objects.filter(turma=turma)
    
    #criar lista de aulas
    aulas_nescessarias = []

    for td in turma_disciplinas:
        for _ in range(td.aulas_semanais):
            aulas_nescessarias.append(td)
    # Para cada disciplina, adiciona à lista uma entrada para cada aula semanal necessária

    #Exemplo: se uma disciplina tem 3 aulas por semana, ela aparecerá 3 vezes na lista

    #Resultado: uma lista com todas as aulas que precisam ser alocadas na semana'''

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
        #Para cada slot de horário disponível, pega uma aula da lista (usando pop() que remove e retorna o último item)
        #verificar conflit?

        conflito = Aula.objects.filter(
              turma_disciplina__professor=td.professor,
              slot=slot
              ).exists()
        #Verifica se o professor já tem alguma aula alocada neste mesmo horário

        #Usa __ para acessar o professor através da relação turma_disciplina
       
                 
        if conflito:
            aulas_nescessarias.insert(0,td)
            continue
        # Se houver conflito, devolve a aula para o início da lista (insert(0, ...))

        #continue pula para o próximo slot sem criar a aula
        Aula.objects.create(
              turma_disciplina=td,
              slot=slot
            )
        aulas_criadas += 
        #se nao tiver conflitos  cria a aula no banco de dados e incrementa o valor ao log

    print(f"{aulas_criadas}aulas criadas para{turma.nome}")