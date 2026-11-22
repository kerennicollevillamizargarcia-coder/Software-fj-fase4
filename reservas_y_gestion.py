reservas_y_gestion.py
from datetime import datetime  # Importa datetime para registrar marcas de tiempo en reservas[cite: 3, 4]
from excepciones_y_logs import (  # Importa excepciones personalizadas y registrador de logs del Commit 2
    ErrorValidacionDato,  # Excepción para datos inválidos o faltantes[cite: 4]
    ErrorOperacionNoPermitida,  # Excepción para acciones no permitidas según el estado[cite: 4]
    ErrorReserva,  # Excepción para fallos en reservas[cite: 4]
    ErrorCalculoCosto,  # Excepción para cálculos inconsistentes[cite: 4]
    RegistradorLogs,  # Clase para guardar eventos y errores en el archivo .log[cite: 4]
)
from entidades_y_servicios import Cliente, Servicio  # Importa Cliente y Servicio del Commit 3[cite: 1, 4]


class CalculadoraCostos:  # Implementa variantes/sobrecarga de cálculo de costos con parámetros opcionales[cite: 4]
    """Calcula costos de servicios con variantes opcionales de descuento e impuesto."""  # Documenta la clase[cite: 4]

    @staticmethod  # Método estático que permite calcular costo base o con descuento/impuesto opcionales[cite: 4]
    def calcular(
        servicio: Servicio,  # Servicio al cual se le calculará el costo[cite: 4]
        duracion_horas: int,  # Duración solicitada en horas[cite: 4]
        cantidad_unidades: int = 1,  # Parámetro opcional: cantidad de unidades/sesiones (por defecto 1)[cite: 4]
        descuento_pct: float = 0.0,  # Parámetro opcional: porcentaje de descuento (0.0 a 50.0)[cite: 4]
        impuesto_pct: float = 0.0,  # Parámetro opcional: porcentaje de impuesto (0.0 a 30.0)[cite: 4]
    ) -> float:  # Retorna el costo final calculado[cite: 4]
        if not isinstance(servicio, Servicio):  # Verifica que el objeto sea instancia de Servicio[cite: 4]
            raise ErrorCalculoCosto("El servicio proporcionado para calcular el costo no es válido.")  # Lanza error[cite: 4]

        if isinstance(descuento_pct, bool) or not isinstance(descuento_pct, (int, float)) or not (0.0 <= descuento_pct <= 50.0):
            raise ErrorCalculoCosto("El porcentaje de descuento debe estar entre 0% y 50%.")  # Valida descuento[cite: 4]

        if isinstance(impuesto_pct, bool) or not isinstance(impuesto_pct, (int, float)) or not (0.0 <= impuesto_pct <= 30.0):
            raise ErrorCalculoCosto("El porcentaje de impuesto debe estar entre 0% y 30%.")  # Valida impuesto[cite: 4]

        try:  # Intenta calcular el subtotal usando el método polimórfico del servicio[cite: 4]
            subtotal = servicio.calcular_costo(duracion_horas, cantidad_unidades)  # Calcula costo base del servicio[cite: 4]
        except ErrorValidacionDato as exc:  # Captura error de validación de parámetros del servicio[cite: 4]
            raise ErrorCalculoCosto("No fue posible calcular el costo por parámetros inválidos del servicio.") from exc  # Encadena[cite: 4]

        monto_descuento = subtotal * (float(descuento_pct) / 100.0)  # Calcula valor monetario del descuento[cite: 4]
        base_con_descuento = subtotal - monto_descuento  # Aplica el descuento al subtotal[cite: 4]
        monto_impuesto = base_con_descuento * (float(impuesto_pct) / 100.0)  # Calcula impuesto sobre base neta[cite: 4]
        total = base_con_descuento + monto_impuesto  # Calcula el total final[cite: 4]

        if total <= 0:  # Verifica que el costo final no sea cero ni negativo[cite: 4]
            raise ErrorCalculoCosto("El costo total calculado es inconsistente o menor/igual a cero.")  # Lanza error[cite: 4]

        return round(float(total), 2)  # Devuelve el total redondeado a dos decimales[cite: 4]


