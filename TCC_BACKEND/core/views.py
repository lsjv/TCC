from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Sum, Count
from django.http import HttpResponse

from core.models import (
    Escola, Professor, Disciplina, Turma, TurmaDisciplina,
    Slot, Aula, DisponibilidadeProfessor,
)
from core.forms import (
    EscolaForm, ProfessorForm, DisciplinaForm, TurmaForm,
    TurmaDisciplinaForm, SlotBulkForm,
)
from core.algoritimos.gerar_horario import gerar_horario_baseado_professor


# ─── Dashboard ────────────────────────────────────────────────────────────────

def dashboard(request):
    escolas = Escola.objects.annotate(num_turmas=Count('turma'))
    return render(request, 'core/dashboard.html', {'escolas': escolas})


# ─── Escola ───────────────────────────────────────────────────────────────────

def escola_detail(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    turmas = (
        escola.turma_set
        .annotate(
            num_disciplinas=Count('turmadisciplina'),
            total_aulas=Sum('turmadisciplina__aulas_semanais'),
        )
        .order_by('turno', 'nome')
    )
    slots_por_turno = {}
    for slot in Slot.objects.filter(escola=escola).order_by('turno', 'dia_semana', 'numero_aula'):
        slots_por_turno.setdefault(slot.turno, []).append(slot)

    num_professores  = escola.professores.count()
    num_disciplinas  = escola.disciplinas.count()

    return render(request, 'core/escola_detail.html', {
        'escola': escola,
        'turmas': turmas,
        'slots_por_turno': slots_por_turno,
        'num_professores': num_professores,
        'num_disciplinas': num_disciplinas,
    })


def escola_create(request):
    form = EscolaForm(request.POST or None)
    if form.is_valid():
        escola = form.save()
        messages.success(request, f'Escola "{escola.nome}" criada.')
        return redirect('escola_detail', escola_id=escola.id)
    return render(request, 'core/escola_form.html', {
        'form': form,
        'titulo': 'Nova Escola',
        'cancel_url': reverse('dashboard'),
    })


def escola_edit(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    form = EscolaForm(request.POST or None, instance=escola)
    if form.is_valid():
        form.save()
        messages.success(request, 'Escola atualizada.')
        return redirect('escola_detail', escola_id=escola.id)
    return render(request, 'core/escola_form.html', {
        'form': form,
        'titulo': 'Editar Escola',
        'cancel_url': reverse('escola_detail', args=[escola_id]),
    })


def escola_delete(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    if request.method == 'POST':
        nome = escola.nome
        escola.delete()
        messages.success(request, f'Escola "{nome}" excluída.')
        return redirect('dashboard')
    return render(request, 'core/confirm_delete.html', {
        'object_name': escola.nome,
        'cancel_url': reverse('escola_detail', args=[escola_id]),
    })


def gerar_horario_view(request, escola_id):
    if request.method == 'POST':
        resultado = gerar_horario_baseado_professor(escola_id, debug=False)
        if resultado:
            messages.success(request, 'Horário gerado com sucesso!')
        else:
            messages.error(
                request,
                'Não foi possível gerar o horário. Verifique se o total de aulas '
                'de cada turma não excede os slots disponíveis.'
            )
    return redirect('escola_detail', escola_id=escola_id)


# ─── Slots ────────────────────────────────────────────────────────────────────

DIAS_NOMES = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']


def slot_list(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    form = SlotBulkForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        turno = form.cleaned_data['turno']
        num_aulas = form.cleaned_data['num_aulas']
        dias = [int(d) for d in form.cleaned_data['dias']]

        criados = 0
        for dia in dias:
            for aula in range(1, num_aulas + 1):
                _, created = Slot.objects.get_or_create(
                    escola=escola,
                    dia_semana=dia,
                    numero_aula=aula,
                    turno=turno,
                )
                if created:
                    criados += 1

        messages.success(request, f'{criados} slot(s) criado(s) com sucesso.')
        return redirect('slot_list', escola_id=escola_id)

    slots_qs = Slot.objects.filter(escola=escola).order_by('turno', 'dia_semana', 'numero_aula')
    grupos = {}
    for s in slots_qs:
        grupos.setdefault(s.turno, {}).setdefault(s.dia_semana, []).append(s)

    return render(request, 'core/slot_list.html', {
        'escola': escola,
        'form': form,
        'grupos': grupos,
        'dias_nomes': DIAS_NOMES,
    })


def slot_delete_turno(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    if request.method == 'POST':
        turno = request.POST.get('turno')
        if turno:
            count, _ = Slot.objects.filter(escola=escola, turno=turno).delete()
            messages.success(request, f'{count} slot(s) do turno "{turno}" excluídos.')
        else:
            messages.error(request, 'Turno não informado.')
    return redirect('slot_list', escola_id=escola_id)


# ─── Professor ────────────────────────────────────────────────────────────────

def professor_list(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    professores = escola.professores.order_by('nome')
    return render(request, 'core/professor_list.html', {
        'escola': escola,
        'professores': professores,
    })


def professor_create(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    form = ProfessorForm(request.POST or None)
    if form.is_valid():
        prof = form.save(commit=False)
        prof.escola = escola
        prof.save()
        messages.success(request, f'Professor "{prof.nome}" criado.')
        return redirect('professor_list', escola_id=escola_id)
    return render(request, 'core/professor_form.html', {
        'form': form,
        'titulo': 'Novo Professor',
        'escola': escola,
        'cancel_url': reverse('professor_list', args=[escola_id]),
    })


def professor_edit(request, professor_id):
    prof = get_object_or_404(Professor, id=professor_id)
    escola_id = prof.escola_id
    form = ProfessorForm(request.POST or None, instance=prof)
    if form.is_valid():
        form.save()
        messages.success(request, 'Professor atualizado.')
        return redirect('professor_list', escola_id=escola_id)
    return render(request, 'core/professor_form.html', {
        'form': form,
        'titulo': 'Editar Professor',
        'escola': prof.escola,
        'cancel_url': reverse('professor_list', args=[escola_id]),
    })


def professor_delete(request, professor_id):
    prof = get_object_or_404(Professor, id=professor_id)
    escola_id = prof.escola_id
    if request.method == 'POST':
        nome = prof.nome
        prof.delete()
        messages.success(request, f'Professor "{nome}" excluído.')
        return redirect('professor_list', escola_id=escola_id)
    return render(request, 'core/confirm_delete.html', {
        'object_name': prof.nome,
        'cancel_url': reverse('professor_list', args=[escola_id]),
    })


def professor_disponibilidade(request, professor_id):
    """Grade de checkboxes (dia × aula) para configurar disponibilidade do professor."""
    prof = get_object_or_404(Professor, id=professor_id)
    escola_id = prof.escola_id

    # Filtra slots apenas da escola deste professor
    todos_slots = (
        Slot.objects
        .filter(escola_id=escola_id)
        .values_list('dia_semana', 'numero_aula')
        .distinct()
        .order_by('numero_aula', 'dia_semana')
    )
    numeros_aula = sorted({n for _, n in todos_slots})

    disp_atual = set(
        DisponibilidadeProfessor.objects
        .filter(professor=prof)
        .values_list('dia_semana', 'numero_aula')
    )

    if request.method == 'POST':
        novas = set()
        for dia in range(5):
            for num in numeros_aula:
                if request.POST.get(f'slot_{dia}_{num}'):
                    novas.add((dia, num))

        for (dia, num) in disp_atual - novas:
            DisponibilidadeProfessor.objects.filter(
                professor=prof, dia_semana=dia, numero_aula=num
            ).delete()

        for (dia, num) in novas - disp_atual:
            DisponibilidadeProfessor.objects.get_or_create(
                professor=prof, dia_semana=dia, numero_aula=num
            )

        messages.success(request, f'Disponibilidade de {prof.nome} atualizada.')
        return redirect('professor_list', escola_id=escola_id)

    return render(request, 'core/professor_disponibilidade.html', {
        'prof': prof,
        'escola': prof.escola,
        'numeros_aula': numeros_aula,
        'dias': list(enumerate(DIAS_NOMES)),
        'disp_atual': disp_atual,
    })


# ─── Disciplina ───────────────────────────────────────────────────────────────

def disciplina_list(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    disciplinas = escola.disciplinas.order_by('nome')
    return render(request, 'core/disciplina_list.html', {
        'escola': escola,
        'disciplinas': disciplinas,
    })


def disciplina_create(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    form = DisciplinaForm(request.POST or None)
    if form.is_valid():
        disc = form.save(commit=False)
        disc.escola = escola
        disc.save()
        messages.success(request, f'Disciplina "{disc.nome}" criada.')
        return redirect('disciplina_list', escola_id=escola_id)
    return render(request, 'core/disciplina_form.html', {
        'form': form,
        'titulo': 'Nova Disciplina',
        'escola': escola,
        'cancel_url': reverse('disciplina_list', args=[escola_id]),
    })


def disciplina_edit(request, disciplina_id):
    disc = get_object_or_404(Disciplina, id=disciplina_id)
    escola_id = disc.escola_id
    form = DisciplinaForm(request.POST or None, instance=disc)
    if form.is_valid():
        form.save()
        messages.success(request, 'Disciplina atualizada.')
        return redirect('disciplina_list', escola_id=escola_id)
    return render(request, 'core/disciplina_form.html', {
        'form': form,
        'titulo': 'Editar Disciplina',
        'escola': disc.escola,
        'cancel_url': reverse('disciplina_list', args=[escola_id]),
    })


def disciplina_delete(request, disciplina_id):
    disc = get_object_or_404(Disciplina, id=disciplina_id)
    escola_id = disc.escola_id
    if request.method == 'POST':
        nome = disc.nome
        disc.delete()
        messages.success(request, f'Disciplina "{nome}" excluída.')
        return redirect('disciplina_list', escola_id=escola_id)
    return render(request, 'core/confirm_delete.html', {
        'object_name': disc.nome,
        'cancel_url': reverse('disciplina_list', args=[escola_id]),
    })


# ─── Turma ────────────────────────────────────────────────────────────────────

def turma_create(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    form = TurmaForm(request.POST or None)
    if form.is_valid():
        turma = form.save(commit=False)
        turma.escola = escola
        turma.save()
        messages.success(request, f'Turma "{turma.nome}" criada.')
        return redirect('escola_detail', escola_id=escola_id)
    return render(request, 'core/turma_form.html', {
        'form': form,
        'titulo': 'Nova Turma',
        'escola': escola,
        'cancel_url': reverse('escola_detail', args=[escola_id]),
    })


def turma_edit(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    form = TurmaForm(request.POST or None, instance=turma)
    if form.is_valid():
        form.save()
        messages.success(request, 'Turma atualizada.')
        return redirect('escola_detail', escola_id=turma.escola_id)
    return render(request, 'core/turma_form.html', {
        'form': form,
        'titulo': 'Editar Turma',
        'escola': turma.escola,
        'cancel_url': reverse('escola_detail', args=[turma.escola_id]),
    })


def turma_delete(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    escola_id = turma.escola_id
    if request.method == 'POST':
        nome = turma.nome
        turma.delete()
        messages.success(request, f'Turma "{nome}" excluída.')
        return redirect('escola_detail', escola_id=escola_id)
    return render(request, 'core/confirm_delete.html', {
        'object_name': turma.nome,
        'cancel_url': reverse('escola_detail', args=[escola_id]),
    })


# ─── TurmaDisciplina ──────────────────────────────────────────────────────────

def turma_disciplina_list(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    relacoes = (
        TurmaDisciplina.objects
        .filter(turma=turma)
        .select_related('disciplina', 'professor')
        .order_by('disciplina__nome')
    )
    total_aulas = sum(r.aulas_semanais for r in relacoes)
    total_slots = Slot.objects.filter(escola=turma.escola, turno=turma.turno).count()
    return render(request, 'core/turma_disciplina_list.html', {
        'turma': turma,
        'relacoes': relacoes,
        'total_aulas': total_aulas,
        'total_slots': total_slots,
    })


def turma_disciplina_create(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    form = TurmaDisciplinaForm(request.POST or None, escola=turma.escola)
    if form.is_valid():
        td = form.save(commit=False)
        td.turma = turma
        td.save()
        messages.success(request, f'"{td.disciplina.nome}" adicionada à turma.')
        return redirect('turma_disciplina_list', turma_id=turma_id)
    return render(request, 'core/turma_disciplina_form.html', {
        'form': form,
        'titulo': 'Adicionar Disciplina',
        'turma': turma,
        'cancel_url': reverse('turma_disciplina_list', args=[turma_id]),
    })


def turma_disciplina_edit(request, td_id):
    td = get_object_or_404(TurmaDisciplina, id=td_id)
    form = TurmaDisciplinaForm(request.POST or None, instance=td, escola=td.turma.escola)
    if form.is_valid():
        form.save()
        messages.success(request, 'Disciplina atualizada.')
        return redirect('turma_disciplina_list', turma_id=td.turma_id)
    return render(request, 'core/turma_disciplina_form.html', {
        'form': form,
        'titulo': 'Editar Disciplina',
        'turma': td.turma,
        'cancel_url': reverse('turma_disciplina_list', args=[td.turma_id]),
    })


def turma_disciplina_delete(request, td_id):
    td = get_object_or_404(TurmaDisciplina, id=td_id)
    turma_id = td.turma_id
    if request.method == 'POST':
        td.delete()
        messages.success(request, 'Disciplina removida da turma.')
        return redirect('turma_disciplina_list', turma_id=turma_id)
    return render(request, 'core/confirm_delete.html', {
        'object_name': f'{td.disciplina.nome} — {td.turma.nome}',
        'cancel_url': reverse('turma_disciplina_list', args=[turma_id]),
    })


# ─── Grade ────────────────────────────────────────────────────────────────────

def _build_grade_context(turma_id):
    turma = get_object_or_404(Turma, id=turma_id)

    numeros_aula = sorted(
        Slot.objects.filter(
            escola=turma.escola,
            turno=turma.turno,
        ).values_list('numero_aula', flat=True).distinct()
    )

    aulas_qs = Aula.objects.filter(
        turma_disciplina__turma=turma
    ).select_related(
        'slot',
        'turma_disciplina__disciplina',
        'turma_disciplina__professor',
    )

    aulas_dict = {}
    for aula in aulas_qs:
        chave = (aula.slot.dia_semana, aula.slot.numero_aula)
        aulas_dict[chave] = aula

    grade = []
    for numero in numeros_aula:
        linha = []
        for dia in range(5):
            linha.append(aulas_dict.get((dia, numero)))
        grade.append(linha)

    return {
        'turma': turma,
        'dias': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'],
        'grade': grade,
    }


def grade_turma(request, turma_id):
    ctx = _build_grade_context(turma_id)
    return render(request, 'core/grade.html', ctx)


def grade_pdf(request, turma_id):
    try:
        from weasyprint import HTML
    except ImportError:
        return HttpResponse(
            'WeasyPrint não está instalado. Execute: pip install weasyprint',
            status=500,
        )

    ctx = _build_grade_context(turma_id)
    html_string = render(request, 'core/grade_pdf.html', ctx).content.decode('utf-8')
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()

    turma = ctx['turma']
    nome_arquivo = f"grade_{turma.nome.replace(' ', '_')}.pdf"
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    return response
