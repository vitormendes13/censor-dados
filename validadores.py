def calcular_digito_verificador(numeros: str, peso_inicial: int) -> int:
    """
    Calcula um dígito verificador de CPF a partir de uma sequência de
    números e do peso inicial (10 para o primeiro dígito, 11 para o segundo).
    """
    peso = peso_inicial
    soma = 0

    for letra in numeros:
        numero = int(letra)
        soma = soma + (numero * peso)
        peso = peso - 1

    resto = (soma * 10) % 11

    if resto == 10 or resto == 11:
        digito_verificador = 0
    else:
        digito_verificador = resto

    return digito_verificador


def validar_cpf(cpf: str) -> bool:
    """
    Valida matematicamente um CPF, aceitando formatação comum
    (pontos, hífen, espaço, vírgula), conferindo se os dígitos
    verificadores batem com o cálculo esperado.
    """
    cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "").replace(",", "")

    if len(cpf_limpo) != 11:
        return False

    primeiros_9 = cpf_limpo[0:9]
    primeiro_digito_calculado = calcular_digito_verificador(primeiros_9, 10)

    primeiros_10 = primeiros_9 + str(primeiro_digito_calculado)
    segundo_digito_calculado = calcular_digito_verificador(primeiros_10, 11)

    digitos_reais = cpf_limpo[9:11]
    digitos_calculados = str(primeiro_digito_calculado) + str(segundo_digito_calculado)

    return digitos_reais == digitos_calculados