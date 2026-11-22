entidades_y_servicios.py
from abc import ABC, abstractmethod  # Importa ABC y abstractmethod para definir clases y métodos abstractos[cite: 3]
import re  # Importa re para validar el formato del correo electrónico con expresiones regulares[cite: 4]
from excepciones_y_logs import ErrorValidacionDato, ErrorCalculoCosto  # Importa excepciones personalizadas del Commit 2[cite: 1, 4]

class EntidadBase(ABC):  # Clase abstracta que representa entidades generales del sistema de Software FJ[cite: 3, 4]
    """Clase abstracta base para entidades identificables del sistema."""  # Documenta la clase abstracta[cite: 4]

    def __init__(self, id_entidad: str, nombre: str):  # Constructor que recibe identificador y nombre[cite: 4]
        self._id_entidad = ""  # Inicializa el atributo protegido del identificador[cite: 4]
        self._nombre = ""  # Inicializa el atributo protegido del nombre[cite: 4]
        self.id_entidad = id_entidad  # Asigna el ID pasando por su validación (setter)[cite: 4]
        self.nombre = nombre  # Asigna el nombre pasando por su validación (setter)[cite: 4]

        @property  # Expone id_entidad como propiedad controlada[cite: 4]
    def id_entidad(self) -> str:  # Retorna el identificador de la entidad[cite: 4]
        return self._id_entidad  # Devuelve el valor almacenado en _id_entidad[cite: 4]

    @id_entidad.setter  # Valida el valor asignado a id_entidad[cite: 4]
    def id_entidad(self, valor: str) -> None:  # Verifica que sea un texto no vacío[cite: 4]
        if not isinstance(valor, str) or not valor.strip():  # Comprueba tipo string y ausencia de espacios vacíos[cite: 4]
            raise ErrorValidacionDato("El identificador es obligatorio y debe ser un texto válido.")  # Lanza excepción[cite: 4]
        self._id_entidad = valor.strip()  # Guarda el identificador limpio[cite: 4]

        @property  # Expone nombre como propiedad controlada[cite: 4]
    def nombre(self) -> str:  # Retorna el nombre de la entidad[cite: 4]
        return self._nombre  # Devuelve el valor almacenado en _nombre[cite: 4]

    @nombre.setter  # Valida el valor asignado a nombre[cite: 4]
    def nombre(self, valor: str) -> None:  # Verifica longitud mínima y tipo de dato[cite: 4]
        if not isinstance(valor, str) or len(valor.strip()) < 2:  # Exige al menos 2 caracteres de texto[cite: 4]
            raise ErrorValidacionDato("El nombre debe ser un texto de al menos 2 caracteres.")  # Lanza excepción[cite: 4]
        self._nombre = valor.strip()  # Guarda el nombre limpio[cite: 4]

        @abstractmethod  # Obliga a las subclases a definir su propia descripción[cite: 4]
    def describir(self) -> str:  # Método abstracto para describir la entidad[cite: 4]
        """Retorna una descripción legible de la entidad."""  # Documenta el método abstracto[cite: 4]

        class Cliente(EntidadBase):  # Clase Cliente que hereda de EntidadBase con encapsulación y validaciones[cite: 4]
    """Representa un cliente de Software FJ con datos personales encapsulados."""  # Documenta la clase Cliente[cite: 4]

    def __init__(self, id_cliente: str, nombre: str, correo: str, activo: bool = True):  # Constructor de Cliente[cite: 4]
        super().__init__(id_cliente, nombre)  # Inicializa id_entidad y nombre desde EntidadBase[cite: 4]
        self.__correo = ""  # Atributo privado (__correo) para encapsular el correo electrónico[cite: 4]
        self.__activo = True  # Atributo privado (__activo) para encapsular el estado del cliente[cite: 4]
        self.correo = correo  # Valida y asigna el correo mediante su setter[cite: 4]
        self.activo = activo  # Valida y asigna el estado activo mediante su setter[cite: 4]

        @property  # Getter para consultar el correo encapsulado[cite: 4]
    def correo(self) -> str:  # Devuelve el correo del cliente[cite: 4]
        return self.__correo  # Retorna el atributo privado __correo[cite: 4]

    @correo.setter  # Setter con validación estricta de formato de correo[cite: 4]
    def correo(self, valor: str) -> None:  # Valida que el correo tenga formato básico correcto[cite: 4]
        if not isinstance(valor, str) or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", valor.strip()):  # Valida email[cite: 4]
            raise ErrorValidacionDato(f"Correo electrónico inválido para el cliente '{self._nombre}'.")  # Lanza error[cite: 4]
        self.__correo = valor.strip().lower()  # Guarda el correo limpio y en minúsculas[cite: 4]

        @property  # Getter para consultar si el cliente está activo[cite: 4]
    def activo(self) -> bool:  # Retorna si el cliente está activo[cite: 4]
        return self.__activo  # Retorna el atributo privado __activo[cite: 4]

    @activo.setter  # Setter para validar el estado booleano del cliente[cite: 4]
    def activo(self, valor: bool) -> None:  # Valida que el valor sea de tipo bool[cite: 4]
        if not isinstance(valor, bool):  # Verifica que sea True o False[cite: 4]
            raise ErrorValidacionDato("El estado 'activo' del cliente debe ser un valor booleano.")  # Lanza error[cite: 4]
        self.__activo = valor  # Guarda el estado booleano[cite: 4]

        def describir(self) -> str:  # Sobrescribe describir() aplicando polimorfismo[cite: 4]
        estado_texto = "Activo" if self.__activo else "Inactivo"  # Convierte el estado booleano a texto[cite: 4]
        return f"Cliente [{self._id_entidad}] - {self._nombre} | Correo: {self.__correo} | Estado: {estado_texto}"  # Texto[cite: 4]

    class Servicio(EntidadBase):  # Clase abstracta Servicio que hereda de EntidadBase[cite: 4]
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""  # Documenta la clase Servicio[cite: 4]

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):  # Constructor[cite: 4]
        super().__init__(id_servicio, nombre)  # Valida y asigna id_entidad y nombre[cite: 4]
        self._tarifa_base = 0.0  # Atributo protegido para la tarifa base[cite: 4]
        self._disponible = True  # Atributo protegido para indicar disponibilidad[cite: 4]
        self.tarifa_base = tarifa_base  # Valida y asigna la tarifa base[cite: 4]
        self.disponible = disponible  # Valida y asigna la disponibilidad[cite: 4]

        @property  # Getter para tarifa_base[cite: 4]
    def tarifa_base(self) -> float:  # Retorna la tarifa base[cite: 4]
        return self._tarifa_base  # Devuelve el valor protegido[cite: 4]

    @tarifa_base.setter  # Setter que exige una tarifa mayor que cero[cite: 4]
    def tarifa_base(self, valor: float) -> None:  # Valida que tarifa_base sea positiva[cite: 4]
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:  # Valida número > 0[cite: 4]
            raise ErrorCalculoCosto("La tarifa base del servicio debe ser un número mayor que cero.")  # Lanza error[cite: 4]
        self._tarifa_base = float(valor)  # Guarda la tarifa como número flotante[cite: 4]

        @property  # Getter para disponible[cite: 4]
    def disponible(self) -> bool:  # Retorna si el servicio está disponible[cite: 4]
        return self._disponible  # Devuelve el estado de disponibilidad[cite: 4]

    @disponible.setter  # Setter para validar la disponibilidad[cite: 4]
    def disponible(self, valor: bool) -> None:  # Valida que disponible sea booleano[cite: 4]
        if not isinstance(valor, bool):  # Verifica tipo bool[cite: 4]
            raise ErrorValidacionDato("La disponibilidad del servicio debe ser un valor booleano.")  # Lanza error[cite: 4]
        self._disponible = valor  # Guarda el estado de disponibilidad[cite: 4]

    @abstractmethod  # Método abstracto que cada servicio debe sobrescribir[cite: 4]
    def validar_parametros(self, duracion_horas: int, cantidad_unidades: int = 1) -> None:  # Valida parámetros[cite: 4]
        """Valida los parámetros de uso del servicio."""  # Documenta el método[cite: 4]

    @abstractmethod  # Método abstracto para calcular el costo base del servicio[cite: 4]
    def calcular_costo(self, duracion_horas: int, cantidad_unidades: int = 1) -> float:  # Calcula costo[cite: 4]
        """Calcula el costo del servicio según duración y cantidad."""  # Documenta el método[cite: 4]

    @abstractmethod  # Método abstracto para describir el servicio[cite: 4]
    def describir(self) -> str:  # Retorna la descripción del servicio[cite: 4]
        """Retorna una descripción detallada del servicio."""  # Documenta el método[cite: 4]


