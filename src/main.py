"""
DoodleEduMaker - Main Application Entry Point

This is the primary entry point for the DoodleEduMaker application.
It can be run in CLI mode or GUI mode.
"""

import argparse
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('doodleedumaker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main_cli(args):
    """Run in CLI mode"""
    from core.script_parser import ScriptParser
    from core.doodle_generator import DoodleGenerator, GenerationConfig, QualityPreset
    from core.tts_engine import TTSEngine
    
    logger.info("DoodleEduMaker starting in CLI mode")
    logger.info(f"Script: {args.input}")
    
    try:
        # Parse script
        logger.info("Parsing script...")
        parser = ScriptParser()
        script = parser.parse_file(args.input)
        logger.info(f"Loaded script: '{script.title}' with {script.get_total_scenes()} scenes")
        
        # Validate reference images
        errors = parser.validate_reference_images(script)
        if errors:
            for error in errors:
                logger.warning(error)
        
        # Initialize generators
        logger.info("Initializing AI models...")
        
        # Set quality preset
        quality_map = {
            'fast': QualityPreset.FAST,
            'balanced': QualityPreset.BALANCED,
            'high': QualityPreset.HIGH
        }
        quality = quality_map.get(args.quality, QualityPreset.BALANCED)
        
        doodle_gen = DoodleGenerator(config=GenerationConfig(quality_preset=quality))
        tts_engine = TTSEngine()
        
        # Generate doodles and audio for each scene
        for scene in script.scenes:
            logger.info(f"Processing scene {scene.id}...")
            
            # Generate doodle
            logger.info(f"  - Generating doodle...")
            image = doodle_gen.generate(
                prompt=scene.visual_description,
                reference_image=scene.reference_image,
                scene_id=scene.id
            )
            logger.info(f"  - Doodle generated: {image.size}")
            
            # Generate narration
            logger.info(f"  - Generating narration...")
            audio_path = tts_engine.generate(
                text=scene.narration,
                scene_id=scene.id
            )
            logger.info(f"  - Narration generated: {audio_path}")
        
        logger.info("All scenes processed successfully!")
        logger.info("Video assembly would happen here (not yet implemented)")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error processing script: {e}", exc_info=True)
        return 1


def main_gui():
    """Run in GUI mode"""
    logger.info("DoodleEduMaker starting in GUI mode")
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        
        # Note: GUI implementation would be imported here
        # from ui.main_window import MainWindow
        
        app = QApplication(sys.argv)
        app.setApplicationName("DoodleEduMaker")
        app.setOrganizationName("DoodleEduMaker Contributors")
        
        logger.info("GUI not yet implemented - please use CLI mode for now")
        logger.info("Example: python src/main.py --input examples/water_conservation.json")
        
        # window = MainWindow()
        # window.show()
        
        return 0  # app.exec()
        
    except ImportError as e:
        logger.error(f"GUI dependencies not available: {e}")
        logger.info("Please install GUI dependencies: pip install PySide6")
        return 1
    except Exception as e:
        logger.error(f"Error starting GUI: {e}", exc_info=True)
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="DoodleEduMaker - AI-Powered Educational Video Creator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run in GUI mode (default)
  python src/main.py
  
  # Generate video from script (CLI)
  python src/main.py --input examples/water_conservation.json
  
  # Generate with specific quality preset
  python src/main.py --input script.json --quality high
  
  # Preview mode (generate doodles only)
  python src/main.py --input script.json --preview
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=Path,
        help='Input script file (JSON or Markdown)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output video file (default: auto-generated from title)'
    )
    
    parser.add_argument(
        '--quality', '-q',
        choices=['fast', 'balanced', 'high'],
        default='balanced',
        help='Quality preset (default: balanced)'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview mode: generate doodles only, no video assembly'
    )
    
    parser.add_argument(
        '--no-gui',
        action='store_true',
        help='Force CLI mode (no GUI)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Determine mode
    if args.input or args.no_gui:
        # CLI mode
        if not args.input:
            parser.error("--input required in CLI mode")
        return main_cli(args)
    else:
        # GUI mode
        return main_gui()


if __name__ == "__main__":
    sys.exit(main())
