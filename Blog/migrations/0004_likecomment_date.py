# Generated by Django 3.0.1 on 2020-01-10 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_user_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='likecomment',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
