# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

**DoodleEduMaker** - An AI-powered desktop application for generating doodle-style educational videos locally using offline AI models. Designed for educators, public service organizations, and content creators to produce professional-quality explanatory videos without video editing expertise or cloud dependencies.

**Current State**: Active Development (45% complete). Core AI pipeline implemented (script parsing → doodle generation → TTS). Video assembly, GUI, and plugin system pending.

## Project Details

**Systems Analysis**: `Systems_Analysis.md`

**Target Platform**: Cross-platform desktop (Fedora Linux KDE primary, Windows/macOS secondary)

**Tech Stack** (planned):
- Framework: Qt (PySide6) for GUI
- Language: Python
- AI Models: Stable Diffusion 1.5 + ControlNet for doodle generation
- TTS: MeloTTS (primary), Piper TTS (fallback)
- Video: FFmpeg, MoviePy for assembly

**Target Hardware**: Mid-range systems (Ryzen 3G 4-core, 8GB RAM, integrated GPU)

**License**: GPLv3 or Apache 2.0 (planned)

## Development Workflow (When Implementation Begins)

### Initial Setup

1. **Setup Python Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install pyside6 torch diffusers transformers
   ```

2. **Install System Dependencies**:
   ```powershell
   # FFmpeg for video processing
   winget install Gyan.FFmpeg
   
   # PyTorch with CPU support (or CUDA if GPU available)
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

### Project Structure

```
DOODLE_MAKER/
├── src/
│   ├── core/                    # Core AI pipeline modules
│   │   ├── script_parser.py     # ✅ JSON/Markdown parsing with validation
│   │   ├── doodle_generator.py  # ✅ Stable Diffusion + ControlNet
│   │   ├── tts_engine.py        # ✅ MeloTTS/Piper TTS integration
│   │   └── video_assembler.py   # ⬜ TODO: FFmpeg/MoviePy video assembly
│   ├── ui/                      # ⬜ TODO: Qt GUI (PySide6)
│   ├── utils/                   # Utility functions
│   ├── plugins/                 # ⬜ TODO: Plugin system
│   └── main.py                  # ✅ CLI entry point (GUI mode pending)
├── cache/                       # Generated doodles and audio (gitignored)
│   ├── doodles/
│   └── audio/
├── models/                      # AI models ~4GB (gitignored, downloaded on first run)
├── tests/                       # ⬜ TODO: Unit and integration tests
├── examples/
│   └── water_conservation.json  # Example script
├── docs/                        # Documentation
├── pyproject.toml               # Python packaging & tool config
├── requirements.txt             # Production dependencies
└── requirements-dev.txt         # Dev dependencies (pytest, ruff, mypy)
```

### Testing

```powershell
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage (target >80%)
pytest --cov=src/doodleedumaker tests/ --cov-report=term-missing --cov-report=html

# Run specific test file
pytest tests/unit/test_script_parser.py -v

# Run linting
ruff check src/

# Run type checking
mypy src/

# Run code formatting
black src/ tests/
```

## Architecture & Key Implementation Details

### Core Pipeline Flow
```
JSON/Markdown Script → ScriptParser → Script + Scene objects
                                        ↓
                            DoodleGenerator (SD1.5 + ControlNet)
                                        ↓
                            PIL Image (cached to cache/doodles/)
                                        ↓
                            TTSEngine (MeloTTS/Piper)
                                        ↓
                            Audio file (cached to cache/audio/)
                                        ↓
                            [TODO] VideoAssembler (FFmpeg/MoviePy)
                                        ↓
                            Final MP4/WebM video
```

### Module Responsibilities

**script_parser.py**
- Parses JSON and Markdown (with YAML frontmatter) script formats
- Validates against JSON schema using jsonschema library
- Returns Script dataclass containing list of Scene dataclasses
- Handles UTF-8 for multi-language support
- Scene validation: ensures narration, visual_description are non-empty
- Reference image path validation

**doodle_generator.py**
- Stable Diffusion 1.5 + ControlNet (scribble model) for doodle aesthetic
- Quality presets: FAST (4 steps, LCM scheduler), BALANCED (20 steps, INT8 quant), HIGH (50 steps, 768x768)
- Hardware detection: auto-enables INT8 quantization for <4GB VRAM
- Caching: generates hash from prompt+config, caches to avoid regeneration
- Style prompts: adds "simple line drawing, hand-drawn sketch, whiteboard doodle" etc.
- Negative prompts: excludes "photo, realistic, detailed shading" etc.
- Models loaded lazily on first generation call

**tts_engine.py**
- Dual-engine: MeloTTS (primary, expressive) + Piper TTS (fallback, fast)
- Voice mappings: maps internal Voice enum to engine-specific voice IDs
- Supports English (US/UK) and Spanish (LATAM/ES) with multiple voices per language
- Caching: generates hash from text+voice+config, saves WAV to cache/audio/
- Current implementation uses placeholder audio (real TTS integration pending)
- Returns Path to generated WAV file

