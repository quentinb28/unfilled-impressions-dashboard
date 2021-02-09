# !/usr/bin/env python
# ! -*- coding: utf-8 -*-

"""
   Copyright © Investing.com
   Licensed under Private License.
   See LICENSE file for more information.
"""

#################################################

# Project: Create an Unfilled Impressions report to grow revenue
# This file does the following:
# - Step1: Get report yesterday of unfilled impressions per ad unit.
# - Step2: Get average eCPM last 30 days per siteGeo.
# - Step3: Compute potential revenue => unfilled impressions / 1000 * eCPM siteGeo wise.

#################################################


# Libraries

import google.cloud.bigquery as bigquery


# Define function get BQ table

def get_bq_table(table_name, columns='*', filters={}):

    # Instantiate client
    __c = bigquery.Client(project='madrid-investing')

    # Query SQL
    if 'startDate' in filters:
        query_sql = f"""
        SELECT {', '.join(columns)} 
        FROM `madrid-investing.DATA_LAKE_MODELING_US.{table_name}` 
        WHERE datetime >= '{filters['startDate']}'"""
    else:
        query_sql = f"""
        SELECT {', '.join(columns)} 
        FROM `madrid-investing.DATA_LAKE_MODELING_US.{table_name}`"""

    # Get results
    __res = __c.query(query_sql).result()

    return __res.to_dataframe()


# Define function save_to_bq

def save_to_bq(df, project, dataset, filename):

    df.to_gbq(
        f'{dataset}.{filename}',
        if_exists='append',
        project_id=project
    )
