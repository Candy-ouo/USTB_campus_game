import random
from typing import List, Dict

class EventOption:
    def __init__(self, text: str, effects: Dict[str, int]):
        self.text = text
        self.effects = effects

class GameEvent:
    def __init__(self, title: str, description: str, options: List[EventOption]):
        self.title = title
        self.description = description
        self.options = options

class EventManager:
    def __init__(self):
        self.local_templates = self._load_local_templates()
        self.ai = None
        try:
            from .ai_service import SimpleAI
            self.ai = SimpleAI()
        except:
            pass
    
    def _load_local_templates(self) -> List[Dict]:
        templates = []
        
        templates.append({
            "title": "课堂小测",
            "description": "老师突然宣布要进行一次突击小测！",
            "options": [
                {"text": "认真答题", "effects": {"knowledge": 2, "mood": -5}},
                {"text": "偷看同桌答案", "effects": {"knowledge": 1, "charm": -2, "mood": 5}},
                {"text": "假装生病请假", "effects": {"health": -5, "mood": 0}}
            ]
        })
        
        templates.append({
            "title": "食堂奇遇",
            "description": "在食堂吃饭时，发现一位同学忘带饭卡了。",
            "options": [
                {"text": "帮他刷饭卡", "effects": {"living_expenses": -10, "charm": 2, "mood": 5}},
                {"text": "假装没看到", "effects": {"mood": -3}},
                {"text": "邀请他一起拼单", "effects": {"living_expenses": -5, "charm": 1, "mood": 3}}
            ]
        })
        
        templates.append({
            "title": "图书馆座位",
            "description": "图书馆人满为患，你发现一个空位，但旁边同学在睡觉。",
            "options": [
                {"text": "轻轻坐下学习", "effects": {"knowledge": 2, "mood": 2}},
                {"text": "叫醒同学询问", "effects": {"charm": 1, "mood": -1}},
                {"text": "换个地方", "effects": {"action_points": -1}}
            ]
        })
        
        templates.append({
            "title": "晨跑偶遇",
            "description": "早上跑步时，看到体育老师在指导新生训练。",
            "options": [
                {"text": "加入训练", "effects": {"physical": 2, "action_points": -1, "mood": 3}},
                {"text": "打个招呼就走", "effects": {"charm": 1, "mood": 1}},
                {"text": "默默跑自己的步", "effects": {"physical": 1}}
            ]
        })
        
        templates.append({
            "title": "社团招新",
            "description": "新学期社团招新开始了，各个社团都在摆摊位。",
            "options": [
                {"text": "加入学习社", "effects": {"knowledge": 2, "living_expenses": -5}},
                {"text": "加入健身社", "effects": {"physical": 2, "living_expenses": -5}},
                {"text": "加入文艺社", "effects": {"charm": 2, "living_expenses": -5}}
            ]
        })
        
        templates.append({
            "title": "宿舍夜谈",
            "description": "晚上宿舍同学提议一起熬夜聊天。",
            "options": [
                {"text": "参与讨论", "effects": {"charm": 2, "health": -5, "mood": 5}},
                {"text": "委婉拒绝继续学习", "effects": {"knowledge": 1, "mood": -3}},
                {"text": "提议早点休息", "effects": {"health": 3, "charm": 1}}
            ]
        })
        
        templates.append({
            "title": "兼职机会",
            "description": "校门口便利店正在招聘兼职员工。",
            "options": [
                {"text": "报名兼职", "effects": {"living_expenses": 15, "action_points": -2, "health": -3}},
                {"text": "推荐给同学", "effects": {"charm": 2, "mood": 2}},
                {"text": "不感兴趣", "effects": {}}
            ]
        })
        
        templates.append({
            "title": "雨天忘伞",
            "description": "下课突然下起大雨，你没带雨伞。",
            "options": [
                {"text": "淋雨跑回宿舍", "effects": {"health": -5, "mood": -5}},
                {"text": "在教学楼等雨停", "effects": {"action_points": -1, "knowledge": 1}},
                {"text": "和同学共伞", "effects": {"charm": 2, "mood": 3}}
            ]
        })
        
        templates.append({
            "title": "捡到钱包",
            "description": "在教学楼门口捡到一个钱包。",
            "options": [
                {"text": "交给辅导员", "effects": {"charm": 3, "mood": 5}},
                {"text": "原地等待失主", "effects": {"charm": 2, "action_points": -1}},
                {"text": "据为己有", "effects": {"living_expenses": 50, "charm": -5}}
            ]
        })
        
        templates.append({
            "title": "考试周临近",
            "description": "期末考试快要到了，同学们都在紧张复习。",
            "options": [
                {"text": "通宵复习", "effects": {"knowledge": 3, "health": -5, "mood": -3}},
                {"text": "正常作息复习", "effects": {"knowledge": 1, "mood": 2}},
                {"text": "找学霸划重点", "effects": {"knowledge": 2, "social": 1}}
            ]
        })
        
        templates.append({
            "title": "食堂饭菜",
            "description": "今天食堂推出了新菜品，看起来很美味。",
            "options": [
                {"text": "尝试新菜品", "effects": {"health": 5, "living_expenses": -8, "mood": 3}},
                {"text": "吃常规饭菜", "effects": {"health": 2, "living_expenses": -5}},
                {"text": "不吃了省钱", "effects": {"health": -3, "mood": -2}}
            ]
        })
        
        templates.append({
            "title": "周末安排",
            "description": "周末到了，你打算怎么度过？",
            "options": [
                {"text": "去图书馆学习", "effects": {"knowledge": 2, "mood": -1}},
                {"text": "和朋友出去玩", "effects": {"charm": 2, "mood": 5, "living_expenses": -10}},
                {"text": "在宿舍休息", "effects": {"health": 5, "mood": 2}}
            ]
        })
        
        return templates

    def generate_random_event(self) -> GameEvent:
        if self.ai and self.ai.is_enabled():
            probability = self.ai.config.get("probability", 0.3)
            if random.random() < probability:
                try:
                    ai_result = self.ai.generate_event()
                    print(f"AI生成事件: {ai_result.get('title')}")
                    return self._create_event(ai_result)
                except Exception as e:
                    print(f"AI调用失败: {e}")
        
        template = random.choice(self.local_templates)
        return self._create_event(template)
    
    def _create_event(self, data: Dict) -> GameEvent:
        options = []
        for opt in data.get("options", []):
            options.append(EventOption(opt.get("text", "选项"), opt.get("effects", {})))
        if not options:
            options.append(EventOption("确认", {}))
        return GameEvent(data.get("title", "未知事件"), data.get("description", ""), options)