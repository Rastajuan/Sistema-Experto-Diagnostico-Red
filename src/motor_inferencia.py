# ============================================================
# MOTOR DE INFERENCIA
# ============================================================
# Este módulo contiene la lógica general que evalúa las reglas
# de la base de conocimiento.
#
# El motor NO contiene conocimiento específico sobre redes.
# No sabe qué significa Wi-Fi, Ethernet, DNS o una puerta de
# enlace.
#
# Su responsabilidad es:
#
# 1. recibir los hechos conocidos;
# 2. comprobar qué reglas cumplen todas sus condiciones;
# 3. incorporar las conclusiones de esas reglas;
# 4. registrar qué reglas se han activado;
# 5. repetir el proceso hasta que no aparezcan hechos nuevos.
#
# Este comportamiento implementará un mecanismo de
# encadenamiento hacia delante:
#
# hechos -> reglas aplicables -> nuevos hechos -> nuevas reglas
# ============================================================
def se_cumplen_condiciones(condiciones, hechos):
    for nombre_hecho, valor_esperado in condiciones.items():
        if nombre_hecho not in hechos:
            return False

        if hechos[nombre_hecho] != valor_esperado:
            return False

    return True


# ============================================================
# APLICACIÓN DE CONCLUSIONES
# ============================================================
# Cuando una regla cumple todas sus condiciones, sus conclusiones
# se incorporan a la memoria de trabajo.
#
# Esta función no decide si una regla debe activarse. Esa decisión
# corresponde a se_cumplen_condiciones().
#
# Además de añadir los hechos inferidos, la función indicará si
# la memoria de trabajo ha cambiado. Esta información será
# necesaria posteriormente para saber cuándo debe detenerse el
# encadenamiento hacia delante.
def aplicar_conclusiones(conclusiones, hechos):
    hubo_cambios = False

    for nombre_hecho, valor_inferido in conclusiones.items():
        if nombre_hecho not in hechos:
            hechos[nombre_hecho] = valor_inferido
            hubo_cambios = True

        elif hechos[nombre_hecho] != valor_inferido:
            raise ValueError(
                f"Conflicto de conocimiento para '{nombre_hecho}': "
                f"valor existente = {hechos[nombre_hecho]!r}, "
                f"valor inferido = {valor_inferido!r}"
            )

    return hubo_cambios


# ============================================================
# ENCADENAMIENTO HACIA DELANTE
# ============================================================
# El motor parte de los hechos presentes en la memoria de trabajo
# y evalúa repetidamente las reglas de la base de conocimiento.
#
# Cuando una regla cumple todas sus condiciones, se aplican sus
# conclusiones y pueden aparecer nuevos hechos.
#
# Esos nuevos hechos pueden permitir que otras reglas, que antes
# no eran aplicables, pasen a serlo.
#
# El proceso continúa hasta alcanzar un punto fijo:
# una pasada completa por todas las reglas no produce ningún
# hecho nuevo.
#
# Además, se conservará una traza de las reglas que hayan
# producido nuevo conocimiento para poder explicar posteriormente
# el razonamiento seguido por el sistema.
def encadenamiento_hacia_adelante(reglas, hechos):
    """
    Aplica repetidamente las reglas compatibles con los hechos conocidos
    hasta que no se pueda inferir ningún hecho nuevo.

    Devuelve una traza con las reglas que han producido nuevo conocimiento.
    """

    traza = []
    hubo_cambios = True

    while hubo_cambios:
        hubo_cambios = False

        for regla in reglas:
            if se_cumplen_condiciones(regla["condiciones"], hechos):
                hay_hechos_nuevos = aplicar_conclusiones(
                    regla["conclusiones"],
                    hechos,
                )

                if hay_hechos_nuevos:
                    hubo_cambios = True
                    traza.append(
                        {
                            "id": regla["id"],
                            "condiciones": regla["condiciones"],
                            "conclusiones": regla["conclusiones"],
                            "explicacion": regla["explicacion"],
                        }
                    )
    return traza
