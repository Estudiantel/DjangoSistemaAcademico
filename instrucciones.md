PROYECTO DE **PYTHON + DJANGO** 

Desarrollo de Sistemas web con enfoque en buenas prácticas, arquitectura en capas y persistencia de datos. 

1. **Modalidad de Aprobación** 
- Entrega  de  un  proyecto  integrador  grupal  completo,  desarrollado  en Python con Django. 
- Examen presencial (oral), enfocado en los contenidos teóricos y en la defensa del proyecto.

2. **Proyecto Integrador Obligatorio** 
Fecha  de  entrega:  Coordinada  con  la  mesa  de  examen. El  proyecto  debe  entregarse  hasta  72  horas  antes  del  examen presencial. 

**Forma de entrega:** 

Subida del proyecto completo a un repositorio grupal en GitHub (código fuente, incluyendo *requirements.txt, manage.py*, migraciones, etc.). 

3. **Tecnología Obligatoria** 
- Python 3.8 o superior 
- 🖥Django 4.x o superior (framework web) 
- 🗃Django  ORM  como  tecnología  de  persistencia  (base  de  datos  relacional: SQLite, PostgreSQL o MySQL) 
- Estructura basada en buenas prácticas de desarrollo: 
- Separación  clara  de  responsabilidades  (Modelos,  Vistas,  Formularios, Servicios). 
- Reutilización de código mediante funciones, clases y mixins. 
- Validaciones en formularios y modelos. 
- Uso de *apps* para modularizar funcionalidades. 
- Refactorización y legibilidad del código 

4. **Requisitos mínimos del sistema**
El  sistema  debe  ser  una  aplicación  web  de  gestión  académica  con  las siguientes características: 

- CRUD completo para: Usuarios, Carreras, Materias, Alumnos. 
- Gestión  de  relaciones  entre  entidades,  incluyendo  inscripciones (Alumno–Materia). 
- Persistencia  de  datos  mediante  Django  ORM  y  una  base  de  datos relacional. 
- Navegación clara mediante menú o barra de navegación (navbar) visible en todas las páginas. 
- Validaciones  en  formularios  (campos  obligatorios,  formato  de  correo, etc.) usando *forms* de Django. 
- Aplicación de principios de Programación Orientada a Objetos (POO): 
- Encapsulamiento:  atributos  privados,  propiedades, métodos de instancia. 
- Abstracción: uso de servicios o managers para aislar lógica de negocio. 
- Interfaces (abstractas): uso de clases base abstractas en modelos o servicios. 
- Herencia:  una  clase  *Persona*  como  base  común  para *Alumno*, etc. 
- Sistema de autenticación con inicio de sesión y roles diferenciados. 
- Permitir que el usuario cambie su contraseña tras el primer acceso. 
- Estilo visual mínimo usando Bootstrap 5 u otro framework CSS moderno. 
- Proyecto  compilable  y  funcional  sin  errores  (sin  errores  de  sintaxis, migraciones aplicadas, etc.).

5. **Requisitos funcionales principales** 
El  sistema  debe  simular  un  módulo  de  gestión  académica  con  las siguientes funcionalidades: 

- Crear,  consultar,  modificar  y  eliminar:  carreras,  materias,  alumnos  y usuarios. 
- Mostrar datos en tablas ordenadas y paginadas (usando *Django tables2* o estructura manual). 
- Formularios con validaciones (requeridos, duplicados, formatos). 
- Mensajes claros ante errores (validación, permisos, restricciones). 
- Navegación mediante navbar con enlaces según rol. 
- Separación de capas: 
- Presentación:  vistas  (Class-Based  Views  o  Function-Based  Views)  y templates. 

- Lógica  de  negocio:  servicios  (módulos  *.py*  separados)  o  métodos  en modelos. 
- Acceso a datos: modelos y managers de Django ORM. 
- Sistema de login con roles diferenciados. 
- Validación de integridad de datos (no  duplicados, no eliminación con relaciones activas). 
- Cambio de contraseña tras primer login.

6. **Roles definidos obligatorios** 
El sistema debe incluir autenticación con roles: 

| ROL           | PERMISOS                                                                                                         |
|---------------|------------------------------------------------------------------------------------------------------------------|
| Administrador | Puede crear, modificar y eliminar: carreras, materias, alumnos y usuarios. Puede ver todas las inscripciones.    |
| Alumno        | Puede ver la oferta académica, inscribirse o darse de baja de materias. Solo ve sus datos.                       |
| Invitado      | Solo puede ver carreras y materias. Sin acceso a edición ni inscripción.                                         |
| Docente       | Puede ver sus materias y listas de alumnos (solo visual).                                                        |