class ReservaSala(Servicio):  # Servicio especializado 1: reserva de salas[cite: 3, 4]
    """Servicio especializado para reserva de salas en Software FJ."""  # Documenta ReservaSala[cite: 3, 4]

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad_personas: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)  # Inicializa atributos de Servicio[cite: 4]
        if isinstance(capacidad_personas, bool) or not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            raise ErrorValidacionDato("La capacidad de la sala debe ser un entero mayor que cero.")  # Valida capacidad[cite: 4]
        self.capacidad_personas = capacidad_personas  # Guarda la capacidad máxima de la sala[cite: 4]

    def validar_parametros(self, duracion_horas: int, cantidad_unidades: int = 1) -> None:  # Sobrescribe validación[cite: 4]
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, int) or duracion_horas <= 0:  # Valida horas[cite: 4]
            raise ErrorValidacionDato("La duración en horas de la sala debe ser un entero mayor que 0.")  # Lanza error[cite: 4]
        if duracion_horas > 12:  # Verifica límite máximo de horas continuas[cite: 4]
            raise ErrorValidacionDato("La reserva de sala no puede superar las 12 horas continuas.")  # Lanza error[cite: 4]
        if isinstance(cantidad_unidades, bool) or not isinstance(cantidad_unidades, int) or cantidad_unidades <= 0:
            raise ErrorValidacionDato("La cantidad de personas/unidades debe ser un entero mayor que 0.")  # Lanza error[cite: 4]
        if cantidad_unidades > self.capacidad_personas:  # Verifica que no supere la capacidad de la sala[cite: 4]
            raise ErrorValidacionDato(
                f"La cantidad ({cantidad_unidades}) supera la capacidad de la sala ({self.capacidad_personas})."
            )  # Lanza error[cite: 4]

    def calcular_costo(self, duracion_horas: int, cantidad_unidades: int = 1) -> float:  # Sobrescribe cálculo[cite: 4]
        self.validar_parametros(duracion_horas, cantidad_unidades)  # Valida parámetros primero[cite: 4]
        costo = self._tarifa_base * duracion_horas  # Calcula tarifa por horas[cite: 4]
        if costo <= 0:  # Verifica que el costo sea positivo[cite: 4]
            raise ErrorCalculoCosto("El costo calculado para la reserva de sala es inválido.")  # Lanza error[cite: 4]
        return round(float(costo), 2)  # Retorna el costo redondeado a 2 decimales[cite: 4]

    def describir(self) -> str:  # Sobrescribe describir() con polimorfismo[cite: 4]
        estado_disp = "Disponible" if self._disponible else "No disponible"  # Estado en texto[cite: 4]
        return (
            f"Servicio [Sala - {self._id_entidad}] {self._nombre} | "
            f"Tarifa/h: ${self._tarifa_base:.2f} | Capacidad: {self.capacidad_personas} | {estado_disp}"
        )  # Retorna descripción[cite: 4]


