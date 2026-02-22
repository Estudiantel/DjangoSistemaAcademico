from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True)),
                ('duracion', models.PositiveIntegerField(help_text='Duración en años.')),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('especialidad', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('cupo_maximo', models.PositiveIntegerField()),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materias', to='usuarios.carrera')),
                ('profesor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='materias', to='usuarios.docente')),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('legajo', models.CharField(max_length=30, unique=True)),
                ('carrera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='alumnos', to='usuarios.carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inscripciones', to='usuarios.alumno')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inscripciones', to='usuarios.materia')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('dni', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('rol', models.CharField(choices=[('ADMINISTRADOR', 'Administrador'), ('ALUMNO', 'Alumno'), ('DOCENTE', 'Docente'), ('INVITADO', 'Invitado')], max_length=20)),
                ('debe_cambiar_password', models.BooleanField(default=True)),
                ('alumno', models.OneToOneField(blank=True, help_text='Vincular cuando el usuario tenga rol Alumno.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario', to='usuarios.alumno')),
                ('docente', models.OneToOneField(blank=True, help_text='Vincular cuando el usuario tenga rol Docente.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario', to='usuarios.docente')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='materia',
            constraint=models.UniqueConstraint(fields=('nombre', 'carrera'), name='unique_materia_nombre_por_carrera'),
        ),
        migrations.AddConstraint(
            model_name='inscripcion',
            constraint=models.UniqueConstraint(fields=('alumno', 'materia'), name='unique_inscripcion_alumno_materia'),
        ),
    ]
