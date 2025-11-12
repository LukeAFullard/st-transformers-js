__version__ = "0.2.0"

# For backward compatibility, the main function is the v1 pipeline
from .v1 import transformers_js_pipeline
from .v1 import transformers_js_pipeline as transformers_js_pipeline_v1
from .v2 import transformers_js_pipeline_v2

__all__ = ["transformers_js_pipeline", "transformers_js_pipeline_v1", "transformers_js_pipeline_v2"]
