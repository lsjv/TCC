from django import forms
from .models import Escola, Professor, Disciplina, Turma, TurmaDisciplina, Slot

TURNO_CHOICES = [
    ('manha',      'Manhã'),
    ('tarde',      'Tarde'),
    ('vespertino', 'Vespertino'),
    ('noturno',    'Noturno'),
]


class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome da escola'}),
        }


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'carga_maxima_semana', 'max_aulas_consecutivas']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'carga_maxima_semana': forms.NumberInput(attrs={'min': 1, 'max': 40}),
            'max_aulas_consecutivas': forms.NumberInput(attrs={'min': 0, 'max': 10}),
        }
        labels = {
            'carga_maxima_semana': 'Carga máxima semanal (aulas)',
            'max_aulas_consecutivas': 'Máx. aulas consecutivas (0 = sem limite)',
        }


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'cor_bg', 'cor_borda', 'cor_texto']
        widgets = {
            'nome':     forms.TextInput(attrs={'placeholder': 'Nome da disciplina'}),
            'cor_bg':   forms.TextInput(attrs={'type': 'color', 'class': 'color-input'}),
            'cor_borda': forms.TextInput(attrs={'type': 'color', 'class': 'color-input'}),
            'cor_texto': forms.TextInput(attrs={'type': 'color', 'class': 'color-input'}),
        }
        labels = {
            'cor_bg':    'Cor de fundo',
            'cor_borda': 'Cor da borda',
            'cor_texto': 'Cor do texto',
        }


class TurmaForm(forms.ModelForm):
    turno = forms.ChoiceField(choices=TURNO_CHOICES, label='Turno')

    class Meta:
        model = Turma
        fields = ['nome', 'turno']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: ENF P26, 3A, INFO 64'}),
        }


class TurmaDisciplinaForm(forms.ModelForm):
    def __init__(self, *args, escola=None, **kwargs):
        super().__init__(*args, **kwargs)
        if escola is not None:
            self.fields['disciplina'].queryset = (
                Disciplina.objects.filter(escola=escola).order_by('nome')
            )
            self.fields['professor'].queryset = (
                Professor.objects.filter(escola=escola).order_by('nome')
            )
        else:
            self.fields['disciplina'].queryset = Disciplina.objects.none()
            self.fields['professor'].queryset = Professor.objects.none()

    class Meta:
        model = TurmaDisciplina
        fields = ['disciplina', 'professor', 'aulas_semanais']
        widgets = {
            'aulas_semanais': forms.NumberInput(attrs={'min': 1, 'max': 20}),
        }
        labels = {
            'aulas_semanais': 'Aulas por semana',
        }



DIAS_CHOICES = [
    (0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'), (3, 'Quinta'), (4, 'Sexta'),
]


class SlotBulkForm(forms.Form):
    """Formulário para criar slots em lote para uma escola."""
    turno = forms.ChoiceField(
        choices=[
            ('manha', 'Manhã'),
            ('tarde', 'Tarde'),
            ('vespertino', 'Vespertino'),
            ('noturno', 'Noturno'),
        ],
        label='Turno',
    )
    num_aulas = forms.IntegerField(
        min_value=1, max_value=10, initial=4,
        label='Quantidade de aulas por dia',
    )
    dias = forms.MultipleChoiceField(
        choices=DIAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        initial=[0, 1, 2, 3, 4],
        label='Dias da semana',
    )
