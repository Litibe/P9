# Generated by Django 3.2.7 on 2021-10-25 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20211005_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, max_length=8192, null=True, verbose_name='Commentaire'),
        ),
        migrations.AlterField(
            model_name='review',
            name='headline',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Titre de Critique'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Titre du Ticket'),
        ),
    ]
