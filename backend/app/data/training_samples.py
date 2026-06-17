# Synthetic training samples for Document Classifier (Phase 11)
# 50 samples: 40 CV, 10 Non-CV

TRAINING_SAMPLES = [
    {
        "text": """
EXPERIENCIA LABORAL
Analista de Sistemas
Empresa Tecnologica S.A. | Enero 2020 - Presente
- Desarrollo y mantenimiento de aplicaciones web con Python y Django
- Administracion de bases de datos PostgreSQL
- Implementacion de APIs RESTful

FORMACION ACADEMICA
Ingenieria en Informatica
Universidad de Chile | 2015 - 2020

HABILIDADES
Python, Django, PostgreSQL, Docker, Git, AWS

IDIOMAS
Espanol: Nativo
Ingles: Avanzado (C1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA PROFESIONAL
Gerente de Ventas
Distribuidora del Norte Ltda. | Marzo 2018 - Actualidad
- Gestion de equipo comercial de 15 personas
- Incremento de ventas en un 35% anual
- Negociacion con proveedores internacionales

ESTUDIOS
Administracion de Empresas
Universidad Adolfo Ibanez | 2012 - 2017

COMPETENCIAS
Liderazgo, negociacion, Excel avanzado, CRM Salesforce

IDIOMAS
Espanol: Nativo
Ingles: Intermedio (B1)
""",
        "label": "cv"
    },
    {
        "text": """
ANTECEDENTES LABORALES
Jefe de Proyectos de Construccion
Constructora del Sur SpA | Junio 2019 - Diciembre 2023
- Supervision de obras civiles por sobre $500MM
- Coordinacion de equipos multidisciplinarios
- Control de presupuestos y cronogramas

FORMACION
Ingeniero Civil
Pontificia Universidad Catolica de Chile | 2010 - 2015

CURSOS
- PMP Project Management Professional (2020)
- Lean Construction (2021)

REFERENCIAS
Disponibles bajo solicitud
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCE
Senior Software Engineer
Tech Corp | San Francisco, CA | 2021 - Present
- Led migration from monolith to microservices architecture
- Designed and implemented event-driven systems with Kafka
- Mentored 4 junior engineers

EDUCATION
M.S. Computer Science
Stanford University | 2019 - 2021

SKILLS
Go, Python, Kubernetes, Kafka, AWS, Terraform

LANGUAGES
English: Native
Spanish: Fluent
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Medico Cirujano
Hospital Clinico Universidad de Chile | 2022 - Actualidad
- Atencion en urgencias y consultas generales
- Participacion en cirugias programadas y de emergencia

EDUCACION
Medicina
Universidad de Chile | 2015 - 2021

ESPECIALIZACION
Cirugia General (en curso)

IDIOMAS
Espanol: Nativo
Ingles: Avanzado (C1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA
Profesor de Educacion Basica
Colegio San Ignacio | 2020 - Actualidad
- Docencia en cursos de 3 a 6 basico
- Coordinador del area de matematicas

FORMACION
Pedagogia en Educacion Basica
Universidad Metropolitana | 2015 - 2019

CURSOS
- Didactica de las Matematicas (2021)
- Inclusion Educativa (2022)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Contador General
Estudio Contable Torres y Asociados | Enero 2019 - Actualidad
- Preparacion de declaraciones de impuestos mensuales y anuales
- Contabilidad general para 20+ empresas PYME
- Conciliaciones bancarias y analisis de cuentas

FORMACION ACADEMICA
Contador Auditor
Universidad de Santiago | 2013 - 2018

HABILIDADES
Excel avanzado, SAP, QuickBooks, ChileTributa
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Disenadora Grafica Senior
Agencia Creativa Ltda. | 2021 - Presente
- Diseno de identidad corporativa y branding
- Creacion de contenido para redes sociales
- Direccion de arte para campanas publicitarias

FORMACION
Diseno Grafico
Universidad del Pacifico | 2016 - 2020

HERRAMIENTAS
Adobe Illustrator, Photoshop, Figma, After Effects

IDIOMAS
Espanol: Nativo
Ingles: Intermedio (B1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Abogado Litigante
Estudio Juridico Mendez & Cia. | 2020 - Actualidad
- Litigacion en materia civil y comercial
- Redaccion de contratos y recursos legales
- Atencion a clientes corporativos

FORMACION ACADEMICA
Derecho
Universidad de Chile | 2013 - 2018

ESTUDIOS COMPLEMENTARIOS
- Diplomado en Derecho Tributario (2021)
- Mediacion y Arbitraje (2022)

IDIOMAS
Espanol: Nativo
Ingles: Avanzado (C1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ingeniero Electrico
Compania Electrica del Sur | 2019 - Actualidad
- Diseno de sistemas de distribucion electrica
- Supervision de mantenimiento de subestaciones
- Elaboracion de informes tecnicos

FORMACION
Ingenieria Electrica
Universidad Tecnica Federico Santa Maria | 2013 - 2018

CERTIFICACIONES
- Certificacion SEC Clase A (2020)
- Curso de Protecciones Electricas (2021)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Periodista Digital
El Mercurio Online | 2022 - Actualidad
- Redaccion de noticias de actualidad
- Edicion de contenido multimedia
- Gestion de redes sociales institucionales

FORMACION
Periodismo
Universidad Catolica | 2017 - 2021

HABILIDADES
Redaccion SEO, WordPress, Google Analytics, Canva

IDIOMAS
Espanol: Nativo
Portugues: Intermedio (B1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Enfermera Jefe
Clinica Alemana | 2020 - Actualidad
- Supervision de personal de enfermeria (12 personas)
- Coordinacion de turnos y procedimientos
- Manejo de pacientes criticos en UCI

FORMACION
Enfermeria
Universidad de los Andes | 2014 - 2019

CURSOS
- Reanimacion Avanzada (ACLS, 2021)
- Infecciones Intrahospitalarias (2022)
""",
        "label": "cv"
    },
    {
        "text": """
WORK EXPERIENCE
Mechanical Engineer
Siemens AG | Munich, Germany | 2020 - 2024
- Designed HVAC systems for commercial buildings
- Performed thermal load calculations and energy modelling
- Coordinated with cross-functional engineering teams

EDUCATION
B.S. Mechanical Engineering
Technical University of Munich | 2015 - 2019

SKILLS
AutoCAD, SolidWorks, ANSYS, MATLAB, Revit

CERTIFICATIONS
- EIT Certified (2020)
- LEED Green Associate (2021)

LANGUAGES
German: Native
English: Advanced (C1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ejecutivo de Ventas
Banco Santander | 2021 - Actualidad
- Captacion y asesoria de clientes patrimoniales
- Venta de productos financieros (inversiones, seguros)
- Cumplimiento de metas mensuales (+120% promedio)

FORMACION
Ingenieria Comercial
Universidad Adolfo Ibanez | 2015 - 2020

HABILIDADES
CRM Salesforce, Excel, Bloomberg Terminal
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Arquitecto Proyectista
Oficina de Arquitectura GP | 2019 - Actualidad
- Diseno y modelado 3D de proyectos residenciales
- Elaboracion de planos de construccion
- Gestion de permisos municipales

FORMACION
Arquitectura
Pontificia Universidad Catolica | 2012 - 2018

SOFTWARE
Revit, AutoCAD, SketchUp, Lumion, Adobe Suite
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Tecnico en Prevencion de Riesgos
Minera Escondida | 2020 - Actualidad
- Inspecciones de seguridad en terreno
- Capacitacion al personal en normas de seguridad
- Investigacion de accidentes e incidentes

FORMACION
Tecnico en Prevencion de Riesgos
DUOC UC | 2017 - 2020

CERTIFICACIONES
- Auditor Interno ISO 45001 (2021)
- Manejo de Emergencias (2022)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Community Manager
Agencia Digital Mkt | 2022 - Presente
- Gestion de redes sociales para 8 cuentas corporativas
- Creacion de calendario editorial y contenido
- Analisis de metricas y reporting mensual

FORMACION
Publicidad
Universidad del Desarrollo | 2018 - 2022

HERRAMIENTAS
Meta Business Suite, Hootsuite, Canva, Photoshop
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ingeniero Civil Industrial
CMPC | 2019 - Actualidad
- Optimizacion de procesos productivos en planta
- Reduccion de costos operativos en 12% anual
- Implementacion de sistema de gestion de calidad

FORMACION
Ingenieria Civil Industrial
Universidad de Concepcion | 2013 - 2018

IDIOMAS
Espanol: Nativo
Ingles: Avanzado (C1)

HERRAMIENTAS
Python, SQL, Power BI, Minitab, SAP
""",
        "label": "cv"
    },
    {
        "text": """
PROFESSIONAL EXPERIENCE
Data Scientist
Mercado Libre | Buenos Aires | 2022 - Present
- Built recommendation systems serving 10M+ users
- Developed NLP pipelines for product categorization
- A/B testing and statistical analysis

EDUCATION
M.S. Data Science
Universidad de Buenos Aires | 2020 - 2022

TECHNICAL SKILLS
Python, TensorFlow, PyTorch, Spark, SQL, Airflow

LANGUAGES
Spanish: Native
English: Advanced (C1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Psicologa Clinica
Consultorio Particular | 2020 - Actualidad
- Atencion psicologica a adolescentes y adultos
- Evaluacion y diagnostico clinico
- Terapia cognitivo-conductual

FORMACION
Psicologia
Universidad de Chile | 2013 - 2018

DIPLOMADOS
- Terapia Cognitivo-Conductual (2020)
- Psicologia Clinica Infanto-Juvenil (2021)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Desarrollador Mobile
StartupChile | 2021 - Actualidad
- Desarrollo de apps Android nativas con Kotlin
- Publicacion en Google Play Store (5 apps publicadas)
- Integracion con APIs REST y Firebase

FORMACION
Ingenieria en Computacion
Universidad de Valparaiso | 2015 - 2020

TECNOLOGIAS
Kotlin, Java, Firebase, Retrofit, Room, Git
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Analista de Recursos Humanos
Entel | 2020 - Actualidad
- Reclutamiento y seleccion de personal tecnico
- Gestion de nomina y beneficios
- Evaluacion de desempeno y clima laboral

FORMACION
Ingenieria en Recursos Humanos
Universidad de Santiago | 2015 - 2020

HERRAMIENTAS
SuccessFactors, WorkDay, Excel avanzado
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Chef Ejecutivo
Restaurant Borago | 2019 - Actualidad
- Direccion de cocina con equipo de 8 personas
- Creacion de menus de temporada
- Control de inventario y costos de alimentos

FORMACION
Cocina Internacional
Instituto Culinary | 2015 - 2018

CURSOS
- Pasteleria Profesional (2019)
- Cocina Peruana (2020)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Geologa
CODELCO | 2021 - Actualidad
- Exploracion y evaluacion de yacimientos mineros
- Modelamiento geologico 3D con Leapfrog
- Estimacion de recursos y reservas

FORMACION
Geologia
Universidad de Chile | 2014 - 2019

IDIOMAS
Espanol: Nativo
Ingles: Tecnico (B2)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA PROFESIONAL
Traductor e Interprete
Freelance | 2018 - Actualidad
- Traduccion juridica y comercial (EN-ES)
- Interpretacion simultanea en conferencias
- Localizacion de software y sitios web

FORMACION
Traduccion e Interpretacion
Universidad de Santiago | 2013 - 2018

IDIOMAS
Espanol: Nativo
Ingles: Bilingue (C2)
Frances: Avanzado (C1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ingeniero en Logistica
Cencosud | 2020 - Actualidad
- Gestion de cadena de suministro para 15 tiendas
- Optimizacion de rutas de distribucion
- Reduccion de costos logisticos en 18%

FORMACION
Ingenieria en Logistica
Universidad Andres Bello | 2015 - 2020

HERRAMIENTAS
SAP EWM, WMS, Power BI, Excel avanzado
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Trabajadora Social
Municipalidad de Providencia | 2019 - Actualidad
- Atencion y derivacion de casos sociales
- Gestion de programas comunitarios
- Elaboracion de informes sociales

FORMACION
Trabajo Social
Universidad Catolica | 2014 - 2019

AREAS
Intervencion familiar, mediacion, desarrollo comunitario
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ingeniero en Acuicultura
AquaChile | 2022 - Actualidad
- Supervision de centros de cultivo de salmon
- Control de calidad del agua y alimentacion
- Gestion de biomasa y produccion

FORMACION
Ingenieria en Acuicultura
Universidad Austral | 2016 - 2021

CURSOS
- Bienestar Animal en Acuicultura (2022)
- Gestion Ambiental (2023)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Product Manager
Fintual | 2021 - Actualidad
- Definicion de roadmap de producto
- Coordinacion con equipos de ingenieria y diseno
- Analisis de metricas y OKRs

FORMACION
Ingenieria Civil Industrial
Universidad de Chile | 2014 - 2019

HABILIDADES
Product strategy, SQL, Figma, Jira, data-driven decision making
""",
        "label": "cv"
    },
    {
        "text": """
WORK EXPERIENCE
UX Researcher
Globant | 2022 - Present
- Conducted user research for 6 enterprise products
- Usability testing and heuristic evaluations
- Developed user personas and journey maps

EDUCATION
B.A. Cognitive Science
UC Berkeley | 2018 - 2022

TOOLS
Figma, Miro, UserTesting, DScout, OptimalSort

LANGUAGES
English: Native
Spanish: Advanced (C1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Tecnico en Construccion
Constructora Loga | 2020 - Actualidad
- Lectura e interpretacion de planos
- Supervision de obras en terreno
- Control de calidad de materiales

FORMACION
Tecnico en Construccion
INACAP | 2017 - 2020

CURSOS
- Topografia Basica (2020)
- Normativa de Construccion (2021)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ingeniero Agronomo
Vina Concha y Toro | 2019 - Actualidad
- Gestion de vinedos (120 hectareas)
- Implementacion de riego tecnificado
- Control fitosanitario integrado

FORMACION
Ingenieria Agronomica
Universidad de Talca | 2013 - 2018

IDIOMAS
Espanol: Nativo
Ingles: Intermedio (B1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ejecutiva de Cuentas
Ogilvy Chile | 2022 - Actualidad
- Atencion de cuentas clave (Entel, CCU)
- Coordinacion de campanas publicitarias
- Preparacion de propuestas y presentaciones

FORMACION
Publicidad
Universidad Santo Tomas | 2017 - 2021

IDIOMAS
Espanol: Nativo
Ingles: Avanzado (C1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Kinesiologo
Centro de Rehabilitacion Integra | 2021 - Actualidad
- Rehabilitacion de lesiones deportivas y musculoesqueleticas
- Evaluacion funcional y planes de tratamiento
- Kinesioterapia y terapias manuales

FORMACION
Kinesiologia
Universidad de Chile | 2014 - 2019

DIPLOMADOS
- Kinesiologia Deportiva (2021)
- Dolor Musculoesqueletico (2022)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ingeniero en Medio Ambiente
Aguas Andinas | 2020 - Actualidad
- Monitoreo de calidad del agua potable
- Gestion de residuos y cumplimiento normativo
- Elaboracion de evaluaciones de impacto ambiental

FORMACION
Ingenieria Ambiental
Universidad de Concepcion | 2014 - 2019

CERTIFICACIONES
- Auditor Ambiental ISO 14001 (2021)
- Evaluacion de Impacto Ambiental (2020)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Tecnico en Electricidad Industrial
CMPC Celulosa | 2020 - Actualidad
- Mantenimiento de equipos electricos industriales
- Diagnostico y reparacion de fallas
- Lectura de planos electricos y esquemas

FORMACION
Tecnico en Electricidad Industrial
DUOC UC | 2017 - 2020

CERTIFICACIONES
- Certificacion SEC (2020)
- Trabajo en Altura (2021)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Bioquimica
Laboratorio Clinico UC | 2019 - Actualidad
- Analisis clinicos automatizados y manuales
- Control de calidad interno y externo
- Validacion de resultados criticos

FORMACION
Bioquimica
Universidad de Concepcion | 2013 - 2018

IDIOMAS
Espanol: Nativo
Ingles: Intermedio (B1)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Asistente Ejecutiva
Grupo BICE | 2021 - Actualidad
- Gestion de agenda de gerencia general
- Coordinacion de reuniones y viajes
- Elaboracion de informes y presentaciones

FORMACION
Secretariado Ejecutivo
INACAP | 2018 - 2021

HABILIDADES
Office 365 avanzado, SAP basico, organizacion de eventos
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Captain (Aviador Comercial)
LATAM Airlines | 2018 - Actualidad
- Comandante de aeronave Airbus A320
- Mas de 8,000 horas de vuelo acumuladas
- Instructor de simulador de vuelo

FORMACION
Capitan de Aviacion Comercial
Escuela de Aviacion | 2014 - 2017

LICENCIAS
- ATPL (Airline Transport Pilot License)
- Instructor Rating
- CRM Facilitator
""",
        "label": "cv"
    },
    {
        "text": """
WORK EXPERIENCE
DevOps Engineer
Ripley.com | 2021 - Present
- Managed Kubernetes clusters (EKS) serving 2M+ users
- Implemented CI/CD pipelines with GitHub Actions
- Reduced deployment time from 45min to 8min

EDUCATION
Computer Engineering
Universidad de Ingenieria del Peru | 2015 - 2020

TECH STACK
Docker, Kubernetes, Terraform, AWS, Helm, ArgoCD

CERTIFICATIONS
- AWS Solutions Architect (2022)
- CKA (Certified Kubernetes Administrator) (2023)
""",
        "label": "cv"
    },
    {
        "text": """
EXPERIENCIA LABORAL
Ingeniero Comercial
Falabella | 2019 - Actualidad
- Analisis de rentabilidad de lineas de negocio
- Elaboracion de presupuestos y proyecciones financieras
- Evaluacion de inversiones y proyectos

FORMACION
Ingenieria Comercial
Universidad de Chile | 2013 - 2018

HABILIDADES
Excel avanzado, SQL, Power BI, SAP FICO, Bloomberg
""",
        "label": "cv"
    },
    {
        "text": """
FACTURA ELECTRONICA N 0012345
RUT: 76.123.456-7
Razon Social: Empresa Ejemplo Ltda.

Fecha de Emision: 15 de marzo de 2025

Detalle:
- Servicios de consultoria tecnologica (ene 2025) $2.500.000
- Licencias de software (12 meses) $840.000
- Hosting y dominio anual $120.000

Subtotal: $3.460.000
IVA 19%: $657.400
Total: $4.117.400

Forma de pago: Transferencia electronica - 30 dias
""",
        "label": "non-cv"
    },
    {
        "text": """
Estimado Sr. Perez,

Por medio de la presente, tengo el agrado de postular al cargo de Jefe de Proyectos informado en LinkedIn.

Adjunto mi curriculum vitae para su revision.

Quedo atento a su respuesta para coordinar una entrevista.

Saludos cordiales,
Carlos Munoz
+56 9 1234 5678
carlos.munoz@email.com
""",
        "label": "non-cv"
    },
    {
        "text": """
ACTA DE REUNION N 042

Proyecto: Implementacion Sistema ERP
Fecha: 10 de enero de 2025
Asistentes: J. Martinez, L. Flores, R. Soto, M. Alvarez

Temas tratados:
1. Estado actual del desarrollo - 70% completado
2. Cronograma actualizado - entrega estimada marzo 2025
3. Presupuesto - dentro de lo planificado
4. Riesgos identificados - migracion de datos historicos

Proxima reunion: 24 de enero de 2025
""",
        "label": "non-cv"
    },
    {
        "text": """
ORDEN DE COMPRA N OC-2025-0893
Proveedor: TechSupply Chile SpA
Fecha: 20 febrero 2025

Item 1: Notebook Lenovo ThinkPad X1 Carbon (x5) $7.500.000
Item 2: Monitor Dell 27 4K (x10) $3.200.000
Item 3: Teclado inalambrico Logitech (x10) $450.000

Total: $11.150.000 + IVA
Entrega: 5 dias habiles
Condiciones de pago: 60 dias

Aprobado por: Gerencia de Administracion
""",
        "label": "non-cv"
    },
    {
        "text": """
CONTRATO DE PRESTACION DE SERVICIOS

Entre Servicios Tecnologicos SpA (en adelante "el Prestador")
y Cliente Final S.A. (en adelante "el Cliente")

OBJETO: Desarrollo de plataforma e-commerce

DURACION: 6 meses desde la fecha de firma

VALOR: UF 850 + IVA

FORMA DE PAGO:
- 30% al inicio del proyecto
- 40% a la entrega del MVP
- 30% a la entrega final

FIRMAS:
__________________          __________________
Prestador                    Cliente
""",
        "label": "non-cv"
    },
    {
        "text": """
BOLETIN OFICIAL N 43.215

Ministerio de Educacion
Subsecretaria de Educacion Superior

Dispone la creacion de la Mesa Tecnica de Innovacion Curricular
para las universidades del Consejo de Rectores.

Articulo 1: Convocar a las 18 universidades del CRUCH a
participar en la mesa tecnica.

Articulo 2: El plazo de entrega de propuestas sera de 90
dias corridos desde la publicacion del presente boletin.

Publicado: 15 de enero de 2025
""",
        "label": "non-cv"
    },
    {
        "text": """
MEMORANDUM INTERNO N 045/GTH/2025

Para: Todos los departamentos
De: Gerencia de Talento Humano
Asunto: Actualizacion proceso de evaluacion de desempeno

Se informa que a partir del 1 de abril de 2025 se
implementara el nuevo sistema de evaluacion de desempeno.

Los jefes directos deberan completar las evaluaciones
de sus equipos antes del 15 de marzo.

Saluda atentamente,
Maria Gonzalez
Gerenta de Talento Humano
""",
        "label": "non-cv"
    },
    {
        "text": """
EXTRACTO DE CUENTA CORRIENTE

Banco del Estado de Chile
Cuenta: 987654321
Titular: Juan Perez Perez
Periodo: Febrero 2025

Fecha    Descripcion                 Monto
01-02    Deposito sueldo            $1.500.000
05-02    Pago dividendos            -$450.000
10-02    Transferencia recibida      $200.000
15-02    Pago tarjeta credito       -$350.000
28-02    Cobro de servicios          -$80.000

Saldo actual: $820.000
""",
        "label": "non-cv"
    },
    {
        "text": """
Por la presente se certifica que:

Don Patricio Andres Lopez Munoz
RUT: 12.345.678-9

Ha completado satisfactoriamente el curso de
"Liderazgo y Gestion de Equipos"

Con una duracion de 40 horas pedagogicas
Realizado entre el 3 y el 28 de febrero de 2025

Santiago, 1 de marzo de 2025

___________________
Directora de Capacitacion
Consultora Gestion Ltda.
""",
        "label": "non-cv"
    },
    {
        "text": """
INFORME DE VENTAS - ENERO 2025
Sucursal: Providencia

Metrica           Valor     Variacion
Ventas totales   $45.2M    +12% vs mes ant.
Ticket promedio  $23.500   +5% vs mes ant.
Clientes nuevos  184       +22% vs mes ant.
Conversion web   3.2%      +0.4pp vs mes ant.

Top productos:
1. Notebooks ($12.5M, +8%)
2. Smartphones ($9.8M, +15%)
3. Accesorios ($5.2M, +3%)

Preparado por: Departamento de Analisis
""",
        "label": "non-cv"
    },
    {
        "text": """
Patricio Henry Parra Jimenez Carrera Docente Avanzado Experiencia Directiva Liderazgo Director Escuela Pablo Correa Montt Desde Agosto 2022 Director Liceo Fray Pablo de Royo Desde Abril 2021 a Julio de 2022 Coordinador Red Avance Autonomia Red de escuelas en contexto de encierro region del Bio Bio Director Escuela Carcelaria Centro Penitenciario Yumbel Jefe Tecnico Escuela carcelaria Centro Penitenciario Yumbel Coordinador Tecnico PSU Profesor Guia Preprofesional Docente Universidad de Concepcion Docencia Universitaria Universidad del Bio Bio Alumno Ayudante en Finanzas Contabilidad y Estadistica Formacion Profesional Universidad Autonoma Diplomado Gestion de la Convivencia Escolar Pontificia Universidad Catolica de Chile Diplomado Direccion y Liderazgo Escolar Universidad Andres Bello Magister en Direccion y Liderazgo para Gestion Educacional Universidad del Bio Bio Contador Auditor Universidad de Concepcion Licenciado en Educacion mencion Historia y Geografia Diplomados y Postitulos Universidad Andres Bello Diplomado en Gestion Estrategica en Organizaciones Diplomado en Politica y Gestion Educacional Universidad Santo Tomas Diplomado en Gestion Directiva Educacional Universidad Tecnologica Metropolitana Postitulo Administracion de Organizaciones Educativas Distinciones Tercer lugar en el Diplomado Direccion y Liderazgo Escolar por la PUC Seleccionado en la Pasantia Nacional por el CPEIP Tercer Lugar Nacional concurso MERCOSUR Primer seleccionado en la Carrera de Auditoria Universidad del Bio Bio
""",
        "label": "cv"
    },
    {
        "text": """
Rodrigo Rene Pardo Inzulza Profesor de Educacion General Basica Universidad de los Lagos Resumen Docente Educador interesado en Relatorias Investigacion Educacional Razonamiento Logico Matematico Ortografia Redaccion Antecedentes Academicos Magister en Educacion Mencion Gestion de Calidad Universidad Miguel de Cervantes Postitulo de Mencion en Gestion de la Convivencia Escolar Universidad Miguel de Cervantes Postitulo de Mencion en Administracion Educacional Universidad Miguel de Cervantes Diplomado en Convivencia Escolar para Lideres Educativos CEDLE Profesor Educacion General Basica Licenciado en Educacion Universidad de Los Lagos Actividades Academicas Docencia escolar DAEM Talca Escuela Prosperidad Coordinador SEP Docente Aula Encargado de Inventarios DAEM Talca Escuela Prosperidad Coordinador SEP Docente Aula Apoyo UTP Biblioteca CRA DAEM Pencahue Escuela Banos de Tanhuao Coordinador SEP Colegio Lyon School Profesor Encargado DEM Concepcion Escuela Luis David Cruz Ocampo Docente Educacion Artistica DEM Concepcion Colegio Bio Bio Encargado Unidad Tecnica Pedagogica DAEM Constitucion Escuela Gilda Bernal Docente Educacion Matematicas Datos Personales Fecha de nacimiento 02 de Marzo 1981 Carnet de identidad 14.018.012-2 Nacionalidad Chilena Estado Civil Soltero
""",
        "label": "cv"
    },
    {
        "text": """
Carlos Andres Munoz Soto Ingeniero Civil Informatico Universidad Tecnica Federico Santa Maria Resumen Profesional Experiencia en desarrollo de software arquitectura de microservicios y liderazgo de equipos tecnologicos Experiencia Laboral Lider Tecnico Empresa Innovacion Tecnologica Agosto 2020 Presente Diseno e implementacion de arquitectura cloud nativa con AWS Kubernetes y Terraform Liderazgo de equipo de 8 desarrolladores frontend y backend Reduccion de costos de infraestructura en 40 porcentaje mediante optimizacion de recursos Desarrollador Senior Soluciones Digitales SpA Enero 2017 Julio 2020 Desarrollo de APIs RESTful con Python FastAPI y PostgreSQL Implementacion de pipelines CI CD con GitLab y Docker Colaboracion en migracion de monolitos a microservicios Formacion Academica Ingenieria Civil Informatica Universidad Tecnica Federico Santa Maria 2011 2016 Certificaciones AWS Solutions Architect Professional 2023 Kubernetes Administrator CKA 2022 Competencias Python FastAPI Django AWS Docker Kubernetes Terraform PostgreSQL Git CI CD Idiomas Espanol Nativo Ingles Avanzado C1
""",
        "label": "cv"
    },
]
