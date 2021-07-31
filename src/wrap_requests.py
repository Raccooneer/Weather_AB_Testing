"""Individual wrapper functions for (paginated) requests."""

# %% [Markdown] ======================================================================
#
# Section 0: imports and credentials
#   (1) package import
# 
# ====================================================================================

# %% (1) package import
import pandas as pd
import requests
import urllib

# %% [Markdown] ======================================================================
# 
# Section 1: helper functions, classes and decorators
# 
# ====================================================================================

# %% [Markdown] ======================================================================
#
# Section 2: get request function
#   (1) function to get (simply nested) data from api and transform to df
#   (2) wrapper function to get paginated (unnested) data from api and transform to df
# 
# ====================================================================================

# %% (1) function to get (simply nested) data from api and transform to df
def get_to_dataframe(url, headers=None, params={}, sub_key=None, session=None):
    """GET data from API and transform to dataframe.

    params:
        url (str) : url of the API
        headers (dict) : the required authorization for the api
        params (dict) : additional parameters for the get request
        sub_key (str) : key of nested 
        session (object of requests) : an session of the requests package that is
            provided for continuous requests

    exceptions:
        Raises Exception of wrong Authorization
    """
    # open session if not provided
    session_provided = True
    if session is None:
        session = requests.Session()
        session_provided = False
    # adapt params
    params = urllib.parse.urlencode(
        params,
        quote_via=urllib.parse.quote
    )
    payload = session.get(url, params = params, headers=headers)
    # Raise Exception of wrong Authorization
    if payload.status_code == 401:
        raise f"""Status Code 401: No / wrong Authorization
            -------------------------------------------------
            {payload.content}"""
    # close session if explicitly created
    if not session_provided:
        session.close()
    # return data
    if sub_key is None:
        return pd.json_normalize(payload.json(), max_level=0)
    else:
        return pd.json_normalize(payload.json()[sub_key], max_level=0)


# %%
