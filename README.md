# Sistema experto para diagnóstico inicial de conectividad de red

Sistema experto **basado en reglas**, desarrollado en Python como ejercicio práctico del módulo **5071 · Modelos de Inteligencia Artificial**, NF2, del Curso de Especialización en Inteligencia Artificial y Big Data (2026–2027).

El programa guía al usuario a través de comprobaciones de red habituales en Windows y, a partir de las respuestas proporcionadas, propone un **diagnóstico orientativo**. Utiliza una base de conocimiento de **20 reglas (R01–R20)** y un motor de inferencia de **encadenamiento hacia delante**, con una traza legible de las reglas que han contribuido a las conclusiones.

> [!IMPORTANT]
> **Herramienta educativa, no de diagnóstico definitivo.** No realiza sondas de red por sí sola, no verifica la veracidad de las respuestas y no modifica la configuración del equipo. Una conclusión probable no demuestra por sí sola la causa de una incidencia.

## Qué permite hacer

- Guiar la comprobación de interfaces **Wi-Fi y Ethernet**, dirección **IPv4**, puerta de enlace, comunicación mediante `ping` y resolución de nombres mediante `nslookup`.
- Aplicar reglas explícitas a hechos introducidos por el usuario y obtener nuevos hechos por encadenamiento hacia delante.
- Mostrar un diagnóstico inicial, recomendaciones y la **traza de inferencia**, con identificadores de reglas y explicaciones.
- Distinguir ciertos escenarios habituales: conectividad aparentemente funcional, posible problema de resolución DNS, posible problema de conectividad externa y posible alcance local o general.
- Detectar contradicciones entre hechos ya conocidos y conclusiones propuestas por las reglas, lanzando una excepción en el motor de inferencia.

## Arquitectura

```text
src/
  sistema_experto_red.py    # Interacción, validación de respuestas y presentación
  reglas.py                 # Base de conocimiento R01–R20
  motor_inferencia.py       # Evaluación de condiciones, inferencias y traza
pruebas/
  prueba_motor_inferencia.py  # Comprobaciones automatizadas del motor y reglas
README.md
LICENSE
requirements.txt
.gitignore
```

**Separación de responsabilidades:** `reglas.py` describe el conocimiento del dominio; `motor_inferencia.py` evalúa condiciones y aplica conclusiones sin codificar conceptos específicos de redes; `sistema_experto_red.py` solicita los datos y comunica el resultado. Los hechos se almacenan en un diccionario y las reglas se reevalúan hasta que una pasada completa no añade nuevos hechos.

## Requisitos

- **Python 3.13** (versión usada en el entorno de desarrollo). El código emplea únicamente la **biblioteca estándar** de Python; no requiere instalar paquetes de terceros.
- Terminal interactiva para introducir respuestas.
- Entorno Windows para seguir las comprobaciones guiadas descritas en la interfaz. Las pruebas automatizadas del motor no requieren Windows.

El archivo `requirements.txt` está vacío **intencionadamente**, porque no hay dependencias externas. Para una instalación más reproducible se recomienda utilizar un entorno virtual, aunque no es obligatorio.

## Ejecución en Windows (PowerShell)

