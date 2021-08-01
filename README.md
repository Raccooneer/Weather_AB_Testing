# Weather_AB_Testing


## Data

The analysis collects 1-7 day forecasts as well as the actual weather from two provider.

### Meteostat

Meteostat has a freemium model that allows 500 calls per month. It accepts donations as well. The rate limit is unlikely enough for professional purposes but satisfies for testing and this experimental design.  

Using the `point/hourly` API endpoint (via rapidapi), the payload looks like this (data not displayed). The data comes in UTC, but the timestamp doesn't carry timezone information:

```
{'meta': {'generated': '2021-08-01 11:05:41',
  'stations': ['10384', '10381', '10385', '10379']},
 'data': [{'time': '2021-08-01 00:00:00',
   'temp': ##.#,
   'dwpt': ##.#,
   'rhum': ##.#,
   'prcp': ##.#,
   'snow': # or None,
   'wdir': ##.#,
   'wspd': ##.#,
   'wpgt': ##.#,
   'pres': ##.#,
   'tsun': # or None,
   'coco': #},
  {'time': '2021-08-01 01:00:00',
   'temp': ##.#,
   'dwpt': ##.#,
   'rhum': ##.#,
   'prcp': ##.#,
   'snow': # or None,
   'wdir': ##.#,
   'wspd': ##.#,
   'wpgt': ##.#,
   'pres': ##.#,
   'tsun': # or None,
   'coco': #},
   ...
  {'time': '2021-08-01 23:00:00',
   'temp': ##.#,
   'dwpt': ##.#,
   'rhum': ##.#,
   'prcp': ##.#,
   'snow': # or None,
   'wdir': ##.#,
   'wspd': ##.#,
   'wpgt': ##.#,
   'pres': ##.#,
   'tsun': # or None,
   'coco': #}]}
```

