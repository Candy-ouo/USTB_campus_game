import pygame
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT


class TimeSeasonPanel:
    def __init__(self, screen):
        self.screen = screen
        self.font = None
        self.panel_bg = None
        self.season_icons = {}
        self._initialize_font()
        self._load_images()
        self.year = 1
        self.month = 9
        self.week = 1
    
    def _initialize_font(self):
        """初始化字体"""
        
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'fonts_start.ttf')
        try:
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 28)
                return
        except:
            self.font = pygame.font.Font(None, 32)
        
        # 如果本地字体都失败，尝试使用系统字体
        font_names = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
        for font_name in font_names:
            try:
                self.font = pygame.font.SysFont(font_name, 16)
                return
            except:
                continue
        
        # 最后使用默认字体
        self.font = pygame.font.Font(None, 16)
    
    def _load_images(self):
        """加载面板背景和季节图标"""
        # 加载面板背景
        panel_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'time_box.png')
        try:
            if os.path.exists(panel_path):
                self.panel_bg = pygame.image.load(panel_path)
        except Exception as e:
            print(f"加载时间框背景失败: {e}")
        
        # 加载季节图标
        seasons = ['spring', 'summer', 'autumn', 'winter']
        for season in seasons:
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'image', f'{season}_icon.png')
            try:
                if os.path.exists(icon_path):
                    self.season_icons[season] = pygame.image.load(icon_path)
            except Exception as e:
                print(f"加载{season}图标失败: {e}")
    
    def _get_season_by_month(self, month):
        """根据月份获取季节"""
        if 3 <= month <= 5:
            return 'spring'
        elif 6 <= month <= 8:
            return 'summer'
        elif 9 <= month <= 11:
            return 'autumn'
        else:  # 12, 1, 2
            return 'winter'
    
    def update(self, year, month, week):
        """更新时间信息"""
        self.year = year
        self.month = month
        self.week = week
    
    def draw(self, screen):
        """绘制时间季节面板"""
        if not self.panel_bg:
            return
        
        # 绘制面板背景
        panel_rect = self.panel_bg.get_rect(topleft=(10, 10))
        screen.blit(self.panel_bg, panel_rect)
        
        # 获取季节并绘制季节图标
        season = self._get_season_by_month(self.month)
        if season in self.season_icons:
            icon = self.season_icons[season]
            # 计算图标位置（左侧）
            icon_x = 40
            icon_y = 25
            screen.blit(icon, (icon_x, icon_y))
        
        # 绘制时间信息（右侧，靠右垂直居中）
        panel_width, panel_height = self.panel_bg.get_size()
        text_x = panel_width - 140  # 右侧边距
        text_y = 22  # 顶部边距
        line_height = 36
        
        # 第x年
        year_text = self.font.render(f"第{self.year}年", True, (0, 0, 0))
        screen.blit(year_text, (text_x, text_y))
        
        # x月
        month_text = self.font.render(f"{self.month}月", True, (0, 0, 0))
        screen.blit(month_text, (text_x, text_y + line_height))
        
        # 第x周或期末周
        if isinstance(self.week, str) and self.week == "期末周":
            week_text = self.font.render("期末周", True, (0, 0, 0))
        else:
            week_text = self.font.render(f"第{self.week}周", True, (0, 0, 0))
        screen.blit(week_text, (text_x, text_y + line_height * 2))
