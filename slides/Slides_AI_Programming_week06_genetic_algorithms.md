---
marp: true
theme: ap-theme
paginate: true
---

<!-- _class: title-slide -->

# Genetische algoritmes
## Algoritmes die zichzelf veranderen

---

![](images/Slides_ML_Algorithms_genetic_algorithms_p02_img001.jpeg)

## Introductie – Survival of the fittest

- Genetische algoritmes zijn algoritmes die, zoals in biologie, langzaam kunnen veranderen
- Er is dus een kanscomponent aan verbonden
- Zijn heel krachtig en efficiëntier dan pure random zoekalgoritmes of bruteforce zoekalgoritmes (zie AI
Programming)
- Ze worden vaak gebruikt voor optimalisatieproblemen

---

## Algemene werking

- Het algoritme wordt elke stap aangepast:
- Genereer een set van random items
- Kies daaruit de beste
- Kruis deze met elkaar:
Nu zijn er ‘children’ of ‘offspring’ uit deze ‘parents’
- Muteer de nieuwe generatie ‘offsprings’
- Herhaal deze stappen tot aan termination
- Een oplossing voor het optimalisatieprobleem is dus een ‘individu’ in deze populatie

---

## Initiële populatie

- De initiële populatie wordt willekeurig gekozen
- Ofwel volledig willekeurig
- Ofwel, als er al enige kennis is over het probleem, volgens een heuristiek of ‘educated guess’

![h:400](images/Slides_ML_Algorithms_genetic_algorithms_p04_img001.png)

Bron afbeelding: https://towardsai.net/p/l/a‐ gentle‐introduction‐to‐genetic‐algorithms

---

## Fitness van een individu

- Om in te schatten hoe goed een oplossing is, hebben we een fitness function nodig
- Op basis hiervan kunnen we de beste individuen (oplossingen) selecteren, en hiermee verder ‘kweken’
- Idealiter zou deze functie aangeven hoe dicht je bij de ideale oplossing zit
- Zoals wel vaker, is er een afweging tussen
    - Een snel berekenbare functie
    - De accuraatheid van deze functie
    - omdat we de exacte oplossing, per definitie, niet hebben

---

## Selectie

- Vervolgens worden individuen gekozen
- Hierbij moeten we twee aspecten afwegen:
- Enerzijds de beste individuen;
- Anderzijds voldoende variatie ! Anders gaan de volgende generaties teveel op mekaar lijken - > niet robuust
- Strategieën voor selectie:
- Fitness proportionate: kans op selectie is evenredig met fitness score
- Tournament selection: in een soort bracketed matchup random individuen vergelijken
- Rankings: hoogste fitness-scores worden geselecteerd

---

## Crossover – volgende generatie

- Twee methodes van crossover:
- Point crossover: zie prentje hiernaast
- Gene-based crossover: elke parent levert 50% van de oplossing

![h:400](images/Slides_ML_Algorithms_genetic_algorithms_p07_img001.jpeg)

---

## Mutatie – volgende generatie

- Lichte wijziging van de nieuwe generatie : dit creëert variatie in de dataset
- De kans op mutatie kan worden vastgelegd in een parameter. Als deze hoog is, ga je eerder naar een randomized algoritme zoals simulated annealing

![h:400](images/Slides_ML_Algorithms_genetic_algorithms_p08_img001.jpeg)

---

## Termination

- Het algoritme eindigt wanneer een individu zodanig fit is, eg zodanig dicht tegen de optimale oplossing, dat we stoppen
- Er kan ook worden beslist na een aantal generaties altijd te stoppen, ongeacht de fitheid.

![](images/Slides_ML_Algorithms_genetic_algorithms_p09_img001.png)

---

## Toepassing van dit idee: evolving code
In mei 2025 publiceerde Deepmind (deel van Google) een whitepaper over een AI gedreven mechanisme dat zelf code schrijft. Het mechanisme is onderliggende sterk gebaseerd op genetic programming, toegepast op de Git-stack van een coding project.

Er ziijn verschillende webartikels geschreven die kort (en wel goed) uitleggen hoe dit in zijn werk gaat, zoals bijvoorbeeld hier: 
- https://towardsdatascience.com/googles-alphaevolve-is-evolving-new-algorithms-and-it-could-be-a-game-changer/


De volledige whitepaper is te lezen op 
- https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf
