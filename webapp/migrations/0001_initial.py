# Generated by Django 4.2.3 on 2023-08-01 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone_number', models.IntegerField(blank=True)),
                ('roles', models.CharField(choices=[('Vendor', 'Vendor'), ('AreaMgr', 'AreaMgr'), ('Manager', 'Manager'), ('Admin', 'Admin')], max_length=50, null=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
