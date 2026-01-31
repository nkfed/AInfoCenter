---
name: duckduckgo-search
description: Search the web using DuckDuckGo. Free, no API key required. Use when you need to find information on the internet, get current news, or answer questions requiring web search.
metadata: {"openclaw": {"emoji": "🔍", "always": true}}
---

# DuckDuckGo Web Search

Search the web using DuckDuckGo's HTML interface. No API key required, completely free.

## When to use

- User asks to search the web
- Need current information not in your knowledge base
- Questions like "what is...", "find information about...", "search for..."
- News, weather, current events
- Technical documentation lookup
- Any query requiring fresh web data

## Usage

Call the `duckduckgo_search` tool with a search query:

```typescript
duckduckgo_search({
  query: "latest news about AI",
  num_results: 5
})
```

## Parameters

- `query` (required): Search query string
- `num_results` (optional): Number of results to return (1-10, default: 5)

## Output

Returns structured search results with:
- Title
- URL
- Snippet (description)
- Position in results

## Examples

**Example 1: Simple search**
```
User: "Search for weather in Sambir"
Assistant calls: duckduckgo_search({ query: "weather Sambir Ukraine" })
```

**Example 2: Technical documentation**
```
User: "Find documentation for Node.js fs module"
Assistant calls: duckduckgo_search({ query: "Node.js fs module documentation", num_results: 3 })
```

**Example 3: Current news**
```
User: "What's happening with OpenAI today?"
Assistant calls: duckduckgo_search({ query: "OpenAI news today" })
```

## Notes

- DuckDuckGo respects privacy (no tracking)
- Results may differ slightly from Google
- Rate limiting: reasonable requests only (avoid rapid-fire searches)
- HTML parsing may occasionally fail if DuckDuckGo changes their format

## Limitations

- No image search (text only)
- No advanced search operators
- Results quality depends on DuckDuckGo's index
