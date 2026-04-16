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
        self._load_images()
    
    def _load_images(self):
        """加载学生活动中心背景图片"""
        student_center_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'studentActivityCenter.png')
        try:
            if os.path.exists(student_center_path):
                self.student_center_background = pygame.image.load(student_center_path)
        except:
            pass
    
    def draw(self):
        """绘制学生活动中心场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.student_center_background:
            scaled_bg = pygame.transform.scale(self.student_center_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.game.draw_text("学生活动中心", SCREEN_WIDTH // 2 - 100, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 420, 100, 50)
        
        # 绘制选项框
        # 社团活动 - 科技协会/文学社团
        pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
        self.game.draw_text("科技协会/文学社团：学识+20 心情+10", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
        
        # 社团活动 - 体育协会
        pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
        self.game.draw_text("体育协会：体能+20 心情+10", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
        
        # 社团活动 - 街舞社/音乐社
        pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
        self.game.draw_text("街舞社/音乐社：魅力+20 心情+10", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))
        
        # 团委学生会 - 学生活动
        pygame.draw.rect(self.screen, (220, 180, 140), option4_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option4_rect, 2)
        self.game.draw_text("学生活动：技能+20 心情+10", option4_rect.x + 10, option4_rect.y + 10, (254, 247, 201))
        
        # 团委学生会 - 实习
        pygame.draw.rect(self.screen, (220, 180, 140), option5_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option5_rect, 2)
        self.game.draw_text("实习：技能+20 心情-10", option5_rect.x + 10, option5_rect.y + 10, (254, 247, 201))
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.game.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.game.message_timer > 0:
            self.game.draw_text(self.game.message, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 60, (254, 247, 201), self.large_font)
            self.game.message_timer -= 1
    
    def handle_events(self, events):
        """处理学生活动中心场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 420, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if option1_rect.collidepoint(pos):
                    # 选择科技协会/文学社团
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_knowledge(20)
                        self.game.player.add_mood(10)
                        self.game.message = "你选择了科技协会/文学社团，学识+20，心情+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option2_rect.collidepoint(pos):
                    # 选择体育协会
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_physical(20)
                        self.game.player.add_mood(10)
                        self.game.message = "你选择了体育协会，体能+20，心情+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option3_rect.collidepoint(pos):
                    # 选择街舞社/音乐社
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_charm(20)
                        self.game.player.add_mood(10)
                        self.game.message = "你选择了街舞社/音乐社，魅力+20，心情+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option4_rect.collidepoint(pos):
                    # 选择学生活动
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        # 假设技能是一个属性，如果没有可以添加
                        self.game.player.add_mood(10)
                        self.game.message = "你选择了学生活动，技能+20，心情+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option5_rect.collidepoint(pos):
                    # 选择实习
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        # 假设技能是一个属性，如果没有可以添加
                        self.game.player.add_mood(-10)
                        self.game.message = "你选择了实习，技能+20，心情-10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()  # 确保地图显示
