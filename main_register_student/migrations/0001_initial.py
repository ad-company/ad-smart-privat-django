# Generated by Django 2.1.7 on 2020-08-05 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main_register_student.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=250)),
                ('year', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('note', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Paid',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('SD 1-5', 'SD 1-5'), ('SD 6', 'SD 6'), ('SMP 7-8', 'SMP 7-8'), ('SMP 9', 'SMP 9'), ('SMA 10-11', 'SMA 10-11'), ('SMA 12', 'SMA 12')], max_length=250)),
                ('mode', models.CharField(choices=[('online (remote)', 'Online (remote)'), ('offline', 'Offline')], max_length=250)),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Price',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=250)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=2)),
                ('parent_name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=14)),
                ('id_pic', models.ImageField(blank=True, default='uploads/user-no-image.png', null=True, upload_to=main_register_student.models.photo_id, verbose_name='img')),
                ('profile_pic', models.ImageField(blank=True, default='uploads/user-no-image.png', null=True, upload_to=main_register_student.models.photo_profile, verbose_name='img')),
                ('schedule_1', models.CharField(max_length=20)),
                ('schedule_2', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('schedule_3', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('schedule_4', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('schedule_5', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('schedule_6', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('mapel_1', models.CharField(max_length=20)),
                ('mapel_2', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('mapel_3', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('mapel_4', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('mapel_5', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('mapel_6', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('grade', models.CharField(choices=[('SD 1', 'SD 1'), ('SD 2', 'SD 2'), ('SD 3', 'SD 3'), ('SD 4', 'SD 4'), ('SD 5', 'SD 5'), ('SD 6', 'SD 6'), ('SMP 7', 'SMP 7'), ('SMP 8', 'SMP 8'), ('SMP 9', 'SMP 9'), ('SMA 10', 'SMA 10'), ('SMA 11', 'SMA 11'), ('SMA 12', 'SMA 12')], default='', max_length=10)),
                ('total_student', models.CharField(max_length=250)),
                ('school', models.CharField(max_length=150)),
                ('mode', models.CharField(choices=[('online (remote)', 'Online (remote)'), ('offline', 'Offline')], max_length=150)),
                ('user_type', models.CharField(default='student', editable=False, max_length=100)),
                ('status', models.BooleanField(default=False, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Student',
            },
        ),
    ]
