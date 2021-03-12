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

## 2. Techniques

The technique was to collect and visualize those unfilled impressions. Then the idea was to compute the average eCPM (Rate * Events * 1000 / Impressions) over the last 30-day period per each SiteGeo combination and multiply that by the number of unfilled impressions to represent the opportunity cost.

## 3. Action

A Tableau dashboard was built to visualize those unfilled impressions in addition to the current day and month. Then the opportunity cost was computed:

* Step 1: Get report of yesterday unfilled impressions from Ad Manager using Python.
* Step 2: Compute average eCPM per each SiteGeo combination with last 30-day data.
* Step 3: Compute the opportunity cost / potential revenue => unfilled impressions / 1000 * eCPM.

## 4. Results

The solution enables us to prioritize and make our decisions not only on the highest number of unfilled impressions but also on the highest opportunity cost.

## 4. Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

Please keep in mind that some of these projects might not be relevant anymore,
as our processes constantly evolve.

## 5. Licensing

Copyright © Investing.com . All rights reserved.
