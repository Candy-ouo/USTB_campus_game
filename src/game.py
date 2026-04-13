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
from src.map import MapSystem
from src.character import Character
from src.create_character_scene import CreateCharacterScene

# 游戏状态
STATE_CREATE_CHARACTER = "CREATE_CHARACTER"
STATE_MAIN_GAME = "MAIN_GAME"
STATE_MENU = "MENU"
STATE_CANTEEN = "CANTEEN"
STATE_TEACHING = "TEACHING"
STATE_SPORTS = "SPORTS"
STATE_SUPERMARKET = "SUPERMARKET"
STATE_DORM = "DORM"
STATE_STUDENT_CENTER = "STUDENT_CENTER"
STATE_HOSPITAL = "HOSPITAL"

class Game:
    def __init__(self, character=None):
        pygame.init()
        # 创建可调整大小的窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("北科校园物语")
        self.clock = pygame.time.Clock()
        # 存储当前窗口大小
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        # 尝试使用本地字体文件
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'msyh.ttf')
        start_font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'fonts_start.ttf')
        self.font = None
        self.large_font = None
        self.start_font = None
        
        try:
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 18)  # 增大字体大小
                self.large_font = pygame.font.Font(font_path, 24)  # 增大字体大小
        except:
            pass
        
        # 加载粗体字体
        try:
            if os.path.exists(start_font_path):
                self.start_font = pygame.font.Font(start_font_path, 20)
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
        if self.start_font is None:
            self.start_font = self.font
        
        # 游戏状态
        self.current_state = STATE_MAIN_GAME if character else STATE_CREATE_CHARACTER
        
        # 角色和场景
        self.character = character
        self.create_character_scene = None
        
        # 加载地图按钮图片
        map_button_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'map_button.png')
        self.map_button_image = None
        try:
            if os.path.exists(map_button_path):
                self.map_button_image = pygame.image.load(map_button_path)
        except:
            pass
        
        # 加载食堂背景图片
        canteen_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'canteen.png')
        self.canteen_background = None
        try:
            if os.path.exists(canteen_path):
                self.canteen_background = pygame.image.load(canteen_path)
        except:
            pass
        
        # 加载教学区背景图片
        classroom_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'classroom.png')
        self.classroom_background = None
        try:
            if os.path.exists(classroom_path):
                self.classroom_background = pygame.image.load(classroom_path)
        except:
            pass
        
        # 加载操场背景图片
        gym_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'gym.png')
        self.gym_background = None
        try:
            if os.path.exists(gym_path):
                self.gym_background = pygame.image.load(gym_path)
        except:
            pass
        
        # 加载超市背景图片
        supermarket_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'supermarket.png')
        self.supermarket_background = None
        try:
            if os.path.exists(supermarket_path):
                self.supermarket_background = pygame.image.load(supermarket_path)
        except:
            pass
        
        # 加载学生活动中心背景图片
        student_center_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'studentActivityCenter.png')
        self.student_center_background = None
        try:
            if os.path.exists(student_center_path):
                self.student_center_background = pygame.image.load(student_center_path)
        except:
            pass
        
        # 加载宿舍背景图片
        dorm_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'dorm.png')
        self.dorm_background = None
        try:
            if os.path.exists(dorm_path):
                self.dorm_background = pygame.image.load(dorm_path)
        except:
            pass
        
        # 加载校医院背景图片
        hospital_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'hospital.png')
        self.hospital_background = None
        try:
            if os.path.exists(hospital_path):
                self.hospital_background = pygame.image.load(hospital_path)
        except:
            pass
        
        # 区域状态
        self.has_eaten = False
        self.has_studied = False
        self.has_exercised = False
        self.supermarket_purchases = 0
        
        # 其他游戏对象
        self.player = Player()
        self.time_system = TimeSystem()
        self.map_system = MapSystem()
        
        # 游戏状态
        self.running = True
        self.message = ""
        self.message_timer = 0
        
        # 加载地图背景图片
        self.map_background = None
        map_image_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'map_background.jpg')
        try:
            if os.path.exists(map_image_path):
                self.map_background = pygame.image.load(map_image_path)
                # 缩放到屏幕大小
                self.map_background = pygame.transform.scale(self.map_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"加载地图背景失败: {e}")
        
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
        # 重置各区域状态
        self.has_eaten = False  # 重置用餐状态
        self.has_studied = False  # 重置学习状态
        self.has_exercised = False  # 重置运动状态
        self.supermarket_purchases = 0  # 重置超市购买次数
        
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
                elif event.key == pygame.K_SPACE:
                    if not self.map_system.is_map_showing():
                        self.advance_day()
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
        elif self.current_state == STATE_CANTEEN:
            self._handle_canteen(events)
        elif self.current_state == STATE_TEACHING:
            self._handle_teaching(events)
        elif self.current_state == STATE_SPORTS:
            self._handle_sports(events)
        elif self.current_state == STATE_SUPERMARKET:
            self._handle_supermarket(events)
        elif self.current_state == STATE_DORM:
            self._handle_dorm(events)
        elif self.current_state == STATE_STUDENT_CENTER:
            self._handle_student_center(events)
        elif self.current_state == STATE_HOSPITAL:
            self._handle_hospital(events)
    
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
                    if not self.map_system.is_map_showing():
                        self.save_game()
                elif event.key == pygame.K_l:
                    if not self.map_system.is_map_showing():
                        self.load_game()
                elif event.key == pygame.K_m:
                    self.map_system.toggle_map()
                    self.map_system.clear_active_area()
                elif event.key == pygame.K_1:
                    if not self.map_system.is_map_showing():
                        self.do_action("学习")
                    else:
                        self.handle_map_action(0)
                elif event.key == pygame.K_2:
                    if not self.map_system.is_map_showing():
                        self.do_action("运动")
                    else:
                        self.handle_map_action(1)
                elif event.key == pygame.K_3:
                    if not self.map_system.is_map_showing():
                        self.do_action("休息")
                elif event.key == pygame.K_4:
                    if not self.map_system.is_map_showing():
                        self.do_action("打工")
                elif event.key == pygame.K_5:
                    if not self.map_system.is_map_showing():
                        self.do_action("社交")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.map_system.is_map_showing():
                    pos = pygame.mouse.get_pos()
                    area_id = self.map_system.get_area_at(pos)
                    if area_id:
                        if area_id == 'canteen':
                            # 切换到食堂场景
                            self.map_system.toggle_map()  # 确保地图不显示
                            self.current_state = STATE_CANTEEN
                        elif area_id == 'teaching':
                            # 切换到教学区场景
                            self.map_system.toggle_map()  # 确保地图不显示
                            self.current_state = STATE_TEACHING
                        elif area_id == 'sports':
                            # 切换到操场场景
                            self.map_system.toggle_map()  # 确保地图不显示
                            self.current_state = STATE_SPORTS
                        elif area_id == 'food':
                            # 切换到超市场景
                            self.map_system.toggle_map()  # 确保地图不显示
                            self.current_state = STATE_SUPERMARKET
                        elif area_id == 'dorm':
                            # 切换到宿舍场景
                            self.map_system.toggle_map()  # 确保地图不显示
                            self.current_state = STATE_DORM
                        elif area_id == 'supermarket':
                            # 切换到学生活动中心场景
                            self.map_system.toggle_map()  # 确保地图不显示
                            self.current_state = STATE_STUDENT_CENTER
                        elif area_id == 'hospital':
                            # 切换到校医院场景
                            self.map_system.toggle_map()  # 确保地图不显示
                            self.current_state = STATE_HOSPITAL
                        else:
                            self.map_system.set_active_area(area_id)
                    else:
                        self.map_system.clear_active_area()
    
    def _handle_canteen(self, events):
        """处理食堂场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 440, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not self.has_eaten:
                    if option1_rect.collidepoint(pos):
                        # 选择鸡腿套餐
                        if self.player.gold >= 10:
                            self.player.gold -= 10
                            self.player.change_attribute('mood', 10)
                            self.player.change_attribute('health', 10)
                            self.player.action_points += 1
                            self.has_eaten = True
                            self.message = "你选择了鸡腿套餐，金钱-10，心情+10，健康值+10，行动点+1"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                    elif option2_rect.collidepoint(pos):
                        # 选择营养套餐
                        if self.player.gold >= 15:
                            self.player.gold -= 15
                            self.player.change_attribute('mood', 20)
                            self.player.change_attribute('health', 10)
                            self.player.action_points += 2
                            self.has_eaten = True
                            self.message = "你选择了营养套餐，金钱-15，心情+20，健康值+10，行动点+2"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                    elif option3_rect.collidepoint(pos):
                        # 选择特色美食
                        if self.player.gold >= 20:
                            self.player.gold -= 20
                            self.player.change_attribute('mood', 30)
                            self.player.change_attribute('health', 10)
                            self.player.action_points += 3
                            self.has_eaten = True
                            self.message = "你选择了特色美食，金钱-20，心情+30，健康值+10，行动点+3"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
    
    def _draw_teaching(self):
        """绘制教学区场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.classroom_background:
            scaled_bg = pygame.transform.scale(self.classroom_background, (self.width, self.height))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.draw_text("教学区", self.width // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 440, 100, 50)
        
        # 绘制选项框
        if not self.has_studied:
            # 上课
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.draw_text("上课：行动点-2 学识+30 心情-30 健康值-5", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
            
            # 自习
            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.draw_text("自习：行动点-1 学识+15 心情-20 健康值-5", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
        else:
            # 已学习提示
            self.draw_text("已学习", self.width // 2 - 50, 200, (254, 247, 201), self.large_font)
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 300, self.height - 60, (254, 247, 201), self.large_font)
            self.message_timer -= 1
    
    def _handle_teaching(self, events):
        """处理教学区场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 440, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not self.has_studied:
                    if option1_rect.collidepoint(pos):
                        # 选择上课
                        if self.player.action_points >= 2:
                            self.player.action_points -= 2
                            self.player.change_attribute('intelligence', 30)
                            self.player.change_attribute('mood', -30)
                            self.player.change_attribute('health', -5)
                            self.has_studied = True
                            self.message = "你选择了上课，行动点-2，学识+30，心情-30，健康值-5"
                            self.message_timer = 90
                        else:
                            self.message = "行动点不足！"
                            self.message_timer = 60
                    elif option2_rect.collidepoint(pos):
                        # 选择自习
                        if self.player.action_points >= 1:
                            self.player.action_points -= 1
                            self.player.change_attribute('intelligence', 15)
                            self.player.change_attribute('mood', -20)
                            self.player.change_attribute('health', -5)
                            self.has_studied = True
                            self.message = "你选择了自习，行动点-1，学识+15，心情-20，健康值-5"
                            self.message_timer = 90
                        else:
                            self.message = "行动点不足！"
                            self.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
    
    def _draw_sports(self):
        """绘制操场场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.gym_background:
            scaled_bg = pygame.transform.scale(self.gym_background, (self.width, self.height))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.draw_text("操场", self.width // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 440, 100, 50)
        
        # 绘制选项框
        if not self.has_exercised:
            # 散步
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.draw_text("散步：行动点-1 体能+5", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
            
            # 跑步
            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.draw_text("跑步：行动点-2 体能+10", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
            
            # 游泳
            pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
            self.draw_text("游泳：行动点-2 金钱-20 体能+15", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))
        else:
            # 已运动提示
            self.draw_text("已运动", self.width // 2 - 50, 200, (254, 247, 201), self.large_font)
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 300, self.height - 60, (254, 247, 201), self.large_font)
            self.message_timer -= 1
    
    def _handle_sports(self, events):
        """处理操场场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 440, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not self.has_exercised:
                    if option1_rect.collidepoint(pos):
                        # 选择散步
                        if self.player.action_points >= 1:
                            self.player.action_points -= 1
                            self.player.change_attribute('physical', 5)
                            self.has_exercised = True
                            self.message = "你选择了散步，行动点-1，体能+5"
                            self.message_timer = 90
                        else:
                            self.message = "行动点不足！"
                            self.message_timer = 60
                    elif option2_rect.collidepoint(pos):
                        # 选择跑步
                        if self.player.action_points >= 2:
                            self.player.action_points -= 2
                            self.player.change_attribute('physical', 10)
                            self.has_exercised = True
                            self.message = "你选择了跑步，行动点-2，体能+10"
                            self.message_timer = 90
                        else:
                            self.message = "行动点不足！"
                            self.message_timer = 60
                    elif option3_rect.collidepoint(pos):
                        # 选择游泳
                        if self.player.action_points >= 2 and self.player.gold >= 20:
                            self.player.action_points -= 2
                            self.player.gold -= 20
                            self.player.change_attribute('physical', 15)
                            self.has_exercised = True
                            self.message = "你选择了游泳，行动点-2，金钱-20，体能+15"
                            self.message_timer = 90
                        elif self.player.action_points < 2:
                            self.message = "行动点不足！"
                            self.message_timer = 60
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
    
    def _draw_supermarket(self):
        """绘制超市场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.supermarket_background:
            scaled_bg = pygame.transform.scale(self.supermarket_background, (self.width, self.height))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.draw_text("超市", self.width // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 绘制购买次数提示
        self.draw_text(f"今日购买次数：{self.supermarket_purchases}/2", 20, 100, (254, 247, 201), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)
        option6_rect = pygame.Rect(400, 400, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 470, 100, 50)
        
        # 绘制选项框
        if self.supermarket_purchases < 2:
            # 美味蛋糕
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.draw_text("美味蛋糕：金钱-15 心情+30", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
            
            # 潮流衣服
            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.draw_text("潮流衣服：金钱-30 魅力+10", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
            
            # 课外教材
            pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
            self.draw_text("课外教材：金钱-20 学识+10", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))
            
            # 健身器材
            pygame.draw.rect(self.screen, (220, 180, 140), option4_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option4_rect, 2)
            self.draw_text("健身器材：金钱-30 体能+10", option4_rect.x + 10, option4_rect.y + 10, (254, 247, 201))
            
            # 不健康的零食
            pygame.draw.rect(self.screen, (220, 180, 140), option5_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option5_rect, 2)
            self.draw_text("不健康的零食：金钱-15 心情+40 健康-5", option5_rect.x + 10, option5_rect.y + 10, (254, 247, 201))
            
            # 体力药水
            pygame.draw.rect(self.screen, (220, 180, 140), option6_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option6_rect, 2)
            self.draw_text("体力药水：金钱-30 行动点+1", option6_rect.x + 10, option6_rect.y + 10, (254, 247, 201))
        else:
            # 已达到购买次数上限
            self.draw_text("今日购买次数已达上限", self.width // 2 - 150, 200, (254, 247, 201), self.large_font)
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 300, self.height - 60, (254, 247, 201), self.large_font)
            self.message_timer -= 1
    
    def _handle_supermarket(self, events):
        """处理超市场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)
        option6_rect = pygame.Rect(400, 400, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 470, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.supermarket_purchases < 2:
                    if option1_rect.collidepoint(pos):
                        # 购买美味蛋糕
                        if self.player.gold >= 15:
                            self.player.gold -= 15
                            self.player.change_attribute('mood', 30)
                            self.supermarket_purchases += 1
                            self.message = "你购买了美味蛋糕，金钱-15，心情+30"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                    elif option2_rect.collidepoint(pos):
                        # 购买潮流衣服
                        if self.player.gold >= 30:
                            self.player.gold -= 30
                            self.player.change_attribute('charm', 10)
                            self.supermarket_purchases += 1
                            self.message = "你购买了潮流衣服，金钱-30，魅力+10"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                    elif option3_rect.collidepoint(pos):
                        # 购买课外教材
                        if self.player.gold >= 20:
                            self.player.gold -= 20
                            self.player.change_attribute('intelligence', 10)
                            self.supermarket_purchases += 1
                            self.message = "你购买了课外教材，金钱-20，学识+10"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                    elif option4_rect.collidepoint(pos):
                        # 购买健身器材
                        if self.player.gold >= 30:
                            self.player.gold -= 30
                            self.player.change_attribute('physical', 10)
                            self.supermarket_purchases += 1
                            self.message = "你购买了健身器材，金钱-30，体能+10"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                    elif option5_rect.collidepoint(pos):
                        # 购买不健康的零食
                        if self.player.gold >= 15:
                            self.player.gold -= 15
                            self.player.change_attribute('mood', 40)
                            self.player.change_attribute('health', -5)
                            self.supermarket_purchases += 1
                            self.message = "你购买了不健康的零食，金钱-15，心情+40，健康-5"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                    elif option6_rect.collidepoint(pos):
                        # 购买体力药水
                        if self.player.gold >= 30:
                            self.player.gold -= 30
                            self.player.action_points += 1
                            self.supermarket_purchases += 1
                            self.message = "你购买了体力药水，金钱-30，行动点+1"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足！"
                            self.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
    
    def _draw_dorm(self):
        """绘制宿舍场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.dorm_background:
            scaled_bg = pygame.transform.scale(self.dorm_background, (self.width, self.height))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.draw_text("宿舍", self.width // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 440, 100, 50)
        
        # 绘制选项框
        # 玩游戏
        pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
        self.draw_text("玩游戏：心情+40 行动点-1", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
        
        # 看书
        pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
        self.draw_text("看书：学识+10 心情-10 行动点-1", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
        
        # 床
        pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
        self.draw_text("床：行动点+2 健康值+5", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 300, self.height - 60, (254, 247, 201), self.large_font)
            self.message_timer -= 1
    
    def _handle_dorm(self, events):
        """处理宿舍场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 440, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if option1_rect.collidepoint(pos):
                    # 选择玩游戏
                    if self.player.action_points >= 1:
                        self.player.action_points -= 1
                        self.player.change_attribute('mood', 40)
                        self.message = "你选择了玩游戏，心情+40，行动点-1"
                        self.message_timer = 90
                    else:
                        self.message = "行动点不足！"
                        self.message_timer = 60
                elif option2_rect.collidepoint(pos):
                    # 选择看书
                    if self.player.action_points >= 1:
                        self.player.action_points -= 1
                        self.player.change_attribute('intelligence', 10)
                        self.player.change_attribute('mood', -10)
                        self.message = "你选择了看书，学识+10，心情-10，行动点-1"
                        self.message_timer = 90
                    else:
                        self.message = "行动点不足！"
                        self.message_timer = 60
                elif option3_rect.collidepoint(pos):
                    # 选择床
                    self.player.action_points += 2
                    self.player.change_attribute('health', 5)
                    self.message = "你选择了休息，行动点+2，健康值+5"
                    self.message_timer = 90
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
    
    def _draw_student_center(self):
        """绘制学生活动中心场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.student_center_background:
            scaled_bg = pygame.transform.scale(self.student_center_background, (self.width, self.height))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.draw_text("学生活动中心", self.width // 2 - 100, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 420, 100, 50)
        
        # 绘制选项框
        # 社团活动 - 科技协会/文学社团
        pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
        self.draw_text("科技协会/文学社团：学识+20 心情+10", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
        
        # 社团活动 - 体育协会
        pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
        self.draw_text("体育协会：体能+20 心情+10", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
        
        # 社团活动 - 街舞社/音乐社
        pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
        self.draw_text("街舞社/音乐社：魅力+20 心情+10", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))
        
        # 团委学生会 - 学生活动
        pygame.draw.rect(self.screen, (220, 180, 140), option4_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option4_rect, 2)
        self.draw_text("学生活动：技能+20 心情+10", option4_rect.x + 10, option4_rect.y + 10, (254, 247, 201))
        
        # 团委学生会 - 实习
        pygame.draw.rect(self.screen, (220, 180, 140), option5_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option5_rect, 2)
        self.draw_text("实习：技能+20 心情-10", option5_rect.x + 10, option5_rect.y + 10, (254, 247, 201))
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 300, self.height - 60, (254, 247, 201), self.large_font)
            self.message_timer -= 1
    
    def _handle_student_center(self, events):
        """处理学生活动中心场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 420, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if option1_rect.collidepoint(pos):
                    # 选择科技协会/文学社团
                    if self.player.action_points >= 1:
                        self.player.action_points -= 1
                        self.player.change_attribute('intelligence', 20)
                        self.player.change_attribute('mood', 10)
                        self.message = "你选择了科技协会/文学社团，学识+20，心情+10"
                        self.message_timer = 90
                    else:
                        self.message = "行动点不足！"
                        self.message_timer = 60
                elif option2_rect.collidepoint(pos):
                    # 选择体育协会
                    if self.player.action_points >= 1:
                        self.player.action_points -= 1
                        self.player.change_attribute('physical', 20)
                        self.player.change_attribute('mood', 10)
                        self.message = "你选择了体育协会，体能+20，心情+10"
                        self.message_timer = 90
                    else:
                        self.message = "行动点不足！"
                        self.message_timer = 60
                elif option3_rect.collidepoint(pos):
                    # 选择街舞社/音乐社
                    if self.player.action_points >= 1:
                        self.player.action_points -= 1
                        self.player.change_attribute('charm', 20)
                        self.player.change_attribute('mood', 10)
                        self.message = "你选择了街舞社/音乐社，魅力+20，心情+10"
                        self.message_timer = 90
                    else:
                        self.message = "行动点不足！"
                        self.message_timer = 60
                elif option4_rect.collidepoint(pos):
                    # 选择学生活动
                    if self.player.action_points >= 1:
                        self.player.action_points -= 1
                        # 假设技能是一个属性，如果没有可以添加
                        self.player.change_attribute('mood', 10)
                        self.message = "你选择了学生活动，技能+20，心情+10"
                        self.message_timer = 90
                    else:
                        self.message = "行动点不足！"
                        self.message_timer = 60
                elif option5_rect.collidepoint(pos):
                    # 选择实习
                    if self.player.action_points >= 1:
                        self.player.action_points -= 1
                        # 假设技能是一个属性，如果没有可以添加
                        self.player.change_attribute('mood', -10)
                        self.message = "你选择了实习，技能+20，心情-10"
                        self.message_timer = 90
                    else:
                        self.message = "行动点不足！"
                        self.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
    
    def _draw_hospital(self):
        """绘制校医院场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.hospital_background:
            scaled_bg = pygame.transform.scale(self.hospital_background, (self.width, self.height))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.draw_text("校医院", self.width // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 300, 100, 50)
        
        # 绘制选项框
        # 治病选项
        pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
        self.draw_text("治病：金钱-50 恢复健康状态", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 300, self.height - 60, (254, 247, 201), self.large_font)
            self.message_timer -= 1
    
    def _handle_hospital(self, events):
        """处理校医院场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 300, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if option1_rect.collidepoint(pos):
                    # 选择治病
                    if self.player.get_attribute('health') < 60:
                        if self.player.gold >= 50:
                            self.player.gold -= 50
                            self.player.set_attribute('health', 100)  # 恢复健康状态
                            self.message = "你在医院治疗，金钱-50，健康状态已恢复"
                            self.message_timer = 90
                        else:
                            self.message = "金钱不足，无法治疗！"
                            self.message_timer = 60
                    else:
                        self.message = "你的健康状态良好，不需要治疗"
                        self.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.current_state = STATE_MAIN_GAME
                    self.map_system.toggle_map()  # 确保地图显示

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
    
    def handle_map_action(self, action_index):
        if self.player.action_points <= 0:
            self.message = "行动点不足！"
            self.message_timer = 60
            return
        
        active_area = self.map_system.active_area
        if not active_area:
            return
        
        area = self.map_system.get_area(active_area)
        if not area or action_index >= len(area['actions']):
            return
        
        action = area['actions'][action_index]
        self.player.action_points -= 1
        
        # 应用行动效果
        effects = action['effects']
        effect_messages = []
        for attr, value in effects.items():
            self.player.change_attribute(attr, value)
            effect_messages.append(f"{attr}: {value:+d}")
        
        self.message = f"{area['name']}: {action['name']} - {', '.join(effect_messages)}"
        self.message_timer = 90
    
    def draw_text(self, text, x, y, color=WHITE, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_map(self):
        # 绘制地图背景图片
        if self.map_background:
            self.screen.blit(self.map_background, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制地图标题
        self.draw_text("校园地图", SCREEN_WIDTH // 2 - 100, 30, (80, 40, 0), self.large_font)  # 深棕色文字
        
        # 绘制各个区域（使用map_button作为背景）
        for area_id, area in self.map_system.areas.items():
            # 绘制区域背景
            if self.map_button_image:
                # 缩放按钮图片以适应区域大小
                scaled_button = pygame.transform.scale(self.map_button_image, (area['rect'].width, area['rect'].height))
                self.screen.blit(scaled_button, area['rect'])
            else:
                # 如果没有按钮图片，使用默认背景色
                pygame.draw.rect(self.screen, area['bg_color'], area['rect'])
                # 绘制区域边框
                pygame.draw.rect(self.screen, area['border_color'], area['rect'], 2)
            
            # 绘制区域名称（使用指定的字体和颜色）
            name_text = self.start_font.render(area['name'], True, (254, 247, 201))
            text_rect = name_text.get_rect(center=area['rect'].center)
            self.screen.blit(name_text, text_rect)
        
        # 绘制操作说明
        self.draw_text("点击区域查看详情，按M返回主界面", 20, SCREEN_HEIGHT - 50, (80, 40, 0))  # 深棕色文字
        
        pygame.display.flip()
    
    def draw(self):
        if self.map_system.is_map_showing():
            self.draw_map()
            return
        
        # 根据状态绘制
        if self.current_state == STATE_CREATE_CHARACTER:
            self._draw_create_character()
        elif self.current_state == STATE_MAIN_GAME:
            self._draw_main_game()
        elif self.current_state == STATE_CANTEEN:
            self._draw_canteen()
        elif self.current_state == STATE_TEACHING:
            self._draw_teaching()
        elif self.current_state == STATE_SPORTS:
            self._draw_sports()
        elif self.current_state == STATE_SUPERMARKET:
            self._draw_supermarket()
        elif self.current_state == STATE_DORM:
            self._draw_dorm()
        elif self.current_state == STATE_STUDENT_CENTER:
            self._draw_student_center()
        elif self.current_state == STATE_HOSPITAL:
            self._draw_hospital()
        
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
        self.draw_text("[空格] 推进一天  [S] 存档  [L] 读档  [M] 打开地图  [Q] 退出", 40, y_offset)
        
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 150, self.height - 80, WHITE, self.large_font)
            self.message_timer -= 1

    def _draw_canteen(self):
        """绘制食堂场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.canteen_background:
            scaled_bg = pygame.transform.scale(self.canteen_background, (self.width, self.height))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.draw_text("食堂", self.width // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域（增加宽度）
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(self.width // 2 - 50, 440, 100, 50)
        
        # 绘制选项框
        if not self.has_eaten:
            # 鸡腿套餐
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.draw_text("鸡腿套餐：金钱-10 心情+10 健康值+10 行动点+1", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
            
            # 营养套餐
            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.draw_text("营养套餐：金钱-15 心情+20 健康值+10 行动点+2", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
            
            # 特色美食
            pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
            self.draw_text("特色美食：金钱-20 心情+30 健康值+10 行动点+3", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))
        else:
            # 已用餐提示
            self.draw_text("已用餐", self.width // 2 - 50, 200, (254, 247, 201), self.large_font)
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 300, self.height - 60, (254, 247, 201), self.large_font)
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
