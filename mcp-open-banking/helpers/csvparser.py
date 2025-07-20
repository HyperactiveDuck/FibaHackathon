import csv
import pandas as pd
from typing import List, Dict, Any, Optional

class CSVParser:
    """A helper class for parsing CSV files and extracting data."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read_csv_to_dict(self, delimiter: str = ',') -> List[Dict[str, Any]]:
        """
        Read CSV file and return as list of dictionaries.
        
        Args:
            delimiter: CSV delimiter (default: ',')
            
        Returns:
            List of dictionaries where each dict represents a row
        """
        data = []
        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                for row in reader:
                    data.append(dict(row))
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found")
        except Exception as e:
            print(f"Error reading CSV: {e}")
        
        return data
    
    def read_csv_to_dataframe(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Read CSV file using pandas and return DataFrame.
        
        Args:
            **kwargs: Additional arguments for pd.read_csv()
            
        Returns:
            pandas DataFrame or None if error
        """
        try:
            return pd.read_csv(self.file_path, **kwargs)
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found")
        except Exception as e:
            print(f"Error reading CSV: {e}")
        
        return None
    
    def get_column_data(self, column_name: str) -> List[Any]:
        """
        Extract data from a specific column.
        
        Args:
            column_name: Name of the column to extract
            
        Returns:
            List of values from the specified column
        """
        df = self.read_csv_to_dataframe()
        if df is not None and column_name in df.columns:
            return df[column_name].tolist()
        return []
    
    def filter_data(self, condition: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter CSV data based on conditions.
        
        Args:
            condition: Dictionary with column:value pairs to filter on
            
        Returns:
            Filtered list of dictionaries
        """
        data = self.read_csv_to_dict()
        filtered_data = []
        
        for row in data:
            match = True
            for column, value in condition.items():
                if row.get(column) != str(value):
                    match = False
                    break
            if match:
                filtered_data.append(row)
        
        return filtered_data

# Utility functions
def parse_csv_file(file_path: str, delimiter: str = ',') -> List[Dict[str, Any]]:
    """Quick function to parse a CSV file and return data."""
    parser = CSVParser(file_path)
    return parser.read_csv_to_dict(delimiter)

def get_csv_headers(file_path: str, delimiter: str = ',') -> List[str]:
    """Get column headers from a CSV file."""
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=delimiter)
            return next(reader, [])
    except Exception as e:
        print(f"Error reading headers: {e}")
        return []