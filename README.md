![Gloom Core](https://raw.githubusercontent.com/askgloom/.github/refs/heads/main/images/banner.png)

# Gloom Core

<div align="center">

[![Python Version](https://img.shields.io/pypi/pyversions/gloom-core.svg)](https://pypi.org/project/gloom-core/)
[![PyPI version](https://badge.fury.io/py/gloom-core.svg)](https://badge.fury.io/py/gloom-core)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/ask-gloom/gloom-core/actions/workflows/tests.yml/badge.svg)](https://github.com/ask-gloom/gloom-core/actions/workflows/tests.yml)

</div>

Core browser automation framework for Ask Gloom. Provides a high-level interface for browser control, profile management, and automation tasks.

## Features

- Simplified browser automation with intelligent recovery
- Advanced profile management and persistence
- Flexible configuration system
- Screenshot and visual comparison capabilities  
- Automatic driver management and updates
- Comprehensive error handling and logging
- Cross-platform support (Windows, Linux, macOS)

## Installation

```bash
pip install gloom-core
```

## Quick Start

Basic browser automation:
```python
from askgloom.core import Browser

# Initialize and use browser with context manager
with Browser() as browser:
    browser.navigate("https://crate.lol")
    browser.screenshot("homepage.png")
    
    # Get page content
    title = browser.get_element_text("h1.title")
    print(f"Page title: {title}")
```

Custom profile configuration:
```python
from askgloom.core import Profile, Browser

# Create custom profile
profile = Profile("my_profile")
profile.preferences.update({
    "browser": {
        "window_size": {"width": 1920, "height": 1080},
        "user_agent": "Custom User Agent",
        "download_path": "/custom/download/path"
    }
})
profile.save_preferences()

# Use profile with browser
with Browser(profile=profile) as browser:
    browser.navigate("https://crate.lol")
```

Advanced configuration:
```python
from askgloom.core import Config, Browser

# Configure browser behavior
config = Config()
config.set("browser.headless", True)
config.set("automation.retry_attempts", 5)
config.set("automation.screenshot_on_error", True)

# Use configuration
browser = Browser(options=config.get("browser"))
```

## Documentation

For detailed documentation, visit [crate.lol/docs](https://crate.lol/docs)

### Setup

```bash
# Clone the repository
git clone https://github.com/ask-gloom/gloom-core.git
cd gloom-core

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=askgloom

# Run specific test category
pytest tests/test_browser.py -v
```

### Code Quality

```bash
# Format code
black askgloom tests
isort askgloom tests

# Type checking
mypy askgloom

# Lint
flake8 askgloom tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Visit our website: [crate.lol](https://crate.lol)

---

<div align="center">
Made by Ask Gloom
</div>
```
