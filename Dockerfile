# sifa-mcp — Dockerfile for Glama sandbox build and evaluation
# Glama uses this to run security checks and assign quality/security scores.
#
# Local usage:
#   docker build -t sifa-mcp .
#   docker run sifa-mcp

FROM python:3.11-slim

LABEL org.opencontainers.image.title="sifa-mcp"
LABEL org.opencontainers.image.description="MCP server for portable reputation and skills passports in East Africa"
LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/sifa-mcp"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Gabriel Mahia <contact@aikungfu.dev>"

# Non-root for security
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir sifa-mcp

USER mcpuser

# MCP servers use stdio transport
ENTRYPOINT ["sifa-mcp"]
