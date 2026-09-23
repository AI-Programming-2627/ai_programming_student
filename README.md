# AI programming (11-Week Course)

## Bronnen

* Hands-On Machine Learning – Aurélien Géron
* Artificial Intelligence: A Modern Approach – Russell & Norvig

---

## 📁 Projectstructuur

```
.
├── .github/workflows/autograde.yml   # CI/CD: automatisch nakijken
├── grade.py                           # Score calculator
├── requirements.txt                   # pytest
├── README.md                          # Deze handleiding
├── tests/
│   ├── test_week01.py               # Week 1:  Insertion Sort + Floor Cleaning Agent
│   ├── test_week02.py               # Week 2:  Self-Driving Car, BFS, Sliding Puzzle
│   ├── test_week03.py               # Week 3:  Maze + Dijkstra
│   ├── test_week04.py               # Week 4:  TSP Simulated Annealing
│   ├── test_week05.py               # Week 5:  Word Generator (GA) + Knapsack
│   ├── test_week06.py               # Week 6:  TicTacToe (Minimax/Alpha-Beta)
│   ├── test_week07.py               # Week 7:  Othello (Minimax)
│   ├── test_week08.py               # Week 8:  Portfolio Optimization (OSQP)
│   ├── test_week09.py               # Week 9:  Explore vs Exploit (Gittins)
│   ├── test_week10.py               # Week 10: Q-learning (Taxi, CartPole)
│   ├── test_week11.py               # Week 11: Tool-using agents
│   └── __init__.py
│
├── exercises/
│   ├── week01/                       # Week 1 exercises
│   │   └── solution.py
│   ├── week02/                       # Week 2 exercises
│   │   └── solution.py
│   ├── week03/                       # Week 3 exercises
│   │   └── solution.py
│   ├── week04/                       # Week 4 exercises
│   │   └── solution.py
│   ├── week05/                       # Week 5 exercises
│   │   └── solution.py
│   ├── week06/                       # Week 6 exercises
│   │   └── solution.py
│   ├── week07/                       # Week 7 exercises
│   │   └── solution.py
│   ├── week08/                       # Week 8 exercises
│   │   └── solution.py
│   ├── week09/                       # Week 9 exercises
│   │   └── solution.py
│   ├── week10/                       # Week 10 exercises
│   │   └── solution.py
│   └── week11/                       # Week 11 exercises
│       └── solution.py
│
```

---

## 📋 Overzicht setup

In deze handleiding leer je stap voor stap:

1. Hoe je de repository **forkt** (eigen kopie maken)
2. Hoe je **Git instelt op je Windows-machine**
3. Hoe je de **devcontainer opent in VS Code**
4. Hoe je **wijzigingen commit & pusht** naar je eigen fork
5. Hoe je **updates binnenhaalt** van de hoofdbranch

---

## 1. Fork de repository

Een **fork** is je persoonlijke kopie van de repo op GitHub.
Je werkt in je eigen fork, maar kan later updates uit de originele repo (`upstream`) binnenhalen.

1. Ga naar de originele repository in je browser:
   `https://github.com/AI-Programming-2627/ai_programming_student`
2. Klik op **"Fork"** (rechtsboven).
3. Kies je eigen GitHub-account als bestemming.
4. Laat **"Copy the `main` branch only"** aangevinkt en klik **Create fork**.

Je fork staat nu op:
`https://github.com/<JOUW_GEBRUIKERSNAAM>/ai_programming_student`

> **Waarom forken?** Je kan vrij pushen zonder de originele repo te verstoren.
> Via `upstream` haal je later nieuwe oefeningen van de lector binnen.

---

## 2. Git installeren op je Windows-host

```powershell
winget install --id Git.Git -e
```

Of download van https://git-scm.com/download/win (64-bit).

**Check:** `git --version` moet `2.4x.x.windows.1` tonen.

---

## 3. Git configureren

Stel je naam en e-mail in **op Windows** (de devcontainer neemt dit over):

```powershell
git config --global user.name "Jouw Naam"
git config --global user.email "jouw.email@student.com"
```

---

## 4. Authenticatie (eenmalig)

Kies een van deze methodes:

### A — GitHub CLI (aanbevolen)

```powershell
winget install --id GitHub.cli -e
gh auth login
```

Kies: **GitHub.com** > **HTTPS** > **Yes** > log in via browser.

### B — SSH-key

```powershell
type C:\Users\%USERNAME%\.ssh\id_ed25519.pub
```

Voeg de output toe op https://github.com/settings/ssh/new

### C — Personal Access Token

Maak een token aan op https://github.com/settings/tokens (klassiek, scopes: `repo`).
Bewaar het:

```powershell
git config --global credential.helper wincred
```

Bij de eerste push plak je het token.

---

## 5. Devcontainer openen

Clone **je fork** en open in VS Code:

```powershell
git clone https://github.com/<JOUW_GEBRUIKERSNAAM>/AI_Prog_student.git
cd AI_Prog_student
code .
```

VS Code vraagt: **"Reopen in Container?"** → klik **Reopen**.
(Of `F1` → **"Reopen in Container"**)

De container:
- ✅ Trekt `ghcr.io/astral-sh/uv:python3.13-trixie` binnen
- ✅ Installeert Git
- ✅ Voert `uv sync` uit (Python packages)
- ✅ Gebruikt jouw Git-credentials van de host



---

## 6. Werken met Git in de container

```bash
git add .
git commit -m "Beschrijving van wat je veranderd hebt"
git push origin main
```

Je kan ook de VS Code Git UI gebruiken: Source Control-icoon (`Ctrl+Shift+G`).

---

## 7. Updates van de lector binnenhalen

**Eenmalig** — voeg de originele repo toe:

```bash
git remote add upstream https://github.com/AI_Programming-2627/ai_programming_student.git
```

**Periodiek** — haal nieuwe oefeningen binnen:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

Doe dit voor elke les zodat je altijd de laatste versie hebt.

---

## 8. Flow-overzicht

```
1. Fork de originele repo op GitHub
2. Clone JOUW fork lokaal
3. Open folder in VS Code
4. VS Code: "Reopen in Container"
5. Werk aan oefeningen
6. git add / git commit / git push
7. (Periodiek) git merge upstream/main
```

---

## 9. Problemen oplossen

| Probleem | Oplossing |
|---|---|
| `git: not found` in container | `F1` → **"Rebuild Container"** |
| `Permission denied (publickey)` | SSH-key toevoegen aan GitHub (stap 4) |
| `could not read Username` | `gh auth login` op **host** (niet in container) |
| Geen "Reopen" prompt | `F1` → **"Reopen in Container"** |
| Wijzigingen niet zichtbaar | Source Control (`Ctrl+Shift+G`) → bestanden **stage**-en |

