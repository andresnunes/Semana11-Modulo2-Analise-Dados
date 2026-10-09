"""Funções auxiliares de limpeza de texto, números e datas."""
import re

import pandas as pd

from config import PARTICULAS, SIGLAS


def aparar(serie: pd.Series) -> pd.Series:
    """Remove espaços nas pontas e espaços repetidos; texto vazio vira nulo."""
    serie = serie.str.strip().str.replace(r"\s+", " ", regex=True)
    return serie.replace("", pd.NA)


def capitalizar(texto):
    """'SÃO PAULO' / 'são paulo' -> 'São Paulo'; 'granola sem açúcar 500G'
    -> 'Granola sem Açúcar 500g'."""
    if pd.isna(texto):
        return texto
    palavras = []
    for i, palavra in enumerate(texto.lower().split(" ")):
        if palavra in SIGLAS:
            palavras.append(SIGLAS[palavra])
        elif any(c.isdigit() for c in palavra):
            # Medidas: 900g, 500ml, 1kg ficam minúsculas; litro fica "L"
            palavras.append(re.sub(r"^(\d+)l$", r"\1L", palavra))
        elif i > 0 and palavra in PARTICULAS:
            palavras.append(palavra)
        else:
            # "pré-treino" -> "Pré-Treino"
            palavras.append("-".join(p.capitalize() for p in palavra.split("-")))
    return " ".join(palavras)


def para_numero(serie: pd.Series) -> pd.Series:
    """'1.234,56' (padrão BR) -> 1234.56"""
    return pd.to_numeric(
        serie.str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
        errors="coerce",
    )


def para_data(serie: pd.Series) -> pd.Series:
    return pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")


def faixa_etaria(idade):
    if pd.isna(idade):
        return "Não informado"
    if idade < 25:
        return "18-24"
    if idade < 35:
        return "25-34"
    if idade < 45:
        return "35-44"
    if idade < 60:
        return "45-59"
    return "60+"
