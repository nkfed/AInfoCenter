#!/usr/bin/env python3
"""
DuckDuckGo Web Search Tool using ddgs library
Install: pip install ddgs
"""

import sys
import json

try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        print(json.dumps({
            'error': True,
            'message': 'Missing dependency: pip install ddgs',
            'install_command': 'pip install ddgs'
        }))
        sys.exit(1)


def search_duckduckgo(query: str, num_results: int = 5):
    """
    Search DuckDuckGo using official library
    
    Args:
        query: Search query string
        num_results: Number of results to return (1-10)
    
    Returns:
        List of result dictionaries
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
            
            # Format results
            formatted = []
            for i, result in enumerate(results, 1):
                formatted.append({
                    'position': i,
                    'title': result.get('title', 'No title'),
                    'url': result.get('href', result.get('link', '')),
                    'snippet': result.get('body', result.get('description', ''))
                })
            
            return formatted
    
    except Exception as e:
        return [{
            'error': True,
            'message': f'Search failed: {str(e)}',
            'query': query
        }]


def main():
    """Main entry point for CLI usage"""
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Missing query parameter',
            'usage': 'duckduckgo_search.py "query" [num_results]'
        }))
        sys.exit(1)
    
    query = sys.argv[1]
    num_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    # Validate
    if num_results < 1 or num_results > 10:
        num_results = 5
    
    results = search_duckduckgo(query, num_results)
    
    # Output JSON
    output = {
        'query': query,
        'num_results': len(results),
        'results': results
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
