# Suggesties voor verbetering

## Typfout in .clinerules/general.md
- `.clinerules/general.md` regel 8: "devcobtainer" moet "devcontainer" zijn

## Devcontainer-omgeving
- Deze repository gebruikt een devcontainer (zie `.devcontainer/` en `student-setup.md`)
- De `harness/run_tests.sh` werkt binnen de container; lokaal op Windows zonder container
  kan de harness niet direct gerund worden
- Alle code moet binnen de container gerund worden, niet op de host

## Bestaande test heeft platform-afhankelijke code
- `exercises_ai_assisted/week01/week_01_test.py` gebruikt `signal.SIGALRM` (Unix-only)
- Dit werkt niet in de Windows-host-omgeving
- Bij herschrijven een cross-platform time-out gebruiken (bv. `threading.Timer` of `pytest-timeout`)

## Skills
- `.clinerules/skills.md` bevat de herbruikbare skill "create testset oefeningen"