7. **Inicio de sesión y autenticación** 
- Los usuarios inician sesión con DNI y correo electrónico registrados. 
- Al  crear  un  usuario,  el  sistema  genera  una  contraseña  inicial  (por ejemplo, el DNI). 
- Tras el primer login, se obliga a cambiar la contraseña. 
- El  acceso  a  vistas  debe  estar  restringido  por  decoradores  o  mixins *(@login\_required, user\_passes\_test, UserPassesTestMixin*). 
- El  rol  del  usuario  debe  almacenarse  como  un  campo  en  el  modelo *Usuario* (ver más abajo). 
- Uso  de  grupos  (Groups)  o  campos  personalizados  en  el  modelo  de usuario para manejar roles. 


8. **Modelo de datos y relaciones**
Entidades principales:
- Persona (Clase base abstracta) 
- Alumno (hereda de Persona) 
- Usuario (para autenticación) 
- Alternativa válida: Duplicar datos personales en Usuario (nombre, dni, email) si se prefiere simplicidad. Ambos enfoques son aceptables. 
- Inscripción (tabla intermedia: Alumno–Materia) 

9. **Restricciones lógicas obligatorias**
- No permitir eliminar una Carrera si tiene Materias o Alumnos asociados.
- No permitir eliminar una Materia si tiene Inscripciones activas.
- Validar integridad referencial en eliminación y edición.
- Evitar duplicados de DNI, correo, nombre de materia, etc.
- Impedir inscripciones si el cupo está lleno.

10. **Gestión de usuarios** 
- El Administrador puede hacer CRUD de usuarios. 
- Al crear un usuario: 

  Se debe asignar un rol válido. 

  Si el rol es Alumno, se debe crear o vincular un registro en Alumno. La contraseña inicial se genera automáticamente.  

- Validar que no se cree un usuario sin rol. 
- El usuario debe poder cambiar su contraseña tras el primer acceso.

11. **Casos de uso esperados (mínimos)** 

Acciones del Administrador 

- Iniciar sesión y acceder al panel de gestión. 
- CRUD completo de Carreras, Materias, Alumnos y Usuarios. 
- Asignar Alumnos a Carreras. 
- Ver todas las inscripciones. 
- No crear Materias con nombre duplicado. 
- No cargar Alumnos con DNI o email duplicado. 
- No eliminar Carreras o Materias con relaciones activas. 

Acciones del Alumno 

- Iniciar sesión con DNI y correo. 
- Cambiar contraseña tras primer acceso. 
- Ver materias de su carrera. 
- Inscribirse o darse de baja de materias disponibles. 
- Ver materias con cupo disponible. 

Validaciones generales 

- Mostrar mensajes de error en formularios. 
- Evitar inscripciones duplicadas. 
- Validar cupo máximo antes de inscribir. 
- Permitir inscripción directa (sin correlativas).

12. **Filtros y consultas funcionales (obligatorios)** 

El sistema debe incluir al menos dos filtros accesibles desde la interfaz: 

Ejemplos: 
- Filtrar Materias por Carrera (usando un <select>). 
- Ver todas las materias en las que está inscripto un Alumno. 
- Ver todos los Alumnos inscriptos en una Materia. 
- Filtrar Materias con cupo disponible. 
- Implementar con Django ORM + vistas + templates. Puede usarse ListView con filtros o forms para búsquedas.

13. **Consideraciones de diseño avanzadas** 

Herencia vs. Composición: *Usuario y Persona*

Se aceptan dos enfoques válidos: 

Separación con datos duplicados: 
- Usuario tiene: dni, email, nombre. 
- Alumno (hereda de Persona) también tiene: dni, email, nombre. 
- Simplicidad, pero duplicación controlada. 
- Válido si se mantiene coherencia. 

Composición con relación uno a uno: 
- Usuario tiene un campo OneToOneField(Persona). 
- Alumno hereda de Persona. 
- Mayor reutilización, menos duplicación. 
- Más complejo, pero mejor diseño. 

14. **Examen Presencial** 

El examen evaluará: 

- Comprensión de los contenidos teóricos del programa (POO, estructuras de datos, algoritmos, patrones).
- Conocimiento sobre: 

  Django (ORM, vistas, autenticación). 

  Python (POO, manejo de excepciones, modularización). 

  Bases de datos relacionales y Django ORM. 

  Buenas prácticas (separación de capas, reutilización, validaciones). 

15. **Recomendaciones finales** 
- Usa virtualenv o pipenv para gestionar dependencias. 
- Incluye un requirements.txt generado con pip freeze. 
- Documenta el proyecto con un README.md (cómo instalar, configurar, correr). 
- Usa migrations correctamente. 
- Prueba todas las funcionalidades antes de entregar.


