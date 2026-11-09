#!/usr/bin/env node
// The directory can inspect this bundled entry point. The portable manifest
// remains the source of the installed executable and its arguments.
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { spawn } = require('node:child_process');

try {
  const root = join(__dirname, '..');
  const { mcpServers } = JSON.parse(readFileSync(join(root, 'mcp.json'), 'utf8'));
  const name = process.argv[2] || Object.keys(mcpServers)[0];
  const server = mcpServers[name];
  if (!server || (server.type && server.type !== 'stdio') || !server.command) {
    throw new Error(`No local stdio MCP server configured for ${name}`);
  }
  const child = spawn(server.command, [...(server.args || []), ...process.argv.slice(3)], {
    stdio: 'inherit',
    shell: false,
  });
  child.once('error', (error) => {
    console.error(`Cannot start ${server.command}: ${error.message}. Install the MCP executable and make it available on PATH; see the plugin README.`);
    process.exitCode = 1;
  });
  child.once('exit', (code) => { process.exitCode = code ?? 1; });
  for (const signal of ['SIGINT', 'SIGTERM']) {
    process.on(signal, () => child.kill(signal));
  }
} catch (error) {
  console.error(`Cannot load MCP configuration: ${error.message}`);
  process.exitCode = 1;
}
