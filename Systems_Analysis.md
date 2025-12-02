# DoodleEduMaker: Complete Systems Analysis Document

**Version:** 1.0  
**Date:** December 2025  
**Prepared By:** Senior Systems Analyst  
**Project Classification:** Open-Source Educational Media Software

---

## Executive Summary

DoodleEduMaker represents an innovative approach to democratizing educational video creation by providing a fully local, AI-powered desktop application for generating doodle-style explanatory videos. This systems analysis evaluates the technical feasibility, architectural design, and implementation strategy for a cross-platform application that prioritizes offline operation, mid-range hardware accessibility, and multi-language support.

The analysis concludes that the project is **technically feasible** with current open-source AI technologies, though with important performance considerations for integrated GPU systems. Estimated development timeline is 12-18 months for MVP release, with modular architecture enabling continuous enhancement through community-developed plug-ins.

**Key Findings:**
- Local AI inference is viable on Ryzen 3G 4-core systems with 8GB RAM, though generation times will range from 2-8 minutes per video
- Open-source TTS solutions like MeloTTS and XTTS-v2 provide acceptable narration quality for English and Spanish
- Stable Diffusion with ControlNet offers robust doodle-style image generation
- Qt framework provides optimal KDE integration while maintaining cross-platform capability
- Modular architecture enables future extensibility without core refactoring

---

## 1. Introduction and Purpose

### 1.1 Project Vision

DoodleEduMaker aims to empower educators, public service organizations, and content creators to produce professional-quality explanatory videos without requiring video editing expertise, expensive software subscriptions, or cloud-dependent services. By leveraging local AI processing, the application ensures privacy, accessibility in bandwidth-limited environments, and independence from internet connectivity.

### 1.2 Scope Definition

**In Scope:**
- Desktop application for Fedora Linux KDE (primary) with Windows/macOS compatibility
- Structured script input parsing (JSON, Markdown formats)
- AI-driven doodle/whiteboard-style video generation
- High-quality offline text-to-speech narration
- Multi-language support (English, Latin American Spanish initially)
- Local processing without cloud dependencies
- Modular architecture for plug-in extensibility
- Export to common video formats (MP4, WebM)

**Out of Scope (Initial Release):**
- Built-in video editing capabilities (reserved for plug-ins)
- Real-time video rendering/preview
- Realistic or photographic video styles
- Live animation or character rigging
- Mobile application versions
- Cloud synchronization or collaboration features

### 1.3 Target Stakeholders

**Primary Users:**
- Public health educators creating awareness campaigns
- Environmental organizations producing explainer content
- Civic education initiatives
- Independent educational content creators
- Non-profit organizations with limited media budgets
- Teachers creating supplementary classroom materials

**Secondary Stakeholders:**
- Open-source developers contributing plug-ins
- Linux/KDE community members
- Accessibility advocates
- Multi-language education communities

### 1.4 Key Terminology

**Doodle-Style Video:** Animated video format where illustrations appear to be hand-drawn in real-time, typically on a whiteboard or clean background. Elements progressively sketch onto screen, maintaining viewer engagement through visual revelation.

**Structured Script:** Formatted input document (JSON or Markdown) containing hierarchical scene definitions with narration text, visual descriptions, timing cues, and metadata. Example structure:

```json
{
  "title": "Water Conservation Tips",
  "language": "en",
  "scenes": [
    {
      "id": 1,
      "narration": "Water is our most precious resource",
      "visual_description": "Drawing of Earth with water droplets",
      "duration": "auto",
      "reference_image": "earth.jpg"
    }
  ]
}
```

**Integrated GPU:** Graphics processing unit embedded within CPU die (e.g., AMD Vega, Intel UHD), sharing system RAM, typically with 512MB-2GB effective memory and lower computational throughput than discrete GPUs.

**Offline TTS:** Text-to-speech synthesis performed entirely on local hardware using pre-downloaded models, without requiring internet connectivity for voice generation.

---

## 2. Requirements Gathering

### 2.1 Functional Requirements

