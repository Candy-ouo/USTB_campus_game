import pygame
import os

class PixelPopup:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = game.font
        self.large_font = game.large_font
        
        self.colors = {
            'bg': (220, 180, 140),
            'border': (150, 100, 50),
            'button': (254, 247, 201),
            'button_hover': (255, 215, 0),
            'button_pressed': (218, 165, 32),
            'text': (150, 100, 50),
            'title': (150, 100, 50),
            'shadow': (0, 0, 0),
            'panel': (245, 235, 220)
        }

    def draw_text_with_shadow(self, text, x, y, color, surface, font=None):
        text_font = font if font else self.font
        shadow_surf = text_font.render(text, True, self.colors['shadow'])
        text_surf = text_font.render(text, True, color)
        surface.blit(shadow_surf, (x + 1, y + 1))
        surface.blit(text_surf, (x, y))

    def show_event_popup(self, event) -> int:
        popup_width = 560
        popup_height = 340
        padding = 25
        
        screen_width, screen_height = self.screen.get_size()
        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2
        
        button_height = 45
        button_padding = 15
        button_y_start = y + popup_height - button_height - padding - 10
        
        buttons = []
        button_width = (popup_width - padding * (len(event.options) + 1)) // len(event.options)
        
        for i, option in enumerate(event.options):
            btn_x = x + padding + i * (button_width + padding)
            buttons.append({
                'rect': pygame.Rect(btn_x, button_y_start, button_width, button_height),
                'text': option.text,
                'effects': option.effects,
                'index': i
            })
        
        selected_button = None
        result_index = None
        
        while result_index is None:
            for event_pygame in pygame.event.get():
                if event_pygame.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event_pygame.type == pygame.MOUSEMOTION:
                    mouse_pos = event_pygame.pos
                    selected_button = None
                    for btn in buttons:
                        if btn['rect'].collidepoint(mouse_pos):
                            selected_button = btn['index']
                            break
                
                if event_pygame.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event_pygame.pos
                    for btn in buttons:
                        if btn['rect'].collidepoint(mouse_pos):
                            result_index = btn['index']
                            break
            
            self.screen.fill((15, 15, 20))
            
            pygame.draw.rect(self.screen, self.colors['border'], (x - 4, y - 4, popup_width + 8, popup_height + 8), 3)
            pygame.draw.rect(self.screen, self.colors['bg'], (x, y, popup_width, popup_height))
            
            pygame.draw.line(self.screen, self.colors['border'], (x, y + 50), (x + popup_width, y + 50), 2)
            
            title_y = y + 15
            title_surf = self.large_font.render(event.title, True, self.colors['title'])
            title_x = x + (popup_width - title_surf.get_width()) // 2
            self.screen.blit(title_surf, (title_x, title_y))
            
            desc_lines = self._wrap_text(event.description, popup_width - padding * 2)
            desc_y = y + 70
            for line in desc_lines:
                self.draw_text_with_shadow(line, x + padding, desc_y, self.colors['text'], self.screen)
                desc_y += 24
            
            for i, btn in enumerate(buttons):
                if selected_button == i:
                    pygame.draw.rect(self.screen, self.colors['button_hover'], btn['rect'])
                    pygame.draw.rect(self.screen, self.colors['border'], btn['rect'], 2)
                else:
                    pygame.draw.rect(self.screen, self.colors['button'], btn['rect'])
                    pygame.draw.rect(self.screen, self.colors['border'], btn['rect'], 2)
                
                btn_text = self.font.render(btn['text'], True, self.colors['text'])
                btn_text_x = btn['rect'].x + (btn['rect'].width - btn_text.get_width()) // 2
                btn_text_y = btn['rect'].y + (btn['rect'].height - btn_text.get_height()) // 2
                self.screen.blit(btn_text, (btn_text_x, btn_text_y))
            
            pygame.display.flip()
        
        return result_index

    def _wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            test_surf = self.font.render(test_line, True, self.colors['text'])
            
            if test_surf.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def show_attribute_change(self, effects):
        popup_width = 360
        popup_height = 200
        
        screen_width, screen_height = self.screen.get_size()
        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2
        
        button_rect = pygame.Rect(x + 80, y + 140, 200, 40)
        selected = False
        
        while True:
            for event_pygame in pygame.event.get():
                if event_pygame.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event_pygame.type == pygame.MOUSEMOTION:
                    selected = button_rect.collidepoint(event_pygame.pos)
                if event_pygame.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event_pygame.pos):
                        return
            
            self.screen.fill((15, 15, 20))
            
            pygame.draw.rect(self.screen, self.colors['border'], (x - 4, y - 4, popup_width + 8, popup_height + 8), 3)
            pygame.draw.rect(self.screen, self.colors['bg'], (x, y, popup_width, popup_height))
            
            title_text = self.large_font.render("属性变化", True, self.colors['title'])
            title_x = x + (popup_width - title_text.get_width()) // 2
            self.screen.blit(title_text, (title_x, y + 15))
            
            attr_names = {
                'living_expenses': '生活费',
                'action_points': '行动力',
                'mood': '心情',
                'health': '健康值',
                'knowledge': '学识',
                'physical': '体能',
                'charm': '魅力',
                'social': '人脉'
            }
            
            y_offset = 55
            for attr, value in effects.items():
                if value != 0:
                    sign = '+' if value > 0 else ''
                    text = f"{attr_names.get(attr, attr)}: {sign}{value}"
                    color = (0, 150, 0) if value > 0 else (150, 0, 0)
                    self.draw_text_with_shadow(text, x + 30, y + y_offset, color, self.screen)
                    y_offset += 25
            
            if selected:
                pygame.draw.rect(self.screen, self.colors['button_hover'], button_rect)
                pygame.draw.rect(self.screen, self.colors['border'], button_rect, 2)
            else:
                pygame.draw.rect(self.screen, self.colors['button'], button_rect)
                pygame.draw.rect(self.screen, self.colors['border'], button_rect, 2)
            
            btn_text = self.font.render("继续游戏", True, self.colors['text'])
            btn_text_x = button_rect.x + (button_rect.width - btn_text.get_width()) // 2
            btn_text_y = button_rect.y + (button_rect.height - btn_text.get_height()) // 2
            self.screen.blit(btn_text, (btn_text_x, btn_text_y))
            
            pygame.display.flip()