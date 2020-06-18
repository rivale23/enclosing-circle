To run the script, it is assumed that  python 3 and pip are installed in the system
1) Open a command line and go to the folder where the start.py file is located
2) To setup the environment, install the virtual environment running the following command:
    python -m pip install --user virtualenv -i https://pypi.python.org/simple
3) Create the environment with the following command:
    python -m venv env
4) Activate the environment:
    windows: .\env\Scripts\activate.bat
    linux: source env/bin/activate
5) Install the required dependencies:
    python -m pip install numpy -i https://pypi.python.org/simple
    python -m pip install matplotlib -i https://pypi.python.org/simple
    python -m pip install pandas -i https://pypi.python.org/simple
6) Run the script:
    python start.py


For windows, two bat files are provided:
    setup.bat runs the steps 2-4
    install_packages.bat runs the step
