# 🏛️ Gestor de Audiencias

Sistema profesional para gestionar audiencias judiciales con inteligencia artificial integrada.

## 🚀 Uso Rápido

### Desarrollo:
```bash
python main.py
```

### Generar Ejecutable:
```bash
python build_exe.py
```

## 📂 Estructura del Proyecto

```
gestor_audiencias/
├── 📂 config/                    # Configuración de OpenAI
│   ├── config.py                 # Configuración actual
│   └── config_template.py        # Plantilla de configuración
├── 📂 docs/                      # Documentación técnica
│   └── SISTEMA_COMPLETO_FINAL.md # Documentación completa del sistema
├── 📂 gui/                       # Interfaz gráfica de usuario
│   ├── constants.py              # Constantes y temas
│   ├── dialogs.py                # Diálogos de la aplicación
│   ├── ia_config_dialog.py       # Configuración de IA
│   ├── main_window.py            # Ventana principal
│   └── widgets.py                # Widgets personalizados
├── 📂 models/                    # Modelos de datos
│   ├── audiencia.py              # Modelo de audiencia
│   └── excel_manager.py          # Gestor de archivos Excel
├── 📂 services/                  # Servicios (IA)
│   └── ai_service.py             # Servicio de inteligencia artificial
├── 📂 templates/                 # Plantillas de archivos
│   └── plantilla_audiencias.xlsx # Plantilla de Excel
├── 📂 tests/                     # Pruebas del sistema
│   └── test_seguridad_maxima.py  # Pruebas de seguridad
├── 📂 utils/                     # Utilidades
│   ├── anonimizador.py           # Sistema de anonimización
│   ├── file_manager.py           # Gestor de archivos
│   └── validators.py             # Validaciones
├── 📂 archivos_creados/          # Archivos generados por la app
├── main.py                       # Aplicación principal
├── build_exe.py                  # Generador de ejecutable
└── requirements.txt              # Dependencias
```

## ⚡ Características

- ✅ **Interfaz Moderna**: Framework Flet
- ✅ **IA Integrada**: OpenAI GPT-4o-mini
- ✅ **Gestión Excel**: Plantillas automáticas
- ✅ **Ejecutable**: Sin instalación requerida
- ✅ **Temas**: Claro y oscuro

## 🤖 Configuración IA

La aplicación incluye configuración de IA integrada:
1. Haz clic en el botón "🤖 IA" 
2. Configura tu API Key de OpenAI
3. ¡Listo para usar!

---
**Desarrollado por Jose David Bustamante Sánchez - 2025**
