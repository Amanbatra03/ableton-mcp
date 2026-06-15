#!/usr/bin/env python3
"""Test FastMCP lifecycle hooks."""
from mcp.server.fastmcp import FastMCP
import inspect

app = FastMCP("test")
print("FastMCP.run signature:")
print(inspect.signature(app.run))
print("\nFastMCP methods:")
print([m for m in dir(app) if not m.startswith('_')][:20])
print("\nFastMCP instance attributes:")
print([k for k in app.__dict__.keys() if not k.startswith('_')])
