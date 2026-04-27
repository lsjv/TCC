# Relatório de Análise de Código — TCC Geração de Horários

> Problemas identificados e sugestões. **Nenhuma alteração foi feita no código.**

---

## BUGS CRÍTICOS

### 1. Código de diagnóstico executando em escopo de módulo (`gerar_horario.py`, linhas 11–34)

**O problema**: As linhas 11 a 34 do arquivo `gerar_horario.py` ficam fora de qualquer função. Isso significa que toda vez que o módulo for importado (ex: `from core.algoritimos import gerar_horario`), essas linhas executam automaticamente: consultam o banco de dados, imprimem no console e podem lançar erros.

```python
# Estas linhas estão no escopo do módulo — executam no import!
slots_noturno = Slot.objects.filter(escola_id=2, turno="noturno").count()
slots_vespertino = Slot.objects.filter(escola_id=2, turno="vespertino").count()
...
```

Além disso, o `escola_id=2` está hardcoded — vai quebrar em outro ambiente.

**Sugestão**: Mover esse bloco para dentro de uma função `diagnostico_escola(escola_id)` separada, ou simplesmente removê-lo (era claramente código de debug temporário).

---

### 2. Lógica de disponibilidade de professores é global, não individual (`gerar_horario.py`, linha 149)

**O problema**: A verificação de disponibilidade funciona assim:

```python
if disponibilidades:  # Se QUALQUER professor tiver registro...
    if (rel.professor.id, slot.dia_semana, slot.numero_aula) not in disponibilidades:
        return False  # ...todos os professores sem registro são bloqueados
```

Se você cadastrar disponibilidade para apenas 1 professor, todos os outros passam a ser tratados como "sem disponibilidade em lugar nenhum", pois `disponibilidades` estará preenchido e nenhum outro professor terá entradas nesse conjunto.

**Sugestão**: Criar um dicionário por professor: `disponibilidades_por_prof[professor_id] = set(...)`. Então verificar apenas se aquele professor específico tem registros:

```python
disp_prof = disponibilidades_por_prof.get(rel.professor.id)
if disp_prof is not None:
    if (slot.dia_semana, slot.numero_aula) not in disp_prof:
        return False
```

---

### 3. Verificação de viabilidade ignora o turno do professor (`gerar_horario.py`, linhas 79–88)

**O problema**: O limite de viabilidade usa `total_slots` — o total de slots da escola (noturno + vespertino juntos). Um professor noturno tem no máximo 20 slots disponíveis (4 aulas × 5 dias), não 40.

```python
limite = min(total_slots, prof.carga_maxima_semana)  # total_slots = 40 (errado)
```

Se a carga de um professor noturno for 22, o sistema diz "OK: 22 ≤ 40", mas o algoritmo vai falhar em tempo de execução tentando alocar 22 aulas em 20 slots noturno.

**Sugestão**: Calcular `slots_por_turno` separadamente e usar o turno das turmas do professor para determinar o limite correto.

---

## PROBLEMAS FUNCIONAIS

### 4. Dupla importação de módulos (`gerar_horario.py`, linhas 6–9)

```python
from collections import defaultdict  # linha 6
import random
import time
from collections import defaultdict  # linha 9 — duplicado!
from core.models import TurmaDisciplina, Slot  # linha 9 — duplicado com linha 2!
```

Não causa erro, mas é código desnecessário que indica o arquivo foi editado de forma desorganizada.

**Sugestão**: Limpar os imports, deixando cada um apenas uma vez no topo do arquivo.

---

### 5. `CORES_DISCIPLINA` não corresponde às disciplinas do seed (`views.py`, linhas 4–13)

**O problema**: O mapa de cores define disciplinas como "Matemática", "Língua Portuguesa", "História" — mas as disciplinas cadastradas no seed são como "Anatomia e Fisio. Humana", "Redes de Computadores", "Avicultura", etc. Nenhuma corresponde.

Resultado: todas as células da grade são renderizadas sem cor (cor padrão/branco), pois nenhuma disciplina encontra match no dicionário.

**Sugestão**: Atualizar `CORES_DISCIPLINA` com as disciplinas reais do projeto, ou — melhor ainda — armazenar a cor diretamente no modelo `Disciplina` (campo `cor` ou `cor_bg` + `cor_border`), tornando o sistema dinâmico para qualquer disciplina cadastrada.

---

### 6. Seed usa `get_or_create` sem atualizar dados existentes (`seed_escola.py`)

**O problema**: Em `TurmaDisciplina.objects.get_or_create(...)`, o campo `aulas_semanais` está em `defaults`. Se o registro já existir (ao rodar a seed pela segunda vez), o `aulas_semanais` não é atualizado.

```python
TurmaDisciplina.objects.get_or_create(
    turma=turma, disciplina=disciplina, professor=professor,
    defaults={'aulas_semanais': aulas}  # ignorado se o registro já existe
)
```

**Sugestão**: Usar `update_or_create` em vez de `get_or_create`, ou adicionar `update_fields` para os casos de reruns.

---

### 7. A constraint `unique_together` de `Aula` não impede turma com duas disciplinas no mesmo slot

