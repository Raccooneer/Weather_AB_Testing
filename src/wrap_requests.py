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
#   (1) save multiple calls to file wrapper
#  
# ====================================================================================

# %% (1) save to file wrapper
def get_multiple_to_file(url, filename, multi_type=None, headers=None, params_dict={}, 
    sub_key=None, record_path=None, session=None):
    """Save data from multiple API Calls with same url, auth, and data structure but different params to file.

    args:
        url (str or dict) : url of the API
        filename (str) : filename and path including file extension
        multi_type (str or None) : accepts None, "params" and "urls"
        headers (dict) : the required authorization for the api
        params_dict (dict or dict of dicts) : dict of multiple additional parameters for the 
            get request with different dict keys
        sub_key (str) : key of nested 
        record_path (str) : record_path of further nested json 
        session (object of requests) : an session of the requests package that is
            provided for continuous requests

    exceptions:
        Raises Exception of wrong Authorization
    """
    # setup
    session_provided = session is not None
    if not session_provided:
        session = requests.Session()
    res = pd.DataFrame()

    # check the way to call the API
    if multi_type is None:
        res = get_to_dataframe(
            url=url, 
            headers=headers, 
            params=params_dict, 
            sub_key=sub_key,
            record_path=record_path,
            session=session)

    elif multi_type == "params":
        # make calls
        for key, value in params_dict.items(): 
            temp = get_to_dataframe(
                url=url, 
                headers=headers, 
                params=value, 
                sub_key=sub_key,
                record_path=record_path,
                session=session)
            temp = temp.assign(
                city = key
            )
            res = res.append(temp, ignore_index=True)
    
    elif multi_type == "urls":
        # data type check
        if type(url) == str:
            url = {"unknown" : url}
        # make calls
        for key, value in url.items(): 
            temp = get_to_dataframe(
                url=value, 
                headers=headers, 
                params=params_dict, 
                sub_key=sub_key,
                record_path=record_path,
                session=session)
            temp = temp.assign(
                city = key
            )
            res = res.append(temp, ignore_index=True)
    else:
        raise f"multi_type {multi_type} unknown"
    
    # save to file
    res.to_csv(filename, index=False)
    
    # closing statements
    if not session_provided:
        session.close()
    pass

# %% [Markdown] ======================================================================
#
# Section 2: get request function
#   (1) function to get (simply nested) data from api and transform to df
#   (2) wrapper function to get paginated (not nested) data from api and transform to df
# 
# ====================================================================================

# %% (1) function to get (simply nested) data from api and transform to df
def get_to_dataframe(url, headers=None, params={}, sub_key=None, record_path=None, 
    session=None):
    """GET data from API and transform to dataframe.

    args:
        url (str) : url of the API
        headers (dict) : the required authorization for the api
        params (dict) : additional parameters for the get request
        sub_key (str) : key of nested
        record_path (str) : record_path of further nested json 
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
        return pd.json_normalize(payload.json(), record_path=record_path, max_level=0)
    else:
        return pd.json_normalize(payload.json()[sub_key], record_path=record_path, max_level=0)


# %%
