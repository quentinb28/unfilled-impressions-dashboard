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

from src.gcp_function import gcp_function


if __name__ == '__main__':

    # Execute gcp function
    gcp_function()
