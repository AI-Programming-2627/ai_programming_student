---
marp: true
theme: ap-theme
paginate: true
---

<!-- _class: title-slide -->

# Iets complexere problemen

• Tot nu toe hebben we ons beperkt tot deterministische, volledig observeerbare problemen.
• In dit hoofdstuk gaan we dit lichtjes uitbreiden om meer realistische problemen op te lossen
• We gaan nu kijken naar zoekalgoritmes waarbij enkel de eindoplossing telt, niet zozeer het pad naar die oplossing

---

## Local search

• Local search gebruikt minder geheugen, het slaat geen informatie op
• Is niet systematisch
• Vindt vaak wel een goede oplossing, zelfs in grote zoekruimtes
• De kunst is om niet in een lokaal minimum vast komen te zitten
• Hieronder hebben we bijvoorbeeld een kostfunctie. Je wil het punt vinden met minimale kost voor je probleem

---

## Verband tussen ‘zoeken’ en optimaliseren

• Een ‘zoekprobleem’ kan je vaak herfomuleren naar een optimalisatieprobleem
• Hiervoor moet je dan een goede performance metric hebben (P uit
PEAS) – ook wel kostfunctie genoemd
• De oplossing van je zoektocht is dan het minimaliseren van die functie

---

## Voorbeeld van kostfuncties

• De meest gebruikte kostfunctie is de zogenaamde
‘Euclidische afstand’, of het kwadraat ervan
• ଵ
ଶ, …, ௡
ଵ
ଶ, …, ௡
௜
௜ଶ
௡
௜ୀଵ
Dit is niets meer of minder dan de ‘afstand in vogelvlucht’ tussen die punten
Vaak wordt om berekening te versimpelen de vierkantswortel weggelaten. Dit concept komt vaak terug, onder andere in Machine Learning scoringsmetrieken zoals Mean Squared Error
(MSE)

---

## Optimalisatie van functies

• Welk algoritme kennen jullie om de minimum van een functie te zoeken ?
• Hoe werkt dat algoritme ?

---

## Gradient Descent

• Gradient descent is een algoritme om op zoek te gaan naar een minimum.
• Het berekent op elk punt de verschillende partiële afgeleiden en zoekt zo de richting die het meest veelbelovend is voor de volgende stap
• Het zet een stap (met een bepaalde grootte) in de richting.
• Gradient descent werkt dus enkel goed op functies die goed ‘afleidbaar’ zijn
• Er is altijd het risico in een lokaal minimum te blijven steken

---

## Gradient Descent

• Gradient descent is een algoritme om op zoek te gaan naar een minimum.
• Het berekent op elk punt de verschillende partiële afgeleiden en zoekt zo de richting die het meest veelbelovend is voor de volgende stap
• Het zet een stap (met een bepaalde grootte) in de richting.
• Het stopt wanneer er niets meer verandert
• Implementatie
• # Gradient descent x = initial_x converged = False while not converged: y = cost_function(x) grad = gradient(x) new_x = x ‐ learning_rate * grad if np.abs(new_x ‐ x) < convergence_threshold: converged = True x = new_x

---

## Gradient Descent

• Gradient descent is een ‘greedy algorithm’: het kiest op elke stap de op dat moment beste richting, zelfs indien je dan in een lokaal minimum dreigt verzeild te raken
Bij gradient descent moet je vaak een stapgrootte of ‘learning rate’ meegeven

---

## Gradient Descent

• Bij een te hoge learning rate kun je over de oplossing springen. Een lagere learning rate is veiliger, maar duurt langer.
Bovendien kan je nog steeds blijven steken op
• Plateau
• ‘Ridge’, een opeenvolging van lokale minima
Bij gradient descent moet je vaak een stapgrootte of ‘learning rate’ meegeven

---

## Gradient Descent

• (Demo)

---

## Gradient Descent variaties

• Stochastic gradient descent
• Kies een richting, waarbij de kansverdeling van de richting bepaald wordt door de gradiënt
• First-choice gradient descent: indien er veel verschillende states zijn, sample nieuwe vectors totdat er een betere richting is (niet per se optimaal!)
• Random restart – een paar keer opnieuw blijven proberen
• Lokale minima blijven een probleem, omdat gradient descent niet even ‘naar boven durft gaan’ alvorens verder af te dalen
• Je zou, in theorie, in random richtingen kunnen wandelen en uiteindelijk de oplossing vinden. Dit is natuurlijk héél inefficiënt
• Als oplossing is er een ander algoritme, ‘simulated annealing’

---

## Simulated annealing

