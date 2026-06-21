# vidgrab

**PT-BR** | [EN](#english)

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.4.0-orange)
[![Lint](https://github.com/gsjonio/video_grabber/actions/workflows/lint.yml/badge.svg)](https://github.com/gsjonio/video_grabber/actions/workflows/lint.yml)
[![CodeQL](https://github.com/gsjonio/video_grabber/actions/workflows/codeql.yml/badge.svg)](https://github.com/gsjonio/video_grabber/actions/workflows/codeql.yml)
[![Coverage](https://codecov.io/gh/gsjonio/video_grabber/branch/main/graph/badge.svg)](https://codecov.io/gh/gsjonio/video_grabber)
![Last commit](https://img.shields.io/github/last-commit/gsjonio/video_grabber)

CLI para baixar vídeos do YouTube na **maior qualidade técnica disponível** — streams de vídeo e áudio separados (DASH), mesclados via FFmpeg sem nenhum reencode. Feito para quem usa vídeo como material bruto em edição.

---

## PT-BR

- [Como funciona](#como-funciona)
- [Funcionalidades](#funcionalidades)
- [Dependências](#dependências-externas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Config file](#config-file)
- [Opções](#referência-de-opções)
- [Qualidade de código](#qualidade-de-código)

---

### Como funciona

A maioria das ferramentas de download aplica reencode para juntar vídeo e áudio — o que degrada a qualidade e desperdiça tempo. O vidgrab faz diferente:

```text
YouTube  →  stream de vídeo (H.264 / VP9 / AV1)  ─┐
         →  stream de áudio (AAC / Opus)           ─┴→  FFmpeg mux  →  arquivo final
```

Os dois streams são baixados separadamente no formato DASH (maior qualidade disponível) e mesclados em **modo cópia** — sem recodificação, sem perda de qualidade.

---

### Funcionalidades

| | Funcionalidade | Detalhe |
| --- | --- | --- |
| ⚡ | **Downloads paralelos** | Até 8 simultâneos via `--workers` |
| 🔁 | **Retry inteligente** | Backoff exponencial em rate-limits (até 5 tentativas) |
| 🔍 | **Dry run** | Veja título, resolução e tamanho antes de baixar |
| ⏸ | **Resume automático** | Downloads interrompidos são retomados de onde pararam |
| 📋 | **Batch download** | Arquivo `.txt` com uma URL por linha |
| 🎬 | **Playlists** | Expande e baixa todos os vídeos de uma playlist |
| 📁 | **Skip inteligente** | Detecta arquivo existente pelo ID e pula automaticamente |
| 📄 | **Metadados JSON** | Sidecar `.json` com título, canal, data, tags e mais |
| 🔒 | **Conteúdo restrito** | Suporte a cookies (Netscape) para vídeos com age-gate |
| ⚙️ | **Config file** | Defaults pessoais em `~/.config/vidgrab/config.toml` |
| 🏷 | **Nomes previsíveis** | `{data}-{slug}-{video_id}.{ext}` em todo download |
| ⚠️ | **Aviso de licença** | Alerta quando o vídeo não é Creative Commons |

---

### Dependências externas

| Ferramenta | Para quê | Como instalar |
| --- | --- | --- |
| **Python 3.11+** | Runtime | [python.org](https://www.python.org/downloads/) |
| **ffmpeg** | Mesclar streams de vídeo e áudio | Veja abaixo |
| **yt-dlp** | Engine de download | Instalado automaticamente via Poetry |
| **Deno** *(opcional)* | Acesso a todos os formatos do YouTube, incluindo 4K/HDR | Veja abaixo |

<details>
<summary>Instalando o ffmpeg</summary>

#### Windows

```bash
winget install ffmpeg
```

#### macOS

```bash
brew install ffmpeg
```

#### Linux (Debian/Ubuntu)

```bash
sudo apt install ffmpeg
```

Ou baixe o executável em <https://ffmpeg.org/download.html> e adicione ao `PATH`.

</details>

<details>
<summary>Instalando o Deno (recomendado para 4K/HDR)</summary>

Sem o Deno, o yt-dlp usa um método alternativo que pode não enxergar todos os formatos disponíveis. Com o Deno instalado, a extração é completa.

#### Windows

```bash
winget install DenoLand.Deno
```

#### macOS

```bash
brew install deno
```

#### Linux

```bash
curl -fsSL https://deno.land/install.sh | sh
```

</details>

---

### Instalação

```bash
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber
poetry install
```

---

### Uso

```bash
# Vídeo único — qualidade máxima
vidgrab https://youtu.be/dQw4w9WgXcQ

# Inspecionar antes de baixar (dry run)
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run

# Limitar a 1080p
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080

# Salvar em diretório específico
vidgrab https://youtu.be/dQw4w9WgXcQ --output ~/Videos/raw

# Baixar playlist inteira
vidgrab "https://youtube.com/playlist?list=PLxxxx" --playlist

# Múltiplas URLs de um arquivo .txt com 5 workers
vidgrab --batch urls.txt --workers 5

# Forçar re-download mesmo se o arquivo já existir
vidgrab https://youtu.be/dQw4w9WgXcQ --force

# Conteúdo com restrição de idade
vidgrab https://youtu.be/dQw4w9WgXcQ --cookies ~/cookies.txt

# Salvar metadados em JSON
vidgrab https://youtu.be/dQw4w9WgXcQ --write-json
```

#### Arquivo `--batch`

Uma URL por linha. Linhas com `#` são ignoradas.

```text
# Meus vídeos
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/VIDEO_ID_2
```

---

### Config file

Salve seus defaults pessoais em `~/.config/vidgrab/config.toml` para não precisar repetir as flags:

```toml
output     = "~/Videos/raw"
workers    = 5
max_height = 1080
```

Flags passadas na linha de comando sempre têm prioridade sobre o config file.

---

### Nomeação dos arquivos

```text
{data_upload}-{slug-do-titulo}-{video_id}.{ext}
```

Exemplo: `20240315-never-gonna-give-you-up-dQw4w9WgXcQ.mp4`

Com `--write-json`, um sidecar `.json` é criado ao lado do vídeo:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "channel": "Rick Astley",
  "upload_date": "2009-10-25",
  "duration_seconds": 212,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "description": "...",
  "tags": ["pop", "80s"]
}
```

---

### Container e qualidade

| Streams disponíveis | Container de saída |
| --- | --- |
| H.264 + AAC | `mp4` (sem reencode) |
| VP9 / AV1 + Opus | `mkv` (sem reencode) |

O objetivo é **nunca recodificar** — apenas mesclar os streams.

---

### Referência de opções

| Opção | Atalho | Descrição |
| --- | --- | --- |
| `[URLS]...` | | Uma ou mais URLs do YouTube |
| `--batch FILE` | `-b` | Arquivo `.txt` com uma URL por linha |
| `--output DIR` | `-o` | Diretório de saída (padrão: `~/Downloads`) |
| `--max-height INT` | | Limitar resolução vertical (ex.: `1080`) |
| `--playlist` | | Tratar URLs como playlists |
| `--force` | `-f` | Re-download mesmo se o arquivo já existe |
| `--cookies FILE` | | Arquivo de cookies (formato Netscape) |
| `--write-json` | | Salvar metadados em `.json` ao lado do vídeo |
| `--workers INT` | `-w` | Downloads paralelos (padrão: `3`, máx: `8`) |
| `--dry-run` | | Mostrar o que seria baixado, sem baixar |
| `--quiet` | `-q` | Suprimir toda saída exceto erros (útil para scripts) |
| `--version` | `-V` | Exibir versão |
| `--install-completion` | | Instalar autocomplete no shell atual |
| `--help` | | Exibir ajuda |

---

### Qualidade de código

O projeto usa uma stack completa de qualidade, integrada ao CI e aos pre-commit hooks:

| Ferramenta | Função |
| --- | --- |
| **Ruff** | Linter + formatador (9 categorias de regras) |
| **Pylint** | Análise estática avançada |
| **Mypy** (strict) | Type checking completo — `dict[str, Any]` em todas as fronteiras com yt-dlp |
| **pytest + pytest-cov** | 38 testes unitários, cobertura reportada ao Codecov |
| **pre-commit** | Ruff, Pylint, Mypy e Markdownlint rodando antes de cada commit |
| **GitHub Actions** | Lint, testes, CodeQL e release automática por tag |
| **Dependabot** | Atualizações semanais de dependências Python e Actions |

<details>
<summary>Estrutura do projeto</summary>

```text
vidgrab/
├── cli.py          # Interface Typer — parsing de argumentos e orquestração
├── downloader.py   # Lógica core — parallelismo, retry, classificação de erros
├── models.py       # VideoMetadata e DownloadResult como dataclasses tipadas
├── exceptions.py   # Hierarquia de exceções (geo-block, age-gate, unavailable…)
└── config.py       # Loader de ~/.config/vidgrab/config.toml via tomllib

tests/
├── test_downloader.py  # _slugify, _classify_error, _format_selector, DownloadConfig
├── test_models.py      # VideoMetadata serialization / deserialization
├── test_cli.py         # _collect_urls com batch e URLs posicionais
└── test_config.py      # config.load com TOML válido, inválido e ausente
```

</details>

---

## English

CLI to download YouTube videos at the **highest technically available quality** — separate DASH video and audio streams, muxed via FFmpeg with no re-encoding. Built for raw footage in video editing workflows.

- [How it works](#how-it-works)
- [Features](#features)
- [Dependencies](#external-dependencies)
- [Installation](#installation)
- [Usage](#usage-1)
- [Config file](#config-file-1)
- [Options](#option-reference)
- [Code quality](#code-quality)

---

### How it works

Most download tools re-encode to merge video and audio — degrading quality and wasting time. vidgrab does it differently:

```text
YouTube  →  video stream (H.264 / VP9 / AV1)  ─┐
         →  audio stream (AAC / Opus)           ─┴→  FFmpeg mux  →  final file
```

Both streams are downloaded separately in DASH format (highest quality available) and muxed in **copy mode** — no transcoding, no quality loss.

---

### Features

| | Feature | Detail |
| --- | --- | --- |
| ⚡ | **Parallel downloads** | Up to 8 simultaneous via `--workers` |
| 🔁 | **Smart retry** | Exponential backoff on rate-limits (up to 5 attempts) |
| 🔍 | **Dry run** | Preview title, resolution and size before downloading |
| ⏸ | **Auto resume** | Interrupted downloads pick up where they left off |
| 📋 | **Batch download** | `.txt` file with one URL per line |
| 🎬 | **Playlists** | Expands and downloads every video in a playlist |
| 📁 | **Smart skip** | Detects existing file by video ID and skips automatically |
| 📄 | **JSON metadata** | Sidecar `.json` with title, channel, date, tags and more |
| 🔒 | **Restricted content** | Cookie support (Netscape format) for age-gated videos |
| ⚙️ | **Config file** | Personal defaults at `~/.config/vidgrab/config.toml` |
| 🏷 | **Predictable names** | `{date}-{slug}-{video_id}.{ext}` on every download |
| ⚠️ | **License warning** | Alerts when a video is not under a Creative Commons license |

---

### External dependencies

| Tool | Purpose | How to install |
| --- | --- | --- |
| **Python 3.11+** | Runtime | [python.org](https://www.python.org/downloads/) |
| **ffmpeg** | Merge video + audio streams | See below |
| **yt-dlp** | Download engine | Installed automatically via Poetry |
| **Deno** *(optional)* | Access all YouTube formats including 4K/HDR | See below |

<details>
<summary>Installing ffmpeg</summary>

#### Windows

```bash
winget install ffmpeg
```

#### macOS

```bash
brew install ffmpeg
```

#### Linux (Debian/Ubuntu)

```bash
sudo apt install ffmpeg
```

Or grab the binary from <https://ffmpeg.org/download.html> and add it to your `PATH`.

</details>

<details>
<summary>Installing Deno (recommended for 4K/HDR)</summary>

Without Deno, yt-dlp falls back to an alternative extraction method that may not expose all available formats. With Deno, extraction is complete.

#### Windows

```bash
winget install DenoLand.Deno
```

#### macOS

```bash
brew install deno
```

#### Linux

```bash
curl -fsSL https://deno.land/install.sh | sh
```

</details>

---

### Installation

```bash
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber
poetry install
```

---

### Usage

```bash
# Single video — maximum quality
vidgrab https://youtu.be/dQw4w9WgXcQ

# Inspect before downloading (dry run)
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run

# Cap at 1080p
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080

# Save to a specific directory
vidgrab https://youtu.be/dQw4w9WgXcQ --output ~/Videos/raw

# Download an entire playlist
vidgrab "https://youtube.com/playlist?list=PLxxxx" --playlist

# Download from a .txt file with 5 parallel workers
vidgrab --batch urls.txt --workers 5

# Force re-download even if the file already exists
vidgrab https://youtu.be/dQw4w9WgXcQ --force

# Age-restricted content
vidgrab https://youtu.be/dQw4w9WgXcQ --cookies ~/cookies.txt

# Save metadata as JSON
vidgrab https://youtu.be/dQw4w9WgXcQ --write-json
```

#### `--batch` file format

One URL per line. Lines starting with `#` are ignored.

```text
# My videos
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/VIDEO_ID_2
```

---

### Config file

Save your personal defaults at `~/.config/vidgrab/config.toml` to avoid repeating flags:

```toml
output     = "~/Videos/raw"
workers    = 5
max_height = 1080
```

Flags passed on the command line always take precedence over the config file.

---

### Output filename pattern

```text
{upload_date}-{title-slug}-{video_id}.{ext}
```

Example: `20240315-never-gonna-give-you-up-dQw4w9WgXcQ.mp4`

With `--write-json`, a sidecar `.json` is saved next to each video:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "channel": "Rick Astley",
  "upload_date": "2009-10-25",
  "duration_seconds": 212,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "description": "...",
  "tags": ["pop", "80s"]
}
```

---

### Container and quality

| Available streams | Output container |
| --- | --- |
| H.264 + AAC | `mp4` (no re-encode) |
| VP9 / AV1 + Opus | `mkv` (no re-encode) |

The goal is to **never re-encode** — only mux the streams.

---

### Option reference

| Option | Short | Description |
| --- | --- | --- |
| `[URLS]...` | | One or more YouTube URLs |
| `--batch FILE` | `-b` | `.txt` file with one URL per line |
| `--output DIR` | `-o` | Output directory (default: `~/Downloads`) |
| `--max-height INT` | | Cap vertical resolution (e.g. `1080`) |
| `--playlist` | | Treat URLs as playlists |
| `--force` | `-f` | Re-download even if the file already exists |
| `--cookies FILE` | | Cookies file (Netscape format) |
| `--write-json` | | Save metadata as a `.json` sidecar next to the video |
| `--workers INT` | `-w` | Parallel downloads (default: `3`, max: `8`) |
| `--dry-run` | | Show what would be downloaded without downloading |
| `--quiet` | `-q` | Suppress all output except errors (useful for scripting) |
| `--version` | `-V` | Show version and exit |
| `--install-completion` | | Install shell autocomplete for the current shell |
| `--help` | | Show help |

---

### Code quality

The project uses a full quality stack, integrated into CI and pre-commit hooks:

| Tool | Role |
| --- | --- |
| **Ruff** | Linter + formatter (9 rule categories) |
| **Pylint** | Advanced static analysis |
| **Mypy** (strict) | Full type checking — `dict[str, Any]` at every yt-dlp boundary |
| **pytest + pytest-cov** | 38 unit tests, coverage reported to Codecov |
| **pre-commit** | Ruff, Pylint, Mypy and Markdownlint run before every commit |
| **GitHub Actions** | Lint, tests, CodeQL and automatic release on tag push |
| **Dependabot** | Weekly updates for Python deps and Actions |

<details>
<summary>Project structure</summary>

```text
vidgrab/
├── cli.py          # Typer interface — argument parsing and orchestration
├── downloader.py   # Core logic — parallelism, retry, typed error classification
├── models.py       # VideoMetadata and DownloadResult as typed dataclasses
├── exceptions.py   # Exception hierarchy (geo-block, age-gate, unavailable…)
└── config.py       # ~/.config/vidgrab/config.toml loader via tomllib

tests/
├── test_downloader.py  # _slugify, _classify_error, _format_selector, DownloadConfig
├── test_models.py      # VideoMetadata serialization / deserialization
├── test_cli.py         # _collect_urls with batch and positional URLs
└── test_config.py      # config.load with valid, invalid and missing TOML
```

</details>
