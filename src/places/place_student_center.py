import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class StudentCenter:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.student_center_background = None
        self.shixi_button = None
        self.shetuan1_button = None
        self.tiyu_button = None
        self.dance_music_button = None
        self.xueshenghuodong_button = None
        self._load_images()

    def _load_images(self):
        """加载学生活动中心背景图片"""
        student_center_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'student_center_background.png')
        try:
            if os.path.exists(student_center_path):
                self.student_center_background = pygame.image.load(student_center_path)
        except:
            pass
        
        # 加载实习按钮图片
        shixi_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'shixi_button.png')
        try:
            if os.path.exists(shixi_button_path):
                self.shixi_button = pygame.image.load(shixi_button_path)
        except:
            pass
        
        # 加载科技协会/文学社按钮图片
        shetuan1_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'shetuan1_button.png')
        try:
            if os.path.exists(shetuan1_button_path):
                self.shetuan1_button = pygame.image.load(shetuan1_button_path)
        except:
            pass
        
        # 加载体育协会按钮图片
        tiyu_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'tiyu_button.png')
        try:
            if os.path.exists(tiyu_button_path):
                self.tiyu_button = pygame.image.load(tiyu_button_path)
        except:
            pass
        
        # 加载街舞社/音乐社按钮图片
        dance_music_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'dance_music_button.png')
        try:
            if os.path.exists(dance_music_button_path):
                self.dance_music_button = pygame.image.load(dance_music_button_path)
        except:
            pass
        
        # 加载学生活动按钮图片
        xueshenghuodong_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'xueshenghuodong_button.png')
        try:
            if os.path.exists(xueshenghuodong_button_path):
                self.xueshenghuodong_button = pygame.image.load(xueshenghuodong_button_path)
        except:
            pass

    def draw(self):
        """绘制学生活动中心场景"""
        if self.student_center_background:
            scaled_bg = pygame.transform.scale(self.student_center_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)

        # 绘制科技协会/文学社按钮
        if self.shetuan1_button:
            # 保持图片原始比例，计算显示大小
            button_width = 253
            button_height = 78
            # 计算按钮位置
            self.shetuan1_button_rect = pygame.Rect(500, 150, button_width, button_height)
            # 缩放按钮图片
            scaled_button = pygame.transform.scale(self.shetuan1_button, (button_width, button_height))
            self.screen.blit(scaled_button, self.shetuan1_button_rect)
        else:
            # 如果图片加载失败，绘制默认矩形
            self.shetuan1_button_rect = pygame.Rect(600, 150, 500, 50)
            pygame.draw.rect(self.screen, (220, 180, 140), self.shetuan1_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), self.shetuan1_button_rect, 2)
            self.game.draw_text("科技协会/文学社团：学识+20 心情+10", self.shetuan1_button_rect.x + 10, self.shetuan1_button_rect.y + 10, (254, 247, 201))

        # 绘制体育协会按钮
        if self.tiyu_button:
            # 保持图片原始比例，计算显示大小
            button_width = 150
            button_height = 78
            # 计算按钮位置
            self.tiyu_button_rect = pygame.Rect(300, 450, button_width, button_height)
            # 缩放按钮图片
            scaled_button = pygame.transform.scale(self.tiyu_button, (button_width, button_height))
            self.screen.blit(scaled_button, self.tiyu_button_rect)
        else:
            # 如果图片加载失败，绘制默认矩形
            self.tiyu_button_rect = pygame.Rect(400, 200, 500, 50)
            pygame.draw.rect(self.screen, (220, 180, 140), self.tiyu_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), self.tiyu_button_rect, 2)
            self.game.draw_text("体育协会：体能+20 心情+10", self.tiyu_button_rect.x + 10, self.tiyu_button_rect.y + 10, (254, 247, 201))

        # 绘制街舞社/音乐社按钮
        if self.dance_music_button:
            # 保持图片原始比例，计算显示大小
            button_width = 215
            button_height = 78
            # 计算按钮位置
            self.dance_music_button_rect = pygame.Rect(925, 250, button_width, button_height)
            # 缩放按钮图片
            scaled_button = pygame.transform.scale(self.dance_music_button, (button_width, button_height))
            self.screen.blit(scaled_button, self.dance_music_button_rect)
        else:
            # 如果图片加载失败，绘制默认矩形
            self.dance_music_button_rect = pygame.Rect(400, 250, 500, 50)
            pygame.draw.rect(self.screen, (220, 180, 140), self.dance_music_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), self.dance_music_button_rect, 2)
            self.game.draw_text("街舞社/音乐社：魅力+20 心情+10", self.dance_music_button_rect.x + 10, self.dance_music_button_rect.y + 10, (254, 247, 201))

        # 绘制学生活动按钮
        if self.xueshenghuodong_button:
            # 保持图片原始比例，计算显示大小
            button_width = 150
            button_height = 78
            # 计算按钮位置
            self.xueshenghuodong_button_rect = pygame.Rect(925, 570, button_width, button_height)
            # 缩放按钮图片
            scaled_button = pygame.transform.scale(self.xueshenghuodong_button, (button_width, button_height))
            self.screen.blit(scaled_button, self.xueshenghuodong_button_rect)
        else:
            # 如果图片加载失败，绘制默认矩形
            self.xueshenghuodong_button_rect = pygame.Rect(400, 300, 500, 50)
            pygame.draw.rect(self.screen, (220, 180, 140), self.xueshenghuodong_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), self.xueshenghuodong_button_rect, 2)
            self.game.draw_text("学生活动：技能+20 心情+10", self.xueshenghuodong_button_rect.x + 10, self.xueshenghuodong_button_rect.y + 10, (254, 247, 201))

        # 绘制实习按钮
        if self.shixi_button:
            # 保持图片原始比例，计算显示大小
            button_width = 150
            button_height = 78
            # 计算按钮位置（居中）
            self.shixi_button_rect = pygame.Rect(
                500, 
                350, 
                button_width, 
                button_height
            )
            # 缩放按钮图片
            scaled_button = pygame.transform.scale(self.shixi_button, (button_width, button_height))
            self.screen.blit(scaled_button, self.shixi_button_rect)
        else:
            # 如果图片加载失败，绘制默认矩形
            self.shixi_button_rect = pygame.Rect(500, 350, 500, 50)
            pygame.draw.rect(self.screen, (220, 180, 140), self.shixi_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), self.shixi_button_rect, 2)
            self.game.draw_text("实习：技能+20 心情-10", self.shixi_button_rect.x + 10, self.shixi_button_rect.y + 10, (254, 247, 201))

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理学生活动中心场景事件"""
        # 计算科技协会/文学社按钮矩形
        if self.shetuan1_button:
            button_width = 253
            button_height = 78
            button_height = min(button_height, 50)
            shetuan1_button_rect = pygame.Rect(500, 150, button_width, button_height)
        else:
            shetuan1_button_rect = pygame.Rect(500, 150, 500, 50)
        
        # 计算体育协会按钮矩形
        if self.tiyu_button:
            button_width = 150
            button_height = 78
            button_height = min(button_height, 50)
            tiyu_button_rect = pygame.Rect(300, 450, button_width, button_height)
        else:
            tiyu_button_rect = pygame.Rect(300, 500, 500, 50)
        
        # 计算街舞社/音乐社按钮矩形
        if self.dance_music_button:
            button_width = 215
            button_height = 78
            button_height = min(button_height, 50)
            dance_music_button_rect = pygame.Rect(925, 250, button_width, button_height)
        else:
            dance_music_button_rect = pygame.Rect(925, 250, 500, 50)
        
        # 计算学生活动按钮矩形
        if self.xueshenghuodong_button:
            button_width = 150
            button_height = 78
            button_height = min(button_height, 50)
            xueshenghuodong_button_rect = pygame.Rect(925, 570, button_width, button_height)
        else:
            xueshenghuodong_button_rect = pygame.Rect(925, 570, 500, 50)
        
        # 计算实习按钮矩形
        if self.shixi_button:
            button_width = 150
            button_height = 78
            shixi_button_rect = pygame.Rect(600, 350, button_width, button_height)
        else:
            shixi_button_rect = pygame.Rect(600, 350, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.return_to_start = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if shetuan1_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_knowledge(20, current_year)
                        self.game.player.add_skill(3)  # 增加技能
                        self.game.player.add_reputation(2)  # 增加声望
                        self.game.player.add_mood(10)
                        self.game.message = "你选择了科技协会/文学社团，学识+20，技能+3，声望+2，心情+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif tiyu_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_physical(20, current_year)
                        self.game.player.add_reputation(2)  # 增加声望
                        self.game.player.add_mood(10)
                        self.game.message = "你选择了体育协会，体能+20，声望+2，心情+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif dance_music_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_charm(20, current_year)
                        self.game.player.add_social(3)  # 增加人脉
                        self.game.player.add_reputation(2)  # 增加声望
                        self.game.player.add_mood(10)
                        self.game.message = "你选择了街舞社/音乐社，魅力+20，人脉+3，声望+2，心情+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif xueshenghuodong_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_skill(20)  # 增加技能
                        self.game.player.add_social(2)  # 增加人脉
                        self.game.player.add_reputation(1)  # 增加声望
                        self.game.player.add_mood(10)
                        self.game.message = "你选择了学生活动，技能+20，人脉+2，声望+1，心情+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif shixi_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_skill(20)  # 增加技能
                        self.game.player.add_social(3)  # 增加人脉
                        self.game.player.add_reputation(2)  # 增加声望
                        self.game.player.add_mood(-10)
                        self.game.player.add_living_expenses(50)  # 增加生活费
                        self.game.message = "你选择了实习，技能+20，人脉+3，声望+2，心情-10，生活费+50"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
