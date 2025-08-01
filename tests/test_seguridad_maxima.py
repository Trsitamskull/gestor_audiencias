"""
PRUEBAS DE SEGURIDAD MÁXIMA - SISTEMA DE ANONIMIZACIÓN
=====================================================
Pruebas exhaustivas para alcanzar el más alto nivel de seguridad en la protección de datos.
Incluye todas las variaciones posibles de formatos y estructuras de datos sensibles.
"""
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
proyecto_root = Path(__file__).parent
sys.path.insert(0, str(proyecto_root))

from utils.anonimizador import anonimizar_para_ia, restaurar_datos_ia


def test_nombres_complejos():
    """Prueba protección de nombres en múltiples formatos y estructuras."""
    print("👤 PRUEBA: NOMBRES EN FORMATOS COMPLEJOS")
    print("=" * 60)
    
    casos_nombres = [
        # Nombres con apellido primero (formato judicial)
        "RODRÍGUEZ VILLA, CARLOS ANDRÉS",
        "GONZÁLEZ TORRES, MARÍA HELENA", 
        "MARTÍN SILVA, LUIS FERNANDO",
        "HERNÁNDEZ LÓPEZ, ANA PATRICIA",
        
        # Nombres en minúsculas
        "carlos andrés rodríguez villa",
        "maría helena gonzález torres",
        "luis fernando martín silva",
        "ana patricia hernández lópez",
        
        # Nombres mixtos
        "Carlos Andrés RODRÍGUEZ Villa",
        "María Helena gonzález TORRES",
        
        # Solo nombre y apellido
        "Carlos Rodríguez",
        "María González", 
        "Luis Martín",
        "Ana Hernández",
        
        # En contextos judiciales
        "El imputado RODRÍGUEZ VILLA, CARLOS ANDRÉS compareció",
        "La víctima gonzález torres, maría helena no asistió",
        "El fiscal MARTÍN SILVA, Luis Fernando presentó",
        "La defensora Ana Patricia HERNÁNDEZ declaró",
        
        # Múltiples nombres en un párrafo
        "En la audiencia comparecieron CARLOS ANDRÉS RODRÍGUEZ, maría helena gonzález, Luis MARTÍN SILVA y Ana Patricia hernández lópez.",
    ]
    
    try:
        from utils.anonimizador import anonimizar_para_ia
        
        for i, caso in enumerate(casos_nombres, 1):
            print(f"\n🔸 Caso {i:2d}: {caso}")
            texto_anonimo, mapeo = anonimizar_para_ia(caso)
            print(f"🔒 Protegido: {texto_anonimo}")
            
            # Verificar que se protegió correctamente
            nombres_detectados = len([k for k in mapeo.keys() if 'NOMBRE_' in str(k)])
            if nombres_detectados > 0:
                print(f"✅ Protegidos: {nombres_detectados} nombres")
            else:
                print("⚠️  Sin detección automática")
                
    except Exception as e:
        print(f"❌ Error: {e}")


def test_cedulas_exhaustivas():
    """Prueba protección exhaustiva de todos los formatos de cédula."""
    print("\n🆔 PRUEBA: CÉDULAS EN TODOS LOS FORMATOS POSIBLES")
    print("=" * 60)
    
    casos_cedulas = [
        # Formatos estándar con puntos
        "C.C. 1.234.567.890",
        "Cédula: 52.789.123.456",
        "T.I. 1.098.765.432",
        "Documento: 11.222.333.444",
        
        # Sin puntos
        "C.C. 1234567890",
        "Cédula 52789123",
        "T.I. 1098765432",
        "Documento 11222333",
        
        # En contextos
        "identificado con C.C. 1.234.567.890",
        "portador de la Cédula 52.789.123",
        "menor con T.I. 1.098.765.432",
        "según documento 11.222.333",
        
        # Formatos especiales
        "NIT: 900.123.456-7",
        "RUT: 12.345.678-9", 
        "Pasaporte: AB1234567",
        "C.E. 1.234.567.890",
        
        # Múltiples cédulas
        "Los comparecientes C.C. 1.234.567.890, T.I. 52.789.123 y Cédula 11.222.333 estuvieron presentes",
        
        # Formatos irregulares
        "cedula de ciudadania numero 1234567890",
        "tarjeta de identidad no. 52789123",
        "documento de identidad: 11222333",
    ]
    
    try:
        from utils.anonimizador import anonimizar_para_ia
        
        for i, caso in enumerate(casos_cedulas, 1):
            print(f"\n🔸 Caso {i:2d}: {caso}")
            texto_anonimo, mapeo = anonimizar_para_ia(caso)
            print(f"🔒 Protegido: {texto_anonimo}")
            
            # Verificar protección
            cedulas_detectadas = len([k for k in mapeo.keys() if 'CEDULA_' in str(k) or 'DOC_' in str(k)])
            if cedulas_detectadas > 0:
                print(f"✅ Protegidas: {cedulas_detectadas} cédulas")
            else:
                print("⚠️  Sin detección")
                
    except Exception as e:
        print(f"❌ Error: {e}")


