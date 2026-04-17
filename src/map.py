import pygame
import sys
import os

# 导入屏幕宽度和高度常量
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

class MapSystem:
    def __init__(self):
        # 统一的样式设置
        bg_color = (220, 180, 140)  # 木色背景
        text_color = (80, 40, 0)    # 深棕色文字
        border_color = (150, 100, 50)  # 边框颜色
        
        # 地图大小设置
        self.map_width = SCREEN_WIDTH
        self.map_height = SCREEN_HEIGHT
        
        # 加载地图图像
        map_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'map.png')
        try:
            if os.path.exists(map_path):
                self.map_image = pygame.image.load(map_path)
            else:
                self.map_image = None
                print(f"地图图像文件不存在: {map_path}")
        except Exception as e:
            print(f"加载地图图像失败: {e}")
            self.map_image = None
        
        # 加载关闭按钮图像
        close_button_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'close_map_button.png')
        try:
            if os.path.exists(close_button_path):
                self.close_button = pygame.image.load(close_button_path)
            else:
                self.close_button = None
                print(f"关闭按钮图像文件不存在: {close_button_path}")
        except Exception as e:
            print(f"加载关闭按钮图像失败: {e}")
            self.close_button = None
        
        # 计算关闭按钮位置（右上角）
        self.close_button_rect = None
        if self.close_button:
            # 缩小关闭按钮的大小
            button_width = int(self.close_button.get_width() * 0.7)
            button_height = int(self.close_button.get_height() * 0.7)
            self.close_button_rect = pygame.Rect(SCREEN_WIDTH - button_width - 265, 170, button_width, button_height)
        
        self.areas = {
            'teaching': {
                'name': '教学区',
                'rect': pygame.Rect(450, 220, 80, 50),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color,
                'actions': [
                    {'name': '上课', 'effects': {'knowledge': 10, 'skill': 2}},
                    {'name': '自习', 'effects': {'knowledge': 5, 'skill': 1}}
                ]
            },
            'food': {
                'name': '超市',
                'rect': pygame.Rect(600, 260, 65, 50),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color,
                'actions': [
                    {'name': '购物', 'effects': {'living_expenses': -20, 'mood': 5}},
                    {'name': '休息', 'effects': {'mood': 10}}
                ]
            },
            'sports': {
                'name': '运动场',
                'rect': pygame.Rect(610, 320, 80, 50),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color,
                'actions': [
                    {'name': '锻炼', 'effects': {'physical': 10, 'health': 5}},
                    {'name': '比赛', 'effects': {'physical': 5, 'reputation': 2}}
                ]
            },
            'canteen': {
                'name': '食堂',
                'rect': pygame.Rect(450, 460, 65, 50),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color,
                'actions': [
                    {'name': '就餐', 'effects': {'living_expenses': -15, 'mood': 8, 'health': 3}},
                    {'name': '社交', 'effects': {'charm': 5, 'social': 3}}
                ]
            },
            'supermarket': {
                'name': '学生活动中心',
                'rect': pygame.Rect(550,390, 150, 45),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color,
                'actions': [
                    {'name': '参加活动', 'effects': {'charm': 8, 'social': 5, 'reputation': 2}},
                    {'name': '组织活动', 'effects': {'charm': 5, 'social': 8, 'reputation': 3}}
                ]
            },
            'dorm': {
                'name': '宿舍',
                'rect': pygame.Rect(610, 450, 65, 50),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color,
                'actions': [
                    {'name': '休息', 'effects': {'mood': 15, 'health': 10}},
                    {'name': '学习', 'effects': {'knowledge': 3, 'skill': 2}}
                ]
            },
            'hospital': {
                'name': '校医院',
                'rect': pygame.Rect(760, 450, 80, 50),
                'bg_color': bg_color,
                'text_color': text_color,
                'border_color': border_color,
                'actions': [
                    {'name': '治疗', 'effects': {'living_expenses': -30, 'health': 20}},
                    {'name': '体检', 'effects': {'living_expenses': -10, 'health': 5}}
                ]
            }
        }
        self.active_area = None
        self.show_map = False
    
    def get_area_at(self, pos, is_sick=False):
        for area_id, area in self.areas.items():
            # 生病时只检测校医院
            if is_sick and area_id != 'hospital':
                continue
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
    
    def is_close_button_clicked(self, pos):
        """检测是否点击了关闭按钮"""
        if self.close_button_rect:
            return self.close_button_rect.collidepoint(pos)
        return False
    
    def set_map_size(self, width, height):
        """设置地图大小
        
        Args:
            width: 地图宽度
            height: 地图高度
        """
        self.map_width = width
        self.map_height = height
        
        # 重新计算关闭按钮位置和大小
        if self.close_button:
            # 缩小关闭按钮的大小
            button_width = int(self.close_button.get_width() * 0.7)
            button_height = int(self.close_button.get_height() * 0.7)
            self.close_button_rect = pygame.Rect(width - button_width - 20, 20, button_width, button_height)