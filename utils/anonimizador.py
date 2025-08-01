"""
Módulo de anonimización de datos para uso seguro con OpenAI Free Tier.
Protege información sensible en textos judiciales antes del procesamiento de IA.
"""

import re
import random
from typing import Dict, Tuple


class AnonimizadorDatos:
    """Anonimiza datos sensibles en textos judiciales para uso seguro con IA."""
    
    def __init__(self):
        self.mapeo_nombres = {}
        self.mapeo_radicados = {}
        self.mapeo_cedulas = {}
        self.mapeo_juzgados = {}
        self.mapeo_celulares = {}
        self.mapeo_tarjetas = {}
        self.mapeo_correos = {}
        self.mapeo_direcciones = {}
        
        # Nombres ficticios EXPANDIDOS para máxima variedad y seguridad
        self.nombres_ficticios = [
            # FORMATO TRADICIONAL (Nombre Apellido Apellido)
            "JUAN PÉREZ GARCÍA", "MARÍA GONZÁLEZ LÓPEZ", "CARLOS RODRÍGUEZ MARTÍN",
            "ANA FERNÁNDEZ SILVA", "LUIS MARTÍN RUIZ", "CARMEN SÁNCHEZ TORRES",
            "JOSÉ LÓPEZ HERNÁNDEZ", "PILAR GARCÍA MORENO", "ANTONIO RUIZ JIMÉNEZ",
            "TERESA MARTÍN ALONSO", "FRANCISCO TORRES RAMOS", "ISABEL HERNÁNDEZ VEGA",
            "PEDRO MORALES DÍAZ", "LAURA JIMÉNEZ CASTRO", "MIGUEL VARGAS LUNA",
            "SOFÍA MENDOZA RUIZ", "DIEGO HERRERA VEGA", "CAMILA ORTIZ PEÑA",
            
            # FORMATO JUDICIAL (APELLIDO, NOMBRE)  
            "PÉREZ GARCÍA, JUAN", "GONZÁLEZ LÓPEZ, MARÍA", "RODRÍGUEZ MARTÍN, CARLOS",
            "FERNÁNDEZ SILVA, ANA", "MARTÍN RUIZ, LUIS", "SÁNCHEZ TORRES, CARMEN",
            "LÓPEZ HERNÁNDEZ, JOSÉ", "GARCÍA MORENO, PILAR", "RUIZ JIMÉNEZ, ANTONIO",
            "MARTÍN ALONSO, TERESA", "TORRES RAMOS, FRANCISCO", "HERNÁNDEZ VEGA, ISABEL",
            
            # NOMBRES EN MINÚSCULAS
            "juan pérez garcía", "maría gonzález lópez", "carlos rodríguez martín",
            "ana fernández silva", "luis martín ruiz", "carmen sánchez torres",
            "josé lópez hernández", "pilar garcía moreno", "antonio ruiz jiménez",
            "teresa martín alonso", "francisco torres ramos", "isabel hernández vega",
            
            # FORMATO JUDICIAL MINÚSCULAS (apellido, nombre)
            "pérez garcía, juan", "gonzález lópez, maría", "rodríguez martín, carlos",
            "fernández silva, ana", "martín ruiz, luis", "sánchez torres, carmen",
            "lópez hernández, josé", "garcía moreno, pilar", "ruiz jiménez, antonio",
            
            # SOLO NOMBRE Y APELLIDO - MAYÚSCULAS
            "JUAN PÉREZ", "MARÍA GONZÁLEZ", "CARLOS RODRÍGUEZ", "ANA FERNÁNDEZ",
            "LUIS MARTÍN", "CARMEN SÁNCHEZ", "JOSÉ LÓPEZ", "PILAR GARCÍA",
            "ANTONIO RUIZ", "TERESA ALONSO", "FRANCISCO TORRES", "ISABEL HERNÁNDEZ",
            "PEDRO MORALES", "LAURA JIMÉNEZ", "MIGUEL VARGAS", "SOFÍA MENDOZA",
            
            # SOLO NOMBRE Y APELLIDO - minúsculas
            "juan pérez", "maría gonzález", "carlos rodríguez", "ana fernández",
            "luis martín", "carmen sánchez", "josé lópez", "pilar garcía",
            "antonio ruiz", "teresa alonso", "francisco torres", "isabel hernández",
            
            # FORMATO MIXTO (Primera letra mayúscula)
            "Juan Pérez García", "María González López", "Carlos Rodríguez Martín",
            "Ana Fernández Silva", "Luis Martín Ruiz", "Carmen Sánchez Torres",
            "José López Hernández", "Pilar García Moreno", "Antonio Ruiz Jiménez",
            
            # NOMBRES ADICIONALES PARA MAYOR VARIEDAD
            "ALEJANDRO VEGA CASTRO", "CRISTINA MORA BLANCO", "EDUARDO LEÓN SANTOS",
            "PATRICIA RAMOS PRIETO", "RICARDO HERRERA CAMPOS", "BEATRIZ NAVARRO CRUZ",
            "alejandro vega castro", "cristina mora blanco", "eduardo león santos",
            "VEGA CASTRO, ALEJANDRO", "MORA BLANCO, CRISTINA", "LEÓN SANTOS, EDUARDO",
            "vega castro, alejandro", "mora blanco, cristina", "león santos, eduardo"
        ]
        
        # Juzgados ficticios
        self.juzgados_ficticios = [
            "JUZGADO PRIMERO PENAL DEL CIRCUITO DE CIUDAD EJEMPLO",
            "TRIBUNAL SUPERIOR DE JURISDICCIÓN MODELO",
            "JUZGADO SEGUNDO PENAL MUNICIPAL DE DISTRITO DEMO",
            "FISCALÍA SECCIONAL DE TERRITORIO MUESTRA"
        ]
        
        # Prefijos de celulares colombianos ficticios
        self.prefijos_celular = ["300", "301", "302", "310", "311", "312", "313", "314", "315", "316", "317", "318", "319", "320", "321", "322", "323", "324", "350", "351"]
        
        # Dominios de correo ficticios
        self.dominios_correo = ["ejemplo.com", "demo.org", "muestra.net", "ficticio.co", "prueba.edu"]
    
    def anonimizar_texto(self, texto: str) -> Tuple[str, Dict]:
        """
        Anonimiza un texto judicial manteniendo la estructura legal.
        
        Args:
            texto: Texto original con datos sensibles
            
        Returns:
            Tuple[str, Dict]: (texto_anonimizado, mapeo_reverso)
        """
        texto_anonimo = texto
        mapeo_reverso = {}
        
        # 1. Anonimizar números de cédula/documento (PRIMERO para evitar conflictos)
        texto_anonimo, mapeo_cedulas = self._anonimizar_cedulas(texto_anonimo)
        mapeo_reverso.update(mapeo_cedulas)
        
        # 2. Anonimizar números de celular
        texto_anonimo, mapeo_celulares = self._anonimizar_celulares(texto_anonimo)
        mapeo_reverso.update(mapeo_celulares)
        
        # 3. Anonimizar tarjetas de crédito
        texto_anonimo, mapeo_tarjetas = self._anonimizar_tarjetas_credito(texto_anonimo)
        mapeo_reverso.update(mapeo_tarjetas)
        
        # 4. Anonimizar correos electrónicos
        texto_anonimo, mapeo_correos = self._anonimizar_correos(texto_anonimo)
        mapeo_reverso.update(mapeo_correos)
        
        # 5. Anonimizar direcciones
        texto_anonimo, mapeo_direcciones = self._anonimizar_direcciones(texto_anonimo)
        mapeo_reverso.update(mapeo_direcciones)
        
        # 6. Anonimizar números profesionales (tarjetas profesionales, etc.)
        texto_anonimo, mapeo_profesionales = self._anonimizar_numeros_profesionales(texto_anonimo)
        mapeo_reverso.update(mapeo_profesionales)
        
        # 7. Anonimizar radicados
        texto_anonimo, mapeo_radicados = self._anonimizar_radicados(texto_anonimo)
        mapeo_reverso.update(mapeo_radicados)
        
        # 8. Anonimizar nombres de personas (ÚLTIMO para evitar conflictos)
        texto_anonimo, mapeo_nombres = self._anonimizar_nombres(texto_anonimo)
        mapeo_reverso.update(mapeo_nombres)
        
        # 9. Anonimizar juzgados específicos
        texto_anonimo, mapeo_juzgados = self._anonimizar_juzgados(texto_anonimo)
        mapeo_reverso.update(mapeo_juzgados)
        
        return texto_anonimo, mapeo_reverso
    
    def _anonimizar_radicados(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza números de radicado manteniendo el formato."""
        mapeo = {}
        
        # Patrones de radicados colombianos
        patrones = [
            r'\b\d{5}-\d{2}-\d{5}-\d{4}-\d{5}-\d{2}\b',  # 11001-60-00000-2024-00000-00
            r'\b\d{11,20}\b',  # Números largos de radicado
            r'\b\d{4}-\d{6}-\d{2}\b',  # 2024-000000-00
        ]
        
        for patron in patrones:
            matches = re.findall(patron, texto)
            for match in matches:
                if match not in mapeo:
                    # Generar radicado ficticio con mismo formato
                    radicado_ficticio = self._generar_radicado_ficticio(match)
                    mapeo[radicado_ficticio] = match
                    texto = texto.replace(match, radicado_ficticio)
        
        return texto, mapeo
    
    def _anonimizar_celulares(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza números de celular."""
        mapeo = {}
        
        # Patrones para números de celular colombianos
        patrones_celulares = [
            r'\b(?:cel|celular|móvil|teléfono)[\s:]*([3][0-9]{2}[\s-]?[0-9]{3}[\s-]?[0-9]{4})\b',  # cel: 300 123 4567
            r'\b([3][0-9]{2}[\s-]?[0-9]{3}[\s-]?[0-9]{4})\b',  # 300 123 4567 directo
            r'\b([3][0-9]{9})\b',  # 3001234567 sin espacios
            r'\+57[\s-]?([3][0-9]{2})[\s-]?([0-9]{3})[\s-]?([0-9]{4})',  # +57 300 123 4567
            r'\b([3][0-9]{2})\.([0-9]{3})\.([0-9]{4})\b',  # 300.123.4567 con puntos
            r'\(57\)\s+([3][0-9]{2})\s+([0-9]{3})\s+([0-9]{4})',  # (57) 300 123 4567
        ]
        
        for patron in patrones_celulares:
            matches = re.findall(patron, texto, re.IGNORECASE)
            for match in matches:
                # Si es una tupla (grupo capturado), reconstruir
                if isinstance(match, tuple):
                    numero_original = ''.join(match)
                else:
                    numero_original = match
                
                if numero_original not in mapeo and len(numero_original) >= 10:
                    # Generar celular ficticio
                    celular_ficticio = self._generar_celular_ficticio(numero_original)
                    mapeo[celular_ficticio] = numero_original
                    texto = texto.replace(numero_original, celular_ficticio)
        
        return texto, mapeo
    
    def _anonimizar_tarjetas_credito(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza números de tarjetas de crédito."""
        mapeo = {}
        
        # Patrones para tarjetas de crédito (Visa, MasterCard, American Express)
        patrones_tarjetas = [
            r'\b(?:tarjeta|card|visa|mastercard|amex)[\s:]*([4-6][0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4})\b',  # Con etiqueta 16 dígitos
            r'\b(?:tarjeta|card|amex|american\s+express)[\s:]*([3][0-9]{3}[\s-]?[0-9]{6}[\s-]?[0-9]{5})\b',  # Amex 15 dígitos
            r'\b([4-6][0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4})\b',  # Solo número 16 dígitos
            r'\b([3][0-9]{3}[\s-]?[0-9]{6}[\s-]?[0-9]{5})\b',  # Solo número Amex 15 dígitos
            r'\b([4-6][0-9]{15})\b',  # Sin espacios ni guiones 16 dígitos
            r'\b([3][0-9]{14})\b',  # Sin espacios ni guiones Amex 15 dígitos
            r'terminada\s+en\s+(\d{4})',  # Terminada en 1234
        ]
        
        for patron in patrones_tarjetas:
            matches = re.findall(patron, texto, re.IGNORECASE)
            for match in matches:
                if match not in mapeo and len(match.replace(' ', '').replace('-', '')) >= 4:
                    # Generar tarjeta ficticia
                    tarjeta_ficticia = self._generar_tarjeta_ficticia(match)
                    mapeo[tarjeta_ficticia] = match
                    texto = texto.replace(match, tarjeta_ficticia)
        
        return texto, mapeo
    
    def _anonimizar_correos(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza direcciones de correo electrónico."""
        mapeo = {}
        
        # Patrón para correos electrónicos
        patron_correos = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        
        matches = re.findall(patron_correos, texto)
        for match in matches:
            if match not in mapeo:
                # Generar correo ficticio
                correo_ficticio = self._generar_correo_ficticio(match)
                mapeo[correo_ficticio] = match
                texto = texto.replace(match, correo_ficticio)
        
        return texto, mapeo
    
    def _anonimizar_direcciones(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza direcciones físicas."""
        mapeo = {}
        
        # Patrones para direcciones colombianas
        patrones_direcciones = [
            r'(?:dirección|dir\.|domicilio)[\s:]*([A-Za-z0-9\s#\-,]{15,80})',  # Con etiqueta
            r'\b(?:calle|carrera|avenida|av\.|cr\.|cl\.)[\s]+[0-9A-Za-z\s#\-]{10,50}',  # Formato típico colombiano
            r'\b[A-Za-z]+[\s]+[0-9]+[\s]*#[0-9\-]+[A-Za-z0-9\s]*',  # Carrera 15 #45-67
        ]
        
        for patron in patrones_direcciones:
            matches = re.findall(patron, texto, re.IGNORECASE)
            for match in matches:
                if len(match) > 10 and match not in mapeo:
                    # Generar dirección ficticia
                    direccion_ficticia = self._generar_direccion_ficticia(match)
                    mapeo[direccion_ficticia] = match
                    texto = texto.replace(match, direccion_ficticia)
        
        return texto, mapeo
    
    def _anonimizar_numeros_profesionales(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza números de tarjetas profesionales y similares."""
        mapeo = {}
        
        # Patrones para números profesionales
        patrones_profesionales = [
            r'Tarjeta\s+Profesional:\s*(\d{4,8})',  # Tarjeta Profesional: 123456
            r'T\.P\.?\s*(\d{4,8})',  # T.P. 123456
            r'Registro:\s*(\d{4,8})',  # Registro: 123456
        ]
        
        for patron in patrones_profesionales:
            matches = re.findall(patron, texto)
            for match in matches:
                if match not in mapeo:
                    # Generar número profesional ficticio
                    numero_ficticio = ''.join([str(random.randint(0, 9)) for _ in range(len(match))])
                    # Asegurar que no sea igual
                    while numero_ficticio == match:
                        numero_ficticio = ''.join([str(random.randint(0, 9)) for _ in range(len(match))])
                    
                    mapeo[numero_ficticio] = match
                    texto = texto.replace(match, numero_ficticio)
        
        return texto, mapeo
    
    def _anonimizar_nombres(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza nombres de personas con MÁXIMA SEGURIDAD - todos los formatos."""
        mapeo = {}
        
        # Patrones EXHAUSTIVOS para máxima detección de nombres
        patrones_nombres = [
            # 1. APELLIDO, NOMBRE (formato judicial típico) - MAYÚSCULAS
            r'([A-ZÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ]+)*,\s*[A-ZÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ]+)*)',
            
            # 2. APELLIDO, NOMBRE (formato judicial) - minúsculas
            r'([a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)*,\s*[a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)*)',
            
            # 3. APELLIDO, NOMBRE (formato judicial) - Mixto
            r'([A-Za-záéíóúñÁÉÍÓÚÑ]+(?:\s+[A-Za-záéíóúñÁÉÍÓÚÑ]+)*,\s*[A-Za-záéíóúñÁÉÍÓÚÑ]+(?:\s+[A-Za-záéíóúñÁÉÍÓÚÑ]+)*)',
            
            # 4. Después de roles específicos - MAYÚSCULAS
            r'(?:Imputado|Defensor|Fiscal|Víctima|señor|señora|Dr\.|Dra\.|Abg\.|Testigo|Abogado)[\s:]*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{8,60})',
            
            # 5. Después de roles específicos - minúsculas
            r'(?:imputado|defensor|fiscal|víctima|señor|señora|dr\.|dra\.|abg\.|testigo|abogado)[\s:]*([a-záéíóúñ][a-záéíóúñ\s]{8,60})',
            
            # 6. Nombres completos 3-5 palabras MAYÚSCULAS
            r'\b([A-ZÁÉÍÓÚÑ]{2,}(?:\s+[A-ZÁÉÍÓÚÑ]{2,}){2,4})\b',
            
            # 7. Nombres completos 3-5 palabras minúsculas  
            r'\b([a-záéíóúñ]{2,}(?:\s+[a-záéíóúñ]{2,}){2,4})\b',
            
            # 8. Solo nombre y apellido - MAYÚSCULAS (más restrictivo)
            r'\b([A-ZÁÉÍÓÚÑ]{3,20}\s+[A-ZÁÉÍÓÚÑ]{3,20})\b',
            
            # 9. Solo nombre y apellido - minúsculas
            r'\b([a-záéíóúñ]{3,20}\s+[a-záéíóúñ]{3,20})\b',
            
            # 10. Formato Título (Primera letra mayúscula)
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,4})\b',
            
            # 11. Formato mixto (Juan PÉREZ García)
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ]{2,})+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\b',
            
            # 12. En contextos legales específicos - MAYÚSCULAS
            r'\b([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{15,45})\s+(?:compareció|declaró|manifestó|expuso|asistió|no\s+compareció)',
            
            # 13. En contextos legales específicos - minúsculas
            r'\b([a-záéíóúñ][a-záéíóúñ\s]{15,45})\s+(?:compareció|declaró|manifestó|expuso|asistió|no\s+compareció)',
            
            # 14. Patrones "El señor/La señora" + NOMBRE
            r'(?:El\s+señor|La\s+señora|El\s+imputado|La\s+víctima)\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{8,40})\s+(?:identificado|portador|compareció|declaró)',
            
            # 15. Patrones "el señor/la señora" + nombre (minúsculas)
            r'(?:el\s+señor|la\s+señora|el\s+imputado|la\s+víctima)\s+([a-záéíóúñ][a-záéíóúñ\s]{8,40})\s+(?:identificado|portador|compareció|declaró)',
        ]
        
        nombres_usados = []
        
        for patron in patrones_nombres:
            matches = re.findall(patron, texto)
            for match in matches:
                # Si el patrón captura grupos, tomar el primer grupo
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1] if len(match) > 1 else ""
                
                match = match.strip()
                if match and self._es_nombre_persona(match) and match not in mapeo:
                    # Asignar nombre ficticio
                    nombre_ficticio = self._obtener_nombre_ficticio(nombres_usados)
                    nombres_usados.append(nombre_ficticio)
                    mapeo[nombre_ficticio] = match
                    texto = texto.replace(match, nombre_ficticio)
        
        return texto, mapeo
    
    def _anonimizar_cedulas(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza números de cédula o documento."""
        mapeo = {}
        
        # Patrones más específicos y completos para cédulas
        patrones_cedula = [
            r'C\.C\.\s*\d{1,3}(?:\.\d{3})*(?:\.\d{1,3})',  # C.C. 1.234.567.890
            r'T\.I\.\s*\d{1,3}(?:\.\d{3})*(?:\.\d{1,3})',  # T.I. 1.098.765.432
            r'Cédula(?:\s+de\s+Ciudadanía)?:\s*\d{1,3}(?:\.\d{3})*(?:\.\d{1,3})',  # Cédula: 1.234.567.890
            r'Documento:\s*\d{1,3}(?:\.\d{3})*(?:\.\d{1,3})',  # Documento: 11.222.333
            r'NIT:\s*\d{1,3}(?:\.\d{3})*(?:\.\d{1,3})(?:-\d)?',  # NIT: 900.123.456-7
            r'RUT:\s*\d{1,3}(?:\.\d{3})*(?:\.\d{1,3})(?:-\d)?',  # RUT: 12.345.678-9
            r'Pasaporte:\s*[A-Z]{2}\d{6,9}',  # Pasaporte: AB1234567
            r'\b\d{1,3}(?:\.\d{3}){2,3}\b',  # Números con puntos (1.234.567.890 o 11.222.333)
            r'\b\d{8,12}\b(?!\s*[:]\s*\d)',  # Números largos sin puntos (evitar horas)
            r'C\.C\.\s*\d{8,12}',  # C.C. sin puntos
            r'T\.I\.\s*\d{8,12}',  # T.I. sin puntos
        ]
        
        for patron in patrones_cedula:
            matches = re.findall(patron, texto)
            for match in matches:
                if match not in mapeo:
                    # Generar cédula ficticia
                    cedula_ficticia = self._generar_cedula_ficticia(match)
                    mapeo[cedula_ficticia] = match
                    texto = texto.replace(match, cedula_ficticia)
        
        return texto, mapeo
    
    def _anonimizar_juzgados(self, texto: str) -> Tuple[str, Dict]:
        """Anonimiza nombres específicos de juzgados."""
        mapeo = {}
        
        # Patrones para juzgados específicos
        patron_juzgado = r'(JUZGADO|TRIBUNAL|FISCALÍA)[^\.]{10,100}'
        
        matches = re.findall(patron_juzgado, texto, re.IGNORECASE)
        for match in matches:
            if match not in mapeo and len(match) > 20:  # Solo juzgados específicos largos
                juzgado_ficticio = random.choice(self.juzgados_ficticios)
                mapeo[juzgado_ficticio] = match
                texto = texto.replace(match, juzgado_ficticio)
        
        return texto, mapeo
    
    def desaronimizar_datos(self, datos_ia: Dict, mapeo_reverso: Dict) -> Dict:
        """
        Revierte la anonimización en los datos extraídos por la IA.
        
        Args:
            datos_ia: Datos extraídos por IA con información anonimizada
            mapeo_reverso: Mapeo para revertir anonimización
            
        Returns:
            Dict: Datos con información real restaurada
        """
        datos_reales = datos_ia.copy()
        
        # Revertir en todos los campos de texto
        for campo, valor in datos_reales.items():
            if isinstance(valor, str):
                for anonimo, real in mapeo_reverso.items():
                    datos_reales[campo] = valor.replace(anonimo, real)
        
        return datos_reales
    
    def _generar_radicado_ficticio(self, radicado_original: str) -> str:
        """Genera un radicado ficticio con el mismo formato."""
        # Mantener formato pero cambiar números
        if '-' in radicado_original:
            partes = radicado_original.split('-')
            nuevas_partes = []
            for parte in partes:
                if parte.isdigit():
                    nueva_parte = ''.join([str(random.randint(0, 9)) for _ in range(len(parte))])
                    # Asegurar que no sea igual al original
                    while nueva_parte == parte:
                        nueva_parte = ''.join([str(random.randint(0, 9)) for _ in range(len(parte))])
                    nuevas_partes.append(nueva_parte)
                else:
                    nuevas_partes.append(parte)
            return '-'.join(nuevas_partes)
        else:
            # Número sin guiones
            return ''.join([str(random.randint(0, 9)) for _ in range(len(radicado_original))])
    
    def _obtener_nombre_ficticio(self, nombres_usados: list) -> str:
        """Obtiene un nombre ficticio no usado."""
        disponibles = [n for n in self.nombres_ficticios if n not in nombres_usados]
        if disponibles:
            return random.choice(disponibles)
        else:
            # Generar nombre adicional si se agotan
            return f"PERSONA_{random.randint(100, 999)} APELLIDO_{random.randint(100, 999)}"
    
    def _generar_cedula_ficticia(self, cedula_original: str) -> str:
        """Genera una cédula ficticia manteniendo el formato."""
        
        # Caso especial: Pasaporte
        if 'Pasaporte:' in cedula_original or re.match(r'[A-Z]{2}\d{6,9}', cedula_original):
            letras = ''.join([chr(random.randint(65, 90)) for _ in range(2)])  # AA-ZZ
            numeros = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            return f"{letras}{numeros}"
        
        # Si contiene prefijo (C.C., T.I., etc.)
        if any(prefijo in cedula_original for prefijo in ['C.C.', 'T.I.', 'Cédula', 'Documento', 'NIT:', 'RUT:']):
            # Extraer solo los números con puntos
            numeros_con_puntos = re.search(r'\d{1,3}(?:\.\d{3})*(?:\.\d{1,3})', cedula_original)
            if numeros_con_puntos:
                numeros_originales = numeros_con_puntos.group()
                nueva_cedula = self._generar_numeros_con_formato(numeros_originales)
                return cedula_original.replace(numeros_originales, nueva_cedula)
        
        # Si es solo números con puntos
        if '.' in cedula_original and cedula_original.replace('.', '').replace('-', '').isdigit():
            return self._generar_numeros_con_formato(cedula_original)
        
        # Si es solo números sin formato
        if cedula_original.replace('-', '').isdigit():
            nueva_cedula = ''.join([str(random.randint(0, 9)) for _ in range(len(cedula_original.replace('-', '')))])
            # Asegurar que no sea igual
            while nueva_cedula == cedula_original.replace('-', ''):
                nueva_cedula = ''.join([str(random.randint(0, 9)) for _ in range(len(cedula_original.replace('-', '')))])
            
            # Restaurar guiones si existían
            if '-' in cedula_original:
                pos_guion = cedula_original.rfind('-')
                return nueva_cedula[:pos_guion] + '-' + nueva_cedula[pos_guion:]
            return nueva_cedula
        
        return cedula_original
    
    def _generar_numeros_con_formato(self, numeros_con_puntos: str) -> str:
        """Genera números ficticios manteniendo el formato con puntos."""
        partes = numeros_con_puntos.split('.')
        nuevas_partes = []
        
        for parte in partes:
            nueva_parte = ''.join([str(random.randint(0, 9)) for _ in range(len(parte))])
            # Evitar que sea igual
            while nueva_parte == parte:
                nueva_parte = ''.join([str(random.randint(0, 9)) for _ in range(len(parte))])
            nuevas_partes.append(nueva_parte)
        
        return '.'.join(nuevas_partes)
    
    def _generar_celular_ficticio(self, celular_original: str) -> str:
        """Genera un número de celular ficticio manteniendo el formato."""
        # Limpiar el número (solo dígitos)
        solo_digitos = re.sub(r'[^\d]', '', celular_original)
        
        if len(solo_digitos) >= 10:
            # Generar con prefijo colombiano ficticio
            prefijo = random.choice(self.prefijos_celular)
            resto = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            nuevo_numero = prefijo + resto
            
            # Mantener el formato original (espacios, guiones)
            if ' ' in celular_original:
                return f"{nuevo_numero[:3]} {nuevo_numero[3:6]} {nuevo_numero[6:]}"
            elif '-' in celular_original:
                return f"{nuevo_numero[:3]}-{nuevo_numero[3:6]}-{nuevo_numero[6:]}"
            else:
                return nuevo_numero
        else:
            # Si es muy corto, generar similar
            return ''.join([str(random.randint(0, 9)) for _ in range(len(solo_digitos))])
    
    def _generar_tarjeta_ficticia(self, tarjeta_original: str) -> str:
        """Genera un número de tarjeta de crédito ficticio."""
        # Limpiar (solo dígitos)
        solo_digitos = re.sub(r'[^\d]', '', tarjeta_original)
        
        # Caso especial: "terminada en XXXX"
        if len(solo_digitos) == 4:
            return str(random.randint(1000, 9999))
        
        # Generar según longitud (15 para Amex, 16 para otros)
        if len(solo_digitos) == 15:  # American Express
            primer_digito = '3'
            resto = ''.join([str(random.randint(0, 9)) for _ in range(14)])
            nueva_tarjeta = primer_digito + resto
            
            # Mantener formato original
            if ' ' in tarjeta_original or '-' in tarjeta_original:
                separador = ' ' if ' ' in tarjeta_original else '-'
                return f"{nueva_tarjeta[:4]}{separador}{nueva_tarjeta[4:10]}{separador}{nueva_tarjeta[10:]}"
            else:
                return nueva_tarjeta
                
        elif len(solo_digitos) == 16:  # Visa, MasterCard, etc.
            primer_digito = solo_digitos[0] if solo_digitos[0] in '456' else '4'  # 4=Visa, 5=MasterCard, 6=Discover
            resto = ''.join([str(random.randint(0, 9)) for _ in range(15)])
            nueva_tarjeta = primer_digito + resto
            
            # Mantener formato original
            if ' ' in tarjeta_original or '-' in tarjeta_original:
                separador = ' ' if ' ' in tarjeta_original else '-'
                return f"{nueva_tarjeta[:4]}{separador}{nueva_tarjeta[4:8]}{separador}{nueva_tarjeta[8:12]}{separador}{nueva_tarjeta[12:]}"
            else:
                return nueva_tarjeta
        else:
            # Longitud no estándar, generar de la misma longitud
            return ''.join([str(random.randint(0, 9)) for _ in range(len(solo_digitos))])
    
    def _generar_correo_ficticio(self, correo_original: str) -> str:
        """Genera un correo electrónico ficticio."""
        try:
            usuario, dominio = correo_original.split('@')
            # Generar usuario ficticio de longitud similar
            nuevo_usuario = 'usuario' + str(random.randint(100, 999))
            nuevo_dominio = random.choice(self.dominios_correo)
            return f"{nuevo_usuario}@{nuevo_dominio}"
        except:
            return f"usuario{random.randint(100, 999)}@ejemplo.com"
    
    def _generar_direccion_ficticia(self, direccion_original: str) -> str:
        """Genera una dirección ficticia manteniendo el formato."""
        # Direcciones ficticias típicas colombianas
        calles = ["Carrera", "Calle", "Avenida", "Diagonal", "Transversal"]
        numeros_principales = [random.randint(10, 150) for _ in range(5)]
        numeros_secundarios = [f"{random.randint(10, 99)}-{random.randint(10, 99)}" for _ in range(5)]
        
        calle = random.choice(calles)
        num_principal = random.choice(numeros_principales)
        num_secundario = random.choice(numeros_secundarios)
        
        return f"{calle} {num_principal} #{num_secundario}"
    
    def _es_nombre_persona(self, texto: str) -> bool:
        """Determina si un texto parece ser un nombre de persona."""
        # Filtrar instituciones obvias
        instituciones = ['JUZGADO', 'TRIBUNAL', 'FISCALÍA', 'MINISTERIO', 'DEFENSORÍA', 
                        'POLICÍA', 'INPEC', 'ICBF', 'AUDIENCIA', 'SALA', 'PENAL',
                        'CIRCUITO', 'MUNICIPAL', 'COLOMBIA', 'BOGOTÁ', 'MEDELLÍN',
                        'CALI', 'BARRANQUILLA', 'NACIONAL', 'DISTRITO']
        
        texto_upper = texto.upper().strip()
        
        for inst in instituciones:
            if inst in texto_upper:
                return False
        
        # Filtrar si contiene números (no es nombre de persona)
        if re.search(r'\d', texto):
            return False
        
        # Debe ser entre 2-5 palabras (aumentado para nombres completos)
        palabras = texto_upper.split()
        if len(palabras) < 2 or len(palabras) > 5:
            return False
        
        # Filtrar palabras muy cortas o muy largas
        for palabra in palabras:
            if len(palabra) < 2 or len(palabra) > 15:
                return False
        
        # Cada palabra debe empezar con letra
        for palabra in palabras:
            if not palabra[0].isalpha():
                return False
        
        # Verificar que no sean solo conectores
        conectores = ['DE', 'DEL', 'LA', 'LAS', 'LOS', 'Y', 'E']
        if all(palabra in conectores for palabra in palabras):
            return False
        
        return True


# Instancia global
anonimizador = AnonimizadorDatos()


def anonimizar_para_ia(texto: str) -> Tuple[str, Dict]:
    """
    Función de conveniencia para anonimizar texto antes de enviarlo a IA.
    
    Args:
        texto: Texto original
        
    Returns:
        Tuple[str, Dict]: (texto_anonimizado, mapeo_reverso)
    """
    return anonimizador.anonimizar_texto(texto)


def restaurar_datos_ia(datos_ia: Dict, mapeo_reverso: Dict) -> Dict:
    """
    Función de conveniencia para restaurar datos reales después de IA.
    
    Args:
        datos_ia: Datos de IA con información anonimizada
        mapeo_reverso: Mapeo para revertir
        
    Returns:
        Dict: Datos con información real
    """
    return anonimizador.desaronimizar_datos(datos_ia, mapeo_reverso)
