# IoT for SMF 2.0 - ETEC Pilotcase

## Om ETEC 

Ett hållbart tekniskt utbildningscentrum inom elteknik- och automation i Oskarshamn. 

## Projektets mål 

Projektets mål är att utveckla en online-applikation som visualiserar elanvändning i olika delar av byggnaden på ETEC och kvantifierar den i realtid med ett aktuelltpris. Till exempel bör dashboarden visa - "just nu kostar en hissresa på 2 minuter X antal SEK". Det bör också vara möjligt att analysera historiska data för att se vilka elbehov som kostade mest för att hitta sätt att optimera energianvändningen i byggnaden.

## Data - ETEC 

MQTT Server API 

Strukturen är enligt följande:
SITE/BYGGNAD/RUM/FUNKTION/PLACERING/MÄTDATA
 
Exempelvis
ETEC/ETEC/114/WAGO_EDM/D1/AL1
ETEC/CONTAINER/WAGO_EDM/A1D/AL1
ETEC/T1/TEORI/TMP/PT1000

## Data - Elpris API 
Vårt förslag är att använda Elpris API från [Elprisetjustnu.se](https://www.elprisetjustnu.se/elpris-api ) 

