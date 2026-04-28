import pygame
import os
import json
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.config import SAVE_FILE


class SaveSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        # 确保存档文件保存在USTB_campus_game文件夹下的save文件夹中
        game_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.save_dir = os.path.join(game_root, 'save')
        self.save_file = os.path.join(self.save_dir, 'savegame.json')
        self.max_saves = 5

    def save_game(self, game, is_new_game=False, save_file_path=None):
        try:
            save_data = {
                'character': self._get_character_data(game),
                'player': game.player.to_dict(),
                'time_system': game.time_system.to_dict(),
                'game_state': {
                    'current_state': game.current_state,
                    'has_eaten': game.has_eaten,
                    'has_studied': game.has_studied,
                    'has_exercised': game.has_exercised,
                    'has_played_games': game.has_played_games,
                    'has_read_book': game.has_read_book,
                    'supermarket_purchases': game.supermarket_purchases,
                    'has_rested': game.has_rested,
                    'schedule_selected': game.schedule_selected,
                    'has_scheduled': game.has_scheduled,
                    'schedule_scroll_offsets': game.schedule_scroll_offsets,
                    'course_study_counts': game.course_study_counts,
                    'final_scores': game.final_scores,
                    'final_gpas': game.final_gpas,
                    'current_final_score': game.current_final_score,
                    'current_final_grade': game.current_final_grade,
                    'current_final_gpa': game.current_final_gpa,
                    'current_need_makeup': game.current_need_makeup,
                    'current_ending': game.current_ending
                }
            }
            os.makedirs(self.save_dir, exist_ok=True)
            
            if save_file_path:
                # 读档后修改旧存档
                with open(save_file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                return True, "游戏已保存！"
            elif is_new_game:
                # 新游戏创建新存档
                # 获取所有存档文件（排除savegame.json）
                save_files = [f for f in os.listdir(self.save_dir) if f.endswith('.json') and f != 'savegame.json']
                print(f"Debug: 存档文件列表 = {save_files}")
                print(f"Debug: 存档数量 = {len(save_files)}")
                print(f"Debug: 最大存档数量 = {self.max_saves}")
                
                # 如果存档数量达到上限，删除最旧的存档
                if len(save_files) >= self.max_saves:
                    # 获取每个存档的修改时间
                    save_files_with_time = []
                    for file_name in save_files:
                        file_path = os.path.join(self.save_dir, file_name)
                        mtime = os.path.getmtime(file_path)
                        save_files_with_time.append((file_path, mtime))
                    
                    # 按修改时间排序，删除最旧的
                    save_files_with_time.sort(key=lambda x: x[1])
                    oldest_save = save_files_with_time[0][0]
                    os.remove(oldest_save)
                
                # 创建新存档
                timestamp = int(time.time())
                new_save_path = os.path.join(self.save_dir, f'save_{timestamp}.json')
                with open(new_save_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                # 返回新创建的存档路径
                return True, "游戏已保存！", new_save_path
            else:
                # 常规保存（覆盖默认存档）
                with open(self.save_file, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                return True, "游戏已保存！"
        except Exception as e:
            return False, f"保存失败: {str(e)}"

    def load_game(self, game, file_path=None):
        try:
            load_path = file_path if file_path else self.save_file
            if not os.path.exists(load_path):
                return False, "没有找到存档！"

            with open(load_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            if 'character' in save_data:
                from src.character import Character
                game.character = Character.from_dict(save_data['character'])
                # 先恢复角色数据到玩家
                self._restore_character_to_player(game)

            if 'player' in save_data:
                # 再用玩家数据覆盖，确保获取游戏过程中的实际状态
                game.player.from_dict(save_data['player'])
            if 'time_system' in save_data:
                game.time_system.from_dict(save_data['time_system'])
                # 检查游戏是否已结束
                if game.time_system.is_ended():
                    # 游戏已结束，直接进入结局界面
                    game.handle_game_end()
                else:
                    # 更新UIHUD的时间信息
                    year = game.time_system.get_year()
                    month = game.time_system.get_month()
                    week = game.time_system.get_week_in_month()
                    game.ui_hud.update_time(year, month, week)
            if 'game_state' in save_data:
                gs = save_data['game_state']
                game.current_state = gs.get('current_state', 'MAIN_GAME')
                game.has_eaten = gs.get('has_eaten', False)
                game.has_studied = gs.get('has_studied', False)
                game.has_exercised = gs.get('has_exercised', False)
                game.has_played_games = gs.get('has_played_games', False)
                game.has_read_book = gs.get('has_read_book', False)
                game.supermarket_purchases = gs.get('supermarket_purchases', 0)
                game.has_rested = gs.get('has_rested', False)
                game.schedule_selected = gs.get('schedule_selected', [])
                game.has_scheduled = gs.get('has_scheduled', False)
                game.schedule_scroll_offsets = gs.get('schedule_scroll_offsets', [0, 0, 0])
                game.course_study_counts = gs.get('course_study_counts', {})
                game.final_scores = gs.get('final_scores', [])
                game.final_gpas = gs.get('final_gpas', [])
                game.current_final_score = gs.get('current_final_score', 0)
                game.current_final_grade = gs.get('current_final_grade', '')
                game.current_final_gpa = gs.get('current_final_gpa', 0.0)
                game.current_need_makeup = gs.get('current_need_makeup', False)
                game.current_ending = gs.get('current_ending', None)

            return True, "游戏已加载！"
        except Exception as e:
            return False, f"加载失败: {str(e)}"

    def load_character_from_save(self):
        try:
            if not os.path.exists(self.save_file):
                return None

            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            if 'character' in save_data:
                from src.character import Character
                return Character.from_dict(save_data['character'])
            return None
        except:
            return None

    def has_save_file(self):
        return os.path.exists(self.save_file)

    def delete_save(self):
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                return True
            return False
        except:
            return False

    def _get_character_data(self, game):
        if game.character:
            return game.character.to_dict()
        elif game.player:
            from src.character import Character
            char = Character()
            char.knowledge = game.player.knowledge
            char.knowledge_level = game.player.knowledge_level
            char.charm = game.player.charm
            char.charm_level = game.player.charm_level
            char.physical = game.player.physical
            char.physical_level = game.player.physical_level
            char.living_expenses = game.player.living_expenses
            char.action_points = game.player.action_points
            char.mood = game.player.mood
            char.health = game.player.health
            char.skill = game.player.skill
            char.social = game.player.social
            char.reputation = game.player.reputation
            char.theory_experiment = game.player.theory_experiment
            char.employment_entrepreneurship = game.player.employment_entrepreneurship
            char.aesthetic_cultivation = game.player.aesthetic_cultivation
            return char.to_dict()
        return None

    def _restore_character_to_player(self, game):
        if game.character:
            game.player.knowledge = game.character.knowledge
            game.player.knowledge_level = game.character.knowledge_level
            game.player.charm = game.character.charm
            game.player.charm_level = game.character.charm_level
            game.player.physical = game.character.physical
            game.player.physical_level = game.character.physical_level
            game.player.living_expenses = game.character.living_expenses
            game.player.action_points = game.character.action_points
            game.player.mood = game.character.mood
            game.player.health = game.character.health
            game.player.skill = game.character.skill
            game.player.social = game.character.social
            game.player.reputation = game.character.reputation
            game.player.theory_experiment = game.character.theory_experiment
            game.player.employment_entrepreneurship = game.character.employment_entrepreneurship
            game.player.aesthetic_cultivation = game.character.aesthetic_cultivation