# ⬡ Mini BugTracker

Sistema desktop de rastreamento de defeitos de software, desenvolvido em **Python puro** com interface gráfica **Tkinter** e banco de dados **SQLite**. Não requer instalação de bibliotecas externas.

---

## 📋 Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Como executar](#como-executar)
- [Estrutura do banco de dados](#estrutura-do-banco-de-dados)
- [Fluxo de status dos bugs](#fluxo-de-status-dos-bugs)
- [Campos do relatório de bug](#campos-do-relatório-de-bug)
- [Capturas de tela](#capturas-de-tela)
- [Classificações disponíveis](#classificações-disponíveis)
- [Atalhos de teclado](#atalhos-de-teclado)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Contexto didático](#contexto-didático)

---

## Sobre o projeto

O **Mini BugTracker** é uma ferramenta didática e funcional para o gerenciamento completo do ciclo de vida de defeitos de software. Foi desenvolvido para fins didáticos, permitindo que equipes registrem, classifiquem, acompanhem e fechem bugs por meio de uma interface visual intuitiva.

O sistema segue as boas práticas de documentação de defeitos descritas na literatura de Engenharia de Software, incluindo os campos essenciais de um relatório de bug profissional: ambiente, passos para reproduzir, resultado esperado versus resultado obtido e frequência de ocorrência.

---

## Funcionalidades

### Gerenciamento de bugs
- **Registrar bug** com formulário completo dividido em seções: Identificação, Responsáveis, Ambiente e Descrição do Defeito
- **Editar bug** a qualquer momento durante o ciclo de vida
- **Deletar bug** com confirmação de segurança
- **Reabrir bug** fechado quando necessário

### Fluxo de trabalho
- Avanço de status em cinco etapas com botão de ação contextual
- Diálogo de observações a cada transição de status
- Registro automático de data/hora de criação, atualização e fechamento
- Barra visual de progresso do fluxo na tela de detalhes

### Relatórios
- **Relatório de bug completo** gerado automaticamente a partir dos dados cadastrados
- Visualização formatada com realce de cores por severidade e resultado
- Botão para **copiar o relatório** para a área de transferência

### Organização e consulta
- **Busca** por título e descrição em tempo real
- **Filtro por status** — Aberto, Em análise, Em correção, Verificado ou Fechado
- **Filtro por severidade** — Crítica, Alta, Média ou Baixa
- **Filtro por projeto** via menu suspenso dinâmico
- **Dashboard lateral** com contadores por status e contador de bugs críticos abertos
- Listagem ordenada por data de criação (mais recente primeiro)

---

## Pré-requisitos

| Requisito | Versão mínima |
|-----------|--------------|
| Python    | 3.8+         |
| Tkinter   | Incluso na instalação padrão do Python |
| SQLite3   | Incluso na instalação padrão do Python |

> **Nenhuma biblioteca externa precisa ser instalada.** O projeto utiliza exclusivamente módulos da biblioteca padrão do Python.

### Verificar se o Tkinter está disponível

```bash
python -c "import tkinter; print('Tkinter OK')"
```

Se o comando retornar erro em sistemas Linux, instale com:

```bash
# Ubuntu / Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

---

## Como executar

**1. Clone ou baixe o arquivo**

```bash
# Clonar via git
git clone https://github.com/orlandosaraivajr/bugtracker.git
cd bugtracker

# Ou simplesmente copie o arquivo bug_tracker.py para uma pasta local
```

**2. Execute o programa**

```bash
python mini_bugtracker.py
```

> O banco de dados `bugs.db` será criado automaticamente na mesma pasta do arquivo `.py` na primeira execução.

**3. Migração automática**

Se você já possuía uma versão anterior do `bugs.db`, o sistema detecta as colunas ausentes e realiza a migração automaticamente, sem perda de dados.

---

## Estrutura do banco de dados

O sistema utiliza uma única tabela SQLite chamada `bugs`:

| Coluna               | Tipo    | Descrição                                      |
|----------------------|---------|------------------------------------------------|
| `id`                 | INTEGER | Identificador único auto-incrementado          |
| `titulo`             | TEXT    | Título descritivo do bug                       |
| `descricao`          | TEXT    | Descrição geral do comportamento incorreto     |
| `projeto`            | TEXT    | Projeto ou módulo afetado                      |
| `prioridade`         | TEXT    | Urgência de correção: Crítica / Alta / Média / Baixa |
| `severidade`         | TEXT    | Impacto técnico: Crítica / Alta / Média / Baixa |
| `status`             | TEXT    | Etapa atual no fluxo de trabalho               |
| `ambiente`           | TEXT    | SO, navegador, versão e dispositivo de teste   |
| `passos`             | TEXT    | Passos numerados para reproduzir o defeito     |
| `resultado_esperado` | TEXT    | Comportamento correto esperado                 |
| `resultado_obtido`   | TEXT    | O que o sistema realmente apresentou           |
| `frequencia`         | TEXT    | Com que frequência o bug ocorre                |
| `tipo_defeito`       | TEXT    | Classificação técnica do defeito               |
| `reportado_por`      | TEXT    | Nome do testador que identificou o bug         |
| `responsavel`        | TEXT    | Desenvolvedor responsável pela correção        |
| `criado_em`          | TEXT    | Data e hora de criação (DD/MM/AAAA HH:MM)      |
| `atualizado_em`      | TEXT    | Data e hora da última atualização              |
| `fechado_em`         | TEXT    | Data e hora de fechamento (quando aplicável)   |
| `notas_fechamento`   | TEXT    | Descrição da solução aplicada                  |

---

## Fluxo de status dos bugs

```
Aberto  →  Em análise  →  Em correção  →  Verificado  →  Fechado
```

| Status        | Cor        | Significado                                        |
|---------------|------------|----------------------------------------------------|
| Aberto        | 🟠 Coral   | Bug registrado, aguardando análise                 |
| Em análise    | 🟡 Âmbar   | Bug sendo investigado pela equipe                  |
| Em correção   | 🟣 Roxo    | Desenvolvedor trabalhando na correção              |
| Verificado    | 🔵 Azul    | Correção implementada, aguardando validação do QA  |
| Fechado       | 🟢 Verde   | Bug confirmado como resolvido                      |

A qualquer momento, um bug fechado pode ser **reaberto** caso a correção se mostre insuficiente.

---

## Campos do relatório de bug

O relatório gerado automaticamente pelo sistema segue o padrão profissional de documentação de defeitos e inclui:

```
BUG #[ID]  —  [TÍTULO]
─────────────────────────────────────────────────────────────────────
STATUS              [status atual]
SEVERIDADE          [nível de impacto técnico]
PRIORIDADE          [urgência de correção]
TIPO DE DEFEITO     [classificação técnica]
PROJETO             [módulo afetado]
REPORTADO POR       [testador]
RESPONSÁVEL         [desenvolvedor]
CRIADO EM           [data/hora]
ATUALIZADO EM       [data/hora]

AMBIENTE
─────────────────────────────────────────────────────────────────────
[Sistema operacional, navegador, versão, dispositivo]

DESCRIÇÃO
─────────────────────────────────────────────────────────────────────
[Descrição geral do comportamento incorreto]

PASSOS PARA REPRODUZIR
─────────────────────────────────────────────────────────────────────
[Passos numerados para reprodução do defeito]

RESULTADO ESPERADO
─────────────────────────────────────────────────────────────────────
[Comportamento correto que o sistema deveria apresentar]

RESULTADO OBTIDO
─────────────────────────────────────────────────────────────────────
[O que o sistema realmente fez]

FREQUÊNCIA DE OCORRÊNCIA
─────────────────────────────────────────────────────────────────────
[Sempre (100%) / Frequente (~75%) / Ocasional (~50%) / Raro (~10%)]
```

---

## Classificações disponíveis

### Severidade e Prioridade
| Nível    | Cor        |
|----------|------------|
| Crítica  | 🔴 Vermelho |
| Alta     | 🟡 Âmbar   |
| Média    | 🔵 Azul    |
| Baixa    | 🟢 Verde   |

### Tipo de Defeito
| Tipo        | Descrição                                              |
|-------------|--------------------------------------------------------|
| Lógica      | Erro no raciocínio ou algoritmo do código              |
| Interface   | Problema visual ou de interação com o usuário          |
| Desempenho  | Lentidão ou comportamento inadequado sob carga         |
| Segurança   | Vulnerabilidade de acesso ou proteção de dados         |
| Integração  | Falha na comunicação entre módulos ou sistemas         |
| Dados       | Erro no armazenamento, leitura ou cálculo de dados     |
| Outro       | Defeitos que não se enquadram nas categorias anteriores|

### Frequência de Ocorrência
| Frequência        | Descrição                              |
|-------------------|----------------------------------------|
| Sempre (100%)     | Reproduzível em todas as tentativas    |
| Frequente (~75%)  | Ocorre na maioria das tentativas       |
| Ocasional (~50%)  | Ocorre aproximadamente metade das vezes|
| Raro (~10%)       | Difícil de reproduzir, parece aleatório|

---

## Atalhos de teclado

| Atalho       | Ação                  |
|--------------|-----------------------|
| `Ctrl + N`   | Registrar novo bug    |
| `Enter`      | Confirmar formulários |

---

## Estrutura do projeto

```
bugtracker/
│
├── bug_tracker.py      # Aplicação completa (arquivo único)
└── bugs.db             # Banco de dados SQLite (gerado automaticamente)
```

O projeto foi intencionalmente desenvolvido em **arquivo único** para facilitar a distribuição, o estudo do código e o uso em ambientes educacionais.

---

## Contexto didático

Este sistema foi desenvolvido como ferramenta de apoio e ilustra na prática os conceitos estudados em aula:

- **Identificação e classificação de defeitos** — os campos de severidade, prioridade e tipo de defeito uma prática didática em um ambiente controlado.

- **Uso de ferramentas de rastreamento** — o próprio sistema é um exemplo funcional de ferramenta de rastreamento, comparável a soluções de mercado como Jira, GitHub Issues e Redmine.

- **Criação de relatórios de testes eficazes** — o formulário de cadastro e o relatório gerado seguem a estrutura profissional: ambiente, passos para reproduzir, resultado esperado versus resultado obtido e frequência de ocorrência

---

*Desenvolvido para fins educacionais*