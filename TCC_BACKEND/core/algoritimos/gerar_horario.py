from core.models import (
    Turma,
    Slot,
    Aula,
    TurmaDisciplina,
    DisponibilidadeProfessor
)
from django.db import transaction
import random
import time


class LimiteTentativas(Exception):
    pass


def verificar_viabilidade(escola_id):
    from collections import defaultdict

    total_slots = Slot.objects.filter(escola_id=escola_id).count()
    relacoes = TurmaDisciplina.objects.filter(
        turma__escola_id=escola_id
    ).select_related('professor')

    carga_por_professor = defaultdict(int)
    for rel in relacoes:
        carga_por_professor[rel.professor.id] += rel.aulas_semanais

    professores = {
        rel.professor.id: rel.professor
        for rel in relacoes
    }

    inviavel = False
    for prof_id, carga in carga_por_professor.items():
        prof = professores[prof_id]
        limite = min(total_slots, prof.carga_maxima_semana)
        if carga > limite:
            print(
                f"INVIÁVEL: {prof.nome} tem {carga} aulas "
                f"mas o limite é {limite} "
                f"(slots={total_slots}, carga_max={prof.carga_maxima_semana})"
            )
            inviavel = True

    if not inviavel:
        print("Viabilidade OK — pode rodar o algoritmo.")

    return not inviavel


def gerar_horario_escola(escola_id):

    inicio = time.time()

    def log(msg):
        print(f"[{time.time() - inicio:6.1f}s] {msg}")

    log("Verificando viabilidade...")
    if not verificar_viabilidade(escola_id):
        log("Abortando — dados inviáveis.")
        return False

    log("Carregando dados do banco...")

    slots = list(Slot.objects.filter(escola_id=escola_id))
    turmas = list(Turma.objects.filter(escola_id=escola_id))

    disponibilidades = set(
        DisponibilidadeProfessor.objects
        .values_list('professor_id', 'dia_semana', 'numero_aula')
    )

    relacoes = TurmaDisciplina.objects.filter(
        turma__escola_id=escola_id
    ).select_related('turma', 'disciplina', 'professor')

    tarefas = []
    for rel in relacoes:
        for _ in range(rel.aulas_semanais):
            tarefas.append(rel)

    # Agrupa por turma primeiro, depois por mais aulas — reduz conflitos
    tarefas.sort(key=lambda r: (r.turma.id, -r.aulas_semanais))

    log(
        f"Dados: {len(turmas)} turmas, "
        f"{len(slots)} slots, "
        f"{len(tarefas)} aulas para alocar"
    )

    alocacoes        = []
    ocupado_turma    = {}
    ocupado_prof     = {}
    carga_atual_prof = {}

    tentativas = [0]
    backtracks = [0]
    ultimo_log = [0]

    def pode_alocar(slot, rel):
        sid = slot.id

        if slot.turno != rel.turma.turno:
            return False

        if rel.turma.id in ocupado_turma.get(sid, set()):
            return False

        if rel.professor.id in ocupado_prof.get(sid, set()):
            return False

        if carga_atual_prof.get(rel.professor.id, 0) >= rel.professor.carga_maxima_semana:
            return False

        if disponibilidades:
            chave = (rel.professor.id, slot.dia_semana, slot.numero_aula)
            if chave not in disponibilidades:
                return False

        return True

    def alocar(slot, rel):
        sid = slot.id
        ocupado_turma.setdefault(sid, set()).add(rel.turma.id)
        ocupado_prof.setdefault(sid, set()).add(rel.professor.id)
        carga_atual_prof[rel.professor.id] = (
            carga_atual_prof.get(rel.professor.id, 0) + 1
        )
        alocacoes.append((slot, rel))

    def desalocar():
        slot, rel = alocacoes.pop()
        sid = slot.id
        ocupado_turma[sid].discard(rel.turma.id)
        ocupado_prof[sid].discard(rel.professor.id)
        carga_atual_prof[rel.professor.id] -= 1

    def backtrack(idx):
        tentativas[0] += 1

        if tentativas[0] > 500_000:
            raise LimiteTentativas()

        agora = time.time() - inicio
        if agora - ultimo_log[0] >= 5.0:
            ultimo_log[0] = agora
            log(
                f"Progresso: {idx}/{len(tarefas)} aulas | "
                f"{tentativas[0]:,} tentativas | "
                f"{backtracks[0]:,} backtracks"
            )

        if idx == len(tarefas):
            return True

        rel = tarefas[idx]

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

    log("Iniciando backtracking...")

    try:
        sucesso = backtrack(0)
    except LimiteTentativas:
        log(f"ABORTADO: limite atingido após {tentativas[0]:,} tentativas")
        return False

    if not sucesso:
        log(
            f"FALHOU: {tentativas[0]:,} tentativas, "
            f"{backtracks[0]:,} backtracks"
        )
        return False

    log(
        f"Solução encontrada! "
        f"{tentativas[0]:,} tentativas, "
        f"{backtracks[0]:,} backtracks"
    )
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