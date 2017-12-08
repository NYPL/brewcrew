# Generated by Django 2.0 on 2017-12-08 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='locations',
            field=models.ManyToManyField(to='accounts.Location'),
        ),
    ]
