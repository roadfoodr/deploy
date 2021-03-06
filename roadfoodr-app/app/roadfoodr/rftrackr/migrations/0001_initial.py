# Generated by Django 2.2.4 on 2019-10-20 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Roadfood',
            fields=[
                ('rf_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name_first', models.CharField(max_length=40)),
                ('name_last', models.CharField(max_length=40)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('visit_id', models.AutoField(primary_key=True, serialize=False)),
                ('visit_date', models.DateTimeField(verbose_name='date visited')),
                ('rf_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rftrackr.Roadfood')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rftrackr.User')),
            ],
        ),
    ]
