# To run this script directly, run this in an elevated admin PowerShell prompt:
#     Invoke-WebRequest -UseBasicParsing https://raw.githubusercontent.com/Bugs-Zero/HumanDoTask/master/machine-setup.ps1 | Invoke-Expression

# This script is intended to setup a dev machine from scratch. Very useful for setting up a EC2 instance for mobbing.
#


Invoke-WebRequest -useb https://raw.githubusercontent.com/JayBazuzi/machine-setup/main/windows.ps1 | Invoke-Expression
Invoke-WebRequest -useb https://raw.githubusercontent.com/JayBazuzi/machine-setup/main/python-pycharm.ps1 | Invoke-Expression


& "C:\Program Files\Git\cmd\git.exe" clone https://github.com/Bugs-Zero/HumanDoTask.git C:\Code\HumanDoTask

