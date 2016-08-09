# OSVR-Blender
> Maintained at <https://github.com/BlendOSVR/OSVR-Blender>
>
> For details, see <http://osvr.github.io>
>
> For support, see <http://support.osvr.com>

## Python Binding for OSVR - "OSVR-Python"
The Blender integration is based on the [OSVR-Python][] Python binding for OSVR, which is maintained in a separate repository. That code is entirely Blender-independent so it can be used in other applications/frameworks.

[OSVR-Python]: https://github.com/BlendOSVR/OSVR-Python

## OSVR Blender integration
We are currently maintaining support for Blender 2.76 and Python 3.x in this tree.

Blender integration is accomplished via add-ons. OSVR-Blender-addon is the main component of OSVR, which starts and shuts down ClientContext. All the other add-ons are for adding functionality to game objects: they add a sensor and a Python controller. However, Blender does not allow links and specifying the Python module to use for the Python controller, so these must occur for any functionality to happen.
osvrClientKit.dll, osvrClient.dll, osvrUtil.dll, and osvrCommon.dll must be accessible via the Blender executable. Currently the only filepath supported is where the dlls are in the same folder as the Blender executable.

Note that if you're looking at the source, you'll need to download and import the Pythonic-OSVR project artifacts.

## License
This project: Licensed under the Apache License, Version 2.0.
