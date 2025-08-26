from dify_plugin import Plugin, DifyPluginEnv

# 配置EdgeTTS插件环境，设置60秒超时（适合TTS音频生成）
plugin = Plugin(DifyPluginEnv(MAX_REQUEST_TIMEOUT=60))

if __name__ == '__main__':
    plugin.run()