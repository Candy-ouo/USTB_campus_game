import pygame
import os

class Item:
    def __init__(self, item_id, name, description, icon_path, item_type='consumable', effects=None, price=0):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.icon_path = icon_path
        self.item_type = item_type
        self.effects = effects if effects is not None else {}
        self.price = price
        self.icon = None
        self._load_icon()
    
    def _load_icon(self):
        try:
            full_path = os.path.join(os.path.dirname(__file__), '..', 'image', self.icon_path)
            if os.path.exists(full_path):
                self.icon = pygame.image.load(full_path).convert_alpha()
                self.icon = pygame.transform.scale(self.icon, (48, 48))
            else:
                self.icon = self._create_default_icon()
        except Exception as e:
            self.icon = self._create_default_icon()
    
    def _create_default_icon(self):
        surface = pygame.Surface((48, 48), pygame.SRCALPHA)
        pygame.draw.rect(surface, (100, 100, 100), (0, 0, 48, 48))
        pygame.draw.rect(surface, (150, 150, 150), (0, 0, 48, 48), 2)
        return surface
    
    def can_use(self):
        return self.item_type == 'consumable' and self.effects
    
    def to_dict(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'icon_path': self.icon_path,
            'item_type': self.item_type,
            'effects': self.effects,
            'price': self.price
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data['item_id'],
            name=data['name'],
            description=data['description'],
            icon_path=data['icon_path'],
            item_type=data.get('item_type', 'consumable'),
            effects=data.get('effects', {}),
            price=data.get('price', 0)
        )

class ItemFactory:
    _items = {
        'cake': {
            'name': '美味蛋糕',
            'description': '香甜可口的蛋糕，能提升心情和人脉',
            'icon_path': 'cake.png',
            'item_type': 'consumable',
            'effects': {'mood': 30, 'social': 2},
            'price': 15
        },
        'cloth': {
            'name': '潮流衣服',
            'description': '时尚的衣服，提升魅力和声望',
            'icon_path': 'cloth.png',
            'item_type': 'consumable',
            'effects': {'charm': 10, 'reputation': 2},
            'price': 30
        },
        'book': {
            'name': '课外教材',
            'description': '知识丰富的教材，提升学识和技能',
            'icon_path': 'book.png',
            'item_type': 'consumable',
            'effects': {'knowledge': 10, 'skill': 3},
            'price': 20
        },
        'fitness': {
            'name': '健身器材',
            'description': '专业的健身器材，提升体能和声望',
            'icon_path': 'jianshenqicai.png',
            'item_type': 'consumable',
            'effects': {'physical': 10, 'reputation': 2},
            'price': 30
        },
        'snack': {
            'name': '不健康的零食',
            'description': '虽然美味但不健康的零食',
            'icon_path': 'lingshi.png',
            'item_type': 'consumable',
            'effects': {'mood': 40, 'health': -5, 'social': 1},
            'price': 15
        },
        'potion': {
            'name': '体力药水',
            'description': '神奇的药水，恢复行动力',
            'icon_path': 'tiliyaoshui.png',
            'item_type': 'consumable',
            'effects': {'action_points': 1},
            'price': 30
        }
    }
    
    @classmethod
    def create_item(cls, item_id):
        if item_id in cls._items:
            data = cls._items[item_id]
            return Item(
                item_id=item_id,
                name=data['name'],
                description=data['description'],
                icon_path=data['icon_path'],
                item_type=data['item_type'],
                effects=data['effects'],
                price=data['price']
            )
        return None
    
    @classmethod
    def get_item_template(cls, item_id):
        return cls._items.get(item_id)
    
    @classmethod
    def get_all_item_ids(cls):
        return list(cls._items.keys())