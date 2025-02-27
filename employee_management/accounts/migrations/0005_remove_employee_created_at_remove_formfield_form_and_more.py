# Generated by Django 5.1.3 on 2024-11-30 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_employee_alter_formfield_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='form',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='order',
        ),
        migrations.AlterField(
            model_name='formfield',
            name='field_type',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='label',
            field=models.CharField(max_length=100),
        ),
    ]
