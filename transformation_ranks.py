# Transformation, use for ranking, difficulty rates, etc.

import numpy as np
import requests

def linear_transform(data, a, b):
    # Linear Transformation with Rounding
    np_data = np.array(data)
    min_orig = np.min(np_data)
    max_orig = np.max(np_data)
    normalized_series = (np_data - min_orig) / (max_orig - min_orig)
    # scale to target
    scaled_series = a + normalized_series * (b - a)
    curved_series = np.round(scaled_series).astype(int)
    return curved_series

def exponent_transform(data, a, b):
    np_data = np.array(data)
    min_orig = np.min(np_data)
    max_orig = np.max(np_data)
    normalized_series = (np_data - min_orig) / (max_orig - min_orig)
    scaled_series = a + (b - a) * (np.exp(normalized_series) - 1) / (np.exp(1) - 1)
    curved_series = np.round(scaled_series).astype(int)
    return curved_series


# Test
def test():
    print("Processing Data Query...")
    births = get_chinese_births_by_year(2005, 2023)
    print("Birth data obtained.")
    print(births)
    births_values = list(births.values())
    print("Linear Transform:")
    print(linear_transform(births_values, 1, 5))
    print("Exponent Transform:")
    print(exponent_transform(births_values, 1, 5))
    
    
    
def fetch_data(indicator, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/CN/indicator/{indicator}?date={start_year}:{end_year}&format=json&per_page=1000"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    data = response.json()
    if len(data) < 2:
        raise Exception("No data found")
    
    return data[1]

def get_chinese_births_by_year(start_year, end_year):
    birth_rate_data = fetch_data('SP.DYN.CBRT.IN', start_year, end_year)
    population_data = fetch_data('SP.POP.TOTL', start_year, end_year)
    
    birth_rates = {entry['date']: entry['value'] for entry in birth_rate_data}
    populations = {entry['date']: entry['value'] for entry in population_data}
    
    births_by_year = {}
    for year in range(start_year, end_year + 1):
        year_str = str(year)
        if year_str in birth_rates and year_str in populations:
            birth_rate = birth_rates[year_str]
            population = populations[year_str]
            if birth_rate is not None and population is not None:
                births_by_year[year_str] = (birth_rate / 1000) * population
    
    return births_by_year


if __name__ == "__main__":
    test()