Thereby, the [documentation](https://dev.meteostat.net/api/stations/hourly.html#response) explains the content of the response as follows:

| Parameter | Description                                | Type    |
| --------- | ------------------------------------------ | ------- |
| time      | Time of observation (YYYY-MM-DD hh:mm:ss)  | String  |
| temp      | The air temperature in °C                  | Float   |
| dwpt      | The dew point in °C                        | Float   |
| rhum      | The relative humidity in percent (%)       | Integer |
| prcp      | The one hour precipitation total in mm     | Float   |
| snow      | The snow depth in mm                       | Integer |
| wdir      | The wind direction in degrees (°)          | Integer |
| wspd      | The average wind speed in km/h             | Float   |
| wpgt      | The peak wind gust in km/h                 | Float   |
| pres      | The sea-level air pressure in hPa          | Float   |
| tsun      | The one hour sunshine total in minutes (m) | Integer |
| coco      | The weather condition code                 | Integer |

### Brightsky

Brightsky is part of the open data program of the `Deutsche Wetter Dienst`, the german weather servcie, and no cost are associated with this API. 

Using the `weather` API endpoint, the payload looks like this (data not displayed). The data comes in UTC and the timestamp does carry timezone information:

```
{'weather': [{'timestamp': '2021-07-31T00:00:00+00:00',
   'source_id': #,
   'precipitation': ##.#,
   'pressure_msl': ##.#,
   'sunshine': ##.#,
   'temperature': ##.#,
   'wind_direction': #,
   'wind_speed': ##.#,
   'cloud_cover': #,
   'dew_point': ##.#,
   'relative_humidity': #,
   'visibility': #,
   'wind_gust_direction': #,
   'wind_gust_speed': ##.#,
   'condition': str,
   'fallback_source_ids': {'visibility': #, 'cloud_cover': #},
   'icon': str},
  {'timestamp': '2021-07-31T01:00:00+00:00',
   'source_id': #,
   'precipitation': ##.#,
   'pressure_msl': ##.#,
   'sunshine': ##.#,
   'temperature': ##.#,
   'wind_direction': #,
   'wind_speed': ##.#,
   'cloud_cover': #,
   'dew_point': ##.#,
   'relative_humidity': #,
   'visibility': #,
   'wind_gust_direction': #,
   'wind_gust_speed': ##.#,
   'condition': str,
   'fallback_source_ids': {'visibility': #, 'cloud_cover': #},
   'icon': str},
   ...
  {'timestamp': '2021-08-01T00:00:00+00:00',
   'source_id': #,
   'precipitation': ##.#,
   'pressure_msl': ##.#,
   'sunshine': ##.#,
   'temperature': ##.#,
   'wind_direction': #,
   'wind_speed': ##.#,
   'cloud_cover': #,
   'dew_point': ##.#
   'relative_humidity': #,
   'visibility': #,
   'wind_gust_direction': None,
   'wind_gust_speed': ##.#,
   'condition': str,
   'fallback_source_ids': {'visibility': #,
    'cloud_cover': #,
    'condition': #},
   'icon': str}],
'sources': [{'id': #,
   'dwd_station_id': str,
   'observation_type': str,
   'lat': ##.####,
   'lon': ##.####,
   'height': ##.#,
   'station_name': str,
   'wmo_station_id': str,
   'first_record': '2010-01-01T00:00:00+00:00',
   'last_record': '2021-07-31T23:00:00+00:00',
   'distance': ##.#},
   ...
  {'id': #,
   'dwd_station_id': str,
   'observation_type': str,
   'lat': ##.####,
   'lon': ##.####,
   'height': ##.#,
   'station_name': str,
   'wmo_station_id': str,
   'first_record': '2021-07-30T09:00:00+00:00',
   'last_record': '2021-08-01T08:00:00+00:00',
   'distance': ##.#}]}
```

Thereby, the [documentation](https://brightsky.dev/docs/#tag--weather) explains the content of the response as follows:

| Field | Type | Description |
| --------- | ------------------------------------------ | ------- |
| timestamp | timestamp |  |ISO 8601-formatted timestamp of this weather record/forecast |
| source_id | integer | Main Bright Sky source ID for this record |
| cloud_cover | number/null | Total cloud cover at timestamp |
| condition | enum/null | Allowed: dry/fog/rain/sleet/snow/hail/thunderstorm/
Current weather conditions. Unlike the numerical parameters, this field is not taken as-is from the raw data (because it does not exist), but is calculated from different fields in the raw data as a best effort. Not all values are available for all source types. |
| dew_point | number/null | Dew point at timestamp, 2 m above ground |
| icon | enum/null | Allowed: clear-day/clear-night/partly-cloudy-day/partly-cloudy-night/cloudy/fog/wind/rain/sleet/snow/hail/thunderstorm/
Icon alias suitable for the current weather conditions. Unlike the numerical parameters, this field is not taken as-is from the raw data (because it does not exist), but is calculated from different fields in the raw data as a best effort. Not all values are available for all source types. |
| precipitation | number/null | Total precipitation during previous 60 minutes |
| pressure_msl | number/null | Atmospheric pressure at timestamp, reduced to mean sea level |
| relative_humidity | number/null | Relative humidity at timestamp |
| sunshine | number/null | Sunshine duration during previous 60 minutes |
| temperature | number/null | Air temperature at timestamp, 2 m above the ground |
| visibility | number/null | Visibility at timestamp |
| wind_direction | number/null | Mean wind direction during previous hour, 10 m above the ground |
| wind_speed | number/null | Mean wind speed during previous hour, 10 m above the ground |
| wind_gust_direction | number/null | Direction of maximum wind gust during previous hour, 10 m above the ground |
| wind_gust_speed | number/null | Speed of maximum wind gust during previous hour, 10 m above the ground |
| fallback_source_ids | object | Object mapping meteorological parameters to the source IDs of alternative sources that were used to fill up missing values in the main source |