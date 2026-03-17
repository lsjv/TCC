from core.models import (
    Turma,
    Slot,
    Aula,
    TurmaDisciplina
)

import random


def gerar_horario_escola(escola_id):
    """
    Função que gera horários para TODAS as turmas de uma escola.
    
    ATENÇÃO: Esta função TEM PROBLEMAS! Vou destacá-los nos comentários.
    """

    print("Gerando horários...")

    # ===== PROBLEMA 1: LIMPEZA TOTAL =====
    # limpa aulas antigas
    Aula.objects.all().delete()
    """
    PROBLEMA: Isso deleta TODAS as aulas do sistema, não apenas da escola!
    Se houver múltiplas escolas no banco, isso apaga os horários de todas elas.
    
    SOLUÇÃO: Deveria filtrar por escola:
    Aula.objects.filter(turma_disciplina__turma__escola_id=escola_id).delete()
    """

    turmas = Turma.objects.filter(escola_id=escola_id)

    slots = list(
        Slot.objects.filter(escola_id=escola_id)
    )

    # embaralha slots para evitar padrões ruins
    random.shuffle(slots)

    total_criadas = 0

    # ===== PROBLEMA 2: ORDEM DAS TURMAS =====
    for turma in turmas:
        """
        PROBLEMA: As turmas são processadas em ordem, e as primeiras têm
        "vantagem" na escolha dos slots. As últimas turmas podem ficar sem opções.
        
        SOLUÇÃO: Embaralhar as turmas também:
        turmas = list(turmas)
        random.shuffle(turmas)
        """

        print(f"Gerando para turma {turma.nome}")

        relacoes = TurmaDisciplina.objects.filter(
            turma=turma
        ).select_related(
            "disciplina",
            "professor"
        )

        # ===== PROBLEMA 3: ORDEM DAS DISCIPLINAS =====
        for rel in relacoes:
            """
            PROBLEMA: Mesmo problema - primeiras disciplinas têm vantagem.
            
            SOLUÇÃO: Embaralhar as relações também.
            """

            aulas_restantes = rel.aulas_semanais

            while aulas_restantes > 0:

                colocado = False

                # ===== PROBLEMA 4: SEMPRE PERCORRE DO INÍCIO =====
                for slot in slots:
                    """
                    PROBLEMA: Cada nova aula começa a busca do PRIMEIRO slot.
                    Isso causa:
                    1. Ineficiência - repete verificações
                    2. Acúmulo nos primeiros horários
                    
                    SOLUÇÃO: Começar de onde parou ou usar um índice.
                    """

                    # slot precisa ser do mesmo turno
                    if slot.turno != turma.turno:
                        continue

                    # ===== PROBLEMA 5: CONSULTAS EXCESSIVAS =====
                    # turma já tem aula nesse horário?
                    conflito_turma = Aula.objects.filter(
                        slot=slot,
                        turma_disciplina__turma=turma
                    ).exists()
                    """
                    PROBLEMA: Isso faz UMA CONSULTA POR SLOT!
                    Para 50 slots × várias disciplinas × várias turmas = centenas de consultas!
                    
                    SOLUÇÃO: Carregar aulas existentes em memória e verificar localmente.
                    """

                    if conflito_turma:
                        continue

                    # professor já está ocupado?
                    conflito_prof = Aula.objects.filter(
                        slot=slot,
                        turma_disciplina__professor=rel.professor
                    ).exists()
                    """
                    PROBLEMA: Outra consulta por slot! O número explode.
                    """

                    if conflito_prof:
                        continue

                    # criar aula
                    Aula.objects.create(
                        slot=slot,
                        turma_disciplina=rel
                    )

                    aulas_restantes -= 1
                    total_criadas += 1
                    colocado = True
                    break

                # ===== PROBLEMA 6: SEM RETROCESSO =====
                if not colocado:
                    """
                    PROBLEMA: Quando não consegue alocar, simplesmente desiste.
                    Não tenta rearranjar aulas já alocadas para liberar espaço.
                    
                    Isso é um algoritmo GULOSO sem backtracking - pode falhar
                    mesmo quando uma solução existe.
                    """
                    print(
                        f"Não foi possível alocar "
                        f"{rel.disciplina} para {turma.nome}"
                    )
                    break

    print(f"Aulas criadas: {total_criadas}")

    #___*( ￣皿￣)/#____