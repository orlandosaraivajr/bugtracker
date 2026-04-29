# Lista de Requisitos de Teste — Calculadora de Notas

**Aplicação:** Calculadora de Notas em Python/Tkinter  
**Objetivo didático:** Praticar identificação de casos de teste, classificação por tipo e elaboração de resultado esperado vs. obtido.

---

# Contexto para o aluno

Antes de executar os testes, lembre-se da lógica implementada na aplicação:

- **Média ≥ 6,0 → Aprovado (verde)**
- **Média entre 4,0 e 5,9 → Em Recuperação (amarelo)**
- **Média entre 0,0 e 3,9 → Reprovado (vermelho)**
- **Notas válidas:** valores numéricos entre **0 e 10**

---

# Requisitos de Teste

---

## RT-001 — Nota com valor negativo

**Tipo:** Validação de entrada  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: João Silva  
- Nota 1: -1  
- Nota 2: 8  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve exibir uma mensagem de aviso informando que as notas devem estar entre **0 e 10**, sem calcular a média.

**Critério de aprovação**

Nenhum resultado é apresentado na tela de média; a mensagem de erro é exibida.

---

## RT-002 — Nota com valor acima do máximo permitido

**Tipo:** Validação de entrada  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: Maria Souza  
- Nota 1: 10  
- Nota 2: 11  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve exibir mensagem de aviso indicando que o valor **11** está fora do intervalo permitido (**0 a 10**), sem exibir resultado.

**Critério de aprovação**

Mensagem de erro exibida; painel de resultado permanece oculto.

---

## RT-003 — Campo de nome vazio

**Tipo:** Validação de campo obrigatório  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: (vazio)  
- Nota 1: 7  
- Nota 2: 8  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve exibir aviso solicitando que o **nome do aluno** seja informado, sem prosseguir com o cálculo.

**Critério de aprovação**

Mensagem de campo obrigatório exibida; nenhuma média calculada.

---

## RT-004 — Média exatamente igual a 6,0 (fronteira de aprovação)

**Tipo:** Teste de valor-limite  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: Carlos Lima  
- Nota 1: 6  
- Nota 2: 6  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve exibir:

- Média **6,0**
- Mensagem **"Aprovado"**
- Cor **verde**

**Critério de aprovação**

Situação exibida é **Aprovado**; cor do texto é **verde**; média exibida é **6,0**.

---

## RT-005 — Média exatamente igual a 4,0 (fronteira de recuperação)

**Tipo:** Teste de valor-limite  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: Ana Paula  
- Nota 1: 4  
- Nota 2: 4  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve exibir:

- Média **4,0**
- Mensagem **"Em Recuperação"**
- Cor **amarela**

**Critério de aprovação**

Situação exibida é **Em Recuperação**; cor do texto é **amarela**; média exibida é **4,0**.

---

## RT-006 — Nota informada com vírgula como separador decimal

**Tipo:** Compatibilidade de formato de entrada  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: Pedro Alves  
- Nota 1: 7,5  
- Nota 2: 8,5  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve reconhecer a vírgula como separador decimal, calcular a média **8,0** e exibir **"Aprovado"** em **verde**.

**Critério de aprovação**

Média calculada corretamente; sem mensagem de erro por formato.

---

## RT-007 — Entrada de texto no campo de nota

**Tipo:** Validação de tipo de dado  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: Fernanda Costa  
- Nota 1: sete  
- Nota 2: 8  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve exibir mensagem de aviso informando que as notas devem ser **valores numéricos**, sem calcular a média.

**Critério de aprovação**

Mensagem de erro de tipo exibida; painel de resultado permanece oculto.

---

## RT-008 — Média resultando em situação "Reprovado"

**Tipo:** Teste funcional de regra de negócio  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: Lucas Mendes  
- Nota 1: 2  
- Nota 2: 3  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve exibir:

- Média **2,5**
- Mensagem **"Reprovado"**
- Cor **vermelha**

**Critério de aprovação**

Situação exibida é **Reprovado**; cor do texto é **vermelha**; média exibida é **2,5**.

---

## RT-009 — Funcionamento do botão Limpar após cálculo

**Tipo:** Teste funcional de interface  

**Pré-condição:**  
Um cálculo já foi realizado e o painel de resultado está visível.

**Entrada**

Nenhuma — apenas acionar o botão.

**Ação**

Clicar no botão **↺ Limpar**

**Resultado esperado**

- Todos os campos de entrada devem ser esvaziados  
- Os placeholders devem retornar  
- O painel de resultado deve desaparecer da tela

**Critério de aprovação**

Campos em branco; painel de resultado oculto; aplicação no estado inicial.

---

## RT-010 — Notas nos extremos válidos (0 e 10)

**Tipo:** Teste de valor-limite  

**Pré-condição:**  
Aplicação aberta e em estado inicial.

**Entrada**

- Nome: Beatriz Torres  
- Nota 1: 0  
- Nota 2: 10  

**Ação**

Clicar no botão **Calcular**

**Resultado esperado**

O sistema deve:

- Aceitar os valores sem erro
- Calcular média **5,0**
- Exibir **"Em Recuperação"** em **amarelo**

**Critério de aprovação**

Nenhuma mensagem de erro; média exibida é **5,0**; situação **Em Recuperação** em **amarelo**.

---

# Tabela Resumo

| ID | Descrição resumida | Tipo | Resultado esperado |
|----|-------------------|------|-------------------|
| RT-001 | Nota 1 com valor negativo (-1) | Validação de entrada | Mensagem de erro |
| RT-002 | Nota 2 acima do máximo (11) | Validação de entrada | Mensagem de erro |
| RT-003 | Nome do aluno vazio | Campo obrigatório | Mensagem de erro |
| RT-004 | Média exatamente 6,0 | Valor-limite | Aprovado (verde) |
| RT-005 | Média exatamente 4,0 | Valor-limite | Em Recuperação (amarelo) |
| RT-006 | Nota com vírgula decimal (7,5) | Formato de entrada | Cálculo correto |
| RT-007 | Texto no campo de nota ("sete") | Tipo de dado | Mensagem de erro |
| RT-008 | Média resultando em reprovação (2,5) | Regra de negócio | Reprovado (vermelho) |
| RT-009 | Botão Limpar após cálculo | Interface | Estado inicial restaurado |
| RT-010 | Notas nos extremos válidos (0 e 10) | Valor-limite | Em Recuperação (amarelo) |

---

# Dica para a atividade

Execute cada requisito **na ordem apresentada**, registre o **resultado obtido** em cada teste e compare com o **resultado esperado**.

Quando o resultado obtido diferir do esperado, você encontrou um **defeito** — registre-o.

# Gabarito

Você poderá acessar o [Gabarito](gabarito.md) da atividade proposta.