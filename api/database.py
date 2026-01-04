import json
import copy

class Database:
    def __init__(self, data_file="data/music_genres.json"):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_all(self):
        return copy.deepcopy(self.data)
    
    def get_by_id(self, genre_id):
        genre_id = int(genre_id)
        for item in self.data:
            if item['genre_id'] == genre_id:
                return copy.deepcopy(item)
        return None
    
    def get_by_era(self, era):
        return [copy.deepcopy(item) for item in self.data 
                if era.lower() in item['era_of_origin'].lower()]
    
    def get_by_country(self, country):
        return [copy.deepcopy(item) for item in self.data 
                if country.lower() in item['origin_country'].lower()]
    
    def get_by_artist(self, artist_name):
        return [copy.deepcopy(item) for item in self.data 
                if artist_name.lower() in item['artist'].lower()]
    
    def create(self, item):
        max_id = max([i['genre_id'] for i in self.data])
        item['genre_id'] = max_id + 1
        self.data.append(item)
        self.save_data()
        return item
    
    def update(self, genre_id, update_data):
        genre_id = int(genre_id)
        for i, item in enumerate(self.data):
            if item['genre_id'] == genre_id:
                update_data['genre_id'] = genre_id
                if 'subgenres' not in update_data:
                    update_data['subgenres'] = item.get('subgenres', [])
                self.data[i] = update_data
                self.save_data()
                return update_data
        return None
    
    def delete(self, genre_id):
        genre_id = int(genre_id)
        for i, item in enumerate(self.data):
            if item['genre_id'] == genre_id:
                deleted = self.data.pop(i)
                self.save_data()
                return deleted
        return None