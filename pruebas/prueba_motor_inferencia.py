from src.reglas import reglas
from src.motor_inferencia import (
    aplicar_conclusiones,
    encadenamiento_hacia_adelante,
)


def comprobar_caso(
    nombre,
    hechos,
    nombre_hecho_esperado,
    valor_esperado,
    regla_esperada,
):
    """
    Ejecuta un escenario de prueba y comprueba que el motor
    infiere el hecho esperado y activa la regla prevista.
    """
    traza = encadenamiento_hacia_adelante(reglas, hechos)

    assert hechos[nombre_hecho_esperado] == valor_esperado

    ids_reglas_activadas = [paso["id"] for paso in traza]
    assert regla_esperada in ids_reglas_activadas

    print(f"[OK] {nombre}")


# ============================================================
# PRUEBAS DE LAS REGLAS DE ESTADO DE LA INTERFAZ
# ============================================================


# ------------------------------------------------------------
# R01 - Interfaz Wi-Fi conectada
# ------------------------------------------------------------
# Si el adaptador está activo y el equipo está asociado a una
# red Wi-Fi, el motor debe inferir que la interfaz está conectada.

hechos_prueba_wifi_conectado = {
    "tipo_conexion": "w",
    "adaptador_activo": True,
    "wifi_conectado": True,
}

comprobar_caso(
    "Wi-Fi conectado",
    hechos_prueba_wifi_conectado,
    "interfaz_conectada",
    True,
    "R01",
)


# ------------------------------------------------------------
# R02 - Interfaz Ethernet conectada
# ------------------------------------------------------------
# Si existe cable y enlace Ethernet, el motor debe inferir
# que la interfaz está conectada.

hechos_prueba_ethernet = {
    "tipo_conexion": "e",
    "adaptador_activo": True,
    "cable_conectado": True,
    "hay_enlace": True,
}

comprobar_caso(
    "Ethernet con enlace",
    hechos_prueba_ethernet,
    "interfaz_conectada",
    True,
    "R02",
)


# ------------------------------------------------------------
# R03 - Interfaz desactivada
# ------------------------------------------------------------
# Si el adaptador está desactivado, el motor debe inferir
# que la interfaz no está conectada.

hechos_prueba_adaptador_inactivo = {
    "tipo_conexion": "w",
    "adaptador_activo": False,
}

comprobar_caso(
    "Adaptador desactivado",
    hechos_prueba_adaptador_inactivo,
    "interfaz_conectada",
    False,
    "R03",
)


# ------------------------------------------------------------
# R04 - Interfaz Wi-Fi no conectada
# ------------------------------------------------------------
# Un adaptador Wi-Fi puede estar activo sin estar asociado
# a ninguna red inalámbrica.

hechos_prueba_wifi_desconectado = {
    "tipo_conexion": "w",
    "adaptador_activo": True,
    "wifi_conectado": False,
}

comprobar_caso(
    "Wi-Fi no conectado",
    hechos_prueba_wifi_desconectado,
    "interfaz_conectada",
    False,
    "R04",
)


# ------------------------------------------------------------
# R05 - Interfaz Ethernet sin cable conectado
# ------------------------------------------------------------
# Sin cable Ethernet no puede establecerse enlace físico
# con otro dispositivo de red.

hechos_prueba_sin_cable = {
    "tipo_conexion": "e",
    "adaptador_activo": True,
    "cable_conectado": False,
}

comprobar_caso(
    "Ethernet sin cable",
    hechos_prueba_sin_cable,
    "interfaz_conectada",
    False,
    "R05",
)


# ------------------------------------------------------------
# R06 - Interfaz Ethernet sin enlace
# ------------------------------------------------------------
# Aunque exista cable, si no se establece enlace Ethernet
# el motor debe inferir que la interfaz no está conectada.

hechos_prueba_sin_enlace = {
    "tipo_conexion": "e",
    "adaptador_activo": True,
    "cable_conectado": True,
    "hay_enlace": False,
}

comprobar_caso(
    "Ethernet sin enlace",
    hechos_prueba_sin_enlace,
    "interfaz_conectada",
    False,
    "R06",
)


# ============================================================
# PRUEBAS DE LAS REGLAS DE CONFIGURACIÓN IPv4
# ============================================================


# ------------------------------------------------------------
# R07 - Dirección IPv4 link-local (APIPA)
# ------------------------------------------------------------
# Una dirección APIPA debe permitir al motor inferir un
# posible fallo en la obtención de configuración mediante DHCP.

