# Ponko Engine

The `ponko` MCP server connects to local Ponko games using the
`ponko-mcp` executable. Use the matching workflow as needed:

- [Setup and connection troubleshooting](skills/ponko-setup/SKILL.md)
- [Basic engine guidance and documentation](skills/ponko/SKILL.md)
- [Inspecting and debugging a game](skills/ponko-inspect/SKILL.md)
- [Measuring performance](skills/ponko-profile/SKILL.md)

Select a game with `list_instances` and pass its `instance` id explicitly.
When launching, pass the game's absolute Cargo project directory as `cwd`;
the extension install directory is not the game directory. Follow the schemas
of the tools exposed by the connected server.
