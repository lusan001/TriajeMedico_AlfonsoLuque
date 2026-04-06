# Fecha: 06/04/2026
# Autor: Alfonso Luque Sánchez
"""
PRÁCTICA: SISTEMA EXPERTO MÉDICO INTERACTIVO (IA)
Motor de inferencia clínica usando Python y Experta.
"""

"""
Contexto del problema:
Un hospital necesita un asistente de triaje que ayude a los enfermeros a clasificar
pacientes. El sistema debe basarse en una Base de Conocimiento que
relacione síntomas, enfermedades y fármacos.
"""

from experta import Fact, KnowledgeEngine, MATCH, NOT, Rule, TEST


# ─────────────────────────────────────────────
# BASE DE CONOCIMIENTO  (Diccionario de Datos)
# ─────────────────────────────────────────────

BASE_CONOCIMIENTO = {
    "Gripe":        {"sintomas": ["Fiebre", "Tos", "Cansancio"],       "farmaco": "Aspirina"},
    "Mononucleosis": {"sintomas": ["Cansancio", "Fiebre"], "farmaco": "Descanso"},
    "Intoxicacion": {"sintomas": ["Diarrea", "Náuseas"],               "farmaco": "Lomotil"},
    "Migraña":      {"sintomas": ["Dolor de cabeza", "Sensibilidad luz"], "farmaco": "Paracetamol"},
}

PACIENTES = {
    "Pedro":  {"enfermedad": "Gripe",        "sintomas": ["Fiebre", "Tos", "Cansancio"]},
    "Ana":    {"enfermedad": "Migraña",       "sintomas": ["Dolor de cabeza", "Sensibilidad luz"]},
    "Carlos": {"enfermedad": "Intoxicacion",  "sintomas": ["Diarrea", "Náuseas"]},
}


# ─────────────────────────────────────────────
# DEFINICIÓN DE HECHOS (Facts)
# ─────────────────────────────────────────────

class Enfermedad(Fact):
    """Hecho que representa una enfermedad con sus síntomas y fármaco."""
    pass  # campos: nombre, sintomas (lista), farmaco


class Paciente(Fact):
    """Hecho que representa un paciente."""
    pass  # campos: nombre, enfermedad, sintomas (lista)


class Consulta(Fact):
    """Hecho temporal para consultas interactivas."""
    pass  # campos: tipo, valor / sintoma1, sintoma2


# ─────────────────────────────────────────────
# MOTOR DE INFERENCIA
# ─────────────────────────────────────────────

class SistemaExperto(KnowledgeEngine):

    # ── Regla 1: Inferencia de Alivio ─────────────────────────────────────
    """
    alivio_enfermedad:
    dado el nombre de la enfermedad, deduce el fármaco
    """
    @Rule(Consulta(tipo="alivio", valor=MATCH.enfermedad),
          Enfermedad(nombre=MATCH.enfermedad, farmaco=MATCH.farmaco))
    def alivio_enfermedad(self, enfermedad, farmaco):
        print(f"\n El fármaco recomendado para '{enfermedad}' es: {farmaco}")

    # ── Regla 2: Diagnóstico de paciente ──────────────────────────────────
    """
    diagnostico_paciente:
    muestra diagnóstico completo y receta del paciente
    """
    @Rule(Consulta(tipo="paciente", valor=MATCH.nombre),
          Paciente(nombre=MATCH.nombre, enfermedad=MATCH.enf, sintomas=MATCH.sint))
    def diagnostico_paciente(self, nombre, enf, sint):
        farmaco = BASE_CONOCIMIENTO[enf]["farmaco"]
        print(f"\n  Paciente  : {nombre}")
        print(f"  Diagnóstico: {enf}")
        print(f"  Síntomas  : {', '.join(sint)}")
        print(f"  Receta    : {farmaco}")

    # ── Regla 3: Búsqueda inversa por síntoma ─────────────────────────────
    """
    busqueda_inversa:
    lista qué pacientes tienen un síntoma concreto
    """
    @Rule(Consulta(tipo="busqueda", valor=MATCH.sintoma),
          Paciente(nombre=MATCH.nombre, sintomas=MATCH.sint),
          TEST(lambda sint, sintoma: sintoma.lower() in [s.lower() for s in sint]))
    def busqueda_inversa(self, sintoma, nombre, sint):
        print(f"  → {nombre} presenta '{sintoma}'")

    # ── Regla 4: Triaje con dos síntomas (coincidencia) ───────────────────
    """
    triage_coincide:
    diagnóstico si coinciden con alguna enfermedad
    """
    @Rule(Consulta(tipo="triage", sintoma1=MATCH.s1, sintoma2=MATCH.s2),
          Enfermedad(nombre=MATCH.enf, sintomas=MATCH.sint, farmaco=MATCH.farm),
          TEST(lambda sint, s1, s2: (s1.lower() in [s.lower() for s in sint] and
                                     s2.lower() in [s.lower() for s in sint])))
    def triage_coincide(self, s1, s2, enf, farm):
        print(f"\n  Diagnóstico: {enf}")
        print(f"  Fármaco     : {farm}")
        self.declare(Fact(triage_resuelto=True))

    # ── Regla 5: Triaje sin coincidencia → Alerta Roja ────────────────────
    """
    triage_alerta:
    si no hay coincidencia emite CUADRO DESCONOCIDO: ACUDA A URGENCIAS
    """
    @Rule(Consulta(tipo="triage", sintoma1=MATCH.s1, sintoma2=MATCH.s2),
          NOT(Fact(triage_resuelto=True)))
    def triage_alerta(self, s1, s2):
        print("\n ALERTA ROJA !!!!!")
        print("  CUADRO DESCONOCIDO: ACUDA A URGENCIAS INMEDIATAMENTE")


