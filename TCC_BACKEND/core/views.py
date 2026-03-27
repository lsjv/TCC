from django.shortcuts import render, get_object_or_404
from core.models import Turma, Slot, Aula

CORES_DISCIPLINA = {
    "Matemática":        {"bg": "#EEEDFE", "border": "#534AB7", "text": "#3C3489"},
    "Língua Portuguesa": {"bg": "#E1F5EE", "border": "#0F6E56", "text": "#085041"},
    "História":          {"bg": "#FAEEDA", "border": "#854F0B", "text": "#633806"},
    "Geografia":         {"bg": "#FAECE7", "border": "#993C1D", "text": "#712B13"},
    "Ciências":          {"bg": "#EAF3DE", "border": "#3B6D11", "text": "#27500A"},
    "Língua Inglesa":    {"bg": "#E6F1FB", "border": "#185FA5", "text": "#0C447C"},
    "Educação Física":   {"bg": "#FBEAF0", "border": "#993556", "text": "#72243E"},
    "Artes":             {"bg": "#F1EFE8", "border": "#5F5E5A", "text": "#444441"},
}

def grade_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)

    # Pega só os números de aula únicos — deve retornar [1,2,3,4,5]
    numeros_aula = sorted(
        Slot.objects.filter(
            escola=turma.escola
        ).values_list('numero_aula', flat=True).distinct()
    )

    aulas_qs = Aula.objects.filter(
        turma_disciplina__turma=turma
    ).select_related(
        'slot',
        'turma_disciplina__disciplina',
        'turma_disciplina__professor'
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

    return render(request, 'core/grade.html', {
        'turma': turma,
        'dias': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'],
        'grade': grade,
        'cores_disciplina': CORES_DISCIPLINA,
    })