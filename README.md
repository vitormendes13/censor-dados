# Censor de Dados

Filtro em Python que detecta e censura dados pessoais (PII) em textos e o expõe como **servidor MCP**, para que o Claude (ou qualquer cliente MCP) use a ferramenta diretamente.

Projeto 2 do meu roteiro de transição para IA aplicada + segurança.

## O que ele faz

Troca dados sensíveis por placeholders:

| Tipo | Detecção | Placeholder |
|------|----------|-------------|
| CPF | regex + **validação dos dígitos verificadores** (CPF inválido não é censurado) | `[CPF_OCULTO]` |
| E-mail | regex | `[EMAIL_OCULTO]` |
| Telefone | regex (com ou sem DDD) | `[TELEFONE_OCULTO]` |

Exemplo:

```
Entrada: Meu CPF é 111.444.777-35 e meu e-mail é fulano@exemplo.com
Saída:   Meu CPF é [CPF_OCULTO] e meu e-mail é [EMAIL_OCULTO]
```

## Estrutura

- `filtros_pii.py`: função `censurar_pii(texto)` → `(texto_censurado, tipos_encontrados)`
- `validadores.py`: `validar_cpf(cpf)`
- `mcp_server.py`: servidor MCP (stdio) com as ferramentas `censurar_pii` e `validar_cpf`
- `teste.py`: testes simples (usa apenas CPF fictício)
- `requirements.txt`: dependências (`mcp==1.30.0`)

## Como rodar

```bash
python -m venv venv
# Windows: venv\Scripts\activate    |   Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python teste.py
```

## Usar como servidor MCP no Claude Code

```bash
claude mcp add censor-dados -- python /caminho/completo/mcp_server.py
```

Use o Python do venv no comando (ex.: `venv\Scripts\python.exe`). O registro vale por computador e por pasta.

## Decisões de segurança

- **Erros sanitizados:** o servidor nunca devolve o texto de entrada em mensagens de erro (evita vazar PII via eco de validação do pydantic).
- **Limites de entrada:** texto até 10.000 caracteres; CPF até 20, só caracteres `0-9 . - ,` e espaço.
- **Sem logs de conteúdo:** log em nível `WARNING`; nada do que o usuário envia é registrado.
- **Fail closed:** na dúvida, o servidor recusa a entrada em vez de processá-la.

## Limitações

Cobre apenas dados com formato previsível (CPF, e-mail, telefone). Não detecta nomes, endereços ou dados em texto livre; isso exigiria NER/ML e fica como evolução.

## Dados de teste

Todos os exemplos usam o CPF fictício `111.444.777-35`. Nunca coloque dados reais no repositório.
