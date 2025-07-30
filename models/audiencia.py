from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Audiencia:
    """Modelo de datos para una audiencia."""

    radicado: str
    tipo: str
    fecha: str
    hora: str
    juzgado: str
    realizada_si: str
    realizada_no: str
    motivos: List[str]
    observaciones: str

    def __post_init__(self):
        """Validaciones básicas después de crear el objeto."""
        if not self.radicado:
            raise ValueError("El radicado es obligatorio")
        if not self.tipo:
            raise ValueError("El tipo de audiencia es obligatorio")

    @classmethod
    def from_form_data(cls, datos: dict) -> "Audiencia":
        """Crea una instancia de Audiencia desde los datos del formulario."""
        return cls(
            radicado=datos["radicado"],
            tipo=datos["tipo"],
            fecha=datos["fecha"],
            hora=datos["hora"],
            juzgado=datos["juzgado"],
            realizada_si=datos["realizada_si"],
            realizada_no=datos["realizada_no"],
            motivos=datos["motivos"],
            observaciones=datos["observaciones"],
        )

    def to_excel_row(self) -> List[str]:
        """Convierte los datos a una fila de Excel."""
        row = [
            self.radicado,
            self.tipo,
            self.fecha,
            self.hora,
            self.juzgado,
            self.realizada_si,
            self.realizada_no,
        ]
        row.extend(self.motivos)
        row.append(self.observaciones)
        return row

    def validate_date(self) -> bool:
        """Valida que la fecha tenga el formato correcto."""
        try:
            datetime.strptime(self.fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False
