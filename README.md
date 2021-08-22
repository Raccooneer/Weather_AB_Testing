# A/B-Testing of Weather data providers

A showcase project that intends to compare the forecast accuracy of different weather data providers using A/B-Testing.

It compares the weather data providers based on two questions:
1. is the occurrence of rain correctly predicted?
2. How accurate is the temperature prediction?

As showcase project, the git shows:
* data fetching and transformation from a REST api
* SQL-based Database creation, storage and querying of data via python
* Automation of data collection with airflow
* A/B-Testing of 3 providers for one binary metric and a continuous metric
* Various data transformations with pandas
* Various data visualization with matplotlib and seaborn

## Motivation

Weather data can be a crucial factor for a variety that impacts business activities. Certain products sell more during hot and sunny days as in the typical ice cream stand example. Other products may sell more during cold and rainy days such as e-commerce shops that may attract more customers when these customers are limited in doing outdoor activities. Certain activities may mot be conducted during rainy days ranging from outdoor weddings to certain construction site activities. While the weather can change quite fast, operations may, however, not have this opportunity. Even quite flexible activities can only change to a limited degree and this flexibility usually comes at a price.

To improve the fit of operations to weather dependent situations, weather forecasting is an essential source of information. While weather forecasting has become more accurate over time and is becoming ever more accurate with more and ongoing research, there is still a level of error in the forecasts. This level of error is not the first thing one will find on the website of a weather data provider. The error level has to be calculated. However, the forecasts are not stored and fetched like historical data. The seven day forecast of today plus 7 days can only be fetched today. Tomorrow, one will only be able to fetch the six day forecast from tomorrow on (usually a new forecast) for the day of interest. To evaluate the seven day forecasts, the forecasts have to be collected and compared to their actual values in today plus 7 days. With a multitude of providers to choose from, this can be a time-consuming endeavor. 

This analysis focusses on two ideas on how weather can impact business activities, calculates metrics on the accuracy of forecasts provided by weather data providers and compares 3 weather data providers.

1. The operational activities or the demand of an organization can be strongly impacted by precipitation. Organizations may see a large drop in demand or jump in demand when rain occurs and with the rain persisting for several hours, this can lead to over-staffing or under-staffing compared to a non-rain situation. In that scenario, however, the amount of rain may not be the most important factor. A difference of 0.1 mm/m^2 may have no impact att all, when it is already raining heavily. More relevant is the question, whether there will be precipitation under a certain threshold that nobody cares about (no precipitation or some light drizzle) or will there be precipitation that impacts customers behavior. Hence, the Business Question is: *What is the success rate of forecasting the occurrence of rain correctly?*
2. Another factor on business activities is the temperature. As opposed to precipitation, that can have a somewhat binary effect of switching demand on or off, temperature leads more to a scaling of demand. The demand for hot tea in a coffee shop may scale upwards with decreasing temperatures while the demand for ice cream cones scales the other way around. For both businesses, buying stocks may take a few days planning ahead and not having accurate weather information may leave some latent demand for competitors to fill. Hence, the Business Question is: *How accurate is the temperature forecast?*

## Analysis

For this data, it has to be assumed that the providers use some kind of time-series based prediction methods. In result, it cannot be assumed that the forecast errors are independent from each other since the forecast of day d is probably used to forecast the weather of day d+1 with a propagation of the error of one forecast to the other. However, since this is a showcase focussed on the methods, some methods will be applied despite the violation of their basic assumption with a strong warning about the usability of the results.

### Occurrence of rain

TODO: write details on analysis of occurrence of rain

### Accuracy of Temperature

TODO: write details on analysis of temperature accuracy

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
   ...
  ]}
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

Brightsky is part of the open data program of the `Deutsche Wetter Dienst`, the german weather service, and no cost are associated with this API. 

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
  ],
  ...
}
```

Thereby, the [documentation](https://brightsky.dev/docs/#tag--weather) explains the content of the response as follows:

| Field | Type | Description |
| --------- | ------------------------------------------ | ------- |
| timestamp | timestamp | ISO 8601-formatted timestamp of this weather record/forecast |
| source_id | integer | Main Bright Sky source ID for this record |
| cloud_cover | number/null | Total cloud cover at timestamp |
| condition | enum/null | Conditions: dry/fog/rain/sleet/snow/hail/thunderstorm (calculated from different fields) |
| dew_point | number/null | Dew point at timestamp, 2 m above ground |
| icon | enum/null | Allowed: clear-day/clear-night/partly-cloudy-day/partly-cloudy-night/cloudy/fog/wind/rain/sleet/snow/hail/thunderstorm (calculated from different fields) |
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
| fallback_source_ids | object | alternative sources that were used to fill up missing values in the main source |

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
            ...]}],
     ...,
    }
```

Thereby, the [documentation](https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/) explains the content of the response as follows:

| Field | Description |
| -- | -- |
| cloudcover | how much of the sky is covered in cloud ranging from 0-100% |
| conditions | textual representation of the weather conditions. See Weather Data Conditions. |
| description | longer text descriptions suitable for displaying in weather displays. |
| datetime | ISO formatted date |
| datetimeEpoch | number of seconds since 1st January 1970 in UTC time |
| tzoffset | the time zone offset in hours. |
| dew | dew point temperature |
| feelslike | what the temperature feels like accounting for heat index or windchill |
| hours | array of hourly weather data objects. |
| humidity | relative humidity in % |
| icon | a fixed, machine readable summary that can be used to display an icon |
| moonphase |  represents the fractional portion through the current moon |
| normal | array of normal weather data values |
| offsetseconds (hourly only) | time zone offset in seconds |
| precip | the amount of precipitation |
| precipcover (days only) | the proportion of hours where there was non-zero precipitation |
| precipprob (forecast only) | the likelihood of measurable precipitation |
| preciptype (forecast only) | rain/snow/freezingrain/ice. |
| pressure | the sea level atmospheric or barometric pressure in millibars |
| snow | the amount of snow that fell or is predicted to fall |
| snowdepth | the depth of snow on the ground |
| source |  the type of weather data used for this weather object |
| stations (historical only) | the weather stations used for collecting |
| sunrise (day only) | The formatted time of the sunrise |
| sunriseEpoch | sunrise time epoch |
| sunset | The formatted time of the sunset |
| sunsetEpoch | sunset time epoch |
| temp | temperature at the location |
| tempmax (day only) | maximum temperature at the location. |
| tempmin (day only) | minimum temperature at the location. |
| uvindex | a value between 0 and 10 indicating the level of ultra violet (UV) exposure |
| visibility | distance at which distant objects are visible |
| winddir | direction from which the wind is blowing |
| windgust | instantaneous wind speed at a location |
| windspeed | average wind speed over a minute |
| solarradiation | (W/m2) the solar radiation power |
| solarenergy | (MJ or kWh) indicates the total energy from the sun |
| severerisk | a value between 0 and 100 representing the likelihood of severe weather |