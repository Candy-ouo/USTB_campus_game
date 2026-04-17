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
        self.action_font = None  # 行动属性字体
        self.attribute_bg = None
        # 加载UI图片
        self.ui_top_button = None
        self.life_propertise_icon = None
        self.map_icon = None
        self.scedule_icon = None
        self.file_icon = None
        self.bag_icon = None
        self.relationship_icon = None
        # 时间季节面板相关属性
        self.time_panel_bg = None
        self.season_icons = {}
        self.year = 1
        self.month = 9
        self.week = 1
        # 初始化字体和图片
        self._initialize_fonts()
        self._load_attribute_background()
        self._load_ui_images()
        self._load_time_season_images()
    
    def _initialize_fonts(self):
        """初始化字体（只初始化一次）"""
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'fonts_start.ttf')
        cute_font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'cute.ttf')
        try:
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 20)
                self.large_font = pygame.font.Font(font_path, 24)
                self.action_font = pygame.font.Font(cute_font_path, 36)  # 行动属性字体，大小可单独修改
            else:
                font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'msyh.ttf')
                if os.path.exists(font_path):
                    self.font = pygame.font.Font(font_path, 18)
                    self.large_font = pygame.font.Font(font_path, 24)
                    self.action_font = pygame.font.Font(cute_font_path, 36)  # 行动属性字体，大小可单独修改
                else:
                    self.font = pygame.font.SysFont('SimHei', 18)
                    self.large_font = pygame.font.SysFont('SimHei', 24)
                    self.action_font = pygame.font.SysFont(cute_font_path, 36)  # 行动属性字体，大小可单独修改
        except:
            self.font = pygame.font.Font(None, 18)
            self.large_font = pygame.font.Font(None, 24)
            self.action_font = pygame.font.Font(cute_font_path, 36)  # 行动属性字体，大小可单独修改
    
    def _load_attribute_background(self):
        """加载属性框背景图片"""
        bg_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'propertise_box.png')
        try:
            if os.path.exists(bg_path):
                self.attribute_bg = pygame.image.load(bg_path)
        except Exception as e:
            print(f"加载属性框背景失败: {e}")
    
    def _load_ui_images(self):
        """加载UI图片"""
        # 加载ui_top_button.png
        ui_top_button_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'ui_top_bottom.png')
        try:
            if os.path.exists(ui_top_button_path):
                self.ui_top_button = pygame.image.load(ui_top_button_path)
        except Exception as e:
            print(f"加载ui_top_button.png失败: {e}")
        
        # 加载life_propertise_icon.png
        life_propertise_icon_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'life_propertise_icon.png')
        try:
            if os.path.exists(life_propertise_icon_path):
                self.life_propertise_icon = pygame.image.load(life_propertise_icon_path)
        except Exception as e:
            print(f"加载life_propertise_icon.png失败: {e}")
        
        # 加载map_icon.png
        map_icon_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'map_icon.png')
        try:
            if os.path.exists(map_icon_path):
                self.map_icon = pygame.image.load(map_icon_path)
        except Exception as e:
            print(f"加载map_icon.png失败: {e}")
        
        # 加载scedule_icon.png
        scedule_icon_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'scedule_icon.png')
        try:
            if os.path.exists(scedule_icon_path):
                self.scedule_icon = pygame.image.load(scedule_icon_path)
        except Exception as e:
            print(f"加载scedule_icon.png失败: {e}")
        
        # 加载file_icon.png
        file_icon_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'file_icon.png')
        try:
            if os.path.exists(file_icon_path):
                self.file_icon = pygame.image.load(file_icon_path)
        except Exception as e:
            print(f"加载file_icon.png失败: {e}")
        
        # 加载bag_icon.png
        bag_icon_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'bag_icon.png')
        try:
            if os.path.exists(bag_icon_path):
                self.bag_icon = pygame.image.load(bag_icon_path)
        except Exception as e:
            print(f"加载bag_icon.png失败: {e}")
        
        # 加载relationship_icon.png
        relationship_icon_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'relationship_icon.png')
        try:
            if os.path.exists(relationship_icon_path):
                self.relationship_icon = pygame.image.load(relationship_icon_path)
        except Exception as e:
            print(f"加载relationship_icon.png失败: {e}")
    
    def _load_time_season_images(self):
        """加载时间季节面板图片"""
        # 加载时间框背景
        time_box_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'time_box.png')
        try:
            if os.path.exists(time_box_path):
                self.time_panel_bg = pygame.image.load(time_box_path)
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
    
    def update_time(self, year, month, week):
        """更新时间信息"""
        self.year = year
        self.month = month
        self.week = week
    
    def draw_time(self, time_display):
        """绘制时间信息（左上角）"""
        text = self.large_font.render(time_display, True, WHITE)
        self.screen.blit(text, (20, 20))
    
    def draw_time_season_panel(self):
        """绘制时间季节面板"""
        if not self.time_panel_bg:
            return
        
        # 绘制面板背景
        self.screen.blit(self.time_panel_bg, (0, 0))
        
        # 获取季节并绘制季节图标
        season = self._get_season_by_month(self.month)
        if season in self.season_icons:
            icon = self.season_icons[season]
            # 计算图标位置（左侧）
            icon_x = 6
            icon_y = 6
            self.screen.blit(icon, (icon_x, icon_y))
        
        # 绘制时间信息（右侧，靠右垂直居中）
        panel_width, panel_height = self.time_panel_bg.get_size()
        text_x = panel_width - 140  # 右侧边距
        line_height = 36
        total_text_height = line_height * 3  # 三行文本的总高度
        
        # 计算起始Y坐标，使文本块垂直居中
        text_y = (panel_height - total_text_height) // 2
        
        # 第x年
        year_text = self.font.render(f"第{self.year}年", True, (0, 0, 0))
        self.screen.blit(year_text, (text_x, text_y))
        
        # x月
        month_text = self.font.render(f"{self.month}月", True, (0, 0, 0))
        self.screen.blit(month_text, (text_x, text_y + line_height))
        
        # 第x周或期末周
        if isinstance(self.week, str) and self.week == "期末周":
            week_text = self.font.render("期末周", True, (0, 0, 0))
        else:
            week_text = self.font.render(f"第{self.week}周", True, (0, 0, 0))
        self.screen.blit(week_text, (text_x, text_y + line_height * 2))
    
    def draw_action_attributes(self, living_expenses, action_points, mood, health, player):
        """绘制行动属性（顶部中间）"""
        # 每个属性的Y坐标，可以根据需要修改
        y_offset = 36
        line_spacing = 25
        
        # 绘制生活费
        expense_text = self.action_font.render(f"{living_expenses}", True, (225, 182, 83))
        expense_rect = expense_text.get_rect(center=(360, y_offset))
        self.screen.blit(expense_text, expense_rect)
        
        # 绘制行动力
        if player.health < 40:
            max_action_points = 0
        else:
            max_action_points = 5 + (player.physical_level - 1)
            if player.health < 60:
                max_action_points = max(1, max_action_points // 2)
        action_text = self.action_font.render(f"{action_points}/{max_action_points}", True, (225, 182, 83))
        action_rect = action_text.get_rect(center=(580, y_offset))
        self.screen.blit(action_text, action_rect)
        
        # 绘制心情
        mood_text = self.action_font.render(f"{mood}/100", True, (225, 182, 83))
        mood_rect = mood_text.get_rect(center=(875, y_offset))
        self.screen.blit(mood_text, mood_rect)
        
        # 绘制健康值
        health_text = self.action_font.render(f"{health}/100", True, (225, 182, 83))
        health_rect = health_text.get_rect(center=(1110, y_offset))
        self.screen.blit(health_text, health_rect)
    
    def draw_main_attributes(self, knowledge, knowledge_level, charm, charm_level, physical, physical_level, skill, social, reputation, mood=100):
        """绘制主属性和副属性（左下角）"""
        # 调整位置，确保在窗口左下角
        margin = 0
        
        # 绘制属性框背景（只一个）
        bg_height = 200  # 默认高度
        if self.attribute_bg:
            bg_width, bg_height = self.attribute_bg.get_size()
            # 绘制主属性背景框在左下角
            self.screen.blit(self.attribute_bg, (margin, SCREEN_HEIGHT - bg_height - margin))
        
        # 计算垂直位置，确保从上到下垂直排列
        total_attributes = 6  # 主属性3个 + 副属性3个
        start_y = SCREEN_HEIGHT - bg_height - margin + 92  # 从属性框顶部开始，留出一些边距
        
        # 技能
        skill_text = self.font.render(f"{skill}", True, (95, 58, 31)) 
        self.screen.blit(skill_text, (30, start_y))
        
        # 人脉
        social_text = self.font.render(f"{social}", True, (95, 58, 31))  
        self.screen.blit(social_text, (95, start_y))
        
        # 声望
        reputation_text = self.font.render(f"{reputation}", True, (95, 58, 31))  
        self.screen.blit(reputation_text, (160, start_y))
        
        # 心情影响：心情低于50时，属性显示上限为50，当前值为实际值的一半
        if mood < 50:
            # 学识
            display_knowledge = int(knowledge * 0.5)
            knowledge_text = self.font.render(f"LV{knowledge_level} {display_knowledge}/50", True, (60, 172, 100))  # 绿色
            self.screen.blit(knowledge_text, (65, start_y + 30))
            
            # 魅力
            display_charm = int(charm * 0.5)
            charm_text = self.font.render(f"LV{charm_level} {display_charm}/50", True, (252, 173, 72))  # 黄色
            self.screen.blit(charm_text, (65, start_y + 75))
            
            # 体能
            display_physical = int(physical * 0.5)
            physical_text = self.font.render(f"LV{physical_level} {display_physical}/50", True, (186, 50, 50))  # 红色
            self.screen.blit(physical_text, (65, start_y + 115))
        else:
            # 学识
            knowledge_text = self.font.render(f"LV{knowledge_level} {knowledge}/100", True, (60, 172, 100))  # 绿色
            self.screen.blit(knowledge_text, (65, start_y + 30))
            
            # 魅力
            charm_text = self.font.render(f"LV{charm_level} {charm}/100", True, (252, 173, 72))  # 黄色
            self.screen.blit(charm_text, (65, start_y + 75))
            
            # 体能
            physical_text = self.font.render(f"LV{physical_level} {physical}/100", True, (186, 50, 50))  # 红色
            self.screen.blit(physical_text, (65, start_y + 115))
        
        
    
    def draw_secondary_attributes(self, skill, social, reputation):
        """绘制副属性（主属性下方）"""
        # 副属性现在在draw_main_attributes中一起绘制，避免重叠
        pass
    
    def draw_all(self, time_display, player):
        """绘制所有UI元素"""
        # 绘制ui_top_button作为界面的上下框（位于底部）
        if self.ui_top_button:
            # 绘制顶部框
            self.screen.blit(self.ui_top_button, (0, 0))
            
        # 绘制时间季节面板（在ui_top_button之上）
        self.draw_time_season_panel()
        
        # 绘制life_propertise_icon在页面顶部
        if self.life_propertise_icon:
            life_propertise_icon_width = self.life_propertise_icon.get_width()
            life_propertise_icon_height = self.life_propertise_icon.get_height()
            # 绘制在顶部中央
            self.screen.blit(self.life_propertise_icon, (
                SCREEN_WIDTH // 2 - life_propertise_icon_width // 2 + 10,
                6
            ))
        
        # 绘制map_icon和scedule_icon在页面右侧靠下的位置
        if self.map_icon:
            self.map_icon_rect = pygame.Rect(
                SCREEN_WIDTH - self.map_icon.get_width() - 10,
                SCREEN_HEIGHT - self.map_icon.get_height() - 165,
                self.map_icon.get_width(),
                self.map_icon.get_height()
            )
            self.screen.blit(self.map_icon, self.map_icon_rect)
        
        if self.scedule_icon:
            self.scedule_icon_rect = pygame.Rect(
                SCREEN_WIDTH - self.scedule_icon.get_width() - 10,
                SCREEN_HEIGHT - self.scedule_icon.get_height() - 65,
                self.scedule_icon.get_width(),
                self.scedule_icon.get_height()
            )
            self.screen.blit(self.scedule_icon, self.scedule_icon_rect)
        
        # 绘制file_icon，bag_icon，relationship_icon在页面底部
        icon_spacing = 20
        bottom_margin = 8
        
        if self.file_icon:
            self.file_icon_rect = pygame.Rect(
                210,
                SCREEN_HEIGHT - self.file_icon.get_height() - bottom_margin,
                self.file_icon.get_width(),
                self.file_icon.get_height()
            )
            self.screen.blit(self.file_icon, self.file_icon_rect)
        
        if self.bag_icon:
            self.bag_icon_rect = pygame.Rect(
                210 + (self.file_icon.get_width() if self.file_icon else 0) + icon_spacing,
                SCREEN_HEIGHT - self.bag_icon.get_height() - bottom_margin,
                self.bag_icon.get_width(),
                self.bag_icon.get_height()
            )
            self.screen.blit(self.bag_icon, self.bag_icon_rect)
        
        if self.relationship_icon:
            self.relationship_icon_rect = pygame.Rect(
                210 + (self.file_icon.get_width() if self.file_icon else 0) + (self.bag_icon.get_width() if self.bag_icon else 0) + icon_spacing * 2,
                SCREEN_HEIGHT - self.relationship_icon.get_height() - bottom_margin,
                self.relationship_icon.get_width(),
                self.relationship_icon.get_height()
            )
            self.screen.blit(self.relationship_icon, self.relationship_icon_rect)
        
        # 绘制行动属性
        living_expenses = player.get_living_expenses()
        action_points = player.get_action_points()
        mood = player.get_mood()
        health = player.get_health()
        self.draw_action_attributes(living_expenses, action_points, mood, health, player)
        
        # 绘制主属性和副属性（一起绘制，避免重叠）
        knowledge, knowledge_level = player.get_knowledge()
        charm, charm_level = player.get_charm()
        physical, physical_level = player.get_physical()
        skill = player.get_skill()
        social = player.get_social()
        reputation = player.get_reputation()
        mood = player.get_mood()
        self.draw_main_attributes(knowledge, knowledge_level, charm, charm_level, physical, physical_level, skill, social, reputation, mood)
    
    def handle_events(self, events):
        """处理UI事件"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 检查是否点击了map_icon
                if hasattr(self, 'map_icon_rect') and self.map_icon_rect.collidepoint(mouse_pos):
                    return 'MAP'
                # 检查是否点击了scedule_icon
                if hasattr(self, 'scedule_icon_rect') and self.scedule_icon_rect.collidepoint(mouse_pos):
                    return 'SCHEDULE'
                # 检查是否点击了file_icon
                if hasattr(self, 'file_icon_rect') and self.file_icon_rect.collidepoint(mouse_pos):
                    return 'FILE'
                # 检查是否点击了bag_icon
                if hasattr(self, 'bag_icon_rect') and self.bag_icon_rect.collidepoint(mouse_pos):
                    return 'BAG'
                # 检查是否点击了relationship_icon
                if hasattr(self, 'relationship_icon_rect') and self.relationship_icon_rect.collidepoint(mouse_pos):
                    return 'RELATIONSHIP'
        return None
