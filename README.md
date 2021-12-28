<p align="center">
  <img src="https://github.com/tbrus/install-ifcopenshell-python/blob/master/logo.png?raw=true"/>
</p>

# install-ifcopenshell-python

This package is a "part" of another repo: 
[pyifc](https://github.com/tbrus/pyifc/).
 
[ifcopenshell on github](https://github.com/IfcOpenShell/IfcOpenShell)  
[ifcopenshell website](http://ifcopenshell.org/python)

Unfortunately **ifcopenshell** is not distributed via PyPi. Hence you can get 
error while installing **pyifc**:

```bash
ModuleNotFoundError: No module named 'ifcopenshell'
```

To address this issue you can use 
[install-ifcopenshell-python](https://github.com/tbrus/install-ifcopenshell-python).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
**install-ifcopenshell-python**.

```bash
pip install install-ifcopenshell-python
```

## Usage

Ifcopenshell is downloaded via hard coded URL (v0.6.0).

No arguments are needed. System, architecture and python version are determined 
automatically. You can simply run:

```bash
python -m install_ifcopenshell_python
```
Notice that here underscores are used, not hyphens.

However, if you would like to, you can determine your own arguments. You can 
run:

```bash
python -m install_ifcopenshell_python -h
```

To produce output:

```bash
usage: install_ifcopenshell_python [-h] [-s {linux,win,macos}] [-a {32,64}] [-v {37,38,39}]

Download ifcopenshell based on platform system, platform architecture and running python version.

optional arguments:
  -h, --help            show this help message and exit
  -s {linux,win,macos}, --system {linux,win,macos}
                        Platform system.
  -a {32,64}, --architecture {32,64}
                        Platform architecture.
  -v {37,38,39}, --python-version {37,38,39}
                        Running python version; string of major and minor version, e.g. '39'. pyifc supports python >=
                        3.7.
```

## References

[1] [Logo](https://github.com/tbrus/install-ifcopenshell-python/blob/master/logo.png) 
is created based on logo of [pyifc](https://github.com/tbrus/pyifc/) 
and logo of [ifcopenshell](http://ifcopenshell.org/python).
