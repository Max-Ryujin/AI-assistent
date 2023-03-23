# let the user choose between --no-console and normal
set /p console=Do you want to build with console? (y/n)
if %console% == y (
    pyinstaller --add-data "c:\users\maxka\appdata\local\packages\pythonsoftwarefoundation.python.3.10_qbz5n2kfra8p0\localcache\local-packages\python310\site-packages/customtkinter;customtkinter/" ".\Assistent.py"
) else (
    pyinstaller --noconsole --add-data "c:\users\maxka\appdata\local\packages\pythonsoftwarefoundation.python.3.10_qbz5n2kfra8p0\localcache\local-packages\python310\site-packages/customtkinter;customtkinter/" ".\Assistent.py"
)