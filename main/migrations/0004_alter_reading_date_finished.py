# Generated by Django 5.0.1 on 2024-03-15 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_bookclub_types_delete_clubtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='date_finished',
            field=models.DateField(null=True),
        ),
    ]
