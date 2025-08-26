import os
import time
import tempfile
from collections.abc import Generator
from openai import OpenAI
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool

class TextToSpeechTool(Tool):
    def _invoke(
        self, tool_parameters: dict
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        EdgeTTS文本转语音工具（本地存储版本）
        基于edgetts_service.py的完整实现逻辑，但保存到本地而不是COS
        
        Args:
            tool_parameters: 工具参数字典
            
        Yields:
            ToolInvokeMessage: 工具调用消息
        """
        try:
            # 1. 获取认证信息（参考edgetts_service.py的配置加载）
            api_key = self.runtime.credentials.get("api_key")
            base_url = self.runtime.credentials.get("base_url", "https://edgettsapi.duckcloud.fun/v1")
            
            # 2. 参数验证（基于TTSRequest模型）
            input_text = tool_parameters.get("input_text")
            if not input_text or not input_text.strip():
                yield self.create_text_message("❌ 文本内容不能为空")
                return
            
            voice = tool_parameters.get("voice", "zh-CN-XiaoxiaoNeural")
            model = tool_parameters.get("model", "tts-1")
            speed = tool_parameters.get("speed", 1.0)
            response_format = tool_parameters.get("response_format", "mp3")
            
            # 验证语速范围
            if not (0.25 <= speed <= 4.0):
                yield self.create_text_message("❌ 语速必须在0.25-4.0之间")
                return
            
            # 验证文本长度（避免过长文本导致API超时）
            if len(input_text) > 5000:
                yield self.create_text_message("❌ 文本长度不能超过5000字符")
                return
            
            yield self.create_text_message("🚀 开始生成语音...")
            yield self.create_text_message(f"📝 文本长度: {len(input_text)} 字符")
            yield self.create_text_message(f"🎵 使用语音: {voice}")
            yield self.create_text_message(f"⚡ 语速设置: {speed}x")
            
            # 3. 创建OpenAI客户端（参考edgetts_service.py）
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            
            # 4. 构建请求数据（完全按照edgetts_service.py的格式）
            data = {
                'model': model,
                'input': input_text,
                'voice': voice,
                'response_format': response_format,
                'speed': speed,
            }
            
            # 5. 调用EdgeTTS API（参考edgetts_service.py的调用方式）
            yield self.create_text_message("🔄 正在调用EdgeTTS API...")
            
            response = client.audio.speech.create(**data)
            
            if not hasattr(response, 'content') or not response.content:
                yield self.create_text_message("❌ EdgeTTS API返回空响应")
                return
            
            yield self.create_text_message("✅ 语音生成成功")
            yield self.create_text_message(f"📊 音频大小: {len(response.content)} 字节")
            
            # 6. 处理音频文件（本地存储）
            audio_content = response.content
            
            # 7. 生成本地文件名（参考edgetts_service.py的命名规则）
            timestamp = int(time.time())
            filename = f"edgetts_audio_{timestamp}.{response_format}"
            
            yield self.create_text_message("💾 正在保存音频文件到本地...")
            
            # 8. 保存到本地临时目录
            try:
                # 创建临时目录用于存储音频文件
                temp_dir = tempfile.gettempdir()
                local_file_path = os.path.join(temp_dir, filename)
                
                with open(local_file_path, 'wb') as f:
                    f.write(audio_content)
                
                yield self.create_text_message(f"✅ 音频文件已保存到: {local_file_path}")
                
                # 返回音频文件和本地路径信息
                yield self.create_blob_message(
                    blob=audio_content,
                    meta={
                        "mime_type": f"audio/{response_format}",
                        "filename": filename,
                        "local_path": local_file_path,
                        "file_size": len(audio_content)
                    }
                )
                
            except Exception as save_error:
                yield self.create_text_message(f"⚠️ 本地保存失败: {str(save_error)}")
                yield self.create_text_message("📁 返回音频文件内容")
                yield self.create_blob_message(
                    blob=audio_content,
                    meta={"mime_type": f"audio/{response_format}"}
                )
            
            yield self.create_text_message("🎉 语音转换完成！")
                
        except Exception as e:
            # EdgeTTS 特定错误处理
            error_msg = str(e).lower()
            if "401" in error_msg or "unauthorized" in error_msg:
                yield self.create_text_message("❌ EdgeTTS API Key 无效或已过期")
            elif "403" in error_msg or "forbidden" in error_msg:
                yield self.create_text_message("❌ EdgeTTS API Key 权限不足")
            elif "404" in error_msg or "not found" in error_msg:
                yield self.create_text_message("❌ EdgeTTS API 端点不存在，请检查base_url配置")
            elif "429" in error_msg or "rate limit" in error_msg:
                yield self.create_text_message("❌ EdgeTTS API 调用频率过高，请稍后重试")
            elif "500" in error_msg or "internal server error" in error_msg:
                yield self.create_text_message("❌ EdgeTTS 服务器内部错误")
            elif "timeout" in error_msg:
                yield self.create_text_message("❌ EdgeTTS API 连接超时，请检查网络连接")
            else:
                yield self.create_text_message(f"❌ 语音生成失败: {str(e)}")
    
    def _validate_tts_parameters(self, parameters: dict) -> bool:
        """EdgeTTS参数验证"""
        # 验证必需参数
        input_text = parameters.get("input_text")
        if not input_text or not input_text.strip():
            return False
        
        # 验证语速范围
        speed = parameters.get("speed", 1.0)
        if not (0.25 <= speed <= 4.0):
            return False
        
        # 验证文本长度（避免过长文本导致API超时）
        if len(input_text) > 5000:
            return False
        
        return True