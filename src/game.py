import pygame
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, GRAY,
    DAILY_ACTION_POINTS, SAVE_FILE
)
from src.player import Player
from src.time_system import TimeSystem
from src.character import Character
from src.create_character_scene import CreateCharacterScene

# 游戏状态
STATE_CREATE_CHARACTER = "CREATE_CHARACTER"
STATE_MAIN_GAME = "MAIN_GAME"
STATE_MENU = "MENU"


class Game:
    def __init__(self):
        pygame.init()
        # 创建可调整大小的窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("北科校园物语")
        self.clock = pygame.time.Clock()
        # 存储当前窗口大小
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        # 尝试使用本地字体文件
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'msyh.ttf')
        self.font = None
        self.large_font = None
        
        try:
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 18)  # 增大字体大小
                self.large_font = pygame.font.Font(font_path, 24)  # 增大字体大小
        except:
            pass
        
        # 如果本地字体失败，尝试使用系统字体
        if self.font is None or self.large_font is None:
            font_names = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
            for font_name in font_names:
                try:
                    if self.font is None:
                        self.font = pygame.font.SysFont(font_name, 18)  # 增大字体大小
                    if self.large_font is None:
                        self.large_font = pygame.font.SysFont(font_name, 24)  # 增大字体大小
                    if self.font and self.large_font:
                        break
                except:
                    continue
        
        # 如果所有字体都失败，使用默认字体
        if self.font is None:
            self.font = pygame.font.Font(None, 18)  # 增大字体大小
        if self.large_font is None:
            self.large_font = pygame.font.Font(None, 24)  # 增大字体大小
        
        # 游戏状态
        self.current_state = STATE_CREATE_CHARACTER
        
        # 角色和场景
        self.character = None
        self.create_character_scene = None
        
        # 其他游戏对象
        self.player = Player()
        self.time_system = TimeSystem()
        
        # 游戏状态
        self.running = True
        self.message = ""
        self.message_timer = 0
        
        self.player.action_points = DAILY_ACTION_POINTS
    
    def reset(self):
        self.player.reset()
        self.time_system.reset()
        self.player.action_points = DAILY_ACTION_POINTS
        self.message = "新游戏开始！"
        self.message_timer = 120
    
    def save_game(self):
        try:
            save_data = {
                'player': self.player.to_dict(),
                'time_system': self.time_system.to_dict()
            }
            os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            self.message = "游戏已保存！"
            self.message_timer = 120
        except Exception as e:
            self.message = f"保存失败: {str(e)}"
            self.message_timer = 120
    
    def load_game(self):
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                self.player.from_dict(save_data['player'])
                self.time_system.from_dict(save_data['time_system'])
                self.message = "游戏已加载！"
                self.message_timer = 120
            else:
                self.message = "没有找到存档！"
                self.message_timer = 120
        except Exception as e:
            self.message = f"加载失败: {str(e)}"
            self.message_timer = 120
    
    def advance_day(self):
        if self.time_system.is_ended():
            self.message = "游戏已结束！"
            self.message_timer = 120
            return
        
        self.time_system.next_day()
        self.player.action_points = DAILY_ACTION_POINTS
        
        self.player.change_attribute('mood', -2)
        self.player.change_attribute('health', -1)
        
        if self.time_system.is_ended():
            self.message = "恭喜！你完成了128天的校园生活！"
            self.message_timer = 300
        else:
            self.message = f"新的一天开始了！{self.time_system.get_time_display()}"
            self.message_timer = 120
    
    def handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
            elif event.type == pygame.VIDEORESIZE:
                # 处理窗口大小变化
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        
        # 根据状态处理事件
        if self.current_state == STATE_CREATE_CHARACTER:
            self._handle_create_character(events)
            # 更新角色创建场景的窗口大小
            if self.create_character_scene is not None:
                self.create_character_scene.width = self.width
                self.create_character_scene.height = self.height
        elif self.current_state == STATE_MAIN_GAME:
            self._handle_main_game(events)
    
    def _handle_create_character(self, events):
        """处理角色创建"""
        if self.create_character_scene is None:
            self.create_character_scene = CreateCharacterScene(self.screen, self.font, self.large_font)
        
        # 处理事件
        result = self.create_character_scene.handle_events(events)
        
        # 检查是否完成创建
        if result is not None:
            if isinstance(result, Character):
                self.character = result
                self.current_state = STATE_MAIN_GAME
                self.create_character_scene = None
            else:
                # 取消创建，退出游戏
                self.running = False
    
    def _handle_main_game(self, events):
        """处理主游戏事件"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.advance_day()
                elif event.key == pygame.K_s:
                    self.save_game()
                elif event.key == pygame.K_l:
                    self.load_game()
                elif event.key == pygame.K_1:
                    self.do_action("学习")
                elif event.key == pygame.K_2:
                    self.do_action("运动")
                elif event.key == pygame.K_3:
                    self.do_action("休息")
                elif event.key == pygame.K_4:
                    self.do_action("打工")
                elif event.key == pygame.K_5:
                    self.do_action("社交")
    
    def do_action(self, action_name):
        if self.player.action_points <= 0:
            self.message = "行动点不足！"
            self.message_timer = 60
            return
        
        self.player.action_points -= 1
        
        if action_name == "学习":
            self.player.change_attribute('intelligence', 5)
            self.player.change_attribute('mood', -3)
            self.player.change_attribute('health', -2)
            self.message = "努力学习，智力+5"
        elif action_name == "运动":
            self.player.change_attribute('physical', 5)
            self.player.change_attribute('health', 3)
            self.player.change_attribute('mood', 2)
            self.message = "运动健身，体力+5"
        elif action_name == "休息":
            self.player.change_attribute('health', 5)
            self.player.change_attribute('mood', 5)
            self.player.change_attribute('physical', -1)
            self.message = "好好休息，恢复体力"
        elif action_name == "打工":
            self.player.change_attribute('gold', 100)
            self.player.change_attribute('mood', -5)
            self.player.change_attribute('health', -3)
            self.message = "辛苦打工，金币+100"
        elif action_name == "社交":
            self.player.change_attribute('charm', 3)
            self.player.change_attribute('mood', 5)
            self.player.change_attribute('gold', -20)
            self.message = "社交活动，魅力+3"
        
        self.message_timer = 90
    
    def draw_text(self, text, x, y, color=WHITE, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw(self):
        # 根据状态绘制
        if self.current_state == STATE_CREATE_CHARACTER:
            self._draw_create_character()
        elif self.current_state == STATE_MAIN_GAME:
            self._draw_main_game()
        
        pygame.display.flip()
    
    def _draw_create_character(self):
        """绘制角色创建场景"""
        if self.create_character_scene is not None:
            self.create_character_scene.update()
            self.create_character_scene.draw()
    
    def _draw_main_game(self):
        """绘制主游戏场景"""
        self.screen.fill(BLACK)
        
        # 绘制角色信息（左上角）
        if self.character:
            self._draw_character_info()
        
        # 调整时间显示位置，避免与角色信息重叠
        if self.character:
            self.draw_text(self.time_system.get_time_display(), 20, 180, WHITE, self.large_font)
            y_offset = 220
        else:
            self.draw_text(self.time_system.get_time_display(), 20, 20, WHITE, self.large_font)
            y_offset = 80
        attr_names = {
            'health': '健康',
            'mood': '心情',
            'intelligence': '智力',
            'physical': '体力',
            'charm': '魅力',
            'gold': '金币'
        }
        
        for attr, name in attr_names.items():
            value = self.player.get_attribute(attr)
            self.draw_text(f"{name}: {value}", 20, y_offset)
            y_offset += 30
        
        self.draw_text(f"行动点: {self.player.action_points}", 20, y_offset + 10)
        y_offset += 50
        
        self.draw_text("可用行动:", 20, y_offset)
        y_offset += 30
        actions = [
            "[1] 学习 (智力+5)",
            "[2] 运动 (体力+5)",
            "[3] 休息 (恢复)",
            "[4] 打工 (金币+100)",
            "[5] 社交 (魅力+3)"
        ]
        
        for action in actions:
            self.draw_text(action, 40, y_offset)
            y_offset += 25
        
        y_offset += 20
        self.draw_text("操作说明:", 20, y_offset)
        y_offset += 30
        self.draw_text("[空格] 推进一天  [S] 存档  [L] 读档  [Q] 退出", 40, y_offset)
        
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 150, self.height - 80, WHITE, self.large_font)
            self.message_timer -= 1
    
    def _draw_character_info(self):
        """绘制角色信息面板"""
        # 面板背景
        panel_rect = pygame.Rect(20, 20, 280, 150)
        pygame.draw.rect(self.screen, (50, 50, 60), panel_rect)
        pygame.draw.rect(self.screen, (150, 150, 150), panel_rect, 2)
        
        # 内边框
        inner_rect = panel_rect.inflate(-4, -4)
        pygame.draw.rect(self.screen, (70, 70, 80), inner_rect, 1)
        
        # 角色名称
        name_text = self.large_font.render(f"姓名: {self.character.name}", True, (240, 240, 240))
        self.screen.blit(name_text, (35, 35))
        
        # 学院
        college_text = self.font.render(f"学院: {self.character.college}学院", True, (100, 200, 255))
        self.screen.blit(college_text, (35, 70))
        
        # 专业
        major_text = self.font.render(f"专业: {self.character.major}", True, (240, 240, 240))
        self.screen.blit(major_text, (35, 95))
        
        # 绩点
        gpa_text = self.font.render(f"绩点: {self.character.gpa}", True, (255, 200, 100))
        self.screen.blit(gpa_text, (35, 120))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
