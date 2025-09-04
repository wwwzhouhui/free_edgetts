中文 ｜ [English](./README.md)

[项目源码地址](https://github.com/wwwzhouhui/free_edgetts)：

# EdgeTTS Dify 插件

## 功能描述
EdgeTTS 是一个基于 EdgeTTS API 的文本转语音 Dify 插件，兼容 OpenAI API 格式，支持多种中文语音、语速控制和音频格式输出。生成的音频文件保存在本地临时目录。

## 核心特性
- 🎵 支持多种中文语音（晓晓、云希、晓伊、云健等）
- ⚡ 语速控制（0.25x - 4.0x）
- 📁 多种音频格式（MP3、WAV、FLAC）
- 💾 本地文件存储（保存到系统临时目录）
- 🔒 安全的API密钥管理
- 🚀 OpenAI API 格式兼容
- 📊 实时处理进度显示
- ✅ 完整的参数验证和错误处理

## 安装配置

### 依赖要求
- Python 3.12+
- dify_plugin >= 0.1.0, < 0.2.0
- openai >= 1.0.0
- requests >= 2.31.0
- pydantic >= 2.0.0

### 技术栈
- **Dify Plugin Framework**: 基于 Dify 插件框架构建
- **OpenAI Compatible API**: 使用 OpenAI 客户端库调用 EdgeTTS API
- **异步处理**: 支持生成器模式的流式处理
- **数据验证**: 使用 Pydantic 进行参数验证
- **错误处理**: 完整的异常处理和用户友好的错误消息

### EdgeTTS API Key 获取
1. 访问 EdgeTTS 服务提供商：https://edgettsapi.duckcloud.fun
2. 注册账户并获取 API Key
3. 确保 API Key 兼容 OpenAI API 格式

### 插件安装
1. 将插件目录复制到 Dify 插件目录
2. 在 Dify 管理界面中启用 EdgeTTS 插件
3. 配置必要的认证信息

### 配置说明
在 Dify 插件管理界面配置以下参数：

#### 必需配置
- **EdgeTTS API Key**：从 EdgeTTS 服务提供商获取的 API 密钥
  - 类型：加密输入
  - 说明：兼容 OpenAI API 格式的认证密钥

#### 可选配置  
- **API Base URL**：EdgeTTS API 基础地址
  - 默认值：https://edgettsapi.duckcloud.fun/v1
  - 类型：文本输入
  - 说明：可自定义 EdgeTTS API 服务器地址

## 使用方法

### 基本用法
1. 在 Dify 工作流中添加 EdgeTTS 插件
2. 输入要转换的文本内容
3. 选择语音模型和参数
4. 获取生成的音频文件（保存到本地临时目录）

### 详细参数说明

#### 文本内容 (input_text)
- **类型**: 字符串 (必需)
- **描述**: 要转换为语音的文本内容
- **限制**: 最大 5000 字符
- **支持**: 中文及其他支持的语言

#### 语音模型 (voice)  
- **类型**: 下拉选择 (可选)
- **默认值**: zh-CN-XiaoxiaoNeural
- **可选项**:
  - `zh-CN-XiaoxiaoNeural`: 晓晓（中文女声）
  - `zh-CN-YunxiNeural`: 云希（中文男声）
  - `zh-CN-XiaoyiNeural`: 晓伊（中文女声）
  - `zh-CN-YunjianNeural`: 云健（中文男声）

#### TTS 模型 (model)
- **类型**: 下拉选择 (可选)  
- **默认值**: tts-1
- **可选项**:
  - `tts-1`: 标准质量，处理速度快
  - `tts-1-hd`: 高质量，音频效果更佳

#### 语音速度 (speed)
- **类型**: 数值 (可选)
- **默认值**: 1.0
- **范围**: 0.25 - 4.0
- **说明**: 1.0 为正常速度，0.25 最慢，4.0 最快

#### 音频格式 (response_format)
- **类型**: 下拉选择 (可选)
- **默认值**: mp3
- **可选项**:
  - `mp3`: MP3 格式（推荐，兼容性好）
  - `wav`: WAV 格式（无损音质）
  - `flac`: FLAC 格式（无损压缩）

### 使用示例
```
输入文本："欢迎使用EdgeTTS插件，这是一个高质量的文本转语音服务。"
语音模型：zh-CN-XiaoxiaoNeural (晓晓)
TTS模型：tts-1 (标准)
语速：1.0x (正常速度)
格式：mp3
输出：生成高质量的中文女声MP3音频文件
保存位置：系统临时目录（如 /tmp/edgetts_audio_1693123456.mp3）
```

### 处理流程
插件执行时会显示详细的处理进度：
1. 🚀 开始生成语音...
2. 📝 文本长度验证
3. 🎵 语音模型确认  
4. ⚡ 语速设置确认
5. 🔄 正在调用EdgeTTS API...
6. ✅ 语音生成成功
7. 📊 音频大小统计
8. 💾 正在保存音频文件到本地...
9. 🎉 语音转换完成！

## 故障排除

### 常见问题
1. **API Key 无效**：检查 EdgeTTS API Key 是否正确
2. **连接超时**：检查网络连接和 API Base URL
3. **文本过长**：确保文本长度不超过5000字符
4. **本地保存失败**：检查本地磁盘空间和权限

### 错误代码
- 401：API Key 无效或已过期
- 403：API Key 权限不足
- 404：API 端点不存在
- 429：API 调用频率过高
- 500：服务器内部错误

## 项目结构
```
free_edgetts/                    # 插件根目录
├── manifest.yaml                # 插件清单文件（定义插件元数据和配置）
├── main.py                      # 插件入口文件（启动插件服务器）
├── requirements.txt             # Python 依赖管理
├── README.md                    # 项目文档
├── test_edgetts_fixed.py        # 测试文件
├── _assets/                     # 静态资源目录
│   └── icon.svg                 # 插件图标
├── provider/                    # 服务提供者配置
│   ├── __init__.py
│   ├── edgetts.yaml            # 提供者配置（认证、工具列表）
│   └── edgetts_provider.py     # 提供者实现（凭据验证逻辑）
├── tools/                       # TTS 工具实现
│   ├── __init__.py
│   ├── text_to_speech.yaml     # 工具配置（参数定义）
│   └── text_to_speech.py       # 工具实现（核心 TTS 逻辑）
└── utils/                       # 工具类目录（预留）
    └── __init__.py
```

### 核心文件说明

#### manifest.yaml
- 定义插件基本信息（名称、版本、作者）
- 配置运行环境（Python 3.12、内存分配 2GB）
- 指定工具提供者和权限设置

#### provider/edgetts_provider.py
- 实现 `EdgeTTSProvider` 类，继承自 `ToolProvider`
- 提供凭据验证功能（`_validate_credentials`）
- 测试 EdgeTTS API 连接可用性

#### tools/text_to_speech.py
- 实现 `TextToSpeechTool` 类，继承自 `Tool`  
- 核心 TTS 转换逻辑（`_invoke` 方法）
- 参数验证、API 调用、音频文件保存
- 完整的错误处理和用户反馈

## 开发和测试

### 本地开发环境设置
1. **环境要求**
   ```bash
   Python 3.12+
   pip >= 21.0
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **本地测试**  
   ```bash
   python main.py          # 启动插件服务器
   python test_edgetts_fixed.py  # 运行测试用例
   ```

### 测试说明
- `test_edgetts_fixed.py`: 包含 EdgeTTS API 连接和功能测试
- 测试涵盖：参数验证、API 调用、音频生成、错误处理
- 建议在修改代码后运行测试确保功能正常

### 调试技巧
1. **日志输出**: 插件运行时会显示详细的处理状态
2. **参数验证**: 检查输入参数是否符合要求
3. **API 连接**: 验证 EdgeTTS API Key 和 Base URL 配置
4. **本地存储**: 检查系统临时目录的写入权限

### 插件配置文件
- `manifest.yaml`: 插件元数据和运行配置
- `provider/edgetts.yaml`: 认证参数和工具列表定义  
- `tools/text_to_speech.yaml`: 工具参数配置和用户界面定义

## 版本信息
- **当前版本**: v0.0.1
- **作者**: wwwzhouhui
- **支持架构**: AMD64, ARM64  
- **运行环境**: Python 3.12
- **插件类型**: Dify 工具插件
- **分类**: 实用工具 (utilities)

## 更新日志

### v0.0.1 (2025-08-26)
**初始版本发布**
- ✨ 完整的 EdgeTTS 文本转语音功能
- 🔧 OpenAI API 格式兼容
- 🎵 支持多种中文语音模型（晓晓、云希、晓伊、云健）
- ⚡ 语速控制（0.25x - 4.0x）
- 📁 多格式音频输出（MP3、WAV、FLAC）
- 💾 本地临时目录文件存储
- 🔒 安全的 API 密钥管理
- ✅ 完整的参数验证和错误处理
- 📊 实时处理进度显示
- 🧪 包含测试用例和开发文档

**技术特性**
- 基于 Dify Plugin Framework 构建
- 使用生成器模式支持流式处理
- 完整的异常处理机制
- 2GB 内存分配用于音频处理
- 支持最大 5000 字符文本输入

## 许可证
本项目遵循开源协议，具体许可证信息请查看项目根目录。

## 贡献
欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式
- 作者：wwwzhouhui
- EdgeTTS API 服务：https://edgettsapi.duckcloud.fun