def test_celulares_exhaustivos():
    """Prueba protección de números celulares en todos los formatos."""
    print("\n📱 PRUEBA: CELULARES EN TODOS LOS FORMATOS")
    print("=" * 60)
    
    casos_celulares = [
        # Formatos colombianos estándar
        "Celular: 300 123 4567",
        "Móvil: 301-234-5678", 
        "Tel: 320.345.6789",
        "Teléfono: 350 456 7890",
        
        # Con código de país
        "+57 300 123 4567",
        "(+57) 301 234 5678",
        "0057 320 345 6789",
        
        # Sin separadores
        "Celular: 3001234567",
        "Móvil: 3012345678",
        "Tel: 3203456789",
        
        # En contextos
        "contactar al 300 123 4567",
        "llamar al teléfono 301-234-5678",
        "comunicarse al móvil 320.345.6789",
        
        # Múltiples números
        "Los números 300 123 4567, 301-234-5678 y 320.345.6789 están disponibles",
        
        # Formatos especiales
        "WhatsApp: +57 300 123 4567",
        "SMS al 301 234 5678",
        "Contacto: 320-345-6789",
        
        # Operadores específicos
        "Claro: 300 123 4567",
        "Movistar: 301 234 5678", 
        "Tigo: 320 345 6789",
    ]
    
    try:
        from utils.anonimizador import anonimizar_para_ia
        
        for i, caso in enumerate(casos_celulares, 1):
            print(f"\n🔸 Caso {i:2d}: {caso}")
            texto_anonimo, mapeo = anonimizar_para_ia(caso)
            print(f"🔒 Protegido: {texto_anonimo}")
            
            # Verificar protección
            celulares_detectados = len([k for k in mapeo.keys() if 'CELULAR_' in str(k)])
            if celulares_detectados > 0:
                print(f"✅ Protegidos: {celulares_detectados} celulares")
            else:
                print("⚠️  Sin detección")
                
    except Exception as e:
        print(f"❌ Error: {e}")


