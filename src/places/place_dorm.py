import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Dorm:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.dorm_background = None
        self.playgame_button = None
        self.reading_button = None
        self.bed_button = None
        self._load_images()

    def _load_images(self):
        """加载宿舍背景图片"""
        dorm_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'dorm_background.png')
        try:
            if os.path.exists(dorm_path):
                self.dorm_background = pygame.image.load(dorm_path)
        except:
            pass
        
        # 加载玩游戏按钮图片
        playgame_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'playgame_button.png')
        try:
            if os.path.exists(playgame_button_path):
                self.playgame_button = pygame.image.load(playgame_button_path)
        except:
            pass
        
        # 加载看书按钮图片
        reading_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'reading_button.png')
        try:
            if os.path.exists(reading_button_path):
                self.reading_button = pygame.image.load(reading_button_path)
        except:
            pass
        
        # 加载床按钮图片
        bed_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'bed_button.png')
        try:
            if os.path.exists(bed_button_path):
                self.bed_button = pygame.image.load(bed_button_path)
        except:
            pass

    def draw(self):
        """绘制宿舍场景"""
        if self.dorm_background:
            scaled_bg = pygame.transform.scale(self.dorm_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)

        # 只有未玩游戏时显示玩游戏选项
        if not self.game.has_played_games:
            if self.playgame_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.playgame_button_rect = pygame.Rect(800, 350, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.playgame_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.playgame_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.playgame_button_rect = pygame.Rect(400, 200, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.playgame_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.playgame_button_rect, 2)
                self.game.draw_text("玩游戏：心情+40 行动点-1", self.playgame_button_rect.x + 10, self.playgame_button_rect.y + 10, (254, 247, 201))

        # 只有未看书时显示看书选项
        if not self.game.has_read_book:
            if self.reading_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.reading_button_rect = pygame.Rect(350, 300, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.reading_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.reading_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.reading_button_rect = pygame.Rect(400, 280, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.reading_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.reading_button_rect, 2)
                self.game.draw_text("看书：学识+10 心情-10 行动点-1", self.reading_button_rect.x + 10, self.reading_button_rect.y + 10, (254, 247, 201))

        # 只有未休息时显示休息选项
        if not self.game.has_rested:
            if self.bed_button:
                # 保持图片原始比例，计算显示大小
                button_width = 180
                button_height = 78
                # 计算按钮位置
                self.bed_button_rect = pygame.Rect(450, 150, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.bed_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.bed_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.bed_button_rect = pygame.Rect(400, 360, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.bed_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.bed_button_rect, 2)
                self.game.draw_text("床：行动点+2 健康值+5", self.bed_button_rect.x + 10, self.bed_button_rect.y + 10, (254, 247, 201))

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理宿舍场景事件"""
        # 计算玩游戏按钮矩形
        if self.playgame_button:
            button_width = 150
            button_height = 78
            playgame_button_rect = pygame.Rect(800, 350, button_width, button_height)
        else:
            playgame_button_rect = pygame.Rect(400, 200, 500, 50)
        
        # 计算看书按钮矩形
        if self.reading_button:
            button_width = 150
            button_height = 78
            reading_button_rect = pygame.Rect(350, 300, button_width, button_height)
        else:
            reading_button_rect = pygame.Rect(400, 280, 500, 50)
        
        # 计算床按钮矩形
        if self.bed_button:
            button_width = 180
            button_height = 78
            bed_button_rect = pygame.Rect(450, 150, button_width, button_height)
        else:
            bed_button_rect = pygame.Rect(400, 360, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 只有未玩游戏时才能点击玩游戏选项
                if not self.game.has_played_games and playgame_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_mood(30)
                        self.game.has_played_games = True
                        self.game.message = "你选择了玩游戏，心情+30，行动点-1"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                # 只有未看书时才能点击看书选项
                elif not self.game.has_read_book and reading_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_knowledge(10, current_year)
                        self.game.player.add_mood(10)
                        self.game.has_read_book = True
                        self.game.message = "你选择了看书，学识+10 心情+10 行动点-1"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                # 只有未休息时才能点击休息选项
                elif not self.game.has_rested and bed_button_rect.collidepoint(pos):
                    self.game.player.action_points += 2
                    self.game.player.add_health(5)
                    self.game.has_rested = True
                    self.game.message = "你选择了休息，行动点+2，健康值+5"
                    self.game.message_timer = 90
