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

from datetime import date, timedelta
from src.gam_class import GAM
from src.gcp_bigquery import get_bq_table, save_to_bq


# Define function get period

def get_period(days):

    end_date = date.today()

    start_date = end_date - timedelta(days=days)

    return start_date, end_date


# Define constants

DIMENSIONS_YESTERDAY = ['DATE', 'AD_UNIT_NAME', 'COUNTRY_NAME']

COLUMNS_YESTERDAY = ['TOTAL_LINE_ITEM_LEVEL_IMPRESSIONS', 'TOTAL_INVENTORY_LEVEL_UNFILLED_IMPRESSIONS']

DATE_RANGE_YESTERDAY = 'YESTERDAY'

DIMENSIONS_LAST30DAYS = ['AD_UNIT_NAME', 'COUNTRY_NAME', 'LINE_ITEM_NAME']

COLUMNS_LAST30DAYS = ['TOTAL_LINE_ITEM_LEVEL_IMPRESSIONS', 'AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE']

DATE_RANGE_LAST30DAYS = 'CUSTOM_DATE'

AD_UNITS_FLT = ['Video', 'Sponsored', 'TextNote', 'MobInt', 'IM_', 'Content', 'Bubble', 'Native', '6938', 'JW', 'Ext']

LINE_ITEMS_FLT = [' IO ', 'AdSense', ' - ']

RATES_TO_USD = {'USD': 1, 'EUR': 1.09320, 'TRY': 0.17650, 'RUB': 0.01545, 'BRL': 0.24036}


# Define function gcp function

def gcp_function():
   
    # Instantiate GAM object
    __gam = GAM()

    """
    Step1: Get report yesterday of unfilled impressions per ad unit.

    """

    # Report yesterday params
    yesterday_params = {
        'dimensions': DIMENSIONS_YESTERDAY,
        'columns': COLUMNS_YESTERDAY,
        'dateRange': DATE_RANGE_YESTERDAY
    }

    # Get report yesterday
    __ry = __gam.get_report(yesterday_params, RATES_TO_USD)

    # Get child from ad unit names
    __ry = __gam.get_child_from_ad_unit(__ry)

    # Filter ad unit names
    __ry = __gam.filter_ad_unit_names(__ry, AD_UNITS_FLT)

    # Get site from ad unit name
    __ry['site'] = __ry['ad_unit_name'].apply(lambda __a: __a.split('_')[1] if '_' in __a else 'XX')

    # Add country code column from country name column
    __ry = __gam.country_from_name_to_code(__ry)

    # Make siteGeo column
    __ry['siteGeo'] = __ry['site'] + __ry['country_code']

    # Make total ad requests column
    __ry['total_ad_requests'] = __ry['total_line_item_level_impressions'].fillna(0) + \
                                __ry['total_inventory_level_unfilled_impressions'].fillna(0)

    """
    Step2: Get average eCPM last 30 days per siteGeo.
    """

    # Get period dates
    start_date, end_date = get_period(days=30)

    # Report last 30 days params
    last30days_params = {
        'dimensions': DIMENSIONS_LAST30DAYS,
        'columns': COLUMNS_LAST30DAYS,
        'dateRange': DATE_RANGE_LAST30DAYS,
        'startDate': start_date,
        'endDate': end_date

    }

    # Get report last 30 days
    __rl = __gam.get_report(last30days_params, RATES_TO_USD)

    # Get child from ad unit names
    __rl = __gam.get_child_from_ad_unit(__rl)

    # Filter ad unit names
    __rl = __gam.filter_ad_unit_names(__rl, AD_UNITS_FLT)

    # Filter line item names
    __rl = __gam.filter_line_items(__rl, LINE_ITEMS_FLT)

    # Get site from ad unit name
    __rl['site'] = __rl['ad_unit_name'].apply(lambda __a: __a.split('_')[1] if '_' in __a else 'XX')

    # Add country code column from country name column
    __rl = __gam.country_from_name_to_code(__rl)

    # Make siteGeo column
    __rl['siteGeo'] = __rl['site'] + __rl['country_code']

    # Convert AdEx revenues from EUR to USD
    __rl = __gam.convert_to_usd(__rl, RATES_TO_USD)

    # Group by siteGeo, sum revenue
    __rl = __rl.groupby('siteGeo', as_index=False)[
        'total_line_item_level_impressions',
        'ad_exchange_line_item_level_revenue'].sum()

    # Get BQ table postbacks revenue last 30 days
    __pr = get_bq_table('postbacks_revenue', filters={'startDate': start_date})

    # Make siteGeo column
    __pr['siteGeo'] = __pr['line_item'].apply(lambda __l: __l[:4])

    # Group by siteGeo, sum revenue
    __pr = __pr.groupby('siteGeo', as_index=False)[
        'converted_revenue'].sum()

    # Merge report last 30 days + BQ table postbacks revenue
    __fl = __rl.merge(__pr, how='left', on='siteGeo')

    # Make total_revenue column
    __fl['total_revenue'] = __fl['ad_exchange_line_item_level_revenue'].fillna(0) + __fl['converted_revenue'].fillna(0)

    # Make siteGeo_eCPM column - Add 1 to avoid division by 0
    __fl['siteGeo_eCPM'] = __fl['total_revenue'] * 1000 / (__fl['total_line_item_level_impressions'] + 1)

    # Filter relevant columns
    __fl = __fl.loc[:, ['siteGeo', 'siteGeo_eCPM']]

    """
    # Step3: Compute potential revenue => unfilled impressions / 1000 * eCPM siteGeo wise.
    """

    # Merge eCPM dataframe with report data
    __fy = __ry.merge(__fl, how='left', on='siteGeo')

    # Compute potential revenue
    __fy['potential_revenue'] = __fy['total_inventory_level_unfilled_impressions'] / 1000 * __fy['siteGeo_eCPM']

    # Save to BigQuery
    save_to_bq(
        __fy,
        project='madrid-investing',
        dataset='DATA_LAKE_MODELING_US',
        filename='unfilled_imps_report_yesterday'
    )
