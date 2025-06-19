import subprocess
import os

def get_project_root():
    """Gets the project root directory, which is one level up from this script."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def transcribe_audio(audio_path: str, model_name: str = "medium", progress_callback=None) -> (str, str):
    """
    Transcribes the given audio file using WhisperKit CLI.

    Args:
        audio_path: The absolute path to the audio file.
        model_name: The name of the WhisperKit model to use (e.g., "large-v3").
        progress_callback: A function to call with progress updates.

    Returns:
        A tuple containing the transcription text and any error message.
        If transcription is successful, the error message is None.
        If it fails, the transcription is None.
    """
    project_root = get_project_root()
    # The model folder name in the repo is like `openai_whisper-large-v3`
    model_folder_name = f"openai_whisper-{model_name}"
    model_path = os.path.join("Models", "whisperkit-coreml", model_folder_name)
    
    full_model_path = os.path.join(project_root, model_path)

    if not os.path.exists(full_model_path):
        error_msg = f"Model '{model_name}' not found at expected path: {full_model_path}\\n\\nPlease make sure you have downloaded the model using 'make download-model MODEL={model_name}' from the root of the WhisperKit project."
        return None, error_msg

    if not os.path.exists(audio_path):
        return None, f"Audio file not found at {audio_path}"

    command = [
        "swift", "run", "whisperkit-cli", "transcribe",
        "--model-path", model_path,
        "--audio-path", audio_path,
        "--verbose"
    ]

    try:
        if progress_callback:
            progress_callback("Transcribing... This may take a moment.")

        # Execute the command from the project root
        process = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )

        # Find the transcription in the output.
        # Based on the CLI code, the final transcription is printed last.
        output = process.stdout.strip()
        
        # A simple way to find the transcription is to look for the last non-empty line
        # that doesn't look like a debug or info message.
        # A more robust solution might be needed if CLI output changes.
        lines = [line for line in output.split('\\n') if line.strip()]
        transcription = lines[-1] if lines else ""

        if "Error:" in transcription: # Simple error check
            return None, transcription

        return transcription, None
    except subprocess.CalledProcessError as e:
        error_message = f"WhisperKit CLI failed with exit code {e.returncode}.\\n"
        error_message += f"Stderr: {e.stderr}\\n"
        error_message += f"Stdout: {e.stdout}"
        return None, error_message
    except FileNotFoundError:
        return None, "Error: 'swift' command not found. Please ensure Xcode and its command line tools are installed and you are on macOS."
    except Exception as e:
        return None, f"An unexpected error occurred: {e}" 