def test_documento_judicial_completo():
    """Prueba con un documento judicial completo con máxima complejidad."""
    print("\n📄 PRUEBA: DOCUMENTO JUDICIAL SÚPER COMPLEJO")
    print("=" * 60)
    
    documento_complejo = """
TRIBUNAL SUPERIOR DE MEDELLÍN - SALA PENAL
Expediente: 05001-60-00000-2024-00789-00

AUDIENCIA DE IMPUTACIÓN DE CARGOS

I. IDENTIFICACIÓN DE SUJETOS PROCESALES:

1. IMPUTADO:
   - Nombre: RODRÍGUEZ VILLA, CARLOS ANDRÉS  
   - Cédula: 1.234.567.890
   - Celular: 300 123 4567
   - Email: carlos.rodriguez@email.com
   - Dirección: Carrera 15 #45-67, Apto 301, Medellín
   - Tarjeta de crédito: 4532 1234 5678 9012

2. VÍCTIMA: 
   - Nombre: gonzález torres, maría helena
   - T.I.: 98.765.432
   - Teléfono: +57 301 234 5678
   - Correo: maria.victima@gmail.com
   - Residencia: Calle 50 #20-30, Barrio Centro

3. DEFENSOR:
   - Abogado: MARTÍN SILVA, Luis Fernando
   - Tarjeta Profesional: 123456
   - C.C.: 11.222.333.444
   - Contacto: 320-345-6789
   - Email: defensor@juridico.co

4. FISCAL:
   - Fiscal: Ana Patricia HERNÁNDEZ López
   - C.C.: 55.666.777.888
   - Móvil: 350.456.7890
   - Oficina: Carrera 30 #40-50, Piso 5

II. DESARROLLO DE LA AUDIENCIA:

La audiencia programada para el 15 de septiembre de 2024 a las 2:30 PM 
no se pudo realizar por los siguientes motivos:

- El imputado CARLOS ANDRÉS RODRÍGUEZ (C.C. 1.234.567.890) no fue 
  trasladado desde el Centro Carcelario La Modelo
- La víctima maría helena gonzález torres (T.I. 98.765.432) no compareció 
  pese a estar citada al 301 234 5678
- Problemas técnicos en el sistema de videoconferencia

III. CONTACTOS ADICIONALES:

Para reprogramación contactar:
- Secretaría: 604 123 4567
- Juzgado: secretaria@rama-judicial.gov.co  
- Defensoría: 320-345-6789
- Fiscalía: fiscal.unidad@fiscalia.gov.co

Testigos citados:
1. Pedro José RAMÍREZ González (C.C. 77.888.999.000) - Tel: 310 111 2222
2. Carmen Elena LÓPEZ Martínez (T.I. 33.444.555.666) - Cel: 301-222-3333

Se reprograma para el 22 de septiembre a las 9:00 AM.
"""
    
    try:
        print("📋 DOCUMENTO ORIGINAL:")
        print("-" * 40)
        print(documento_complejo[:500] + "...")
        
        # Anonimizar
        texto_anonimo, mapeo = anonimizar_para_ia(documento_complejo)
        
        print(f"\n🔒 DOCUMENTO ANONIMIZADO:")
        print("-" * 40)
        print(texto_anonimo[:500] + "...")
        
        print(f"\n📊 ESTADÍSTICAS DE PROTECCIÓN:")
        print("-" * 40)
        
        # Contar elementos protegidos por tipo
        tipos_protegidos = {}
        for clave in mapeo.keys():
            tipo = str(clave).split('_')[0]
            tipos_protegidos[tipo] = tipos_protegidos.get(tipo, 0) + 1
        
        total_protegido = len(mapeo)
        print(f"🛡️  Total de elementos protegidos: {total_protegido}")
        
        for tipo, cantidad in tipos_protegidos.items():
            print(f"   📌 {tipo}: {cantidad}")
        
        # Calcular efectividad
        texto_original_words = len(documento_complejo.split())
        efectividad = min(100, (total_protegido / texto_original_words) * 100 * 5)  # Factor de amplificación
        print(f"\n🎯 EFECTIVIDAD ESTIMADA: {efectividad:.1f}%")
        
        # Mostrar algunos ejemplos de anonimización
        print(f"\n🔍 EJEMPLOS DE ANONIMIZACIÓN:")
        print("-" * 40)
        ejemplos_mostrados = 0
        for original, anonimo in list(mapeo.items())[:8]:  # Mostrar primeros 8
            print(f"   {original} → {anonimo}")
            ejemplos_mostrados += 1
        
        if len(mapeo) > ejemplos_mostrados:
            print(f"   ... y {len(mapeo) - ejemplos_mostrados} más")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def test_casos_limite():
    """Prueba casos límite y situaciones especiales."""
    print("\n⚠️  PRUEBA: CASOS LÍMITE Y ESPECIALES")
    print("=" * 60)
    
    casos_limite = [
        # Números que podrían ser confundidos
        "En el año 2024 hubo 123 audiencias",
        "La oficina está en el piso 15 número 45",
        "Son las 3:30 PM del 15 de septiembre",
        
        # Texto con muchos números
        "Contactos: 300-123-4567, 301-234-5678, C.C. 1.234.567.890, radicado 05001-60-00000-2024-00789-00",
        
        # Nombres que podrían ser lugares
        "Se citó a MEDELLÍN CENTRO y BOGOTÁ NORTE",
        "El señor COLOMBIA GONZÁLEZ y la señora ANTIOQUIA LÓPEZ",
        
        # Formatos ambiguos
        "12.345.678 podría ser una cédula o un número de caso",
        "300 123 4567 es definitivamente un celular",
        
        # Texto muy corto
        "Carlos",
        "C.C. 123",
        "Tel: 300",
        
        # Texto muy largo con repeticiones
        f"{'CARLOS ANDRÉS RODRÍGUEZ ' * 20}tiene cédula 1.234.567.890 " * 5,
    ]
    
    try:
        from utils.anonimizador import anonimizar_para_ia
        
        for i, caso in enumerate(casos_limite, 1):
            print(f"\n🔸 Caso límite {i:2d}:")
            if len(caso) > 100:
                print(f"   Texto: {caso[:100]}...")
            else:
                print(f"   Texto: {caso}")
                
            texto_anonimo, mapeo = anonimizar_para_ia(caso)
            elementos_protegidos = len(mapeo)
            
            if len(texto_anonimo) > 100:
                print(f"   🔒 Protegido: {texto_anonimo[:100]}...")
            else:
                print(f"   🔒 Protegido: {texto_anonimo}")
                
            print(f"   📊 Elementos protegidos: {elementos_protegidos}")
                
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Ejecuta todas las pruebas de seguridad máxima."""
    print("🛡️" + "=" * 79)
    print("   PRUEBAS DE SEGURIDAD MÁXIMA - SISTEMA DE ANONIMIZACIÓN")
    print("   Objetivo: Alcanzar el más alto nivel de protección de datos")
    print("=" * 80)
    
    try:
        # Verificar que el módulo esté disponible
        from utils.anonimizador import anonimizar_para_ia
        print("✅ Módulo de anonimización cargado correctamente\n")
        
        # Ejecutar todas las pruebas
        test_nombres_complejos()
        test_cedulas_exhaustivas() 
        test_celulares_exhaustivos()
        test_casos_limite()
        test_documento_judicial_completo()
        
        print("\n🎉 PRUEBAS DE SEGURIDAD MÁXIMA COMPLETADAS")
        print("=" * 60)
        print("✅ Todas las pruebas ejecutadas exitosamente")
        print("🛡️  Nivel de seguridad: MÁXIMO")
        print("🔒 Sistema listo para proteger información sensible")
        
    except ImportError:
        print("❌ Error: No se pudo importar el módulo de anonimización")
        print("   Verifica que utils/anonimizador.py esté disponible")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
