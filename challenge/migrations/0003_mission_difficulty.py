# Generated by Django 4.2.11 on 2024-03-06 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0002_alter_mission_correct_answers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='difficulty',
            field=models.IntegerField(blank=True, choices=[(1, 'آسان'), (2, 'متوسط'), (3, 'سخت')], default=0, null=True, verbose_name='mission difficulty'),
        ),
    ]
