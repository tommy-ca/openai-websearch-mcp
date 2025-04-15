# Configuring Your MCP Client for OpenAI WebSearch

This document explains how to configure any Model Context Protocol (MCP) compatible client to use the `openai-websearch-mcp` server.

## Prerequisites

1.  **OpenAI API Key:** You need an API key from OpenAI. You can obtain one from the [OpenAI Platform](https://platform.openai.com/).
2.  **Server Installation:** Ensure the `openai-websearch-mcp` server is installed in an environment accessible to your MCP client. You can install it using pip:
    ```bash
    pip install openai-websearch-mcp
    ```
    Alternatively, if using `uv`, ensure it's available via `uvx`.

## Client Configuration

You need to add this server to your MCP client's configuration. The exact method depends on your client, but generally involves defining a server entry that specifies how to run the server and provides the necessary environment variables.

**Key Configuration Parameters:**

- **Server Name:** Typically `openai-websearch-mcp` (or any name you prefer).
- **Command:** The command to execute the server.
  - If installed via pip: `python`
  - If using `uvx`: `uvx`
- **Arguments:** Arguments passed to the command.
  - If installed via pip: `["-m", "openai_websearch_mcp"]`
  - If using `uvx`: `["openai-websearch-mcp"]`
- **Environment Variables (`env`):**
  - `OPENAI_API_KEY`: Your OpenAI API key (e.g., `"sk-..."`).

**Example Configuration (Conceptual JSON):**

_Using standard Python installation:_

```json
{
  "mcpServers": {
    "openai-websearch-mcp": {
      "command": "python",
      "args": ["-m", "openai_websearch_mcp"],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
    // ... other servers
  }
}
```

_Using `uvx`:_

```json
{
  "mcpServers": {
    "openai-websearch-mcp": {
      "command": "uvx",
      "args": ["openai-websearch-mcp"],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
    // ... other servers
  }
}
```

**Note:** Replace `"your-api-key-here"` with your actual OpenAI API key. Consult your specific MCP client's documentation for the exact configuration format (e.g., `settings.json`, `.yaml` file).

## Available Tool

Once configured, your client can utilize the following tool provided by this server:

- **`web_search`**: Performs a web search using OpenAI.
  - **Arguments:**
    - `type` (string, required): `web_search_preview`
    - `search_context_size` (string, optional): Guidance on context usage (`low`, `medium`, `high`). Default: `medium`.
    - `user_location` (object, optional): User's approximate location (`city`, `country`, `region`, `timezone`).

Refer to the main `README.md` for more details on the tool arguments.
