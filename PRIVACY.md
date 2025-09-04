# Privacy Policy

This plugin processes your text prompts to generate speech audio using the EdgeTTS API. Here's how your data is handled:

## Data Processing

- **Text Prompts**: Your text content is sent to the EdgeTTS API service to generate corresponding speech audio
- **API Communication**: The plugin communicates with EdgeTTS servers (https://edgettsapi.duckcloud.fun) to process text-to-speech requests
- **Generated Audio**: Audio files are temporarily downloaded and processed by the plugin, then returned to your Dify workflow
- **Processing Mode**: Uses synchronous API calls to ensure reliable audio generation

## Data Storage

- **No Local Storage**: The plugin does not permanently store your text prompts or generated audio files locally
- **Temporary Processing**: All data processing is temporary and happens only during the audio generation process
- **API Key Security**: Your EdgeTTS API key is stored securely within your Dify environment and is not logged or transmitted elsewhere

## Third-Party Services

- **EdgeTTS API**: Your text prompts are sent to the EdgeTTS text-to-speech service to create audio files
- **Network Communication**: The plugin requires internet connectivity to communicate with EdgeTTS servers
- **Service Provider**: EdgeTTS API service (edgettsapi.duckcloud.fun) processes your requests according to their privacy policy

## Data Retention

- The plugin does not retain any user data after task completion
- Generated audio files are temporarily processed and immediately returned to your workflow
- No persistent storage of prompts, audio files, or user information within the plugin