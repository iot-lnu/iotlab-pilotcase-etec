# IoT for SMF 2.0 - ETEC Pilotcase

## Om ETEC 

Ett hållbart tekniskt utbildningscentrum inom elteknik- och automation i Oskarshamn. 

## Projektets mål 

Projektets mål är att utveckla en online-applikation som visualiserar elanvändning i olika delar av byggnaden på ETEC och kvantifierar den i realtid med ett aktuelltpris. Till exempel bör dashboarden visa - "just nu kostar en hissresa X antal SEK". Det bör också vara möjligt att analysera historiska data för att se vilka elbehov som kostade mest för att hitta sätt att optimera energianvändningen i byggnaden.

## Data - Elförbrukning

MQTT Server API 

Strukturen är enligt följande:
SITE/BYGGNAD/RUM/FUNKTION/PLACERING/MÄTDATA
 
Exempelvis
- ETEC/ETEC/114/WAGO_EDM/D1/AL1
- ETEC/CONTAINER/WAGO_EDM/A1D/AL1
- ETEC/T1/TEORI/TMP/PT1000

Mätvärden som är tillgänliga i MQQTn just nu:
- Grupp1 - Elpanna
- Grupp 11 - Bergvärme
- Grupp 12 - Ventilation LA1
- Grupp 13 - Hiss
- Grupp 18 - Ventilation LA2
- Grupp 19 - Kyla LA2
  
Utöver dessa mätvärden finns det även data tillgänglig från en funktion som kallas 'Container' samt en central kallad 'A1D'. Elementet av störst intresse är elförbrukning mätt i watt, vilket är representerat av W_TOT värdet, exempel: "ETEC/ETEC/ETEC/114/WAGO_EDM/D1/GR1/W_TOT".

## Data - Elpriser
Vi hämtar realtidspriser i SE4 zonen från Elpris API [Elprisetjustnu.se](https://www.elprisetjustnu.se/elpris-api ). Observera att dessa priser endast är en uppskattning då de inte inkluderar kostnader för eltransport, abonnemang och liknande.


## Data - Temperatur
I MQTT:n finns även mätvärden från två analoga termometrar, dessa representeras som Temp_n (nord) och Temp_s (syd). 

## Implementation

Efter våra initiala experiment, tillgängliga under `"first_pilot"` mappen, har vi beslutat att fortsätta med en **Influx** + **Grafana** stack för detta projekt. Denna lösning levererar en kraftfull kombination för realtidsdataanalys och visualisering av stora datamängder. InfluxDB är särskilt utformad för att lagra tidsserie-data, vilket gör den till en ideal partner för IoT-data som kräver snabb datainskrivning och effektiv lagring. När det gäller visualisering, är Grafana heltäckande för att skapa informativa och intuitiva dashboards med användarvänliga drag-and-drop-verktyg som kräver ingen programmering, vilket gör det tillgängligt för användare på alla teknikerfarenhetsnivåer. 

- Instruktioner för hur man ställer in dataströmningspipelinen från MQQT till Influx finns tillgängliga [här](https://github.com/iot-lnu/iotlab-pilotcase-etec/blob/main/mqtt_influx_import/INSTRUCTIONS.md)
- Flux queries och exempel på Grafana visualiseringar finns här

