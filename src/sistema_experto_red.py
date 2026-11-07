from src.reglas import reglas
from src.motor_inferencia import encadenamiento_hacia_adelante
import ipaddress


def pedir_ipv4(mensaje, ayuda):
    """
    Solicita al usuario una dirección IPv4 y repite la petición
    hasta obtener una dirección sintácticamente válida.

    Si el usuario introduce "?", muestra el texto de ayuda recibido
    como parámetro y vuelve a solicitar la dirección.

    Devuelve un objeto IPv4Address para poder realizar después
    comprobaciones técnicas sobre la dirección.
    """

    while True:
        entrada = input(mensaje).strip()

        if entrada == "?":
            print(ayuda)
            continue

        try:
            direccion = ipaddress.ip_address(entrada)

            if isinstance(direccion, ipaddress.IPv4Address):
                return direccion

            print("La dirección es válida, pero no es IPv4. Es IPv6.")

        except ValueError:
            print("La dirección introducida no es una dirección IP válida.")


def pedir_si_no(mensaje, ayuda=None):
    """
    Solicita al usuario una respuesta de tipo sí/no.

    Devuelve True para "s" y False para "n".

    Si se proporciona un texto de ayuda, el usuario puede introducir
    "?" para mostrarlo y volver a responder.
    """

    while True:
        respuesta = input(mensaje).lower().strip()

        if respuesta in ("s", "n"):
            return respuesta == "s"

        if respuesta == "?" and ayuda is not None:
            print(ayuda)
            continue

        if ayuda is not None:
            print("Introduzca una opción válida: s / n / ? para ayuda.")
        else:
            print("Introduzca una opción válida: s / n.")


