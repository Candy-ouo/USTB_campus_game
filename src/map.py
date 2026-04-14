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
                'rect': pygame.Rect(50, 20, 300, 220),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'food': {
                'name': '超市',
                'rect': pygame.Rect(650, 125, 100, 100),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'sports': {
                'name': '运动场',
                'rect': pygame.Rect(600, 240, 300, 220),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'canteen': {
                'name': '食堂',
                'rect': pygame.Rect(380, 500, 100, 100),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'supermarket': {
                'name': '学生活动中心',
                'rect': pygame.Rect(570,460, 200, 70),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'dorm': {
                'name': '宿舍',
                'rect': pygame.Rect(590, 550, 150, 120),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color
            },
            'hospital': {
                'name': '校医院',
                'rect': pygame.Rect(880, 600, 160, 110),
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