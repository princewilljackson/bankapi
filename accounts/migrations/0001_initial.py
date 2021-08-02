# Generated by Django 3.2.5 on 2021-07-30 15:27

import accounts.models
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
                ('passport', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('phone', models.CharField(max_length=50)),
                ('account_number', models.CharField(default=accounts.models.random_account, max_length=200, unique=True)),
                ('available_bal', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Dormant', 'Dormant'), ('Deactivated', 'Deactivated')], default='Active', max_length=11, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UpdateUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('valid_ID_frontview', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('valid_ID_backview', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('next_of_kin', models.CharField(max_length=100)),
                ('relationship_nok', models.CharField(max_length=50)),
                ('phone_nok', models.CharField(max_length=50)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Data',
            },
        ),
        migrations.CreateModel(
            name='PendingTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('transfer_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('transfer_date', models.DateField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pendingtransfers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pending Transfers',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('transaction_type', models.CharField(blank=True, choices=[('Withdraw', 'Withdrawal'), ('Deposit', 'Deposit')], default='Deposit', max_length=11, null=True)),
                ('transaction_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('transaction_description', models.CharField(blank=True, max_length=100, null=True)),
                ('transaction_date', models.DateField()),
                ('transaction_id', models.CharField(default=accounts.models.transaction_id, max_length=200, unique=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Transaction History',
            },
        ),
    ]
