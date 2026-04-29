# ✅ Gabarito — Correção de Bugs
## Atividade: Testes na Calculadora de Notas

 
**Arquivo testado:** `calculadora_notas.py`

---

## Orientações gerais

Antes de aplicar as correções, certifique-se de que:

1. Você **executou os testes** descritos nos requisitos RT-001 a RT-010 e registrou os resultados obtidos
2. Você abriu o arquivo `calculadora_notas.py` em um editor de texto ou IDE de sua preferência
3. Para localizar rapidamente uma linha, use o atalho `Ctrl + G` (VS Code, Gedit) ou `Ctrl + L` (Sublime Text)
4. Após cada correção, **salve o arquivo** e **execute novamente o teste** correspondente para confirmar que o defeito foi resolvido

> 💡 **Dica:** Antes de alterar qualquer linha, faça uma cópia do arquivo original com o nome `calculadora_notas_original.py`. Isso permite comparar o código com bug e o código corrigido a qualquer momento.

---

## Bug 1 — RT-001: Nota com valor negativo

### Descrição do defeito

O sistema permitia que a Nota 1 recebesse o valor `-1` (e outros negativos até `-2`) sem exibir mensagem de erro, prosseguindo com o cálculo da média como se fosse uma entrada válida. O intervalo correto para qualquer nota é de **0 a 10**.

### Localização

| Campo       | Valor                  |
|-------------|------------------------|
| Arquivo     | `calculadora_notas.py` |
| Linha       | **38**                 |
| Função      | `calcular()`           |

### Como identificar a linha

Procure pelo trecho de código que realiza a validação do intervalo das notas. Ele se parece com:

```python
if not (-2 <= nota1 <= 10) or not (0 <= nota2 <= 10):
```

### Correção

**Substitua** a linha 38 de:

```python
if not (-2 <= nota1 <= 10) or not (0 <= nota2 <= 10):
```

**Por:**

```python
if not (0 <= nota1 <= 10) or not (0 <= nota2 <= 10):
```

### O que foi corrigido

O limite inferior da validação da Nota 1 estava incorretamente definido como `-2` em vez de `0`. Isso fazia com que valores negativos entre `-2` e `-0,1` fossem aceitos pelo sistema sem nenhuma mensagem de aviso. A correção alinha a regra da Nota 1 com a regra já correta da Nota 2, garantindo que ambas aceitem apenas valores no intervalo `[0, 10]`.

### Como verificar a correção

1. Execute o programa: `python calculadora_notas.py`
2. Preencha o campo **Nome** com qualquer nome
3. Preencha **Nota 1** com o valor `-1`
4. Preencha **Nota 2** com qualquer valor válido (ex: `8`)
5. Clique em **Calcular**
6. ✅ **Resultado esperado após a correção:** O sistema deve exibir a mensagem *"As notas devem estar entre 0 e 10"* e **não calcular** a média

---

## Bug 2 — RT-004: Média exatamente igual a 6,0 não resulta em "Aprovado"

### Descrição do defeito

Quando a média calculada era exatamente `6,0`, o sistema exibia a mensagem **"Em Recuperação"** em vez de **"Aprovado"**. Isso ocorria porque a condição de aprovação usava o operador `>` (estritamente maior que), excluindo o valor de fronteira `6,0`.

### Localização

| Campo       | Valor                  |
|-------------|------------------------|
| Arquivo     | `calculadora_notas.py` |
| Linha       | **45**                 |
| Função      | `calcular()`           |

### Como identificar a linha

Procure pelo bloco de decisão que define a situação do aluno com base na média. Ele se parece com:

```python
if media > 6:
```

### Correção

**Substitua** a linha 45 de:

```python
if media > 6:
```

**Por:**

```python
if media >= 6:
```

### O que foi corrigido

O operador `>` (maior que) foi substituído por `>=` (maior ou igual a). Com o operador incorreto, a média `6,0` não satisfazia a condição de aprovação e o fluxo seguia para a verificação da faixa de recuperação, resultando em classificação errada. A especificação da aplicação define que **média igual ou superior a 6,0 resulta em Aprovado** — portanto o operador `>=` é o correto.

### Como verificar a correção

1. Execute o programa: `python calculadora_notas.py`
2. Preencha o campo **Nome** com qualquer nome
3. Preencha **Nota 1** com `6`
4. Preencha **Nota 2** com `6`
5. Clique em **Calcular**
6. ✅ **Resultado esperado após a correção:** O sistema deve exibir a média `6,0` e a mensagem **"Aprovado"** na cor **verde**

---

## Resumo das correções

| Requisito | Linha | Código com bug                                               | Código corrigido                                             |
|-----------|-------|--------------------------------------------------------------|--------------------------------------------------------------|
| RT-001    | 38    | `if not (-2 <= nota1 <= 10) or not (0 <= nota2 <= 10):`     | `if not (0 <= nota1 <= 10) or not (0 <= nota2 <= 10):`      |
| RT-004    | 45    | `if media > 6:`                                              | `if media >= 6:`                                             |

---

## Reflexão para o aluno

Estes dois defeitos ilustram categorias distintas de erros muito comuns no desenvolvimento de software:

O **RT-001** é um defeito de **validação de dados**: o intervalo permitido estava incorretamente codificado, aceitando entradas inválidas que deveriam ser rejeitadas. Em sistemas reais — como um sistema bancário ou médico — aceitar valores fora do intervalo permitido pode gerar cálculos incorretos com consequências sérias.

O **RT-004** é um defeito de **lógica de fronteira**: o operador relacional estava errado em exatamente um ponto do intervalo, o valor `6,0`. Esse tipo de defeito é chamado de *off-by-one* (erro de um ponto) e é um dos mais frequentes e mais difíceis de detectar sem testes de valor-limite específicos — exatamente como o RT-004 foi projetado para fazer.

Ambos reforçam a importância de **testar os valores extremos dos intervalos** (0, 6, 10) além dos casos do meio .

