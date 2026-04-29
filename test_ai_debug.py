import sys
sys.path.append('.')

from src.ai_service import SimpleAI

def test_ai_debug():
    print("=== AI服务调试 ===")
    
    ai = SimpleAI()
    
    print(f"\n1. 配置检查:")
    print(f"   enabled: {ai.config.get('enabled')}")
    print(f"   provider: {ai.config.get('provider')}")
    print(f"   api_key: {ai.config.get('api_key', '')[:20]}...")
    print(f"   endpoint: {ai.config.get('endpoint', '未设置')}")
    print(f"   probability: {ai.config.get('probability')}")
    print(f"   is_enabled(): {ai.is_enabled()}")
    
    if not ai.is_enabled():
        print("\n❌ AI未启用或配置不完整")
        return
    
    print("\n2. 尝试调用AI生成事件...")
    
    try:
        event = ai.generate_event()
        print("\n✅ 成功生成事件!")
        print(f"标题: {event.get('title')}")
        print(f"描述: {event.get('description')}")
        print("选项:")
        for i, opt in enumerate(event.get("options", []), 1):
            print(f"  {i}. {opt.get('text')}")
            effects = opt.get("effects", {})
            if effects:
                print(f"     效果: {effects}")
    except Exception as e:
        print(f"\n❌ 生成失败: {str(e)}")

if __name__ == "__main__":
    test_ai_debug()