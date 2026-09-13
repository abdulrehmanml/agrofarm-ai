import logging
import pandas as pd
from typing import Dict, Any

# Import path from our centralized config
from src.config import FIELD_STATUS_PATH

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class WeatherEngine:
    """Loads and retrieves simulated real-time field telemetry and weather metrics."""
    
    def __init__(self):
        try:
            self.field_data = pd.read_csv(FIELD_STATUS_PATH)
            logging.info("Weather & Field Engine successfully initialized.")
        except FileNotFoundError:
            logging.error(f"Field status file not found at {FIELD_STATUS_PATH}. Did you run Step 1?")
            self.field_data = None
        except Exception as e:
            logging.error(f"Failed to load field status data: {e}")
            self.field_data = None

    def get_field_status(self, field_id: str) -> Dict[str, Any]:
        """Returns the current status, crop type, and soil metrics for a specific field."""
        if self.field_data is None:
            return {"error": "Field data system is currently offline."}
            
        field_row = self.field_data[self.field_data['field_id'] == field_id.upper()]
        
        if field_row.empty:
            return {"error": f"No telemetry found for Field ID: {field_id}"}
            
        return field_row.iloc[0].to_dict()

    def get_available_fields(self) -> list:
        """Returns a list of all active field IDs for the UI dropdown."""
        if self.field_data is not None:
            return self.field_data['field_id'].tolist()
        return []

if __name__ == "__main__":
    # Quick test to verify data loading
    engine = WeatherEngine()
    print("\nTesting Field Data Retrieval for F1:")
    print(engine.get_field_status("F1"))