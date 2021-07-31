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
    auth = json.loads(os.getenv(provider))

    # create temp folder if it does not exist
    if not os.path.isdir("temp"):
        os.mkdir("temp")
    
    # load config
    with open("res/config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    
    # escape if provider not in config or credentials
    if auth == "" or provider not in config.keys():
        raise f"Provider {provider} missing credentials or config"

    # setup vars
    start = pd.to_datetime("now").date()
    end = start + pd.Timedelta("7d")

    # create params to call TODO: adjust to other providers as well
    params_dict = {
        point :
            {
                "lon" : config["points"][point]["lon"],
                "lat" : config["points"][point]["lat"],
                "start" : str(start),
                "end" : str(end)
            }
        for point in config["points"].keys()}

    # call and save to temp
    get_multiple_to_file(
        url = config[provider]["url"],
        filename = f"temp/{ provider }.csv",
        params_dict = params_dict,
        sub_key = config[provider]["sub_key"],
        headers = auth
        )
    
    pass