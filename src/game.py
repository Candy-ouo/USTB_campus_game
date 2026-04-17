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

# 时间季节面板类
class TimeSeasonPanel:
    def __init__(self, screen):
        self.screen = screen
    
    def draw(self, time_system):
        pass

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
STATE_FINAL_EXAM = "FINAL_EXAM"
STATE_SCHEDULE = "SCHEDULE"

class Game:
    def __init__(self, character=None, screen=None):
        if screen is None:
            pygame.init()
            # 创建可调整大小的窗口
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            pygame.display.set_caption("北科校园物语")
        else:
            self.screen = screen
        
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
        self.current_state = STATE_DORM if character else STATE_CREATE_CHARACTER
        self.previous_state = self.current_state  # 初始化前一个状态
        print(f"游戏状态设置为: {self.current_state}")
        
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
        self.has_rested = False
        
        # 其他游戏对象
        self.player = Player()
        self.time_system = TimeSystem()
        self.map_system = MapSystem()
        self.ui_hud = UIHUD(self.screen)
        self.time_season_panel = TimeSeasonPanel(self.screen)
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
        
        # 期末成绩记录
        self.final_scores = []
        self.final_gpas = []
        # 当前期末成绩信息
        self.current_final_score = 0
        self.current_final_grade = ""
        self.current_final_gpa = 0.0
        self.current_need_makeup = False
        
        # 加载地图背景图片
        self.map_background = None
        map_image_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'map_background.png')
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
            self.player.knowledge_level = character.knowledge_level
            self.player.charm = character.charm
            self.player.charm_level = character.charm_level
            self.player.physical = character.physical
            self.player.physical_level = character.physical_level
            # 行动属性
            self.player.living_expenses = character.living_expenses
            self.player.action_points = character.action_points
            self.player.mood = character.mood
            self.player.health = character.health
            # 副属性
            self.player.skill = character.skill
            self.player.social = character.social
            self.player.reputation = character.reputation
            # 学习属性
            self.player.theory_experiment = character.theory_experiment
            self.player.employment_entrepreneurship = character.employment_entrepreneurship
            self.player.aesthetic_cultivation = character.aesthetic_cultivation
        else:
            self.player.action_points = DAILY_ACTION_POINTS
        
        # 日程安排相关属性
        self.schedule_selected = []  # 已选择的日程
        self.has_scheduled = False  # 是否已经安排日程
        self.schedule_scroll_offsets = [0, 0, 0]  # 每列的滚动偏移量
        self.course_study_counts = {}  # 课程学习次数追踪
    
    def reset(self):
        self.player.reset()
        self.time_system.reset()
        self.player.action_points = DAILY_ACTION_POINTS
        # 重置日程安排相关属性
        self.schedule_selected = []
        self.has_scheduled = False
        self.course_study_counts = {}
        self.message = "新游戏开始！"
        self.message_timer = 120
        self.final_scores = []
        self.final_gpas = []
    
    def save_game(self):
        try:
            save_data = {
                'player': self.player.to_dict(),
                'time_system': self.time_system.to_dict(),
                'course_study_counts': self.course_study_counts
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
                if 'course_study_counts' in save_data:
                    self.course_study_counts = save_data['course_study_counts']
                else:
                    self.course_study_counts = {}
                self.message = "游戏已加载！"
                self.message_timer = 120
            else:
                self.message = "没有找到存档！"
                self.message_timer = 120
        except Exception as e:
            self.message = f"加载失败: {str(e)}"
            self.message_timer = 120
    
    def calculate_final_score(self, current_year=None):
        """计算期末成绩"""
        knowledge = self.player.knowledge
        knowledge_level = self.player.knowledge_level
        theory_experiment = self.player.theory_experiment
        mood = self.player.mood
        if current_year is None:
            current_year = self.time_system.get_year()
        
        # 检查学识等级是否符合当前学年要求
        if knowledge_level < current_year:
            return 0, "F", 1.0, True
        
        # 检查学识是否低于30
        if knowledge < 30:
            return 0, "F", 1.0, True
        
        # 心情影响：心情低于50时，属性效果减半
        mood_multiplier = 0.5 if mood < 50 else 1.0
        
        # 计算分数
        score = (knowledge * mood_multiplier / 100) * 60 + (theory_experiment * mood_multiplier / 300) * 40
        score = max(0, min(100, score))
        score = round(score, 1)
        
        # 计算评级和绩点
        if score >= 90:
            grade = "A"
            gpa = 4.0
        elif score >= 85:
            grade = "A-"
            gpa = 3.7
        elif score >= 80:
            grade = "B+"
            gpa = 3.4
        elif score >= 75:
            grade = "B"
            gpa = 3.0
        elif score >= 70:
            grade = "B-"
            gpa = 2.4
        elif score >= 65:
            grade = "C+"
            gpa = 2.0
        elif score >= 60:
            grade = "C"
            gpa = 1.0
        else:
            grade = "F"
            gpa = 1.0
        
        # 检查是否需要补考
        need_makeup = score < 60 or knowledge < 30
        
        return score, grade, gpa, need_makeup
    
    def handle_final_exam_week(self, current_year=None):
        """处理期末周结算"""
        # 保存结算前的理论实验值
        self.current_theory_experiment = self.player.theory_experiment
        
        score, grade, gpa, need_makeup = self.calculate_final_score(current_year)
        
        # 记录成绩
        self.final_scores.append(score)
        self.final_gpas.append(gpa)
        
        # 处理补考
        if need_makeup:
            self.player.add_mood(-20)
            self.player.add_charm(-10)
            self.player.add_health(-10)
        else:
            # 奖学金机制
            if grade == "A":
                self.player.add_living_expenses(100)
            elif grade == "A-":
                self.player.add_living_expenses(50)
        
        # 存储当前期末成绩信息
        self.current_final_score = score
        self.current_final_grade = grade
        self.current_final_gpa = gpa
        self.current_need_makeup = need_makeup
        
        # 切换到期末成绩显示状态
        self.current_state = STATE_FINAL_EXAM
    
    def advance_day(self):
        if self.time_system.is_ended():
            self.message = "游戏已结束！"
            self.message_timer = 120
            return
        
        # 记录当前天数、是否是期末周、当前学年
        current_day = self.time_system.day
        is_current_final_week = self.time_system.is_final_exam_week()
        current_year = self.time_system.get_year()  # 保存结算前的学年
        
        self.time_system.next_day()
        # 设置行动点，健康值低于60时减半
        if self.player.health < 60:
            self.player.action_points = DAILY_ACTION_POINTS // 2
        else:
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
        
        # 处理期末周结算（在期末周结束后显示）
        if is_current_final_week:
            self.handle_final_exam_week(current_year)  # 传递结算前的学年
            # 期末周结算后重置理论实验
            self.player.theory_experiment = 0
        
        if self.time_system.is_ended():
            # 游戏结束，进行结局判定
            self.handle_game_end()
        elif not is_current_final_week:
            # 如果不是期末周结束，显示正常的新天消息
            self.message = "新的一天开始了！"
            self.message_timer = 120
    
    def handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                # 无论当前状态是什么，只要按M键就切换地图
                elif event.key == pygame.K_m:
                    self.map_system.toggle_map()
                    self.map_system.clear_active_area()

        # 处理UI事件
        ui_event = self.ui_hud.handle_events(events)
        if ui_event == 'MAP':
            # 显示地图
            self.map_system.toggle_map()
        elif ui_event == 'SCHEDULE':
            # 记录当前场景
            self.previous_state = self.current_state
            # 跳转到日程安排页面
            self.current_state = STATE_SCHEDULE
            # 如果还没有安排日程，重置已选择的日程
            if not self.has_scheduled:
                self.schedule_selected = []
        elif ui_event == 'FILE':
            # 记录当前场景
            self.previous_state = self.current_state
            # 处理档案事件
            pass
        elif ui_event == 'BAG':
            # 记录当前场景
            self.previous_state = self.current_state
            # 处理背包事件
            pass
        elif ui_event == 'RELATIONSHIP':
            # 记录当前场景
            self.previous_state = self.current_state
            # 处理关系事件
            pass

        # 如果地图显示，处理地图相关事件
        if self.map_system.is_map_showing():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # 检测是否点击了关闭按钮
                    if self.map_system.is_close_button_clicked(pos):
                        self.map_system.toggle_map()  # 关闭地图
                        return
                    # 检测是否点击了地图区域
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
                self.hospital.handle_events(events)
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
                self.current_state = STATE_DORM  # 直接切换到宿舍场景
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
                        # 检查是否生病
                        if self.player.is_sick:
                            if area_id == 'hospital':
                                # 切换到校医院场景
                                self.map_system.toggle_map()  # 确保地图不显示
                                self.current_state = STATE_HOSPITAL
                            else:
                                # 生病时只能去校医院
                                self.message = "你生病了，只能去校医院！"
                                self.message_timer = 90
                        else:
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
                    # 检查"安排"图标是否被点击
                    # 根据截图，"安排"图标位于界面右侧，地图图标的下方
                    schedule_icon_rect = pygame.Rect(self.width - 100, self.height - 150, 80, 80)
                    if schedule_icon_rect.collidepoint(pos):
                        # 跳转到日程安排页面
                        self.current_state = STATE_SCHEDULE
                        # 如果还没有安排日程，重置已选择的日程
                        if not self.has_scheduled:
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
                {"name": "固体物理", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "材料分析技术", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "量子力学导论", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "大学物理实验", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "数理方法", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "材料合成与制备", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "金相分析实验", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "工程制图", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "计算机辅助设计", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "材料性能实验", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "大学英语", "hours": 8, "attribute": "theory_experiment", "value": 50},
                {"name": "思修与法律基础", "hours": 8, "attribute": "theory_experiment", "value": 50},
                {"name": "大学体育", "hours": 8, "attribute": "theory_experiment", "value": 50},
            ],
            "创新创业": [
                {"name": "科研项目实训", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "企业实习实践", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "专利撰写与申报", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "创业大赛指导", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "本科就业指导", "hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
                {"name": "科研伦理与规范", "hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
                {"name": "科技文献检索", "hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
            ],
            "美育素养": [
                {"name": "交响乐团鉴赏", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "中国书法艺术", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "国画赏析", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "影视鉴赏", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "西方哲学史", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "演讲与口才", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "摄影技术", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "舞蹈基础", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "茶文化", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "中外民俗", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "心理健康", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "安全教育", "hours": 8, "attribute": "aesthetic_cultivation", "value": 50},
                {"name": "通识课任选", "hours": 8, "attribute": "aesthetic_cultivation", "value": 50},
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
            item_spacing = 40
            items_per_column = 6
            
            # 计算当前显示的课程范围
            start_index = max(0, -self.schedule_scroll_offsets[i] // item_spacing)
            end_index = min(len(schedules[category]), start_index + items_per_column)
            
            # 绘制课程（过滤掉已修满的课程）
            item_y = column_y + 40
            visible_items = []
            
            # 先过滤出未修满的课程
            for j in range(len(schedules[category])):
                item = schedules[category][j]
                course_name = item['name']
                study_count = self.course_study_counts.get(course_name, 0)
                if study_count < item['hours']:
                    visible_items.append(item)
            
            # 计算可见课程的显示范围
            visible_start = max(0, -self.schedule_scroll_offsets[i] // item_spacing)
            visible_end = min(len(visible_items), visible_start + items_per_column)
            
            # 绘制可见的课程
            for j in range(visible_start, visible_end):
                item = visible_items[j]
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
                    if self.has_scheduled:
                        # 已经安排了日程，禁用未选中的日程项
                        pygame.draw.rect(self.screen, (200, 200, 200), (item_x, item_y, item_width, item_height))
                        pygame.draw.rect(self.screen, (100, 100, 100), (item_x, item_y, item_width, item_height), 2)
                    else:
                        pygame.draw.rect(self.screen, (254, 247, 201), (item_x, item_y, item_width, item_height))
                        pygame.draw.rect(self.screen, (150, 100, 50), (item_x, item_y, item_width, item_height), 2)
                
                # 绘制日程项文本
                if self.has_scheduled:
                    # 已经安排了日程，使用灰色文本
                    item_text = self.font.render(f"{item['name']}: {item['hours']}学时, {self._get_attribute_name(item['attribute'])}+{item['value']}", True, (100, 100, 100))
                else:
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
        
        # 提示信息
        self.draw_text("选择课程并执行后立即进入下一周", 100, selected_info_y + 60, (150, 100, 50))
        
        # 绘制操作按钮
        confirm_button_rect = pygame.Rect(self.width // 2 - 200, self.height - 80, 180, 50)
        cancel_button_rect = pygame.Rect(self.width // 2 + 20, self.height - 80, 180, 50)
        
        # 执行并进入下一回合按钮
        if len(self.schedule_selected) > 0 and not self.has_scheduled:
            pygame.draw.rect(self.screen, (220, 180, 140), confirm_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), confirm_button_rect, 2)
            # 计算文本宽度，使文本居中
            text_surface = self.large_font.render("执行", True, (254, 247, 201))
            text_x = confirm_button_rect.x + (confirm_button_rect.width - text_surface.get_width()) // 2
            self.draw_text("执行", text_x, confirm_button_rect.y + 15, (254, 247, 201), self.large_font)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), confirm_button_rect)
            pygame.draw.rect(self.screen, (50, 50, 50), confirm_button_rect, 2)
            # 计算文本宽度，使文本居中
            text_surface = self.large_font.render("执行", True, (200, 200, 200))
            text_x = confirm_button_rect.x + (confirm_button_rect.width - text_surface.get_width()) // 2
            self.draw_text("执行", text_x, confirm_button_rect.y + 15, (200, 200, 200), self.large_font)
        
        # 取消选择按钮
        pygame.draw.rect(self.screen, (220, 180, 140), cancel_button_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), cancel_button_rect, 2)
        # 计算文本宽度，使文本居中
        text_surface = self.large_font.render("取消", True, (254, 247, 201))
        text_x = cancel_button_rect.x + (cancel_button_rect.width - text_surface.get_width()) // 2
        self.draw_text("取消", text_x, cancel_button_rect.y + 15, (254, 247, 201), self.large_font)
        
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
                {"name": "固体物理", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "材料分析技术", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "量子力学导论", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "大学物理实验", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "数理方法", "hours": 16, "attribute": "theory_experiment", "value": 100},
                {"name": "材料合成与制备", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "金相分析实验", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "工程制图", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "计算机辅助设计", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "材料性能实验", "hours": 12, "attribute": "theory_experiment", "value": 75},
                {"name": "大学英语", "hours": 8, "attribute": "theory_experiment", "value": 50},
                {"name": "思修与法律基础", "hours": 8, "attribute": "theory_experiment", "value": 50},
                {"name": "大学体育", "hours": 8, "attribute": "theory_experiment", "value": 50},
            ],
            "创新创业": [
                {"name": "科研项目实训", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "企业实习实践", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "专利撰写与申报", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "创业大赛指导", "hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
                {"name": "本科就业指导", "hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
                {"name": "科研伦理与规范", "hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
                {"name": "科技文献检索", "hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
            ],
            "美育素养": [
                {"name": "交响乐团鉴赏", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "中国书法艺术", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "国画赏析", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "影视鉴赏", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "西方哲学史", "hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
                {"name": "演讲与口才", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "摄影技术", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "舞蹈基础", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "茶文化", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "中外民俗", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "心理健康", "hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
                {"name": "安全教育", "hours": 8, "attribute": "aesthetic_cultivation", "value": 50},
                {"name": "通识课任选", "hours": 8, "attribute": "aesthetic_cultivation", "value": 50},
            ]
        }
        
        # 计算日程项的位置（三列布局）
        column_width = (self.width - 100) // 3
        categories = list(schedules.keys())
        
        # 处理操作按钮点击
        confirm_button_rect = pygame.Rect(self.width // 2 - 200, self.height - 80, 180, 50)
        cancel_button_rect = pygame.Rect(self.width // 2 + 20, self.height - 80, 180, 50)
        
        # 处理所有事件
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回之前的场景
                    self.current_state = self.previous_state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 只处理鼠标左键点击
                if event.button != 1:
                    continue
                
                pos = pygame.mouse.get_pos()
                
                # 检查确认按钮
                if confirm_button_rect.collidepoint(pos):
                    # 执行并进入下一回合
                    if len(self.schedule_selected) > 0 and not self.has_scheduled:
                        # 记录属性变化前的值
                        before_theory = self.player.theory_experiment
                        before_employment = self.player.employment_entrepreneurship
                        before_aesthetic = self.player.aesthetic_cultivation
                        
                        # 计算总学时（不扣除行动力）
                        total_hours = sum(item['hours'] for item in self.schedule_selected)
                        
                        # 执行属性修改（累计学习次数，达到学时时增加属性）
                        for item in self.schedule_selected:
                            course_name = item['name']
                            # 初始化课程学习次数
                            if course_name not in self.course_study_counts:
                                self.course_study_counts[course_name] = 0
                            
                            # 增加学习次数
                            self.course_study_counts[course_name] += 1
                            
                            # 检查是否达到学时要求
                            if self.course_study_counts[course_name] >= item['hours']:
                                # 增加属性
                                if item['attribute'] == "theory_experiment":
                                    self.player.add_theory_experiment(item['value'])
                                elif item['attribute'] == "employment_entrepreneurship":
                                    self.player.add_employment_entrepreneurship(item['value'])
                                elif item['attribute'] == "aesthetic_cultivation":
                                    self.player.add_aesthetic_cultivation(item['value'])
                                # 重置学习次数（可选：如果课程可以重复学习）
                                # self.course_study_counts[course_name] = 0
                        
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
                        # 打印课程学习进度
                        print("\n=== 课程学习进度 ===")
                        for item in self.schedule_selected:
                            course_name = item['name']
                            count = self.course_study_counts.get(course_name, 0)
                            print(f"{course_name}: {count}/{item['hours']} 学时")
                        print("=====================\n")
                        
                        # 进入下一回合
                        self.time_system.next_week()
                        # 重置行动点
                        self.player.action_points = DAILY_ACTION_POINTS
                        # 重置日程安排相关属性
                        self.schedule_selected = []
                        self.has_scheduled = False
                        # 返回主界面
                        self.current_state = STATE_MAIN_GAME
                elif cancel_button_rect.collidepoint(pos):
                    # 取消选择
                    self.schedule_selected = []
                    # 返回主界面
                    self.current_state = STATE_MAIN_GAME
                else:
                    # 检查日程项点击
                    if not self.has_scheduled:
                        for i, category in enumerate(categories):
                            # 计算列的位置
                            column_x = 50 + i * column_width
                            column_y = 140
                            
                            # 绘制日程项
                            item_spacing = 40
                            items_per_column = 6
                            
                            # 计算当前显示的课程范围
                            start_index = max(0, -self.schedule_scroll_offsets[i] // item_spacing)
                            end_index = min(len(schedules[category]), start_index + items_per_column)
                            
                            # 检查日程项点击
                            item_y = column_y + 40
                            # 过滤出未修满的课程
                            visible_items = []
                            for j in range(len(schedules[category])):
                                item = schedules[category][j]
                                course_name = item['name']
                                study_count = self.course_study_counts.get(course_name, 0)
                                if study_count < item['hours']:
                                    visible_items.append(item)
                            
                            # 计算当前显示的可见课程范围
                            visible_start = max(0, -self.schedule_scroll_offsets[i] // item_spacing)
                            visible_end = min(len(visible_items), visible_start + items_per_column)
                            
                            # 检查可见课程的点击
                            item_y = column_y + 40
                            for j in range(visible_start, visible_end):
                                item = visible_items[j]
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
            elif event.type == pygame.MOUSEWHEEL:
                # 处理鼠标滚轮事件，实现每列独立滚动
                pos = pygame.mouse.get_pos()
                for i in range(3):
                    column_x = 50 + i * column_width
                    column_rect = pygame.Rect(column_x, 140, column_width, self.height - 300)
                    if column_rect.collidepoint(pos):
                        # 过滤出未修满的课程
                        visible_items = []
                        for item in schedules[categories[i]]:
                            course_name = item['name']
                            study_count = self.course_study_counts.get(course_name, 0)
                            if study_count < item['hours']:
                                visible_items.append(item)
                        
                        # 计算最大滚动偏移量
                        items_per_column = 6
                        item_spacing = 40
                        max_scroll = (len(visible_items) - items_per_column) * item_spacing
                        if max_scroll < 0:
                            max_scroll = 0
                        
                        # 滚动速度
                        scroll_speed = item_spacing  # 每次滚动一个课程的高度
                        
                        # 更新滚动偏移量
                        if event.y > 0:  # 向上滚动
                            self.schedule_scroll_offsets[i] = min(0, self.schedule_scroll_offsets[i] + scroll_speed)
                        else:  # 向下滚动
                            self.schedule_scroll_offsets[i] = max(-max_scroll, self.schedule_scroll_offsets[i] - scroll_speed)
                        # 返回之前的场景
                        self.current_state = self.previous_state
                elif cancel_button_rect.collidepoint(pos):
                    # 取消选择
                    self.schedule_selected = []
                    # 返回之前的场景
                    self.current_state = self.previous_state
                    
    def do_action(self, action_name):
        if self.player.action_points <= 0:
            self.message = "行动点不足！"
            self.message_timer = 60
            return
        
        self.player.action_points -= 1
        current_year = self.time_system.get_year()
        
        if action_name == "学习":
            self.player.add_knowledge(5, current_year)
            self.player.add_mood(-3)
            self.player.add_physical(-2, current_year)
            self.message = "努力学习，学识+5"
        elif action_name == "运动":
            self.player.add_physical(5, current_year)
            self.player.add_mood(2)
            self.player.add_charm(2, current_year)
            self.message = "运动健身，体能+5"
        elif action_name == "休息":
            self.player.add_mood(5)
            self.player.add_physical(2, current_year)
            self.message = "好好休息，恢复体力"
        elif action_name == "打工":
            self.player.add_living_expenses(100)
            self.player.add_mood(-5)
            self.player.add_skill(2)
            self.message = "辛苦打工，生活费+100"
        elif action_name == "社交":
            self.player.add_charm(3, current_year)
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
    
    def draw_text(self, text, x, y, color, font=None):
        """绘制文本"""
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_message(self):
        """绘制消息"""
        if self.message_timer > 0:
            # 创建消息背景框
            message_lines = self.message.split('\n')
            max_line_width = max([self.large_font.size(line)[0] for line in message_lines])
            box_width = max_line_width + 40
            box_height = len(message_lines) * 30 + 20
            
            # 计算消息框位置（居中显示）
            box_x = self.width // 2 - box_width // 2
            box_y = self.height // 2 - box_height // 2
            
            # 绘制背景框
            pygame.draw.rect(self.screen, (0, 0, 0, 180), (box_x, box_y, box_width, box_height), border_radius=10)
            pygame.draw.rect(self.screen, (254, 247, 201), (box_x, box_y, box_width, box_height), 2, border_radius=10)
            
            # 绘制消息文本
            for i, line in enumerate(message_lines):
                text_x = box_x + 20
                text_y = box_y + 10 + i * 30
                self.draw_text(line, text_x, text_y, (254, 247, 201), self.large_font)
            
            self.message_timer -= 1
    
    def draw_map(self):
        # 绘制地图背景图片
        if self.map_system.map_image:
            # 缩放地图图像以适应设置的大小
            scaled_map = pygame.transform.scale(self.map_system.map_image, (int(self.map_system.map_width * 0.6), int(self.map_system.map_height * 0.6)))
            # 计算地图居中位置
            map_x = (SCREEN_WIDTH - scaled_map.get_width()) // 2
            map_y = (SCREEN_HEIGHT - scaled_map.get_height()) // 2
            self.screen.blit(scaled_map, (map_x, map_y))
        elif self.map_background:
            self.screen.blit(self.map_background, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        
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
        
        # 绘制关闭按钮
        if self.map_system.close_button:
            # 缩放关闭按钮图像以适应设置的大小
            scaled_close_button = pygame.transform.scale(self.map_system.close_button, (self.map_system.close_button_rect.width, self.map_system.close_button_rect.height))
            self.screen.blit(scaled_close_button, self.map_system.close_button_rect)
        
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
            self.hospital.draw()
        elif self.current_state == STATE_SCHEDULE:
            self._draw_schedule()
        elif self.current_state == STATE_FINAL_EXAM:
            self._draw_final_exam()
        
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
    
    def handle_game_end(self):
        """处理游戏结束，进行结局判定"""
        # 计算平均成绩和平均绩点
        if not self.final_scores or not self.final_gpas:
            self.message = "游戏结束！但没有期末成绩记录。"
            self.message_timer = 300
            return
        
        avg_score = sum(self.final_scores) / len(self.final_scores)
        avg_gpa = sum(self.final_gpas) / len(self.final_gpas)
        
        # 检查是否能顺利毕业
        can_graduate = False
        if (avg_score >= 60 and avg_gpa >= 1.0 and
            self.player.knowledge_level >= 4 and self.player.knowledge >= 60 and
            self.player.theory_experiment >= 600 and
            self.player.employment_entrepreneurship >= 200 and
            self.player.aesthetic_cultivation >= 200 and
            self.player.health >= 60 and
            self.player.mood >= 60 and
            self.player.skill >= 50 and
            self.player.social >= 30 and
            self.player.reputation >= 20):
            can_graduate = True
        
        if not can_graduate:
            self.message = "很遗憾，你未能顺利毕业，需要延毕。"
            self.message_timer = 300
            return
        
        # 顺利毕业，进行结局判定
        # 优先级：保研 > 考研 > 优质就业 > 普通就业/创业
        
        # 1. 保研
        if (avg_score >= 85 and avg_gpa >= 3.7 and
            self.player.knowledge_level >= 4 and self.player.knowledge >= 90 and
            self.player.charm_level >= 2 and self.player.charm >= 70 and
            self.player.physical_level >= 4 and self.player.physical >= 50 and
            self.player.theory_experiment >= 800 and
            self.player.employment_entrepreneurship >= 200 and
            self.player.aesthetic_cultivation >= 200 and
            self.player.skill >= 100 and
            self.player.reputation >= 80 and
            self.player.social >= 70):
            self.message = "恭喜！你成功保研了！"
            self.message_timer = 300
            return
        
        # 2. 考研上岸
        if (avg_score >= 75 and avg_gpa >= 3.0 and
            self.player.knowledge_level >= 4 and self.player.knowledge >= 75 and
            self.player.charm_level >= 2 and self.player.charm >= 50 and
            self.player.physical_level >= 4 and self.player.physical >= 60 and
            self.player.theory_experiment >= 600 and
            self.player.employment_entrepreneurship >= 200 and
            self.player.aesthetic_cultivation >= 200 and
            self.player.skill >= 80 and
            self.player.reputation >= 50 and
            self.player.social >= 40):
            self.message = "恭喜！你考研上岸了！"
            self.message_timer = 300
            return
        
        # 3. 优质就业
        if (avg_score >= 70 and avg_gpa >= 2.4 and
            self.player.knowledge_level >= 4 and self.player.knowledge >= 70 and
            self.player.charm_level >= 2 and self.player.charm >= 80 and
            self.player.physical_level >= 4 and self.player.physical >= 50 and
            self.player.theory_experiment >= 500 and
            self.player.employment_entrepreneurship >= 300 and
            self.player.aesthetic_cultivation >= 200 and
            self.player.skill >= 150 and
            self.player.reputation >= 60 and
            self.player.social >= 100):
            self.message = "恭喜！你获得了优质就业机会！"
            self.message_timer = 300
            return
        
        # 4. 普通就业
        if (avg_score >= 60 and avg_gpa >= 1.0 and
            self.player.knowledge_level >= 4 and self.player.knowledge >= 60 and
            self.player.charm_level >= 2 and self.player.charm >= 50 and
            self.player.physical_level >= 4 and self.player.physical >= 50 and
            self.player.theory_experiment >= 500 and
            self.player.employment_entrepreneurship >= 300 and
            self.player.aesthetic_cultivation >= 200 and
            self.player.skill >= 130 and
            self.player.reputation >= 50 and
            self.player.social >= 60):
            self.message = "恭喜！你获得了普通就业机会。"
            self.message_timer = 300
            return
        
        # 5. 创业
        if (avg_score >= 65 and avg_gpa >= 2.0 and
            self.player.knowledge_level >= 4 and self.player.knowledge >= 60 and
            self.player.charm_level >= 3 and self.player.charm >= 80 and
            self.player.physical_level >= 4 and self.player.physical >= 50 and
            self.player.theory_experiment >= 500 and
            self.player.employment_entrepreneurship >= 400 and
            self.player.aesthetic_cultivation >= 200 and
            self.player.skill >= 170 and
            self.player.reputation >= 80 and
            self.player.social >= 120):
            self.message = "恭喜！你成功创业了！"
            self.message_timer = 300
            return
        
        # 其他情况
        self.message = "游戏结束！你顺利毕业了。"
        self.message_timer = 300
    
    def _draw_final_exam(self):
        """绘制期末成绩单"""
        # 绘制背景
        self.screen.fill((240, 240, 240))
        
        # 绘制成绩单边框
        transcript_width = 400
        transcript_height = 350
        transcript_x = self.width // 2 - transcript_width // 2
        transcript_y = self.height // 2 - transcript_height // 2
        
        # 绘制成绩单背景
        pygame.draw.rect(self.screen, (255, 255, 255), (transcript_x, transcript_y, transcript_width, transcript_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (transcript_x, transcript_y, transcript_width, transcript_height), 2)
        
        # 绘制标题
        self.draw_text("成绩单", transcript_x + 150, transcript_y + 20, (0, 0, 0), self.large_font)
        
        # 绘制科目和成绩
        subjects = ["学识", "理论实验"]
        mood = self.player.mood
        mood_multiplier = 0.5 if mood < 50 else 1.0
        
        if mood < 50:
            scores = [
                int(self.player.knowledge * mood_multiplier),
                int(self.current_theory_experiment * mood_multiplier)
            ]
        else:
            scores = [
                int(self.player.knowledge),
                int(self.current_theory_experiment)
            ]
        
        y_offset = 70
        for i, (subject, score) in enumerate(zip(subjects, scores)):
            self.draw_text(f"{subject}", transcript_x + 50, transcript_y + y_offset + i * 40, (0, 0, 0))
            if subject == "理论实验":
                if mood < 50:
                    self.draw_text(f"{score}/150", transcript_x + 250, transcript_y + y_offset + i * 40, (0, 0, 0))
                else:
                    self.draw_text(f"{score}/300", transcript_x + 250, transcript_y + y_offset + i * 40, (0, 0, 0))
            else:
                if mood < 50:
                    self.draw_text(f"{score}/50", transcript_x + 250, transcript_y + y_offset + i * 40, (0, 0, 0))
                else:
                    self.draw_text(f"{score}/100", transcript_x + 250, transcript_y + y_offset + i * 40, (0, 0, 0))
        
        # 绘制期末周结果
        self.draw_text(f"期末成绩：{self.current_final_score}分", transcript_x + 50, transcript_y + y_offset + 2 * 40, (0, 0, 0))
        self.draw_text(f"评级：{self.current_final_grade}", transcript_x + 50, transcript_y + y_offset + 3 * 40, (0, 0, 0))
        self.draw_text(f"绩点：{self.current_final_gpa}", transcript_x + 50, transcript_y + y_offset + 4 * 40, (0, 0, 0))
        
        # 绘制奖学金信息
        if self.current_final_grade == "A":
            self.draw_text("恭喜获得奖学金100！", transcript_x + 50, transcript_y + y_offset + 5 * 40, (0, 150, 0))
        elif self.current_final_grade == "A-":
            self.draw_text("恭喜获得奖学金50！", transcript_x + 50, transcript_y + y_offset + 5 * 40, (0, 150, 0))
        
        # 绘制返回按钮
        back_rect = pygame.Rect(self.width // 2 - 50, transcript_y + transcript_height + 20, 100, 50)
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.draw_text("返回", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
    
    def _handle_final_exam(self, events):
        """处理期末成绩单事件"""
        # 定义返回按钮区域
        transcript_width = 400
        transcript_height = 300
        transcript_y = self.height // 2 - transcript_height // 2
        back_rect = pygame.Rect(self.width // 2 - 50, transcript_y + transcript_height + 20, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回主游戏
                    self.current_state = STATE_MAIN_GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 返回主游戏
                if back_rect.collidepoint(pos):
                    self.current_state = STATE_MAIN_GAME
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
