# Projekt počasí vs. realita
## Zdroje

## Data
### Tabulka df_joined.csv
#### Sloupce
- forecast                   - object - pozůstatek z předpovědi weathercom - neměl by tam být, zapomněla jsem sloupec smazat
- **forecast_date**          - object - datum, na kdy je předpověď (v případě předpovědi) nebo datum měření (v případě čhmú)
- **location**               - object - název stanice
- date_stamp_f       - datetime64[ns] - datum a čas, kdy byla stažena předpoveď
- temp_max                  - float64 - předpovězená maximální teplota ve °C
- temp_min                  - float64 - předpovězená minimální teplota ve °C
- rain_bool                  - object - True/False - jestli byl předpovězen déšť
- **fday**                  - float64 - kolikadenní je to předpověď - na kolik dní dopředu
- **source**                 - object - zdroj předpovědi
- temp_mean                 - float64 - průměrná předpovězená teplota ve °C
- rain                      - float64 - předpovězené množství srážek v mm
- snow                      - float64 - předpovězené množství sněhu (asi v cm)
- chmi_temp_avg             - float64 - naměřená průměrná teplota v °C
- chmi_temp_max             - float64 - naměřená maximální teplota v °C
- chmi_temp_min             - float64 - naměřená minimální teplota v °C
- date_stamp_chmi    - datetime64[ns] - datum a čas, kdy byla stažena data z čhmú
- chmi_rain                 - float64 - namřené srážky v mm
- chmi_snow                 - float64 - nový sníh v cm
- chmi_rain_bool             - object - True/False údaj o tom, jestli pršelo *
- latitude                  - float64 - zeměpisná šířka (gps stanice)
- longitude                 - float64 - zeměpisná délka (gps stanice)

>\* chmi_rain - **misinterpretation** - čhmú udává množství srážek v mm, ale neříká, jestli pršelo. Pokud pršelo, ale bylo to neměřitelné, pak nám zde vzniká chyba. 

### Tabulka df_grouped1.csv
Toto je tabulka df_joined zgrupovaná podle source, fday a location. 

#### Sloupce
- location                     -  object - název stanice
- fday                         - float64 - kolikadenní je to předpověď - na kolik dní dopředu
- source                       -  object - zdroj předpovědi
- temp_max_diff_mean           - float64 - průměr rozdílu maximálních teplot předpovědi vs. realita (mean (temp_max - chmi_temp_max))
- temp_max_diff_median         - float64 - medián rozdílu maximálních teplot předpovědi vs. realita (median (temp_max - chmi_temp_max))
- temp_max_diff_std            - float64 - standardní odchylka rozdílu maximálních teplot předpovědi vs. realita (std (temp_max - chmi_temp_max))
- temp_max_diff_var            - float64 - rozptyl rozdílu maximálních teplot předpovědi vs. realita (var (temp_max - chmi_temp_max))
- temp_min_diff_count          -   int64 - počet hodnot ve statistice (count (temp_max - chmi_temp_max)) *
- temp_mean_diff_mean          - float64 - průměr rozdílu průměrných teplot předpovědi vs. realita (mean (temp_mean - chmi_temp_mean))
- temp_mean_diff_median        - float64 - medián rozdílu průměrných teplot předpovědi vs. realita (median (temp_mean - chmi_temp_mean))
- temp_mean_diff_std           - float64 - standardní odchylka rozdílu průměrných teplot předpovědi vs. realita (std (temp_mean - chmi_temp_mean))
- temp_mean_diff_var           - float64 - rozptyl rozdílu průměrných teplot předpovědi vs. realita (var (temp_mean - chmi_temp_mean))
- temp_mean_diff_count         -   int64 - počet hodnot ve statistice (count (temp_mean - chmi_temp_mean)) *
- rain_diff_mean               - float64 - průměr rozdílu předpovězených srážek vs. naměřených srážek (mean(rain - chmi_rain))
- rain_diff_median             - float64 - medián rozdílu předpovězených srážek vs. naměřených srážek (median(rain - chmi_rain))
- rain_diff_std                - float64 - standardní odchylka rozdílu předpovězených srážek vs. naměřených srážek (std(rain - chmi_rain))
- rain_diff_var                - float64 - rozptyl rozdílu předpovězených srážek vs. naměřených srážek (var(rain - chmi_rain))
- rain_diff_count              -   int64 - počet hodnot ve statistice (count(rain - chmi_rain)) *
- temp_max_diff_abs_mean       - float64 - průměr absolutních hodnot rozdílů maximálních teplot předpovědi vs. realita (mean(abs(temp_max - chmi_temp_max)))
- temp_max_diff_abs_median     - float64 - medián absolutních hodnot rozdílů maximálních teplot předpovědi vs. realita (median(abs(temp_max - chmi_temp_max)))
- temp_max_diff_abs_std        - float64 - standardní odchylka absolutních hodnot rozdílů maximálních teplot předpovědi vs. realita (std(abs(temp_max - chmi_temp_max)))
- temp_max_diff_abs_var        - float64 - rozptyl absolutních hodnot rozdílů maximálních teplot předpovědi vs. realita (var(abs(temp_max - chmi_temp_max)))
- temp_min_diff_abs_mean       - float64 - průměr absolutních hodnot rozdílů minimálních teplot předpovědi vs. realita (mean(abs(temp_min - chmi_temp_min)))
- temp_min_diff_abs_median     - float64 - medián absolutních hodnot rozdílů minimálních teplot předpovědi vs. realita (median(abs(temp_min - chmi_temp_min)))
- temp_min_diff_abs_std        - float64 - standardní odchylka absolutních hodnot rozdílů minimálních teplot předpovědi vs. realita (std(abs(temp_min - chmi_temp_min)))
- temp_min_diff_abs_var        - float64 - rozptyl absolutních hodnot rozdílů minimálních teplot předpovědi vs. realita (var(abs(temp_min - chmi_temp_min)))
- temp_mean_diff_abs_mean      - float64 - průměr absolutních hodnot rozdílů průměrných teplot předpovědi vs. realita (mean(abs(temp_mean - chmi_temp_mean)))
- temp_mean_diff_abs_median    - float64 - medián -||-
- temp_mean_diff_abs_std       - float64 - standardní odchylka -||-
- temp_mean_diff_abs_var       - float64 - rozptyl -||-
- rain_match_sum               - float64 - počet dní, kdy předpověď deště (True/False) se trefila do reality (rain_bool a chmi_rain_bool jsou True/True nebo False/False)
- rain_falsenegative_sum       - float64 - to je, když předpověď je False, ale skutečnost True.
- rain_falsepositive_sum       - float64 - to je, když je předpověď True, ale skutečnost False
>\* počet hodnot ve statistice - myslím, že by bylo fér ke každému grafu, kde jsou agregovaná data také dodat nějaký popis těchto dat. Přinejmenším to, jak velké vzorky mezi sebou porovnávám. Protože z některých zdrojů máme více dat než z jiných. 

### Tabulka df_grouped2.csv
Toto je tabulka df_joined, která je zgrupovaná podle source a fday. Má úplně totožné sloupce jako df_grouped1, ale chybí jí sloupec location. Data jsou agregovaná přes všechny stanice - tedy za celou republiku. Oproti df_grouped1 má tedy podstatně méně řádků. 