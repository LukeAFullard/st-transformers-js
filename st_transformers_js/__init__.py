import os
import warnings

__version__ = "0.2.0"

# Verify frontend builds exist
_package_dir = os.path.dirname(os.path.abspath(__file__))

_v1_build_dir = os.path.join(_package_dir, "frontend_v1", "build")
_v1_required_files = ["index.html", "transformers.min.js"]

_v2_build_dir = os.path.join(_package_dir, "frontend_v2", "dist")
_v2_required_files = ["index.html"]

def _verify_build(build_dir: str, required_files: list, version: str) -> bool:
    """Verify that frontend build files exist."""
    if not os.path.exists(build_dir):
        warnings.warn(
            f"Frontend {version} build directory not found at {build_dir}. "
            f"The {version} component will not work. "
            f"Run './build_script.sh' to build frontend assets.",
            RuntimeWarning,
            stacklevel=2
        )
        return False

    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(build_dir, file)):
            missing_files.append(file)

    if missing_files:
        warnings.warn(
            f"Frontend {version} is missing required files: {missing_files}. "
            f"The {version} component may not work correctly. "
            f"Run './build_script.sh' to rebuild frontend assets.",
            RuntimeWarning,
            stacklevel=2
        )
        return False

    return True

# Verify builds on import
_v1_ok = _verify_build(_v1_build_dir, _v1_required_files, "v1")
_v2_ok = _verify_build(_v2_build_dir, _v2_required_files, "v2")

# Import with warnings if builds missing
if _v1_ok:
    from .v1 import transformers_js_pipeline
    from .v1 import transformers_js_pipeline as transformers_js_pipeline_v1
else:
    def transformers_js_pipeline(*args, **kwargs):
        raise RuntimeError(
            "V1 component frontend not built. Run './build_script.sh' first."
        )
    transformers_js_pipeline_v1 = transformers_js_pipeline

if _v2_ok:
    from .v2 import transformers_js_pipeline_v2
else:
    def transformers_js_pipeline_v2(*args, **kwargs):
        raise RuntimeError(
            "V2 component frontend not built. Run './build_script.sh' first."
        )

__all__ = [
    "transformers_js_pipeline",
    "transformers_js_pipeline_v1",
    "transformers_js_pipeline_v2"
]
