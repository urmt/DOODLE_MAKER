# DoodleEduMaker

**AI-Powered Educational Video Creator for Everyone**

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()

---

## Overview

DoodleEduMaker is a fully local, AI-powered desktop application that generates professional doodle-style explanatory videos without requiring video editing expertise, expensive software subscriptions, or cloud dependencies. Perfect for educators, public service organizations, and content creators who need to produce engaging educational content quickly and privately.

### Key Features

- 🎨 **AI Doodle Generation**: Stable Diffusion + ControlNet creates whiteboard-style illustrations
- 🗣️ **Multi-Language Narration**: High-quality text-to-speech in English and Spanish
- 💻 **100% Local Processing**: All AI runs on your hardware - no internet required after setup
- 🔌 **Plugin System**: Extend functionality with community-developed modules
- 🎯 **Simple Script Format**: Write in JSON or Markdown, let AI do the rest
- 🚀 **Mid-Range Hardware**: Runs on Ryzen 3G systems with 8GB RAM
- 🔒 **Privacy First**: No telemetry, no cloud uploads, your data stays yours

---

## Quick Start

### System Requirements

**Minimum:**
- CPU: 4-core processor (AMD Ryzen 3 3200G or equivalent)
- RAM: 8GB
- GPU: Integrated graphics (512MB-2GB VRAM)
- Storage: 10GB free space
- OS: Fedora Linux (KDE), Ubuntu, Windows 10/11, or macOS 12+

**Recommended:**
- CPU: 6+ core processor
- RAM: 16GB
- GPU: Discrete GPU with 4GB+ VRAM
- Storage: 20GB free space (SSD preferred)

### Installation

#### Fedora Linux (Primary Platform)

**Flatpak (Recommended):**
```bash
flatpak install flathub io.github.urmt.DoodleEduMaker
```

**RPM:**
```bash
sudo dnf install doodleedumaker
```

**AppImage:**
```bash
chmod +x DoodleEduMaker-*.AppImage
./DoodleEduMaker-*.AppImage
```

#### Windows

Download the installer from [Releases](https://github.com/urmt/DOODLE_MAKER/releases) and run:
```powershell
DoodleEduMaker-Setup.exe
```

#### From Source (Development)

```bash
# Clone repository
git clone https://github.com/urmt/DOODLE_MAKER.git
cd DOODLE_MAKER

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Download AI models (first run only, ~4GB)
python src/setup_models.py

# Run application
python src/main.py
```

---

## Usage

### Creating Your First Video

1. **Write a Script** (example.json):
```json
{
  "title": "Water Conservation Tips",
  "language": "en",
  "voice": "female_us",
  "scenes": [
    {
      "id": 1,
      "narration": "Water is our most precious resource",
      "visual_description": "Drawing of Earth with water droplets surrounding it",
      "duration": "auto"
    },
    {
      "id": 2,
      "narration": "Turning off the tap while brushing saves 200 gallons per month",
      "visual_description": "Bathroom sink with running faucet and toothbrush",
      "duration": "auto"
    }
  ]
}
```

2. **Launch DoodleEduMaker**

3. **Import Script**: File → Open Script → Select your JSON/Markdown file

4. **Preview Settings**: Choose quality preset (Fast/Balanced/High)

5. **Generate**: Click "Generate Video" and wait 2-8 minutes per minute of content

6. **Export**: Save as MP4 or WebM

### Script Formats

**JSON Format**: Structured data with full control over parameters

**Markdown Format**: Easier to write, YAML frontmatter for metadata
```markdown
---
title: My Educational Video
language: es
voice: female_latam
---

## Scene 1
**Narration:** El agua es nuestro recurso más valioso
**Visual:** Dibujo de la Tierra con gotas de agua

## Scene 2
**Narration:** Cerrar el grifo al cepillarse ahorra 750 litros al mes
**Visual:** Lavabo de baño con grifo abierto y cepillo de dientes
```

---

## Documentation

- **User Guide**: [docs/user-guide.md](docs/user-guide.md)
- **API Documentation**: [docs/api-reference.md](docs/api-reference.md)
- **Plugin Development**: [docs/plugin-development.md](docs/plugin-development.md)
- **Systems Analysis**: [Systems_Analysis.md](Systems_Analysis.md)
- **Examples**: [examples/](examples/)

---

## Architecture

```
DoodleEduMaker Pipeline:
Script (JSON/MD) → Parser → AI Doodle Generator → Draw-On Animator
                                                         ↓
                                                    Video Assembler
                                                         ↑
                    TTS Engine (MeloTTS/Piper) ←────────┘
```

### Technology Stack

- **GUI**: PySide6 (Qt6) - Native KDE integration
- **Image Generation**: Stable Diffusion 1.5 + ControlNet
- **Text-to-Speech**: MeloTTS (primary), Piper TTS (fallback)
- **Video Processing**: FFmpeg, MoviePy
- **Languages**: Python 3.10+

---

## Performance

On target hardware (Ryzen 3G, 8GB RAM, integrated GPU):
- 1-minute video: ~2-3 minutes generation
- 3-minute video: ~5-7 minutes generation
- 5-minute video: ~8-12 minutes generation

Generation time scales linearly with content length. Discrete GPUs significantly reduce processing time.

---

## Language Support

| Language | Status | Voices Available |
|----------|--------|------------------|
| English  | ✅ Full | Male US, Female US, Male UK, Female UK, Neutral |
| Spanish (Latin America) | ✅ Full | Male, Female, Neutral |
| French   | 🔄 Planned | Coming in v2.0 |
| Chinese  | 🔄 Planned | Coming in v2.0 |

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v --cov=src

# Run linter
ruff check src/

# Type checking
mypy src/
```

---

## License

DoodleEduMaker is licensed under the **GNU General Public License v3.0**.

AI models included have their own permissive licenses:
- Stable Diffusion 1.5: CreativeML OpenRAIL-M
- MeloTTS: MIT License
- Piper TTS: MIT License

See [LICENSE](LICENSE) for full details.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/urmt/DOODLE_MAKER/issues)
- **Discussions**: [GitHub Discussions](https://github.com/urmt/DOODLE_MAKER/discussions)
- **Documentation**: [docs/](docs/)

---

## Roadmap

### v1.0 (MVP) - Current Development
- ✅ Script parsing (JSON/Markdown)
- ✅ AI doodle generation
- ✅ English/Spanish TTS
- ✅ Video assembly
- ✅ Qt GUI
- ✅ Plugin system foundation

### v1.1
- Background music support
- More voice options
- Batch processing
- Video templates

### v2.0
- Additional languages (French, Chinese, Japanese)
- Real-time preview
- Advanced editing tools
- Character animation

---

## Acknowledgments

Built with:
- [Stable Diffusion](https://github.com/CompVis/stable-diffusion) by CompVis
- [MeloTTS](https://github.com/myshell-ai/MeloTTS) by MyShell
- [Piper TTS](https://github.com/rhasspy/piper) by Rhasspy
- [PySide6](https://wiki.qt.io/Qt_for_Python) by The Qt Company
- [FFmpeg](https://ffmpeg.org/) and countless open-source contributors

---

**Made with ❤️ for educators, by educators**
