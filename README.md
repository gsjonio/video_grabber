# Vidgrab

**PT-BR** | [EN](#english)

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.2.0-orange)
[![Lint](https://github.com/gsjonio/video_grabber/actions/workflows/lint.yml/badge.svg)](https://github.com/gsjonio/video_grabber/actions/workflows/lint.yml)
[![CodeQL](https://github.com/gsjonio/video_grabber/actions/workflows/codeql.yml/badge.svg)](https://github.com/gsjonio/video_grabber/actions/workflows/codeql.yml)
![Last commit](https://img.shields.io/github/last-commit/gsjonio/video_grabber)

Ferramenta de linha de comando para baixar vídeos do YouTube na **maior qualidade técnica disponível** — vídeo + áudio em streams separados (DASH), mesclados sem reencode. Pensada para uso como material bruto em edição de vídeo.

---

## PT-BR

- [Dependências](#dependências-externas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Opções](#referência-de-opções)

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
git clone https://github.com/gsjonio/vidgrab.git
cd vidgrab
poetry install
```

---

### Uso

```bash
# Vídeo único — qualidade máxima
vidgrab https://youtu.be/dQw4w9WgXcQ

# Limitar a 1080p
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080

# Salvar em diretório específico
vidgrab https://youtu.be/dQw4w9WgXcQ --output ~/Videos/raw

# Baixar playlist inteira
vidgrab "https://youtube.com/playlist?list=PLxxxx" --playlist

# Múltiplas URLs de um arquivo .txt
vidgrab --batch urls.txt

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

### Nomeação dos arquivos

```text
{data_upload}-{slug-do-titulo}-{video_id}.{ext}
```

Exemplo: `20240315-never-gonna-give-you-up-dQw4w9WgXcQ.mp4`

Com `--write-json`, um arquivo `.json` é criado ao lado do vídeo:

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
| `--output DIR` | `-o` | Diretório de saída (padrão: diretório atual) |
| `--max-height INT` | | Limitar resolução vertical (ex.: `1080`) |
| `--playlist` | | Tratar URLs como playlists |
| `--force` | `-f` | Re-download mesmo se o arquivo já existe |
| `--cookies FILE` | | Arquivo de cookies (formato Netscape) |
| `--write-json` | | Salvar metadados em `.json` ao lado do vídeo |
| `--workers INT` | `-w` | Número de downloads paralelos (padrão: `3`, máx: `8`) |
| `--version` | `-V` | Exibir versão |
| `--help` | | Exibir ajuda |

---

## English

CLI tool to download YouTube videos at the **highest technically available quality** — separate video + audio DASH streams, merged without re-encoding. Intended as raw footage for video editing.

- [Dependencies](#external-dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#option-reference)

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
git clone https://github.com/gsjonio/vidgrab.git
cd vidgrab
poetry install
```

---

### Usage

```bash
# Single video — maximum quality
vidgrab https://youtu.be/dQw4w9WgXcQ

# Cap at 1080p
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080

# Save to a specific directory
vidgrab https://youtu.be/dQw4w9WgXcQ --output ~/Videos/raw

# Download an entire playlist
vidgrab "https://youtube.com/playlist?list=PLxxxx" --playlist

# Download from a .txt file
vidgrab --batch urls.txt

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

### Output filename pattern

```text
{upload_date}-{title-slug}-{video_id}.{ext}
```

Example: `20240315-never-gonna-give-you-up-dQw4w9WgXcQ.mp4`

With `--write-json`, a `.json` sidecar is saved next to each video:

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
| `--output DIR` | `-o` | Output directory (default: current directory) |
| `--max-height INT` | | Cap vertical resolution (e.g. `1080`) |
| `--playlist` | | Treat URLs as playlists |
| `--force` | `-f` | Re-download even if the file already exists |
| `--cookies FILE` | | Cookies file (Netscape format) |
| `--write-json` | | Save metadata as a `.json` sidecar next to the video |
| `--workers INT` | `-w` | Number of parallel downloads (default: `3`, max: `8`) |
| `--version` | `-V` | Show version and exit |
| `--help` | | Show help |