#### FR1: Script Input and Parsing
- **FR1.1:** Accept structured scripts in JSON format with schema validation
- **FR1.2:** Accept Markdown format with YAML frontmatter for metadata
- **FR1.3:** Parse scene definitions including narration text, visual descriptions, timing parameters
- **FR1.4:** Support reference image attachment per scene (JPEG, PNG, WebP formats)
- **FR1.5:** Validate script completeness and provide actionable error messages
- **FR1.6:** Support UTF-8 encoding for multi-language characters

#### FR2: AI Doodle Generation
- **FR2.1:** Generate doodle-style images from text descriptions using local AI models
- **FR2.2:** Apply sketch/whiteboard aesthetic consistently across scenes
- **FR2.3:** Optionally use reference images to guide style and composition
- **FR2.4:** Support batch generation of multiple scenes
- **FR2.5:** Generate draw-on animation sequences (stroke-by-stroke reveal)
- **FR2.6:** Maintain visual consistency within a project (color palette, line style)

#### FR3: Narrator Voice Synthesis
- **FR3.1:** Generate natural-sounding speech from narration text using offline TTS
- **FR3.2:** Support English (multiple accents: US, UK, neutral) and Latin American Spanish
- **FR3.3:** Provide expressive prosody with appropriate intonation and pacing
- **FR3.4:** Allow voice selection (male, female, neutral options per language)
- **FR3.5:** Support SSML markup for pronunciation control and emphasis
- **FR3.6:** Sync audio generation with video scene timing

#### FR4: Video Assembly
- **FR4.1:** Combine generated doodle animations with synchronized narration
- **FR4.2:** Apply draw-on effects with configurable speed
- **FR4.3:** Add background music or ambient sound (user-provided, optional)
- **FR4.4:** Insert transitions between scenes (fade, wipe, or none)
- **FR4.5:** Export to MP4 (H.264/H.265) and WebM formats
- **FR4.6:** Support resolution options: 720p, 1080p, with quality presets

#### FR5: User Interface
- **FR5.1:** Provide intuitive script editor with syntax highlighting
- **FR5.2:** Enable drag-and-drop for reference images
- **FR5.3:** Display generation progress with estimated time remaining
- **FR5.4:** Offer preview capability for generated doodles before final render
- **FR5.5:** Include language selector for output
- **FR5.6:** Provide settings panel for quality/performance trade-offs

#### FR6: Extensibility and Modularity
- **FR6.1:** Implement plug-in system with documented API
- **FR6.2:** Support dynamic loading of extension modules
- **FR6.3:** Provide hooks for pre/post-processing at each pipeline stage
- **FR6.4:** Enable community-developed components (effects, editors, exporters)

### 2.2 Non-Functional Requirements

#### NFR1: Performance
- **NFR1.1:** Generate 1-minute video in 2-8 minutes on target hardware (Ryzen 3G, 8GB RAM)
- **NFR1.2:** GUI remains responsive during background processing
- **NFR1.3:** Memory usage not exceeding 6GB during generation
- **NFR1.4:** Efficient caching to avoid regenerating unchanged scenes
- **NFR1.5:** Startup time under 10 seconds on SSD systems

#### NFR2: Usability
- **NFR2.1:** Intuitive workflow requiring no video editing expertise
- **NFR2.2:** Clear documentation with tutorials and example projects
- **NFR2.3:** Helpful error messages with recovery suggestions
- **NFR2.4:** Sample templates for common educational video types
- **NFR2.5:** Keyboard shortcuts for power users
- **NFR2.6:** Accessibility compliance (screen reader compatibility, keyboard navigation)

#### NFR3: Compatibility
- **NFR3.1:** Primary support for Fedora Linux with KDE Plasma desktop
- **NFR3.2:** Secondary support for Ubuntu, Arch, Windows 10/11, macOS 12+
- **NFR3.3:** CPU architecture support: x86_64 (primary), ARM64 (future consideration)
- **NFR3.4:** Minimum hardware: 4-core CPU, 8GB RAM, integrated GPU, 10GB storage
- **NFR3.5:** Recommended hardware: 6+ core CPU, 16GB RAM, discrete GPU, 20GB storage

#### NFR4: Reliability
- **NFR4.1:** Graceful degradation on lower-end hardware
- **NFR4.2:** Auto-save project state every 5 minutes
- **NFR4.3:** Crash recovery with partial work preservation
- **NFR4.4:** Validation checks preventing corrupt output
- **NFR4.5:** Comprehensive logging for troubleshooting

