from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_disponibilidadeprofessor_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplina',
            name='cor_bg',
            field=models.CharField(default='#F1EFE8', max_length=7),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='cor_borda',
            field=models.CharField(default='#5F5E5A', max_length=7),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='cor_texto',
            field=models.CharField(default='#444441', max_length=7),
        ),
    ]
