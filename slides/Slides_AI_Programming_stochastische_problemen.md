---
marp: true
theme: ap-theme
paginate: true
---

<!-- _class: title-slide -->

# Stochastische problemen
## Niet meer volledig deterministisch

---

## Stochastische problemen

• Je kan niet exact voorspellen wat een bepaalde zet gaat opleveren
• Denk aan dobbelstenen
• Hoe bepaal je een goede strategie ?
• In tegenstelling tot een determinisch probleem, moet je elke keer herevalueren

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

---

## Partieel observeerbare problemen

• States: je hebt nu een ‘belief’-state space, die niet noodzakelijk overeenkomt met de realiteit
• Initiële state
• Acties:
• Als een illegale zet niets uithaalt, dan kan je de unie nemen van alle acties op de belief states
• Transitie
• Eigenlijk kan je dit probleem ook omzetten in een tree, alleen zijn er nu veel meer verschillende mogelijkheden: bij elke zet van de tegenspeler moet de ‘belief’-state space worden bijgewerkt
