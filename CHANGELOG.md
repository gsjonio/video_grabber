# Changelog

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
