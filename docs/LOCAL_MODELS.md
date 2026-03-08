# Using Local LLM Models

This guide explains how to run the College Admissions AI Counselor **without an OpenAI API key** using free, open-source local models.

## Quick Start

1. **Install dependencies with local model support:**
   ```bash
   pip install torch transformers accelerate
   ```

2. **Configure for local mode:**
   Edit your `.env` file:
   ```bash
   USE_LOCAL_MODEL=true
   LOCAL_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
   ```

3. **Run the application:**
   ```bash
   python main.py --interactive
   ```

The model will download automatically on first run (~2GB for TinyLlama).

## Recommended Models

### TinyLlama (Default) - Best for Testing
- **Model**: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
- **Size**: ~2GB
- **RAM**: 4-8GB
- **Speed**: Fast on CPU
- **Quality**: Basic, good for testing

### Phi-2 - Balanced Performance
- **Model**: `microsoft/phi-2`
- **Size**: ~5GB
- **RAM**: 8-16GB
- **Speed**: Moderate on CPU
- **Quality**: Good for most tasks

### Llama-2-7B - Best Quality
- **Model**: `meta-llama/Llama-2-7b-chat-hf`
- **Size**: ~13GB
- **RAM**: 16-32GB recommended
- **Speed**: Slow on CPU, fast with GPU
- **Quality**: Excellent, closest to GPT-3.5

### Other Options
Any HuggingFace model that supports text generation can be used:
- `mistralai/Mistral-7B-Instruct-v0.1`
- `HuggingFaceH4/zephyr-7b-beta`
- `stabilityai/stablelm-2-1_6b-chat`

## Configuration

### Basic Configuration (.env)
```bash
# Enable local model
USE_LOCAL_MODEL=true

# Choose your model
LOCAL_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0

# Model parameters
TEMPERATURE=0.7
MAX_TOKENS=2000
```

### Programmatic Configuration
```python
import os
from counselor_ai import CounselorAgent

# Force local model
os.environ['USE_LOCAL_MODEL'] = 'true'
os.environ['LOCAL_MODEL'] = 'microsoft/phi-2'

# Create agent (will use local model)
agent = CounselorAgent()
```

### GPU Acceleration

If you have an NVIDIA GPU with CUDA:

```bash
# Install PyTorch with CUDA support
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Models will automatically use GPU
```

For Apple Silicon Macs:
```bash
# MPS (Metal Performance Shaders) is used automatically
# No additional setup needed
```

## Performance Comparison

| Model | Size | RAM | CPU Speed | GPU Speed | Quality |
|-------|------|-----|-----------|-----------|---------|
| TinyLlama | 2GB | 4GB | Fast | Very Fast | Basic |
| Phi-2 | 5GB | 8GB | Medium | Fast | Good |
| Llama-2-7B | 13GB | 16GB | Slow | Fast | Excellent |
| GPT-4 (API) | N/A | N/A | Fast | Fast | Best |

**Note**: CPU speeds are on modern processors. Older CPUs may be significantly slower.

## Advantages of Local Models

### Privacy
- All data stays on your computer
- No data sent to external APIs
- Full FERPA compliance
- No internet required after download

### Cost
- Zero API costs
- No usage limits
- Free forever
- Only one-time download

### Availability
- Works offline
- No rate limits
- Always available
- No API key management

## Limitations

### Resource Requirements
- Requires available RAM
- First download can be slow
- Takes disk space for models

### Performance
- Slower than cloud APIs (without GPU)
- May produce less accurate results
- Limited context window
- Requires more prompt engineering

### Quality Trade-offs
- Smaller models = lower quality
- May not follow instructions as well
- Less creative and nuanced
- May need more validation

## Troubleshooting

### Out of Memory Errors
```bash
# Try a smaller model
LOCAL_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0

# Or close other applications
# Or add swap space (Linux)
```

### Slow Performance
```bash
# Use smaller model
# Enable GPU if available
# Reduce MAX_TOKENS in .env
MAX_TOKENS=1000
```

### Model Download Fails
```bash
# Check internet connection
# Verify sufficient disk space
# Try manual download from Hugging Face
# Use HF_HOME to specify cache location
export HF_HOME=/path/to/large/disk
```

### Import Errors
```bash
# Install all required packages
pip install torch transformers accelerate

# Update to latest versions
pip install --upgrade torch transformers accelerate
```

## Examples

### Example 1: Quick Student Analysis
```python
from counselor_ai import CounselorAgent, StudentProfile
from counselor_ai.models.student import AcademicRecord
import os

os.environ['USE_LOCAL_MODEL'] = 'true'

student = StudentProfile(
    name="Jane Doe",
    graduation_year=2025,
    academic_record=AcademicRecord(gpa=3.8, sat_total=1450),
    cs_interests=["AI/ML"]
)

agent = CounselorAgent()
analysis = agent.analyze_student_profile(student)
print(analysis['quick_summary'])
```

### Example 2: Running Complete Example
```bash
python examples/local_model_example.py
```

### Example 3: Comparing Models
```bash
# Test with TinyLlama
USE_LOCAL_MODEL=true LOCAL_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0 python main.py

# Test with Phi-2 (better quality)
USE_LOCAL_MODEL=true LOCAL_MODEL=microsoft/phi-2 python main.py
```

## Switching Between Local and API

You can easily switch between local models and OpenAI API:

```bash
# Use OpenAI API
USE_LOCAL_MODEL=false
OPENAI_API_KEY=your_key_here

# Use local model
USE_LOCAL_MODEL=true
LOCAL_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

The application will automatically detect and use the appropriate backend.

## Best Practices

1. **Start Small**: Begin with TinyLlama to test, upgrade if needed
2. **Use GPU**: Much faster inference with CUDA/MPS
3. **Monitor RAM**: Close other apps when using large models
4. **Validate Output**: Local models may be less accurate
5. **Hybrid Approach**: Use local for testing, API for production

## Getting Help

- Check model compatibility on HuggingFace
- Join the community discussions
- Report issues on GitHub
- Check HuggingFace model cards for requirements

## Resources

- **HuggingFace Models**: https://huggingface.co/models
- **Transformers Docs**: https://huggingface.co/docs/transformers
- **PyTorch Installation**: https://pytorch.org/get-started/locally/
- **CUDA Setup**: https://docs.nvidia.com/cuda/

---

**Need more help?** See the main [Usage Guide](USAGE_GUIDE.md) or [Quick Start](QUICKSTART.md).
