# Sistema Experto Medico de Triaje

Proyecto practico de Inteligencia Artificial basado en reglas con `experta`.
Simula un asistente de triaje para apoyar la clasificacion inicial de pacientes.

---

## Que hace este sistema

- Relaciona sintomas, enfermedades y farmacos desde una base de conocimiento.
- Permite consultar:
  - enfermedad -> farmaco recomendado
  - paciente -> diagnostico y receta
  - sintoma -> pacientes relacionados
  - triaje por dos sintomas
- Muestra alerta roja cuando no hay coincidencias en triaje.

---

## Estructura del proyecto

```text
TriajeMedico_AlfonsoLuque/
|-- sistema_experto_medico.py
|-- README.md
```

---

## Requisitos

- Python 3.9 recomendado
- `experta`

> Nota: con Python 3.10+ puede aparecer incompatibilidad en dependencias antiguas de `experta`.

---

## Instalacion rapida (Windows / PowerShell)

```powershell
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install experta
```

---

## Ejecucion

```powershell
python .\sistema_experto_medico.py
```

Al iniciar veras un menu con opciones de consulta e inferencia.

---

## Flujo de uso recomendado

1. Probar inferencia de alivio (opcion 1)
2. Consultar un paciente (opcion 2)
3. Buscar por sintoma (opcion 3)
4. Ejecutar triaje con dos sintomas (opcion 4)

---

## Ejemplo corto

```text
MENu PRINCIPAL
1. Inferencia de Alivio
2. Gestion de Pacientes
3. Busqueda Inversa
4. Triaje de Urgencias
0. Salir
```

---

## Autor

- Alfonso Luque Sanchez

