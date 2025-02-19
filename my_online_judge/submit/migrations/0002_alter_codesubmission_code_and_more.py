# Generated by Django 5.1 on 2024-08-24 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codesubmission',
            name='code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='codesubmission',
            name='language',
            field=models.CharField(blank=True, choices=[('py', 'Python'), ('c', 'C'), ('cpp', 'C++')], max_length=10, null=True),
        ),
    ]
