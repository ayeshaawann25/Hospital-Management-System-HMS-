# storage.py
import json
import os
from datetime import datetime

class Storage:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self._ensure_directory()
    
    def _ensure_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _get_file_path(self, entity):
        return os.path.join(self.data_dir, f'{entity}.json')
    
    def save(self, entity, data):
        file_path = self._get_file_path(entity)
        existing_data = self.load(entity)
        
        # If data is a list, merge or replace
        if isinstance(data, list):
            # Replace entire list
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            # Single item - add to existing
            existing_data.append(data)
            with open(file_path, 'w') as f:
                json.dump(existing_data, f, indent=2)
    
    def load(self, entity):
        file_path = self._get_file_path(entity)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_all(self, entity, data_list):
        file_path = self._get_file_path(entity)
        with open(file_path, 'w') as f:
            json.dump(data_list, f, indent=2)
    
    def delete(self, entity, item_id):
        data = self.load(entity)
        data = [item for item in data if item.get('id') != item_id]
        self.save_all(entity, data)
        return True
    
    def find(self, entity, item_id):
        data = self.load(entity)
        for item in data:
            if item.get('id') == item_id:
                return item
        return None
    
    def update(self, entity, item_id, updated_data):
        data = self.load(entity)
        for i, item in enumerate(data):
            if item.get('id') == item_id:
                data[i] = updated_data
                self.save_all(entity, data)
                return True
        return False
