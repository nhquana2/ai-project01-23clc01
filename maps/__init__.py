import json 
from typing import Dict
from definition.vehicle import Vehicle
from definition.board import Board

def load_map(file_name: str) -> Board:
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON from file {file_name}: {e}")
    
    vehicle_dict: Dict[int, Vehicle] = {}

    for vehicle_data in data:
        if not all(key in vehicle_data for key in ('id', 'length', 'orientation', 'row', 'col')):
            raise ValueError("Each vehicle must have 'id', 'length', 'orientation', 'row', and 'col' keys.")
        
        vehicle_id = int(vehicle_data['id']) 
        length = int(vehicle_data['length'])
        orientation = str(vehicle_data['orientation'])
        row = int(vehicle_data['row'])
        col = int(vehicle_data['col'])

        tmp_vehicle = Vehicle(length, orientation, row, col)

        vehicle_dict[vehicle_id] = tmp_vehicle 

    return Board(vehicle_dict)
    
    










    