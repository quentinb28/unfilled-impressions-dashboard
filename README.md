<h1 align="center">
  Unfilled Impressions Dashboard
</p>

<img src="https://github.com/quentinb28/unfilled-impressions-dashboard/blob/main/images/unfilled-impressions-dashboard.gif" width=100%>

<p align="center">
 <img src="https://img.shields.io/badge/admanager-v2021-pink.svg" />
 <img src="https://img.shields.io/badge/python-v3.7-yellow.svg" />
 <img src="https://img.shields.io/badge/tableau-v2019-informational.svg" />
</p>

## Table of Contents

1. [Project Objectives](#Project-Objectives)
2. [Resources / Tools](#Resources-/-Tools)
3. [Data Collection](#Data-Collection)
4. [Tableau Dashboard](#Tableau-Dashboard)
5. [Contributing](#Contributing)
6. [Licensing](#Licensing)

## 1. Project Objectives

* Collect Ad Manager report data
* Estimate average eCPM per Country Site
* Save table to Google BigQuery
* Create a dynamic Tableau visual

## 2. Resources / Tools

* Ad Manager
* Python
* Tableau

## 3. Data Collection

* Create Ad Manager class: [GAM class](https://github.com/quentinb28/unfilled-impressions-dashboard/blob/main/src/gam_class.py)
* Build GCP function: [GCP function](https://github.com/quentinb28/unfilled-impressions-dashboard/blob/main/src/gcp_function.py)
  * Step 1: Get report yesterday of unfilled impressions per ad unit.
  * Step 2: Get average eCPM last 30 days per siteGeo.
  * Step 3: Compute potential revenue => unfilled impressions / 1000 * eCPM siteGeo wise.

## 4. Tableau Dashboard



## 5. Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

Please keep in mind that some of these projects might not be relevant anymore,
as our processes constantly evolve.

## 6. Licensing

Copyright © Investing.com . All rights reserved.
