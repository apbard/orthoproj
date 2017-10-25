"""
Orthoproj
"""

from .orthogonal_projection import OrthoProj
try:
    from orthoproj.version import version as __version__
except:
    __version__ = "UNKNOWN"

__all__ = ["OrthoProj"]
