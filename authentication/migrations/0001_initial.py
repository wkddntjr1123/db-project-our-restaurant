# Generated by Django 3.2.9 on 2021-12-01 01:45

import authentication.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=10)),
                ('nickname', models.CharField(max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='manager', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group',
            },
        ),
        migrations.CreateModel(
            name='GroupAndMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('accept', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_and_group',
            },
        ),
    ]
