from src.item_system import ItemFactory

class Inventory:
    MAX_SLOTS = 20
    
    def __init__(self):
        self.items = {}
        self.item_order = []
    
    def add_item(self, item_id, quantity=1):
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            if len(self.item_order) >= self.MAX_SLOTS:
                return False, "背包已满"
            self.items[item_id] = quantity
            self.item_order.append(item_id)
        return True, f"获得 {ItemFactory.get_item_template(item_id)['name']} x{quantity}"
    
    def remove_item(self, item_id, quantity=1):
        if item_id not in self.items:
            return False, "物品不存在"
        if self.items[item_id] < quantity:
            return False, "数量不足"
        self.items[item_id] -= quantity
        if self.items[item_id] == 0:
            del self.items[item_id]
            self.item_order.remove(item_id)
        return True, "使用成功"
    
    def get_item_quantity(self, item_id):
        return self.items.get(item_id, 0)
    
    def get_all_items(self):
        result = []
        for item_id in self.item_order:
            item = ItemFactory.create_item(item_id)
            if item:
                result.append((item, self.items[item_id]))
        return result
    
    def get_slot_items(self):
        result = []
        for i in range(self.MAX_SLOTS):
            if i < len(self.item_order):
                item_id = self.item_order[i]
                item = ItemFactory.create_item(item_id)
                if item:
                    result.append((item, self.items[item_id]))
            else:
                result.append((None, 0))
        return result
    
    def is_full(self):
        return len(self.item_order) >= self.MAX_SLOTS
    
    def get_empty_slots(self):
        return self.MAX_SLOTS - len(self.item_order)
    
    def use_item(self, item_id, player, current_year=None):
        item = ItemFactory.create_item(item_id)
        if not item:
            return False, "物品不存在"
        
        if not item.can_use():
            return False, "该物品不可使用"
        
        success, msg = self.remove_item(item_id, 1)
        if not success:
            return False, msg
        
        for attr, value in item.effects.items():
            if attr == 'knowledge':
                player.add_knowledge(value, current_year)
            elif attr == 'charm':
                player.add_charm(value, current_year)
            elif attr == 'physical':
                player.add_physical(value, current_year)
            elif attr == 'living_expenses':
                player.add_living_expenses(value)
            elif attr == 'action_points':
                player.add_action_points(value)
            elif attr == 'mood':
                player.add_mood(value)
            elif attr == 'health':
                player.add_health(value)
            elif attr == 'skill':
                player.add_skill(value)
            elif attr == 'social':
                player.add_social(value)
            elif attr == 'reputation':
                player.add_reputation(value)
        
        effect_desc = ", ".join([f"{self._get_attr_name(k)} {v:+}" for k, v in item.effects.items()])
        return True, f"使用了 {item.name}，{effect_desc}"
    
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
    
    def to_dict(self):
        return {
            'items': self.items,
            'item_order': self.item_order
        }
    
    def from_dict(self, data):
        self.items = data.get('items', {})
        self.item_order = data.get('item_order', [])
        for item_id in list(self.items.keys()):
            if item_id not in self.item_order:
                self.item_order.append(item_id)
        if len(self.item_order) > self.MAX_SLOTS:
            self.item_order = self.item_order[:self.MAX_SLOTS]
        for item_id in list(self.item_order):
            if item_id not in self.items:
                self.item_order.remove(item_id)
    
    def clear(self):
        self.items = {}
        self.item_order = []