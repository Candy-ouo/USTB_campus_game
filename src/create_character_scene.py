
import pygame
import os
import sys
# 禁用libpng警告
class DevNull:
    def write(self, *args): pass
    def flush(self): pass

# 重定向stderr以忽略libpng警告
old_stderr = sys.stderr
sys.stderr = DevNull()

from typing import Optional
from src.character import Character, COLLEGE_MAJORS

# 恢复stderr
sys.stderr = old_stderr


class CreateCharacterScene:
    
    
    # 颜色定义
    COLOR_TEXT = (85, 45, 17)     # 文字颜色
    COLOR_HIGHLIGHT = (178, 34, 34)  # 高亮颜色
    COLOR_ACTIVE = (255, 165, 0)     # 激活颜色
    
    def __init__(self, screen: pygame.Surface, font, large_font):
        self.screen = screen
        self.font = font
        self.large_font = large_font
        # 动态获取窗口大小
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 角色数据
        self.name = ""
        self.gender = "男"
        self.character_height = ""
        self.weight = ""
        self.birth_month = 1
        self.birth_day = 1
        self.college_index = 0
        self.college_list = list(COLLEGE_MAJORS.keys())
        self.major = Character.get_major_by_college(self.college_list[self.college_index])
        
        # 激活的输入框/选项
        self.active_field = "name"  # name, gender, height, weight, birthday_month, birthday_day, college
        
        # 光标闪烁
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # 毫秒
        
        # 字段顺序，用于方向键导航
        self.fields = ["name", "gender", "height", "weight", "birthday_month", "birthday_day", "college"]
        self.current_field_index = 0
        
        # 加载图片素材
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_dir = os.path.join(base_dir, "image")
        
        # 加载背景图片
        self.start_background = pygame.image.load(os.path.join(image_dir, "start_background.png"))
        # 加载角色编辑框图片
        self.create_box = pygame.image.load(os.path.join(image_dir, "create_box.png"))

        # 加载确认按钮图片
        self.certain_button = pygame.image.load(os.path.join(image_dir, "certain_button.png"))
        # 加载新的输入框图片
        self.name_major_box = pygame.image.load(os.path.join(image_dir, "name_major_box.png"))
        self.origin_box = pygame.image.load(os.path.join(image_dir, "origin_box.png"))
        # 加载箭头图片
        self.left_arrow = pygame.image.load(os.path.join(image_dir, "left_arrow.png"))
        self.right_arrow = pygame.image.load(os.path.join(image_dir, "right_arrow.png"))
        # 加载性别图标
        self.male_icon = pygame.image.load(os.path.join(image_dir, "male_icon.png"))
        self.female_icon = pygame.image.load(os.path.join(image_dir, "female_icon.png"))
    
    def handle_events(self, events: list) -> Optional[Character]:
        """处理事件，返回 Character 表示创建完成"""
        for event in events:
            if event.type == pygame.QUIT:
                return None
            
            elif event.type == pygame.KEYDOWN:
                # ESC 退出
                if event.key == pygame.K_ESCAPE:
                    return None
                
                # Enter 确认
                elif event.key == pygame.K_RETURN:
                    # 检查姓名是否为空
                    if not self.name:
                        self.name = "玩家"
                    return self._create_character()
                
                # 方向键导航
                elif event.key == pygame.K_TAB:
                    # 切换到下一个字段
                    self.current_field_index = (self.current_field_index + 1) % len(self.fields)
                    self.active_field = self.fields[self.current_field_index]
                
                # 方向键调整数值
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self._handle_navigation(event.key)
                
                # 退格键
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_field == "name":
                        self.name = self.name[:-1]
                    elif self.active_field == "height":
                        # 退格删除最后一位数字
                        if isinstance(self.character_height, str):
                            self.character_height = self.character_height[:-1]
                        else:
                            height_str = str(self.character_height)
                            if len(height_str) > 1:
                                self.character_height = height_str[:-1]
                            else:
                                self.character_height = ""
                    elif self.active_field == "weight":
                        # 退格删除最后一位数字
                        if isinstance(self.weight, str):
                            self.weight = self.weight[:-1]
                        else:
                            weight_str = str(self.weight)
                            if len(weight_str) > 1:
                                self.weight = weight_str[:-1]
                            else:
                                self.weight = ""
                
                # 文本输入（处理中文）
                elif event.unicode:
                    if self.active_field == "name":
                        if len(self.name) < 10:
                            # 直接添加 unicode 字符，包括中文
                            self.name += event.unicode
                    elif self.active_field == "height" and event.unicode.isdigit():
                        # 只允许输入数字，类似于姓名的输入模式
                        if isinstance(self.character_height, str):
                            self.character_height += event.unicode
                        else:
                            self.character_height = str(self.character_height) + event.unicode
                    elif self.active_field == "weight" and event.unicode.isdigit():
                        # 只允许输入数字，类似于姓名的输入模式
                        if isinstance(self.weight, str):
                            self.weight += event.unicode
                        else:
                            self.weight = str(self.weight) + event.unicode
            
            # 文本输入事件（处理中文输入）
            elif event.type == pygame.TEXTINPUT:
                if self.active_field == "name":
                    if len(self.name) < 10:
                        # 直接添加文本，包括中文
                        self.name += event.text
                elif self.active_field == "height" and event.text.isdigit():
                    # 只允许输入数字，类似于姓名的输入模式
                    if isinstance(self.character_height, str):
                        self.character_height += event.text
                    else:
                        self.character_height = str(self.character_height) + event.text
                elif self.active_field == "weight" and event.text.isdigit():
                    # 只允许输入数字，类似于姓名的输入模式
                    if isinstance(self.weight, str):
                        self.weight += event.text
                    else:
                        self.weight = str(self.weight) + event.text
            
            # 鼠标事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                result = self._handle_mouse_click(pos)
                if result is not None:
                    return result
        
        return None
    
    def _handle_navigation(self, key):
        """处理方向键导航"""
        if self.active_field == "gender":
            if key in (pygame.K_UP, pygame.K_DOWN):
                self.gender = "女" if self.gender == "男" else "男"
        
        elif self.active_field == "height":
            if key == pygame.K_UP and self.character_height < 210:
                self.character_height += 1
            elif key == pygame.K_DOWN and self.character_height > 140:
                self.character_height -= 1
            elif key == pygame.K_LEFT and self.character_height > 140:
                self.character_height -= 1
            elif key == pygame.K_RIGHT and self.character_height < 210:
                self.character_height += 1
        
        elif self.active_field == "weight":
            if key == pygame.K_UP and self.weight < 150:
                self.weight += 1
            elif key == pygame.K_DOWN and self.weight > 40:
                self.weight -= 1
            elif key == pygame.K_LEFT and self.weight > 40:
                self.weight -= 1
            elif key == pygame.K_RIGHT and self.weight < 150:
                self.weight += 1
        
        elif self.active_field == "birthday_month":
            if key == pygame.K_UP and self.birth_month < 12:
                self.birth_month += 1
                # 调整日期
                max_day = self._get_max_day(self.birth_month)
                if self.birth_day > max_day:
                    self.birth_day = max_day
            elif key == pygame.K_DOWN and self.birth_month > 1:
                self.birth_month -= 1
                # 调整日期
                max_day = self._get_max_day(self.birth_month)
                if self.birth_day > max_day:
                    self.birth_day = max_day
        
        elif self.active_field == "birthday_day":
            max_day = self._get_max_day(self.birth_month)
            if key == pygame.K_UP and self.birth_day < max_day:
                self.birth_day += 1
            elif key == pygame.K_DOWN and self.birth_day > 1:
                self.birth_day -= 1
        
        elif self.active_field == "college":
            if key == pygame.K_UP and self.college_index > 0:
                self.college_index -= 1
                self.major = Character.get_major_by_college(self.college_list[self.college_index])
            elif key == pygame.K_DOWN and self.college_index < len(self.college_list) - 1:
                self.college_index += 1
                self.major = Character.get_major_by_college(self.college_list[self.college_index])
    
    def _handle_mouse_click(self, pos):
        """处理鼠标点击"""
        # 实时更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 计算编辑框位置（与draw方法一致）
        box_width = self.create_box.get_width()
        box_height = self.create_box.get_height()
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2
        
        # 右侧属性编辑区（在编辑框内）
        preview_width = 300
        editor_width = box_width - preview_width - 100
        editor_x = box_x + preview_width + 50
        editor_y = box_y + 50
        editor_height = box_height - 100
        editor_rect = pygame.Rect(editor_x, editor_y, editor_width, editor_height)
        
        # 偏右侧起始位置（与draw方法一致）
        right_align_x = editor_x + 125
        base_spacing = 95  # 与draw方法一致
        
        # 姓名和性别一行
        y_offset = editor_y + 150  # 与draw方法一致
        
        # 姓名输入框
        name_box_width = self.name_major_box.get_width()
        name_box_height = self.name_major_box.get_height()
        name_x = right_align_x
        name_y = y_offset - name_box_height // 2
        name_rect = pygame.Rect(name_x, name_y, name_box_width, name_box_height)
        if name_rect.collidepoint(pos):
            self.active_field = "name"
            self.current_field_index = self.fields.index("name")
        
        # 性别图标（与draw方法一致）
        gender_icon_size = 50
        male_x = name_x + name_box_width + 120
        female_x = male_x + gender_icon_size + 20
        gender_y = y_offset - gender_icon_size // 2
        
        male_rect = pygame.Rect(male_x, gender_y, gender_icon_size, gender_icon_size)
        female_rect = pygame.Rect(female_x, gender_y, gender_icon_size, gender_icon_size)
        
        if male_rect.collidepoint(pos):
            self.gender = "男"
        elif female_rect.collidepoint(pos):
            self.gender = "女"
        
        # 身高和体重一行
        y_offset += base_spacing
        
        # 身高输入框
        origin_box_width = self.origin_box.get_width()
        origin_box_height = self.origin_box.get_height()
        height_x = right_align_x
        height_y = y_offset - origin_box_height // 2
        height_rect = pygame.Rect(height_x, height_y, origin_box_width, origin_box_height)
        if height_rect.collidepoint(pos):
            self.active_field = "height"
            self.current_field_index = self.fields.index("height")
            # 清空现有值，让用户直接输入
            self.character_height = ""
        
        # 体重输入框（与draw方法一致）
        weight_x = height_x + origin_box_width + 180
        weight_y = y_offset - origin_box_height // 2 + 10
        weight_rect = pygame.Rect(weight_x, weight_y, origin_box_width, origin_box_height)
        if weight_rect.collidepoint(pos):
            self.active_field = "weight"
            self.current_field_index = self.fields.index("weight")
            # 清空现有值，让用户直接输入
            self.weight = ""
        
        # 生日一行
        y_offset += base_spacing
        
        # 月份输入框
        month_x = right_align_x
        month_y = y_offset - origin_box_height // 2 + 10
        month_rect = pygame.Rect(month_x, month_y, origin_box_width, origin_box_height)
        if month_rect.collidepoint(pos):
            self.active_field = "birthday_month"
            self.current_field_index = self.fields.index("birthday_month")
        
        # 日期输入框
        day_x = month_x + origin_box_width + 30
        day_y = y_offset - origin_box_height // 2 + 10
        day_rect = pygame.Rect(day_x, day_y, origin_box_width, origin_box_height)
        if day_rect.collidepoint(pos):
            self.active_field = "birthday_day"
            self.current_field_index = self.fields.index("birthday_day")
        
        # 学院一行
        y_offset += base_spacing
        
        # 学院输入框（与draw方法一致）
        college_x = right_align_x + 80
        college_y = y_offset - name_box_height // 2 + 10
        college_rect = pygame.Rect(college_x, college_y, name_box_width, name_box_height)
        if college_rect.collidepoint(pos):
            self.active_field = "college"
            self.current_field_index = self.fields.index("college")
        
        # 学院左右箭头（与draw方法一致）
        arrow_size = 30
        left_arrow_x = college_x - arrow_size - 10
        right_arrow_x = college_x + name_box_width + 10
        arrow_y = y_offset - arrow_size // 2 + 10
        
        left_arrow_rect = pygame.Rect(left_arrow_x, arrow_y, arrow_size, arrow_size)
        right_arrow_rect = pygame.Rect(right_arrow_x, arrow_y, arrow_size, arrow_size)
        
        if left_arrow_rect.collidepoint(pos):
            # 切换到上一个学院
            if self.college_index > 0:
                self.college_index -= 1
                self.major = Character.get_major_by_college(self.college_list[self.college_index])
        elif right_arrow_rect.collidepoint(pos):
            # 切换到下一个学院
            if self.college_index < len(self.college_list) - 1:
                self.college_index += 1
                self.major = Character.get_major_by_college(self.college_list[self.college_index])
        
        # 确认按钮 - 使用draw方法中保存的按钮矩形
        if hasattr(self, 'confirm_rect') and self.confirm_rect.collidepoint(pos):
            if not self.name:
                self.name = "玩家"
            return self._create_character()
    
    def _get_max_day(self, month: int) -> int:
        """获取月份的最大天数"""
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif month in (4, 6, 9, 11):
            return 30
        else:  # 2月
            return 28
    
    def _create_character(self) -> Character:
        """创建角色对象"""
        college = self.college_list[self.college_index]
        birthday = f"{self.birth_month:02d}-{self.birth_day:02d}"
        
        # 处理身高体重为空的情况
        height = self.character_height
        if not height:
            height = 170
        else:
            try:
                height = int(height)
            except ValueError:
                height = 170
        
        weight = self.weight
        if not weight:
            weight = 60
        else:
            try:
                weight = int(weight)
            except ValueError:
                weight = 60
        
        character = Character(
            name=self.name,
            gender=self.gender,
            height=height,
            weight=weight,
            birthday=birthday,
            college=college,
            major=self.major
        )
        
        # 打印角色数据
        print("角色创建完成！")
        print(f"姓名: {character.name}")
        print(f"性别: {character.gender}")
        print(f"身高: {character.height} cm")
        print(f"体重: {character.weight} kg")
        print(f"生日: {character.birthday}")
        print(f"学院: {character.college}")
        print(f"专业: {character.major}")
        
        return character
    
    def update(self):
        """更新状态"""
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer > self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time
    
    def draw(self):
        """绘制界面"""
        # 动态更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 绘制背景图片
        scaled_bg = pygame.transform.scale(self.start_background, (self.screen_width, self.screen_height))
        self.screen.blit(scaled_bg, (0, 0))
        
        # 使用原始编辑框大小
        box_width = self.create_box.get_width()
        box_height = self.create_box.get_height()
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2
        self.create_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        # 绘制角色编辑框（不拉伸）
        self.screen.blit(self.create_box, self.create_box_rect)
        
        # 左侧角色预览区（在编辑框内）
        preview_width = 300
        preview_rect = pygame.Rect(box_x + 50, box_y + 50, preview_width, box_height - 100)
        self._draw_character_preview(preview_rect)
        
        # 右侧属性编辑区（在编辑框内）
        editor_width = box_width - preview_width - 100
        editor_rect = pygame.Rect(box_x + preview_width + 50, box_y + 50, editor_width, box_height - 100)
        self._draw_attribute_editor(editor_rect)
        
        # 绘制确认按钮（在编辑框的靠右下边位置）
        button_width = self.certain_button.get_width()
        button_height = self.certain_button.get_height()
        button_x = box_x + box_width - button_width - 60
        button_y = box_y + box_height - button_height - 40
        self.confirm_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        # 不拉伸确认按钮
        self.screen.blit(self.certain_button, self.confirm_rect)
    
    def _draw_character_preview(self, rect):
        """绘制角色预览区"""
        # 加载角色立绘
        try:
            # 使用绝对路径加载图片
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if self.gender == "男":
                character_image = pygame.image.load(os.path.join(base_dir, "image", "boy.png"))
            else:
                character_image = pygame.image.load(os.path.join(base_dir, "image", "girl.png"))
            
            # 调整立绘大小，保持比例
            max_height = min(400, rect.height - 50)
            scale_factor = max_height / character_image.get_height()
            new_width = int(character_image.get_width() * scale_factor)
            character_image = pygame.transform.scale(character_image, (new_width, max_height))
            
            # 计算立绘位置（居中）
            character_x = rect.x + (rect.width - new_width) // 2 - 30
            character_y = rect.y + (rect.height - max_height) // 2 + 10
            
            # 绘制立绘
            self.screen.blit(character_image, (character_x, character_y))
        except Exception as e:
            # 如果图片加载失败，显示错误信息
            self._draw_text("立绘加载失败", rect.x + rect.width // 2, rect.y + 150, font=self.font, color=(255, 0, 0))
            print(f"立绘加载失败: {e}")
    
    def _draw_attribute_editor(self, rect):
        """绘制属性编辑区"""
        # 偏右侧起始位置
        right_align_x = rect.x + 125
        
        # 计算可用高度和元素间距
        available_height = rect.height - 100  # 顶部60 + 底部40
        base_spacing = 95  # 增加间距
        
        # 姓名和性别一行
        y_offset = rect.y + 150
        
        # 姓名输入框
        name_box_width = self.name_major_box.get_width()
        name_box_height = self.name_major_box.get_height()
        name_x = right_align_x
        name_y = y_offset - name_box_height // 2
        name_rect = pygame.Rect(name_x, name_y, name_box_width, name_box_height)
        self.screen.blit(self.name_major_box, name_rect)
        
        # 姓名文字
        display_name = self.name
        if self.active_field == "name" and self.cursor_visible:
            display_name += "|"
        text_surface = self.font.render(display_name, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = name_rect.x + (name_rect.width - text_width) // 2
        text_y = name_rect.y + (name_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 性别图标
        gender_icon_size = 50
        male_icon = pygame.transform.scale(self.male_icon, (gender_icon_size, gender_icon_size))
        female_icon = pygame.transform.scale(self.female_icon, (gender_icon_size, gender_icon_size))
        
        male_x = name_x + name_box_width + 120
        female_x = male_x + gender_icon_size + 20
        gender_y = y_offset - gender_icon_size // 2
        
        male_rect = pygame.Rect(male_x, gender_y, gender_icon_size, gender_icon_size)
        female_rect = pygame.Rect(female_x, gender_y, gender_icon_size, gender_icon_size)
        
        # 绘制性别图标
        self.screen.blit(male_icon, male_rect)
        self.screen.blit(female_icon, female_rect)
        
        # 选中状态
        if self.gender == "男":
            pygame.draw.rect(self.screen, (255, 215, 0), male_rect, 3)
        else:
            pygame.draw.rect(self.screen, (255, 215, 0), female_rect, 3)
        
        # 身高和体重一行
        y_offset += base_spacing
        
        # 身高输入框 
        origin_box_width = self.origin_box.get_width()
        origin_box_height = self.origin_box.get_height()
        height_x = right_align_x
        height_y = y_offset - origin_box_height // 2
        height_rect = pygame.Rect(height_x, height_y, origin_box_width, origin_box_height)
        self.screen.blit(self.origin_box, height_rect)
        
        # 身高文字
        height_text = str(self.character_height) if self.character_height else ""
        if self.active_field == "height" and self.cursor_visible:
            height_text += "|"
        text_surface = self.font.render(height_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = height_rect.x + (height_rect.width - text_width) // 2
        text_y = height_rect.y + (height_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 体重输入框
        weight_x = height_x + origin_box_width + 180
        weight_y = y_offset - origin_box_height // 2 + 10
        weight_rect = pygame.Rect(weight_x, weight_y, origin_box_width, origin_box_height)
        self.screen.blit(self.origin_box, weight_rect)
        
        # 体重文字
        weight_text = str(self.weight) if self.weight else ""
        if self.active_field == "weight" and self.cursor_visible:
            weight_text += "|"
        text_surface = self.font.render(weight_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = weight_rect.x + (weight_rect.width - text_width) // 2
        text_y = weight_rect.y + (weight_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 生日一行
        y_offset += base_spacing
        
        # 月份输入框
        month_x = right_align_x
        month_y = y_offset - origin_box_height // 2 + 10
        month_rect = pygame.Rect(month_x, month_y, origin_box_width, origin_box_height)
        self.screen.blit(self.origin_box, month_rect)
        
        # 月份文字
        month_text = f"{self.birth_month:02d}"
        text_surface = self.font.render(month_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = month_rect.x + (month_rect.width - text_width) // 2
        text_y = month_rect.y + (month_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 连接符
        self._draw_text("-", month_x + origin_box_width + 10, y_offset + 10, font=self.font)
        
        # 日期输入框
        day_x = month_x + origin_box_width + 30
        day_y = y_offset - origin_box_height // 2 + 10
        day_rect = pygame.Rect(day_x, day_y, origin_box_width, origin_box_height)
        self.screen.blit(self.origin_box, day_rect)
        
        # 日期文字
        day_text = f"{self.birth_day:02d}"
        text_surface = self.font.render(day_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = day_rect.x + (day_rect.width - text_width) // 2
        text_y = day_rect.y + (day_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 学院一行
        y_offset += base_spacing
        
        # 学院输入框
        college_x = right_align_x + 80
        college_y = y_offset - name_box_height // 2 + 10
        college_rect = pygame.Rect(college_x, college_y, name_box_width, name_box_height)
        self.screen.blit(self.name_major_box, college_rect)
        
        # 学院文字
        college_text = self.college_list[self.college_index]
        text_surface = self.font.render(college_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = college_rect.x + (college_rect.width - text_width) // 2
        text_y = college_rect.y + (college_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 左右箭头
        arrow_size = 30
        left_arrow = pygame.transform.scale(self.left_arrow, (arrow_size, arrow_size))
        right_arrow = pygame.transform.scale(self.right_arrow, (arrow_size, arrow_size))
        
        left_arrow_x = college_x - arrow_size - 10
        right_arrow_x = college_x + name_box_width + 10
        arrow_y = y_offset - arrow_size // 2 + 10
        
        self.left_arrow_rect = pygame.Rect(left_arrow_x, arrow_y, arrow_size, arrow_size)
        self.right_arrow_rect = pygame.Rect(right_arrow_x, arrow_y, arrow_size, arrow_size)
        
        self.screen.blit(left_arrow, self.left_arrow_rect)
        self.screen.blit(right_arrow, self.right_arrow_rect)
    

    
    def _draw_text(self, text, x, y, color=None, left=False, font=None):
        """绘制文字"""
        if color is None:
            color = self.COLOR_TEXT
        if font is None:
            font = self.font
        surface = font.render(text, True, color)
        if left:
            rect = surface.get_rect(topleft=(x, y - surface.get_height() // 2))
        else:
            rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)
