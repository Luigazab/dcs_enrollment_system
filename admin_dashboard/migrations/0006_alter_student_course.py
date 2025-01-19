# Generated by Django 5.1.3 on 2025-01-14 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0005_alter_subject_prerequisite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ForeignKey(default=1, null=True, db_column='course_id', on_delete=django.db.models.deletion.PROTECT, to='admin_dashboard.program'),
        ),
    ]