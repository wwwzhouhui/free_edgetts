from typing import Any
from openai import OpenAI
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin import ToolProvider

class EdgeTTSProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证 EdgeTTS API 凭据有效性
        基于 edgetts_service.py 和 testedgettsapi.py 的验证逻辑
        
        Args:
            credentials: 包含 EdgeTTS API 认证信息的字典
            
        Raises:
            ToolProviderCredentialValidationError: 当凭据验证失败时
        """
        try:
            # 1. 检查必需字段
            api_key = credentials.get("api_key")
            if not api_key:
                raise ToolProviderCredentialValidationError(
                    "EdgeTTS API key 不能为空"
                )
            
            # 2. 获取API基础URL（默认值来自config.ini）
            base_url = credentials.get("base_url", "https://edgettsapi.duckcloud.fun/v1")
            if not base_url:
                raise ToolProviderCredentialValidationError(
                    "EdgeTTS API base_url 不能为空"
                )
            
            # 3. 验证URL格式
            if not base_url.startswith(("http://", "https://")):
                raise ToolProviderCredentialValidationError(
                    "无效的 API base_url 格式，必须以 http:// 或 https:// 开头"
                )
            
            # 4. 测试API连接（参考testedgettsapi.py的测试逻辑）
            self._test_edgetts_connection(api_key, base_url)
            
        except ToolProviderCredentialValidationError:
            # 重新抛出已知的验证错误
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"EdgeTTS API 凭据验证失败: {str(e)}"
            )
    
    def _test_edgetts_connection(self, api_key: str, base_url: str) -> None:
        """
        测试EdgeTTS API连接
        基于testedgettsapi.py的测试逻辑
        
        Args:
            api_key: EdgeTTS API密钥
            base_url: EdgeTTS API基础URL
            
        Raises:
            ToolProviderCredentialValidationError: 当API连接测试失败时
        """
        try:
            # 创建OpenAI客户端（参考testedgettsapi.py）
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            
            # 发送测试请求（使用最小的测试数据）
            test_data = {
                'model': 'tts-1',
                'input': '测试',  # 最短的测试文本
                'voice': 'zh-CN-XiaoxiaoNeural',
                'response_format': 'mp3',
                'speed': 1.0,
            }
            
            # 执行测试请求（参考edgetts_service.py的调用方式）
            response = client.audio.speech.create(**test_data)
            
            # 检查响应是否有效
            if not hasattr(response, 'content') or not response.content:
                raise ToolProviderCredentialValidationError(
                    "EdgeTTS API 返回无效响应"
                )
            
            # 检查返回的音频数据是否有效（基本长度检查）
            if len(response.content) < 100:  # 音频文件应该至少有100字节
                raise ToolProviderCredentialValidationError(
                    "EdgeTTS API 返回的音频数据无效"
                )
                
        except ToolProviderCredentialValidationError:
            raise
        except Exception as e:
            # 处理常见的API错误
            error_msg = str(e).lower()
            if "401" in error_msg or "unauthorized" in error_msg:
                raise ToolProviderCredentialValidationError(
                    "EdgeTTS API Key 无效或已过期"
                )
            elif "403" in error_msg or "forbidden" in error_msg:
                raise ToolProviderCredentialValidationError(
                    "EdgeTTS API Key 权限不足"
                )
            elif "404" in error_msg or "not found" in error_msg:
                raise ToolProviderCredentialValidationError(
                    "EdgeTTS API 端点不存在，请检查 base_url 配置"
                )
            elif "timeout" in error_msg:
                raise ToolProviderCredentialValidationError(
                    "EdgeTTS API 连接超时，请检查网络连接"
                )
            else:
                raise ToolProviderCredentialValidationError(
                    f"EdgeTTS API 连接测试失败: {str(e)}"
                )