class Reserva:  # Clase Reserva que integra cliente, servicio, duración y estado[cite: 4]
    """Representa una reserva de Software FJ y gestiona su ciclo de vida con validaciones."""  # Documenta Reserva[cite: 4]

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")  # Tupla de estados permitidos[cite: 4]

    def __init__(
        self,  # Referencia a la instancia actual de Reserva[cite: 4]
        id_reserva: str,  # Identificador único de la reserva[cite: 4]
        cliente: Cliente,  # Cliente asociado a la reserva[cite: 4]
        servicio: Servicio,  # Servicio reservado[cite: 4]
        duracion_horas: int,  # Duración en horas[cite: 4]
        cantidad_unidades: int = 1,  # Cantidad de unidades solicitadas[cite: 4]
        descuento_pct: float = 0.0,  # Descuento opcional[cite: 4]
        impuesto_pct: float = 0.0,  # Impuesto opcional[cite: 4]
    ):  # Fin de parámetros del constructor[cite: 4]
        if not isinstance(id_reserva, str) or not id_reserva.strip():  # Valida ID de reserva[cite: 4]
            raise ErrorReserva("El identificador de la reserva es obligatorio.")  # Lanza ErrorReserva[cite: 4]
        if not isinstance(cliente, Cliente):  # Valida que cliente sea instancia de Cliente[cite: 4]
            raise ErrorReserva("Debe asignarse un cliente válido a la reserva.")  # Lanza ErrorReserva[cite: 4]
        if not cliente.activo:  # Impide reservas para clientes inactivos[cite: 4]
            raise ErrorReserva(f"El cliente '{cliente.nombre}' está inactivo y no puede realizar reservas.")  # Lanza error[cite: 4]
        if not isinstance(servicio, Servicio):  # Valida que servicio sea instancia de Servicio[cite: 4]
            raise ErrorReserva("Debe asignarse un servicio válido a la reserva.")  # Lanza ErrorReserva[cite: 4]
        if not servicio.disponible:  # Impide reservas de servicios no disponibles[cite: 4]
            raise ErrorReserva(f"El servicio '{servicio.nombre}' no está disponible en este momento.")  # Lanza error[cite: 4]

        self.id_reserva = id_reserva.strip()  # Guarda el ID limpio de la reserva[cite: 4]
        self.cliente = cliente  # Guarda la referencia al cliente[cite: 4]
        self.servicio = servicio  # Guarda la referencia al servicio[cite: 4]
        self.duracion_horas = duracion_horas  # Guarda la duración en horas[cite: 4]
        self.cantidad_unidades = cantidad_unidades  # Guarda la cantidad de unidades[cite: 4]
        self.estado = "PENDIENTE"  # Inicia la reserva en estado PENDIENTE[cite: 4]
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Registra fecha y hora de creación[cite: 4]
        self.costo_total = CalculadoraCostos.calcular(  # Calcula y almacena el costo total de la reserva[cite: 4]
            servicio=servicio,  # Pasa el servicio[cite: 4]
            duracion_horas=duracion_horas,  # Pasa la duración[cite: 4]
            cantidad_unidades=cantidad_unidades,  # Pasa la cantidad[cite: 4]
            descuento_pct=descuento_pct,  # Pasa el descuento[cite: 4]
            impuesto_pct=impuesto_pct,  # Pasa el impuesto[cite: 4]
        )  # Cierra llamada a CalculadoraCostos.calcular[cite: 4]

    def confirmar(self) -> None:  # Cambia el estado de la reserva a CONFIRMADA si procede[cite: 4]
        if self.estado == "CANCELADA":  # Verifica que no esté cancelada[cite: 4]
            raise ErrorOperacionNoPermitida(f"No se puede confirmar la reserva '{self.id_reserva}' porque está cancelada.")
        if self.estado == "PROCESADA":  # Verifica que no esté ya procesada[cite: 4]
            raise ErrorOperacionNoPermitida(f"La reserva '{self.id_reserva}' ya fue procesada.")  # Lanza error[cite: 4]
        self.estado = "CONFIRMADA"  # Actualiza el estado a CONFIRMADA[cite: 4]

    def cancelar(self) -> None:  # Cambia el estado de la reserva a CANCELADA si procede[cite: 4]
        if self.estado == "PROCESADA":  # Impide cancelar una reserva ya procesada[cite: 4]
            raise ErrorOperacionNoPermitida(f"No se puede cancelar la reserva '{self.id_reserva}' ya procesada.")
        if self.estado == "CANCELADA":  # Evita cancelar dos veces la misma reserva[cite: 4]
            raise ErrorOperacionNoPermitida(f"La reserva '{self.id_reserva}' ya se encuentra cancelada.")  # Lanza error[cite: 4]
        self.estado = "CANCELADA"  # Actualiza el estado a CANCELADA[cite: 4]

    def procesar(self) -> float:  # Procesa una reserva confirmada y retorna el costo cobrado[cite: 4]
        if self.estado == "CANCELADA":  # Valida que no esté cancelada[cite: 4]
            raise ErrorReserva(f"No se puede procesar la reserva '{self.id_reserva}' porque fue cancelada.")  # Lanza error[cite: 4]
        if self.estado != "CONFIRMADA":  # Exige que la reserva haya sido confirmada previamente[cite: 4]
            raise ErrorOperacionNoPermitida(
                f"La reserva '{self.id_reserva}' debe estar CONFIRMADA antes de procesarse (estado actual: {self.estado})."
            )  # Lanza error[cite: 4]
        self.estado = "PROCESADA"  # Marca la reserva como PROCESADA[cite: 4]
        return self.costo_total  # Devuelve el costo total procesado[cite: 4]

    def resumen(self) -> str:  # Genera un resumen legible de la reserva[cite: 4]
        return (  # Retorna cadena con los datos clave de la reserva[cite: 4]
            f"Reserva [{self.id_reserva}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion_horas}h | "
            f"Unidades: {self.cantidad_unidades} | Total: ${self.costo_total:.2f} | Estado: {self.estado}"
        )  # Fin de f-string[cite: 4]