def mostrar_resultado(hechos, traza):
    """
    Muestra al usuario el resultado final del diagnóstico,
    las recomendaciones correspondientes y la secuencia de
    reglas que han producido nuevo conocimiento.

    Esta función presenta información ya obtenida por el sistema.
    No modifica la memoria de trabajo ni ejecuta nuevas reglas.
    """

    print("\n" + "=" * 60)
    print("RESULTADO DEL DIAGNÓSTICO")
    print("=" * 60)

    # --------------------------------------------------------
    # DIAGNÓSTICO PRINCIPAL
    # --------------------------------------------------------
    print("\nDiagnóstico principal:")

    if hechos.get("interfaz_conectada") is False:
        print("- La interfaz de red no ha establecido conexión con la red.")

    elif hechos.get("posible_fallo_dhcp", False):
        print(
            "- Se ha detectado una dirección APIPA. "
            "Existe un posible problema al obtener la "
            "configuración mediante DHCP."
        )

    elif hechos.get("posible_fallo_configuracion_ip", False):
        print(
            "- No existe una puerta de enlace predeterminada. "
            "La configuración IP puede estar incompleta o ser incorrecta."
        )

    elif hechos.get("problema_dns_probable", False):
        print(
            "- La comunicación externa por IP funciona, pero falla "
            "la resolución de nombres. El problema parece estar "
            "relacionado con DNS."
        )

    elif hechos.get("problema_conectividad_externa_probable", False):
        alcance = hechos.get("alcance_fallo", "desconocido")

        if alcance == "equipo":
            print(
                "- Existe un problema probable de conectividad externa "
                "localizado en este equipo."
            )

        elif alcance == "red":
            print(
                "- Existe un problema probable de conectividad externa "
                "que parece afectar a la red en general."
            )

        else:
            print(
                "- Existe un problema probable de conectividad externa, "
                "pero no se ha podido determinar su alcance."
            )

    elif hechos.get("conectividad_funcional", False):
        print(
            "- Las comprobaciones principales de conectividad "
            "han resultado satisfactorias."
        )

    else:
        print(
            "- Con la información disponible no se ha podido establecer "
            "un diagnóstico concluyente."
        )

    # --------------------------------------------------------
    # RECOMENDACIONES
    # --------------------------------------------------------
    print("\nRecomendaciones:")

    recomendaciones = []

    if hechos.get("recomendar_activar_adaptador", False):
        recomendaciones.append(
            "Activar el adaptador de red correspondiente en Windows "
            "y repetir el diagnóstico."
        )

    if hechos.get("recomendar_conectar_wifi", False):
        recomendaciones.append(
            "Conectar el equipo a una red Wi-Fi disponible y comprobar "
            "de nuevo la conectividad."
        )

    if hechos.get("recomendar_conectar_cable", False):
        recomendaciones.append(
            "Conectar correctamente el cable Ethernet al equipo "
            "y al dispositivo de red."
        )

    if hechos.get("recomendar_revisar_enlace_ethernet", False):
        recomendaciones.append(
            "Revisar el cable Ethernet, el puerto utilizado y el "
            "dispositivo situado al otro extremo de la conexión."
        )

    if hechos.get("recomendar_revisar_dhcp", False):
        recomendaciones.append(
            "Revisar la obtención automática de la configuración IP "
            "mediante DHCP antes de continuar con otras comprobaciones."
        )

    if hechos.get("recomendar_revisar_configuracion_ip", False):
        recomendaciones.append(
            "Revisar la configuración IPv4 del equipo y comprobar "
            "que exista una puerta de enlace predeterminada adecuada."
        )

    if hechos.get("recomendar_revisar_dns", False):
        recomendaciones.append(
            "Revisar los servidores DNS configurados y realizar nuevas "
            "pruebas de resolución de nombres."
        )

    if hechos.get("recomendar_revisar_equipo", False):
        recomendaciones.append(
            "Centrar las siguientes comprobaciones en este equipo, "
            "revisando su configuración de red, DNS, firewall y adaptador."
        )

    if hechos.get("recomendar_revisar_red", False):
        recomendaciones.append(
            "Revisar los elementos comunes de la red, como el router "
            "o la conexión proporcionada por el proveedor de Internet."
        )

    if hechos.get("recomendar_ampliar_comprobaciones", False):
        recomendaciones.append(
            "Comprobar la conectividad desde otro dispositivo de la misma "
            "red antes de atribuir el fallo al equipo o a la infraestructura."
        )

    if recomendaciones:
        for recomendacion in recomendaciones:
            print(f"- {recomendacion}")

    elif hechos.get("conectividad_funcional", False):
        print(
            "- No se requieren acciones correctivas según las "
            "comprobaciones realizadas."
        )

    else:
        print(
            "- No hay información suficiente para proponer una "
            "acción correctiva específica."
        )

    # --------------------------------------------------------
    # TRAZA DE RAZONAMIENTO
    # --------------------------------------------------------
    print("\nRazonamiento seguido:")

    for paso in traza:
        print(f"- {paso['id']}: {paso['explicacion']}")


