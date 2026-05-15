# Documento de Requisitos

## Introduccion

Esta funcionalidad consolida las filas duplicadas por RUT al momento de exportar los resultados de extraccion de CVs a Excel. Cuando un candidato tiene multiples archivos procesados (por ejemplo, un PDF y un DOCX), el sistema genera una fila por archivo en la tabla extraction_results. Al exportar, el sistema debe producir una unica fila por candidato, identificado por su RUT, fusionando los datos de todos sus archivos. Los datos en Supabase permanecen intactos; la consolidacion ocurre exclusivamente durante la exportacion.

## Glosario

- **Sistema**: El backend FastAPI que procesa la solicitud de exportacion a Excel.
- **Consolidador**: El componente responsable de agrupar y fusionar filas por RUT antes de generar el Excel.
- **ExcelService**: El servicio Python que genera el archivo .xlsx a partir de las filas consolidadas.
- **RUT**: Rol Unico Tributario, identificador unico de personas en Chile. Puede aparecer bajo variantes: RUT, Rut, rut, RUT candidato, etc.
- **Fila**: Un diccionario de pares campo-valor que representa los datos extraidos de un archivo de CV.
- **Valor ausente**: El texto literal NO ENCONTRADO que el sistema de extraccion asigna cuando no puede obtener un campo del CV.
- **Grupo RUT**: Conjunto de filas que comparten el mismo valor de RUT normalizado.