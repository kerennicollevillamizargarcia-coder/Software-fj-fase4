main.py
from excepciones_y_logs import RegistradorLogs, ErrorValidacionDato, ErrorCalculoCosto  # Importa logs y excepciones[cite: 4]
from entidades_y_servicios import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada  # Importa clases del Commit 3[cite: 4]
from reservas_y_gestion import GestorSoftwareFJ  # Importa el gestor del Commit 4[cite: 4]


def ejecutar_simulacion() -> None:  # Ejecuta de forma secuencial las operaciones de prueba del sistema
    registrador = RegistradorLogs("registro_software_fj.log")  # Crea el registrador de eventos y errores en archivo .log[cite: 4]
    gestor = GestorSoftwareFJ(registrador)  # Inicializa el gestor en memoria (sin base de datos)
    registrador.registrar("INICIO", "Iniciando simulación de Software FJ - Fase 4.")  # Registra inicio de ejecución[cite: 4]

    # --- OPERACIÓN 1: Registro válido de cliente ---
    print("Op 1: Registrando cliente válido...")  # Muestra avance en consola[cite: 1]
    cliente_1 = Cliente("CLI-01", "Laura Gómez", "laura.gomez@empresa.com", activo=True)  # Crea cliente válido[cite: 4]
    gestor.registrar_cliente(cliente_1)  # Registra el cliente en la lista interna y en el log[cite: 3, 4]

    # --- OPERACIÓN 2: Registro inválido de cliente (correo incorrecto) ---
    print("Op 2: Intentando registrar cliente con correo inválido...")  # Muestra avance en consola[cite: 1]
    try:  # Intenta construir un cliente con correo inválido[cite: 4]
        cliente_invalido = Cliente("CLI-02", "Carlos Ruiz", "correo-sin-arroba", activo=True)  # Lanza ErrorValidacionDato[cite: 4]
        gestor.registrar_cliente(cliente_invalido)  # No se alcanza si falla la validación[cite: 4]
    except ErrorValidacionDato as err:  # Captura el error de validación[cite: 4]
        registrador.registrar("ERROR", f"Op 2 fallida al crear cliente: {err}")  # Registra el error en el archivo .log[cite: 4]

    # --- OPERACIÓN 3: Registro válido de segundo cliente ---
    print("Op 3: Registrando segundo cliente válido...")  # Muestra avance en consola[cite: 1]
    cliente_3 = Cliente("CLI-03", "Andrés Mendoza", "andres.mendoza@correo.co", activo=True)  # Crea segundo cliente válido[cite: 4]
    gestor.registrar_cliente(cliente_3)  # Agrega el cliente a la lista interna[cite: 3, 4]

    # --- OPERACIÓN 4: Registro de cliente inactivo (para probar bloqueo posterior en reservas) ---
    print("Op 4: Registrando cliente inactivo...")  # Muestra avance en consola[cite: 1]
    cliente_4 = Cliente("CLI-04", "Sofía Herrera", "sofia.herrera@correo.com", activo=False)  # Crea cliente inactivo[cite: 4]
    gestor.registrar_cliente(cliente_4)  # Registra el cliente inactivo[cite: 3, 4]

    # --- OPERACIÓN 5: Creación válida del servicio 1 (Reserva de sala) ---
    print("Op 5: Registrando servicio de reserva de sala...")  # Muestra avance en consola[cite: 1]
    sala_1 = ReservaSala("SRV-SALA-1", "Sala de Conferencias A", tarifa_base=40.0, capacidad_personas=20, disponible=True)  # Sala[cite: 4]
    gestor.registrar_servicio(sala_1)  # Registra la sala en la lista de servicios[cite: 3, 4]

    # --- OPERACIÓN 6: Creación válida del servicio 2 (Alquiler de equipos) ---
    print("Op 6: Registrando servicio de alquiler de equipos...")  # Muestra avance en consola[cite: 1]
    equipo_1 = AlquilerEquipo("SRV-EQ-1", "Portátil Corporativo i7", tarifa_base=15.0, stock_disponible=5, disponible=True)  # Equipo[cite: 4]
    gestor.registrar_servicio(equipo_1)  # Registra el equipo en la lista de servicios[cite: 3, 4]

    # --- OPERACIÓN 7: Creación válida del servicio 3 (Asesoría especializada) ---
    print("Op 7: Registrando servicio de asesoría especializada...")  # Muestra avance en consola[cite: 1]
    asesoria_1 = AsesoriaEspecializada("SRV-ASE-1", "Arquitectura de Software", tarifa_base=60.0, especialidad="Cloud & POO")  # Asesoría[cite: 4]
    gestor.registrar_servicio(asesoria_1)  # Registra la asesoría en la lista de servicios[cite: 3, 4]

    # --- OPERACIÓN 8: Creación incorrecta de servicio (tarifa negativa) ---
    print("Op 8: Intentando crear servicio con tarifa inválida...")  # Muestra avance en consola[cite: 1]
    try:  # Intenta crear un servicio con tarifa base negativa[cite: 4]
        servicio_malo = AlquilerEquipo("SRV-EQ-ERR", "Proyector HD", tarifa_base=-10.0, stock_disponible=3)  # Lanza ErrorCalculoCosto[cite: 4]
        gestor.registrar_servicio(servicio_malo)  # No se ejecuta si falla el constructor[cite: 4]
    except ErrorCalculoCosto as err:  # Captura error de cálculo/tarifa[cite: 4]
        registrador.registrar("ERROR", f"Op 8 fallida al crear servicio: {err}")  # Registra en archivo de logs[cite: 4]

    # --- OPERACIÓN 9: Reserva exitosa de sala con descuento e impuesto opcionales ---
    print("Op 9: Procesando reserva exitosa de sala...")  # Muestra avance en consola[cite: 1]
    gestor.crear_y_procesar_reserva(  # Crea, confirma y procesa reserva válida de sala[cite: 4]
        id_reserva="RES-01",  # ID de la reserva[cite: 4]
        id_cliente="CLI-01",  # Cliente activo Laura Gómez[cite: 4]
        id_servicio="SRV-SALA-1",  # Sala de Conferencias A[cite: 4]
        duracion_horas=3,  # 3 horas de uso[cite: 4]
        cantidad_unidades=10,  # 10 asistentes (dentro de capacidad 20)[cite: 4]
        descuento_pct=10.0,  # 10% de descuento opcional[cite: 4]
        impuesto_pct=5.0,  # 5% de impuesto opcional[cite: 4]
        confirmar_y_procesar=True,  # Confirma y procesa la reserva[cite: 4]
    )  # Fin de operación 9[cite: 4]

    # --- OPERACIÓN 10: Reserva exitosa de alquiler de equipos ---
    print("Op 10: Procesando reserva exitosa de alquiler de equipos...")  # Muestra avance en consola[cite: 1]
    gestor.crear_y_procesar_reserva(  # Crea, confirma y procesa reserva válida de equipos[cite: 4]
        id_reserva="RES-02",  # ID de la reserva[cite: 4]
        id_cliente="CLI-03",  # Cliente activo Andrés Mendoza[cite: 4]
        id_servicio="SRV-EQ-1",  # Portátil Corporativo i7[cite: 4]
        duracion_horas=4,  # 4 horas de alquiler[cite: 4]
        cantidad_unidades=2,  # 2 equipos (dentro de stock 5)[cite: 4]
        confirmar_y_procesar=True,  # Confirma y procesa[cite: 4]
    )  # Fin de operación 10[cite: 4]

    # --- OPERACIÓN 11: Reserva fallida por exceder stock de equipos (encadenamiento de excepciones) ---
    print("Op 11: Intentando reserva fallida por stock insuficiente...")  # Muestra avance en consola[cite: 1]
    gestor.crear_y_procesar_reserva(  # Intenta reservar más equipos de los disponibles[cite: 4]
        id_reserva="RES-03",  # ID de la reserva fallida[cite: 4]
        id_cliente="CLI-01",  # Cliente válido[cite: 4]
        id_servicio="SRV-EQ-1",  # Portátil Corporativo i7 (stock 5)[cite: 4]
        duracion_horas=2,  # 2 horas[cite: 4]
        cantidad_unidades=9,  # 9 unidades exceden el stock de 5[cite: 4]
        confirmar_y_procesar=True,  # Intenta confirmar y procesar[cite: 4]
    )  # Fin de operación 11[cite: 4]

    # --- OPERACIÓN 12: Reserva fallida por cliente inactivo y reserva exitosa de asesoría ---
    print("Op 12a: Intentando reserva con cliente inactivo...")  # Muestra avance en consola[cite: 1]
    gestor.crear_y_procesar_reserva(  # Falla de forma controlada porque CLI-04 está inactivo[cite: 4]
        id_reserva="RES-04",  # ID de reserva fallida[cite: 4]
        id_cliente="CLI-04",  # Cliente inactivo Sofía Herrera[cite: 4]
        id_servicio="SRV-ASE-1",  # Asesoría especializada[cite: 4]
        duracion_horas=2,  # 2 horas[cite: 4]
        cantidad_unidades=1,  # 1 sesión[cite: 4]
    )  # Fin de operación 12a[cite: 4]

    print("Op 12b: Procesando reserva exitosa de asesoría especializada...")  # Muestra avance en consola[cite: 1]
    gestor.crear_y_procesar_reserva(  # Operación válida adicional de asesoría[cite: 4]
        id_reserva="RES-05",  # ID de reserva válida[cite: 4]
        id_cliente="CLI-03",  # Cliente activo Andrés Mendoza[cite: 4]
        id_servicio="SRV-ASE-1",  # Asesoría especializada[cite: 4]
        duracion_horas=2,  # 2 horas[cite: 4]
        cantidad_unidades=1,  # 1 consultor/sesión[cite: 4]
        confirmar_y_procesar=True,  # Confirma y procesa[cite: 4]
    )  # Fin de operación 12b[cite: 4]

    # --- RESUMEN FINAL EN CONSOLA ---
    print("\n=== RESUMEN FINAL DEL SISTEMA SOFTWARE FJ ===")  # Encabezado de resumen[cite: 4]
    print(f"Clientes registrados en memoria: {len(gestor.clientes)}")  # Muestra total de clientes válidos[cite: 3, 4]
    for cli in gestor.clientes:  # Recorre clientes registrados[cite: 4]
        print(" -", cli.describir())  # Imprime descripción polimórfica de cada cliente[cite: 4]

    print(f"\nServicios registrados en memoria: {len(gestor.servicios)}")  # Muestra total de servicios válidos[cite: 3, 4]
    for srv in gestor.servicios:  # Recorre servicios registrados[cite: 4]
        print(" -", srv.describir())  # Imprime descripción polimórfica de cada servicio[cite: 4]

    print(f"\nReservas procesadas en memoria: {len(gestor.reservas)}")  # Muestra total de reservas exitosas[cite: 3, 4]
    for res in gestor.reservas:  # Recorre reservas guardadas[cite: 4]
        print(" -", res.resumen())  # Imprime resumen de cada reserva[cite: 4]

    registrador.registrar("FIN", "Simulación finalizada correctamente sin interrupciones.")  # Registra fin estable[cite: 3, 4]


if __name__ == "__main__":  # Asegura que ejecutar_simulacion() corra al ejecutar main.py directamente
    ejecutar_simulacion()  # Llama a la función principal de simulación
