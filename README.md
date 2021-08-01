# Weather_AB_Testing


## Data

The analysis collects 1-7 day forecasts as well as the actual weather from two provider.

### Meteostat

Meteostat has a freemium model that allows 500 free calls per month. It accepts donations as well. The rate limit is probably not enough for professional purposes but satisfies for testing and this experimental design. 

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

### VisualCrossing

VisualCrossing has a freemium model that allows 1000 free results per day (an 7-day forecast is about 25 results). The rate limit is probably not enough for professional purposes but satisfies for testing and this experimental design.

Using the `services/timeline` API endpoint, the payload looks like this (data not displayed). The data comes in local time and includes the unix epoch as well:

```
{
    ...,
    'days' {
        [
            ...,
        {'datetime': '2021-08-08',
        'datetimeEpoch': 1628373600,
        'tempmax': ##.#,
        'tempmin': ##.#,
        'temp': ##.#,
        'feelslikemax': ##.#,
        'feelslikemin': ##.#,
        'feelslike': ##.#,
        'dew': ##.#,
        'humidity': ##.#,
        'precip': ##.#,
        'precipprob': ##.#,
        'precipcover': list or None,
        'preciptype': list or None,
        'snow': ##.#,
        'snowdepth': ##.#,
        'windgust': ##.#,
        'windspeed': ##.#,
        'winddir': ##.#,
        'pressure': ##.#,
        'cloudcover': ##.#,
        'visibility': ##.#,
        'solarradiation': ##.#,
        'solarenergy': ##.#,
        'uvindex': ##.#,
        'severerisk': ##.#,
        'sunrise': 'HH:MM:SS',
        'sunriseEpoch': #,
        'sunset': 'HH:MM:SS',
        'sunsetEpoch': #,
        'moonphase': ##.#,
        'conditions': str,
        'description': str,
        'icon': str,
        'stations': list or None,
        'source': 'fcst',
        'hours': [{'datetime': '00:00:00',
            'datetimeEpoch': 1628373600,
            'temp': ##.#,
            'feelslike': ##.#,
            'humidity': ##.#,
            'dew': ##.#,
            'precip': ##.#,
            'precipprob': ##.#,
            'snow': ##.#,
            'snowdepth': ##.#,
            'preciptype': str or None,
            'windgust': ##.#,
            'windspeed': ##.#,
            'winddir': ##.#,
            'pressure': ##.#,
            'visibility': ##.#,
            'cloudcover': ##.#,
            'solarradiation': ##.#,
            'solarenergy': ##.#,
            'uvindex': ##.#,
            'severerisk': ##.#,
            'conditions': str,
            'icon': str,
            'stations': None,
            'source': 'fcst'},
            {'datetime': '01:00:00',
            'datetimeEpoch': 1628377200,
            'temp': ##.#,
            'feelslike': ##.#,
            'humidity': ##.#,
            'dew': ##.#,
            'precip': ##.#,
            'precipprob': ##.#,
            'snow': ##.#,
            'snowdepth': ##.#,
            'preciptype': str or None,
            'windgust': ##.#,
            'windspeed': ##.#,
            'winddir': ##.#,
            'pressure': ##.#,
            'visibility': ##.#,
            'cloudcover': ##.#,
            'solarradiation': ##.#,
            'solarenergy': ##.#,
            'uvindex': ##.#,
            'severerisk': ##.#,
            'conditions': str,
            'icon': str,
            'stations': None,
            'source': 'fcst'},
            ...
            {'datetime': '23:00:00',
            'datetimeEpoch': 1628456400,
            'temp': ##.#,
            'feelslike': ##.#,
            'humidity': ##.#,
            'dew': ##.#,
            'precip': ##.#,
            'precipprob': ##.#,
            'snow': ##.#,
            'snowdepth': ##.#,
            'preciptype': str or None,
            'windgust': ##.#,
            'windspeed': ##.#,
            'winddir': ##.#,
            'pressure': ##.#,
            'visibility': ##.#,
            'cloudcover': ##.#,
            'solarradiation': ##.#,
            'solarenergy': ##.#,
            'uvindex': ##.#,
            'severerisk': ##.#,
            'conditions': str,
            'icon': str,
            'stations': None,
            'source': 'fcst'}]}],
     ...,
    }
```

