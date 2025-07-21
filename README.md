# Juego de Visión Computacional: Piedra, Papel o Tijera con IA 🤖

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.6.0-green?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-red?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

## Descripción del Proyecto 🎯

Una implementación avanzada del clásico juego Piedra, Papel o Tijera utilizando Visión Computacional e Inteligencia Artificial. Este proyecto demuestra la integración de reconocimiento de gestos en tiempo real con lógica de juego, ejemplificando aplicaciones prácticas de visión por computadora en sistemas interactivos.

### Desarrollador
**Alex Jhail Sanchez Rea**  
Estudiante de Ingeniería de Sistemas en Universidad UTEPSA  
[LinkedIn](https://www.linkedin.com/in/alex-jhail-sanchez-rea-80637a184/) | [GitHub](https://github.com/TU_USUARIO_GITHUB)

## Implementación Técnica 🔧

### Tecnologías Principales
- **Visión Computacional**: OpenCV 4.6.0
- **IA y ML**: MediaPipe Hand Detection
- **Programación**: Python 3.8+
- **Procesamiento de Imágenes**: Imutils 0.5.4

### Características Técnicas Principales
- **Reconocimiento de Gestos en Tiempo Real** 👋
  - Implementación de detección de puntos de referencia con MediaPipe
  - Algoritmos personalizados de clasificación de gestos
  - Procesamiento y análisis de frames en tiempo real

- **Procesamiento de Visión Computacional** 👁️
  - Captura y preprocesamiento de frames
  - Manipulación y mejora de imágenes
  - Gestión de transmisión de video en tiempo real

- **Implementación de Lógica de Juego** 🎮
  - Arquitectura de máquina de estados
  - Procesamiento multihilo
  - Patrones de programación basados en eventos

- **Diseño de Interfaz de Usuario** 💻
  - Gestión personalizada de ventanas OpenCV
  - Renderizado de superposición en tiempo real
  - Sistema de retroalimentación visual dinámica

## Arquitectura del Sistema 🏗️

### Estructura de Componentes
```
proyecto/
├── Juego.py            # Lógica principal y UI
├── SeguimientoManos.py # Implementación de tracking
├── requirements.txt    # Dependencias
└── Imagenes/          # Recursos gráficos
```

### Flujo de Trabajo Técnico
1. **Captura de Video**
   - Adquisición de frames en tiempo real
   - Gestión de buffer
   - Optimización de tasa de frames

2. **Detección de Manos**
   - Detección de puntos de referencia con MediaPipe
   - Mapeo y normalización de coordenadas
   - Clasificación de gestos

3. **Gestión de Estado del Juego**
   - Seguimiento del estado del jugador
   - Gestión de rondas
   - Cálculo de puntuación

4. **Pipeline de Renderizado**
   - Composición de frames
   - Renderizado de elementos UI
   - Sistema de retroalimentación visual

## Características de Desarrollo 💡

### Integración de IA
- Detección de puntos de referencia usando MediaPipe
- Clasificación de gestos en tiempo real
- Análisis predictivo de movimientos

### Optimizaciones de Rendimiento
- Optimización de procesamiento de frames
- Gestión de memoria
- Control de utilización de recursos

### Experiencia de Usuario
- Controles de gestos intuitivos
- Retroalimentación visual en tiempo real
- Mecánicas de juego responsivas

## Requisitos Técnicos 📋

### Entorno de Desarrollo
- Python 3.8 o superior
- OpenCV 4.6.0.66
- MediaPipe 0.10.21
- Imutils 0.5.4

### Requisitos de Hardware
- CPU: Intel Core i3 o equivalente
- RAM: 2GB mínimo
- Cámara: Webcam funcional
- SO: Windows 10/11, Linux, o macOS

## Guía de Instalación 🔨

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO_GITHUB/Piedra-Papel-o-Tijera-con-IA.git
cd Piedra-Papel-o-Tijera-con-IA

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python Juego.py
```

## Controles del Juego 🎮

| Acción | Control | Descripción |
|--------|---------|-------------|
| Iniciar| `S` | Inicializar juego |
| Reiniciar| `R` | Reiniciar partida actual |
| Salir  | `ESC` | Cerrar aplicación |

## Desafíos de Implementación y Soluciones 🔍

### Desafío 1: Procesamiento en Tiempo Real
- **Problema**: Lograr un procesamiento fluido manteniendo la respuesta del juego
- **Solución**: Implementación de procesamiento multihilo y optimización de buffer de frames

### Desafío 2: Precisión en Reconocimiento de Gestos
- **Problema**: Clasificación precisa de gestos en diferentes condiciones de iluminación
- **Solución**: Mejora de parámetros de MediaPipe y algoritmos de validación personalizados

### Desafío 3: Experiencia de Usuario
- **Problema**: Mantener jugabilidad fluida durante el procesamiento de datos
- **Solución**: Optimización del pipeline de renderizado y tracking predictivo de gestos

## Plan de Desarrollo Futuro 🚀

1. **Mejoras en IA**
   - Predicción de gestos basada en aprendizaje automático
   - Reconocimiento de patrones avanzado
   - Análisis de comportamiento del jugador

2. **Mejoras Técnicas**
   - Optimización de rendimiento
   - Compatibilidad multiplataforma
   - Manejo de errores mejorado

3. **Nuevas Funcionalidades**
   - Capacidades de red multijugador
   - Seguimiento avanzado de estadísticas
   - Entrenamiento de gestos personalizados

## Capturas del Proyecto 📸

### Pantalla de Inicio
<div align="center">
<table>
  <tr>
    <td align="center"><b>Pantalla Principal</b></td>
  </tr>
  <tr>
    <td>
      <img src="imagenes/screenshots/inicio.png" width="800px" alt="Pantalla de Inicio"/>
    </td>
  </tr>
</table>
</div>

### Secuencia de Conteo
<div align="center">
<table>
  <tr>
    <td align="center"><b>Preparados...</b></td>
    <td align="center"><b>Listos...</b></td>
    <td align="center"><b>¡Ya!</b></td>
  </tr>
  <tr>
    <td>
      <img src="imagenes/screenshots/empieza.png" width="350px" alt="Conteo 3"/>
    </td>
    <td>
      <img src="imagenes/screenshots/empieza1.png" width="350px" alt="Conteo 2"/>
    </td>
    <td>
      <img src="imagenes/screenshots/empieza2.png" width="350px" alt="Conteo 1"/>
    </td>
  </tr>
</table>
</div>

### Resultados Posibles
<div align="center">
<table>
  <tr>
    <td align="center"><b>Victoria de la IA</b></td>
    <td align="center"><b>¡Empate!</b></td>
    <td align="center"><b>Victoria del Jugador</b></td>
  </tr>
  <tr>
    <td>
      <img src="imagenes/screenshots/ganaia.png" width="350px" alt="Gana IA"/>
    </td>
    <td>
      <img src="imagenes/screenshots/empate.png" width="350px" alt="Empate"/>
    </td>
    <td>
      <img src="imagenes/screenshots/ganajugador.png" width="350px" alt="Gana Jugador"/>
    </td>
  </tr>
</table>
</div>

## Licencia 📄

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">
Desarrollado con 💻 por Alex Jhail Sanchez Rea<br>
Estudiante de Ingeniería de Sistemas en UTEPSA
</div>