#### NFR5: Maintainability
- **NFR5.1:** Modular codebase with clear separation of concerns
- **NFR5.2:** Comprehensive unit and integration tests (>80% coverage)
- **NFR5.3:** API documentation for plug-in developers
- **NFR5.4:** Versioned model format for backward compatibility
- **NFR5.5:** CI/CD pipeline for automated testing and builds

#### NFR6: Legal and Ethical
- **NFR6.1:** Open-source license (GPLv3 or Apache 2.0)
- **NFR6.2:** All bundled AI models under permissive licenses
- **NFR6.3:** Bias mitigation in visual generation (diverse representation)
- **NFR6.4:** Inclusive voice options across genders and accents
- **NFR6.5:** Privacy-first design with no telemetry/tracking
- **NFR6.6:** Clear attribution for AI-generated content in metadata

### 2.3 User Stories and Use Cases

#### User Story 1: Public Health Educator
*As a public health educator, I want to create a 3-minute video explaining vaccination benefits in Spanish, so that I can reach Spanish-speaking communities on social media without hiring a video production team.*

**Acceptance Criteria:**
- Upload script with 8-10 scenes of narration and visual descriptions
- Select Latin American Spanish voice
- Attach reference images for medical illustrations
- Generate video in under 25 minutes
- Export MP4 suitable for Instagram and YouTube

#### User Story 2: Environmental NGO
*As an environmental organization volunteer, I want to produce weekly explainer videos about climate topics, so that I can maintain consistent educational content without internet access in remote field office.*

**Acceptance Criteria:**
- Work entirely offline after initial setup
- Reuse visual style across multiple videos
- Process scripts quickly with template support
- Export in formats optimized for bandwidth-limited audiences

#### User Story 3: Teacher Creating Classroom Content
*As a middle school teacher, I want to convert my lesson outlines into engaging animated videos, so that I can provide visual learners with supplementary materials.*

**Acceptance Criteria:**
- Simple interface requiring no technical training
- Preview doodles before committing to full render
- Adjust narration voice and speed
- Create 5-minute videos during planning period

### 2.4 Use Case Diagram (Textual Description)

**Primary Actors:** Content Creator, System Administrator, Plug-in Developer

**Use Cases:**
1. **Create New Project:** Creator initiates new video project, sets language and metadata
2. **Import Structured Script:** Creator uploads JSON/Markdown file or uses built-in editor
3. **Attach Reference Images:** Creator adds visual guides for AI generation
4. **Configure Generation Settings:** Creator selects quality preset and voice
5. **Generate Video:** System processes script through AI pipeline
6. **Preview Results:** Creator reviews generated doodles and audio
7. **Adjust and Regenerate:** Creator modifies script/settings and regenerates specific scenes
8. **Export Final Video:** System encodes final video in selected format
9. **Install Application:** Admin installs on Fedora/other platform with dependencies
10. **Develop Plug-in:** Developer creates extension using documented API
11. **Load Community Plug-in:** Creator installs third-party enhancement

**System Boundary:** DoodleEduMaker application and local file system; external boundary includes OS services, file browsers, web browsers (for documentation).

---

## 3. Feasibility Study

### 3.1 Technical Feasibility

#### 3.1.1 AI Model Integration Analysis

**Doodle Image Generation:**

Current open-source solutions offer viable paths for local doodle generation:

| Solution | Approach | Hardware Demands | Quality | License |
|----------|----------|------------------|---------|---------|
| Stable Diffusion 1.5 + ControlNet (Scribble) | Text-to-image with sketch control | 4-6GB VRAM, ~15-30s per image on integrated GPU | High consistency, good doodle aesthetic | CreativeML OpenRAIL-M |
| SDXL-Turbo + ControlNet | Faster inference, similar control | 6-8GB VRAM, ~8-15s per image | Higher quality, more VRAM | OpenRAIL++ |
| LCM-LoRA with SD 1.5 | Latent Consistency Models for speed | 4GB VRAM, ~5-10s per image | Good quality, 4-8 step generation | Apache 2.0 |
| Neural Doodle (Older) | Style transfer approach | 2-3GB VRAM, ~20-40s | Lower quality, deprecated | MIT |