hechos_prueba_apipa = {
    "tipo_conexion": "w",
    "adaptador_activo": True,
    "wifi_conectado": True,
    "es_apipa": True,
}

comprobar_caso(
    "Dirección APIPA",
    hechos_prueba_apipa,
    "posible_fallo_dhcp",
    True,
    "R07",
)


# ------------------------------------------------------------
# R08 - Ausencia de puerta de enlace predeterminada
# ------------------------------------------------------------
# Si no existe gateway configurado, el motor debe señalar
# un posible problema de configuración IP.

hechos_prueba_sin_gateway = {
    "tipo_conexion": "w",
    "adaptador_activo": True,
    "wifi_conectado": True,
    "gateway_configurado": False,
}

comprobar_caso(
    "Puerta de enlace no configurada",
    hechos_prueba_sin_gateway,
    "posible_fallo_configuracion_ip",
    True,
    "R08",
)


# ------------------------------------------------------------
# R09 - Comunicación confirmada con la puerta de enlace
# ------------------------------------------------------------
# Si el ping al gateway tiene éxito, el motor debe confirmar
# comunicación IPv4 mediante ICMP con la puerta de enlace.

hechos_prueba_ping_gateway_ok = {
    "tipo_conexion": "e",
    "adaptador_activo": True,
    "cable_conectado": True,
    "hay_enlace": True,
    "ping_gateway_exitoso": True,
}

comprobar_caso(
    "Ping al gateway correcto",
    hechos_prueba_ping_gateway_ok,
    "comunicacion_gateway_confirmada",
    True,
    "R09",
)


# ------------------------------------------------------------
# R10 - Comunicación con el gateway no confirmada
# ------------------------------------------------------------
# Si el ping no obtiene respuesta, el motor debe indicar que
# la comunicación mediante ICMP no ha podido confirmarse.
#
# Esto no implica necesariamente que el gateway esté caído,
# ya que ICMP podría estar filtrado.

hechos_prueba_ping_gateway_falla = {
    "tipo_conexion": "e",
    "adaptador_activo": True,
    "cable_conectado": True,
    "hay_enlace": True,
    "ping_gateway_exitoso": False,
}

comprobar_caso(
    "Ping al gateway sin respuesta",
    hechos_prueba_ping_gateway_falla,
    "comunicacion_gateway_no_confirmada",
    True,
    "R10",
)

# ------------------------------------------------------------
# R11 - Comunicación externa por IP confirmada
# ------------------------------------------------------------
# Si una dirección IPv4 pública responde al ping, el motor debe
# confirmar comunicación externa por IP sin depender de DNS.

hechos_prueba_ping_internet_ok = {
    "ping_internet_exitoso": True,
}

comprobar_caso(
    "Ping a Internet por IP correcto",
    hechos_prueba_ping_internet_ok,
    "comunicacion_externa_ip_confirmada",
    True,
    "R11",
)


# ------------------------------------------------------------
# R12 - Comunicación externa por IP no confirmada
# ------------------------------------------------------------
# Si el ping a la dirección IPv4 pública no obtiene respuesta,
# el motor debe indicar que la comunicación externa mediante
# ICMP no ha podido confirmarse.

hechos_prueba_ping_internet_falla = {
    "ping_internet_exitoso": False,
}

comprobar_caso(
    "Ping a Internet por IP sin respuesta",
    hechos_prueba_ping_internet_falla,
    "comunicacion_externa_ip_no_confirmada",
    True,
    "R12",
)

# ------------------------------------------------------------
# R13 - Resolución DNS confirmada
# ------------------------------------------------------------
# Si el dominio de prueba se resuelve correctamente, el motor
# debe confirmar que la resolución DNS funciona para esa prueba.

hechos_prueba_dns_ok = {
    "dns_resolucion_exitosa": True,
}

comprobar_caso(
    "Resolución DNS correcta",
    hechos_prueba_dns_ok,
    "dns_confirmado",
    True,
    "R13",
)

# ------------------------------------------------------------
# R14 - Posible fallo de resolución DNS
# ------------------------------------------------------------
# Si el dominio de prueba no puede resolverse, el motor debe
# señalar un posible problema de resolución DNS.

hechos_prueba_dns_falla = {
    "dns_resolucion_exitosa": False,
}

comprobar_caso(
    "Resolución DNS fallida",
    hechos_prueba_dns_falla,
    "posible_fallo_dns",
    True,
    "R14",
)

