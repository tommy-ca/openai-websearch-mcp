# OpenAI WebSearch MCP Server

This MCP server provides access to OpenAI's websearch functionality through the Model Context Protocol. It allows AI assistants to search the web during conversations with users, providing up-to-date information that may not be available in the assistant's training data.

## Available Tools

- `web_search` - Call openai websearch as tool.
  - Required arguments:
    - `type` (string): web_search_preview
    - `search_context_size` (string): High level guidance for the amount of context window space to use for the search. One of low, medium, or high. medium is the default.
    - `user_location` (object or null)
      - `type` (string): The type of location > approximation. Always approximate.
      - `city` (string): Free text input for the city of the user, e.g. San Francisco.
      - `country` (string): The two-letter ISO country code of the user, e.g. US.
      - `region` (string): Free text input for the region of the user, e.g. California.
      - `timezone` (string): The IANA timezone of the user, e.g. America/Los_Angeles.

## Installation and Configuration

You will need to configure your MCP client to run this server. This typically involves specifying the command to execute the server and providing your OpenAI API key as an environment variable (`OPENAI_API_KEY`).

Example using `uvx` (ensure `uvx` is installed):

```json
"mcpServers": {
  "openai-websearch-mcp": {
    "command": "uvx",
    "args": ["openai-websearch-mcp"],
    "env": {
        "OPENAI_API_KEY": "your-api-key-here"
    }
  }
}
```

Example using standard Python installation (install with `pip install openai-websearch-mcp`):

```json
"mcpServers": {
  "openai-websearch-mcp": {
    "command": "python",
    "args": ["-m", "openai_websearch_mcp"],
    "env": {
        "OPENAI_API_KEY": "your-api-key-here"
    }
  }
}
```

Refer to your specific MCP client's documentation for details on adding context servers. You can obtain an OpenAI API key from [openai's open platform](https://platform.openai.com/).

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```bash
npx @modelcontextprotocol/inspector uvx openai-websearch-mcp
```
