from filtros_pii import censurar_pii

textos_teste = [
    "Meu CPF é 111.444.777-35, pode me ajudar?",
    "Meu CPF é 123.456.789-00 (inventado, não deveria censurar)",
    "Meu email é vitor@gmail.com para contato",
    "Me liga no (11) 98765-4321 por favor",
    "Essa frase não tem nenhum dado sensível",
]

for texto in textos_teste:
    resultado, tipos = censurar_pii(texto)
    print(f"Original: {texto}")
    print(f"Censurado: {resultado}")
    print(f"Tipos encontrados: {tipos}")
    print("---")