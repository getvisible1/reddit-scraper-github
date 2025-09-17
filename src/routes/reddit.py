from flask import Blueprint, jsonify, request
import requests
import time
from datetime import datetime
import re
from urllib.parse import urlparse
import random

reddit_bp = Blueprint('reddit', __name__)

# List of user agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]

def extract_subreddit_from_url(url):
    """Extract subreddit name from Reddit URL"""
    # Handle various Reddit URL formats
    patterns = [
        r'reddit\.com/r/([^/]+)',
        r'old\.reddit\.com/r/([^/]+)',
        r'www\.reddit\.com/r/([^/]+)',
        r'^r/([^/]+)',
        r'^([^/]+)$'  # Just subreddit name
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def get_proxy_dict(proxy_string):
    """Convert proxy string to requests proxy dict"""
    if not proxy_string:
        return None
    
    try:
        # Handle different proxy formats
        # Format 1: username:password@host:port
        # Format 2: host:port
        # Format 3: http://username:password@host:port
        # Format 4: http://host:port
        
        if '://' not in proxy_string:
            # No protocol specified, add http://
            if '@' in proxy_string:
                # Authenticated proxy: username:password@host:port
                proxy_string = f'http://{proxy_string}'
            else:
                # Simple proxy: host:port
                proxy_string = f'http://{proxy_string}'
        
        return {
            'http': proxy_string,
            'https': proxy_string
        }
    except Exception:
        return None

def scrape_subreddit_json(subreddit, sort='hot', limit=100, timeframe='all', after=None, proxy=None, delay=2):
    """
    Scrape Reddit posts using the JSON endpoint method with proxy support
    
    Args:
        subreddit: Name of the subreddit
        sort: 'hot', 'new', 'top', 'rising'
        limit: Number of posts (max 100)
        timeframe: 'hour', 'day', 'week', 'month', 'year', 'all'
        after: Token for pagination
        proxy: Proxy string (e.g., 'ip:port' or 'http://ip:port')
        delay: Delay between requests in seconds
    """
    # Build the URL
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json"
    
    # Rotate user agents to avoid detection
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Add parameters
    params = {
        'limit': min(limit, 100),  # Reddit max is 100
        't': timeframe
    }
    
    if after:
        params['after'] = after
    
    # Setup proxy
    proxies = get_proxy_dict(proxy)
    
    try:
        # Add delay to avoid rate limiting
        if delay > 0:
            time.sleep(delay)
        
        response = requests.get(
            url, 
            headers=headers, 
            params=params, 
            proxies=proxies,
            timeout=30,
            verify=True
        )
        response.raise_for_status()
        
        data = response.json()
        posts = []
        
        # Extract post data
        for child in data['data']['children']:
            post = child['data']
            posts.append({
                'id': post['id'],
                'title': post['title'],
                'author': post.get('author', '[deleted]'),
                'created_utc': datetime.fromtimestamp(post['created_utc']).isoformat(),
                'score': post['score'],
                'num_comments': post['num_comments'],
                'url': post['url'],
                'selftext': post.get('selftext', ''),
                'subreddit': post['subreddit'],
                'permalink': f"https://reddit.com{post['permalink']}",
                'is_video': post.get('is_video', False),
                'over_18': post.get('over_18', False),
                'domain': post.get('domain', ''),
                'upvote_ratio': post.get('upvote_ratio', 0)
            })
        
        # Get pagination token
        after_token = data['data'].get('after')
        
        return {
            'success': True,
            'posts': posts,
            'after': after_token,
            'count': len(posts)
        }
        
    except requests.exceptions.ProxyError as e:
        return {
            'success': False,
            'error': f"Proxy error: {str(e)}. Please check your proxy settings.",
            'posts': [],
            'after': None,
            'count': 0
        }
    except requests.exceptions.Timeout as e:
        return {
            'success': False,
            'error': f"Request timeout: {str(e)}. Try increasing the delay or using a different proxy.",
            'posts': [],
            'after': None,
            'count': 0
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f"Request error: {str(e)}. Reddit may be blocking your IP. Try using a proxy.",
            'posts': [],
            'after': None,
            'count': 0
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Parsing error: {str(e)}",
            'posts': [],
            'after': None,
            'count': 0
        }

@reddit_bp.route('/scrape', methods=['POST'])
def scrape_reddit():
    """Main endpoint for scraping Reddit posts"""
    try:
        data = request.json
        
        # Validate input
        if not data or 'input' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing input parameter'
            }), 400
        
        user_input = data['input'].strip()
        if not user_input:
            return jsonify({
                'success': False,
                'error': 'Input cannot be empty'
            }), 400
        
        # Extract subreddit name
        subreddit = extract_subreddit_from_url(user_input)
        if not subreddit:
            return jsonify({
                'success': False,
                'error': 'Could not extract subreddit name from input'
            }), 400
        
        # Get optional parameters
        sort = data.get('sort', 'hot')
        limit = min(int(data.get('limit', 25)), 100)
        timeframe = data.get('timeframe', 'all')
        pages = min(int(data.get('pages', 1)), 10)  # Limit to 10 pages max
        proxy = data.get('proxy', '').strip()  # Proxy string
        delay = max(float(data.get('delay', 2)), 1)  # Minimum 1 second delay
        
        # Validate sort parameter
        valid_sorts = ['hot', 'new', 'top', 'rising']
        if sort not in valid_sorts:
            sort = 'hot'
        
        # Validate timeframe parameter
        valid_timeframes = ['hour', 'day', 'week', 'month', 'year', 'all']
        if timeframe not in valid_timeframes:
            timeframe = 'all'
        
        all_posts = []
        after = None
        total_scraped = 0
        
        # Scrape multiple pages if requested
        for page in range(pages):
            result = scrape_subreddit_json(
                subreddit=subreddit,
                sort=sort,
                limit=limit,
                timeframe=timeframe,
                after=after,
                proxy=proxy if proxy else None,
                delay=delay
            )
            
            if not result['success']:
                if page == 0:  # If first page fails, return error
                    return jsonify(result), 500
                else:  # If subsequent page fails, break and return what we have
                    break
            
            all_posts.extend(result['posts'])
            total_scraped += result['count']
            after = result['after']
            
            # If no more posts available, break
            if not after or result['count'] == 0:
                break
            
            # Be respectful with rate limiting
            if page < pages - 1:  # Don't sleep after last page
                time.sleep(1)
        
        return jsonify({
            'success': True,
            'subreddit': subreddit,
            'posts': all_posts,
            'total_count': total_scraped,
            'pages_scraped': min(page + 1, pages),
            'sort': sort,
            'timeframe': timeframe
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        }), 500