class GestorSoftwareFJ:  # Administra listas internas en memoria y aplica manejo avanzado de excepciones[cite: 3, 4]
    """Gestor en memoria (sin base de datos) para clientes, servicios y reservas de Software FJ."""  # Documenta clase[cite: 3, 4]

    def __init__(self, registrador_logs: RegistradorLogs):  # Recibe el registrador de logs[cite: 4]
        self.clientes: list[Cliente] = []  # Lista interna en memoria para almacenar clientes[cite: 3, 4]
        self.servicios: list[Servicio] = []  # Lista interna en memoria para almacenar servicios[cite: 3, 4]
        self.reservas: list[Reserva] = []  # Lista interna en memoria para almacenar reservas[cite: 3, 4]
        self.logs = registrador_logs  # Guarda la instancia del registrador de logs[cite: 4]

    def registrar_cliente(self, cliente: Cliente) -> bool:  # Registra un cliente usando try/except/else/finally[cite: 3, 4]
        exito = False  # Bandera inicial de resultado[cite: 4]
        try:  # Bloque principal de intento de registro[cite: 4]
            if not isinstance(cliente, Cliente):  # Valida tipo Cliente[cite: 4]
                raise ErrorValidacionDato("El objeto recibido no es una instancia válida de Cliente.")  # Lanza error[cite: 4]
            if any(c.id_entidad == cliente.id_entidad for c in self.clientes):  # Evita IDs duplicados en lista[cite: 4]
                raise ErrorOperacionNoPermitida(f"Ya existe un cliente registrado con el ID '{cliente.id_entidad}'.")
            self.clientes.append(cliente)  # Agrega el cliente a la lista interna[cite: 3, 4]
        except (ErrorValidacionDato, ErrorOperacionNoPermitida) as err:  # Captura errores esperados[cite: 4]
            self.logs.registrar("ERROR", f"Fallo al registrar cliente: {err}")  # Registra el error en el .log[cite: 4]
        else:  # Se ejecuta únicamente si el try no lanzó excepciones[cite: 3, 4]
            exito = True  # Marca la operación como exitosa[cite: 4]
            self.logs.registrar("INFO", f"Cliente registrado correctamente: {cliente.describir()}")  # Registra evento[cite: 4]
        finally:  # Se ejecuta siempre, ocurra o no error[cite: 3, 4]
            self.logs.registrar("AUDITORIA", f"Intento de registro de cliente finalizado. Total clientes: {len(self.clientes)}")
        return exito  # Retorna si se registró o no[cite: 4]

    def registrar_servicio(self, servicio: Servicio) -> bool:  # Registra un servicio en la lista interna[cite: 3, 4]
        try:  # Intenta agregar el servicio a la lista en memoria[cite: 3, 4]
            if not isinstance(servicio, Servicio):  # Valida tipo Servicio[cite: 4]
                raise ErrorValidacionDato("El objeto recibido no es una instancia válida de Servicio.")  # Lanza error[cite: 4]
            if any(s.id_entidad == servicio.id_entidad for s in self.servicios):  # Evita IDs duplicados[cite: 4]
                raise ErrorOperacionNoPermitida(f"Ya existe un servicio registrado con el ID '{servicio.id_entidad}'.")
            self.servicios.append(servicio)  # Guarda el servicio en la lista interna[cite: 3, 4]
        except (ErrorValidacionDato, ErrorOperacionNoPermitida) as err:  # Captura errores de validación/operación[cite: 4]
            self.logs.registrar("ERROR", f"Fallo al registrar servicio: {err}")  # Registra error en .log[cite: 4]
            return False  # Retorna False si falló[cite: 4]
        else:  # Si no hubo errores al registrar[cite: 3, 4]
            self.logs.registrar("INFO", f"Servicio registrado correctamente: {servicio.describir()}")  # Registra éxito[cite: 4]
            return True  # Retorna True si tuvo éxito[cite: 4]
        finally:  # Ejecuta siempre al cerrar el bloque[cite: 3, 4]
            self.logs.registrar("AUDITORIA", f"Intento de registro de servicio finalizado. Total servicios: {len(self.servicios)}")

    def crear_y_procesar_reserva(  # Crea, confirma y procesa una reserva con encadenamiento de excepciones[cite: 3, 4]
        self,  # Referencia al gestor[cite: 4]
        id_reserva: str,  # ID de la nueva reserva[cite: 4]
        id_cliente: str,  # ID del cliente que solicita[cite: 4]
        id_servicio: str,  # ID del servicio solicitado[cite: 4]
        duracion_horas: int,  # Duración en horas[cite: 4]
        cantidad_unidades: int = 1,  # Unidades solicitadas[cite: 4]
        descuento_pct: float = 0.0,  # Descuento opcional[cite: 4]
        impuesto_pct: float = 0.0,  # Impuesto opcional[cite: 4]
        confirmar_y_procesar: bool = True,  # Indica si se confirma y procesa en el flujo[cite: 4]
    ) -> Reserva | None:  # Retorna la Reserva creada o None si ocurrió un error controlado[cite: 4]
        reserva_creada = None  # Inicializa variable de reserva[cite: 4]
        try:  # Bloque principal para localizar entidades y construir/procesar la reserva[cite: 4]
            cliente = next((c for c in self.clientes if c.id_entidad == id_cliente), None)  # Busca cliente en lista[cite: 4]
            if cliente is None:  # Si no existe el cliente[cite: 4]
                raise ErrorReserva(f"Cliente con ID '{id_cliente}' no encontrado en el sistema.")  # Lanza ErrorReserva[cite: 4]

            servicio = next((s for s in self.servicios if s.id_entidad == id_servicio), None)  # Busca servicio en lista[cite: 4]
            if servicio is None:  # Si no existe el servicio[cite: 4]
                raise ErrorReserva(f"Servicio con ID '{id_servicio}' no encontrado en el sistema.")  # Lanza ErrorReserva[cite: 4]

            try:  # Sub-bloque para instanciar Reserva y encadenar excepciones si falla[cite: 3, 4]
                reserva_creada = Reserva(  # Intenta crear la reserva[cite: 4]
                    id_reserva=id_reserva,  # Pasa ID de reserva[cite: 4]
                    cliente=cliente,  # Pasa cliente encontrado[cite: 4]
                    servicio=servicio,  # Pasa servicio encontrado[cite: 4]
                    duracion_horas=duracion_horas,  # Pasa duración[cite: 4]
                    cantidad_unidades=cantidad_unidades,  # Pasa cantidad[cite: 4]
                    descuento_pct=descuento_pct,  # Pasa descuento[cite: 4]
                    impuesto_pct=impuesto_pct,  # Pasa impuesto[cite: 4]
                )  # Cierra constructor Reserva[cite: 4]
            except (ErrorValidacionDato, ErrorCalculoCosto) as causa_original:  # Captura error de validación/cálculo[cite: 4]
                # Encadena la excepción original (from causa_original) dentro de ErrorReserva[cite: 3, 4]
                raise ErrorReserva(f"No se pudo construir la reserva '{id_reserva}'.") from causa_original  # Encadena[cite: 3, 4]

            if confirmar_y_procesar:  # Si se solicita confirmar y procesar de inmediato[cite: 4]
                reserva_creada.confirmar()  # Confirma la reserva[cite: 4]
                reserva_creada.procesar()  # Procesa la reserva[cite: 4]

            self.reservas.append(reserva_creada)  # Agrega la reserva a la lista interna[cite: 3, 4]

        except (ErrorReserva, ErrorOperacionNoPermitida) as err:  # Captura errores de reserva u operación[cite: 4]
            causa = f" (Causa encadenada: {err.__cause__})" if err.__cause__ else ""  # Revisa si hubo encadenamiento[cite: 3, 4]
            self.logs.registrar("ERROR", f"Fallo en reserva '{id_reserva}': {err}{causa}")  # Registra en archivo .log[cite: 4]
            return None  # Mantiene la aplicación activa devolviendo None[cite: 3, 4]

        else:  # Si todo salió bien en el try[cite: 3, 4]
            self.logs.registrar("INFO", f"Reserva gestionada con éxito: {reserva_creada.resumen()}")  # Registra éxito[cite: 4]
            return reserva_creada  # Retorna la reserva creada[cite: 4]

        finally:  # Siempre registra la auditoría final de la operación de reserva[cite: 3, 4]
            self.logs.registrar("AUDITORIA", f"Operación de reserva '{id_reserva}' finalizada. Total reservas: {len(self.reservas)}")
