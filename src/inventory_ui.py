import pygame
import os

from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class InventoryUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = game.font
        self.large_font = game.large_font
        self.visible = False
        self.selected_slot = None
        self.show_detail = False
        self.detail_item = None
        
        self._load_images()
        self._setup_ui_elements()
    
    def _load_images(self):
        close_button_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'close_bag_button.png')
        self.close_button = None
        try:
            if os.path.exists(close_button_path):
                self.close_button = pygame.image.load(close_button_path).convert_alpha()
                self.close_button = pygame.transform.scale(self.close_button, (40, 40))
        except Exception as e:
            print(f"加载关闭按钮失败: {e}")
    
    def _setup_ui_elements(self):
        self.window_width = 580
        self.window_height = 450
        self.window_x = (SCREEN_WIDTH - self.window_width) // 2
        self.window_y = (SCREEN_HEIGHT - self.window_height) // 2
        
        self.slot_size = 64
        self.slot_padding = 8
        self.slot_offset_x = 40
        self.slot_offset_y = 60
        
        self.cols = 5
        self.rows = 4
        
        self.use_button_rect = pygame.Rect(
            self.window_x + self.window_width - 160,
            self.window_y + self.window_height - 60,
            120,
            40
        )
        
        self.close_button_rect = pygame.Rect(
            self.window_x + self.window_width - 50,
            self.window_y + 10,
            40,
            40
        )
        
        self.detail_window_rect = pygame.Rect(
            self.window_x + 40,
            self.window_y + self.window_height - 120,
            self.window_width - 200,
            100
        )
    
    def get_slot_rect(self, index):
        col = index % self.cols
        row = index // self.cols
        x = self.window_x + self.slot_offset_x + col * (self.slot_size + self.slot_padding)
        y = self.window_y + self.slot_offset_y + row * (self.slot_size + self.slot_padding)
        return pygame.Rect(x, y, self.slot_size, self.slot_size)
    
    def draw(self):
        if not self.visible:
            return
        
        self._draw_background()
        self._draw_title()
        self._draw_slots()
        self._draw_use_button()
        self._draw_close_button()
        if self.show_detail and self.detail_item:
            self._draw_detail_window()
    
    def _draw_background(self):
        pygame.draw.rect(self.screen, (200, 180, 140), 
                        (self.window_x, self.window_y, self.window_width, self.window_height))
        pygame.draw.rect(self.screen, (150, 100, 50), 
                        (self.window_x, self.window_y, self.window_width, self.window_height), 3)
        
        inner_x = self.window_x + 5
        inner_y = self.window_y + 5
        inner_width = self.window_width - 10
        inner_height = self.window_height - 10
        pygame.draw.rect(self.screen, (254, 247, 201), 
                        (inner_x, inner_y, inner_width, inner_height))
        pygame.draw.rect(self.screen, (150, 100, 50), 
                        (inner_x, inner_y, inner_width, inner_height), 2)
    
    def _draw_title(self):
        title_text = self.large_font.render("背包", True, (150, 100, 50))
        title_rect = title_text.get_rect(center=(self.window_x + self.window_width // 2, self.window_y + 30))
        self.screen.blit(title_text, title_rect)
        
        empty_slots = self.game.inventory.get_empty_slots()
        slot_text = self.font.render(f"容量: {20 - empty_slots}/20", True, (95, 58, 31))
        slot_rect = slot_text.get_rect(x=self.window_x + 20, y=self.window_y + 28)
        self.screen.blit(slot_text, slot_rect)
    
    def _draw_slots(self):
        slot_items = self.game.inventory.get_slot_items()
        
        for i in range(len(slot_items)):
            item, quantity = slot_items[i]
            slot_rect = self.get_slot_rect(i)
            
            if self.selected_slot == i:
                pygame.draw.rect(self.screen, (255, 215, 0), slot_rect)
                pygame.draw.rect(self.screen, (218, 165, 32), slot_rect, 2)
            else:
                pygame.draw.rect(self.screen, (220, 200, 180), slot_rect)
                pygame.draw.rect(self.screen, (150, 130, 110), slot_rect, 2)
            
            if item:
                icon_x = slot_rect.x + (self.slot_size - item.icon.get_width()) // 2
                icon_y = slot_rect.y + (self.slot_size - item.icon.get_height()) // 2
                self.screen.blit(item.icon, (icon_x, icon_y))
                
                if quantity > 1:
                    quantity_text = self.font.render(str(quantity), True, (95, 58, 31))
                    self.screen.blit(quantity_text, (slot_rect.x + self.slot_size - 20, slot_rect.y + self.slot_size - 20))
    
    def _draw_use_button(self):
        if self.selected_slot is not None:
            slot_items = self.game.inventory.get_slot_items()
            item, _ = slot_items[self.selected_slot]
            if item and item.can_use():
                pygame.draw.rect(self.screen, (60, 172, 100), self.use_button_rect)
                pygame.draw.rect(self.screen, (40, 120, 70), self.use_button_rect, 2)
                use_text = self.font.render("使用", True, (255, 255, 255))
                use_rect = use_text.get_rect(center=self.use_button_rect.center)
                self.screen.blit(use_text, use_rect)
    
    def _draw_close_button(self):
        if self.close_button:
            self.screen.blit(self.close_button, self.close_button_rect)
        else:
            pygame.draw.rect(self.screen, (180, 80, 80), self.close_button_rect)
            pygame.draw.rect(self.screen, (150, 50, 50), self.close_button_rect, 2)
            close_text = self.font.render("X", True, (255, 255, 255))
            close_rect = close_text.get_rect(center=self.close_button_rect.center)
            self.screen.blit(close_text, close_rect)
    
    def _draw_detail_window(self):
        pygame.draw.rect(self.screen, (240, 220, 200), self.detail_window_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), self.detail_window_rect, 2)
        
        item = self.detail_item
        if not item:
            return
        
        content_x = self.detail_window_rect.x + 15
        content_y = self.detail_window_rect.y + 10
        
        name_text = self.large_font.render(item.name, True, (150, 100, 50))
        self.screen.blit(name_text, (content_x, content_y))
        
        desc_text = self.font.render(item.description, True, (95, 58, 31))
        self.screen.blit(desc_text, (content_x, content_y + 30))
        
        if item.effects:
            effects_str = "效果: " + ", ".join([f"{self._get_attr_name(k)} {v:+}" for k, v in item.effects.items()])
            effects_text = self.font.render(effects_str, True, (60, 172, 100))
            self.screen.blit(effects_text, (content_x, content_y + 60))
        
        if not item.can_use():
            tip_text = self.font.render("(不可使用)", True, (150, 100, 100))
            self.screen.blit(tip_text, (self.detail_window_rect.right - 100, content_y))
    
    def _get_attr_name(self, attr):
        names = {
            'knowledge': '学识',
            'charm': '魅力',
            'physical': '体能',
            'living_expenses': '金钱',
            'action_points': '行动点',
            'mood': '心情',
            'health': '健康',
            'skill': '技能',
            'social': '人脉',
            'reputation': '声望'
        }
        return names.get(attr, attr)
    
    def handle_events(self, events):
        if not self.visible:
            return None
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if self.close_button_rect.collidepoint(pos):
                    self.hide()
                    return 'CLOSE'
                
                if self.use_button_rect.collidepoint(pos):
                    if self.selected_slot is not None:
                        slot_items = self.game.inventory.get_slot_items()
                        item, _ = slot_items[self.selected_slot]
                        if item and item.can_use():
                            current_year = self.game.time_system.get_year() if hasattr(self.game, 'time_system') else None
                            success, msg = self.game.inventory.use_item(item.item_id, self.game.player, current_year)
                            self.game.message = msg
                            self.game.message_timer = 90
                            self.show_detail = False
                            self.detail_item = None
                            if not success:
                                self.selected_slot = None
                            return 'USE'
                
                for i in range(20):
                    slot_rect = self.get_slot_rect(i)
                    if slot_rect.collidepoint(pos):
                        slot_items = self.game.inventory.get_slot_items()
                        item, _ = slot_items[i]
                        
                        if self.selected_slot == i:
                            self.show_detail = not self.show_detail
                            self.detail_item = item
                        else:
                            self.selected_slot = i
                            self.show_detail = True
                            self.detail_item = item
                        return 'SELECT'
                
                if self.show_detail and not self.detail_window_rect.collidepoint(pos):
                    self.show_detail = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.hide()
                    return 'CLOSE'
                elif event.key == pygame.K_i:
                    self.hide()
                    return 'CLOSE'
        
        return None
    
    def show(self):
        self.visible = True
        self.selected_slot = None
        self.show_detail = False
        self.detail_item = None
    
    def hide(self):
        self.visible = False
        self.selected_slot = None
        self.show_detail = False
        self.detail_item = None
    
    def is_visible(self):
        return self.visible