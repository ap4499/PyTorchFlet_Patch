Very rough and ready code that shows how a Flet Build runtime cache is patched using files from a seperate cx_freeze.

the issue is that Flet Build, at time of writing, removes files such as bin folders, and .py + .pyc. These then need to be placed in the applications runtime cache, which is what this code achieves.

The code should be run before any imports for related libraries (Pytorch in this case)
