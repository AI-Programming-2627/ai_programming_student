# Student Setup Guide — AI Programming

## 📋 Overzicht

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
   `https://github.com/brunohermanap/AI_Prog_student`
2. Klik op **"Fork"** (rechtsboven).
3. Kies je eigen GitHub-account als bestemming.
4. Laat **"Copy the `main` branch only"** aangevinkt en klik **Create fork**.

Je fork staat nu op:
`https://github.com/<JOUW_GEBRUIKERSNAAM>/AI_Prog_student`

> **Waarom forken?** Je kan vrij pushen zonder de originele repo te verstoren.
> Via `upstream` haal je later nieuwe oefeningen van de docent binnen.

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

## 7. Updates van de docent binnenhalen

**Eenmalig** — voeg de originele repo toe:

```bash
git remote add upstream https://github.com/brunohermanap/AI_Prog_student.git
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