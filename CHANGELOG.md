# Changelog

## [v0.3.0] — 2026-06-21

### ✨ Novas funcionalidades

- **`--dry-run`** — Mostra título, resolução e tamanho estimado sem baixar nada.
  Ideal para inspecionar playlists grandes antes do download.

  ```bash
  vidgrab "https://youtube.com/playlist?list=PLxxx" --playlist --dry-run
  ```

- **Config file** — Salve seus defaults em `~/.config/vidgrab/config.toml`
  para não precisar passar as flags toda vez.

  ```toml
  output = "~/Videos/raw"
  workers = 5
  max_height = 1080
  ```

- **Resume de downloads interrompidos** — `continuedl` habilitado por padrão;
  downloads parciais são retomados automaticamente.

### 🔧 Qualidade

- **Type checking strict** — mypy strict com `dict[str, Any]` em todas as assinaturas
  que recebem dicts do yt-dlp
- **Pipeline de CI expandida** — testes (`pytest`), cobertura (`codecov`),
  type check (`mypy`) e markdownlint adicionados ao workflow
- **Pre-commit hooks** — ruff, pylint, mypy e markdownlint rodam localmente antes de cada commit
- **38 testes unitários** cobrindo `_classify_error`, `_slugify`, `_format_selector`,
  `DownloadConfig`, `VideoMetadata` e helpers do CLI

### 🐛 Correções

- Badge de lint corrigida — `poetry install --with dev` incompatível com formato PEP 735;
  corrigido para `poetry install`
- URLs de clone no README corrigidas (`vidgrab` → `video_grabber`)

---

## [v0.2.0] — 2026-06-21

### ✨ Novas funcionalidades

- **`--write-json`** — O arquivo `.json` de metadados agora é **opt-in**.
  Use a flag para gerá-lo ao lado do vídeo.

  ```bash
  vidgrab https://youtu.be/... --write-json
  ```

- **Aviso de licença Creative Commons** — vidgrab exibe um aviso `⚠ Not Creative Commons`
  quando o vídeo não está sob licença CC, ajudando a rastrear restrições de uso do material.

### 🐛 Correções

- `download()` agora delega para `download_batch()` — erros tratados de forma consistente
  em ambos os métodos
- `_print_summary` não encerra mais o processo internamente de forma oculta
- Escopo de variável corrigido em `expand_playlists`

### 🔧 Chore

- Migração de **setuptools → Poetry**
- Adicionada licença **MIT**

---

## [v0.1.0] — 2026-06-21

Release inicial do vidgrab.

### ✨ Funcionalidades

- Download na maior qualidade disponível (streams DASH, sem re-encode)
- Downloads paralelos via `--workers` (padrão: 3)
- Suporte a playlists via `--playlist`
- Download em lote via `--batch <arquivo.txt>`
- Skip de arquivos existentes; `--force` para re-download
- Limitação de resolução via `--max-height`
- Suporte a cookies via `--cookies` para conteúdo com restrição de idade
- Barra de progresso Rich por download
- Retry automático com backoff exponencial em rate-limits
- Classificação tipada de erros (vídeo indisponível, bloqueio geográfico, restrição de idade)
- Padrão de nome de arquivo: `{upload_date}-{titulo-slug}-{video_id}.{ext}`
