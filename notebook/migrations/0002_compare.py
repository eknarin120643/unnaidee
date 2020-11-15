# Generated by Django 3.1.1 on 2020-11-15 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allstar', models.FloatField()),
                ('notebook', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notebook.notebook')),
            ],
        ),
    ]
