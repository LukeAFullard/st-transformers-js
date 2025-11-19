import base64
from typing import Union, Tuple, Optional

def _get_mime_type_from_magic_numbers(data: bytes) -> Optional[str]:
    """
    Fallback MIME type detection using magic numbers for common image formats.
    """
    if len(data) >= 8 and data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if len(data) >= 2 and data.startswith(b'\xff\xd8'):
        return 'image/jpeg'
    if len(data) >= 6 and (data.startswith(b'GIF87a') or data.startswith(b'GIF89a')):
        return 'image/gif'
    if len(data) >= 2 and data.startswith(b'BM'):
        return 'image/bmp'
    if len(data) >= 12 and data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'
    if len(data) >= 4 and (data.startswith(b'\x49\x49\x2A\x00') or data.startswith(b'\x4D\x4D\x00\x2A')):
        return 'image/tiff'
    if len(data) >= 4 and data.startswith(b'\x00\x00\x01\x00'):
        return 'image/x-icon'
    return None

def _get_mime_type_with_magic(data: bytes) -> Optional[str]:
    """
    Try to get MIME type using python-magic, handling import errors gracefully.
    """
    try:
        import magic
        return magic.from_buffer(data, mime=True)
    except ImportError:
        # python-magic is not installed
        return None
    except Exception as e:
        # Other unexpected errors from the magic library
        print(f"An error occurred with python-magic: {e}")
        return None

def process_inputs(inputs: Union[str, bytes, dict]) -> Tuple[Union[str, dict], Optional[str]]:
    """
    Process the inputs for the component.
    """
    if not isinstance(inputs, (str, bytes, dict)):
        raise TypeError(f"Input type not supported: {type(inputs)}. Must be str, bytes, or dict.")

    processed_inputs = inputs
    mime_type = None

    if isinstance(inputs, bytes):
        # Try python-magic first
        mime_type = _get_mime_type_with_magic(inputs)
        # Fallback to magic numbers if python-magic is not available or fails
        if not mime_type:
            mime_type = _get_mime_type_from_magic_numbers(inputs)

        processed_inputs = base64.b64encode(inputs).decode('utf-8')

    return processed_inputs, mime_type
