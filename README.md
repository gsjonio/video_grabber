# vidgrab

**[ðŸ‡§ðŸ‡· PT-BR](#pt-br)** â€¢ **[ðŸ‡¬ðŸ‡§ English](#english)**

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.5.2-orange)
[![Lint](https://github.com/gsjonio/video_grabber/actions/workflows/lint.yml/badge.svg)](https://github.com/gsjonio/video_grabber/actions/workflows/lint.yml)
[![Tests](https://img.shields.io/badge/tests-120-brightgreen)](https://github.com/gsjonio/video_grabber/actions)
[![Coverage](https://codecov.io/gh/gsjonio/video_grabber/branch/main/graph/badge.svg)](https://codecov.io/gh/gsjonio/video_grabber)
[![CodeQL](https://github.com/gsjonio/video_grabber/actions/workflows/codeql.yml/badge.svg)](https://github.com/gsjonio/video_grabber/actions/workflows/codeql.yml)
![Last commit](https://img.shields.io/github/last-commit/gsjonio/video_grabber)

---

## PT-BR

**vidgrab** Ã© um CLI para baixar vÃ­deos do YouTube na **mÃ¡xima qualidade tÃ©cnica disponÃ­vel** â€” sem reencode, sem perda de qualidade. Streams de vÃ­deo e Ã¡udio separados (DASH) sÃ£o mesclados via FFmpeg em modo cÃ³pia, ideal para editing profissional e material de arquivo.

Feito para quem leva a qualidade a sÃ©rio.

### ðŸ“‹ Ãndice

- [InÃ­cio rÃ¡pido](#inÃ­cio-rÃ¡pido)

- [Como funciona](#como-funciona)

- [Funcionalidades](#funcionalidades)

- [DependÃªncias](#dependÃªncias-externas)

- [InstalaÃ§Ã£o](#instalaÃ§Ã£o)

- [Exemplos](#exemplos)

- [Config file](#config-file)

- [OpÃ§Ãµes](#referÃªncia-de-opÃ§Ãµes)

- [Troubleshooting](#troubleshooting)

- [Qualidade de cÃ³digo](#qualidade-de-cÃ³digo)

- [Contribuindo](#contribuindo)

---

### InÃ­cio rÃ¡pido

```bash
# Instalar
pip install vidgrab

# Usar
vidgrab https://youtu.be/dQw4w9WgXcQ

# Inspecionar antes de baixar
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run

# Batch + 5 workers
vidgrab --batch urls.txt --workers 5 --quiet && echo "âœ“ Done"

`  ext

---

### Como funciona

Ao contrÃ¡rio da maioria das ferramentas, vidgrab **nÃ£o recodifica**. Downloads via reencode perdem qualidade e gastam tempo processando. Veja:

```text
YouTube
  â”œâ”€ vÃ­deo stream (H.264 / VP9 / AV1)  â”€â”
  â””â”€ Ã¡udio stream (AAC / Opus)          â”€â”´â”€â†’ FFmpeg (copy mode) â”€â†’ MP4 / MKV

`  ext

Ambos os streams sÃ£o baixados no formato DASH (mÃ¡xima qualidade) e mesclados **sem recodificaÃ§Ã£o**. O resultado Ã© um arquivo pronto para ediÃ§Ã£o com qualidade intacta.

---

### Funcionalidades

| Feature | DescriÃ§Ã£o | Comando |
| --- | --- | --- |
| âš¡ **Downloads paralelos** | AtÃ© 8 vÃ­deos simultÃ¢neos | `--workers 8` |
| ðŸ” **Retry inteligente** | Backoff exponencial em rate-limits (HTTP 429) | automÃ¡tico |
| ðŸ” **Dry-run** | Veja tÃ­tulo, resoluÃ§Ã£o, tamanho antes de baixar | `--dry-run` |
| â¸ **Resume automÃ¡tico** | Retoma downloads interrompidos | automÃ¡tico |
| ðŸ“‹ **Batch download** | Arquivo `.txt` com uma URL por linha | `--batch urls.txt` |
| ðŸŽ¬ **Playlists** | Expande automaticamente todos os vÃ­deos | `--playlist` |
| ðŸ“ **Skip inteligente** | Detecta e pula arquivos jÃ¡ baixados por ID | automÃ¡tico |
| ðŸ“„ **Metadados JSON** | Sidecar com tÃ­tulo, canal, tags, data | `--write-json` |
| ðŸ”’ **ConteÃºdo restrito** | Suporte a cookies (age-gate, regiÃ£o) | `--cookies file.txt` |
| âš™ï¸ **Config file** | Defaults pessoais em `~/.config/vidgrab/config.toml` | automÃ¡tico |
| ðŸ· **Nomes previsÃ­veis** | `{data}-{slug}-{video_id}.{ext}` | automÃ¡tico |
| âš ï¸ **Aviso de licenÃ§a** | Alerta se nÃ£o Ã© Creative Commons | automÃ¡tico |
| ðŸš« **Modo quiet** | Suprime saÃ­da para scripts e pipelines | `--quiet` |
| ðŸŽ¨ **Shell completion** | Auto-complete para bash/zsh/fish | `--install-completion` |

---

### DependÃªncias externas

| Ferramenta | Para quÃª | Instalar |
| --- | --- | --- |
| **Python 3.11+** | Runtime | [python.org](https://www.python.org/downloads/) |
| **ffmpeg** | Mesclar streams (crÃ­tico) | Veja abaixo |
| **yt-dlp** | Download (automÃ¡tico) | via Poetry |
| **Deno** *(opt)* | 4K/HDR (melhor extraÃ§Ã£o) | Veja abaixo |

<details>
<summary><b>Instalando ffmpeg</b></summary>

**Windows:**

```bash
winget install ffmpeg

`  ext

**macOS:**

```bash
brew install ffmpeg

`  ext

**Linux (Debian/Ubuntu):**

```bash
sudo apt install ffmpeg

`  ext

Ou baixe em [ffmpeg.org/download.html](https://ffmpeg.org/download.html) e adicione ao `PATH`.

Verifique: `ffmpeg -version`

</details>

<details>
<summary><b>Instalando Deno (recomendado para 4K/HDR)</b></summary>

Sem Deno, yt-dlp usa fallback que pode perder formatos 4K. Com Deno, extraÃ§Ã£o Ã© completa.

**Windows:**

```bash
winget install DenoLand.Deno

`  ext

**macOS:**

```bash
brew install deno

`  ext

**Linux:**

```bash
curl -fsSL https://deno.land/install.sh | sh

`  ext

Verifique: `deno --version`

</details>

---

### InstalaÃ§Ã£o

<details>
<summary><b>Via pip (recomendado)</b></summary>

```bash
pip install vidgrab

`  ext

Depois, instale ffmpeg conforme acima.

</details>

<details>
<summary><b>Via Poetry (desenvolvimento)</b></summary>

```bash
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber
poetry install
poetry run vidgrab --help

`  ext

</details>

<details>
<summary><b>Via pipx (isolado)</b></summary>

```bash
pipx install vidgrab

`  ext

Ideal se vocÃª quer isolamento de dependÃªncias.

</details>

---

### Exemplos

**BÃ¡sico â€” um vÃ­deo:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ
# Salva em: ~/Downloads/2009-10-25-never-gonna-give-you-up-dQw4w9WgXcQ.mp4

`  ext

**Inspecionar sem baixar:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run
# Mostra: tÃ­tulo, resoluÃ§Ã£o, tamanho estimado, container

`  ext

**Limitar resoluÃ§Ã£o:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080
# Baixa 1080p se disponÃ­vel, caso contrÃ¡rio a mÃ¡xima abaixo de 1080p

`  ext

**Salvar em outro local:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --output ~/Videos/archive

`  ext

**Playlist inteira:**

```bash
vidgrab "https://youtube.com/playlist?list=PLxxxx" --playlist
# Expande todos os vÃ­deos e baixa em paralelo

`  ext

**MÃºltiplos vÃ­deos em paralelo:**

```bash
vidgrab https://youtu.be/vid1 https://youtu.be/vid2 https://youtu.be/vid3 --workers 3

`  ext

**Batch com arquivo `.txt`:**

```bash
# urls.txt
# Meus vÃ­deos favoritos
https://youtu.be/vid1
https://youtu.be/vid2

vidgrab --batch urls.txt --workers 5 --quiet
# --quiet suprime output (ideal para cron jobs)

`  ext

**ForÃ§ar re-download:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --force
# Por padrÃ£o, pula se o arquivo jÃ¡ existe

`  ext

**ConteÃºdo com age-gate:**

```bash
# Obtenha cookies do navegador via extensÃ£o:
# - https://github.com/yt-dlp/yt-dlp/wiki/Download-using-cookies
vidgrab https://youtu.be/restricted_video --cookies ~/Downloads/cookies.txt

`  ext

**Com metadados JSON:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --write-json
# Cria: 2009-10-25-never-gonna-give-you-up-dQw4w9WgXcQ.json

`  ext

**Auto-complete no shell:**

```bash
vidgrab --install-completion
# Depois: reabra o terminal e use TAB

`  ext

---

### Config file

Salve defaults pessoais em `~/.config/vidgrab/config.toml`:

```toml
# DiretÃ³rio padrÃ£o de saÃ­da
output = "~/Videos/raw"

# Downloads paralelos
workers = 5

# Limitar resoluÃ§Ã£o
max_height = 1080

# Escrever metadados JSON automaticamente
write_json = true

# Arquivo de cookies (para conteÃºdo restrito)
cookies = "~/Downloads/cookies.txt"

`  ext

**PrecedÃªncia:** CLI args > config file > cÃ³digo defaults

Exemplo:

```bash
# Sem --output, usa config file
vidgrab https://youtu.be/x
# ~/Videos/raw/...

# Com --output, sobrescreve config
vidgrab https://youtu.be/x --output ~/tmp
# ~/tmp/...

`  ext

---

### NomeaÃ§Ã£o de arquivos

`  ext

{upload_date}-{tÃ­tulo-slug}-{video_id}.{ext}

`  ext

**Exemplo:**

`  ext

20091025-never-gonna-give-you-up-dQw4w9WgXcQ.mp4
20091025-never-gonna-give-you-up-dQw4w9WgXcQ.json  (se --write-json)

`  ext

**Vantagens:**

- âœ… PrevisÃ­vel e reproducÃ­vel

- âœ… OrdenÃ¡vel por data e nome

- âœ… ID do vÃ­deo no fim para deduplicaÃ§Ã£o

---

### Container e codecs

| Streams | Container | Reencode? |
| --- | --- | --- |
| H.264 + AAC | MP4 | âŒ CÃ³pia |
| VP9 + Opus | MKV | âŒ CÃ³pia |
| AV1 + Opus | MKV | âŒ CÃ³pia |

**O objetivo Ã© sempre: cÃ³pia, nunca recodificaÃ§Ã£o.**

---

### ReferÃªncia de opÃ§Ãµes

`  ext

Uso:  vidgrab [OPÃ‡Ã•ES] [URLs]...

Argumentos:
  [URLs]...                  Uma ou mais URLs do YouTube

OpÃ§Ãµes:
  -b, --batch FILE           Arquivo .txt com uma URL por linha
  -o, --output DIR           DiretÃ³rio de saÃ­da (padrÃ£o: ~/Downloads)
  --max-height INT           Limitar resoluÃ§Ã£o vertical (ex.: 1080)
  --playlist                 Tratar URLs como playlists
  -f, --force                Re-download mesmo se existe
  --cookies FILE             Arquivo de cookies (formato Netscape)
  --write-json               Salvar metadados em .json
  -w, --workers INT          Parallelismo (padrÃ£o: 3, mÃ¡x: 8)
  --dry-run                  Mostrar o que seria baixado
  -q, --quiet                Suprimir output (exceto erros)
  -V, --version              Exibir versÃ£o
  --install-completion       Auto-complete (bash/zsh/fish)
  --help                     Exibir ajuda

`  ext

---

### Troubleshooting

**âŒ "ffmpeg not found in PATH"**

```bash
# Instale ffmpeg (veja dependÃªncias acima)
ffmpeg -version  # Verifique se estÃ¡ acessÃ­vel

`  ext

**âŒ "Video unavailable"**

- VÃ­deo foi deletado ou Ã© privado

- RegiÃ£o bloqueada â†’ tente `--cookies`

- Rate-limited â†’ vidgrab faz retry automÃ¡tico, tente novamente

**âŒ "Age restricted"**

```bash
# FaÃ§a login em uma conta, exporte cookies, e use:
vidgrab URL --cookies ~/cookies.txt

`  ext

**âŒ "Geo-blocked"**

- VÃ­deo sÃ³ estÃ¡ disponÃ­vel em certas regiÃµes

- SoluÃ§Ã£o: VPN + cookies de uma conta naquela regiÃ£o

**âŒ Arquivo incompleto apÃ³s interrupÃ§Ã£o**

```bash
# vidgrab detecta e retoma automaticamente na prÃ³xima tentativa
vidgrab URL  # Retoma de onde parou

`  ext

**âŒ Arquivo jÃ¡ existe, quer re-download**

```bash
vidgrab URL --force

`  ext

---

### Qualidade de cÃ³digo

O projeto segue prÃ¡ticas de cÃ³digo maduro:

| Ferramenta | FunÃ§Ã£o |
| --- | --- |
| **Ruff** | Linter + formatter (E, W, F, I, N, UP, B, C4, SIM) |
| **Pylint** | AnÃ¡lise estÃ¡tica avanÃ§ada |
| **Mypy** (strict) | Type checking completo com `dict[str, Any]` em fronteiras |
| **pytest** (120 testes) | Cobertura 92% (`downloader.py` 90%, `cli.py` 93%) |
| **pre-commit** | Ruff, Pylint, Mypy, Markdownlint em cada commit |
| **GitHub Actions** | CI/CD: lint, tests, CodeQL, Dependabot, release |
| **codecov** | RelatÃ³rio de cobertura contÃ­nuo |

**Commitmente:**

- Semantic versioning (v0.1.0 â†’ v0.5.2)

- Conventional commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`)

- CHANGELOG bilÃ­ngue (PT-BR / EN)

- Branch ruleset: linear history, auto-review, required checks

<details>
<summary><b>Estrutura do projeto</b></summary>

`  ext

vidgrab/
â”œâ”€â”€ __init__.py         # Version
â”œâ”€â”€ cli.py              # Typer CLI, argument parsing
â”œâ”€â”€ downloader.py       # Core: parallel, retry, error classification
â”œâ”€â”€ models.py           # VideoMetadata, DownloadResult (dataclasses)
â”œâ”€â”€ config.py           # Config file loader (~/.config/vidgrab/config.toml)
â””â”€â”€ exceptions.py       # Exception hierarchy (VidGrabError, ...)

tests/
â”œâ”€â”€ test_exceptions.py           # 21 exception tests
â”œâ”€â”€ test_downloader_helpers.py   # 17 downloader helper tests
â”œâ”€â”€ test_downloader_download.py  # 12 download orchestration tests
â”œâ”€â”€ test_cli_handler.py          # 21 CLI handler tests
â”œâ”€â”€ test_rate_limit.py           # 11 rate-limit / retry tests
â””â”€â”€ test_main.py                 # 38 model / config tests

.github/
â”œâ”€â”€ workflows/
â”‚   â”œâ”€â”€ lint.yml        # Ruff, Pylint, Mypy, pytest, codecov, markdownlint
â”‚   â”œâ”€â”€ release.yml     # Auto-bump version + git-cliff CHANGELOG
â”‚   â”œâ”€â”€ codeql.yml      # Security scanning
â”‚   â””â”€â”€ dependabot.yml  # Auto-updates

Docs:
â”œâ”€â”€ README.md           # You are here
â”œâ”€â”€ CHANGELOG.md        # v0.1.0 â€” v0.5.2 (bilÃ­ngue)
â”œâ”€â”€ CONTRIBUTING.md     # Setup, commit convention, PR process
â”œâ”€â”€ SECURITY.md         # Vulnerability disclosure policy
â””â”€â”€ DISCUSSIONS_GUIDE.md # GitHub Discussions setup

`  ext

</details>

---

### Contribuindo

Adoramos contribuiÃ§Ãµes! Veja [CONTRIBUTING.md](CONTRIBUTING.md).

**TL;DR:**

```bash
# 1. Fork + clone
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber

# 2. Setup
poetry install
pre-commit install

# 3. Teste + code quality
poetry run pytest          # 120 testes
poetry run ruff check .    # Lint
poetry run pylint vidgrab  # Static analysis
poetry run mypy vidgrab    # Type check (strict)

# 4. Commit
git commit -m "feat: add cool feature"
git push origin feat/cool-feature

# 5. PR
# â†’ PR â†’ squash-merge â†’ release tag

`  ext

---

### Perguntas?

Use [GitHub Discussions](https://github.com/gsjonio/video_grabber/discussions) para:

- â“ DÃºvidas sobre uso

- ðŸ’¡ Ideias de features

- ðŸ“¢ AnÃºncios de releases

---

---

## English

**vidgrab** is a CLI to download YouTube videos at the **highest technically available quality** â€” no re-encoding, no quality loss. Separate DASH video and audio streams are muxed via FFmpeg in copy mode, perfect for professional editing and raw footage archiving.

Built for those who care about quality.

### ðŸ“‹ Table of Contents

- [Quick start](#quick-start)

- [How it works](#how-it-works-1)

- [Features](#features-1)

- [Dependencies](#external-dependencies-1)

- [Installation](#installation-1)

- [Examples](#examples-1)

- [Config file](#config-file-1)

- [Options](#option-reference)

- [Troubleshooting](#troubleshooting-1)

- [Code quality](#code-quality-1)

- [Contributing](#contributing-1)

---

### Quick start

```bash
# Install
pip install vidgrab

# Use
vidgrab https://youtu.be/dQw4w9WgXcQ

# Inspect before downloading
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run

# Batch + 5 workers
vidgrab --batch urls.txt --workers 5 --quiet && echo "âœ“ Done"

`  ext

---

### How it works

Unlike most tools, vidgrab **does not re-encode**. Re-encoded downloads lose quality and waste processing time. Here's the difference:

```text
YouTube
  â”œâ”€ video stream (H.264 / VP9 / AV1)  â”€â”
  â””â”€ audio stream (AAC / Opus)          â”€â”´â”€â†’ FFmpeg (copy mode) â”€â†’ MP4 / MKV

`  ext

Both streams are downloaded in DASH format (highest quality) and muxed **without re-encoding**. Result: a file ready for editing with quality intact.

---

### Features

| Feature | Description | Command |
| --- | --- | --- |
| âš¡ **Parallel downloads** | Up to 8 videos simultaneous | `--workers 8` |
| ðŸ” **Smart retry** | Exponential backoff on rate-limits (HTTP 429) | automatic |
| ðŸ” **Dry-run** | See title, resolution, size before downloading | `--dry-run` |
| â¸ **Auto-resume** | Resumes interrupted downloads | automatic |
| ðŸ“‹ **Batch download** | `.txt` file with one URL per line | `--batch urls.txt` |
| ðŸŽ¬ **Playlists** | Auto-expands all videos in a playlist | `--playlist` |
| ðŸ“ **Smart skip** | Detects and skips already-downloaded by ID | automatic |
| ðŸ“„ **JSON metadata** | Sidecar with title, channel, tags, date | `--write-json` |
| ðŸ”’ **Restricted content** | Cookie support (age-gate, region) | `--cookies file.txt` |
| âš™ï¸ **Config file** | Personal defaults in `~/.config/vidgrab/config.toml` | automatic |
| ðŸ· **Predictable names** | `{date}-{slug}-{video_id}.{ext}` | automatic |
| âš ï¸ **License alert** | Warns if not Creative Commons | automatic |
| ðŸš« **Quiet mode** | Suppress output for scripts/pipelines | `--quiet` |
| ðŸŽ¨ **Shell completion** | Auto-complete for bash/zsh/fish | `--install-completion` |

---

### External dependencies

| Tool | For | Install |
| --- | --- | --- |
| **Python 3.11+** | Runtime | [python.org](https://www.python.org/downloads/) |
| **ffmpeg** | Mux streams (critical) | See below |
| **yt-dlp** | Download (automatic) | via Poetry |
| **Deno** *(opt)* | 4K/HDR (better extraction) | See below |

<details>
<summary><b>Installing ffmpeg</b></summary>

**Windows:**

```bash
winget install ffmpeg

`  ext

**macOS:**

```bash
brew install ffmpeg

`  ext

**Linux (Debian/Ubuntu):**

```bash
sudo apt install ffmpeg

`  ext

Or download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add to `PATH`.

Verify: `ffmpeg -version`

</details>

<details>
<summary><b>Installing Deno (recommended for 4K/HDR)</b></summary>

Without Deno, yt-dlp uses a fallback that may miss 4K formats. With Deno, extraction is complete.

**Windows:**

```bash
winget install DenoLand.Deno

`  ext

**macOS:**

```bash
brew install deno

`  ext

**Linux:**

```bash
curl -fsSL https://deno.land/install.sh | sh

`  ext

Verify: `deno --version`

</details>

---

### Installation

<details>
<summary><b>Via pip (recommended)</b></summary>

```bash
pip install vidgrab

`  ext

Then install ffmpeg as shown above.

</details>

<details>
<summary><b>Via Poetry (development)</b></summary>

```bash
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber
poetry install
poetry run vidgrab --help

`  ext

</details>

<details>
<summary><b>Via pipx (isolated)</b></summary>

```bash
pipx install vidgrab

`  ext

Great if you want dependency isolation.

</details>

---

### Examples

**Basic â€” single video:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ
# Saves to: ~/Downloads/2009-10-25-never-gonna-give-you-up-dQw4w9WgXcQ.mp4

`  ext

**Inspect without downloading:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run
# Shows: title, resolution, estimated size, container

`  ext

**Limit resolution:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080
# Downloads 1080p if available, otherwise highest below 1080p

`  ext

**Save to custom location:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --output ~/Videos/archive

`  ext

**Entire playlist:**

```bash
vidgrab "https://youtube.com/playlist?list=PLxxxx" --playlist
# Expands all videos and downloads in parallel

`  ext

**Multiple videos in parallel:**

```bash
vidgrab https://youtu.be/vid1 https://youtu.be/vid2 https://youtu.be/vid3 --workers 3

`  ext

**Batch from `.txt` file:**

```bash
# urls.txt
# My favorite videos
https://youtu.be/vid1
https://youtu.be/vid2

vidgrab --batch urls.txt --workers 5 --quiet
# --quiet suppresses output (ideal for cron jobs)

`  ext

**Force re-download:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --force
# By default, skips if file already exists

`  ext

**Age-restricted content:**

```bash
# Get cookies from browser via extension:
# - https://github.com/yt-dlp/yt-dlp/wiki/Download-using-cookies
vidgrab https://youtu.be/restricted_video --cookies ~/Downloads/cookies.txt

`  ext

**With JSON metadata:**

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --write-json
# Creates: 2009-10-25-never-gonna-give-you-up-dQw4w9WgXcQ.json

`  ext

**Shell auto-complete:**

```bash
vidgrab --install-completion
# Then: reopen terminal and press TAB

`  ext

---

### Config file

Save personal defaults in `~/.config/vidgrab/config.toml`:

```toml
# Default output directory
output = "~/Videos/raw"

# Parallel downloads
workers = 5

# Limit resolution
max_height = 1080

# Auto-write JSON metadata
write_json = true

# Cookies file for restricted content
cookies = "~/Downloads/cookies.txt"

`  ext

**Precedence:** CLI args > config file > code defaults

Example:

```bash
# Without --output, uses config
vidgrab https://youtu.be/x
# ~/Videos/raw/...

# With --output, overrides config
vidgrab https://youtu.be/x --output ~/tmp
# ~/tmp/...

`  ext

---

### Filename format

`  ext

{upload_date}-{title-slug}-{video_id}.{ext}

`  ext

**Example:**

`  ext

20091025-never-gonna-give-you-up-dQw4w9WgXcQ.mp4
20091025-never-gonna-give-you-up-dQw4w9WgXcQ.json  (if --write-json)

`  ext

**Advantages:**

- âœ… Predictable and reproducible

- âœ… Sortable by date and name

- âœ… Video ID at end for deduplication

---

### Container and codecs

| Streams | Container | Re-encode? |
| --- | --- | --- |
| H.264 + AAC | MP4 | âŒ Copy |
| VP9 + Opus | MKV | âŒ Copy |
| AV1 + Opus | MKV | âŒ Copy |

**Always copy, never re-encode.**

---

### Option reference

`  ext

Usage:  vidgrab [OPTIONS] [URLs]...

Arguments:
  [URLs]...                  One or more YouTube URLs

Options:
  -b, --batch FILE           .txt file with one URL per line
  -o, --output DIR           Output directory (default: ~/Downloads)
  --max-height INT           Limit resolution height (e.g., 1080)
  --playlist                 Treat URLs as playlists
  -f, --force                Re-download even if exists
  --cookies FILE             Cookies file (Netscape format)
  --write-json               Save metadata as .json
  -w, --workers INT          Parallelism (default: 3, max: 8)
  --dry-run                  Show what would be downloaded
  -q, --quiet                Suppress output (except errors)
  -V, --version              Show version
  --install-completion       Shell auto-complete (bash/zsh/fish)
  --help                     Show help

`  ext

---

### Troubleshooting

**âŒ "ffmpeg not found in PATH"**

```bash
# Install ffmpeg (see dependencies above)
ffmpeg -version  # Verify it's accessible

`  ext

**âŒ "Video unavailable"**

- Video was deleted or is private

- Region blocked â†’ try `--cookies`

- Rate-limited â†’ vidgrab retries automatically, try again

**âŒ "Age restricted"**

```bash
# Sign in to an account, export cookies, then:
vidgrab URL --cookies ~/cookies.txt

`  ext

**âŒ "Geo-blocked"**

- Video only available in certain regions

- Solution: VPN + cookies from an account in that region

**âŒ Incomplete file after interruption**

```bash
# vidgrab detects and resumes automatically on retry
vidgrab URL  # Resumes from where it stopped

`  ext

**âŒ File exists, want to re-download**

```bash
vidgrab URL --force

`  ext

---

### Code quality

The project follows mature code practices:

| Tool | Function |
| --- | --- |
| **Ruff** | Linter + formatter (E, W, F, I, N, UP, B, C4, SIM) |
| **Pylint** | Advanced static analysis |
| **Mypy** (strict) | Full type checking with `dict[str, Any]` at boundaries |
| **pytest** (120 tests) | 92% coverage (`downloader.py` 90%, `cli.py` 93%) |
| **pre-commit** | Ruff, Pylint, Mypy, Markdownlint on every commit |
| **GitHub Actions** | CI/CD: lint, tests, CodeQL, Dependabot, release |
| **codecov** | Continuous coverage reporting |

**Commitment:**

- Semantic versioning (v0.1.0 â†’ v0.5.2)

- Conventional commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`)

- Bilingual CHANGELOG (PT-BR / EN)

- Branch ruleset: linear history, auto-review, required checks

---

### Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

**TL;DR:**

```bash
# 1. Fork + clone
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber

# 2. Setup
poetry install
pre-commit install

# 3. Test + quality
poetry run pytest          # 120 tests
poetry run ruff check .    # Lint
poetry run pylint vidgrab  # Static analysis
poetry run mypy vidgrab    # Type check (strict)

# 4. Commit
git commit -m "feat: add cool feature"
git push origin feat/cool-feature

# 5. PR
# â†’ PR â†’ squash-merge â†’ release tag

`  ext

---

### Questions?

Use [GitHub Discussions](https://github.com/gsjonio/video_grabber/discussions) for:

- â“ Usage questions

- ðŸ’¡ Feature ideas

- ðŸ“¢ Release announcements



