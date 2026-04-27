from collections import defaultdict
<<<<<<< HEAD
from core.models import Escola, Professor, Disciplina, Turma, TurmaDisciplina, Slot

# Paleta de 12 cores, atribuída em ciclo às disciplinas
_PALETA = [
    ("#EEEDFE", "#534AB7", "#3C3489"),  # roxo
    ("#E1F5EE", "#0F6E56", "#085041"),  # verde
    ("#FAEEDA", "#854F0B", "#633806"),  # âmbar
    ("#FAECE7", "#993C1D", "#712B13"),  # terracota
    ("#EAF3DE", "#3B6D11", "#27500A"),  # lima
    ("#E6F1FB", "#185FA5", "#0C447C"),  # azul
    ("#FBEAF0", "#993556", "#72243E"),  # rosa
    ("#F1EFE8", "#5F5E5A", "#444441"),  # cinza
    ("#FFF8E1", "#C77700", "#8B5200"),  # amarelo
    ("#E8F5E9", "#2E7D32", "#1B5E20"),  # verde escuro
    ("#E3F2FD", "#0D47A1", "#01579B"),  # azul escuro
    ("#FCE4EC", "#AD1457", "#880E4F"),  # pink
]
=======
from core.models import (
    Escola,
    Professor,
    Disciplina,
    Turma,
    TurmaDisciplina,
    Slot
)
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae


def seed():

    print("Criando escola...")
    escola, _ = Escola.objects.get_or_create(nome="Escola Trilhas de Futuro")

    # ================================================================
