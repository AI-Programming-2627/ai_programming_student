---
marp: true
theme: ap-theme
paginate: true
---

<!-- _class: title-slide -->

# Q-learning

---

## Late rewards maken leren moeilijker

• Sommige problemen hebben pas een beloning helemaal op het einde
• Mountain car krijgt enkel punten helemaal boven bij de vlag
• Een taxichauffeur wordt pas betaald op de bestemming
• Een diploma krijg je pas na 180 studenten en veel bloed, zweet en tranen
• Hoe kan een agent dan toch onderweg iets leren
?

---

## Late rewards maken leren moeilijker

• Sommige problemen hebben pas een beloning helemaal op het einde
• Mountain car krijgt enkel punten helemaal boven bij de vlag
• Een taxichauffeur wordt pas betaald op de bestemming
• Een diploma krijg je pas na 180 studenten en veel bloed, zweet en tranen
• Hoe kan een agent dan toch onderweg iets leren
?
• We kunnen net zoals in explore vs exploit kijken naar discounted rewards in de toekomst

---

## Een leeromgeving

• Agents
• States
• Acties, met bijbehorende…
• Rewards
• Episodes: een episode eindigt wanneer er een terminal state wordt bereikt

---

## Strategie

Intuitie
• Later een doel bereiken levert minder punten op (discounting)
• Per stap hebben we een idee van de ‘verwachte rewards’ voor elke actie
• Dit gaan we bijhouden in een tabel, de Q-tabel
• Deze tabel gaan we voortdurend updaten op basis van nieuwe informatie
Wiskunde
• Een q-tabel heeft voor elke combinatie (observatie, actie) een bepaalde waarde die de waarde van die actie voorstelt
• Op basis van een bepaalde observatie kan je dus inschatten wat, op basis van de op dat moment gekende informatie, de beste actie is
• Als je een actie doet, en je krijgt feedback (reward / penalty) dan kan je elke keer de tabel lichtjes bijstellen

---

## Strategie

Startfase
• We starten met een q- tabel die voor elke observatie en elke actie een neutrale verwachting heeft
Q-tabel
Ac 5
Ac 4
Ac 3
AC 2
Actie
1
Q‐ tabel
0
0
0
0
0
Obser vatie
1
0
0
0
0
0
Ob 2
0
0
0
0
0
Ob 3
0
0
0
0
0
Ob 4
0
0
0
0
0
Ob 5

---

## Strategie

Epsilon : explore vs exploit
• In elke fase gaan we met een vooraf bepaalde kanse epsilon kijken of we explore of exploit gaan doen
• Explore: kies een random actie
• Exploit: kies voor deze observatie de actie met de grootste verwachte Q-waarde
• Bijvoorbeeld: bij een Q-tabel zoals hiernaast: voor obs 2 zou actie 4 worden gekozen, voor ob 3 zou actie 5 worden gekozen, voor al de rest geen voorkeur.
Q-tabel
Ac 5
Ac 4
Ac 3
AC 2
Actie
1
Q‐ tabel
0
0
0
0
0
Obser vatie
1
0
5
0
4
0
Ob 2
5
‐20
‐2
2
1
Ob 3
0
0
0
0
0
Ob 4
0
0
0
0
0
Ob 5

---

## Strategie

Update fase
• Na de uitvoering van een keuze, krijg je van je omgeving een reward
• Deze reward gaan we terug in de tabel invoeren, via een updateformule. De exacte formule vindt je terug in de RL_voorbeelden.
Q-tabel
Ac 5
Ac 4
Ac 3
AC 2
Actie
1
Q‐ tabel
0
0
0
0
0
Obser vatie
1
0
5
0
4
0
Ob 2
5
‐20
‐2
2
1
Ob 3
0
0
0
0
0
Ob 4
0
0
0
0
0
Ob 5

---

## Voorbeeld: een taxichauffeur

• Penalties:
• Elke move kost -1
• Het fout afzetten van een passagier kost zeer veel
• Dit gaan we bekijken in de notebook.

---

## Reinforcement learning en zelfrijdende auto

---

## Q-learning in de praktijk

• Zie notebook RL_voorbeelden en taxi_notebook.
