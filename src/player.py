import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.config import INITIAL_ATTRIBUTES, ATTRIBUTE_MAX, ATTRIBUTE_MIN


class Player:
    def __init__(self):
        self.attributes = INITIAL_ATTRIBUTES.copy()
        self.action_points = 0
    
    def reset(self):
        self.attributes = INITIAL_ATTRIBUTES.copy()
        self.action_points = 0
    
    def change_attribute(self, attr_name, amount):
        if attr_name not in self.attributes:
            return False
        
        new_value = self.attributes[attr_name] + amount
        if attr_name in ATTRIBUTE_MAX:
            new_value = min(new_value, ATTRIBUTE_MAX[attr_name])
        if attr_name in ATTRIBUTE_MIN:
            new_value = max(new_value, ATTRIBUTE_MIN[attr_name])
        
        self.attributes[attr_name] = new_value
        return True
    
    def get_attribute(self, attr_name):
        return self.attributes.get(attr_name, 0)
    
    def set_attribute(self, attr_name, value):
        if attr_name not in self.attributes:
            return False
        
        if attr_name in ATTRIBUTE_MAX:
            value = min(value, ATTRIBUTE_MAX[attr_name])
        if attr_name in ATTRIBUTE_MIN:
            value = max(value, ATTRIBUTE_MIN[attr_name])
        
        self.attributes[attr_name] = value
        return True
    
    def to_dict(self):
        return {
            'attributes': self.attributes,
            'action_points': self.action_points
        }
    
    def from_dict(self, data):
        if 'attributes' in data:
            self.attributes = data['attributes']
        if 'action_points' in data:
            self.action_points = data['action_points']