• Een soort combinatie van gradient descent en ‘willekeurige dingen proberen’
• Het komt erop neer dat we af en toe ‘schudden’ met de situatie om het algoritme de kans te geven naar boven te gaan
• Hoe verder in het algoritme, hoe minder hard we schudden
‘Annealing’ is in de metaalbewerking een techniek om metaal op te warmen (verhogen) en vervolgens af te koelen om het materiaal sterker te maken

---

## Simulated annealing

• Pseudocode , E is de te minimaliseren functie
• Startwaarde s = s0
• For k = 0 tot kmax:
• T = temperature( 1 - (k+1)/kmax )
• Kies aan random state vanuit s: snew ← valid_state(s)
• Als E(snew) < E(s)
• s ← snew
• Else If P(E(s), E(snew), T) ≥ random(0, 1):
• s ← snew
• Als E(sbest) > E(s): sbest ← s
• Output: de finale staat s
We gaan ‘soms’ toelaten de verkeerde richting uit te wandelen. Die ‘soms’ is gecapteerd in de kansfunctie P, waarbij de kans kleiner wordt ,naarmate de temperatuur T afneemt

---

## Simulated annealing

• Simulated annealing is historisch erg belangrijk
• Het was in de jaren 80 dé techniek om te weten hoe je optimaal circuits op borden moest ordenen – het zogenaamde Very Large Scale
Integration layout probleem voor integrated circuits (ICs) op een chip. Het heeft bijgedragen aan de chipontwikkeling voor tientallen jaren

---

## In puzzels & spellen

• vaak geen continue, maar een discrete functie
• Een ‘stapfunctie’
• Gradient descent is dan helaas niet bruikbaar, want deze functies zijn niet afleidbaar
• In dat geval kun je van het typisch eindig aantal stappen, de beste optie nemen
• Hebben we al eens gedaan voor de schuifpuzzel.

---

## Stochastische problemen

Niet meer volledig deterministisch

---

## Stochastische problemen

• Je kan niet exact voorspellen wat een bepaalde zet gaat opleveren
• Denk aan dobbelstenen
• Hoe bepaal je een goede strategie ?
• In tegenstelling tot een determinisch probleem, moet je elke keer herevalueren
HB0

---

## Slide 93

HB0
Note to self: dat kan verder worden uitgewerkt AIMA p140 ev
Herman Bruno, 2023-10-18T12:58:27.014

---

## Niet-deterministische problemen

• Hier heb je niet alles onder controle
• Denk aan een het trekken van een kaart, of een uitkomst afhankelijk van een dobbelsteen
• Je moet dan in je strategie als-dan redeneringen opbouwen
• Een oplossing is dan niet meer een pad, maar een oplossing is een tree met beslissingen afhankelijk van de state

---

## Niet-deterministische problemen

• Voorbeeld:
• Een automatische bladverzamelaar in de herfst weet niet op voorhand of er tijdens de klus nog bladeren kunnen bijvallen. Er moet dus af en toe gekeken worden of bepaalde stukken opnieuw moeten worden opgeruimd
• Een oplossing is dan niet meer een pad, maar een oplossing is een tree met beslissingen afhankelijk van de state
• In deze tree zijn er naast de beslissingen van de agent, ook mogelijke kans-acties
• Dit zijn typisch AND-OR- zoektrees,
• AND: kanselementen
• OR: beslissingen agent

---

## Niet-deterministische problemen

• Voorbeeld:
• Een automatische bladverzamelaar in de herfst weet niet op voorhand of er tijdens de klus nog bladeren kunnen bijvallen. Er moet dus af en toe gekeken worden of bepaalde stukken opnieuw moeten worden opgeruimd
• Een oplossing is dan niet meer een pad, maar een oplossing is een tree met beslissingen afhankelijk van de state
Vallen er blaadjes?
Robot voert actie uit

---

## Partieel observeerbare problemen

• States: je hebt nu een ‘belief’-state space, die niet noodzakelijk overeenkomt met de realiteit
• Initiële state
• Acties:
• Als een illegale zet niets uithaalt, dan kan je de unie nemen van alle acties op de belief states
• Transitie
• De agent kan nu niet alles zien, en moet deels blind navigeren: hij moet meerdere states in rekening nemen
HB0

---

## Slide 97

HB0
AIMA p144 ev
Herman Bruno, 2023-10-18T12:58:43.312

---

## Partieel observeerbare problemen

• States: je hebt nu een ‘belief’-state space, die niet noodzakelijk overeenkomt met de realiteit
• Initiële state
• Acties:
• Als een illegale zet niets uithaalt, dan kan je de unie nemen van alle acties op de belief states
• Transitie
• Eigenlijk kan je dit probleem omzetten in een
