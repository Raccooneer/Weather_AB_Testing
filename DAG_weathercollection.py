"""Collect weather data and push to DB."""

# %% [Markdown] ######################################################################
#  Section 0 : Imports & Config
#   (1) imports
#   (2) airflow config
#   (3) global variables
#
# ####################################################################################

# %% (1) imports 
from airflow import DAG
import airflow
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd
import sys
import os
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator

# %% (2) airflow config
default_args = {
    'owner': 'Weather_AB_Testing',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),

}
dag = DAG(
    'Weather_Collection',
    default_args=default_args,
    description='Weather Collection of multiple providers',
    schedule_interval="0 13 * * *",
    max_active_runs=1
)

# %% (3) global variables
project_path = Variable.get("Weather_AB_Testing_path")

# %% [Markdown] ######################################################################
#  Section 1 : non-module functions
#   (1) setup func
#   (2) fetch wrapper func
#   (3) forward wrapper func
#   (4) cleanup func
# 
# ####################################################################################

# %% (1) setup func
def setup_func(**kwargs):
    """Create temp folder, if required."""
    temp_folder = os.path.join(project_path, "temp")
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    pass

# %% (2) fetch wrapper func
def fetch_func(provider, **kwargs):
    """Wrap around fetch function to call from different path."""
    # import module by provided path
    sys.path.append(project_path)
    import weather_AB
    # call function
    weather_AB.get_weatherdata_by_provider(provider, filepath = project_path)
    pass

# %% (3) forward wrapper func
def forward_func(provider, **kwargs):
    """Wrap around forward function to call from different path."""
    # import module by provided path
    sys.path.append(project_path)
    import weather_AB
    # call function
    weather_AB.transform_to_db(provider, filepath = project_path)
    pass

# %% (4) cleanup func
def cleanup_func(**kwargs):
    """Cleanup temporary files and folders"""
    temp_folder = os.path.join(project_path, "temp")
    if os.path.exists(temp_folder):
        for i in os.listdir(temp_folder):
            os.remove(os.path.join(temp_folder, i))
        os.rmdir(temp_folder)
    pass

# %% [Markdown] ######################################################################
#  Section 2 : Tasks
#   (1) setup
#   (2) fetch weather data and save temporary: meteostat
#   (3) fetch weather data and save temporary: brightsky
#   (4) fetch weather data and save temporary: visualcrossing
#   (5) transform data and push into weather database: meteostat
#   (6) transform data and push into weather database: brightsky
#   (7) transform data and push into weather database: visualcrossing
#   (8) cleanup
# 
# ####################################################################################

# %% (1) setup
setup = PythonOperator(
    task_id = "setup",
    python_callable = setup_func,
    dag = dag
)

# %% (2) fetch weather data and save temporary: meteostat
fetch_meteostat = PythonOperator(
    task_id = "fetch_meteostat",
    python_callable = fetch_func,
    op_kwargs = {"provider" : "meteostat"},
    dag = dag
)

# %% (3) fetch weather data and save temporary: brightsky
fetch_brightsky = PythonOperator(
    task_id = "fetch_brightsky",
    python_callable = fetch_func,
    op_kwargs = {"provider" : "brightsky"},
    dag = dag
)

# %% (4) fetch weather data and save temporary: visualcrossing
fetch_visualcrossing = PythonOperator(
    task_id = "fetch_visualcrossing",
    python_callable = fetch_func,
    op_kwargs = {"provider" : "visualcrossing"},
    dag = dag
)

# %% (5) transform data and push into weather database: meteostat
forward_meteostat = PythonOperator(
    task_id = "forward_meteostat",
    python_callable = forward_func,
    op_kwargs = {"provider" : "meteostat"},
    dag = dag
)

# %% (6) transform data and push into weather database: brightsky
forward_brightsky = PythonOperator(
    task_id = "forward_brightsky",
    python_callable = forward_func,
    op_kwargs = {"provider" : "brightsky"},
    dag = dag
)

# %% (7) transform data and push into weather database: visualcrossing
forward_visualcrossing = PythonOperator(
    task_id = "forward_visualcrossing",
    python_callable = forward_func,
    op_kwargs = {"provider" : "visualcrossing"},
    dag = dag
)

# %% (8) cleanup
cleanup = PythonOperator(
    task_id = "cleanup",
    python_callable = cleanup_func,
    dag = dag
)

# %% [Markdown] ######################################################################
#  Section 3 : Pipeline
#   (1) Pipeline
# 
# ####################################################################################

# %% (1) Pipeline
# the push to db function run subsequent to avoid erros
setup >> [fetch_meteostat, fetch_brightsky, fetch_visualcrossing]
[fetch_meteostat, fetch_brightsky, fetch_visualcrossing] >> forward_meteostat
forward_meteostat >> forward_brightsky
forward_brightsky >> forward_visualcrossing
forward_visualcrossing >> cleanup

