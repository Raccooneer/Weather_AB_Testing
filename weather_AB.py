"""Get weather forecast data from providers, pull to database and setup AB Testing experiment."""

# %% [Markdown] ======================================================================
#
# Section 0: imports and credentials
#   (1) package import
#   (2) personal modul imports
# 
# ====================================================================================

# %% (1) package import
import pandas as pd
import os
import yaml
import json
from dotenv import load_dotenv

# %% (2) personal modul imports
# for testing and debugging only
# %load_ext autoreload
# %autoreload 2

from src.wrap_requests import get_multiple_to_file

# %% [Markdown] ======================================================================
#
# Section 1: functions
#   (1) save data from one provider to file
# 
# ====================================================================================

# %% (1) save data from one provider to file
def get_weatherdata_by_provider(provider = "meteostat"):
    """Load weather data by one specified provider.

    args:
        provider (str) : provider that has to be present in the config

    return:
        no return
    """
    # load cretendials
    load_dotenv()
    try:
        auth = json.loads(os.getenv(provider))
    except TypeError:
        f"Provider {provider} missing credentials"
        raise Exception
    # create temp folder if it does not exist
    if not os.path.isdir("temp"):
        os.mkdir("temp")
    
    # load config
    with open("res/config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    
    # escape if provider not in config or credentials
    if provider not in config.keys():
        raise f"Provider {provider} missing config"

    # setup vars
    start = pd.to_datetime("now").date() - + pd.Timedelta("1d")
    end = start + pd.Timedelta("8d")

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
            filename = f"temp/{ provider }.csv",
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
            filename = f"temp/{ provider }.csv",
            multi_type="urls",
            params_dict = params_dict,
            sub_key = config[provider]["sub_key"],
            record_path = config[provider]["record_path"],
            headers = None
            )

    else:
        raise f"provider {provider} misses type"

    pass
# %%
