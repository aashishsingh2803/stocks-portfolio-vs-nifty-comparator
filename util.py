from datetime import datetime
import pandas as pd
import glob

def parse_date(date_string):
  parsed_date = str(datetime.strptime(date_string, "%b %d, %Y")
                    .date())
  return parsed_date


def merge_multiple_csv(path):
  """_summary_

  Args:
      path (string): contains path of all the files using wildcard
      eg. "users/aashish/zerodha/*.csv"
  """
  csv_files = glob.glob(path)
  # Initialize an empty DataFrame to store the merged data
  merged_data = pd.DataFrame()

  # Loop through each CSV file and append its data to the merged DataFrame
  for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    merged_data = merged_data.append(df, ignore_index=True)
    
  parent_folder = '/'.join(path.split('/')[:-1])
  
  merged_data.to_csv(f'{parent_folder}/all_trades/trades.csv', index=False)

merge_multiple_csv("users/aashish/zerodha/*.csv")