class AlquilerEquipo(Servicio):  # Servicio especializado 2: alquiler de equipos[cite: 3, 4]
    """Servicio especializado para alquiler de equipos en Software FJ."""  # Documenta AlquilerEquipo[cite: 3, 4]

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, stock_disponible: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)  # Inicializa atributos de Servicio[cite: 4]
        if isinstance(stock_disponible, bool) or not isinstance(stock_disponible, int) or stock_disponible < 0:
            raise ErrorValidacionDato("El stock disponible debe ser un entero igual o mayor que 0.")  # Valida stock[cite: 4]
        self.stock_disponible = stock_disponible  # Guarda el stock disponible[cite: 4]

    def validar_parametros(self, duracion_horas: int, cantidad_unidades: int = 1) -> None:  # Sobrescribe validación[cite: 4]
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, int) or duracion_horas <= 0:  # Valida horas[cite: 4]
            raise ErrorValidacionDato("La duración del alquiler debe ser un entero mayor que 0.")  # Lanza error[cite: 4]
        if isinstance(cantidad_unidades, bool) or not isinstance(cantidad_unidades, int) or cantidad_unidades <= 0:
            raise ErrorValidacionDato("La cantidad de equipos debe ser un entero mayor que 0.")  # Lanza error[cite: 4]
        if cantidad_unidades > self.stock_disponible:  # Comprueba disponibilidad de inventario[cite: 4]
            raise ErrorValidacionDato(
                f"Stock insuficiente para '{self._nombre}': solicitados {cantidad_unidades}, disponibles {self.stock_disponible}."
            )  # Lanza error[cite: 4]

    def calcular_costo(self, duracion_horas: int, cantidad_unidades: int = 1) -> float:  # Sobrescribe cálculo[cite: 4]
        self.validar_parametros(duracion_horas, cantidad_unidades)  # Valida parámetros[cite: 4]
        costo = self._tarifa_base * duracion_horas * cantidad_unidades  # Calcula costo total del alquiler[cite: 4]
        if costo <= 0:  # Verifica consistencia del resultado[cite: 4]
            raise ErrorCalculoCosto("El costo calculado para el alquiler de equipo es inválido.")  # Lanza error[cite: 4]
        return round(float(costo), 2)  # Retorna el costo redondeado a 2 decimales[cite: 4]

    def describir(self) -> str:  # Sobrescribe describir() con polimorfismo[cite: 4]
        estado_disp = "Disponible" if self._disponible else "No disponible"  # Estado en texto[cite: 4]
        return (
            f"Servicio [Equipo - {self._id_entidad}] {self._nombre} | "
            f"Tarifa/h/u: ${self._tarifa_base:.2f} | Stock: {self.stock_disponible} | {estado_disp}"
        )  # Retorna descripción[cite: 4]


