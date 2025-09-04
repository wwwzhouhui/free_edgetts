[中文](./README_CN.md) | English

[Project Source Code](https://github.com/wwwzhouhui/free_edgetts):

# EdgeTTS Dify Plugin

## Description
EdgeTTS is a text-to-speech Dify plugin based on the EdgeTTS API, compatible with the OpenAI API format. It supports multiple Chinese voices, speed control, and audio format output. Generated audio files are saved to the local temporary directory.

## Core Features
- 🎵 Supports multiple Chinese voices (Xiaoxiao, Yunxi, Xiaoyi, Yunjian, etc.)
- ⚡ Speed control (0.25x - 4.0x)
- 📁 Multiple audio formats (MP3, WAV, FLAC)
- 💾 Local file storage (saved to system temporary directory)
- 🔒 Secure API key management
- 🚀 OpenAI API format compatible
- 📊 Real-time processing progress display
- ✅ Complete parameter validation and error handling

## Installation and Configuration

### Requirements
- Python 3.12+
- dify_plugin >= 0.1.0, < 0.2.0
- openai >= 1.0.0
- requests >= 2.31.0
- pydantic >= 2.0.0

### Tech Stack
- **Dify Plugin Framework**: Built on the Dify plugin framework
- **OpenAI Compatible API**: Uses OpenAI client library to call EdgeTTS API
- **Asynchronous Processing**: Supports generator-based streaming processing
- **Data Validation**: Uses Pydantic for parameter validation
- **Error Handling**: Complete exception handling and user-friendly error messages

### EdgeTTS API Key Acquisition
1. Visit the EdgeTTS service provider: https://edgettsapi.duckcloud.fun
2. Register an account and obtain an API Key
3. Ensure the API Key is compatible with the OpenAI API format

### Plugin Installation
1. Copy the plugin directory to the Dify plugins directory
2. Enable the EdgeTTS plugin in the Dify management interface
3. Configure the necessary authentication information

### Configuration Instructions
Configure the following parameters in the Dify plugin management interface:

#### Required Configuration
- **EdgeTTS API Key**: API key obtained from the EdgeTTS service provider
  - Type: Encrypted input
  - Description: Authentication key compatible with OpenAI API format

#### Optional Configuration  
- **API Base URL**: EdgeTTS API base address
  - Default: https://edgettsapi.duckcloud.fun/v1
  - Type: Text input
  - Description: Customizable EdgeTTS API server address

## Usage

### Basic Usage
1. Add the EdgeTTS plugin to your Dify workflow
2. Enter the text content to be converted
3. Select the voice model and parameters
4. Obtain the generated audio file (saved to local temporary directory)

### Detailed Parameter Description

#### Text Content (input_text)
- **Type**: String (Required)
- **Description**: Text content to be converted to speech
- **Limit**: Maximum 5000 characters
- **Support**: Chinese and other supported languages

#### Voice Model (voice)  
- **Type**: Dropdown selection (Optional)
- **Default**: zh-CN-XiaoxiaoNeural
- **Options**:
  - `zh-CN-XiaoxiaoNeural`: Xiaoxiao (Chinese female voice)
  - `zh-CN-YunxiNeural`: Yunxi (Chinese male voice)
  - `zh-CN-XiaoyiNeural`: Xiaoyi (Chinese female voice)
  - `zh-CN-YunjianNeural`: Yunjian (Chinese male voice)

#### TTS Model (model)
- **Type**: Dropdown selection (Optional)  
- **Default**: tts-1
- **Options**:
  - `tts-1`: Standard quality, fast processing
  - `tts-1-hd`: High quality, better audio effect

#### Speech Speed (speed)
- **Type**: Numeric (Optional)
- **Default**: 1.0
- **Range**: 0.25 - 4.0
- **Description**: 1.0 is normal speed, 0.25 is slowest, 4.0 is fastest

#### Audio Format (response_format)
- **Type**: Dropdown selection (Optional)
- **Default**: mp3
- **Options**:
  - `mp3`: MP3 format (recommended, good compatibility)
  - `wav`: WAV format (lossless quality)
  - `flac`: FLAC format (lossless compression)

### Usage Example
```
Input text: "Welcome to use EdgeTTS plugin, this is a high-quality text-to-speech service."
Voice model: zh-CN-XiaoxiaoNeural (Xiaoxiao)
TTS model: tts-1 (standard)
Speed: 1.0x (normal speed)
Format: mp3
Output: Generate high-quality Chinese female voice MP3 audio file
Save location: System temporary directory (e.g. /tmp/edgetts_audio_1693123456.mp3)
```

### Processing Flow
The plugin displays detailed processing progress during execution:
1. 🚀 Starting voice generation...
2. 📝 Text length validation
3. 🎵 Voice model confirmation  
4. ⚡ Speed setting confirmation
5. 🔄 Calling EdgeTTS API...
6. ✅ Voice generation successful
7. 📊 Audio size statistics
8. 💾 Saving audio file to local...
9. 🎉 Voice conversion completed!

## Troubleshooting

### Common Issues
1. **Invalid API Key**: Check if the EdgeTTS API Key is correct
2. **Connection timeout**: Check network connection and API Base URL
3. **Text too long**: Ensure text length does not exceed 5000 characters
4. **Local save failure**: Check local disk space and permissions

### Error Codes
- 401: API Key invalid or expired
- 403: API Key insufficient permissions
- 404: API endpoint not found
- 429: API call rate too high
- 500: Server internal error

## Project Structure
```
free_edgetts/                    # Plugin root directory
├── manifest.yaml                # Plugin manifest file (defines plugin metadata and configuration)
├── main.py                      # Plugin entry file (starts plugin server)
├── requirements.txt             # Python dependency management
├── README.md                    # Project documentation
├── PRIVACY.md                   # Privacy policy
├── test_edgetts_fixed.py        # Test file
├── _assets/                     # Static resources directory
│   └── icon.svg                 # Plugin icon
├── provider/                    # Service provider configuration
│   ├── __init__.py
│   ├── edgetts.yaml            # Provider configuration (authentication, tool list)
│   └── edgetts_provider.py     # Provider implementation (credential validation logic)
├── tools/                       # TTS tool implementation
│   ├── __init__.py
│   ├── text_to_speech.yaml     # Tool configuration (parameter definition)
│   └── text_to_speech.py       # Tool implementation (core TTS logic)
└── utils/                       # Utility directory (reserved)
    └── __init__.py
```

### Core File Description

#### manifest.yaml
- Defines plugin basic information (name, version, author)
- Configures runtime environment (Python 3.12, 2GB memory allocation)
- Specifies tool providers and permission settings

#### provider/edgetts_provider.py
- Implements `EdgeTTSProvider` class, inheriting from `ToolProvider`
- Provides credential validation functionality (`_validate_credentials`)
- Tests EdgeTTS API connection availability

#### tools/text_to_speech.py
- Implements `TextToSpeechTool` class, inheriting from `Tool`  
- Core TTS conversion logic (`_invoke` method)
- Parameter validation, API calls, audio file saving
- Complete error handling and user feedback

## Development and Testing

### Local Development Environment Setup
1. **Environment Requirements**
   ```bash
   Python 3.12+
   pip >= 21.0
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Local Testing**  
   ```bash
   python main.py          # Start plugin server
   python test_edgetts_fixed.py  # Run test cases
   ```

### Testing Instructions
- `test_edgetts_fixed.py`: Contains EdgeTTS API connection and functionality tests
- Tests cover: parameter validation, API calls, audio generation, error handling
- It is recommended to run tests after code modifications to ensure functionality

### Debugging Tips
1. **Log Output**: The plugin displays detailed processing status during runtime
2. **Parameter Validation**: Check if input parameters meet requirements
3. **API Connection**: Verify EdgeTTS API Key and Base URL configuration
4. **Local Storage**: Check write permissions for the system temporary directory

### Plugin Configuration Files
- `manifest.yaml`: Plugin metadata and runtime configuration
- `provider/edgetts.yaml`: Authentication parameters and tool list definition  
- `tools/text_to_speech.yaml`: Tool parameter configuration and user interface definition

## Version Information
- **Current Version**: v0.0.1
- **Author**: wwwzhouhui
- **Supported Architectures**: AMD64, ARM64  
- **Runtime Environment**: Python 3.12
- **Plugin Type**: Dify Tool Plugin
- **Category**: Utilities

## Changelog

### v0.0.1 (2025-08-26)
**Initial Release**
- ✨ Complete EdgeTTS text-to-speech functionality
- 🔧 OpenAI API format compatible
- 🎵 Support for multiple Chinese voice models (Xiaoxiao, Yunxi, Xiaoyi, Yunjian)
- ⚡ Speed control (0.25x - 4.0x)
- 📁 Multi-format audio output (MP3, WAV, FLAC)
- 💾 Local temporary directory file storage
- 🔒 Secure API key management
- ✅ Complete parameter validation and error handling
- 📊 Real-time processing progress display
- 🧪 Includes test cases and development documentation

**Technical Features**
- Built on Dify Plugin Framework
- Uses generator pattern to support streaming processing
- Complete exception handling mechanism
- 2GB memory allocation for audio processing
- Supports maximum 5000 character text input

## License
This project follows an open-source license. See the project root directory for specific license information.

## Contributing
Welcome to submit Issues and Pull Requests to improve this project.

## Contact
- Author: wwwzhouhui
- EdgeTTS API Service: https://edgettsapi.duckcloud.fun