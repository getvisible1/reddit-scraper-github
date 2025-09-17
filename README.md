# Reddit Scraper Pro 🚀

A powerful, feature-rich Reddit scraping tool with advanced anti-detection capabilities and dual export formats. Perfect for data analysis, research, and feeding data into AI tools like NotebookLM.

![Reddit Scraper Pro](https://img.shields.io/badge/Reddit-Scraper-orange?style=for-the-badge&logo=reddit)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask)

## ✨ Features

### 🔧 Core Functionality
- **Easy-to-use Web Interface**: Modern, responsive design
- **Multiple Input Formats**: Reddit URLs or subreddit names
- **Flexible Sorting**: Hot, New, Top, Rising posts
- **Time Filtering**: All time, past year, month, week, day, hour
- **Bulk Scraping**: Up to 100 posts per page, up to 10 pages

### 🔒 Anti-Detection Features
- **Authenticated Proxy Support**: Full support for `username:password@host:port` format
- **User Agent Rotation**: Automatically rotates between 8 different browser user agents
- **Request Delay Control**: Adjustable delays (1-5 seconds) between requests
- **Enhanced Headers**: Realistic browser headers to avoid detection
- **Smart Error Handling**: Specific error messages for different failure scenarios

### 📊 Export Options
- **JSON Export**: Complete structured data for programmatic use
- **Text Export**: Human-readable format perfect for NotebookLM and AI analysis
- **Real-time Progress**: Live progress indicators and status updates

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/reddit-scraper-pro.git
cd reddit-scraper-pro
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python src/main.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

## 🔧 Configuration

### Basic Usage
1. Enter a subreddit name (e.g., `python`) or full Reddit URL
2. Configure sorting and filtering options
3. Click "Start Scraping"
4. Export results as JSON or Text

### Proxy Configuration

**Supported Formats:**
- `username:password@host:port` (Authenticated)
- `host:port` (Simple)
- `http://username:password@host:port`
- `http://host:port`

**Example:**
```
getvisible:lRNnu9WhvpKM2gpz@proxy.packetstream.io:31112
```

### Request Delay Settings
- **1 second**: Fast but higher detection risk
- **2 seconds**: Default balanced setting
- **3 seconds**: Safer for most use cases
- **5 seconds**: Very safe, slower scraping

## 📋 Export Formats

### JSON Export
Complete structured data including:
- Post metadata (title, author, score, comments)
- Timestamps and URLs
- Full post content
- Upvote ratios and engagement metrics

### Text Export (NotebookLM Ready)
Human-readable format featuring:
- Clear post separation with dividers
- All metadata in readable format
- Full post content when available
- Perfect for AI analysis tools

**Sample Text Format:**
```
Reddit Posts from r/python
Total Posts: 25
Exported on: 2025-09-17 19:49:27
================================================================================

POST #1
Title: Amazing Python Library for Data Science
Author: u/pythondev
Score: 156 points
Comments: 23
Upvote Ratio: 94%
Posted: 2025-09-17T10:30:00
URL: https://github.com/example/library
Reddit Link: https://reddit.com/r/python/comments/xyz123/
Content:
Just discovered this incredible library that makes data analysis so much easier...
------------------------------------------------------------
```

## 🐳 Docker Deployment

### Using Docker
```bash
# Build the image
docker build -t reddit-scraper-pro .

# Run the container
docker run -p 5000:5000 reddit-scraper-pro
```

### Using Docker Compose
```bash
docker-compose up -d
```

## 🌐 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

### Using Systemd (Linux)
Create `/etc/systemd/system/reddit-scraper.service`:
```ini
[Unit]
Description=Reddit Scraper Pro
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/path/to/reddit-scraper-pro
Environment=PATH=/path/to/reddit-scraper-pro/venv/bin
ExecStart=/path/to/reddit-scraper-pro/venv/bin/gunicorn --bind 0.0.0.0:5000 src.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable reddit-scraper
sudo systemctl start reddit-scraper
```

### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔍 API Endpoints

### Scraping
- `POST /api/reddit/scrape` - Start scraping process
- `POST /api/reddit/validate` - Validate subreddit input

### Export
- `POST /api/reddit/export-text` - Export as readable text

## 🛠️ Development

### Project Structure
```
reddit-scraper-pro/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── routes/
│   │   ├── reddit.py        # Reddit scraping routes
│   │   └── user.py          # User management routes
│   └── static/
│       └── index.html       # Frontend application
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🔒 Proxy Providers

### Recommended Services
- **PacketStream**: Residential proxies with authentication
- **Bright Data**: Enterprise-grade proxy solutions
- **Smartproxy**: Reliable residential and datacenter proxies
- **ProxyMesh**: Rotating proxy service

### Free Proxy Lists
- Use with caution as they're less reliable
- Higher chance of being blocked
- No authentication support

## 🚨 Error Handling

The application provides specific error messages:
- **Proxy errors**: Check proxy format and availability
- **Timeout errors**: Increase request delay or try different proxy
- **Reddit blocking**: Use proxy or reduce request frequency
- **Invalid input**: Clear validation messages for incorrect inputs

## 📊 Performance Tips

### Optimal Settings
- Use 2-3 second delays for balanced performance
- Start with 25 posts per page for testing
- Use residential proxies for better success rates
- Monitor for rate limiting and adjust accordingly

### Troubleshooting
1. **Slow scraping**: Reduce request delay
2. **Getting blocked**: Use proxy or increase delays
3. **Proxy errors**: Verify proxy credentials and format
4. **No results**: Check subreddit name and availability

## 📝 Legal Notice

This tool is for educational and research purposes only. Please:
- Respect Reddit's Terms of Service
- Use reasonable rate limits
- Consider the impact on Reddit's servers
- Comply with applicable laws and regulations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies
5. Make your changes
6. Test thoroughly
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter issues:
1. Check the error message in the application
2. Verify proxy configuration if using one
3. Try increasing request delays
4. Test with different subreddits
5. Open an issue on GitHub with detailed information

## 🙏 Acknowledgments

- Built with Flask and modern web technologies
- Inspired by the need for reliable Reddit data extraction
- Thanks to the open-source community for tools and libraries

---

**Reddit Scraper Pro** - Professional Reddit data extraction with anti-detection features and AI-ready export formats.

Made with ❤️ for the data science and research community.

