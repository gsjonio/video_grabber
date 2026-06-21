# Changelog

## [v0.2.0] — 2026-06-21

### ✨ Novas funcionalidades

- **`--write-json`** — O arquivo `.json` de metadados agora é **opt-in**. Use a flag para gerá-lo ao lado do vídeo:
  ```bash
  vidgrab https://youtu.be/... --write-json
  ```
- **Aviso de licença Creative Commons** — vidgrab exibe um aviso `⚠ Not Creative Commons` quando o vídeo baixado não está sob licença CC, ajudando a rastrear restrições de uso do material.

### 🐛 Correções

- `download()` agora delega para `download_batch()` — erros tratados de forma consistente em ambos os métodos
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
