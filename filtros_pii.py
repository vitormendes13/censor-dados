import re
from validadores import validar_cpf

# Padrões de dados sensíveis com formato estruturado/previsível
PADROES_PII = {
    "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "EMAIL": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "TELEFONE": r"\b(?:\(\d{2}\)\s?)?\d{4,5}-?\d{4}\b",
}

def censurar_pii(texto: str) -> tuple[str, list[str]]:
    """
    Detecta e substitui dados sensíveis estruturados por placeholders.
    Retorna uma tupla: (texto_censurado, lista_de_tipos_encontrados)
    """
    texto_censurado = texto
    tipos_encontrados = []

    for tipo, padrao in PADROES_PII.items():
        candidatos = re.findall(padrao, texto_censurado)

        for candidato in candidatos:
            if tipo == "CPF":
                if validar_cpf(candidato):
                    tipos_encontrados.append(tipo)
                    texto_censurado = texto_censurado.replace(candidato, f"[{tipo}_OCULTO]")
            else:
                tipos_encontrados.append(tipo)
                texto_censurado = texto_censurado.replace(candidato, f"[{tipo}_OCULTO]")

    return texto_censurado, tipos_encontrados