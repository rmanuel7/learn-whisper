# [venv](https://packaging.python.org/en/latest/key_projects/#venv)

A package in the Python Standard Library (starting with Python 3.3) for creating Virtual Environments. For more information, see the section on Creating Virtual Environments.

The [venv module](https://docs.python.org/3/library/venv.html) supports creating lightweight “virtual environments”, each with their own independent set of Python packages installed in their site directories. A virtual environment is created on top of an existing Python installation, known as the virtual environment’s “base” Python, and by default is isolated from the packages in the base environment, so that only those explicitly installed in the virtual environment are available. See Virtual Environments and site’s virtual environments documentation for more information.


## [Creating virtual environments](https://docs.python.org/3/library/venv.html#creating-virtual-environments)

Virtual environments are created by executing the venv module:

```coffeescript
python -m venv "/path/to/new/virtual/environment"
```

## [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

This guide discusses how to create and activate a virtual environment using the standard library’s virtual environment tool venv and install packages. The guide covers how to:

*   Create and activate a virtual environment

*   Prepare pip

*   Install packages into a virtual environment using the pip command

*   Use and create a requirements file

