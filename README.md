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

1. [Situation](#Situation)
2. [Techniques](#Techniques)
3. [Action](#Action)
4. [Results](#Results)
5. [Contributing](#Contributing)
6. [Licensing](#Licensing)

## 1. Situation

Investing.com is a financial platform and news website; one of the top three global financial websites in the world. It offers market quotes,information about stocks, futures, options, analysis, commodities, and an economic calendar. Most of the revenue is generated through advertising; Premium and Remnant. The Remnant business models are CPL / CPA / Networks. The best bidder fills the ad request. Sometimes ad requests are not filled and generate unfilled impressions although closed deal might be avaible to run on those specific placements. This represents an opportunity cost.

## 2. Task

For this project, the tasks that were performed are, as follows:

* Collect the relevant report data for yesterday from Ad Manager (1), 
* Collect data for all Network / Affiliation activities that occurred in the last 30 days (2),
* Compute the average eCPM (Rate * Events * 1000 / Impressions) per each SiteGeo pair (3),
* Compute the expected eCPM for all unfilled impressions based on each SiteGeo pair (4).

## 3. Action

First, I built a script in Python to extract the relevant data from Ad Manager and BigQuery. Then I computed the average eCPM per SiteGeo pair with the last 30-day traffic (Impressins + Revenue) and calculated the opportunity cost for all unfilled impressions. Finally I loaded the final result to a BigQuery table and built a Tableau dashboard from it so that all the relevant stakeholders, mostly my team, could access it.

## 4. Results

The solution enables us to prioritize and make our decisions not only on the highest number of unfilled impressions but also on the highest opportunity cost.

## 4. Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

Please keep in mind that some of these projects might not be relevant anymore,
as our processes constantly evolve.

## 5. Licensing

Copyright © Investing.com . All rights reserved.