**Recommendation:** Stable Diffusion 1.5 with ControlNet (Scribble/Lineart) and optional LCM-LoRA for speed optimization. This combination provides:
- Acceptable inference time on integrated GPUs (20-30 seconds per scene)
- Strong community support and documentation
- Fine-tuning capability for consistent doodle style
- Permissive licensing for distribution

**Technical Challenges:**
- Integrated GPUs like Vega with 512MB-2GB effective VRAM require model quantization (INT8) and potentially CPU offloading
- Batch size limited to 1 on constrained hardware
- May need reduced resolution generation (512x512) with upscaling for final output

**Mitigation Strategies:**
- Implement INT8 quantization using bitsandbytes library
- Use CPU inference fallback with performance warning
- Provide quality presets: Fast (CPU), Balanced (integrated GPU), High (discrete GPU)
- Cache generated images aggressively to avoid regeneration

**Text-to-Speech Solutions:**

| TTS System | Languages | Voice Quality | Hardware | License |
|------------|-----------|---------------|----------|---------|
| MeloTTS | English, Spanish, French, Chinese, Japanese | Natural, good prosody | CPU-based, ~1-2s per sentence | MIT |
| XTTS-v2 (Coqui) | 17 languages including ES/EN | Expressive, near-human | 2-4GB VRAM or CPU, ~2-5s per sentence | Coqui Public License |
| Piper TTS | 40+ languages | Clear, less expressive | Lightweight CPU, <1s per sentence | MIT |
| eSpeak-ng | 100+ languages | Robotic, functional | Minimal CPU | GPL v3 |

**Recommendation:** Dual implementation with MeloTTS (primary) and Piper TTS (fallback). MeloTTS provides the expressive narration quality needed for engaging educational content, while Piper offers fast processing for previews and low-end hardware.

**Multi-Language Considerations:**
- English: Multiple accent models available (US, UK, Indian)
- Spanish (Latin American): Requires specific model training/fine-tuning or use of Coqui XTTS-v2 with Spanish voices
- Future languages: Documented process for adding language support through model downloads

**Video Assembly:**

Existing frameworks provide robust video composition:
- **FFmpeg:** Industry-standard video encoding, supports all needed formats, CPU-based with hardware acceleration options
- **OpenCV:** Python bindings for image manipulation and basic video operations
- **MoviePy:** High-level Python library wrapping FFmpeg, suitable for programmatic video editing

**Draw-On Animation:**
Traditional approaches use alpha masking to progressively reveal sketches. Implementation via:
1. Generate complete doodle image
2. Create stroke-order mask using edge detection or ControlNet scribble output
3. Apply progressive alpha mask over video frames
4. Composite with background

**Performance:** Animation generation adds minimal overhead (~1-2 seconds per scene) using pre-generated masks.

#### 3.1.2 Cross-Platform Framework Analysis

| Framework | Language | KDE Integration | Cross-Platform | Learning Curve | License |
|-----------|----------|----------------|----------------|----------------|---------|
| Qt (PyQt6/PySide6) | Python/C++ | Excellent (native KDE) | Windows, macOS, Linux | Moderate | LGPL/Commercial |
| GTK (PyGObject) | Python/C | Good (GNOME-native) | Windows, macOS, Linux | Moderate | LGPL |
| Electron | JavaScript | Poor (web-based) | Windows, macOS, Linux | Low | MIT |
| Avalonia UI | C# | Poor (non-native) | Windows, macOS, Linux | Moderate | MIT |
| wxPython | Python | Moderate | Windows, macOS, Linux | Moderate | wxWindows |