**main.py**
- CLI mode: accepts --input (script path), --quality (fast/balanced/high), --preview
- GUI mode: placeholder (PySide6 imported but MainWindow not implemented)
- Logging: writes to doodleedumaker.log and stdout
- Pipeline orchestration: parse → generate doodles → generate audio → [TODO] assemble video

### Important Implementation Notes

**AI Model Loading**
- Models downloaded from HuggingFace on first run (~4GB total)
- Stable Diffusion 1.5: `runwayml/stable-diffusion-v1-5`
- ControlNet: `lllyasviel/control_v11p_sd15_scribble`
- Models cached in HuggingFace cache dir (not in repo)

**Caching Strategy**
- Both doodle_generator and tts_engine use MD5 hash-based caching
- Hash includes: content (prompt/text) + configuration parameters
- Cache files named: `{scene_id}_{hash}.png` or `{scene_id}_{hash}.wav`
- Prevents regeneration when rerunning same script

**Error Handling**
- Extensive validation in Scene and Script __post_init__ methods
- Parser raises ValueError with descriptive messages for invalid scripts
- Generators use try/except with logging, raising RuntimeError on failure
- All modules use Python logging module with class-level loggers

**Configuration**
- Quality presets defined in GenerationConfig dataclass
- TTSConfig dataclass for language/voice/speed settings
- Both use __post_init__ to adjust settings based on presets
- pyproject.toml contains tool configs (ruff, black, mypy, pytest)

## Key Design Principles

### Universal (Per User Rules)
- **No fake/placeholder data** - Use real implementations or clearly mark test data
- **Extensive error checking** - All code should have robust error handling
- **Detailed comments** - Especially for complex AI/data processing logic
- **Update WARP.md** - Keep this file current as project evolves from planning to implementation
- **Local execution preferred** - Build standalone Python/Rust apps rather than shell scripts

### Project-Specific Requirements

**Offline-first**:
- All AI processing must work without internet after initial model download
- Models downloaded once (~4GB) and cached locally
- No cloud dependencies or API calls

**Performance targets**: 
- 1-minute video in 2-8 minutes on target hardware
- Memory usage <6GB during generation
- GUI responsiveness during background processing
- Startup time <10 seconds on SSD

**Modular architecture**: 
- Plugin system for extensibility
- Clear separation of concerns (parsing, generation, TTS, assembly)
- Documented plugin API

**Multi-language support**: 
- English (US, UK accents) and Latin American Spanish initially
- UTF-8 support for scripts
- SSML markup for pronunciation control

**Privacy-first**: 
- No telemetry or tracking
- Local processing only
- User data never leaves machine

## Important Constraints

### Technical
- **Target Hardware Limitation**: Must run on integrated GPUs (512MB-2GB VRAM)
- **Model Quantization Required**: INT8 quantization for Stable Diffusion on constrained hardware
- **Scraping Reliability**: Web scraping may break with site redesigns - implement fallback data sources

### Legal/Ethical
- **AI Model Licensing**: Only use permissive licenses (MIT, Apache 2.0, CreativeML OpenRAIL-M)
- **Bias Mitigation**: Ensure diverse representation in visual generation
- **Data Attribution**: Clear attribution for AI-generated content and scraped data

## GitHub Repository
- **Remote**: https://github.com/urmt/DOODLE_MAKER.git
- **Branch**: main
- **Commit Policy**: Save to GitHub when projects run without errors (per user rules)
- **README Policy**: Always update README.md alongside WARP.md

## Common Commands

### Development Setup
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies (first time)
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```

### Running the Application
```powershell
# Process example script (CLI mode)
python src/main.py --input examples/water_conservation.json

# Use specific quality preset
python src/main.py --input examples/water_conservation.json --quality fast
python src/main.py --input examples/water_conservation.json --quality balanced  # Default
python src/main.py --input examples/water_conservation.json --quality high

# Preview mode (doodles only, no video assembly)
python src/main.py --input script.json --preview

# Verbose logging
python src/main.py --input script.json --verbose

# GUI mode (not yet implemented)
python src/main.py
```

### Cache Management
```powershell
# Clear generated doodles cache
Remove-Item -Recurse -Force cache\doodles\*

# Clear audio cache
Remove-Item -Recurse -Force cache\audio\*

# Clear all caches
Remove-Item -Recurse -Force cache\*

# View cache size
Get-ChildItem cache -Recurse | Measure-Object -Property Length -Sum
```

### Development Tools
```powershell
# Run linter
ruff check src/

# Auto-fix linting issues
ruff check --fix src/

# Format code
black src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest tests/ -v --cov=src/doodleedumaker --cov-report=html