<<<<<<< HEAD
    # PROFESSORES
    # ================================================================
    print("Criando professores...")
    professores_data = {
=======
    # PROFESSORES com carga real extraída dos horários
    # ================================================================
    print("Criando professores...")
    professores_data = {
        # Enfermagem / Radiologia
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
        "HELENITA":  20,
        "DANIELA":   20,
        "MÍRIAN":    20,
        "RAFAEL":    20,
        "GEISE":     20,
        "INGRED":    20,
        "ROBERTA":   20,
        "ANA JÚLIA": 20,
<<<<<<< HEAD
=======
        # Informática
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
        "VILELA":    20,
        "PEDRO":     20,
        "THARLES":   20,
        "ANDRÉ":     20,
<<<<<<< HEAD
=======
        # Agropecuária
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
        "BRUNO":     20,
        "ARTHUR":    20,
        "SAMUEL":    20,
        "MIRELLE":   20,
    }

    for nome, carga in professores_data.items():
        Professor.objects.get_or_create(
            nome=nome,
            escola=escola,
            defaults={'carga_maxima_semana': carga}
        )

    # ================================================================
<<<<<<< HEAD
    # DISCIPLINAS — cor atribuída em ciclo pela posição na lista
    # ================================================================
    print("Criando disciplinas...")
    disciplinas_nomes = [
=======
    # DISCIPLINAS
    # ================================================================
    print("Criando disciplinas...")
    disciplinas_data = [
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
        # Enfermagem P26
        "Assis. a Cli./Pac. em Trat. Cir.",
        "Assistência em Saúde Coletiva",
        "Assis. a Cli./Pac. em Trat. Clí.",
        "Fund. Org. Pr. de Trab. em Enf. I",
        "Assist. à Criança e à Mulher",
        "Assistência em Saúde Mental",
        # Enfermagem 63
        "Anatomia e Fisio. Humana",
        "Educação para o Autocuidado",
        "Pro. da Saúd. e Seg. no Trab.",
        "Prestação de Primeiros Socorros",
        "Org. do Pr. de Trab. em Saúde",
        # Radiologia 55
        "Noções de Radioterapia",
        "Gestão de Serviços Radiológicos",
        "Met. Projeto Conclusão Curso",
        "Radiologia Odontológica",
        "Ressonância Magnética",
        "Tomografia Computadorizada",
        "Incid.as Radiográficas Especiais",
        "Mamografia",
        # Radiologia 65
        "Bios. nas Ações de Saúde",
        "Anat. e Fisiol. H. Apl. à Rad.",
        "Fund. de Enf. Apli. à Radi.",
        "Psi. das Relações Humanas",
        "Hig. Profil. e Orien. p/ o Autocuid.",
        "Primeiros Socorros",
        "Prom. de Saú. e Seg. no Trab.",
        # Informática
        "Redes de Computadores",
        "Prog. de computadores II",
        "Desenv. de Softwares III",
        "Aná. e Proj. de Sist. II",
        "Gestão de Sist. Ope. III",
        "Aplicativos para Internet",
        "Gestão de Sistemas Operacionais I",
        "Operação de Softwares Aplicativos I",
        "Desenvolvimentos de Softwares I",
        "Lógica de Programação",
        "Inst. e Manut. de Computadores I",
        "Ling. Tecn. e Trabalho",
        "Organização Empresarial",
        # Agropecuária
        "Avicultura",
        "Bovinocultura",
        "Zootecnia Geral",
        "Suinocultura",
        "Climatologia",
        "Fruticultura",
        "Forragicultura",
        "Solos",
        "Culturas Anuais",
        "Informática Aplicada",
    ]

<<<<<<< HEAD
    for i, nome in enumerate(disciplinas_nomes):
        cor_bg, cor_borda, cor_texto = _PALETA[i % len(_PALETA)]
        Disciplina.objects.update_or_create(
            nome=nome,
            escola=escola,
            defaults={
                'cor_bg':    cor_bg,
                'cor_borda': cor_borda,
                'cor_texto': cor_texto,
            }
        )
=======
    for nome in disciplinas_data:
        Disciplina.objects.get_or_create(nome=nome)
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae

    # ================================================================
    # TURMAS
    # ================================================================
    print("Criando turmas...")
    turmas_data = [
<<<<<<< HEAD
        ("ENF P26 - Mod II",     "noturno"),
        ("ENF 63 - Mod I",       "noturno"),
        ("RAD 55 - Mod III",     "noturno"),
        ("RAD 65 - Mod I",       "noturno"),
        ("INFO 52 - Mod III",    "vespertino"),
        ("INFO 53/54 - Mod III", "noturno"),
        ("INFO 64 - Mod I",      "noturno"),
        ("AGRO 51 - Mod III",    "noturno"),
        ("AGRO 61 - Mod I",      "noturno"),
        ("AGRO 62 - Mod I",      "noturno"),
=======
        ("ENF P26 - Mod II", "noturno"),
        ("ENF 63 - Mod I",   "noturno"),
        ("RAD 55 - Mod III", "noturno"),
        ("RAD 65 - Mod I",   "noturno"),
        ("INFO 52 - Mod III","vespertino"),
        ("INFO 53/54 - Mod III", "noturno"),
        ("INFO 64 - Mod I",  "noturno"),
        ("AGRO 51 - Mod III","noturno"),
        ("AGRO 61 - Mod I",  "noturno"),
        ("AGRO 62 - Mod I",  "noturno"),
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
    ]

    for nome, turno in turmas_data:
        Turma.objects.get_or_create(
            nome=nome,
            escola=escola,
            defaults={'turno': turno}
        )

    # ================================================================
<<<<<<< HEAD
    # SLOTS — 4 aulas por dia × 5 dias × 2 turnos
=======
    # SLOTS — 4 aulas por dia (2 antes + 2 depois do intervalo)
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
    # ================================================================
    print("Criando slots...")
    for turno in ["noturno", "vespertino"]:
        for dia in range(5):
<<<<<<< HEAD
            for aula in range(1, 5):
=======
            for aula in range(1, 5):  # 4 aulas por dia
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
                Slot.objects.get_or_create(
                    escola=escola,
                    dia_semana=dia,
                    numero_aula=aula,
                    turno=turno
                )

    # ================================================================
<<<<<<< HEAD
    # RELAÇÕES TURMA-DISCIPLINA
    # ================================================================
    print("Criando relações turma-disciplina...")

    relacoes = [
        # ── ENF P26 – Módulo II ──────────────────────────────────────
        ("ENF P26 - Mod II", "Assis. a Cli./Pac. em Trat. Cir.",  "HELENITA", 4),
        ("ENF P26 - Mod II", "Assistência em Saúde Coletiva",      "DANIELA",  2),
        ("ENF P26 - Mod II", "Assis. a Cli./Pac. em Trat. Clí.",  "HELENITA", 4),
        ("ENF P26 - Mod II", "Fund. Org. Pr. de Trab. em Enf. I", "MÍRIAN",   4),
        ("ENF P26 - Mod II", "Assist. à Criança e à Mulher",       "DANIELA",  4),
        ("ENF P26 - Mod II", "Assistência em Saúde Mental",        "DANIELA",  2),

        # ── ENF 63 – Módulo I ────────────────────────────────────────
        ("ENF 63 - Mod I", "Anatomia e Fisio. Humana",        "RAFAEL",  4),
        ("ENF 63 - Mod I", "Educação para o Autocuidado",     "MÍRIAN",  4),
        ("ENF 63 - Mod I", "Pro. da Saúd. e Seg. no Trab.",   "DANIELA", 4),
        ("ENF 63 - Mod I", "Prestação de Primeiros Socorros", "MÍRIAN",  4),
        ("ENF 63 - Mod I", "Org. do Pr. de Trab. em Saúde",   "DANIELA", 4),

        # ── RAD 55 – Módulo III ──────────────────────────────────────
        ("RAD 55 - Mod III", "Noções de Radioterapia",           "INGRED",  2),
        ("RAD 55 - Mod III", "Gestão de Serviços Radiológicos",  "GEISE",   2),
        ("RAD 55 - Mod III", "Met. Projeto Conclusão Curso",     "RAFAEL",  4),
        ("RAD 55 - Mod III", "Radiologia Odontológica",          "ROBERTA", 2),
        ("RAD 55 - Mod III", "Ressonância Magnética",            "GEISE",   2),
        ("RAD 55 - Mod III", "Tomografia Computadorizada",       "INGRED",  4),
        ("RAD 55 - Mod III", "Incid.as Radiográficas Especiais", "INGRED",  2),
        ("RAD 55 - Mod III", "Mamografia",                       "GEISE",   2),

        # ── RAD 65 – Módulo I ────────────────────────────────────────
        ("RAD 65 - Mod I", "Bios. nas Ações de Saúde",             "MÍRIAN",    2),
        ("RAD 65 - Mod I", "Anat. e Fisiol. H. Apl. à Rad.",       "INGRED",    4),
        ("RAD 65 - Mod I", "Fund. de Enf. Apli. à Radi.",          "DANIELA",   2),
        ("RAD 65 - Mod I", "Psi. das Relações Humanas",            "ANA JÚLIA", 2),
        ("RAD 65 - Mod I", "Hig. Profil. e Orien. p/ o Autocuid.","HELENITA",  4),
        ("RAD 65 - Mod I", "Primeiros Socorros",                   "MÍRIAN",    2),
        ("RAD 65 - Mod I", "Prom. de Saú. e Seg. no Trab.",       "MÍRIAN",    4),

        # ── INFO 52 – Módulo III – Vespertino ────────────────────────
        ("INFO 52 - Mod III", "Redes de Computadores",        "VILELA", 4),
        ("INFO 52 - Mod III", "Prog. de computadores II",     "PEDRO",  4),
        ("INFO 52 - Mod III", "Desenv. de Softwares III",     "PEDRO",  2),
        ("INFO 52 - Mod III", "Aná. e Proj. de Sist. II",     "VILELA", 2),
        ("INFO 52 - Mod III", "Gestão de Sist. Ope. III",     "VILELA", 4),
        ("INFO 52 - Mod III", "Aplicativos para Internet",    "VILELA", 2),
        ("INFO 52 - Mod III", "Met. Projeto Conclusão Curso", "RAFAEL", 2),

        # ── INFO 53/54 – Módulo III – Noturno ───────────────────────
        ("INFO 53/54 - Mod III", "Prog. de computadores II",     "PEDRO",   2),
        ("INFO 53/54 - Mod III", "Met. Projeto Conclusão Curso", "RAFAEL",  4),
        ("INFO 53/54 - Mod III", "Desenv. de Softwares III",     "PEDRO",   2),
        ("INFO 53/54 - Mod III", "Gestão de Sist. Ope. III",     "VILELA",  4),
        ("INFO 53/54 - Mod III", "Redes de Computadores",        "THARLES", 4),
        ("INFO 53/54 - Mod III", "Aplicativos para Internet",    "THARLES", 2),
        ("INFO 53/54 - Mod III", "Aná. e Proj. de Sist. II",     "VILELA",  2),

        # ── INFO 64 – Módulo I ───────────────────────────────────────
        ("INFO 64 - Mod I", "Organização Empresarial",             "ANDRÉ",   2),
        ("INFO 64 - Mod I", "Lógica de Programação",               "PEDRO",   4),
        ("INFO 64 - Mod I", "Gestão de Sistemas Operacionais I",   "VILELA",  4),
        ("INFO 64 - Mod I", "Operação de Softwares Aplicativos I", "VILELA",  2),
        ("INFO 64 - Mod I", "Desenvolvimentos de Softwares I",     "PEDRO",   2),
        ("INFO 64 - Mod I", "Inst. e Manut. de Computadores I",    "THARLES", 4),
        ("INFO 64 - Mod I", "Ling. Tecn. e Trabalho",              "ANDRÉ",   2),

        # ── AGRO 51 – Módulo III ─────────────────────────────────────
        ("AGRO 51 - Mod III", "Avicultura",                  "BRUNO",  4),
        ("AGRO 51 - Mod III", "Bovinocultura",               "SAMUEL", 4),
        ("AGRO 51 - Mod III", "Zootecnia Geral",             "BRUNO",  4),
        ("AGRO 51 - Mod III", "Suinocultura",                "BRUNO",  4),
        ("AGRO 51 - Mod III", "Met. Projeto Conclusão Curso","RAFAEL", 4),

        # ── AGRO 61 – Módulo I ───────────────────────────────────────
        ("AGRO 61 - Mod I", "Climatologia",       "ARTHUR",  4),
        ("AGRO 61 - Mod I", "Fruticultura",       "SAMUEL",  4),
        ("AGRO 61 - Mod I", "Forragicultura",     "BRUNO",   4),
        ("AGRO 61 - Mod I", "Solos",              "ARTHUR",  4),
        ("AGRO 61 - Mod I", "Informática Aplicada","ANDRÉ",  2),
        ("AGRO 61 - Mod I", "Culturas Anuais",    "MIRELLE", 2),

        # ── AGRO 62 – Módulo I ───────────────────────────────────────
        ("AGRO 62 - Mod I", "Fruticultura",        "SAMUEL",  4),
        ("AGRO 62 - Mod I", "Climatologia",        "ARTHUR",  4),
        ("AGRO 62 - Mod I", "Forragicultura",      "BRUNO",   4),
        ("AGRO 62 - Mod I", "Solos",               "ARTHUR",  4),
        ("AGRO 62 - Mod I", "Informática Aplicada","ANDRÉ",   2),
        ("AGRO 62 - Mod I", "Culturas Anuais",     "MIRELLE", 2),
    ]

    for turma_nome, disc_nome, prof_nome, aulas in relacoes:
        turma      = Turma.objects.get(nome=turma_nome, escola=escola)
        disciplina = Disciplina.objects.get(nome=disc_nome, escola=escola)
        professor  = Professor.objects.get(nome=prof_nome, escola=escola)

        TurmaDisciplina.objects.update_or_create(
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            defaults={'aulas_semanais': aulas}
        )

=======
    # RELAÇÕES TURMA-DISCIPLINA com aulas_semanais reais
    # ================================================================
    print("Criando relações turma-disciplina...")

    # Formato: (turma_nome, disciplina_nome, professor_nome, aulas_semanais)
    relacoes = [

        # ── ENF P26 – Módulo II ──────────────────────────────────────
        ("ENF P26 - Mod II", "Assis. a Cli./Pac. em Trat. Cir.",  "HELENITA", 4),
        ("ENF P26 - Mod II", "Assistência em Saúde Coletiva",      "DANIELA",  4),
        ("ENF P26 - Mod II", "Assis. a Cli./Pac. em Trat. Clí.",  "HELENITA", 4),
        ("ENF P26 - Mod II", "Fund. Org. Pr. de Trab. em Enf. I", "MÍRIAN",   4),
        ("ENF P26 - Mod II", "Assist. à Criança e à Mulher",       "DANIELA",  4),
        ("ENF P26 - Mod II", "Assistência em Saúde Mental",        "DANIELA",  2),
        # total: 22 aulas — ajustar carga_maxima de HELENITA e DANIELA

        # ── ENF 63 – Módulo I ────────────────────────────────────────
        ("ENF 63 - Mod I", "Anatomia e Fisio. Humana",          "RAFAEL",   4),
        ("ENF 63 - Mod I", "Educação para o Autocuidado",       "MÍRIAN",   4),
        ("ENF 63 - Mod I", "Pro. da Saúd. e Seg. no Trab.",     "DANIELA",  4),
        ("ENF 63 - Mod I", "Prestação de Primeiros Socorros",   "MÍRIAN",   4),
        ("ENF 63 - Mod I", "Org. do Pr. de Trab. em Saúde",     "DANIELA",  4),

        # ── RAD 55 – Módulo III ──────────────────────────────────────
        ("RAD 55 - Mod III", "Noções de Radioterapia",              "INGRED",   2),
        ("RAD 55 - Mod III", "Gestão de Serviços Radiológicos",     "GEISE",    2),
        ("RAD 55 - Mod III", "Met. Projeto Conclusão Curso",        "RAFAEL",   4),
        ("RAD 55 - Mod III", "Radiologia Odontológica",             "ROBERTA",  2),
        ("RAD 55 - Mod III", "Ressonância Magnética",               "GEISE",    2),
        ("RAD 55 - Mod III", "Tomografia Computadorizada",          "INGRED",   4),
        ("RAD 55 - Mod III", "Incid.as Radiográficas Especiais",    "INGRED",   2),
        ("RAD 55 - Mod III", "Mamografia",                          "GEISE",    2),

        # ── RAD 65 – Módulo I ────────────────────────────────────────
        ("RAD 65 - Mod I", "Bios. nas Ações de Saúde",              "MÍRIAN",   2),
        ("RAD 65 - Mod I", "Anat. e Fisiol. H. Apl. à Rad.",        "INGRED",   4),
        ("RAD 65 - Mod I", "Fund. de Enf. Apli. à Radi.",           "DANIELA",  2),
        ("RAD 65 - Mod I", "Psi. das Relações Humanas",             "ANA JÚLIA",2),
        ("RAD 65 - Mod I", "Hig. Profil. e Orien. p/ o Autocuid.", "HELENITA", 4),
        ("RAD 65 - Mod I", "Primeiros Socorros",                    "MÍRIAN",   2),
        ("RAD 65 - Mod I", "Prom. de Saú. e Seg. no Trab.",        "MÍRIAN",   4),

        # ── INFO 52 – Módulo III – Vespertino ────────────────────────
        ("INFO 52 - Mod III", "Redes de Computadores",           "VILELA",  4),
        ("INFO 52 - Mod III", "Prog. de computadores II",        "PEDRO",   4),
        ("INFO 52 - Mod III", "Desenv. de Softwares III",        "PEDRO",   2),
        ("INFO 52 - Mod III", "Aná. e Proj. de Sist. II",        "VILELA",  2),
        ("INFO 52 - Mod III", "Gestão de Sist. Ope. III",        "VILELA",  4),
        ("INFO 52 - Mod III", "Aplicativos para Internet",       "VILELA",  2),
        ("INFO 52 - Mod III", "Met. Projeto Conclusão Curso",    "RAFAEL",  2),

        # ── INFO 53/54 – Módulo III – Noturno ───────────────────────
        ("INFO 53/54 - Mod III", "Prog. de computadores II",     "PEDRO",   2),
        ("INFO 53/54 - Mod III", "Met. Projeto Conclusão Curso", "RAFAEL",  4),
        ("INFO 53/54 - Mod III", "Desenv. de Softwares III",     "PEDRO",   2),
        ("INFO 53/54 - Mod III", "Gestão de Sist. Ope. III",     "VILELA",  4),
        ("INFO 53/54 - Mod III", "Redes de Computadores",        "THARLES", 4),
        ("INFO 53/54 - Mod III", "Aplicativos para Internet",    "THARLES", 2),
        ("INFO 53/54 - Mod III", "Aná. e Proj. de Sist. II",     "VILELA",  2),

        # ── INFO 64 – Módulo I ───────────────────────────────────────
        ("INFO 64 - Mod I", "Organização Empresarial",              "ANDRÉ",   4),
        ("INFO 64 - Mod I", "Lógica de Programação",                "PEDRO",   4),
        ("INFO 64 - Mod I", "Gestão de Sistemas Operacionais I",    "VILELA",  4),
        ("INFO 64 - Mod I", "Operação de Softwares Aplicativos I",  "VILELA",  2),
        ("INFO 64 - Mod I", "Desenvolvimentos de Softwares I",      "PEDRO",   4),
        ("INFO 64 - Mod I", "Inst. e Manut. de Computadores I",     "THARLES", 4),
        ("INFO 64 - Mod I", "Ling. Tecn. e Trabalho",               "ANDRÉ",   2),

        # ── AGRO 51 – Módulo III ─────────────────────────────────────
        ("AGRO 51 - Mod III", "Avicultura",                  "BRUNO",  4),
        ("AGRO 51 - Mod III", "Bovinocultura",               "SAMUEL", 4),
        ("AGRO 51 - Mod III", "Zootecnia Geral",             "BRUNO",  4),
        ("AGRO 51 - Mod III", "Suinocultura",                "BRUNO",  4),
        ("AGRO 51 - Mod III", "Met. Projeto Conclusão Curso","RAFAEL", 4),

        # ── AGRO 61 – Módulo I ───────────────────────────────────────
        ("AGRO 61 - Mod I", "Climatologia",                  "ARTHUR", 4),
        ("AGRO 61 - Mod I", "Fruticultura",                  "SAMUEL", 4),
        ("AGRO 61 - Mod I", "Forragicultura",                "BRUNO",  4),
        ("AGRO 61 - Mod I", "Solos",                         "ARTHUR", 4),
        ("AGRO 61 - Mod I", "Informática Aplicada",          "ANDRÉ",  4),
        ("AGRO 61 - Mod I", "Culturas Anuais",               "MIRELLE",2),

        # ── AGRO 62 – Módulo I ───────────────────────────────────────
        ("AGRO 62 - Mod I", "Fruticultura",                  "SAMUEL", 4),
        ("AGRO 62 - Mod I", "Climatologia",                  "ARTHUR", 4),
        ("AGRO 62 - Mod I", "Forragicultura",                "BRUNO",  4),
        ("AGRO 62 - Mod I", "Solos",                         "ARTHUR", 4),
        ("AGRO 62 - Mod I", "Informática Aplicada",          "ANDRÉ",  4),
        ("AGRO 62 - Mod I", "Culturas Anuais",               "MIRELLE",4),
    ]

    for turma_nome, disc_nome, prof_nome, aulas in relacoes:
        turma      = Turma.objects.get(nome=turma_nome, escola=escola)
        disciplina = Disciplina.objects.get(nome=disc_nome)
        professor  = Professor.objects.get(nome=prof_nome)

        TurmaDisciplina.objects.get_or_create(
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            defaults={'aulas_semanais': aulas}
        )

>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
    # ================================================================
    # Atualizar carga_maxima_semana real por professor
    # ================================================================
    print("Ajustando cargas máximas reais...")

    cargas_reais = defaultdict(int)
    for _, _, prof_nome, aulas in relacoes:
        cargas_reais[prof_nome] += aulas

    for prof_nome, carga in cargas_reais.items():
<<<<<<< HEAD
        Professor.objects.filter(nome=prof_nome, escola=escola).update(carga_maxima_semana=carga)
        print(f"  {prof_nome}: {carga} aulas/semana")

    print("\nSeed finalizado!")
=======
        Professor.objects.filter(nome=prof_nome).update(
            carga_maxima_semana=carga
        )
        print(f"  {prof_nome}: {carga} aulas/semana")

    print("\nSeed finalizado!")
>>>>>>> c3281e1759235e30f2b7ac04a4c2296f2ea209ae
