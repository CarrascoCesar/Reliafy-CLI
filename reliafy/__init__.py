"""
Reliafy CLI - Command-line interface for reliability analysis and design using the Reliafy API.
Copyright (c) 2025 Cesar Carrasco. All rights reserved.
"""

__version__ = "0.1.3"
__author__ = "Cesar Carrasco"
__email__ = "reliafy.app@gmail.com"  # Optional
__description__ = "Command-line interface for reliability analysis and design using the Reliafy API"

# You can also expose main components if needed
from reliafy.reliafy import app as main

__all__ = ["main", "__version__"]