**O problema**: `unique_together = ('slot', 'turma_disciplina')` evita duplicar exatamente a mesma aula, mas não impede que a mesma turma tenha duas disciplinas diferentes no mesmo slot (dois `turma_disciplina` diferentes, mesmo turma, mesmo slot).

O algoritmo verifica isso em memória via `ocupado_turma`, mas o banco de dados não impõe essa restrição. Se alguém inserir dados manualmente via admin ou API, pode criar conflito.

**Sugestão**: Adicionar constraint a nível de banco com `unique_together = ('slot', 'turma_disciplina__turma')` — mas como FK transitiva não é suportada diretamente, a solução seria adicionar uma coluna `turma` direto em `Aula` ou usar uma `constraint` customizada com `UniqueConstraint`.

---

### 8. View não filtra slots por turno da turma (`views.py`, linha 19)

**O problema**: `numeros_aula` é obtido de todos os slots da escola sem filtrar por turno. Se os turnos tiverem números de aula diferentes (ex: manhã tem aulas 1–5, noite tem 1–4), a grade de uma turma noturna mostraria linhas extras vazias.

```python
numeros_aula = sorted(
    Slot.objects.filter(escola=turma.escola)  # sem filtro de turno!
    .values_list('numero_aula', flat=True).distinct()
)
```

**Sugestão**: Adicionar `.filter(turno=turma.turno)` ao queryset.

---

## PROBLEMAS DE SEGURANÇA/CONFIGURAÇÃO

### 9. `SECRET_KEY` e credenciais do banco expostos no `settings.py`

**O problema**: A chave secreta do Django e as credenciais do banco estão hardcoded no código-fonte.

```python
SECRET_KEY = 'django-insecure-nc$jobr-...'
DATABASES = { 'PASSWORD': 'Tcc12345', ... }
```

**Sugestão**: Usar variáveis de ambiente (biblioteca `python-decouple` ou `os.environ`) para armazenar esses valores, e não comitar o arquivo `.env` no git.

---

### 10. Sem autenticação de usuário

O sistema não tem login. Qualquer pessoa com acesso à URL pode ver as grades. O admin do Django requer senha, mas a view pública `/grade/<id>/` não.

**Sugestão**: Dependendo do escopo do TCC, adicionar `@login_required` na view é suficiente. Deixar para um passo posterior junto com a funcionalidade de entrada de dados.

---

### 11. `ALLOWED_HOSTS = []` e `DEBUG = True`

Em produção, `ALLOWED_HOSTS` vazio faz Django rejeitar todas as requisições com `400 Bad Request`. `DEBUG = True` expõe rastreamentos de erro completos.

**Sugestão**: Para apresentação/deploy, configurar `ALLOWED_HOSTS = ['*']` ou o domínio específico, e `DEBUG = False`.

---

## SOBRE OS PRÓXIMOS PASSOS

### Restrições de disponibilidade por professor (Próximo Passo 1)
- **Status**: Modelo `DisponibilidadeProfessor` já existe com a estrutura correta
- **O que falta**: Interface web para cadastrar e editar disponibilidades
- **Bloqueador**: O bug #2 (lógica global) precisa ser corrigido antes, senão a funcionalidade vai quebrar o algoritmo

### Restrições de aulas consecutivas (Próximo Passo 2)
- **Status**: Não implementado em lugar nenhum
- **O que falta**: Adicionar verificação no `pode_alocar` considerando os slots adjacentes já alocados para aquele professor
- **Complexidade**: Média — requer rastrear sequências de aulas por dia/professor no estado do backtracking

### Evitar brechas no horário (Próximo Passo 3)
- **Status**: Não implementado
- **O que falta**: Semelhante ao item anterior, mas verificando brechas para uma turma (não um professor) ao longo do dia
- **Complexidade**: Média-alta — pode aumentar significativamente o tempo do algoritmo

### Edição/criação manual da grade (Próximo Passo 4)
- **Status**: Apenas visualização está feita
- **O que falta**: Views de edição, formulários Django ou interface JS para arrastar aulas
- **Complexidade**: Alta — envolve criar UI completa e lógica de validação de conflitos em tempo real

### Entrada de dados pelo usuário (Próximo Passo 5)
- **Status**: Apenas seed hardcoded
- **O que falta**: Views CRUD completas para Escola, Professor, Disciplina, Turma, TurmaDisciplina, Slots
- **Complexidade**: Alta — é praticamente a metade do sistema que ainda não existe

### Exportação em PDF (Próximo Passo 6)
- **Status**: Não implementado
- **Sugestão técnica**: Biblioteca `reportlab` ou `weasyprint` para gerar PDF a partir do HTML da grade já existente
- **Complexidade**: Baixa-média — pode reaproveitar o template HTML

---

## Ordem de Correção Recomendada

1. **Agora** (antes de qualquer nova feature): corrigir bugs #1, #2, #3 e #4 — são críticos e simples
2. **Antes de mostrar para usuários**: corrigir #5 (cores) e #8 (filtro de turno na view)
3. **No próximo ciclo de desenvolvimento**: implementar entrada de dados (#5 do roadmap) — habilita todos os outros
4. **Junto com disponibilidade**: corrigir #2 definitivamente e criar a UI de disponibilidade
5. **Por último**: PDF (mais simples tecnicamente e depende dos dados estarem certos)