class AsesoriaEspecializada(Servicio):  # Servicio especializado 3: asesorías especializadas[cite: 3, 4]
    """Servicio especializado para asesorías técnicas en Software FJ."""  # Documenta AsesoriaEspecializada[cite: 3, 4]

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)  # Inicializa atributos de Servicio[cite: 4]
        if not isinstance(especialidad, str) or not especialidad.strip():  # Valida que haya especialidad[cite: 4]
            raise ErrorValidacionDato("La especialidad de la asesoría es obligatoria.")  # Lanza error[cite: 4]
        self.especialidad = especialidad.strip()  # Guarda el área de especialidad[cite: 4]

    def validar_parametros(self, duracion_horas: int, cantidad_unidades: int = 1) -> None:  # Sobrescribe validación[cite: 4]
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, int) or duracion_horas <= 0:  # Valida horas[cite: 4]
            raise ErrorValidacionDato("La duración de la asesoría debe ser un entero mayor que 0.")  # Lanza error[cite: 4]
        if isinstance(cantidad_unidades, bool) or not isinstance(cantidad_unidades, int) or cantidad_unidades <= 0:
            raise ErrorValidacionDato("La cantidad de sesiones/consultores debe ser un entero mayor que 0.")  # Lanza error[cite: 4]

    def calcular_costo(self, duracion_horas: int, cantidad_unidades: int = 1) -> float:  # Sobrescribe cálculo[cite: 4]
        self.validar_parametros(duracion_horas, cantidad_unidades)  # Valida parámetros[cite: 4]
        costo = (self._tarifa_base * duracion_horas * cantidad_unidades) + (15.0 * cantidad_unidades)  # Incluye cargo fijo[cite: 4]
        if costo <= 0:  # Verifica que el costo sea positivo[cite: 4]
            raise ErrorCalculoCosto("El costo calculado para la asesoría especializada es inválido.")  # Lanza error[cite: 4]
        return round(float(costo), 2)  # Retorna el costo redondeado a 2 decimales[cite: 4]

    def describir(self) -> str:  # Sobrescribe describir() con polimorfismo[cite: 4]
        estado_disp = "Disponible" if self._disponible else "No disponible"  # Estado en texto[cite: 4]
        return (
            f"Servicio [Asesoría - {self._id_entidad}] {self._nombre} ({self.especialidad}) | "
            f"Tarifa/h: ${self._tarifa_base:.2f} | {estado_disp}"
