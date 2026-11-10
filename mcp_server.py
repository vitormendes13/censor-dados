"""Servidor MCP (stdio) que expõe censura de PII e validação de CPF."""
from typing import Annotated, Any, TypedDict

from pydantic import ValidationError, WithJsonSchema
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from filtros_pii import censurar_pii as _censurar_pii
from validadores import validar_cpf as _validar_cpf

MAX_TEXTO = 10_000
MAX_CPF = 20
CARACTERES_CPF = set("0123456789.-, ")


class ErroEntrada(ValueError):
    """Erro de entrada cuja mensagem é segura para devolver ao cliente."""


class FastMCPSemEco(FastMCP):
    """
    FastMCP que nunca devolve ao cliente trecho dos argumentos recebidos.
    Só mensagens de ErroEntrada passam; qualquer outro erro (ex.: o
    pydantic, que inclui input_value) vira uma mensagem genérica.
    """

    async def call_tool(self, name, arguments):
        try:
            return await super().call_tool(name, arguments)
        except ToolError as erro:
            causa = erro.__cause__
            if isinstance(causa, ErroEntrada):
                raise ToolError(f"Erro na tool '{name}': {causa}") from None
            if isinstance(causa, ValidationError):
                ausentes = sorted(
                    str(e["loc"][0]) for e in causa.errors() if e["type"] == "missing" and e["loc"]
                )
                detalhe = f" Argumento obrigatório ausente: {', '.join(ausentes)}." if ausentes else ""
                raise ToolError(f"Argumentos inválidos para a tool '{name}'.{detalhe}") from None
            if causa is None:
                raise ToolError("Tool desconhecida.") from None
            raise ToolError(f"Erro interno ao executar a tool '{name}'.") from None


mcp = FastMCPSemEco("censor-dados", log_level="WARNING")


class ResultadoCensura(TypedDict):
    texto_censurado: str
    tipos_encontrados: list[str]


def _exigir_str(valor: object, nome: str, limite: int) -> str:
    """
    Garante que o valor é string e respeita o limite de tamanho.
    As mensagens de erro nunca incluem o valor recebido.
    """
    if not isinstance(valor, str):
        raise ErroEntrada(f"'{nome}' deve ser uma string.")
    if len(valor) > limite:
        raise ErroEntrada(f"'{nome}' excede o limite de {limite} caracteres.")
    return valor


@mcp.tool()
def censurar_pii(
    texto: Annotated[Any, WithJsonSchema(
        {"type": "string", "maxLength": MAX_TEXTO, "description": "Texto a ser censurado."}
    )],
) -> ResultadoCensura:
    """Substitui CPF (válido), e-mail e telefone por placeholders [TIPO_OCULTO]."""
    texto = _exigir_str(texto, "texto", MAX_TEXTO)
    texto_censurado, tipos = _censurar_pii(texto)
    return {"texto_censurado": texto_censurado, "tipos_encontrados": tipos}


@mcp.tool()
def validar_cpf(
    cpf: Annotated[Any, WithJsonSchema(
        {"type": "string", "maxLength": MAX_CPF, "description": "CPF com ou sem pontuação."}
    )],
) -> bool:
    """Valida matematicamente os dígitos verificadores de um CPF."""
    cpf = _exigir_str(cpf, "cpf", MAX_CPF)
    if not set(cpf) <= CARACTERES_CPF:
        return False
    return _validar_cpf(cpf)


if __name__ == "__main__":
    mcp.run(transport="stdio")
