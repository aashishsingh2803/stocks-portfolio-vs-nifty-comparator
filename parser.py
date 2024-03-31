import csv
import json

from util import parse_date


def get_nifty_data(filepath='data/nifty_data.json'):
  """
    Returns dict for nifty data 
    {'2023-02-01': 23540.2121, '2023-02-02': 23452.121212}
  """
  
  with open(filepath, 'r') as file:
    nifty_data = json.load(file)
  parsed_nifty_data = {}
  for day_data in nifty_data['data']:
    date_string = parse_date(day_data['rowDate'])
    parsed_nifty_data[date_string] = float(day_data['last_closeRaw'])
  
  return parsed_nifty_data
    
  

def sort_trade_data(list_of_trades):
  """ Sort trade data based on trade date

  Args:
      list_of_trades ([{}, {}]): list of trades

  Returns:
      list_of_trades ([{}, {}]): Sorted list of trades based on trade_date
  """
  return sorted(list_of_trades, key=lambda x: x['trade_date'])

  
  
def get_zerodha_data(user):
  """_summary_

  Args:
      user (string): user name e.g aashish

  Returns:
      extracted_zerodha_data: [{'trade_date': '2022-03-25', 'quantity': '2.0', 'price': '1720.0'}, {.....}]
  """
  filepath = f"users/{user}/zerodha/all_trades/trades.csv"

  fields_to_extract = ["trade_date", "quantity", "price", "trade_type"]
  try:
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # Get the header row to determine field indices
        header = next(reader)
        field_indices = [header.index(field) for field in fields_to_extract]
        
        # Extract the desired fields from each row
        extracted_data = []
        for row in reader:
            extracted_row = {fields_to_extract[idx]: row[csv_idx] for idx, csv_idx in enumerate(field_indices)}
            extracted_row['quantity'] = float(extracted_row['quantity'])
            extracted_row['price'] = float(extracted_row['price'])  
            extracted_row['total_amount'] = extracted_row['quantity'] * extracted_row['price']
            extracted_data.append(extracted_row)

        return sort_trade_data(extracted_data)
  except FileNotFoundError:
    print("Error: CSV file not found")
  except csv.Error as e:
    print(f"Error reading CSV file: {e}")

  
  
get_zerodha_data('aashish')
    
  
  
  