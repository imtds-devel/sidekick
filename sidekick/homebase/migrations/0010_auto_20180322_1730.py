# Generated by Django 2.0 on 2018-03-23 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homebase', '0009_auto_20180320_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifySources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('e', 'email'), ('s', 'Slack'), ('t', 'Text Message')], default='e', max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='emailsubscriptions',
            name='netid',
        ),
        migrations.RemoveField(
            model_name='subscriptions',
            name='netid',
        ),
        migrations.AddField(
            model_name='employees',
            name='notify_level',
            field=models.IntegerField(default=2),
        ),
        migrations.DeleteModel(
            name='EmailSubscriptions',
        ),
        migrations.DeleteModel(
            name='Subscriptions',
        ),
        migrations.AddField(
            model_name='notifysources',
            name='netid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homebase.Employees'),
        ),
    ]
