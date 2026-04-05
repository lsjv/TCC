from core.models import (
    Turma, Slot, Aula, TurmaDisciplina, DisponibilidadeProfessor
)
from django.db import transaction
from collections import defaultdict
import random
import time


def gerar_horario_baseado_professor(escola_id, max_rodadas=10, max_por_rodada=500_000, debug=True):

    inicio = time.time()

    def log(msg):
        if debug:
            print(f"[{time.time() - inicio:6.1f}s] {msg}")

    log("=== INICIANDO GERADOR DE HORÁRIOS ===")

    # Carregar dados
    slots_qs = list(Slot.objects.filter(escola_id=escola_id))
    total_slots = len(slots_qs)

    if total_slots == 0:
        log("ERRO: Nenhum slot encontrado!")
        return False

    relacoes = list(TurmaDisciplina.objects.filter(
        turma__escola_id=escola_id
    ).select_related('turma', 'disciplina', 'professor'))

    if not relacoes:
        log("ERRO: Nenhuma relação turma-disciplina encontrada!")
        return False

    disponibilidades = set(
        DisponibilidadeProfessor.objects
        .values_list('professor_id', 'dia_semana', 'numero_aula')
    )

    # Expandir tarefas agrupadas por professor
    tarefas_por_prof = defaultdict(list)
    for rel in relacoes:
        for _ in range(rel.aulas_semanais):
            tarefas_por_prof[rel.professor.id].append(rel)

    # Mapa de professor_id → objeto professor
    prof_map = {rel.professor.id: rel.professor for rel in relacoes}

    # Verificar viabilidade
    log("=== VERIFICANDO VIABILIDADE ===")
    inviavel = False
    for prof_id, tarefas in tarefas_por_prof.items():
        prof = prof_map[prof_id]
        carga = len(tarefas)
        limite = min(total_slots, prof.carga_maxima_semana)
        if carga > limite:
            log(f"INVIÁVEL: {prof.nome} tem {carga} aulas mas limite é {limite}")
            inviavel = True
        else:
            log(f"OK: {prof.nome} — {carga} aulas / limite {limite}")

    if inviavel:
        log("Abortando — dados inviáveis.")
        return False

    log("Viabilidade OK!")

    # Ordenar professores por carga decrescente (MRV — mais restrito primeiro)
    prof_ids_ordenados = sorted(
        tarefas_por_prof.keys(),
        key=lambda pid: len(tarefas_por_prof[pid]),
        reverse=True
    )

    # Flatten das tarefas na ordem certa
    tarefas_base = []
    for prof_id in prof_ids_ordenados:
        tarefas_base.extend(tarefas_por_prof[prof_id])

    log(f"Total: {len(tarefas_base)} aulas para alocar")
    log("=== INICIANDO BACKTRACKING COM RANDOM RESTART ===")

    tentativas_total = [0]

    for rodada in range(1, max_rodadas + 1):

        log(f"Rodada {rodada}/{max_rodadas}...")

        slots = slots_qs[:]
        random.shuffle(slots)

        # Estado em memória
        ocupado_prof  = {}  # slot_id → set de professor_id
        ocupado_turma = {}  # slot_id → set de turma_id
        carga_prof    = {}  # professor_id → aulas alocadas
        alocacoes     = []

        tentativas_rodada = [0]
        backtracks        = [0]
        ultimo_log        = [0]

        def pode_alocar(slot, rel):
            sid = slot.id

            # Turno compatível
            if slot.turno != rel.turma.turno:
                return False

            # Professor já está nesse slot?
            if rel.professor.id in ocupado_prof.get(sid, set()):
                return False

            # Turma já tem aula nesse slot?
            if rel.turma.id in ocupado_turma.get(sid, set()):
                return False

            # Carga máxima do professor
            if carga_prof.get(rel.professor.id, 0) >= rel.professor.carga_maxima_semana:
                return False

            # Disponibilidade do professor (só verifica se há registros)
            if disponibilidades:
                if (rel.professor.id, slot.dia_semana, slot.numero_aula) not in disponibilidades:
                    return False

            return True

        def alocar(slot, rel):
            sid = slot.id
            ocupado_prof.setdefault(sid, set()).add(rel.professor.id)
            ocupado_turma.setdefault(sid, set()).add(rel.turma.id)
            carga_prof[rel.professor.id] = carga_prof.get(rel.professor.id, 0) + 1
            alocacoes.append((slot, rel))

        def desalocar():
            slot, rel = alocacoes.pop()
            sid = slot.id
            ocupado_prof[sid].discard(rel.professor.id)
            ocupado_turma[sid].discard(rel.turma.id)
            carga_prof[rel.professor.id] -= 1

        def backtrack(idx):
            tentativas_rodada[0] += 1
            tentativas_total[0]  += 1

            if tentativas_rodada[0] > max_por_rodada:
                raise Exception("LimiteTentativas")

            agora = time.time() - inicio
            if agora - ultimo_log[0] >= 5.0:
                ultimo_log[0] = agora
                log(
                    f"Progresso: {idx}/{len(tarefas_base)} aulas | "
                    f"{tentativas_rodada[0]:,} tentativas | "
                    f"{backtracks[0]:,} backtracks"
                )

            if idx == len(tarefas_base):
                return True

            rel = tarefas_base[idx]
            slots_validos = [s for s in slots if pode_alocar(s, rel)]

            if not slots_validos:
                return False

            random.shuffle(slots_validos)

            for slot in slots_validos:
                alocar(slot, rel)
                if backtrack(idx + 1):
                    return True
                desalocar()
                backtracks[0] += 1

            return False

        try:
            sucesso = backtrack(0)
        except Exception as e:
            if "LimiteTentativas" in str(e):
                log(f"Rodada {rodada} abortada — {tentativas_rodada[0]:,} tentativas")
                continue
            raise

        if sucesso:
            log(f"Solução encontrada na rodada {rodada}! Total: {tentativas_total[0]:,} tentativas")
            log("Salvando no banco...")

            with transaction.atomic():
                Aula.objects.filter(
                    turma_disciplina__turma__escola_id=escola_id
                ).delete()
                Aula.objects.bulk_create([
                    Aula(slot=slot, turma_disciplina=rel)
                    for slot, rel in alocacoes
                ])

            log(f"Concluído! {len(alocacoes)} aulas salvas.")
            return True

    log(f"FALHOU após {max_rodadas} rodadas e {tentativas_total[0]:,} tentativas totais.")
    return False