# ============================================================
# BASE DE CONOCIMIENTO DEL SISTEMA EXPERTO
# ============================================================
# Este módulo contiene las reglas utilizadas por el sistema
# experto para diagnosticar problemas básicos de conectividad
# en Windows.
#
# Las reglas representan conocimiento explícito del dominio
# mediante estructuras del tipo:
#
# SI se cumplen determinadas condiciones
# ENTONCES se puede inferir uno o varios hechos nuevos.
#
# Este archivo NO solicita información al usuario y NO decide
# por sí mismo qué reglas deben ejecutarse.
#
# Su función es únicamente almacenar la base de conocimiento.
# El motor de inferencia será el responsable de comprobar las
# condiciones y aplicar las reglas correspondientes.
# ============================================================


# ------------------------------------------------------------
# REGLAS DE ESTADO DE LA INTERFAZ DE RED
# ------------------------------------------------------------
# Estas reglas permiten inferir si la interfaz utilizada ha
# establecido conexión con la red a partir de los hechos
# obtenidos durante la interacción inicial con el usuario.
#
# En Wi-Fi, esto significa asociación con una red inalámbrica.
# En Ethernet, significa existencia de enlace físico.
#
# Este hecho NO implica todavía disponer de una configuración
# IPv4 correcta ni tener acceso a Internet.

# ============================================================
# ESTRUCTURA DE LAS REGLAS
# ============================================================
# Cada regla de la base de conocimiento contendrá:
#
# - id:
#   Identificador único que permitirá saber qué regla
#   se ha activado durante la inferencia.
#
# - condiciones:
#   Conjunto de hechos que deben cumplirse simultáneamente
#   para que la regla pueda ejecutarse.
#
# - conclusiones:
#   Nuevos hechos que podrán incorporarse a la memoria de
#   trabajo cuando se cumplan todas las condiciones.
#
# - explicacion:
#   Texto legible que permitirá justificar posteriormente
#   por qué el sistema ha llegado a una determinada conclusión.
#
# Las reglas contienen conocimiento, pero NO implementan el
# algoritmo que decide cuándo deben activarse. Esa función
# corresponderá al motor de inferencia.

