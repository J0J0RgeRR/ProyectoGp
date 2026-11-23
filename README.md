# Su Plaza al Día (ProyectoGp)

Sistema de gestión para la administración de una plaza comercial, desarrollado en Python con Flask y HTML para la asignatura de Programación Estructurada.

## Propósito

Una plaza necesita llevar en un solo lugar sus cobros, su caja y sus inventarios. Este sistema reemplaza los registros a mano y permite:

- Cobrar los servicios de baños y descontar automáticamente el papel del inventario.
- Registrar los vehículos que entran al parqueo, atenderlos en orden de llegada y cobrarlos.
- Administrar a los comerciantes de la plaza y sus cobros diarios o semanales.
- Controlar la caja (apertura, saldo y cierre) y los gastos.
- Consultar reportes diarios, semanales, quincenales y mensuales.
- Consultar la ruta más corta entre las zonas de la plaza.

**Dirigido a:** administradores y trabajadores de la plaza (dos roles con permisos distintos).

## Estructuras de datos dinámicas utilizadas

| Estructura | Archivo | Para qué se usa |
|---|---|---|
| Árbol binario de búsqueda | `merchants.py` | Almacena los comerciantes ordenados por código de local. Permite insertar, buscar, eliminar y listar en orden (recorrido inorden). |
| Lista enlazada | `parking.py` | Guarda el historial de cobros de parqueo; cada nodo apunta al siguiente. |
| Cola (FIFO) con `deque` | `parking.py` | Mantiene los vehículos pendientes y los atiende en orden de llegada. |
| Grafo con lista de adyacencia | `rutas.py` | Representa las zonas de la plaza y sus conexiones; la ruta con menos tramos se busca con recorrido en anchura (BFS). |

## Estructura del proyecto

```
app.py          Aplicación Flask (rutas web, sesiones y estado general)
main.py         Versión de consola de las primeras etapas del proyecto
users.py        Inicio de sesión y roles
bathrooms.py    Cobros de baños
paper.py        Inventario de papel
parking.py      Parqueo: cola de pendientes y lista enlazada de cobros
merchants.py    Comerciantes y sus cobros: árbol binario de búsqueda
rutas.py        Zonas de la plaza y búsqueda de rutas: grafo
cash.py         Apertura, saldo y cierre de caja
expenses.py     Registro de gastos
reports.py      Reportes por período
files.py        Lectura y escritura de datos en JSON (carpeta data/)
templates/      Interfaz web (index.html)
data/           Datos guardados del sistema y reportes
```

## Cómo ejecutar el programa

Requisitos: Python 3.10 o superior.

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/J0J0RgeRR/ProyectoGp.git
   cd ProyectoGp
   ```
2. (Opcional) Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # Linux / macOS
   ```
3. Instalar Flask:
   ```bash
   pip install flask
   ```
4. Ejecutar la aplicación:
   ```bash
   python app.py
   ```
5. Abrir en el navegador: <http://127.0.0.1:5000>

### Usuarios de prueba

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin` | `admin123` |
| Trabajador | `trabajador` | `trabajador123` |

El administrador puede además gestionar comerciantes, ingresar rollos de papel y ver todos los tipos de reporte. El trabajador solo ve el reporte del día actual.

## Integrantes

| Nombre completo | Usuario de GitHub | Aportes principales (según el historial de commits) |
|---|---|---|
| [Santiago Centeno] | `sjcenteno-ux` | Estructura inicial, inicio de sesión y menú por rol, cobros de baños, caja, gastos, integración con Flask |
| [Roberto Sovalbarro] | `rrsobalvarro-maker` | Lista enlazada y cola (FIFO) del parqueo, historial de parqueo, rutas |
| [Carlos Cerda] | `ccerda25` | Cobro de parqueo (tipo, modalidad, identificador), historial |
| J[orge Pulido] | `J0J0RgeRR` | Menú principal, ingreso de rollos de papel, módulo de comerciantes |

## Asignatura

Programación Estructurada, 2026.
