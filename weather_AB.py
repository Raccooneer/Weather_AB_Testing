"""Get weather forecast data from providers, pull to database and setup AB Testing experiment."""

# %% [Markdown] ======================================================================
#
# Section 0: imports and credentials
#   (1) package import
#   (2) personal module imports
# 
# ====================================================================================

# %% (1) package import
import pandas as pd
import os
import yaml
import json
from dotenv import load_dotenv

# %% (2) personal module imports
# NOTE: for testing and debugging only
# %load_ext autoreload
# %autoreload 2
from src.wrap_requests import get_multiple_to_file
from src.wrap_psql import post_upsert_postgreSQL

# %% [Markdown] ======================================================================
#
# Section 1: functions
#   (1) save data from one provider to file
#   (2) transform data and save to DB
# 
# ====================================================================================

# %% (1) save data from one provider to file
def get_weatherdata_by_provider(provider, filepath=""):
    """Load weather data of one specified provider.

    args:
        provider (str) : provider that has to be present in the config

    return:
        no return
    """
    # load credentials
    load_dotenv(os.path.join(filepath, ".env"))
    try:
        auth = json.loads(os.getenv(provider))
    except TypeError:
        f"Provider {provider} missing credentials"
        raise Exception
    # create temp folder if it does not exist
    if not os.path.isdir(os.path.join(filepath, "temp")):
        os.mkdir(os.path.join(filepath, "temp"))
    
    # load config
    with open(os.path.join(filepath, "res/config/config.yaml"), "r") as file:
        config = yaml.safe_load(file)
    
    # escape if provider not in config
    if provider not in config.keys():
        raise f"Provider {provider} missing config"

    # setup vars
    start = pd.to_datetime("now").date() - + pd.Timedelta("1d")
    end = start + pd.Timedelta("9d")

    if config[provider]["type"] == "params":
        # create params to call
        params_dict = {
            point :
                {
                    "lon" : config["points"][point]["lon"],
                    "lat" : config["points"][point]["lat"],
                    config[provider]["start_date_param"] : str(start),
                    config[provider]["end_date_param"] : str(end)
                }
            for point in config["points"].keys()}

        # call and save to temp
        get_multiple_to_file(
            url = config[provider]["url"],
            filename = os.path.join(filepath, f"temp/{ provider }.csv"),
            multi_type="params",
            params_dict = params_dict,
            sub_key = config[provider]["sub_key"],
            record_path = config[provider]["record_path"],
            headers = auth
            )

    elif config[provider]["type"] == "url":
        # create params to call
        params_dict = {
            **config[provider]["provider_specific_params"],
            **auth
        }
        urls = {
            point : config[provider]["url"].format(
                point = point,
                start = start,
                end = end
            ) 
            for point in config["points"].keys()}
        # call and save to temp
        get_multiple_to_file(
            url = urls,
            filename = os.path.join(filepath, f"temp/{ provider }.csv"),
            multi_type="urls",
            params_dict = params_dict,
            sub_key = config[provider]["sub_key"],
            record_path = config[provider]["record_path"],
            headers = None
            )

    else:
        raise f"provider {provider} misses type"

    pass

# %% (2) transform data and save to DB
def transform_to_db(provider, filepath=""):
    """Load and transform data of provider and push to DB in standardized data structure.
    
    args:
        provider (str) : provider that has to be present in the config

    return:
        no return
    """
    # load auth
    load_dotenv(os.path.join(filepath, ".env"))
    auth = json.loads(os.getenv("database"))

    # load config
    with open(os.path.join(filepath, "res/config/config.yaml"), "r") as file:
        config = yaml.safe_load(file)
    # escape if provider not in config
    if provider not in config.keys():
        raise f"Provider {provider} missing config"

    # check if file exists
    if not os.path.isfile(os.path.join(filepath, f"temp/{provider}.csv")):
        raise f"this provider has no temporary file"

    # load file
    df = pd.read_csv(os.path.join(filepath, f"temp/{provider}.csv"))

    # special operations
    if config[provider]["special_operations"] is not None:
        # apply epoch to datetime (if required)
        if "epoch_to_timestamp" in config[provider]["special_operations"]:
            df = (
                df.assign(timestamp = lambda x : pd.to_datetime(
                    x.datetimeEpoch, 
                    unit='s', 
                    origin='unix', 
                    utc = True))
            )

    # rename columns, filter and add create time
    columns_to_save = [v for k, v in config[provider]["mapping"].items()] + ["city"]
    df = (
        df
            .rename(columns=config[provider]["mapping"])
            .filter(columns_to_save)
            .assign(
                create_time = pd.to_datetime("now", utc=True).floor("1H"),
                provider = provider,
                weather_time = lambda x : pd.to_datetime(x.weather_time, utc=True),
                time_diff = lambda x : (x.weather_time.dt.date - x.create_time.dt.date).dt.days,
                forecast_type = lambda x : x.time_diff.map(lambda x : 
                    "actual"
                    if x < 0
                    else f"{x} day forecast"
                )
            )
            .drop(["time_diff"], axis = 1)
    )

    # post data to db
    post_upsert_postgreSQL("weather_forecast", df, auth=auth)

    pass

# %%