# View coverage report
Start-Process htmlcov\index.html  # Windows
```

## Next Steps (Priority Order)

1. **Implement Video Assembler** - Complete the core pipeline by adding FFmpeg/MoviePy video assembly
   - File: `src/core/video_assembler.py`
   - Combine doodle images with audio
   - Add draw-on animation effects
   - Support MP4/WebM export

2. **Write Comprehensive Tests** - Achieve >80% coverage
   - Unit tests for script_parser, doodle_generator, tts_engine
   - Integration tests for full pipeline
   - Mock AI models to avoid loading during tests
   - Use pytest fixtures for sample scripts

3. **Create Plugin System** - Enable extensibility
   - File: `src/plugins/plugin_api.py`
   - Hook system for pre/post-processing
   - Plugin discovery and loading
   - Example plugin template

4. **Build Qt GUI** - User-friendly interface
   - File: `src/ui/main_window.py`
   - Script editor with syntax highlighting
   - Project management
   - Progress tracking during generation
   - Preview functionality

5. **Add Configuration System** - User preferences
   - File: `src/core/config.py`
   - YAML-based config: `config/default_config.yaml`
   - Quality presets customization
   - Default voice mappings

6. **Package for Distribution** - Flatpak, AppImage, Windows installer
   - Directory: `packaging/`
   - Flatpak manifest
   - AppImage configuration
   - Windows installer (Inno Setup)

## Status Tracking

**Last Updated**: 2025-12-02

**Current Phase**: Active Development (45% Complete)

**Development Environment**: Windows (pwsh), Python 3.10+

### Completed (✅)
- Project structure and configuration (pyproject.toml, requirements.txt, .gitignore)
- Comprehensive documentation (README.md, WARP.md, CHANGELOG.md, Systems_Analysis.md)
- Script parser module with JSON/Markdown support and schema validation
- Doodle generator with Stable Diffusion 1.5 + ControlNet integration
- TTS engine with MeloTTS/Piper support and multi-language voices
- CLI entry point with quality presets and logging
- Example script (examples/water_conservation.json)
- Caching system for doodles and audio

### In Progress (🔄)
- None (pending priority decision)

### Pending (⬜)
- **HIGH**: Video assembler module (FFmpeg/MoviePy integration)
- **HIGH**: Unit and integration tests (pytest suite)
- **MEDIUM**: Plugin system architecture
- **MEDIUM**: Qt GUI application (PySide6)
- **MEDIUM**: Configuration system (YAML-based)
- **LOW**: Packaging (Flatpak, AppImage, Windows installer)

### Known Issues
- TTS engine currently generates placeholder audio (real TTS integration pending)
- GUI mode not implemented (CLI mode only)
- Video assembly not implemented (pipeline stops after audio generation)
- No test suite yet (manual testing only)
- AI models (~4GB) must be downloaded on first run

### Recent Changes
- See CHANGELOG.md for detailed version history
- See PROJECT_STATUS.md for current state overview

## Troubleshooting

### Model Loading Issues
If you encounter errors loading AI models:
```powershell
# Clear HuggingFace cache
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface

# Reinstall dependencies
pip uninstall torch torchvision diffusers transformers -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers accelerate
```

### CUDA/GPU Issues
If CUDA is not detected or GPU errors occur:
```powershell
# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')"

# Force CPU mode by editing GenerationConfig in code
# Or set environment variable
$env:CUDA_VISIBLE_DEVICES = "-1"
```

### Memory Errors
If you run out of memory:
- Use `--quality fast` preset for lower memory usage
- Close other applications
- Ensure swap/pagefile is enabled
- Consider upgrading RAM or using a system with discrete GPU

### Import Errors
If you get import errors:
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Verify installation
pip list | Select-String "PySide6|torch|diffusers"

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## Development Tips

### Working with AI Models
- First run downloads ~4GB of models - expect 10-30 minutes depending on internet speed
- Models are cached in `~/.cache/huggingface/` (not in repo)
- Use FAST preset during development to speed up iteration
- Mock AI models in tests to avoid loading during test runs

### Code Style
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Docstrings required for all classes and public methods (Google style)
- Line length: 100 characters (configured in pyproject.toml)
- Use dataclasses for configuration objects

### Adding New Features
1. Create feature branch from main
2. Implement feature with extensive error checking
3. Add unit tests (>80% coverage)
4. Update documentation (README.md, WARP.md)
5. Run linter and type checker
6. Submit PR or commit to main

### When to Update WARP.md
- After implementing major features
- When adding new commands or workflows
- When discovering non-obvious gotchas
- After architectural changes
- When project phase changes (e.g. planning → development → testing)

### Performance Profiling
To profile performance bottlenecks:
```powershell
# Use cProfile
python -m cProfile -o profile.stats src/main.py --input script.json
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"

# Use line_profiler for specific functions
pip install line_profiler
# Add @profile decorator to functions
kernprof -l -v src/main.py --input script.json
```
