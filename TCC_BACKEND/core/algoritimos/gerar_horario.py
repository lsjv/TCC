from core.models import Turma, Slot, Aula, TurmaDisciplina, DisponibilidadeProfessor
from django.db import transaction


def gerar_horario_escola(escola_id):
    """
    Gera horários usando backtracking com otimizações de desempenho.
    """

    # 1. Carregar tudo em memória (elimina o Problema 5 - consultas excessivas)
    slots = list(Slot.objects.filter(escola_id=escola_id))
    turmas = list(Turma.objects.filter(escola_id=escola_id))

    # Disponibilidades: set de (professor_id, dia_semana, numero_aula)
    disponibilidades = set(
        DisponibilidadeProfessor.objects
        .values_list('professor_id', 'dia_semana', 'numero_aula')
    )

    # Expandir relações em lista de "aulas a alocar"
    # Cada TurmaDisciplina com aulas_semanais=3 vira 3 entradas
    relacoes = TurmaDisciplina.objects.filter(
        turma__escola_id=escola_id
    ).select_related('turma', 'disciplina', 'professor')

    tarefas = []
    for rel in relacoes:
        for _ in range(rel.aulas_semanais):
            tarefas.append(rel)

    # Ordenar por mais restrito primeiro (MRV - Minimum Remaining Values)
    # Disciplinas com mais aulas semanais são mais difíceis de alocar
    tarefas.sort(key=lambda r: -r.aulas_semanais)

    # Estado compartilhado em memória (evita consultas ao banco durante busca)
    alocacoes = []  # lista de (slot, turma_disciplina)
    ocupado_turma  = {}  # slot_id → set de turma_id
    ocupado_prof   = {}  # slot_id → set de professor_id

    def pode_alocar(slot, rel):
        sid = slot.id

        # Turno compatível
        if slot.turno != rel.turma.turno:
            return False

        # Turma já tem aula nesse slot
        if rel.turma.id in ocupado_turma.get(sid, set()):
            return False

        # Professor já tem aula nesse slot
        if rel.professor.id in ocupado_prof.get(sid, set()):
            return False

        # Verificar disponibilidade do professor
        # Se há registros de disponibilidade, o professor só pode
        # dar aula nos slots listados
        if disponibilidades:
            chave = (rel.professor.id, slot.dia_semana, slot.numero_aula)
            if chave not in disponibilidades:
                return False

        return True

    def alocar(slot, rel):
        sid = slot.id
        ocupado_turma.setdefault(sid, set()).add(rel.turma.id)
        ocupado_prof.setdefault(sid, set()).add(rel.professor.id)
        alocacoes.append((slot, rel))

    def desalocar():
        slot, rel = alocacoes.pop()
        sid = slot.id
        ocupado_turma[sid].discard(rel.turma.id)
        ocupado_prof[sid].discard(rel.professor.id)

    def backtrack(idx):
        if idx == len(tarefas):
            return True  # todas as aulas foram alocadas!

        rel = tarefas[idx]

        # Embaralhar slots a cada chamada evita concentração nos primeiros
        # horários e distribui melhor a grade (resolve Problema 4)
        import random
        slots_candidatos = slots[:]
        random.shuffle(slots_candidatos)

        for slot in slots_candidatos:
            if pode_alocar(slot, rel):
                alocar(slot, rel)
                if backtrack(idx + 1):
                    return True
                desalocar()  # ← aqui está o backtracking de verdade

        return False  # nenhum slot funcionou para esta tarefa

    print(f"Iniciando backtracking: {len(tarefas)} aulas para alocar...")

    sucesso = backtrack(0)

    if not sucesso:
        print("Não foi possível gerar um horário completo.")
        return False

    # Salvar no banco apenas se tudo funcionou (resolve Problema 1 - deleção parcial)
    with transaction.atomic():
        Aula.objects.filter(
            turma_disciplina__turma__escola_id=escola_id  # só desta escola!
        ).delete()

        Aula.objects.bulk_create([
            Aula(slot=slot, turma_disciplina=rel)
            for slot, rel in alocacoes
        ])

    print(f"Horário gerado! {len(alocacoes)} aulas criadas.")
    return True