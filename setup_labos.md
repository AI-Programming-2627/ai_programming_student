## Setup voor labos ML Algorithms & AI Programming

1. Installeer WSL2 voor Windows(https://learn.microsoft.com/en-us/windows/wsl/install)
    Dit laat toe om met Linux te werken binnen Windows.
2. Installeer Ubuntu op deze WSL (zelfde link)
3. Installeer miniconda in Ubuntu (https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html) - volg de LINUX installer!
    Conda is een packaging systeem voor Python packages. Het zorgt dat de versies van bepaalde packages onderling compatibel blijven. Conda is de standaard om te gebruiken met machine learning. Een andere gekende package manager is pip.
4. Maak per vak een map, dit is je root directory voor dit vak, die ga je openen in Visual Studio Code.
5. zorg dat je VSCode in deze folder staat, en deze folder geopend is in WSL (Reopen folder in WSL kan helpen)
    In VSCode heb je ook een hoop extensies nodig, de voornaamste zijn python, jupyter, remote development. Die kan je links bij de extensies installeren.
6. Creëer een conda omgeving in een VSCode terminal `conda create --name [naam_vak_env]`
7. Activeer de omgeving `conda activate [naam_vak_env]`
8. `conda install ipykernel`
9. Installeer noodzakelijke packages met conda, schrijf regelmatig je environment weg naar een YML file met `conda env export > environment.yml`. Die zou je ook mee inchecken met Git of andere remote repository tool. Check hiervoor de website van de package zelf bijvoorbeeld voor scikit-learn moet je het kanaal conda-forge er expliciet bijzetten: `conda install -c conda-forge scikit-learn`
10. Voor notebooks (.ipynb files), selecteer rechts bovenaan de juiste conda omgeving die je zelf hebt gemaakt om de notebook te gebruiken. Meer info: https://code.visualstudio.com/docs/datascience/jupyter-kernel-management 

### Opzetten van omgeving met Mamba

Mamba is een variant op conda, maar die beter is in het omgaan met grotere omgevingen. 
Meer info op https://mamba.readthedocs.io/en/latest/index.html 

Installatie op de base:
- `conda install -n base conda-libmamba-solver`
- `conda config --set solver libmamba`

In een nieuwe environment:
- `conda create -n mamba-installer`
- `conda install -n mamba-installer conda-libmamba-solver`
- `conda config --set solver libmamba`

Indien je het in een specieke environment wilt installeren:
- `conda install conda-libmamba-solver`
- `conda config --set solver libmamba`
