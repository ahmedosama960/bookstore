# Generated by Django 3.2.3 on 2021-05-26 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_alter_userorder_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]