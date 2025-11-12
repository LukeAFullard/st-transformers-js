import base64
from typing import Union, Tuple, Optional

def _get_mime_type(data: bytes) -> Optional[str]:
    """
    Get the MIME type of a byte string using magic numbers.
    """
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if data.startswith(b'\xff\xd8'):
        return 'image/jpeg'
    if data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
        return 'image/gif'
    if data.startswith(b'BM'):
        return 'image/bmp'
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'
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
        try:
            import magic
            mime_type = magic.from_buffer(inputs, mime=True)
        except Exception:
            mime_type = _get_mime_type(inputs)

        processed_inputs = base64.b64encode(inputs).decode('utf-8')

    return processed_inputs, mime_type
