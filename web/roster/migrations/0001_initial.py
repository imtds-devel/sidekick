# Generated by Django 2.0 on 2018-04-26 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homebase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(default='')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(default='')),
                ('val', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('about', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disc_about', to='homebase.Employees')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disc_poster', to='homebase.Employees')),
            ],
        ),
        migrations.CreateModel(
            name='Proficiencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic', models.IntegerField(default=0)),
                ('advanced', models.IntegerField(default=0)),
                ('field', models.IntegerField(default=0)),
                ('printer', models.IntegerField(default=0)),
                ('network', models.IntegerField(default=0)),
                ('mobile', models.IntegerField(default=0)),
                ('refresh', models.IntegerField(default=0)),
                ('software', models.IntegerField(default=0)),
                ('netid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees')),
            ],
        ),
        migrations.CreateModel(
            name='Trophies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(default='')),
                ('name', models.TextField(default='')),
                ('trophy_type', models.CharField(choices=[('bdg', 'Badge'), ('udb', 'Under the Bus'), ('str', 'Star'), ('hst', 'Half-Star'), ('pst', 'Puzzle Star')], default='', max_length=3)),
                ('icon', models.CharField(default='', max_length=30)),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trophyGiver', to='homebase.Employees')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trophyRecipient', to='homebase.Employees')),
            ],
        ),
    ]
