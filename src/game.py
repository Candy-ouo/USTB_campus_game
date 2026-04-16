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
from src.ui_hud import UIHUD
from src.places.place_canteen import Canteen
from src.places.place_teaching import Teaching
from src.places.place_sports import Sports
from src.places.place_supermarket import Supermarket
from src.places.place_dorm import Dorm
from src.places.place_student_center import StudentCenter
from src.places.place_hospital import Hospital

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
STATE_SCHEDULE = "SCHEDULE"

class Game:
    def __init__(self, character=None, screen=None):
        self.screen = screen
        self.clock = pygame.time.Clock()
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
        
        # 区域状态
        self.has_eaten = False
        self.has_studied = False
        self.has_exercised = False
        self.supermarket_purchases = 0
        self.has_rested = False
        
        # 其他游戏对象
        self.player = Player()
        self.time_system = TimeSystem()
        self.map_system = MapSystem()
        self.ui_hud = UIHUD(self.screen)
        # 初始化场景对象
        self.canteen = Canteen(self)
        self.teaching = Teaching(self)
        self.sports = Sports(self)
        self.supermarket = Supermarket(self)
        self.dorm = Dorm(self)
        self.student_center = StudentCenter(self)
        self.hospital = Hospital(self)
        
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
        
        if character:
            # 角色创建完成，将Character属性传递给Player
            # 主属性
            self.player.knowledge = character.knowledge
            self.player.charm = character.charm
            self.player.physical = character.energy
            # 行动属性
            self.player.living_expenses = character.money
            self.player.action_points = character.action_points
            self.player.mood = character.mood
            self.player.health = character.health
            # 副属性
            self.player.skill = character.skill
            self.player.social = character.social_network
            self.player.reputation = character.reputation
        else:
            self.player.action_points = DAILY_ACTION_POINTS
        
        # 日程安排相关属性
        self.schedule_selected = []  # 已选择的日程
        self.has_scheduled = False  # 是否已经安排日程
    
    def reset(self):
        self.player.reset()
        self.time_system.reset()
        self.player.action_points = DAILY_ACTION_POINTS
        # 重置日程安排相关属性
        self.schedule_selected = []
        self.has_scheduled = False
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
        # 重置区域状态
        self.has_eaten = False  # 重置用餐状态
        self.has_studied = False  # 重置学习状态
        self.has_exercised = False  # 重置运动状态
        self.supermarket_purchases = 0  # 重置超市购买次数
        self.has_rested = False  # 重置休息状态
        # 重置日程安排状态
        self.schedule_selected = []  # 重置已选择的日程
        self.has_scheduled = False  # 重置是否已经安排日程
        
        self.player.add_mood(-2)
        
        if self.time_system.is_ended():
            self.message = "恭喜！你完成了136天的校园生活！"
            self.message_timer = 300
        else:
            self.message = "新的一天开始了"
            self.message_timer = 120
    
    def handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
        
        # 处理UI事件
        ui_event = self.ui_hud.handle_events(events)
        if ui_event == 'MAP':
            # 显示地图
            self.map_system.toggle_map()

        # 根据状态处理事件
        if self.current_state == STATE_CREATE_CHARACTER:
            self._handle_create_character(events)
            # 更新角色创建场景的窗口大小
            if self.create_character_scene is not None:
                self.create_character_scene.width = SCREEN_WIDTH
                self.create_character_scene.height = SCREEN_HEIGHT
        elif self.current_state == STATE_MAIN_GAME:
            self._handle_main_game(events)
        elif self.current_state == STATE_CANTEEN:
            self.canteen.handle_events(events)
        elif self.current_state == STATE_TEACHING:
            self.teaching.handle_events(events)
        elif self.current_state == STATE_SPORTS:
            self.sports.handle_events(events)
        elif self.current_state == STATE_SUPERMARKET:
            self.supermarket.handle_events(events)
        elif self.current_state == STATE_DORM:
            self.dorm.handle_events(events)
        elif self.current_state == STATE_STUDENT_CENTER:
            self.student_center.handle_events(events)
        elif self.current_state == STATE_HOSPITAL:
            self._handle_hospital(events)
        elif self.current_state == STATE_SCHEDULE:
            self._handle_schedule(events)
    
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
                else:
                    # 处理主界面的鼠标点击
                    pos = pygame.mouse.get_pos()
                    # 检查日程安排按钮是否被点击
                    x_offset = self.width - 300
                    y_offset = self.height - 300 + 30 + 5 * 25 + 20 + 30 + 40
                    schedule_button_rect = pygame.Rect(x_offset, y_offset, 280, 50)
                    print(f"鼠标点击位置: {pos}")
                    print(f"日程安排按钮区域: {schedule_button_rect}")
                    print(f"是否点击了按钮: {schedule_button_rect.collidepoint(pos)}")
                    print(f"是否已经安排日程: {self.has_scheduled}")
                    if schedule_button_rect.collidepoint(pos) and not self.has_scheduled:
                        # 跳转到日程安排页面
                        print("跳转到日程安排页面")
                        self.current_state = STATE_SCHEDULE
                        # 重置已选择的日程
                        self.schedule_selected = []
    
    def _draw_schedule(self):
        """绘制日程安排页面"""
        # 绘制背景
        self.screen.fill((220, 180, 140))
        
        # 绘制标题
        title_text = self.large_font.render("每回合日程安排", True, (150, 100, 50))
        title_rect = title_text.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title_text, title_rect)
        
        # 绘制边框
        border_rect = pygame.Rect(50, 100, self.width - 100, self.height - 200)
        pygame.draw.rect(self.screen, (150, 100, 50), border_rect, 3)
        
        # 定义日程数据
        schedules = {
            "理论实验": [
                {"name": "专业课导论", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "编程语言上机课", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "高数课", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "概率论", "hours": 8, "attribute": "theory_experiment", "value": 50},
                {"name": "专业课课设", "hours": 12, "attribute": "theory_experiment", "value": 75}
            ],
            "创新创业": [
                {"name": "生涯规划课", "hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
                {"name": "创造训练", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "创新与专利", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100}
            ],
            "美育素养": [
                {"name": "世界文明史", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "艺术鉴赏", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "基本乐理", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "乐器演奏", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "人际沟通艺术", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75}
            ]
        }
        
        # 绘制日程分类（三列布局）
        column_width = (self.width - 100) // 3
        categories = list(schedules.keys())
        
        for i, category in enumerate(categories):
            # 计算列的位置
            column_x = 50 + i * column_width
            column_y = 140
            
            # 绘制分类标题
            category_text = self.large_font.render(category, True, (150, 100, 50))
            category_rect = category_text.get_rect(center=(column_x + column_width // 2, column_y))
            self.screen.blit(category_text, category_rect)
            
            # 绘制日程项
            item_y = column_y + 40
            item_spacing = 40
            
            for item in schedules[category]:
                # 计算日程项位置
                item_x = column_x + 10
                item_width = column_width - 20
                item_height = 30
                
                # 检查是否被选中
                is_selected = any(selected['name'] == item['name'] for selected in self.schedule_selected)
                
                # 绘制日程项背景
                if is_selected:
                    pygame.draw.rect(self.screen, (255, 215, 0), (item_x, item_y, item_width, item_height))
                    pygame.draw.rect(self.screen, (218, 165, 32), (item_x, item_y, item_width, item_height), 2)
                else:
                    pygame.draw.rect(self.screen, (254, 247, 201), (item_x, item_y, item_width, item_height))
                    pygame.draw.rect(self.screen, (150, 100, 50), (item_x, item_y, item_width, item_height), 2)
                
                # 绘制日程项文本
                item_text = self.font.render(f"{item['name']}: {item['hours']}学时, {self._get_attribute_name(item['attribute'])}+{item['value']}", True, (150, 100, 50))
                self.screen.blit(item_text, (item_x + 10, item_y + 5))
                
                item_y += item_spacing
        
        # 绘制已选择的日程信息
        selected_info_y = 450  # 移到方框内部，课程列表下方
        self.draw_text(f"已选择: {len(self.schedule_selected)}/3项", 100, selected_info_y, (150, 100, 50), self.large_font)
        
        # 计算总学时和预计增加的属性
        total_hours = sum(item['hours'] for item in self.schedule_selected)
        attribute_gains = {}
        for item in self.schedule_selected:
            if item['attribute'] in attribute_gains:
                attribute_gains[item['attribute']] += item['value']
            else:
                attribute_gains[item['attribute']] = item['value']
        
        self.draw_text(f"总学时: {total_hours}", 100, selected_info_y + 30, (150, 100, 50))
        
        # 绘制预计增加的属性
        gain_text = "预计增加: "
        for attr, value in attribute_gains.items():
            gain_text += f"{self._get_attribute_name(attr)}+{value}, "
        if gain_text != "预计增加: ":
            gain_text = gain_text[:-2]  # 移除最后一个逗号和空格
        self.draw_text(gain_text, 100, selected_info_y + 60, (150, 100, 50))
        
        # 绘制操作按钮
        confirm_button_rect = pygame.Rect(self.width // 2 - 200, self.height - 80, 180, 50)
        cancel_button_rect = pygame.Rect(self.width // 2 + 20, self.height - 80, 180, 50)
        
        # 确认选择按钮
        if len(self.schedule_selected) > 0:
            pygame.draw.rect(self.screen, (220, 180, 140), confirm_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), confirm_button_rect, 2)
            self.draw_text("确认选择", confirm_button_rect.x + 40, confirm_button_rect.y + 15, (254, 247, 201), self.large_font)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), confirm_button_rect)
            pygame.draw.rect(self.screen, (50, 50, 50), confirm_button_rect, 2)
            self.draw_text("确认选择", confirm_button_rect.x + 40, confirm_button_rect.y + 15, (200, 200, 200), self.large_font)
        
        # 取消选择按钮
        pygame.draw.rect(self.screen, (220, 180, 140), cancel_button_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), cancel_button_rect, 2)
        self.draw_text("取消选择", cancel_button_rect.x + 40, cancel_button_rect.y + 15, (254, 247, 201), self.large_font)
        
        # 绘制消息
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 150, 580, (150, 100, 50), self.large_font)
            self.message_timer -= 1
    
    def _get_attribute_name(self, attribute):
        """获取属性的中文名称"""
        attribute_names = {
            "theory_experiment": "理论实验",
            "employment_entrepreneurship": "创新创业",
            "aesthetic_cultivation": "美育素养"
        }
        return attribute_names.get(attribute, attribute)
    
    def _handle_schedule(self, events):
        """处理日程安排页面事件"""
        # 定义日程数据
        schedules = {
            "理论实验": [
                {"name": "专业课导论", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "编程语言上机课", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "高数课", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "概率论", "hours": 8, "attribute": "theory_experiment", "value": 50},
                {"name": "专业课课设", "hours": 12, "attribute": "theory_experiment", "value": 75}
            ],
            "创新创业": [
                {"name": "生涯规划课", "hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
                {"name": "创造训练", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "创新与专利", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100}
            ],
            "美育素养": [
                {"name": "世界文明史", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "艺术鉴赏", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "基本乐理", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "乐器演奏", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "人际沟通艺术", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75}
            ]
        }
        
        # 计算日程项的位置（三列布局）
        column_width = (self.width - 100) // 3
        categories = list(schedules.keys())
        
        # 处理鼠标点击事件
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # 遍历所有日程项，检查是否被点击
                for i, category in enumerate(categories):
                    # 计算列的位置
                    column_x = 50 + i * column_width
                    column_y = 140
                    
                    # 绘制日程项
                    item_y = column_y + 40
                    item_spacing = 40
                    
                    for item in schedules[category]:
                        # 计算日程项位置
                        item_x = column_x + 10
                        item_width = column_width - 20
                        item_height = 30
                        item_rect = pygame.Rect(item_x, item_y, item_width, item_height)
                        
                        if item_rect.collidepoint(pos):
                            # 检查是否已经选择了该日程
                            is_selected = any(selected['name'] == item['name'] for selected in self.schedule_selected)
                            if is_selected:
                                # 取消选择
                                self.schedule_selected = [s for s in self.schedule_selected if s['name'] != item['name']]
                            else:
                                # 检查是否已经选择了3项
                                if len(self.schedule_selected) >= 3:
                                    # 替换最早选择的项
                                    self.schedule_selected.pop(0)
                                # 添加到选择列表
                                self.schedule_selected.append(item)
                        
                        item_y += item_spacing
        
        # 处理操作按钮点击
        confirm_button_rect = pygame.Rect(self.width // 2 - 200, self.height - 80, 180, 50)
        cancel_button_rect = pygame.Rect(self.width // 2 + 20, self.height - 80, 180, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回主界面
                    self.current_state = STATE_MAIN_GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if confirm_button_rect.collidepoint(pos):
                    # 确认选择
                    if len(self.schedule_selected) > 0:
                        # 记录属性变化前的值
                        before_theory = self.player.theory_experiment
                        before_employment = self.player.employment_entrepreneurship
                        before_aesthetic = self.player.aesthetic_cultivation
                        
                        # 执行属性修改
                        for item in self.schedule_selected:
                            if item['attribute'] == "theory_experiment":
                                self.player.add_theory_experiment(item['value'])
                            elif item['attribute'] == "employment_entrepreneurship":
                                self.player.add_employment_entrepreneurship(item['value'])
                            elif item['attribute'] == "aesthetic_cultivation":
                                self.player.add_aesthetic_cultivation(item['value'])
                        # 计算总学时（不扣除行动力）
                        total_hours = sum(item['hours'] for item in self.schedule_selected)
                        # 标记为已安排日程
                        self.has_scheduled = True
                        # 显示消息
                        self.message = f"日程安排完成！选择了{len(self.schedule_selected)}项日程，总学时{total_hours}。"
                        self.message_timer = 120
                        
                        # 在终端打印属性变化
                        print("\n=== 日程安排属性变化 ===")
                        print(f"理论实验: {before_theory} → {self.player.theory_experiment} (+{self.player.theory_experiment - before_theory})")
                        print(f"创新创业: {before_employment} → {self.player.employment_entrepreneurship} (+{self.player.employment_entrepreneurship - before_employment})")
                        print(f"美育素养: {before_aesthetic} → {self.player.aesthetic_cultivation} (+{self.player.aesthetic_cultivation - before_aesthetic})")
                        print(f"总学时: {total_hours}")
                        print(f"剩余行动力: {self.player.action_points}")
                        print("=====================\n")
                        
                        # 返回主界面
                        self.current_state = STATE_MAIN_GAME
                elif cancel_button_rect.collidepoint(pos):
                    # 取消选择
                    self.schedule_selected = []
                    # 返回主界面
                    self.current_state = STATE_MAIN_GAME
                    
    def do_action(self, action_name):
        if self.player.action_points <= 0:
            self.message = "行动点不足！"
            self.message_timer = 60
            return
        
        self.player.action_points -= 1
        
        if action_name == "学习":
            self.player.add_knowledge(5)
            self.player.add_mood(-3)
            self.player.add_physical(-2)
            self.message = "努力学习，学识+5"
        elif action_name == "运动":
            self.player.add_physical(5)
            self.player.add_mood(2)
            self.player.add_charm(2)
            self.message = "运动健身，体能+5"
        elif action_name == "休息":
            self.player.add_mood(5)
            self.player.add_physical(2)
            self.message = "好好休息，恢复体力"
        elif action_name == "打工":
            self.player.add_living_expenses(100)
            self.player.add_mood(-5)
            self.player.add_skill(2)
            self.message = "辛苦打工，生活费+100"
        elif action_name == "社交":
            self.player.add_charm(3)
            self.player.add_mood(5)
            self.player.add_social(2)
            self.player.add_living_expenses(-20)
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
            if attr == 'knowledge':
                self.player.add_knowledge(value)
            elif attr == 'charm':
                self.player.add_charm(value)
            elif attr == 'physical':
                self.player.add_physical(value)
            elif attr == 'living_expenses':
                self.player.add_living_expenses(value)
            elif attr == 'mood':
                self.player.add_mood(value)
            elif attr == 'skill':
                self.player.add_skill(value)
            elif attr == 'social':
                self.player.add_social(value)
            elif attr == 'reputation':
                self.player.add_reputation(value)
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
            self.canteen.draw()
        elif self.current_state == STATE_TEACHING:
            self.teaching.draw()
        elif self.current_state == STATE_SPORTS:
            self.sports.draw()
        elif self.current_state == STATE_SUPERMARKET:
            self.supermarket.draw()
        elif self.current_state == STATE_DORM:
            self.dorm.draw()
        elif self.current_state == STATE_STUDENT_CENTER:
            self.student_center.draw()
        elif self.current_state == STATE_HOSPITAL:
            self._draw_hospital()
        elif self.current_state == STATE_SCHEDULE:
            self._draw_schedule()
        
        pygame.display.flip()
    
    def _draw_create_character(self):
        """绘制角色创建场景"""
        if self.create_character_scene is not None:
            self.create_character_scene.update()
            self.create_character_scene.draw()
    
    def _draw_main_game(self):
        """绘制主游戏场景"""
        self.screen.fill(BLACK)
        
        # 更新时间信息到UI HUD
        year = self.time_system.get_year()
        month = self.time_system.get_month()
        week = self.time_system.get_week_in_month()
        self.ui_hud.update_time(year, month, week)
        
        # 绘制其他UI
        time_display = self.time_system.get_time_display()
        self.ui_hud.draw_all(time_display, self.player)
        
        # 绘制日程安排按钮
        y_offset += 40
        schedule_button_rect = pygame.Rect(x_offset, y_offset, 280, 50)
        if not self.has_scheduled:
            pygame.draw.rect(self.screen, (220, 180, 140), schedule_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), schedule_button_rect, 2)
            self.draw_text("日程安排", schedule_button_rect.x + 100, schedule_button_rect.y + 15, (254, 247, 201), self.large_font)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), schedule_button_rect)
            pygame.draw.rect(self.screen, (50, 50, 50), schedule_button_rect, 2)
            self.draw_text("已安排日程", schedule_button_rect.x + 80, schedule_button_rect.y + 15, (200, 200, 200), self.large_font)
        
        if self.message_timer > 0:
            self.draw_text(self.message, self.width // 2 - 150, self.height - 80, WHITE, self.large_font)
            self.message_timer -= 1

        if self.message_timer > 0:
            # 消息显示配置，可根据需要修改
            message_x = SCREEN_WIDTH // 2 - 150  # 消息X坐标
            message_y = SCREEN_HEIGHT - 80  # 消息Y坐标
            message_color = WHITE  # 消息颜色
            message_font = self.large_font  # 消息字体（可改为self.font或其他字体）
            self.draw_text(self.message, message_x, message_y, message_color, message_font)
            self.message_timer -= 1
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
