"""Pythonic wrapper to the OSVR ClientKit C API

This module provides an object-oriented wrapper for the ClientKit portion of the C API. 
It uses ctypes to make the functions callable in C. The module reorganizes the C functions to
to support Context, Display, and Interface objects.

"""
__date__ = "6 December 2015"
__credits__="""
Austin Needham
Sarah Rust
Adam Wang
"""