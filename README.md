# vidgrab

**PT-BR** | [EN](#english)

---

## PT-BR

Ferramenta de linha de comando para baixar vídeos do YouTube na **maior
qualidade técnica disponível** — vídeo + áudio em streams separados (DASH),
mesclados sem reencode. Pensada para uso como material bruto em edição de
vídeo.

### Dependências externas

| Ferramenta | Para quê | Como instalar |
|------------|----------|---------------|
| **Python 3.11+** | Runtime | [python.org](https://www.python.org/downloads/) |
| **ffmpeg** | Mesclar streams de vídeo e áudio | Veja abaixo |
| **yt-dlp** | Engine de download | Instalado automaticamente via pip |
| **Deno** *(opcional)* | Acesso a todos os formatos do YouTube, incluindo 4K/HDR | Veja abaixo |

#### Instalando o ffmpeg

**Windows** (via winget):
```
winget install ffmpeg
```
Ou baixe o executável em <https://ffmpeg.org/download.html> e adicione ao
`PATH`.

#### Instalando o Deno (recomendado)

Sem o Deno, o yt-dlp usa um método alternativo que pode não enxergar todos os
formatos disponíveis (ex.: 4K, HDR). Com o Deno instalado, a extração é
completa.

**Windows** (via winget):
```
winget install DenoLand.Deno
```

**macOS** (via Homebrew):
```
brew install deno
```

**Linux**:
```
curl -fsSL https://deno.land/install.sh | sh
```

**macOS** (via Homebrew):
```
brew install ffmpeg
```

**Linux** (Debian/Ubuntu):
```
sudo apt install ffmpeg
```

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/vidgrab.git
cd vidgrab

# Crie e ative um virtualenv
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# Instale as dependências
pip install -e .
```

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

# Conteúdo com restrição de idade (forneça um arquivo de cookies do browser)
vidgrab https://youtu.be/dQw4w9WgXcQ --cookies ~/cookies.txt
```

#### Formato do arquivo `--batch`

Uma URL por linha. Linhas começando com `#` são ignoradas.

```
# Meus vídeos favoritos
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/VIDEO_ID_2
```

### Nomeação dos arquivos

```
{data_upload}-{slug-do-titulo}-{video_id}.{ext}
```

Exemplo: `20240315-tutorial-de-edicao-de-video-dQw4w9WgXcQ.mp4`

Um arquivo `.json` de metadados é criado ao lado de cada vídeo:

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

### Container e qualidade

| Streams disponíveis | Container de saída |
|---------------------|-------------------|
| H.264 vídeo + AAC áudio | `mp4` (sem reencode) |
| VP9/AV1 vídeo + Opus áudio | `mkv` (sem reencode) |

O objetivo é **nunca recodificar** — apenas mesclar os streams.

### Referência de opções

```
Argumentos:
  [URLS]...               Uma ou mais URLs do YouTube

Opções:
  -b, --batch FILE        Arquivo .txt com uma URL por linha
  -o, --output DIR        Diretório de saída (padrão: diretório atual)
  --max-height INT        Limitar resolução vertical (ex.: 1080)
  --playlist              Tratar URLs como playlists
  -f, --force             Reforçar download mesmo se arquivo existe
  --cookies FILE          Arquivo de cookies (Netscape format)
  -V, --version           Exibir versão
  --help                  Exibir ajuda
```

---

## English

Command-line tool to download YouTube videos at the **highest technically
available quality** — separate video + audio DASH streams, merged without
re-encoding. Intended as raw footage for video editing.

### External dependencies

| Tool | Purpose | How to install |
|------|---------|----------------|
| **Python 3.11+** | Runtime | [python.org](https://www.python.org/downloads/) |
| **ffmpeg** | Merge video + audio streams | See below |
| **yt-dlp** | Download engine | Installed automatically via pip |

#### Installing ffmpeg

**Windows** (via winget):
```
winget install ffmpeg
```
Or grab the binary from <https://ffmpeg.org/download.html> and add it to your
`PATH`.

**macOS** (via Homebrew):
```
brew install ffmpeg
```

**Linux** (Debian/Ubuntu):
```
sudo apt install ffmpeg
```

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/vidgrab.git
cd vidgrab

# Create and activate a virtualenv
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -e .
```

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

# Age-restricted content (provide a browser cookies file)
vidgrab https://youtu.be/dQw4w9WgXcQ --cookies ~/cookies.txt
```

#### `--batch` file format

One URL per line. Lines starting with `#` are ignored.

```
# My favourite videos
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/VIDEO_ID_2
```

### Output filename pattern

```
{upload_date}-{title-slug}-{video_id}.{ext}
```

Example: `20240315-tutorial-de-edicao-de-video-dQw4w9WgXcQ.mp4`

A `.json` sidecar file is written next to each video:

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

### Container and quality

| Available streams | Output container |
|-------------------|-----------------|
| H.264 video + AAC audio | `mp4` (no re-encode) |
| VP9/AV1 video + Opus audio | `mkv` (no re-encode) |

The goal is to **never re-encode** — only mux the streams.

### Option reference

```
Arguments:
  [URLS]...               One or more YouTube URLs

Options:
  -b, --batch FILE        .txt file with one URL per line
  -o, --output DIR        Output directory (default: current directory)
  --max-height INT        Cap vertical resolution (e.g. 1080)
  --playlist              Treat URLs as playlists
  -f, --force             Re-download even if file exists
  --cookies FILE          Cookies file (Netscape format)
  -V, --version           Show version and exit
  --help                  Show help
```
