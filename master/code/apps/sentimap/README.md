# SentiMap

Showing sentiment analysis data on the US map. 
Uses bounding box: -124.848974,24.396308,-66.885444,49.384358 and filters on twitter API data place full_name and country_code:

So, if place is not null and country_code is "US", parse full_name and extract state. E.g. full_name "South Whittier, CA" is parsed to CA -> California