Consulta de prueba

```sql
select
    /*f.flight_id,*/
    countryfrom.country as origen,
    countryto.country as destino,
    /*f.departure,*/
    timestampdiff(minute, f.departure, f.arrival) as minutos,
    airline.airlinename,
    COUNT(*) as "cantidad de vuelos"
    
    
    /*, f.**/
from flight f

join airline on airline.airline_id = f.airline_id

join airport portfrom on f.`from` = portfrom.airport_id
join airport_geo countryfrom on countryfrom.airport_id = portfrom.airport_id
join airport portto on f.`to` = portto.airport_id
join airport_geo countryto on countryto.airport_id = portto.airport_id

where countryfrom.country = "SPAIN"

group by countryfrom.country, countryto.country, minutos, airline.airlinename

LIMIT 50
```