# Week 11 — Oefeningen: LLM-gestuurde Agents

## Leerdoelen
- Je begrijpt hoe een **LLM-agent** werkt (prompt → actie).
- Je experimenteert met **prompt engineering**.
- Je combineert LLM-reasoning met tools.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | LLM-agent uitproberen | 30 min |
| 2 | Prompt engineering | 30 min |

---

## Oefening 1: LLM-agent uitproberen

Open `llm_agent_start.py`. De code in `agents/agentic_reasoning/` toont een agent die een LLM gebruikt om puzzels op te lossen:

- `tools.py`: simpele acties (`minus1`, `minus3`, `div2`)
- `agent.py`: de agent met `build_prompt()`, `parse_output()`, en `run()`.
- `llm.py`: wrapper voor OpenRouter API.

**Opdracht:** Voer de code uit (je hebt een `OPENROUTER_API_KEY` nodig).  
Zie de uitleg in `agents/agentic_reasoning/explanation.md` voor setup.

## Oefening 2: Prompt engineering

Pas de **prompt** in `build_prompt()` aan:

1. Voeg een doel toe: "minimaliseer het aantal stappen".
2. Voeg **geheugen** toe: vermeld in de prompt dat de agent geen state mag herhalen.
3. Test verschillende prompts:

| Prompt | Succesratio | Gem. stappen |
|--------|-------------|--------------|
| Origineel | ... | ... |
| + minimaliseer stappen | ... | ... |
| + vermijd herhaling | ... | ... |
| Beide | ... | ... |

## Oefening 3 (Uitbreiding): Bouw je eigen agent

Ontwerp een tool-using agent die zelf kiest welk algoritme te gebruiken:

```python
class ToolAgent:
    def __init__(self):
        self.tools = {"bfs": bfs, "dfs": dfs, "astar": astar}
    
    def choose_tool(self, problem):
        # Leer met epsilon-greedy welke tool het best is
        pass
```

Zie `agents/oefeningen/opgave.md` voor meer uitbreidingen.

---

## Klaar?
- Dit is de laatste week. Commit alles en zorg dat je repository up-to-date is.