# Changelog

## [Unreleased]

### ♻️ Refatoração / Refactor

- Extraída a lógica específica de cada site para uma estratégia `Source`
  (`vidgrab/sources.py`), preparando a base para novas fontes além do YouTube
  sem mudar o comportamento atual /
  Extracted site-specific logic into a `Source` strategy
  (`vidgrab/sources.py`), preparing the base for sources beyond YouTube
  with no change to current behaviour

### 🐞 Correções / Fixes

- Entradas de playlist de fontes não-YouTube não são mais prefixadas
  incorretamente com `youtube.com` /
  Playlist entries from non-YouTube sources are no longer wrongly prefixed
  with `youtube.com`

---

## [v0.5.2] — 2026-06-21

### 🧪 Testes / Tests

- 21 novos testes para `_collect_urls`, `_print_summary`, e handler `download`
  — elevou `cli.py` de 43% para 93%, total de 92% /
  21 new tests for `_collect_urls`, `_print_summary`, and `download` handler
  — raised `cli.py` from 43% to 93%, overall total to 92%

### Cobertura / Coverage

- **cli.py**: 93% (↑ from 43%)
- **Total**: 92% (↑ from 83%)
- **Tests**: 120 (↑ from 99)

---

## [v0.5.1] — 2026-06-21

### 🧪 Testes / Tests

- 12 novos testes para `_inspect_one`, `download_batch`, `_write_metadata_json`, `_download_one`
  — elevou `downloader.py` de 79% para 90%, total de 83% /
  12 new tests for `_inspect_one`, `download_batch`, `_write_metadata_json`, `_download_one`
  — raised `downloader.py` from 79% to 90%, overall total to 83%

### Cobertura / Coverage

- **downloader.py**: 90% (↑ from 79%)
- **Total**: 83% (↑ from 76%)
- **Tests**: 99 (↑ from 87)

---

## [v0.5.0] — 2026-06-21

### 🧪 Testes / Tests

- 38 novos testes para exceções, `expand_playlists`, `_resolve_output_path`, `_find_existing`, `_build_ydl_opts`
  — elevou coverage de 66% para 76% /
  38 new tests for exceptions, `expand_playlists`, `_resolve_output_path`, `_find_existing`, `_build_ydl_opts`
  — raised coverage from 66% to 76%

### Cobertura / Coverage

- **exceptions.py**: 100% ✅
- **models.py**: 100% ✅
- **config.py**: 100% ✅
- **downloader.py**: 79% (↑ from 67%)
- **cli.py**: 43% (core handler still needs CLI-specific tests)
- **Total**: 76% (↑ from 66%)

---

## [v0.4.3] — 2026-06-21

### 🧪 Testes / Tests

- 11 novos testes para rate-limit handling e exponential backoff
  — validam que o retry funciona em HTTP 429 e falha rápido em erros não-retryáveis /
  11 new tests for rate-limit handling and exponential backoff
  — validate that retry works on HTTP 429 and fails fast on non-retryable errors

### 📚 Documentação / Documentation

- `SECURITY.md` adicionado com política de disclosure responsável de vulnerabilidades /
  `SECURITY.md` added with responsible vulnerability disclosure policy
- `Makefile` adicionado para simplificar comandos de desenvolvimento /
  `Makefile` added to simplify development commands

### 🔧 Chore

- `git-cliff` adicionado para geração automática de CHANGELOG a partir dos commits
  — reduz erro manual e força disciplina de commits /
  `git-cliff` added for automatic CHANGELOG generation from commits
  — reduces manual error and enforces commit discipline

---

## [v0.4.2] — 2026-06-21

### 🔧 Chore

- Codecov configurado com `codecov.yml` e autenticação via `CODECOV_TOKEN` secret /
  Codecov configured with `codecov.yml` and authentication via `CODECOV_TOKEN` secret
- CONTRIBUTING.md atualizado com instruções de setup do Codecov para maintainers /
  CONTRIBUTING.md updated with Codecov setup instructions for maintainers

---

## [v0.4.1] — 2026-06-21

### 📚 Documentação / Documentation

- `CONTRIBUTING.md` adicionado com guia de setup, convenção de commits e processo de PR /
  `CONTRIBUTING.md` added with setup guide, commit convention and PR process
- Issue templates criados para bug report e feature request /
  Issue templates created for bug report and feature request

---

## [v0.4.0] — 2026-06-21

### ✨ Novas funcionalidades / New features

- **`--quiet` / `-q`** — Suprime toda saída exceto erros. Ideal para uso em scripts e pipelines. /
  Suppresses all output except errors. Ideal for scripting and pipelines.

  ```bash
  vidgrab https://youtu.be/dQw4w9WgXcQ --quiet && echo "done"
  ```

- **Shell completion** — Autocompletar para bash, zsh e fish via Typer.
  Instale com o comando abaixo e reabra o terminal. /
  Autocomplete for bash, zsh and fish via Typer. Run the command below and reopen your terminal.

  ```bash
  vidgrab --install-completion
  ```

---

## [v0.3.2] — 2026-06-21

### 🐛 Correções / Bug fixes

- Diretório de saída padrão alterado de `.` (diretório atual) para `~/Downloads` (pasta
  de Downloads do sistema). Aplica-se tanto ao CLI quanto ao `DownloadConfig` diretamente. /
  Default output directory changed from `.` (current directory) to `~/Downloads` (system
  Downloads folder). Applies to both the CLI and `DownloadConfig` used directly.

---

## [v0.3.1] — 2026-06-21

### 📚 Documentação / Documentation

- README expandido com diagrama de arquitetura, tabela de funcionalidades com ícones,
  seção de qualidade de código e estrutura do projeto /
  README expanded with architecture diagram, icon feature table,
  code quality section and project structure