reglas = [
    # ========================================================
    # REGLAS DE ESTADO DE LA INTERFAZ DE RED
    # ========================================================
    # R01 - Interfaz Wi-Fi conectada
    # La asociación con una red Wi-Fi confirma que la interfaz
    # inalámbrica está conectada a una red, pero no garantiza
    # todavía una configuración IPv4 correcta ni acceso a Internet.
    {
        "id": "R01",
        "condiciones": {
            "tipo_conexion": "w",
            "wifi_conectado": True,
        },
        "conclusiones": {
            "interfaz_conectada": True,
        },
        "explicacion": (
            "El equipo está asociado correctamente a una red Wi-Fi, "
            "por lo que la interfaz inalámbrica está conectada."
        ),
    },
    # R02 - Interfaz Ethernet conectada
    # La existencia de enlace Ethernet confirma que la interfaz
    # ha establecido conexión física con otro dispositivo de red,
    # pero no garantiza todavía conectividad IP ni acceso a Internet.
    {
        "id": "R02",
        "condiciones": {
            "tipo_conexion": "e",
            "hay_enlace": True,
        },
        "conclusiones": {
            "interfaz_conectada": True,
        },
        "explicacion": (
            "La interfaz Ethernet ha establecido correctamente un enlace "
            "físico con otro dispositivo de red."
        ),
    },
    # R03 - Interfaz desactivada
    # Si el adaptador utilizado está desactivado, esa interfaz no puede
    # establecer conexión con la red.
    {
        "id": "R03",
        "condiciones": {
            "adaptador_activo": False,
        },
        "conclusiones": {
            "interfaz_conectada": False,
            "recomendar_activar_adaptador": True,
        },
        "explicacion": (
            "El adaptador de red está desactivado, por lo que la interfaz "
            "no puede establecer conexión con la red."
        ),
    },
    # R04 - Interfaz Wi-Fi no conectada
    # Un adaptador Wi-Fi puede estar activo sin estar asociado
    # a ninguna red inalámbrica.
    {
        "id": "R04",
        "condiciones": {
            "tipo_conexion": "w",
            "wifi_conectado": False,
        },
        "conclusiones": {
            "interfaz_conectada": False,
            "recomendar_conectar_wifi": True,
        },
        "explicacion": (
            "El adaptador Wi-Fi está activo, pero no está asociado "
            "a ninguna red inalámbrica."
        ),
    },
    # R05 - Interfaz Ethernet sin cable conectado
    # Si el cable Ethernet no está conectado al equipo, la interfaz
    # no puede establecer un enlace físico con otro dispositivo de red.
    {
        "id": "R05",
        "condiciones": {
            "tipo_conexion": "e",
            "cable_conectado": False,
        },
        "conclusiones": {
            "interfaz_conectada": False,
            "recomendar_conectar_cable": True,
        },
        "explicacion": (
            "El cable Ethernet no está conectado al equipo, por lo que la "
            "interfaz no puede establecer un enlace físico de red."
        ),
    },
    # R06 - Interfaz Ethernet sin enlace
    # Aunque el cable esté conectado físicamente, la interfaz puede no
    # establecer enlace con el otro extremo de la conexión.
    #
    # Esto puede deberse a problemas de cable, puerto o dispositivo de red.
    {
        "id": "R06",
        "condiciones": {
            "tipo_conexion": "e",
            "cable_conectado": True,
            "hay_enlace": False,
        },
        "conclusiones": {
            "interfaz_conectada": False,
            "recomendar_revisar_enlace_ethernet": True,
        },
        "explicacion": (
            "El cable Ethernet está conectado, pero la interfaz no ha "
            "establecido enlace con el otro extremo de la conexión."
        ),
    },
    # ========================================================
    # REGLAS DE CONFIGURACIÓN IPv4
    # ========================================================
    # R07 - Dirección IPv4 link-local (APIPA)
    # Una dirección 169.254.0.0/16 indica que Windows dispone de una
    # dirección IPv4 link-local. En una red convencional con DHCP,
    # suele indicar que el equipo no ha obtenido una configuración
    # IPv4 utilizable desde el servidor DHCP.
    {
        "id": "R07",
        "condiciones": {
            "es_apipa": True,
        },
        "conclusiones": {
            "posible_fallo_dhcp": True,
            "recomendar_revisar_dhcp": True,
        },
        "explicacion": (
            "El equipo utiliza una dirección IPv4 link-local del rango "
            "169.254.0.0/16. En una red convencional, esto suele indicar "
            "que no se ha obtenido correctamente la configuración mediante DHCP."
        ),
    },
    # R08 - Ausencia de puerta de enlace predeterminada
    # Si no existe una puerta de enlace configurada, el equipo puede
    # comunicarse dentro de su red local, pero normalmente no podrá
    # alcanzar redes externas como Internet.
    #
    # La ausencia de gateway puede deberse a una configuración IP
    # incompleta o incorrecta, aunque también podría ser intencionada
    # en redes que no necesiten acceso fuera de la subred local.
    {
        "id": "R08",
        "condiciones": {
            "gateway_configurado": False,
        },
        "conclusiones": {
            "posible_fallo_configuracion_ip": True,
            "recomendar_revisar_configuracion_ip": True,
        },
        "explicacion": (
            "No existe una puerta de enlace predeterminada configurada. "
            "En una red con acceso a Internet, esto puede indicar una "
            "configuración IP incompleta o incorrecta."
        ),
    },
    # R09 - Comunicación confirmada con la puerta de enlace
    # Si el ping a la puerta de enlace tiene éxito, se confirma
    # comunicación IPv4 mediante ICMP con el gateway configurado.
    {
        "id": "R09",
        "condiciones": {
            "ping_gateway_exitoso": True,
        },
        "conclusiones": {
            "comunicacion_gateway_confirmada": True,
        },
        "explicacion": (
            "La puerta de enlace ha respondido correctamente al ping, "
            "por lo que se confirma comunicación IPv4 mediante ICMP "
            "con el gateway configurado."
        ),
    },
    # R10 - Comunicación con el gateway no confirmada mediante ping
    # Si el ping a la puerta de enlace no obtiene respuesta, no puede
    # confirmarse comunicación mediante ICMP con el gateway.
    #
    # Esto NO demuestra por sí solo que el gateway esté inaccesible,
    # ya que ICMP puede estar filtrado por firewall o configuración.
    {
        "id": "R10",
        "condiciones": {
            "ping_gateway_exitoso": False,
        },
        "conclusiones": {
            "comunicacion_gateway_no_confirmada": True,
        },
        "explicacion": (
            "La puerta de enlace no ha respondido al ping. "
            "No puede confirmarse comunicación mediante ICMP con el gateway, "
            "aunque la ausencia de respuesta no demuestra por sí sola "
            "que el dispositivo esté inaccesible."
        ),
    },
    # R11 - Comunicación externa por IP confirmada
    # Si una dirección IPv4 pública responde al ping, se confirma
    # comunicación IP con un destino externo sin depender de DNS.
    {
        "id": "R11",
        "condiciones": {
            "ping_internet_exitoso": True,
        },
        "conclusiones": {
            "comunicacion_externa_ip_confirmada": True,
        },
        "explicacion": (
            "Una dirección IPv4 pública ha respondido correctamente al ping, "
            "por lo que se confirma comunicación IP con un destino externo "
            "sin depender de la resolución DNS."
        ),
    },
    # R12 - Comunicación externa por IP no confirmada
    # Si el ping a una dirección IPv4 pública no obtiene respuesta,
    # no puede confirmarse comunicación externa mediante ICMP.
    #
    # Esto NO demuestra por sí solo que no exista acceso a Internet,
    # ya que ICMP puede estar filtrado en el destino o en algún punto
    # intermedio de la red.
    {
        "id": "R12",
        "condiciones": {
            "ping_internet_exitoso": False,
        },
        "conclusiones": {
            "comunicacion_externa_ip_no_confirmada": True,
        },
        "explicacion": (
            "La dirección IPv4 pública utilizada como prueba no ha respondido "
            "al ping. No puede confirmarse comunicación externa mediante ICMP, "
            "aunque esto no demuestra por sí solo que no exista acceso a Internet."
        ),
    },
    # R13 - Resolución DNS confirmada
    # Si el dominio de prueba se resuelve correctamente, se confirma
    # que el sistema dispone de resolución DNS funcional para esa prueba.
    {
        "id": "R13",
        "condiciones": {
            "dns_resolucion_exitosa": True,
        },
        "conclusiones": {
            "dns_confirmado": True,
        },
        "explicacion": (
            "El dominio de prueba se ha resuelto correctamente, "
            "por lo que se confirma funcionamiento de la resolución DNS "
            "para esta comprobación."
        ),
    },
    # R14 - Resolución DNS no confirmada
    # Si el dominio de prueba no puede resolverse, existe evidencia
    # compatible con un posible problema de resolución DNS.
    #
    # Una única prueba fallida no permite afirmar de forma absoluta
    # que todo el servicio DNS esté averiado.
    {
        "id": "R14",
        "condiciones": {
            "dns_resolucion_exitosa": False,
        },
        "conclusiones": {
            "posible_fallo_dns": True,
        },
        "explicacion": (
            "El dominio de prueba no ha podido resolverse. "
            "Esto es compatible con un posible problema de DNS, aunque "
            "una única comprobación fallida no permite confirmarlo de forma absoluta."
        ),
    },
    # ========================================================
    # REGLAS DE CLASIFICACIÓN DEL DIAGNÓSTICO
    # ========================================================
    # R15 - Posible problema específico de DNS
    # Si existe comunicación confirmada con un destino externo por IP,
    # pero la resolución DNS falla, la conectividad IP funciona y el
    # problema es compatible con un fallo específico de DNS.
    {
        "id": "R15",
        "condiciones": {
            "comunicacion_externa_ip_confirmada": True,
            "posible_fallo_dns": True,
        },
        "conclusiones": {
            "problema_dns_probable": True,
            "recomendar_revisar_dns": True,
        },
        "explicacion": (
            "Existe comunicación confirmada con un destino externo mediante "
            "dirección IP, pero la resolución de nombres ha fallado. "
            "Esto hace probable un problema específico de DNS."
        ),
    },
    # R16 - Conectividad funcional confirmada
    # Si existe comunicación externa confirmada por IP y la resolución
    # DNS también funciona, las comprobaciones principales realizadas
    # por el sistema han resultado satisfactorias.
    {
        "id": "R16",
        "condiciones": {
            "comunicacion_externa_ip_confirmada": True,
            "dns_confirmado": True,
        },
        "conclusiones": {
            "conectividad_funcional": True,
        },
        "explicacion": (
            "Existe comunicación confirmada con un destino externo por IP "
            "y la resolución DNS funciona correctamente. Las comprobaciones "
            "principales de conectividad realizadas han sido satisfactorias."
        ),
    },
    # R17 - Problema de conectividad externa probable
    # Si no puede confirmarse comunicación con un destino externo
    # mediante IP y además falla la resolución DNS, existen varias
    # evidencias compatibles con un problema de conectividad externa.
    #
    # La conclusión se mantiene como probable porque las pruebas
    # realizadas no permiten determinar todavía el alcance exacto
    # ni descartar completamente filtrado de ICMP u otras causas.
    {
        "id": "R17",
        "condiciones": {
            "comunicacion_externa_ip_no_confirmada": True,
            "posible_fallo_dns": True,
        },
        "conclusiones": {
            "problema_conectividad_externa_probable": True,
        },
        "explicacion": (
            "No se ha podido confirmar comunicación con un destino externo "
            "mediante IP y la resolución DNS también ha fallado. "
            "La combinación de ambas evidencias es compatible con un "
            "problema de conectividad externa."
        ),
    },
    # R18 - Problema probablemente local al equipo
    # Si este equipo presenta un problema probable de conectividad
    # externa, pero otros dispositivos de la misma red sí disponen
    # de acceso a Internet, el alcance del fallo parece estar
    # localizado en este equipo.
    {
        "id": "R18",
        "condiciones": {
            "problema_conectividad_externa_probable": True,
            "hay_otros_dispositivos": True,
            "otros_dispositivos_tienen_internet": True,
        },
        "conclusiones": {
            "alcance_fallo": "equipo",
            "recomendar_revisar_equipo": True,
        },
        "explicacion": (
            "Otros dispositivos conectados a la misma red tienen acceso "
            "a Internet mientras este equipo presenta problemas de conectividad. "
            "Esto hace probable que el origen del fallo esté localizado "
            "en este equipo."
        ),
    },
    # R19 - Problema probablemente general de la red
    # Si este equipo presenta un problema probable de conectividad
    # externa y otros dispositivos de la misma red tampoco tienen
    # acceso a Internet, el alcance del fallo parece afectar a la red.
    {
        "id": "R19",
        "condiciones": {
            "problema_conectividad_externa_probable": True,
            "hay_otros_dispositivos": True,
            "otros_dispositivos_tienen_internet": False,
        },
        "conclusiones": {
            "alcance_fallo": "red",
            "recomendar_revisar_red": True,
        },
        "explicacion": (
            "Este equipo presenta problemas de conectividad y otros dispositivos "
            "de la misma red tampoco tienen acceso a Internet. "
            "Esto hace probable que el problema afecte a la red en general."
        ),
    },
    # R20 - Alcance del fallo no determinado
    # Si existe un problema probable de conectividad externa pero no
    # hay otros dispositivos disponibles para comparar, no puede
    # determinarse si el fallo afecta solo al equipo o a toda la red.
    {
        "id": "R20",
        "condiciones": {
            "problema_conectividad_externa_probable": True,
            "hay_otros_dispositivos": False,
        },
        "conclusiones": {
            "alcance_fallo": "desconocido",
            "recomendar_ampliar_comprobaciones": True,
        },
        "explicacion": (
            "No hay otros dispositivos disponibles en la misma red "
            "para comparar su conectividad. Por tanto, no puede "
            "determinarse si el problema está localizado en este equipo "
            "o afecta a la red en general."
        ),
    },
]
