# Contributing / Contribuindo

**PT-BR** | [EN](#english)

---

## PT-BR

Obrigado por querer contribuir com o vidgrab!

### Pré-requisitos

- Python 3.11+
- [Poetry](https://python-poetry.org/)
- [ffmpeg](https://ffmpeg.org/) no PATH

### Configuração do ambiente

```bash
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber
poetry install
poetry run pre-commit install
```

### Rodando os testes

```bash
poetry run pytest
```

### Verificando qualidade de código

```bash
poetry run ruff check vidgrab/
poetry run pylint vidgrab/
poetry run mypy vidgrab/ --ignore-missing-imports --strict
```

Ou rode tudo de uma vez via pre-commit:

```bash
poetry run pre-commit run --all-files
```

### Convenção de commits

Este projeto segue [Conventional Commits](https://www.conventionalcommits.org/):

| Prefixo | Quando usar |
| --- | --- |
| `feat:` | Nova funcionalidade visível ao usuário → bump **minor** |
| `fix:` | Correção de bug → bump **patch** |
| `docs:` | Apenas documentação → bump **patch** |
| `ci:` | Mudanças em workflows / CI → bump **patch** |
| `chore:` | Manutenção interna (deps, versão) → sem bump |
| `test:` | Adição ou correção de testes → sem bump |
| `refactor:` | Refatoração sem mudança de comportamento → sem bump |

### Configurando Codecov (maintainers only)

Para que o badge de cobertura funcione, você precisa conectar o repositório ao Codecov:

1. Acesse [codecov.io](https://codecov.io) e faça login com sua conta GitHub
2. Autorize o app Codecov a acessar seus repositórios
3. Clique em "Add new repository" e selecione `gsjonio/video_grabber`
4. Copie o token gerado (ou gere um novo em Settings)
5. No repositório GitHub, vá para **Settings → Secrets and variables → Actions**
6. Clique em "New repository secret" e adicione:
   - **Name**: `CODECOV_TOKEN`
   - **Value**: `<token_do_codecov>`

Após isso, o badge de cobertura será atualizado automaticamente em cada push.

### Abrindo um PR

1. Crie um branch a partir de `main`: `git checkout -b feat/minha-feature`
2. Faça commits pequenos e focados (um assunto por commit)
3. Certifique-se de que `poetry run pytest` e todos os linters passam
4. Abra o PR com uma descrição clara do problema e da solução

A branch `main` requer **histórico linear** — use `git rebase`, não merge.

---

## English

Thanks for wanting to contribute to vidgrab!

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/)
- [ffmpeg](https://ffmpeg.org/) on PATH

### Environment setup

```bash
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber
poetry install
poetry run pre-commit install
```

### Running the tests

```bash
poetry run pytest
```

### Checking code quality

```bash
poetry run ruff check vidgrab/
poetry run pylint vidgrab/
poetry run mypy vidgrab/ --ignore-missing-imports --strict
```

Or run everything at once via pre-commit:

```bash
poetry run pre-commit run --all-files
```

### Commit convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | When to use |
| --- | --- |
| `feat:` | New user-visible feature → **minor** bump |
| `fix:` | Bug fix → **patch** bump |
| `docs:` | Documentation only → **patch** bump |
| `ci:` | Workflow / CI changes → **patch** bump |
| `chore:` | Internal maintenance (deps, version) → no bump |
| `test:` | Adding or fixing tests → no bump |
| `refactor:` | Refactor without behaviour change → no bump |

### Setting up Codecov (maintainers only)

To enable the coverage badge, you need to connect the repository to Codecov:

1. Go to [codecov.io](https://codecov.io) and sign in with your GitHub account
2. Authorize the Codecov app to access your repositories
3. Click "Add new repository" and select `gsjonio/video_grabber`
4. Copy the generated token (or create a new one in Settings)
5. In the GitHub repository, go to **Settings → Secrets and variables → Actions**
6. Click "New repository secret" and add:
   - **Name**: `CODECOV_TOKEN`
   - **Value**: `<your_codecov_token>`

After that, the coverage badge will update automatically on every push.

### Opening a PR

1. Branch off `main`: `git checkout -b feat/my-feature`
2. Make small, focused commits (one topic per commit)
3. Make sure `poetry run pytest` and all linters pass
4. Open the PR with a clear description of the problem and solution

The `main` branch requires **linear history** — use `git rebase`, not merge.
