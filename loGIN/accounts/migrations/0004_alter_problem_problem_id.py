# Generated by Django 4.0.5 on 2022-07-08 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='problem_id',
            field=models.BigAutoField(db_column='Problem ID', primary_key=True, serialize=False),
        ),
    ]
