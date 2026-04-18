import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Supermarket:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.start_font = game.start_font
        self.supermarket_background = None
        self.cake_button = None
        self.cloth_button = None
        self.book_button = None
        self.jianshen_button = None
        self.unhealth_button = None
        self.tili_button = None
        self._load_images()

    def _load_images(self):
        """加载超市背景图片"""
        supermarket_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'supermarket_background.png')
        try:
            if os.path.exists(supermarket_path):
                self.supermarket_background = pygame.image.load(supermarket_path)
        except:
            pass
        
        # 加载美味蛋糕按钮图片
        cake_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'cake_button.png')
        try:
            if os.path.exists(cake_button_path):
                self.cake_button = pygame.image.load(cake_button_path)
        except:
            pass
        
        # 加载潮流衣服按钮图片
        cloth_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'cloth_button.png')
        try:
            if os.path.exists(cloth_button_path):
                self.cloth_button = pygame.image.load(cloth_button_path)
        except:
            pass
        
        # 加载课外教程按钮图片
        book_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'book_button.png')
        try:
            if os.path.exists(book_button_path):
                self.book_button = pygame.image.load(book_button_path)
        except:
            pass
        
        # 加载健身器材按钮图片
        jianshen_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'jianshen_button.png')
        try:
            if os.path.exists(jianshen_button_path):
                self.jianshen_button = pygame.image.load(jianshen_button_path)
        except:
            pass
        
        # 加载不健康的零食按钮图片
        unhealth_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'unhealth_button.png')
        try:
            if os.path.exists(unhealth_button_path):
                self.unhealth_button = pygame.image.load(unhealth_button_path)
        except:
            pass
        
        # 加载体力药水按钮图片
        tili_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'tili_button.png')
        try:
            if os.path.exists(tili_button_path):
                self.tili_button = pygame.image.load(tili_button_path)
        except:
            pass

    def draw(self):
        """绘制超市场景"""
        if self.supermarket_background:
            scaled_bg = pygame.transform.scale(self.supermarket_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        self.game.draw_text(f"今日购买次数：{self.game.supermarket_purchases}/2", 20, 100, (254, 247, 201), self.large_font)

        option5_rect = pygame.Rect(400, 350, 500, 50)
        option6_rect = pygame.Rect(400, 400, 500, 50)

        if self.game.supermarket_purchases < 2:
            # 绘制美味蛋糕按钮
            if self.cake_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.cake_button_rect = pygame.Rect(475, 200, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.cake_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.cake_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.cake_button_rect = pygame.Rect(400, 150, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.cake_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.cake_button_rect, 2)
                self.game.draw_text("美味蛋糕：金钱-15 心情+30", self.cake_button_rect.x + 10, self.cake_button_rect.y + 10, (254, 247, 201))

            # 绘制潮流衣服按钮
            if self.cloth_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.cloth_button_rect = pygame.Rect(850, 325, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.cloth_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.cloth_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.cloth_button_rect = pygame.Rect(400, 200, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.cloth_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.cloth_button_rect, 2)
                self.game.draw_text("潮流衣服：金钱-30 魅力+10", self.cloth_button_rect.x + 10, self.cloth_button_rect.y + 10, (254, 247, 201))

            # 绘制课外教材按钮
            if self.book_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.book_button_rect = pygame.Rect(1000, 425, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.book_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.book_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.book_button_rect = pygame.Rect(400, 250, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.book_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.book_button_rect, 2)
                self.game.draw_text("课外教材：金钱-20 学识+10", self.book_button_rect.x + 10, self.book_button_rect.y + 10, (254, 247, 201))

            # 绘制健身器材按钮
            if self.jianshen_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.jianshen_button_rect = pygame.Rect(475, 375, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.jianshen_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.jianshen_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.jianshen_button_rect = pygame.Rect(400, 300, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.jianshen_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.jianshen_button_rect, 2)
                self.game.draw_text("健身器材：金钱-30 体能+10", self.jianshen_button_rect.x + 10, self.jianshen_button_rect.y + 10, (254, 247, 201))

            # 绘制不健康的零食按钮
            if self.unhealth_button:
                # 保持图片原始比例，计算显示大小
                button_width = 198
                button_height = 78
                # 计算按钮位置
                self.unhealth_button_rect = pygame.Rect(325, 500, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.unhealth_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.unhealth_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.unhealth_button_rect = pygame.Rect(400, 350, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.unhealth_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.unhealth_button_rect, 2)
                self.game.draw_text("不健康的零食：金钱-15 心情+40 健康-5", self.unhealth_button_rect.x + 10, self.unhealth_button_rect.y + 10, (254, 247, 201))

            # 绘制体力药水按钮
            if self.tili_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.tili_button_rect = pygame.Rect(225, 350, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.tili_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.tili_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.tili_button_rect = pygame.Rect(400, 400, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.tili_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.tili_button_rect, 2)
                self.game.draw_text("体力药水：金钱-30 行动点+1", self.tili_button_rect.x + 10, self.tili_button_rect.y + 10, (254, 247, 201))
        else:
            self.game.message = "今日购买次数已达上限"
            self.game.message_timer = 90

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理超市场景事件"""
        # 计算美味蛋糕按钮矩形
        if self.cake_button:
            button_width = 150
            button_height = 78
            cake_button_rect = pygame.Rect(475, 200, button_width, button_height)
        else:
            cake_button_rect = pygame.Rect(400, 150, 500, 50)
        
        # 计算潮流衣服按钮矩形
        if self.cloth_button:
            button_width = 150
            button_height = 78
            cloth_button_rect = pygame.Rect(850, 325, button_width, button_height)
        else:
            cloth_button_rect = pygame.Rect(400, 200, 500, 50)
        
        # 计算课外教材按钮矩形
        if self.book_button:
            button_width = 150
            button_height = 78
            book_button_rect = pygame.Rect(1000, 425, button_width, button_height)
        else:
            book_button_rect = pygame.Rect(400, 250, 500, 50)
        
        # 计算健身器材按钮矩形
        if self.jianshen_button:
            button_width = 150
            button_height = 78
            jianshen_button_rect = pygame.Rect(475, 375, button_width, button_height)
        else:
            jianshen_button_rect = pygame.Rect(400, 300, 500, 50)
        
        # 计算不健康的零食按钮矩形
        if self.unhealth_button:
            button_width = 198
            button_height = 78
            unhealth_button_rect = pygame.Rect(325, 500, button_width, button_height)
        else:
            unhealth_button_rect = pygame.Rect(400, 350, 500, 50)
        
        # 计算体力药水按钮矩形
        if self.tili_button:
            button_width = 150
            button_height = 78
            button_height = min(button_height, 50)
            tili_button_rect = pygame.Rect(225, 350, button_width, button_height)
        else:
            tili_button_rect = pygame.Rect(400, 400, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.return_to_start = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.game.supermarket_purchases < 2:
                    if cake_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 15:
                            self.game.player.living_expenses -= 15
                            self.game.player.add_mood(30)
                            self.game.player.add_social(2)  # 增加人脉
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了美味蛋糕，金钱-15，心情+30，人脉+2"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif cloth_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 30:
                            self.game.player.living_expenses -= 30
                            current_year = self.game.time_system.get_year()
                            self.game.player.add_charm(10, current_year)
                            self.game.player.add_reputation(2)  # 增加声望
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了潮流衣服，金钱-30，魅力+10，声望+2"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif book_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 20:
                            self.game.player.living_expenses -= 20
                            current_year = self.game.time_system.get_year()
                            self.game.player.add_knowledge(10, current_year)
                            self.game.player.add_skill(3)  # 增加技能
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了课外教材，金钱-20，学识+10，技能+3"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif jianshen_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 30:
                            self.game.player.living_expenses -= 30
                            current_year = self.game.time_system.get_year()
                            self.game.player.add_physical(10, current_year)
                            self.game.player.add_reputation(2)  # 增加声望
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了健身器材，金钱-30，体能+10，声望+2"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif unhealth_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 15:
                            self.game.player.living_expenses -= 15
                            self.game.player.add_mood(40)
                            self.game.player.add_health(-5)
                            self.game.player.add_social(1)  # 增加人脉
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了不健康的零食，金钱-15，心情+40，健康-5，人脉+1"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足"
                            self.game.message_timer = 90
                    elif tili_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 30:
                            self.game.player.living_expenses -= 30
                            self.game.player.add_action_points(1)
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了体力药水，金钱-30，行动点+1"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足"
                            self.game.message_timer = 90