# ------------------------------------------------------------
# R15 - Problema DNS probable
# ------------------------------------------------------------
# Si existe comunicación externa confirmada por IP, pero falla
# la resolución DNS, el motor debe clasificar el problema como
# probablemente relacionado con DNS.

hechos_prueba_problema_dns = {
    "ping_internet_exitoso": True,
    "dns_resolucion_exitosa": False,
}

comprobar_caso(
    "Problema DNS probable",
    hechos_prueba_problema_dns,
    "problema_dns_probable",
    True,
    "R15",
)

# ------------------------------------------------------------
# R16 - Conectividad funcional confirmada
# ------------------------------------------------------------
# Si existe comunicación externa confirmada por IP y la
# resolución DNS funciona correctamente, el motor debe
# clasificar las comprobaciones principales como satisfactorias.

hechos_prueba_conectividad_funcional = {
    "ping_internet_exitoso": True,
    "dns_resolucion_exitosa": True,
}

comprobar_caso(
    "Conectividad funcional",
    hechos_prueba_conectividad_funcional,
    "conectividad_funcional",
    True,
    "R16",
)

# ------------------------------------------------------------
# R17 - Problema de conectividad externa probable
# ------------------------------------------------------------
# Si no puede confirmarse comunicación externa por IP y además
# falla la resolución DNS, el motor debe señalar un problema
# probable de conectividad externa.

hechos_prueba_conectividad_externa = {
    "ping_internet_exitoso": False,
    "dns_resolucion_exitosa": False,
}

comprobar_caso(
    "Problema de conectividad externa probable",
    hechos_prueba_conectividad_externa,
    "problema_conectividad_externa_probable",
    True,
    "R17",
)

# ------------------------------------------------------------
# R18 - Problema probablemente local al equipo
# ------------------------------------------------------------
# Si este equipo presenta un problema probable de conectividad
# externa, pero otros dispositivos de la misma red sí tienen
# acceso a Internet, el motor debe localizar el alcance en el equipo.

hechos_prueba_fallo_local_equipo = {
    "ping_internet_exitoso": False,
    "dns_resolucion_exitosa": False,
    "hay_otros_dispositivos": True,
    "otros_dispositivos_tienen_internet": True,
}

comprobar_caso(
    "Problema probablemente local al equipo",
    hechos_prueba_fallo_local_equipo,
    "alcance_fallo",
    "equipo",
    "R18",
)


# ------------------------------------------------------------
# R19 - Problema probablemente general de la red
# ------------------------------------------------------------
# Si este equipo presenta un problema probable de conectividad
# externa y otros dispositivos tampoco tienen Internet, el motor
# debe clasificar el alcance como un problema de red.

hechos_prueba_fallo_general_red = {
    "ping_internet_exitoso": False,
    "dns_resolucion_exitosa": False,
    "hay_otros_dispositivos": True,
    "otros_dispositivos_tienen_internet": False,
}

comprobar_caso(
    "Problema probablemente general de la red",
    hechos_prueba_fallo_general_red,
    "alcance_fallo",
    "red",
    "R19",
)


# ------------------------------------------------------------
# R20 - Alcance del fallo desconocido
# ------------------------------------------------------------
# Si existe un problema probable de conectividad externa pero
# no hay otros dispositivos disponibles para comparar, el motor
# no debe inventar el alcance del fallo.

hechos_prueba_alcance_desconocido = {
    "ping_internet_exitoso": False,
    "dns_resolucion_exitosa": False,
    "hay_otros_dispositivos": False,
}

comprobar_caso(
    "Alcance del fallo desconocido",
    hechos_prueba_alcance_desconocido,
    "alcance_fallo",
    "desconocido",
    "R20",
)


# ============================================================
# PRUEBAS DEL MOTOR DE INFERENCIA
# ============================================================


# ------------------------------------------------------------
# Detección de conflicto de conocimiento
# ------------------------------------------------------------
# Esta prueba no corresponde a una regla concreta.
#
# Comprueba que el motor detecta una contradicción cuando se
# intenta inferir para un hecho un valor diferente del que ya
# existe en la memoria de trabajo.

hechos_prueba_conflicto = {
    "interfaz_conectada": True,
}

conclusiones_conflictivas = {
    "interfaz_conectada": False,
}

try:
    aplicar_conclusiones(
        conclusiones_conflictivas,
        hechos_prueba_conflicto,
    )

    raise AssertionError("El motor no detectó el conflicto de conocimiento.")

except ValueError:
    print("[OK] Conflicto de conocimiento detectado")
