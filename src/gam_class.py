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

import pandas as pd
from googleads import ad_manager, errors
from tempfile import NamedTemporaryFile
from src.gcp_bigquery import get_bq_table


# Define Google Ad Manager class

class GAM:

    @staticmethod
    def clean_column_names(df):

        # Remove dot in column names notation
        df.columns = [__c.split('.')[1].lower() for __c in list(df.columns)]

        return df

    @staticmethod
    def get_child_from_ad_unit(df):

        # Get child ad unit when possible
        df['ad_unit_name'] = df['ad_unit_name'].apply(
            lambda x: x.split(' » ')[1].split(' ')[0] if len(x.split(' » ')) > 1 else x)

        return df

    @staticmethod
    def filter_ad_unit_names(df, __f):

        return df[~df.ad_unit_name.str.contains('|'.join(__f))]

    @staticmethod
    def filter_line_items(df, __f):

        # Filter out irrelevant ad units
        return df[~df.line_item_name.str.contains('|'.join(__f))]

    @staticmethod
    def country_from_name_to_code(df):

        # Get countries table from BQ
        __cs = get_bq_table('countries', columns=['country_name', 'country_code'])

        # Merge with dataframe
        df = df.merge(__cs, how='left', on='country_name')

        return df

    @staticmethod
    def convert_to_usd(df, rates_to_usd):

        # Convert AdEx revenues from EUR to USD
        df['ad_exchange_line_item_level_revenue'] = \
            df['ad_exchange_line_item_level_revenue'] / 1000000 * rates_to_usd['EUR']

        return df

    def get_report(self, report_params, exchange_rates=None):

        # 'CUSTOM_DATE' => Needs to specify start / end dates in report job
        if report_params['dateRange'] == 'CUSTOM_DATE':

            __rj = {
                'reportQuery': {
                    'dimensions': report_params['dimensions'],
                    'columns': report_params['columns'],
                    'adUnitView': 'FLAT',
                    'dateRangeType': report_params['dateRange'],
                    'startDate': report_params['startDate'],
                    'endDate': report_params['endDate'],
                }
            }

        else:

            __rj = {
                'reportQuery': {
                    'dimensions': report_params['dimensions'],
                    'columns': report_params['columns'],
                    'adUnitView': 'FLAT',
                    'dateRangeType': report_params['dateRange']
                }
            }

        # Get report id from job
        try:
            __ri = self.data_downloader.WaitForReport(__rj)
            print(__ri)
        # Throw error if failed to get report id
        except errors.AdManagerReportError as e:
            print('Failed to generate report. Error was: %s' % e)

        # Download report data
        with NamedTemporaryFile(suffix='.csv.gz', mode='wb', delete=False) as __rf:
            self.data_downloader.DownloadReportToFile(__ri, 'CSV_DUMP', __rf)

        # Load file to a pandas dataframe
        __df = pd.read_csv(__rf.name)

        # Clean column names
        __df = self.clean_column_names(__df)

        return __df

    def __init__(self):

        # Instantiate client
        self.client = ad_manager.AdManagerClient.LoadFromStorage(path='src/googleads.yaml')

        # Instantiate data downloader
        self.data_downloader = self.client.GetDataDownloader()