**Recommendation:** Qt using PySide6 (official Python bindings). Rationale:
- Native KDE Plasma integration (Qt is KDE's foundation)
- Mature Python bindings with comprehensive documentation
- Excellent cross-platform support with native look-and-feel
- Strong community and commercial backing
- LGPL license compatible with open-source distribution

**Alternative for Future Consideration:** Tauri (Rust + web frontend) for potentially smaller binary sizes and modern web-based UI, though at cost of KDE integration quality.

#### 3.1.3 Hardware Performance Validation

**Target System Specification:**
- CPU: AMD Ryzen 3 3200G (4 cores, 8 threads, 3.6GHz base)
- GPU: Integrated Radeon Vega 8 (512MB-2GB effective)
- RAM: 8GB DDR4
- Storage: 256GB SSD

**Estimated Performance Metrics:**

| Pipeline Stage | Time per Scene | Bottleneck | Optimization |
|----------------|----------------|------------|--------------|
| Script Parsing | <1 second | CPU (negligible) | - |
| Doodle Generation (SD 1.5) | 20-30 seconds | GPU/VRAM | Quantization, caching |
| Draw-On Animation | 1-2 seconds | CPU | Pre-computation |
| TTS Generation | 2-5 seconds | CPU | Batching, caching |
| Video Encoding | 5-10 seconds per minute | CPU | Hardware accel if available |

**Total Time for 3-Minute Video (10 scenes):**
- Doodle Generation: 10 × 25s = 250 seconds (4.2 minutes)
- Animation: 10 × 1.5s = 15 seconds
- TTS: 10 × 3s = 30 seconds
- Video Encoding: 3 × 7s = 21 seconds
- **Total: ~5.5 minutes** (1.8× content length)

**Scaling:**
- 1-minute video: ~2-3 minutes generation
- 5-minute video: ~8-12 minutes generation

**Conclusion:** Performance targets are achievable on specified hardware with appropriate optimizations.

### 3.2 Economic Feasibility

#### 3.2.1 Development Cost Estimation

**Team Composition (Full-Time Equivalents):**
- Senior Software Engineer (Python/AI): 1 FTE × 12 months
- UI/UX Designer: 0.5 FTE × 6 months
- DevOps/Build Engineer: 0.25 FTE × 12 months
- Technical Writer: 0.25 FTE × 6 months
- QA/Testing: 0.5 FTE × 8 months

**Cost Breakdown (USD):**
- Personnel: $180,000 (blended rate for open-source project/grant funding)
- Hardware/Testing Devices: $5,000 (various systems for compatibility)
- Infrastructure: $2,000 (CI/CD, repository hosting if self-managed)
- Licensing/Tools: $1,000 (development tools, assets)
- **Total: ~$188,000 for MVP (12-month development)**

**Open-Source Economic Benefits:**
- Zero licensing costs for end-users
- Community contributions reduce maintenance burden
- Plug-in ecosystem enables features without core team investment
- Educational/non-profit sectors gain tool otherwise unaffordable

**Sustainability Model:**
- Grant funding from educational foundations
- Optional paid support/training for organizations
- Sponsored development of specific features
- Donations from user community

#### 3.2.2 Total Cost of Ownership (User Perspective)

**Initial Investment:**
- Software: $0 (open-source)
- Hardware: $400-800 (mid-range PC if purchasing)
- Training: $0 (documentation/tutorials included)

**Ongoing Costs:**
- Maintenance: $0 (community-maintained)
- Upgrades: $0 (free updates)
- Computing: ~$0.05 electricity per video (negligible)

**Comparison to Alternatives:**
- Commercial tools: $20-50/month subscriptions = $240-600/year
- Outsourced production: $500-2000 per video
- **ROI: Immediate for organizations producing 2+ videos monthly**

### 3.3 Operational Feasibility

#### 3.3.1 Installation and Deployment

**Fedora Linux (Primary Platform):**

Package Distribution:
- Flatpak (recommended): Sandboxed, dependency-managed, fits KDE Discover
- RPM Fusion repository: Native package with system integration
- AppImage: Self-contained, no installation required

Installation Complexity: Medium
- Flatpak: Single-click install via Discover
- RPM: `sudo dnf install doodleedumaker`
- AppImage: Download and run (mark executable)

**Dependency Management:**
- AI models: Downloaded on first run (~4GB) with progress indication
- System libraries: Bundled in Flatpak, specified in RPM dependencies
- Python environment: Isolated via venv or Flatpak runtime

**Cross-Platform:**
- Windows: Installer with embedded Python, auto-dependency resolution
- macOS: DMG with app bundle, Homebrew cask option
- Other Linux: AppImage or distribution-specific packages
