#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EdgeTTS插件测试脚本（修复版）
基于testedgettsapi.py的API配置进行测试
"""

import os
import sys
import tempfile
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.text_to_speech import TextToSpeechTool
from provider.edgetts_provider import EdgeTTSProvider

class MockRuntime:
    """模拟Dify插件运行时环境"""
    def __init__(self):
        # 使用testedgettsapi.py中的配置
        self.credentials = {
            "api_key": "zhouhuizhou",  # 来自testedgettsapi.py
            "base_url": "https://edgettsapi.duckcloud.fun/v1"  # 来自testedgettsapi.py
        }

class MockSession:
    """模拟Dify插件会话环境"""
    def __init__(self):
        pass

def test_provider_validation():
    """测试Provider认证验证功能"""
    print("🔍 测试EdgeTTS Provider认证验证...")
    
    provider = EdgeTTSProvider()
    
    try:
        # 测试有效凭据
        valid_credentials = {
            "api_key": "zhouhuizhou",
            "base_url": "https://edgettsapi.duckcloud.fun/v1"
        }
        provider._validate_credentials(valid_credentials)
        print("✅ Provider认证验证通过")
        return True
        
    except Exception as e:
        print(f"❌ Provider认证验证失败: {str(e)}")
        return False

def test_tts_tool():
    """测试TTS工具功能"""
    print("\n🎵 测试EdgeTTS文本转语音工具...")
    
    # 创建工具实例
    runtime = MockRuntime()
    session = MockSession()
    tool = TextToSpeechTool(runtime=runtime, session=session)
    
    # 测试参数（基于testedgettsapi.py的参数）
    test_parameters = {
        "input_text": "这是一个EdgeTTS插件测试，测试文本转语音功能。欢迎使用EdgeTTS插件！",
        "voice": "zh-CN-XiaoxiaoNeural",
        "model": "tts-1",
        "speed": 1.0,
        "response_format": "mp3"
    }
    
    print(f"📝 测试文本: {test_parameters['input_text']}")
    print(f"🎵 语音模型: {test_parameters['voice']}")
    print(f"⚡ 语速: {test_parameters['speed']}x")
    print(f"📁 格式: {test_parameters['response_format']}")
    
    try:
        # 执行测试
        messages = []
        audio_file_path = None
        audio_blob = None
        
        for message in tool._invoke(test_parameters):
            messages.append(message)
            
            # 打印文本消息
            if hasattr(message, 'type') and str(message.type) == 'MessageType.TEXT':
                if hasattr(message, 'message') and hasattr(message.message, 'text'):
                    print(f"📝 {message.message.text}")
            
            # 处理音频消息
            elif hasattr(message, 'type') and str(message.type) == 'MessageType.BLOB':
                if hasattr(message, 'message') and hasattr(message.message, 'blob'):
                    audio_blob = message.message.blob
                    print(f"🎵 收到音频文件，大小: {len(audio_blob)} 字节")
                    
                    # 检查元数据
                    if hasattr(message, 'meta') and message.meta:
                        filename = message.meta.get('filename', 'test_audio.mp3')
                        local_path = message.meta.get('local_path')
                        file_size = message.meta.get('file_size', len(audio_blob))
                        mime_type = message.meta.get('mime_type', 'audio/mp3')
                        
                        print(f"📄 文件名: {filename}")
                        print(f"📊 文件大小: {file_size} 字节")
                        print(f"🏷️ MIME类型: {mime_type}")
                        
                        if local_path:
                            print(f"💾 本地路径: {local_path}")
                            audio_file_path = local_path
                            
                            # 验证文件是否存在
                            if os.path.exists(local_path):
                                actual_size = os.path.getsize(local_path)
                                print(f"✅ 文件已保存，实际大小: {actual_size} 字节")
                            else:
                                print(f"⚠️ 文件路径不存在: {local_path}")
        
        print("✅ EdgeTTS工具测试完成")
        
        # 验证音频文件
        if audio_blob and len(audio_blob) > 0:
            print(f"🎉 测试成功！音频数据大小: {len(audio_blob)} 字节")
            if audio_file_path:
                print(f"📁 音频文件位置: {audio_file_path}")
            return True, audio_file_path
        else:
            print("❌ 未生成音频数据")
            return False, None
            
    except Exception as e:
        print(f"❌ TTS工具测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def test_different_voices():
    """测试不同语音模型"""
    print("\n🎭 测试不同语音模型...")
    
    voices = [
        ("zh-CN-XiaoxiaoNeural", "晓晓（中文女声）"),
        ("zh-CN-YunxiNeural", "云希（中文男声）"),
        ("zh-CN-XiaoyiNeural", "晓伊（中文女声）"),
        ("zh-CN-YunjianNeural", "云健（中文男声）")
    ]
    
    runtime = MockRuntime()
    session = MockSession()
    tool = TextToSpeechTool(runtime=runtime, session=session)
    
    success_count = 0
    
    for voice_id, voice_name in voices:
        print(f"\n🎵 测试语音: {voice_name} ({voice_id})")
        
        test_parameters = {
            "input_text": f"你好，我是{voice_name}，这是语音测试。",
            "voice": voice_id,
            "model": "tts-1",
            "speed": 1.0,
            "response_format": "mp3"
        }
        
        try:
            audio_generated = False
            for message in tool._invoke(test_parameters):
                if hasattr(message, 'type') and str(message.type) == 'MessageType.BLOB':
                    if hasattr(message, 'message') and hasattr(message.message, 'blob'):
                        audio_generated = True
                        print(f"✅ {voice_name} 测试成功，音频大小: {len(message.message.blob)} 字节")
                        break
            
            if audio_generated:
                success_count += 1
            else:
                print(f"❌ {voice_name} 测试失败：未生成音频")
                
        except Exception as e:
            print(f"❌ {voice_name} 测试失败: {str(e)}")
    
    print(f"\n📊 语音测试结果: {success_count}/{len(voices)} 成功")
    return success_count == len(voices)

def test_speed_control():
    """测试语速控制"""
    print("\n⚡ 测试语速控制...")
    
    speeds = [0.5, 1.0, 1.5, 2.0]
    runtime = MockRuntime()
    session = MockSession()
    tool = TextToSpeechTool(runtime=runtime, session=session)
    
    success_count = 0
    
    for speed in speeds:
        print(f"\n⚡ 测试语速: {speed}x")
        
        test_parameters = {
            "input_text": f"这是{speed}倍速的语音测试。",
            "voice": "zh-CN-XiaoxiaoNeural",
            "model": "tts-1",
            "speed": speed,
            "response_format": "mp3"
        }
        
        try:
            audio_generated = False
            for message in tool._invoke(test_parameters):
                if hasattr(message, 'type') and str(message.type) == 'MessageType.BLOB':
                    if hasattr(message, 'message') and hasattr(message.message, 'blob'):
                        audio_generated = True
                        print(f"✅ {speed}x语速测试成功，音频大小: {len(message.message.blob)} 字节")
                        break
            
            if audio_generated:
                success_count += 1
            else:
                print(f"❌ {speed}x语速测试失败：未生成音频")
                
        except Exception as e:
            print(f"❌ {speed}x语速测试失败: {str(e)}")
    
    print(f"\n📊 语速测试结果: {success_count}/{len(speeds)} 成功")
    return success_count == len(speeds)

def main():
    """主测试函数"""
    print("🚀 开始EdgeTTS插件完整测试...")
    print("=" * 50)
    
    # 测试结果统计
    test_results = []
    
    # 1. 测试Provider认证
    provider_result = test_provider_validation()
    test_results.append(("Provider认证验证", provider_result))
    
    # 2. 测试基础TTS功能
    tts_result, audio_path = test_tts_tool()
    test_results.append(("基础TTS功能", tts_result))
    
    # 3. 测试不同语音模型
    voices_result = test_different_voices()
    test_results.append(("多语音模型", voices_result))
    
    # 4. 测试语速控制
    speed_result = test_speed_control()
    test_results.append(("语速控制", speed_result))
    
    # 输出测试总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print("=" * 50)
    
    success_count = 0
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n🎯 总体结果: {success_count}/{len(test_results)} 项测试通过")
    
    if success_count == len(test_results):
        print("🎉 所有测试通过！EdgeTTS插件功能正常。")
        if audio_path:
            print(f"🎵 示例音频文件: {audio_path}")
    else:
        print("⚠️ 部分测试失败，请检查配置和网络连接。")
    
    return success_count == len(test_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)