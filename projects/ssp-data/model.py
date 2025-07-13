from pydantic import BaseModel
from typing import List

class Delito(BaseModel):
    idDelito: int
    idGrupoDelito: int
    delito: str

class ListaDados(BaseModel):
    idOcorrenciaMensal: int
    idDelito: int
    idDistrito: int
    ano: int
    janeiro: int
    fevereiro: int
    marco: int
    abril: int
    maio: int
    junho: int
    julho: int
    agosto: int
    setembro: int
    outubro: int
    novembro: int
    dezembro: int
    publicado: int
    total: int
    delito: Delito

class DataItem(BaseModel):
    ano: int
    listaDados: List[ListaDados]

class APIResponse(BaseModel):
    success: bool
    data: List[DataItem]
    delegacia: str