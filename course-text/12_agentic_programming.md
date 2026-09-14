# Hoofdstuk 12: Agentic Programming

## Wat is een Agent?

Een **agent** is een systeem dat:
- Een omgeving **waarneemt**
- **Beslissingen** neemt (acties)
- Een **doel** probeert te bereiken
- Vaak **leert** of zich **aanpast**

```
Perceptie → Beslissing → Actie → Observatie → Herhaal
```

Niet elk algoritme is een agent. BFS of A* alleen = geen agent.

---

## Tool-Using Agents

Een tool-using agent beschikt over meerdere algoritmes en kiest **welk algoritme** best geschikt is.

```python
class ToolAgent:
    def __init__(self):
        self.tools = {
            "bfs": bfs,
            "dfs": dfs,
            "astar": astar,
            "annealing": simulated_annealing
        }
    
    def choose_tool(self, problem):
        if problem.size < 10:
            return "bfs"
        return "astar"
```

De agent kan ook leren via **bandits** (epsilon-greedy) om de beste tool te kiezen.

---

## Self-Improving Agents (RL + Minimax)

Combineer **Q-learning** (leren) met **minimax** (exacte planning):

```python
class SelfImprovingAgent:
    def choose_action(self, state):
        if self.is_critical_state(state):
            return self.use_minimax(state)
        else:
            return self.use_qlearning(state)
```

| Methode | Sterkte |
|---------|--------|
| Q-learning | Lange termijn leren |
| Minimax | Perfecte beslissingen (kleine states) |

---

## LLM-Based Agents

Een LLM-agent gebruikt een **taalmodel** als redeneercomponent.

```python
def llm_agent(state, prompt_template):
    prompt = f"""State: {state}
    Beschikbare acties: [links, rechts, stop]
    Doel: bereik het doel
    Gedachte:
    Actie:"""
    response = llm(prompt)
    return parse_action(response)
```

De intelligentie zit in de **prompt**, niet in de code.

---

## Evolutionaire Agents

In plaats van een agent te programmeren, **evolueren** we er een:

```python
weights = {
    "win": 8.2,
    "block": 5.1,
    "center": 1.7
}
# Deze gewichten bepalen de beslissingen
# Goede strategie -> meer nakomelingen
```

---

## Vergelijking

| Type | Sterkte | Zwakte |
|------|---------|--------|
| Tool agent | Efficiënt, duidelijk | Weinig flexibel |
| Self-improving | Leert goed | Training nodig |
| LLM agent | Flexibel | Onbetrouwbaar |
| Evolutionair | Ontdekt strategie | Traag |

## Belangrijkste Inzichten

1. **Agents combineren technieken**
2. Beslissingen op **meerdere niveaus**
3. Geen enkele methode is 'beste'
4. **Ontwerp** is cruciaal

De vraag verschuift van "welk algoritme is correct?" naar "hoe ontwerp je een systeem dat zelfstandig goede keuzes maakt?".
