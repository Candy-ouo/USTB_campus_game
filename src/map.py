import pygame
import sys
import os

class MapSystem:
    def __init__(self):
        # 统一的样式设置
        bg_color = (220, 180, 140)  # 木色背景
        text_color = (80, 40, 0)    # 深棕色文字
        border_color = (150, 100, 50)  # 边框颜色
        
        self.areas = {
            'teaching': {
                'name': '教学区',
                'rect': pygame.Rect(100, 50, 100, 100),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'food': {
                'name': '美食街',
                'rect': pygame.Rect(370, 100, 100, 75),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'sports': {
                'name': '运动场',
                'rect': pygame.Rect(370, 220, 150, 100),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'canteen': {
                'name': '食堂',
                'rect': pygame.Rect(200, 420, 75, 75),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'supermarket': {
                'name': '超市',
                'rect': pygame.Rect(380, 390, 60, 60),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'dorm': {
                'name': '宿舍',
                'rect': pygame.Rect(360, 460, 100, 75),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'hospital': {
                'name': '校医院',
                'rect': pygame.Rect(540, 500, 100, 75),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            }
        }
        self.active_area = None
        self.show_map = False
    
    def get_area_at(self, pos):
        for area_id, area in self.areas.items():
            if area['rect'].collidepoint(pos):
                return area_id
        return None
    
    def get_area(self, area_id):
        return self.areas.get(area_id)
    
    def set_active_area(self, area_id):
        self.active_area = area_id
    
    def clear_active_area(self):
        self.active_area = None
    
    def toggle_map(self):
        self.show_map = not self.show_map
    
    def is_map_showing(self):
        return self.show_map