Thereby, the [documentation](https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/) explains the content of the response as follows:

| Field | Description |
| -- | -- |
| cloudcover | how much of the sky is covered in cloud ranging from 0-100% |
| conditions | textual representation of the weather conditions. See Weather Data Conditions. |
| description | longer text descriptions suitable for displaying in weather displays. The descriptions combine the main features of the weather for the day such as precipitation or amount of cloud cover. Daily descriptions are provided for historical and forecast days. When the timeline request includes the model forecast period, a seven day outlook description is provided at the root response level. |
| datetime | ISO formatted date, time or datetime value indicating the date and time of the weather data in the locale time zone of the requested location |
| datetimeEpoch | number of seconds since 1st January 1970 in UTC time |
| tzoffset | the time zone offset in hours. This will only occur in the data object if it is different from the global timezone offset. |
| dew | dew point temperature |
| feelslike | what the temperature feels like accounting for heat index or windchill |
| hours | array of hourly weather data objects. This is a child of each of the daily weather object when hours are selected. |
| humidity | relative humidity in % |
| icon | a fixed, machine readable summary that can be used to display an icon |
| moonphase |  represents the fractional portion through the current moon  |lunation cycle ranging from 0 (the new moon) to 0.5 (the full moon) and back to 1 (the next new moon) |
| normal | array of normal weather data values – Each weather data normal is an array of three values representing, in order, the minimum value over the statistical period, the mean value, and the maximum value over the statistical period. |
| offsetseconds (hourly only) | time zone offset for this weather data object in seconds – This value may change for a location based on daylight saving time observation. |
| precip | the amount of precipitation that fell or is predicted to fall in the period |
| precipcover (days only) | the proportion of hours where there was non-zero precipitation |
| precipprob (forecast only) | the likelihood of measurable precipitation ranging from 0% to 100% |
| preciptype (forecast only) | an array indicating the type(s) of precipitation expected. Possible values include rain, snow, freezingrain and ice. |
| pressure | the sea level atmospheric or barometric pressure in millibars (or hectopascals) |
| snow | the amount of snow that fell or is predicted to fall |
| snowdepth | the depth of snow on the ground |
| source |  the type of weather data used for this weather object. – Values include historical observation (“obs”), forecast (“fcst”), historical forecast (“histfcst”) or statistical forecast (“stats”). If multiple types are used in the same day, “comb” is used. Today is typically a combination of historical observations and forecast data. |
| stations (historical only) | the weather stations used when collecting an historical observation record |
| sunrise (day only) | The formatted time of the sunrise (For example “2020-10-28T07:33:15-04:00”) |
| sunriseEpoch | sunrise time specified as number of seconds since 1st January 1970 in UTC time |
| sunset | The formatted time of the sunset (For example “2020-10-28T18:12:55-04:00”) |
| sunsetEpoch | sunset time specified as number of seconds since 1st January 1970 in UTC time |
| temp | temperature at the location |
| tempmax (day only) | maximum temperature at the location. |
| tempmin (day only) | minimum temperature at the location. |
| uvindex | a value between 0 and 10 indicating the level of ultra violet (UV)  |exposure for that hour or day. 10 represents high level of exposure, and 0 represents no exposure. The UV index is calculated based on amount of short wave solar radiation which in turn is a level the cloudiness, type of cloud, time of day, time of year and location altitude. Daily values represent the maximum value of the hourly values. |
| visibility | distance at which distant objects are visible |
| winddir | direction from which the wind is blowing |
| windgust | instantaneous wind speed at a location – May be empty if it is not significantly higher than the wind speed. |
| windspeed | average wind speed over a minute |
| solarradiation | (W/m2) the solar radiation power at the instantaneous moment of the observation (or forecast prediction). See the full solar radiation data documentation. |
| solarenergy | (MJ or kWh) indicates the total energy from the sun that builds up over an hour or day. See the full solar radiation data documentation. |
| severerisk | (beta, forecast only) – a value between 0 and 100 representing the likelihood of severe weather such as thunderstorms, hail or tornados. 0 is very low chance of severe weather. 30-60 represents there is a chance of severe weather, 60-100 indicates there is a high chance of severe weather. |