def main():

    # ============================================================
    # SISTEMA EXPERTO PARA DIAGNÓSTICO BÁSICO DE CONECTIVIDAD
    # ============================================================
    # Este módulo coordina el flujo principal del sistema experto.
    #
    # Su responsabilidad es:
    #
    # 1. solicitar al usuario los datos necesarios;
    # 2. transformarlos en hechos de la memoria de trabajo;
    # 3. ejecutar progresivamente el motor de inferencia;
    # 4. incorporar nuevos hechos obtenidos durante el diagnóstico;
    # 5. conservar la traza del razonamiento realizado.
    #
    # El conocimiento del dominio se encuentra en reglas.py y la
    # lógica general de inferencia en motor_inferencia.py.
    # ============================================================

    tipo_conexion = (
        input("¿Utiliza conexión Wi-Fi (w) o Ethernet-por cable (e)? ").lower().strip()
    )

    while tipo_conexion not in ("w", "e"):
        tipo_conexion = (
            input("Introduzca un valor válido: " "'w' (Wi-Fi) / 'e' (Ethernet): ")
            .lower()
            .strip()
        )

    if tipo_conexion == "w":
        print("Ha elegido conexión por Wi-Fi")
    else:
        print("Ha elegido conexión por Ethernet")

    # ------------------------------------------------------------
    # 2. ESTADO DEL ADAPTADOR DE RED
    # ------------------------------------------------------------
    # Antes de realizar comprobaciones específicas de Wi-Fi o Ethernet
    # es necesario saber si el adaptador utilizado está habilitado.
    #
    # Si el adaptador está desactivado, no tendría sentido continuar
    # preguntando por conexión Wi-Fi, cable Ethernet o enlace.
    #
    # Esta comprobación admite ayuda porque localizar el estado del
    # adaptador en Windows puede no resultar evidente para todos los
    # usuarios.

    ayuda_adaptador = (
        "Pulsa Win + R, escribe ncpa.cpl y pulsa Enter.\n\n"
        "Busca el adaptador Wi-Fi o Ethernet que estás utilizando.\n"
        'Si aparece deshabilitado, responde "n".\n'
        'Si está habilitado, responde "s".'
    )
    adaptador_activo = pedir_si_no(
        "¿Está activada en Windows la conexión de red que estás "
        "utilizando? (s/n, ? para ayuda): ",
        ayuda_adaptador,
    )

    # ------------------------------------------------------------
    # 3. COMPROBACIONES SEGÚN EL TIPO DE CONEXIÓN
    # ------------------------------------------------------------
    # Estas comprobaciones solo se realizan si el adaptador de red
    # correspondiente está habilitado.
    #
    # Cada tipo de conexión necesita hechos diferentes:
    # - Wi-Fi: comprobar si la interfaz está asociada a una red.
    # - Ethernet: comprobar cable y existencia de enlace físico.
    #
    # Estos datos permiten al sistema inferir posteriormente si la
    # interfaz ha establecido conexión con la red.

    if adaptador_activo:

        # --------------------------------------------------------
        # 3.1. RAMA WI-FI
        # --------------------------------------------------------
        # En una conexión Wi-Fi interesa comprobar si la interfaz
        # está asociada a una red inalámbrica.
        #
        # Estar conectado a una red Wi-Fi NO implica necesariamente
        # disponer de una configuración IPv4 correcta ni tener
        # acceso a Internet.
        #
        # En esta fase solo obtenemos el hecho necesario para que
        # el motor determine el estado de la interfaz.
        if tipo_conexion == "w":

            wifi_conectado = pedir_si_no(
                "¿Windows indica que el equipo está conectado "
                "a una red Wi-Fi? (s/n): "
            )

        # --------------------------------------------------------
        # 3.2. RAMA ETHERNET
        # --------------------------------------------------------
        # En una conexión Ethernet se comprueban dos niveles:
        #
        # 1. que exista un cable conectado físicamente al equipo;
        # 2. que la interfaz haya establecido enlace con el otro extremo.
        #
        # Cable conectado y enlace Ethernet NO son equivalentes.
        # Un cable puede estar conectado sin que exista comunicación
        # física válida con el dispositivo situado al otro extremo.
        #
        # Estas comprobaciones permiten obtener los hechos necesarios
        # para que el motor determine el estado de la interfaz.
        elif tipo_conexion == "e":

            cable_conectado = pedir_si_no(
                "¿El cable Ethernet está conectado al equipo? (s/n): "
            )

            # La existencia de enlace solo se comprueba si previamente
            # sabemos que hay un cable conectado.
            #
            # Si no existe cable, preguntar por el estado del enlace no
            # aportaría información adicional y rompería la secuencia
            # lógica de adquisición de hechos.

            if cable_conectado:

                hay_enlace = pedir_si_no(
                    "¿Windows detecta la conexión Ethernet y no "
                    "muestra 'cable de red desconectado'? (s/n): "
                )
    # ============================================================
    # 4. CREACIÓN DE LA MEMORIA DE TRABAJO
    # ============================================================
    # Hasta este punto se han obtenido hechos directos a partir
    # de las respuestas y comprobaciones realizadas por el usuario.
    #
    # La memoria de trabajo contiene únicamente los hechos que el
    # sistema conoce en el momento actual.
    #
    # No todos los hechos existen siempre. Algunos dependen de las
    # respuestas anteriores y del tipo de conexión seleccionado.
    #
    # IMPORTANTE:
    # La ausencia de un hecho NO significa que su valor sea False.
    # Significa que el sistema todavía no dispone de esa información.
    #
    # A partir de esta memoria, el motor podrá inferir nuevos hechos
    # mediante las reglas de la base de conocimiento.

    hechos = {
        "tipo_conexion": tipo_conexion,
        "adaptador_activo": adaptador_activo,
    }

    # Los hechos específicos de cada interfaz solo existen si el
    # adaptador correspondiente estaba activo y pudieron comprobarse.
    if adaptador_activo:

        if tipo_conexion == "w":
            hechos["wifi_conectado"] = wifi_conectado

        elif tipo_conexion == "e":
            hechos["cable_conectado"] = cable_conectado

            if cable_conectado:
                hechos["hay_enlace"] = hay_enlace

    # ------------------------------------------------------------
    # 4.1. PRIMERA EJECUCIÓN DEL MOTOR DE INFERENCIA
    # ------------------------------------------------------------
    # Una vez creada la memoria de trabajo con los hechos iniciales,
    # el motor evalúa las reglas de la base de conocimiento.
    #
    # Las conclusiones obtenidas se incorporan directamente a la
    # memoria de trabajo y las reglas que hayan producido nuevo
    # conocimiento quedan registradas en la traza.
    traza = encadenamiento_hacia_adelante(reglas, hechos)

    # ============================================================
    # 5. ADQUISICIÓN DE INFORMACIÓN DE CONFIGURACIÓN IP
    # ============================================================
    # Esta fase solo se ejecuta si el motor de inferencia ha
    # determinado que la interfaz está conectada a una red.
    #
    # A partir de este punto se recopilan datos técnicos necesarios
    # para comprobar progresivamente:
    #
    # - configuración IPv4;
    # - comunicación con la puerta de enlace;
    # - acceso a Internet mediante dirección IP;
    # - resolución de nombres DNS.
    #
    # Las comprobaciones son exclusivamente de diagnóstico y no
    # realizan cambios automáticos en la configuración del equipo.
    if hechos["interfaz_conectada"]:
        # --------------------------------------------------------
        # 5.1. OBTENCIÓN Y VALIDACIÓN DE LA DIRECCIÓN IPv4
        # --------------------------------------------------------
        # El usuario obtiene la dirección IPv4 mediante ipconfig.
        #
        # En esta fase solo se comprueba que el dato introducido sea
        # sintácticamente una dirección IPv4 válida.
        #
        # IMPORTANTE:
        # Una dirección puede ser válida y, aun así, no representar
        # una configuración adecuada para la red utilizada.
        #
        # Por ejemplo, una dirección del rango 169.254.0.0/16 es una
        # IPv4 válida y link-local. En Windows suele aparecer cuando
        # no se ha obtenido correctamente una configuración mediante DHCP.
        #
        # La interpretación diagnóstica no se realiza aquí: se transforma
        # la información técnica en hechos y las reglas determinarán
        # posteriormente qué conclusiones pueden inferirse.
        ayuda_ipv4_equipo = (
            "Pulsa Win + R, escribe cmd y pulsa Enter.\n"
            "Ejecuta el comando: ipconfig\n\n"
            "Busca el adaptador que estás utilizando:\n"
            "- Wi-Fi si utilizas conexión inalámbrica.\n"
            "- Ethernet si utilizas cable.\n\n"
            'Localiza la línea "Dirección IPv4".\n'
            "Ejemplo: 192.168.1.34"
        )

        ipv4_equipo = pedir_ipv4(
            "Introduce la dirección IPv4 mostrada por ipconfig "
            "o escribe '?' si necesitas ayuda: ",
            ayuda_ipv4_equipo,
        )

        # --------------------------------------------------------
        # 5.2. INCORPORACIÓN DE HECHOS SOBRE LA DIRECCIÓN IPv4
        # --------------------------------------------------------
        # La dirección validada se incorpora a la memoria de trabajo
        # como un hecho conocido por el sistema.
        #
        # Además, se obtiene una característica técnica objetiva:
        # si la dirección pertenece al rango IPv4 link-local
        # 169.254.0.0/16.
        #
        # Esta comprobación constituye preprocesamiento técnico.
        # Todavía no se interpreta su significado diagnóstico.
        # Esa responsabilidad corresponde a las reglas de la base
        # de conocimiento.

        hechos["direccion_ipv4"] = str(ipv4_equipo)
        hechos["es_apipa"] = ipv4_equipo.is_link_local

        # --------------------------------------------------------
        # 5.3. NUEVA INFERENCIA TRAS OBTENER LA IPv4
        # --------------------------------------------------------
        # La memoria de trabajo contiene ahora nuevos hechos sobre
        # la configuración IPv4 del equipo.
        #
        # Se vuelve a ejecutar el motor porque estos hechos pueden
        # satisfacer reglas que antes no podían activarse.
        #
        # Las reglas que produzcan nuevo conocimiento se añaden a la
        # traza existente para conservar el razonamiento completo
        # seguido durante toda la ejecución.

        traza.extend(encadenamiento_hacia_adelante(reglas, hechos))

        # --------------------------------------------------------
        # 5.4. DECISIÓN DE CONTINUIDAD DEL DIAGNÓSTICO IP
        # --------------------------------------------------------
        # Si el sistema ha inferido un posible fallo de DHCP a partir
        # de una dirección APIPA, no se continúa todavía con las
        # comprobaciones de gateway, Internet o DNS.
        #
        # En ese caso ya existe una anomalía suficientemente temprana
        # en la configuración IP que debe tratarse antes de avanzar.
        #
        # Si no se ha inferido un posible fallo de DHCP, el diagnóstico
        # puede continuar con la comprobación de la puerta de enlace.

        if not hechos.get("posible_fallo_dhcp", False):
            # ----------------------------------------------------
            # 5.5. COMPROBACIÓN DE LA PUERTA DE ENLACE
            # ----------------------------------------------------
            # Se comprueba primero si Windows dispone de una puerta
            # de enlace predeterminada configurada.
            #
            # No se solicita todavía su dirección: primero debemos
            # saber si ese dato existe realmente en la configuración.
            ayuda_gateway = (
                "Pulsa Win + R, escribe cmd y pulsa Enter.\n"
                "Ejecuta el comando: ipconfig\n\n"
                "Busca el adaptador que estás utilizando y localiza "
                'la línea "Puerta de enlace predeterminada".\n'
                'Si aparece una dirección IPv4, responde "s".\n'
                'Si no aparece ninguna dirección, responde "n".'
            )

            gateway_configurado = pedir_si_no(
                "¿Aparece una puerta de enlace predeterminada en ipconfig? "
                "(s/n, ? para ayuda): ",
                ayuda_gateway,
            )

            hechos["gateway_configurado"] = gateway_configurado

            traza.extend(encadenamiento_hacia_adelante(reglas, hechos))

            if gateway_configurado:
                ayuda_ipv4_gateway = (
                    "Pulsa Win + R, escribe cmd y pulsa Enter.\n"
                    "Ejecuta el comando: ipconfig\n\n"
                    "Busca el adaptador que estás utilizando y localiza "
                    'la línea "Puerta de enlace predeterminada".\n'
                    "Introduce la dirección IPv4 que aparece en esa línea.\n"
                    "Ejemplo: 192.168.1.1"
                )

                ipv4_gateway = pedir_ipv4(
                    "Introduce la dirección IPv4 de la puerta de enlace "
                    "o escribe '?' si necesitas ayuda: ",
                    ayuda_ipv4_gateway,
                )

                hechos["direccion_gateway"] = str(ipv4_gateway)

                # ----------------------------------------------------
                # 5.6. COMPROBACIÓN DE COMUNICACIÓN CON EL GATEWAY
                # ----------------------------------------------------
                # Se comprueba si la puerta de enlace responde a una prueba
                # ICMP mediante el comando ping.
                #
                # El resultado del ping se almacena como un hecho técnico.
                # Su interpretación diagnóstica corresponderá posteriormente
                # a las reglas del sistema experto.

                ayuda_ping_gateway = (
                    "Pulsa Win + R, escribe cmd y pulsa Enter.\n"
                    f"Ejecuta el comando: ping {ipv4_gateway}\n\n"
                    'Si aparecen respuestas del tipo "Respuesta desde...", responde "s".\n'
                    "Si aparecen mensajes de tiempo de espera o destino inaccesible, "
                    'responde "n".'
                )

                ping_gateway_exitoso = pedir_si_no(
                    f"¿La puerta de enlace {ipv4_gateway} responde al ping? "
                    "(s/n, ? para ayuda): ",
                    ayuda_ping_gateway,
                )

                hechos["ping_gateway_exitoso"] = ping_gateway_exitoso

                traza.extend(encadenamiento_hacia_adelante(reglas, hechos))

                # ----------------------------------------------------
                # 5.7. COMPROBACIÓN DE COMUNICACIÓN EXTERNA POR IP
                # ----------------------------------------------------
                # Se realiza una prueba contra una dirección IPv4 pública
                # conocida para comprobar si existe comunicación fuera de
                # la red local sin depender todavía de la resolución DNS.
                #
                # El resultado del ping se almacena como un hecho técnico.
                # Un fallo de respuesta ICMP no demuestra por sí solo que
                # no exista acceso a Internet.

                ip_prueba_internet = "1.1.1.1"

                ayuda_ping_internet = (
                    "Pulsa Win + R, escribe cmd y pulsa Enter.\n"
                    f"Ejecuta el comando: ping {ip_prueba_internet}\n\n"
                    'Si aparecen respuestas del tipo "Respuesta desde...", responde "s".\n'
                    "Si aparecen mensajes de tiempo de espera o destino inaccesible, "
                    'responde "n".'
                )

                ping_internet_exitoso = pedir_si_no(
                    f"¿La dirección pública {ip_prueba_internet} responde al ping? "
                    "(s/n, ? para ayuda): ",
                    ayuda_ping_internet,
                )

                hechos["ping_internet_exitoso"] = ping_internet_exitoso

                traza.extend(encadenamiento_hacia_adelante(reglas, hechos))

                # ----------------------------------------------------
                # 5.8. COMPROBACIÓN DE RESOLUCIÓN DNS
                # ----------------------------------------------------
                # Se comprueba si el equipo puede resolver un nombre de dominio
                # mediante el servicio DNS configurado.
                #
                # Esta prueba se mantiene separada de la conectividad por IP
                # para poder distinguir problemas de acceso a red de problemas
                # específicos de resolución de nombres.

                dominio_prueba_dns = "example.com"

                ayuda_dns = (
                    "Pulsa Win + R, escribe cmd y pulsa Enter.\n"
                    f"Ejecuta el comando: nslookup {dominio_prueba_dns}\n\n"
                    "Si el comando devuelve el nombre del dominio junto con una "
                    'o varias direcciones IP, responde "s".\n'
                    "Si indica que no puede encontrar o resolver el dominio, "
                    'responde "n".'
                )

                dns_resolucion_exitosa = pedir_si_no(
                    f"¿Se resuelve correctamente el dominio {dominio_prueba_dns}? "
                    "(s/n, ? para ayuda): ",
                    ayuda_dns,
                )

                hechos["dns_resolucion_exitosa"] = dns_resolucion_exitosa

                traza.extend(encadenamiento_hacia_adelante(reglas, hechos))

                # ----------------------------------------------------
                # 5.9. COMPROBACIÓN DEL ALCANCE DEL PROBLEMA
                # ----------------------------------------------------
                # Si las pruebas realizadas indican un posible problema de
                # conectividad externa, se intenta determinar si afecta solo
                # a este equipo o también a otros dispositivos de la misma red.
                #
                # Para ello se comprueba primero si existe algún otro dispositivo
                # disponible con el que comparar el comportamiento.

                if hechos.get("problema_conectividad_externa_probable", False):
                    hay_otros_dispositivos = pedir_si_no(
                        "¿Hay otro dispositivo conectado a la misma red "
                        "con el que puedas comprobar el acceso a Internet? (s/n): "
                    )

                    hechos["hay_otros_dispositivos"] = hay_otros_dispositivos

                    if hay_otros_dispositivos:
                        otros_dispositivos_tienen_internet = pedir_si_no(
                            "¿Esos otros dispositivos tienen acceso a Internet? (s/n): "
                        )

                        hechos["otros_dispositivos_tienen_internet"] = (
                            otros_dispositivos_tienen_internet
                        )

                    traza.extend(encadenamiento_hacia_adelante(reglas, hechos))

    mostrar_resultado(hechos, traza)


if __name__ == "__main__":
    main()
