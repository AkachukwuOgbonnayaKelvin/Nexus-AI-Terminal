# -*- coding: utf-8 -*-
"""
ACP Architecture OS
Version 2.0.0
"""

__version__ = "2.0.0"
__author__ = "Nexus AI Terminal Team"

from acp.core.architecture_os import ArchitectureOS
from acp.compilers import *
from acp.output import Visualizer

__all__ = [
    'ArchitectureOS',
    'Visualizer',
    'IdentityCompiler',
    'ArchitectureCompiler',
    'DependencyCompiler',
    'RuntimeCompiler',
    'PlatformCompiler'
]