Desde la carpeta raíz del proyecto:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m src.sistema_experto_red
```

El asistente formula preguntas sobre el estado de la conexión. Cuando se ofrece la opción `?`, muestra ayuda con comprobaciones que puedes realizar manualmente. Introduce respuestas que representen los resultados observados: **el programa no ejecuta esos comandos por ti**.

Si ya tienes un entorno Python compatible activado, también puedes iniciar la aplicación mediante:

```powershell
python -m src.sistema_experto_red
```

## Ejemplo: resolución DNS

Escenario ilustrativo:

1. La interfaz Wi-Fi está conectada y la puerta de enlace responde.
2. Hay respuesta al `ping` de una IP pública.
3. La consulta DNS del dominio de prueba falla.
4. El motor aplica una secuencia de reglas que incluye **R15**, y presenta un **posible problema de resolución DNS**, con la recomendación de revisar los servidores DNS configurados y repetir las pruebas.

**Interpretación:** este patrón apunta a una incidencia DNS, pero no prueba cuál es su causa concreta. Una prueba de `ping` tampoco acredita por sí sola el funcionamiento de todos los protocolos de red.

## Pruebas

Desde la raíz del proyecto:

```powershell
python -m pruebas.prueba_motor_inferencia
```

El conjunto actual realiza **21 comprobaciones automatizadas**: una por cada regla R01–R20 y una sobre detección de conflicto de conocimiento. Se basan en hechos de prueba y comprueban las conclusiones y la traza esperadas.

**Resultado de auditoría de esta entrega:** 21 comprobaciones satisfactorias, ejecutadas en el entorno de revisión con Python 3.13.5; código fuente sin cambios funcionales. Este resultado confirma los casos programados, **no** una cobertura completa de redes reales, ni equivale a pruebas de integración en todos los sistemas Windows.

## Alcance, limitaciones y sesgos

| Aspecto | Límite conocido | Consecuencia |
| --- | --- | --- |
| **Datos de entrada** | Las respuestas son proporcionadas manualmente por el usuario. | Una respuesta incorrecta puede producir una inferencia inapropiada. |
| **Cobertura del conocimiento** | Las 20 reglas representan un conjunto acotado de incidencias frecuentes. | Un caso no previsto puede quedar sin diagnóstico adecuado. |
| **Protocolos** | El flujo está centrado en **IPv4**, Wi-Fi/Ethernet, ICMP y resolución DNS básica. | No evalúa de forma específica escenarios IPv6, proxies, cortafuegos, rutas complejas o fallos por aplicación. |
| **Prueba ICMP** | La ausencia de respuesta a `ping` puede deberse a filtrado u otras restricciones. | No debe interpretarse automáticamente como ausencia de Internet. |
| **Cobertura de pruebas** | Se verifican 20 reglas y la detección de conflictos con casos diseñados. | No se demuestra ausencia de defectos ni precisión diagnóstica en campo. |
| **Conflictos** | El motor informa de contradicciones mediante `ValueError`. | No dispone de un sistema avanzado de resolución o priorización de reglas. |

### Sesgo de selección del conocimiento

La base de reglas refleja las situaciones escogidas durante el diseño y **prioriza ciertas incidencias IPv4**. No utiliza aprendizaje automático ni datos de entrenamiento; por tanto, su sesgo principal no es estadístico por un conjunto de entrenamiento, sino de **selección y representación de reglas**. Las situaciones menos representadas pueden recibir un análisis incompleto. Para reducir este sesgo sería necesario revisar el conocimiento con especialistas y probar una mayor diversidad de escenarios.

## Seguridad y privacidad

- El programa **no cambia** adaptadores, rutas ni servidores DNS.
- No ejecuta automáticamente comandos de red ni solicita credenciales.
- Su propósito es **orientar** comprobaciones manuales y ayudar a razonar sobre resultados; las recomendaciones deben verificarse antes de aplicar cualquier cambio real.
- Al compartir incidencias o salidas en un repositorio público, evita publicar direcciones IP internas, nombres de host, información personal o configuraciones sensibles de terceros.

## Posibles mejoras

- Ampliar las reglas para IPv6 y otros escenarios de red.
- Añadir pruebas de integración e historiales de casos reales anonimizados.
- Introducir prioridades o mecanismos controlados de resolución de conflictos.
- Mejorar la validación y la presentación estructurada de resultados.

Estas mejoras son **líneas futuras**, no funcionalidades existentes.

## Autoría y contexto

**Juan Bello Fernández.** Proyecto académico de aprendizaje sobre representación del conocimiento, sistemas basados en reglas y razonamiento explicable.

## Desarrollo y uso de IA generativa

Durante el aprendizaje, la programación, las pruebas y la documentación se utilizó **ChatGPT como herramienta de apoyo** para comprender conceptos, revisar la lógica de las reglas, depurar errores, preparar comprobaciones y mejorar explicaciones. El proyecto se desarrolló mediante un proceso iterativo de revisión y ejecución; su publicación no implica que todos los textos o fragmentos se hayan redactado sin asistencia. El autor asume la responsabilidad de revisar, mantener y presentar el material publicado.

## Licencia

**MIT License.** Copyright (c) 2026 Juan Bello Fernández.

Se permite usar, copiar, modificar, distribuir y reutilizar el código, también con fines comerciales, conforme a las condiciones del archivo [LICENSE](LICENSE). **En las copias o partes sustanciales del software debe conservarse el aviso de copyright y el texto de la licencia MIT.** La licencia no exige citar al autor en la interfaz de una aplicación derivada ni publicar las modificaciones realizadas.

El software se proporciona **sin garantía** y no debe considerarse una herramienta de diagnóstico profesional certificada. Esta licencia se aplica al contenido del repositorio publicado; no otorga derechos sobre marcas, materiales o servicios de terceros.
