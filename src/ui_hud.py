import pygame
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE


class UIHUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = None
        self.large_font = None
        self.attribute_bg = None
        self._initialize_fonts()
        self._load_attribute_background()
    
    def _initialize_fonts(self):
        """初始化字体（只初始化一次）"""
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'fonts_start.ttf')
        try:
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 20)
                self.large_font = pygame.font.Font(font_path, 24)
            else:
                font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'msyh.ttf')
                if os.path.exists(font_path):
                    self.font = pygame.font.Font(font_path, 18)
                    self.large_font = pygame.font.Font(font_path, 24)
                else:
                    self.font = pygame.font.SysFont('SimHei', 18)
                    self.large_font = pygame.font.SysFont('SimHei', 24)
        except:
            self.font = pygame.font.Font(None, 18)
            self.large_font = pygame.font.Font(None, 24)
    
    def _load_attribute_background(self):
        """加载属性框背景图片"""
        bg_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'propertise_box.png')
        try:
            if os.path.exists(bg_path):
                self.attribute_bg = pygame.image.load(bg_path)
        except Exception as e:
            print(f"加载属性框背景失败: {e}")
    
    def draw_time(self, time_display):
        """绘制时间信息（左上角）"""
        text = self.large_font.render(time_display, True, WHITE)
        self.screen.blit(text, (20, 20))
    
    def draw_action_attributes(self, living_expenses, action_points, mood):
        """绘制行动属性（顶部中间）"""
        text = self.font.render(f"生活费：{living_expenses}  行动力：{action_points}  心情：{mood}/100", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(text, text_rect)
    
    def draw_main_attributes(self, knowledge, knowledge_level, charm, charm_level, physical, physical_level, skill, social, reputation):
        """绘制主属性和副属性（左下角）"""
        # 调整位置，确保在窗口内
        y_offset = SCREEN_HEIGHT - 300  # 向上调整，确保完全显示
        
        # 绘制属性框背景（只一个）
        bg_height = 200  # 默认高度
        if self.attribute_bg:
            bg_width, bg_height = self.attribute_bg.get_size()
            # 绘制主属性背景框
            self.screen.blit(self.attribute_bg, (10, y_offset - 10))
        
        # 计算垂直居中位置，确保从上到下垂直排列
        total_attributes = 6  # 主属性3个 + 副属性3个
        line_height = 40  # 减小行高，避免重叠
        start_y = y_offset + 20  # 从属性框顶部开始，留出一些边距
        
        # 学识
        knowledge_text = self.font.render(f"学识 LV{knowledge_level} {knowledge}/100", True, (0, 0, 0))  # 黑色
        self.screen.blit(knowledge_text, (20, start_y))
        
        # 魅力
        charm_text = self.font.render(f"魅力 LV{charm_level} {charm}/100", True, (0, 0, 0))  # 黑色
        self.screen.blit(charm_text, (20, start_y + line_height))
        
        # 体能
        physical_text = self.font.render(f"体能 LV{physical_level} {physical}/100", True, (0, 0, 0))  # 黑色
        self.screen.blit(physical_text, (20, start_y + line_height * 2))
        
        # 技能
        skill_text = self.font.render(f"技能：{skill}", True, (0, 0, 0))  # 黑色
        self.screen.blit(skill_text, (20, start_y + line_height * 3))
        
        # 人脉
        social_text = self.font.render(f"人脉：{social}", True, (0, 0, 0))  # 黑色
        self.screen.blit(social_text, (20, start_y + line_height * 4))
        
        # 声望
        reputation_text = self.font.render(f"声望：{reputation}", True, (0, 0, 0))  # 黑色
        self.screen.blit(reputation_text, (20, start_y + line_height * 5))
    
    def draw_secondary_attributes(self, skill, social, reputation):
        """绘制副属性（主属性下方）"""
        # 副属性现在在draw_main_attributes中一起绘制，避免重叠
        pass
    
    def draw_all(self, time_display, player):
        """绘制所有UI元素"""
        # 绘制行动属性
        living_expenses = player.get_living_expenses()
        action_points = player.get_action_points()
        mood = player.get_mood()
        self.draw_action_attributes(living_expenses, action_points, mood)
        
        # 绘制主属性和副属性（一起绘制，避免重叠）
        knowledge, knowledge_level = player.get_knowledge()
        charm, charm_level = player.get_charm()
        physical, physical_level = player.get_physical()
        skill = player.get_skill()
        social = player.get_social()
        reputation = player.get_reputation()
        self.draw_main_attributes(knowledge, knowledge_level, charm, charm_level, physical, physical_level, skill, social, reputation)
