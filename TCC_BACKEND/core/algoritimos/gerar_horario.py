from core.models import Slot, Aula, TurmaDisciplina, DisponibilidadeProfessor
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

    # Disponibilidade individual por professor: professor_id → set((dia_semana, numero_aula))
    # None significa sem restrição (professor não tem nenhum registro cadastrado)
    disponibilidades_por_prof = {}
    for prof_id, dia, aula in DisponibilidadeProfessor.objects.values_list(
        'professor_id', 'dia_semana', 'numero_aula'
    ):
        disponibilidades_por_prof.setdefault(prof_id, set()).add((dia, aula))

    # Slots agrupados por turno para a verificação de viabilidade
    slots_por_turno = defaultdict(list)
    for slot in slots_qs:
        slots_por_turno[slot.turno].append(slot)

    # Expandir tarefas agrupadas por professor
    tarefas_por_prof = defaultdict(list)
    for rel in relacoes:
        for _ in range(rel.aulas_semanais):
            tarefas_por_prof[rel.professor.id].append(rel)

    prof_map = {rel.professor.id: rel.professor for rel in relacoes}

    log("=== VERIFICANDO VIABILIDADE ===")
    inviavel = False
    for prof_id, tarefas in tarefas_por_prof.items():
        prof = prof_map[prof_id]
        carga = len(tarefas)
        # Slots acessíveis = soma dos slots de todos os turnos em que o professor leciona
        turnos_prof = {rel.turma.turno for rel in tarefas}
        slots_acessiveis = sum(len(slots_por_turno[t]) for t in turnos_prof)
        limite = min(slots_acessiveis, prof.carga_maxima_semana)
        if carga > limite:
            log(f"INVIÁVEL: {prof.nome} tem {carga} aulas mas limite é {limite} (turnos: {turnos_prof})")
            inviavel = True
        else:
            log(f"OK: {prof.nome} — {carga} aulas / limite {limite}")

    if inviavel:
        log("Abortando — dados inviáveis.")
        return False

    log("Viabilidade OK!")

    # Ordenar professores por carga decrescente (heurística MRV — mais restrito primeiro)
    prof_ids_ordenados = sorted(
        tarefas_por_prof.keys(),
        key=lambda pid: len(tarefas_por_prof[pid]),
        reverse=True
    )

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

        ocupado_prof  = {}  # slot_id → set de professor_id
        ocupado_turma = {}  # slot_id → set de turma_id
        carga_prof    = {}  # professor_id → aulas alocadas
        alocacoes     = []

        # Rastreia aulas alocadas por (professor_id, dia, numero_aula) para verificar consecutivas
        # e por (turma_id, dia) para verificar brechas
        aulas_prof_dia    = defaultdict(set)   # (prof_id, dia) → set(numero_aula)
        aulas_turma_dia   = defaultdict(set)   # (turma_id, dia) → set(numero_aula)

        tentativas_rodada = [0]
        backtracks        = [0]
        ultimo_log        = [0]

        def pode_alocar(slot, rel):
            sid = slot.id
            dia = slot.dia_semana
            num = slot.numero_aula
            prof = rel.professor
            turma = rel.turma

            if slot.turno != turma.turno:
                return False

            if prof.id in ocupado_prof.get(sid, set()):
                return False

            if turma.id in ocupado_turma.get(sid, set()):
                return False

            if carga_prof.get(prof.id, 0) >= prof.carga_maxima_semana:
                return False

            # Verifica disponibilidade apenas se o professor tem registros cadastrados
            disp = disponibilidades_por_prof.get(prof.id)
            if disp is not None:
                if (dia, num) not in disp:
                    return False

            # ── Restrição de aulas consecutivas ─────────────────────────────
            max_consec = prof.max_aulas_consecutivas
            if max_consec > 0:
                aulas_do_prof_neste_dia = aulas_prof_dia[(prof.id, dia)]
                if aulas_do_prof_neste_dia:
                    # Conta quantas aulas consecutivas existem se adicionarmos `num`
                    todas = sorted(aulas_do_prof_neste_dia | {num})
                    max_seq = 1
                    seq_atual = 1
                    for i in range(1, len(todas)):
                        if todas[i] == todas[i-1] + 1:
                            seq_atual += 1
                            max_seq = max(max_seq, seq_atual)
                        else:
                            seq_atual = 1
                    if max_seq > max_consec:
                        return False

            # ── Restrição de brecha na grade da turma ────────────────────────
            # Evita que a turma fique com janela (ex: aula 1, sem aula 2, aula 3)
            # Só aplica se a turma já tem aulas alocadas neste dia
            aulas_da_turma_neste_dia = aulas_turma_dia[(turma.id, dia)]
            if aulas_da_turma_neste_dia:
                # Após adicionar `num`, verifica se haveria brecha interior
                todas_turma = sorted(aulas_da_turma_neste_dia | {num})
                for i in range(1, len(todas_turma)):
                    if todas_turma[i] > todas_turma[i-1] + 1:
                        return False

            return True

        def alocar(slot, rel):
            sid = slot.id
            dia = slot.dia_semana
            num = slot.numero_aula
            prof_id = rel.professor.id
            turma_id = rel.turma.id

            ocupado_prof.setdefault(sid, set()).add(prof_id)
            ocupado_turma.setdefault(sid, set()).add(turma_id)
            carga_prof[prof_id] = carga_prof.get(prof_id, 0) + 1
            aulas_prof_dia[(prof_id, dia)].add(num)
            aulas_turma_dia[(turma_id, dia)].add(num)
            alocacoes.append((slot, rel))

        def desalocar():
            slot, rel = alocacoes.pop()
            sid = slot.id
            dia = slot.dia_semana
            num = slot.numero_aula
            prof_id = rel.professor.id
            turma_id = rel.turma.id

            ocupado_prof[sid].discard(prof_id)
            ocupado_turma[sid].discard(turma_id)
            carga_prof[prof_id] -= 1
            aulas_prof_dia[(prof_id, dia)].discard(num)
            aulas_turma_dia[(turma_id, dia)].discard(num)

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
