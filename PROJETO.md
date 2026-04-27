# TCC — Sistema de Geração de Horários Escolares

## Visão Geral

Aplicação Django para geração automática de grades horárias escolares. Resolve o problema de criação de horários compatíveis com a disponibilidade de professores, usando um algoritmo de backtracking com reinício aleatório (CSP — Constraint Satisfaction Problem).

**Stack**: Python 3, Django 6, PostgreSQL  
**Banco**: `tccdb` em localhost:5432  
**App principal**: `TCC_BACKEND/core/`

---

## Estrutura de Arquivos

```
TCC/
└── TCC_BACKEND/
    ├── manage.py
    ├── requirements.txt
    ├── TCC/
    │   ├── settings.py          — configurações Django (DEBUG=True, credenciais expostas)
    │   └── urls.py              — roteamento raiz
    └── core/
        ├── models.py            — 8 modelos do banco de dados
        ├── views.py             — 1 view: grade_turma
        ├── urls.py              — rota: grade/<turma_id>/
        ├── admin.py             — todos os modelos registrados no admin
        ├── algoritimos/
        │   └── gerar_horario.py — algoritmo de backtracking
        ├── services/
        │   └── seed_escola.py   — carga inicial de dados da escola real
        ├── templatetags/
        │   └── dict_extras.py   — filtro get_item para templates
        └── templates/core/
            └── grade.html       — grade de horários com cores por disciplina
```

---

## Modelos de Dados

```
Escola
 └── Turma (escola FK, turno: "noturno"/"vespertino")
 │    └── TurmaDisciplina (turma FK, disciplina FK, professor FK, aulas_semanais)
 │         └── Aula (slot FK, turma_disciplina FK)  ← resultado do algoritmo
 └── Slot (escola FK, dia_semana 0-4, numero_aula 1-N, turno)

Professor (nome, carga_maxima_semana)
 └── DisponibilidadeProfessor (professor FK, dia_semana, numero_aula)
     — unique_together: (professor, dia_semana, numero_aula)
     — se não houver registros para um professor, assume disponível sempre

Disciplina (nome)
```

---

## Algoritmo — `gerar_horario_baseado_professor(escola_id)`

**Estratégia**: Backtracking recursivo com Random Restart

1. Carrega todos os Slots, TurmaDisciplinas e disponibilidades do banco
2. Verifica viabilidade: `aulas_necessárias ≤ min(total_slots, carga_maxima_semana)`
3. Ordena professores por carga decrescente (heurística MRV)
4. Expande cada TurmaDisciplina em N tarefas individuais (N = aulas_semanais)
5. Loop de até `max_rodadas=10`, cada uma com até `max_por_rodada=500.000` tentativas:
   - Embaralha slots aleatoriamente
   - Backtracking: para cada tarefa, testa slots válidos em ordem aleatória
   - Restrições verificadas em memória: turno compatível, professor livre, turma livre, carga do professor, disponibilidade
6. Ao encontrar solução: salva todas as Aulas em `transaction.atomic()`

---

## Dados de Teste (seed_escola.py)

Dados reais da **Escola Trilhas de Futuro**:
- **16 professores** (Enfermagem/Radiologia/Informática/Agropecuária)
- **34 disciplinas** (técnicas dos cursos)
- **10 turmas**: ENF P26, ENF 63, RAD 55, RAD 65, INFO 52, INFO 53/54, INFO 64, AGRO 51, AGRO 61, AGRO 62
- **Turnos**: noturno (9 turmas) e vespertino (1 turma — INFO 52)
- **Slots**: 4 aulas/dia × 5 dias × 2 turnos = 40 slots
- **54 relações** turma-disciplina-professor com cargas reais

---

## View e Template

**`grade_turma(request, turma_id)`** — renderiza a grade de uma turma  
- Busca aulas alocadas para a turma
- Monta matriz 2D: linhas = número da aula, colunas = dia da semana
- Passa mapa de cores por disciplina para o template

**Template `grade.html`**:
- Header com nome da escola, turma e turno
- Nav com links para todas as turmas da escola
- Tabela com células coloridas por disciplina (cor definida no `CORES_DISCIPLINA` em views.py)

---

## Estado Atual

- [x] Modelos e migrações funcionando
- [x] Algoritmo de geração implementado
- [x] Seed com dados reais testado com resultado positivo
- [x] View de visualização da grade
- [x] Admin configurado para todos os modelos
- [x] Interface de entrada de dados pelo usuário (CRUD completo)
- [x] Acionamento do algoritmo pela interface web
- [x] Gestão de Slots pela UI (criar em lote por turno/dias, excluir por turno)
- [x] Disponibilidade de professor (grade de checkboxes dia × aula)
- [x] Campo `max_aulas_consecutivas` no modelo Professor
- [x] Restrições de aulas consecutivas no algoritmo
- [x] Prevenção de brechas de horário para turmas no algoritmo
- [x] Exportação em PDF (WeasyPrint, A4 landscape)
- [ ] Interface para edição manual da grade

---

## Próximos Passos Planejados

1. Interface para edição manual da grade (arrastar/soltar aulas)
2. Autenticação de usuários (`@login_required`)
3. Melhorias visuais no dashboard e páginas de detalhe

---

## Problemas Identificados (ver RELATORIO.md para detalhes)

- Código de diagnóstico executando em escopo de módulo em `gerar_horario.py` (bug crítico)
- Verificação de disponibilidade com lógica global incorreta
- Verificação de viabilidade ignora turnos
- `CORES_DISCIPLINA` não corresponde às disciplinas do seed
- Credenciais e SECRET_KEY expostos no settings.py
- Sem autenticação de usuário