- CHANGELOG convertido para formato bilíngue PT-BR / EN /
  CHANGELOG converted to bilingual PT-BR / EN format

### 🔧 Chore

- Dependências de teste (`pytest`, `pytest-cov`, `codecov`) adicionadas à pipeline de CI /
  Test dependencies (`pytest`, `pytest-cov`, `codecov`) added to CI pipeline

---

## [v0.3.0] — 2026-06-21

### ✨ Novas funcionalidades / New features

- **`--dry-run`** — Mostra título, resolução e tamanho estimado sem baixar nada.
  Ideal para inspecionar playlists grandes antes do download. /
  Shows title, resolution and estimated size without downloading.
  Useful for inspecting large playlists before committing to a download.

  ```bash
  vidgrab "https://youtube.com/playlist?list=PLxxx" --playlist --dry-run
  ```

- **Config file** — Salve seus defaults em `~/.config/vidgrab/config.toml`
  para não precisar passar as flags toda vez. /
  Save your personal defaults in `~/.config/vidgrab/config.toml`
  so you don't have to repeat flags every time.

  ```toml
  output = "~/Videos/raw"
  workers = 5
  max_height = 1080
  ```

- **Resume de downloads interrompidos / Resume interrupted downloads** —
  `continuedl` habilitado por padrão; downloads parciais são retomados automaticamente. /
  `continuedl` enabled by default; partial downloads are resumed automatically.

### 🔧 Qualidade / Quality

- **Type checking strict** — mypy strict com `dict[str, Any]` em todas as assinaturas
  que recebem dicts do yt-dlp /
  mypy strict with `dict[str, Any]` across all signatures receiving yt-dlp dicts
- **Pipeline de CI expandida / Expanded CI pipeline** — testes (`pytest`), cobertura (`codecov`),
  type check (`mypy`) e markdownlint adicionados ao workflow /
  tests (`pytest`), coverage (`codecov`), type check (`mypy`) and markdownlint added to workflow
- **Pre-commit hooks** — ruff, pylint, mypy e markdownlint rodam localmente antes de cada commit /
  ruff, pylint, mypy and markdownlint run locally before every commit
- **38 testes unitários / 38 unit tests** — cobrindo `_classify_error`, `_slugify`,
  `_format_selector`, `DownloadConfig`, `VideoMetadata` e helpers do CLI /
  covering `_classify_error`, `_slugify`, `_format_selector`, `DownloadConfig`,
  `VideoMetadata` and CLI helpers

### 🐛 Correções / Bug fixes

- Badge de lint corrigida — `poetry install --with dev` incompatível com formato PEP 735;
  corrigido para `poetry install` /
  Lint badge fixed — `poetry install --with dev` incompatible with PEP 735 format;
  changed to `poetry install`
- URLs de clone no README corrigidas (`vidgrab` → `video_grabber`) /
  README clone URLs fixed (`vidgrab` → `video_grabber`)

---

## [v0.2.0] — 2026-06-21

### ✨ Novas funcionalidades / New features

- **`--write-json`** — O arquivo `.json` de metadados agora é **opt-in**.
  Use a flag para gerá-lo ao lado do vídeo. /
  The metadata `.json` file is now **opt-in**.
  Use the flag to generate it alongside the video.

  ```bash
  vidgrab https://youtu.be/... --write-json
  ```

- **Aviso de licença Creative Commons / Creative Commons license warning** —
  vidgrab exibe um aviso `⚠ Not Creative Commons` quando o vídeo não está sob licença CC,
  ajudando a rastrear restrições de uso do material. /
  vidgrab shows a `⚠ Not Creative Commons` warning when the video is not under a CC license,
  helping track usage restrictions on the footage.

### 🐛 Correções / Bug fixes

- `download()` agora delega para `download_batch()` — erros tratados de forma consistente
  em ambos os métodos /
  `download()` now delegates to `download_batch()` — errors handled consistently in both methods
- `_print_summary` não encerra mais o processo internamente de forma oculta /
  `_print_summary` no longer exits the process silently as a hidden side-effect
- Escopo de variável corrigido em `expand_playlists` /
  Variable scope fixed in `expand_playlists`

### 🔧 Chore

- Migração de **setuptools → Poetry** / Migration from **setuptools → Poetry**
- Adicionada licença **MIT** / Added **MIT** license

---

## [v0.1.0] — 2026-06-21

Release inicial do vidgrab. / Initial release of vidgrab.

### ✨ Funcionalidades / Features

- Download na maior qualidade disponível (streams DASH, sem re-encode) /
  Download at the highest available quality (DASH streams, no re-encode)
- Downloads paralelos via `--workers` (padrão: 3) /
  Parallel downloads via `--workers` (default: 3)
- Suporte a playlists via `--playlist` / Playlist support via `--playlist`
- Download em lote via `--batch <arquivo.txt>` / Batch download via `--batch <file.txt>`
- Skip de arquivos existentes; `--force` para re-download /
  Skip existing files; `--force` to re-download
- Limitação de resolução via `--max-height` / Resolution cap via `--max-height`
- Suporte a cookies via `--cookies` para conteúdo com restrição de idade /
  Cookie support via `--cookies` for age-restricted content
- Barra de progresso Rich por download / Rich progress bar per download
- Retry automático com backoff exponencial em rate-limits /
  Automatic retry with exponential backoff on rate-limits
- Classificação tipada de erros (vídeo indisponível, bloqueio geográfico, restrição de idade) /
  Typed error classification (unavailable video, geo-block, age restriction)
- Padrão de nome de arquivo: `{upload_date}-{titulo-slug}-{video_id}.{ext}` /
  Output filename pattern: `{upload_date}-{title-slug}-{video_id}.{ext}`