@reddit_bp.route('/validate', methods=['POST'])
def validate_input():
    """Validate Reddit URL or subreddit name"""
    try:
        data = request.json
        
        if not data or 'input' not in data:
            return jsonify({
                'valid': False,
                'error': 'Missing input parameter'
            }), 400
        
        user_input = data['input'].strip()
        if not user_input:
            return jsonify({
                'valid': False,
                'error': 'Input cannot be empty'
            })
        
        subreddit = extract_subreddit_from_url(user_input)
        
        if subreddit:
            return jsonify({
                'valid': True,
                'subreddit': subreddit,
                'input_type': 'url' if '/' in user_input else 'name'
            })
        else:
            return jsonify({
                'valid': False,
                'error': 'Could not extract subreddit name from input'
            })
            
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f"Validation error: {str(e)}"
        }), 500


@reddit_bp.route('/export-text', methods=['POST'])
def export_text():
    """Export scraped data as readable text format for NotebookLM"""
    try:
        data = request.json
        
        if not data or 'posts' not in data:
            return jsonify({
                'success': False,
                'error': 'No data provided for export'
            }), 400
        
        posts = data['posts']
        subreddit = data.get('subreddit', 'Unknown')
        total_count = data.get('total_count', len(posts))
        
        # Create readable text format
        text_content = f"Reddit Posts from r/{subreddit}\n"
        text_content += f"Total Posts: {total_count}\n"
        text_content += f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        text_content += "=" * 80 + "\n\n"
        
        for i, post in enumerate(posts, 1):
            text_content += f"POST #{i}\n"
            text_content += f"Title: {post['title']}\n"
            text_content += f"Author: u/{post['author']}\n"
            text_content += f"Score: {post['score']} points\n"
            text_content += f"Comments: {post['num_comments']}\n"
            text_content += f"Upvote Ratio: {post.get('upvote_ratio', 0):.0%}\n"
            text_content += f"Posted: {post['created_utc']}\n"
            text_content += f"URL: {post['url']}\n"
            text_content += f"Reddit Link: {post['permalink']}\n"
            
            # Add post content if available
            if post.get('selftext') and post['selftext'].strip():
                text_content += f"Content:\n{post['selftext']}\n"
            
            text_content += "-" * 60 + "\n\n"
        
        return jsonify({
            'success': True,
            'text_content': text_content,
            'filename': f"reddit_{subreddit}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Export error: {str(e)}"
        }), 500

