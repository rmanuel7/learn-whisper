# [pip](https://packaging.python.org/en/latest/key_projects/#pip)

[pip](https://pip.pypa.io/en/stable/) is the package installer for Python. You can use it to install packages from the Python Package Index and other indexes.

The most popular tool for installing Python packages, and the one included with modern versions of Python.

It provides the essential core features for finding, downloading, and installing packages from PyPI and other Python package indexes, and can be incorporated into a wide range of development workflows via its command-line interface (CLI).

## [Getting Started](https://pip.pypa.io/en/stable/getting-started/)

To get started with using pip, you should install Python on your system.

```coffeescript
python --version
# Python 3.N.N
python -m pip --version
# pip X.Y.Z from ... (python 3.N.N)
```

> [!NOTE]
> Run [`python get-pip.py`](https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-pip-setuptools-and-wheel-are-up-to-date). This will install or upgrade pip. Additionally, it will install Setuptools and wheel if they're not installed already.
> 
> ```coffeescript
> python3 -m pip install --upgrade pip setuptools wheel
> ```


## How to install pip for python 3 in ubuntu?

### [Installing pip with Linux Package Managers](https://packaging.python.org/en/latest/guides/installing-using-linux-tools/)

*   Step 1: Updating the package list using the following command:

```coffeescript
sudo apt update
```

*   Step 2: Use the following command to install pip for Python 3:

```coffeescript
sudo apt install python3-pip
```


*   Step 3: Once the installation is complete, verify the installation by checking the pip version:

```coffeescript
pip3 --version
```

## [Install a package](https://pip.pypa.io/en/stable/getting-started/#install-a-package)

```coffeescript
python -m pip install sampleproject
# [...]
# Successfully installed sampleproject
```
