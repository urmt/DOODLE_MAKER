"""
Script Parser Module for DoodleEduMaker

This module handles parsing of structured scripts in JSON and Markdown formats,
validates them against the schema, and converts them into internal Scene objects.

Supports:
- JSON format with full schema validation
- Markdown format with YAML frontmatter
- UTF-8 encoding for multi-language support
- Comprehensive error reporting with actionable messages
"""

import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import frontmatter
import jsonschema
import markdown
import yaml
from jsonschema import validate, ValidationError

# Configure logging
logger = logging.getLogger(__name__)


class ScriptFormat(Enum):
    """Supported script formats"""
    JSON = "json"
    MARKDOWN = "markdown"
    MD = "md"


class LanguageCode(Enum):
    """Supported language codes"""
    ENGLISH = "en"
    SPANISH = "es"
    SPANISH_LATAM = "es_latam"


@dataclass
class Scene:
    """
    Represents a single scene in the video.
    
    Attributes:
        id: Unique scene identifier
        narration: Text to be spoken by TTS
        visual_description: Description for AI doodle generation
        duration: Scene duration in seconds or "auto"
        reference_image: Optional path to reference image
        metadata: Additional scene-specific metadata
    """
    id: int
    narration: str
    visual_description: str
    duration: Union[str, float] = "auto"
    reference_image: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate scene data after initialization"""
        if not self.narration or not self.narration.strip():
            raise ValueError(f"Scene {self.id}: narration cannot be empty")
        
        if not self.visual_description or not self.visual_description.strip():
            raise ValueError(f"Scene {self.id}: visual_description cannot be empty")
        
        # Validate duration
        if self.duration != "auto":
            try:
                duration_float = float(self.duration)
                if duration_float <= 0:
                    raise ValueError(f"Scene {self.id}: duration must be positive")
                self.duration = duration_float
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"Scene {self.id}: duration must be 'auto' or a positive number, got '{self.duration}'"
                ) from e
        
        # Convert reference_image to Path if it's a string
        if isinstance(self.reference_image, str):
            self.reference_image = Path(self.reference_image)


@dataclass
class Script:
    """
    Represents a complete video script with all scenes and metadata.
    
    Attributes:
        title: Video title
        language: Target language code
        voice: Voice identifier for TTS
        scenes: List of Scene objects
        metadata: Additional script-level metadata
    """
    title: str
    language: str
    scenes: List[Scene]
    voice: str = "female_us"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate script data after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Script title cannot be empty")
        
        if not self.scenes:
            raise ValueError("Script must contain at least one scene")
        
        # Validate language code
        valid_languages = [lang.value for lang in LanguageCode]
        if self.language not in valid_languages:
            logger.warning(
                f"Language '{self.language}' not in supported list: {valid_languages}. "
                "Proceeding anyway, but TTS may not work correctly."
            )
        
        # Validate scene IDs are unique and sequential
        scene_ids = [scene.id for scene in self.scenes]
        if len(scene_ids) != len(set(scene_ids)):
            raise ValueError("Scene IDs must be unique")
        
        # Sort scenes by ID
        self.scenes.sort(key=lambda x: x.id)

    def get_scene_by_id(self, scene_id: int) -> Optional[Scene]:
        """Get a scene by its ID"""
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        return None
    
    def get_total_scenes(self) -> int:
        """Get total number of scenes"""
        return len(self.scenes)


# JSON Schema for validation
JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["title", "language", "scenes"],
    "properties": {
        "title": {
            "type": "string",
            "minLength": 1,
            "description": "Video title"
        },
        "language": {
            "type": "string",
            "enum": ["en", "es", "es_latam"],
            "description": "Target language code"
        },
        "voice": {
            "type": "string",
            "description": "Voice identifier for TTS",
            "default": "female_us"
        },
        "scenes": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "narration", "visual_description"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Unique scene identifier"
                    },
                    "narration": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Text to be spoken"
                    },
                    "visual_description": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Description for AI generation"
                    },
                    "duration": {
                        "oneOf": [
                            {"type": "string", "enum": ["auto"]},
                            {"type": "number", "minimum": 0.1}
                        ],
                        "default": "auto",
                        "description": "Scene duration in seconds or 'auto'"
                    },
                    "reference_image": {
                        "type": "string",
                        "description": "Path to reference image"
                    }
                }
            }
        },
        "metadata": {
            "type": "object",
            "description": "Additional metadata"
        }
    }
}


class ScriptParser:
    """
    Parser for DoodleEduMaker script files.
    
    Handles both JSON and Markdown formats with comprehensive validation
    and error reporting.
    """
    
    def __init__(self):
        """Initialize the script parser"""
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def parse_file(self, file_path: Union[str, Path]) -> Script:
        """
        Parse a script file and return a Script object.
        
        Args:
            file_path: Path to the script file (JSON or Markdown)
        
        Returns:
            Script object with all scenes and metadata
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is unsupported or validation fails
            json.JSONDecodeError: If JSON is malformed
            yaml.YAMLError: If YAML frontmatter is malformed
        """
        file_path = Path(file_path)
        
        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"Script file not found: {file_path}")
        
        self.logger.info(f"Parsing script file: {file_path}")
        
        # Determine format from extension
        file_format = self._detect_format(file_path)
        
        # Read file with UTF-8 encoding
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File encoding error: {file_path} must be UTF-8 encoded"
            ) from e
        
        # Parse based on format
        if file_format == ScriptFormat.JSON:
            return self._parse_json(content, file_path)
        elif file_format in (ScriptFormat.MARKDOWN, ScriptFormat.MD):
            return self._parse_markdown(content, file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def _detect_format(self, file_path: Path) -> ScriptFormat:
        """Detect script format from file extension"""
        extension = file_path.suffix.lower()
        
        if extension == '.json':
            return ScriptFormat.JSON
        elif extension in ('.md', '.markdown'):
            return ScriptFormat.MARKDOWN
        else:
            raise ValueError(
                f"Unsupported file extension: {extension}. "
                "Supported formats: .json, .md, .markdown"
            )
    
    def _parse_json(self, content: str, file_path: Path) -> Script:
        """
        Parse JSON format script.
        
        Args:
            content: JSON string content
            file_path: Original file path (for error reporting)
        
        Returns:
            Script object
        
        Raises:
            json.JSONDecodeError: If JSON is malformed
            ValidationError: If JSON doesn't match schema
            ValueError: If data is invalid
        """
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {file_path}: {e.msg}",
                e.doc,
                e.pos
            ) from e
        
        # Validate against schema
        try:
            validate(instance=data, schema=JSON_SCHEMA)
        except ValidationError as e:
            raise ValueError(
                f"Script validation error in {file_path}: {e.message}\n"
                f"Path: {' -> '.join(str(p) for p in e.path)}"
            ) from e
        
        # Convert to Script object
        return self._dict_to_script(data, file_path)
    
    def _parse_markdown(self, content: str, file_path: Path) -> Script:
        """
        Parse Markdown format script with YAML frontmatter.
        
        Expected format:
        ---
        title: My Video
        language: en
        voice: female_us
        ---
        
        ## Scene 1
        **Narration:** The text to speak
        **Visual:** Description of what to draw
        **Duration:** auto
        **Reference:** path/to/image.jpg (optional)
        
        Args:
            content: Markdown string content
            file_path: Original file path (for error reporting)
        
        Returns:
            Script object
        
        Raises:
            yaml.YAMLError: If YAML frontmatter is malformed
            ValueError: If required fields are missing or invalid
        """
        try:
            post = frontmatter.loads(content)
        except yaml.YAMLError as e:
            raise ValueError(
                f"Invalid YAML frontmatter in {file_path}: {str(e)}"
            ) from e
        
        # Extract metadata from frontmatter
        metadata = post.metadata
        if not metadata:
            raise ValueError(
                f"Missing YAML frontmatter in {file_path}. "
                "Markdown scripts must start with --- delimited YAML metadata."
            )
        
        # Validate required fields
        required_fields = ['title', 'language']
        missing_fields = [f for f in required_fields if f not in metadata]
        if missing_fields:
            raise ValueError(
                f"Missing required fields in {file_path} frontmatter: {', '.join(missing_fields)}"
            )
        
        # Parse scenes from markdown content
        scenes = self._parse_markdown_scenes(post.content, file_path)
        
        if not scenes:
            raise ValueError(f"No scenes found in {file_path}")
        
        # Build script dict
        script_dict = {
            'title': metadata['title'],
            'language': metadata['language'],
            'voice': metadata.get('voice', 'female_us'),
            'scenes': scenes,
            'metadata': {k: v for k, v in metadata.items() 
                        if k not in ('title', 'language', 'voice')}
        }
        
        return self._dict_to_script(script_dict, file_path)
    
    def _parse_markdown_scenes(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse scenes from markdown content.
        
        Looks for ## Scene N headers followed by **Field:** value pairs.
        """
        scenes = []
        lines = content.strip().split('\n')
        
        current_scene = None
        scene_id = 0
        
        for line in lines:
            line = line.strip()
            
            # Check for scene header
            if line.startswith('## Scene'):
                # Save previous scene if exists
                if current_scene and 'narration' in current_scene and 'visual_description' in current_scene:
                    scenes.append(current_scene)
                
                # Start new scene
                scene_id += 1
                current_scene = {
                    'id': scene_id,
                    'duration': 'auto'
                }
            
            # Parse field lines
            elif line.startswith('**') and current_scene is not None:
                if ':**' in line or '**:' in line:
                    # Extract field name and value
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        field_name = parts[0].replace('**', '').strip().lower()
                        field_value = parts[1].replace('**', '').strip()
                        
                        # Map field names to scene keys
                        if field_name in ('narration', 'narration text', 'text'):
                            current_scene['narration'] = field_value
                        elif field_name in ('visual', 'visual_description', 'visual description', 'description'):
                            current_scene['visual_description'] = field_value
                        elif field_name == 'duration':
                            current_scene['duration'] = field_value
                        elif field_name in ('reference', 'reference_image', 'reference image', 'image'):
                            current_scene['reference_image'] = field_value
        
        # Add last scene
        if current_scene and 'narration' in current_scene and 'visual_description' in current_scene:
            scenes.append(current_scene)
        
        return scenes
    
    def _dict_to_script(self, data: Dict[str, Any], file_path: Path) -> Script:
        """
        Convert dictionary to Script object.
        
        Args:
            data: Dictionary with script data
            file_path: Original file path (for resolving relative paths)
        
        Returns:
            Script object
        """
        # Convert scenes
        scenes = []
        for scene_data in data['scenes']:
            # Resolve reference image path relative to script file
            if 'reference_image' in scene_data and scene_data['reference_image']:
                ref_path = Path(scene_data['reference_image'])
                if not ref_path.is_absolute():
                    ref_path = file_path.parent / ref_path
                scene_data['reference_image'] = ref_path
            
            try:
                scene = Scene(**scene_data)
                scenes.append(scene)
            except TypeError as e:
                raise ValueError(
                    f"Invalid scene data in {file_path}, scene {scene_data.get('id', '?')}: {str(e)}"
                ) from e
        
        # Create script
        try:
            script = Script(
                title=data['title'],
                language=data['language'],
                scenes=scenes,
                voice=data.get('voice', 'female_us'),
                metadata=data.get('metadata', {})
            )
        except TypeError as e:
            raise ValueError(f"Invalid script data in {file_path}: {str(e)}") from e
        
        self.logger.info(
            f"Successfully parsed script: '{script.title}' "
            f"with {script.get_total_scenes()} scenes"
        )
        
        return script
    
    def validate_reference_images(self, script: Script) -> List[str]:
        """
        Validate that all reference images exist.
        
        Args:
            script: Script object to validate
        
        Returns:
            List of error messages for missing images (empty if all valid)
        """
        errors = []
        
        for scene in script.scenes:
            if scene.reference_image:
                if not scene.reference_image.exists():
                    errors.append(
                        f"Scene {scene.id}: Reference image not found: {scene.reference_image}"
                    )
                elif not scene.reference_image.is_file():
                    errors.append(
                        f"Scene {scene.id}: Reference image is not a file: {scene.reference_image}"
                    )
                else:
                    # Check if it's a supported image format
                    supported_formats = {'.jpg', '.jpeg', '.png', '.webp'}
                    if scene.reference_image.suffix.lower() not in supported_formats:
                        errors.append(
                            f"Scene {scene.id}: Unsupported image format: {scene.reference_image.suffix}. "
                            f"Supported: {', '.join(supported_formats)}"
                        )
        
        return errors