# ─────────────────────────────────────────────
# FUNCIONES DE INICIALIZACIÓN
# ─────────────────────────────────────────────

def inicializar_motor():
    """Crea el motor y carga la base de conocimiento."""
    motor = SistemaExperto()
    motor.reset()

    # Cargar enfermedades
    for nombre, datos in BASE_CONOCIMIENTO.items():
        motor.declare(Enfermedad(nombre=nombre,
                                 sintomas=datos["sintomas"],
                                 farmaco=datos["farmaco"]))

    # Cargar pacientes
    for nombre, datos in PACIENTES.items():
        motor.declare(Paciente(nombre=nombre,
                               enfermedad=datos["enfermedad"],
                               sintomas=datos["sintomas"]))
    return motor


# ─────────────────────────────────────────────
# MENÚ INTERACTIVO
# ─────────────────────────────────────────────

def menu_alivio(motor):
    print("\n  Enfermedades disponibles:", ", ".join(BASE_CONOCIMIENTO.keys()))
    enf = input("  Introduce el nombre de la enfermedad: ").strip()
    motor.declare(Consulta(tipo="alivio", valor=enf))
    motor.run()


def menu_pacientes(motor):
    print("\n  Pacientes disponibles:", ", ".join(PACIENTES.keys()))
    nombre = input("  Introduce el nombre del paciente: ").strip()
    motor.declare(Consulta(tipo="paciente", valor=nombre))
    motor.run()


def menu_busqueda(motor):
    sintoma = input("\n  Introduce el síntoma a buscar: ").strip()
    print(f"\n  Pacientes con '{sintoma}':")
    motor.declare(Consulta(tipo="busqueda", valor=sintoma))
    motor.run()


def menu_triage(motor):
    print("\n  Introduce dos síntomas para el triaje:")
    s1 = input("  Síntoma 1: ").strip()
    s2 = input("  Síntoma 2: ").strip()
    motor.declare(Consulta(tipo="triage", sintoma1=s1, sintoma2=s2))
    motor.run()


def main():
    print("=" * 55)
    print("   SISTEMA EXPERTO MÉDICO DE TRIAJE")
    print("=" * 55)

    while True:
        # Reiniciamos el motor en cada iteración para limpiar hechos temporales
        motor = inicializar_motor()

        print("\n  MENÚ PRINCIPAL")
        print("  1. Inferencia de Alivio (enfermedad → fármaco)")
        print("  2. Gestión de Pacientes (diagnóstico y receta)")
        print("  3. Búsqueda Inversa (síntoma → pacientes)")
        print("  4. Triaje de Urgencias (dos síntomas)")
        print("  0. Salir")

        opcion = input("\n  Selecciona una opción: ").strip()

        if opcion == "1":
            menu_alivio(motor)
        elif opcion == "2":
            menu_pacientes(motor)
        elif opcion == "3":
            menu_busqueda(motor)
        elif opcion == "4":
            menu_triage(motor)
        elif opcion == "0":
            print("\n  Cerrando el sistema. ¡Hasta pronto!\n")
            break
        else:
            print("\n  Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    main()
