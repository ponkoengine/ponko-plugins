# Publishing Ponko plugins

Verified against the linked vendor documentation on 2026-11-09. A repository
marketplace and a vendor's public directory are separate distribution channels.
This repository supplies installable packages and catalogs; it does not imply
vendor approval or an existing public listing.

## Share directly from GitHub

Push the package to `ponkoengine/ponko-plugins`. Claude Code users can add the
repository with `/plugin marketplace add ponkoengine/ponko-plugins`; Codex users
can use `codex plugin marketplace add ponkoengine/ponko-plugins`. Both catalogs
are included. Gemini CLI can install the repository as an extension. Cursor can
load a local copy as described in the README.

This works without waiting for a public-directory listing. Bump `version` in
`plugin.json`, regenerate adapters, validate, and push for each release. Claude
users can run `/plugin update ponko@ponko-plugins`; Codex users can refresh the
marketplace with `codex plugin marketplace upgrade ponko-plugins` and use their
client's plugin update/install controls.

## Claude / Anthropic

For the account shown in the submission portal, submit **`submissions/claude`**
as the plugin directory in `ponkoengine/ponko-plugins`, branch `main`. That folder
is a generated skills-and-documentation bundle with an icon. It contains no
MCP configuration, launcher, maintenance scripts, or tests. It preserves all
four skills; runtime tools are optional and configured separately by the user.
The corresponding ZIP is `dist/ponko-claude-directory-<version>.zip`.

The repository root remains the full local integration for direct installation.
Its Claude MCP command uses a bundled Node.js launcher reading the canonical
`mcp.json`. The portal restricts local MCP servers to Verified organizations;
the launcher fixes command inspection but does not bypass that account gate.
Only submit the root as a local-MCP bundle once the organization qualifies.

1. Run `claude plugin validate submissions/claude --profile directory --strict` and test the plugin in Claude Code
   against a disposable game. Check the current
   [pre-submission requirements](https://code.claude.com/docs/en/plugins/publish).
2. Open [Anthropic's developer portal](https://claude.ai/directory/manage) and
   submit the plugin using its current upload flow. A paid Claude plan and
   the appropriate account/organization permission are required.
3. Supply the requested publisher details, listing text, demonstrations, and
   support information. The skills-only bundle does not run a local server.
   The full plugin's local MCP runs in Claude Code and Cowork, not claude.ai.
4. Resolve portal findings and submit for review. Publish through the portal
   once approved.

Anthropic's directory can reach claude.ai, Cowork, and Claude Code, subject to
component support. The separate `claude-plugins-official` marketplace does not
accept submissions through that directory portal; ask an Anthropic partner
contact about that channel. See the
[official publication instructions](https://code.claude.com/docs/en/plugins/publish).

## ChatGPT / Codex

OpenAI documents a shared public plugin directory for ChatGPT and Codex. The
portable `plugin.json` and `mcp.json` in this repo follow its supported package
layout; the `.codex-plugin` overlay supports compatibility clients. See
[package your plugin](https://developers.openai.com/plugins/build/plugins).

**Ponko currently uses a local stdio MCP server.** A hosted web chat cannot run
`ponko-mcp` on the user's computer by installing a JSON manifest. For the public
local-server path, OpenAI currently requires organization allowlisting:

1. Follow [desktop-only plugin submission](https://developers.openai.com/plugins/deploy/desktop-only).
   Send your Platform organization ID to your OpenAI representative and request
   local MCP submission access. Wait for confirmation.
2. Prepare a submission package that **bundles the MCP executable and its runtime
   dependencies** for the execution platforms you intend to support. The current
   repo ZIP expects `ponko-mcp` on PATH and is a development/distribution archive,
   not a self-contained local-MCP submission. The engine has its own license;
   include the relevant license notices with bundled binaries.
3. In that submission copy, point `mcp.json` at the bundled executable using
   `${PLUGIN_ROOT}`. For example, on a supported Unix platform:

   ```json
   {
     "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
     "mcpServers": {
       "ponko": {
         "type": "stdio",
         "command": "${PLUGIN_ROOT}/bin/ponko-mcp",
         "args": []
       }
     }
   }
   ```

   Preserve executable permissions and test the extracted archive on the target
   platform. Keep this OpenAI submission variant separate from Cursor, which
   does not expand the portable `${PLUGIN_ROOT}` variable in MCP configuration.
4. Keep `extensions.com.openai.requires_local_executor` set to `true` (already
   present). Follow the allowlisted local-MCP upload route, currently **Skills
   only**, including the local MCP config and executable in the initial ZIP.
   That label does not mean dropping the MCP server from the archive.
5. Complete publisher identity verification, listing metadata, review details,
   and test instructions in the submission portal linked by the
   [submission guide](https://developers.openai.com/plugins/deploy/submission).
   Resolve automated findings, submit for review, then publish after approval.

If you want browser/cloud users to control games, that is additional product
work: build an authenticated remote MCP service and a secure connection to the
user's game machine. Do not publish a localhost URL or expose the raw game
control endpoint as a public service. The remote submission route uses public
HTTPS and has separate authentication and domain-verification requirements.

## Cursor

Test the local package, then submit its public repository/package through
[Cursor Marketplace publishing](https://cursor.com/marketplace/publish).
Cursor requires open source plugins and reviews listings and updates. Provide
the listing assets and other fields requested by the portal. See the
[official plugin guide](https://cursor.com/docs/plugins).

## Before any public submission

- Run adapter validation, skill validation, and the MCP smoke check from README.
- Test installation, discovery, reload, and a disposable game session in the
  host you are submitting to. Test a clean machine where practical, including
  missing-binary diagnostics and the installed binary's platform requirements.
- Prepare publisher/contact information, accurate screenshots, support links,
  and review the included official Ponko listing icon,
  and any privacy/terms URLs the selected route requires. This package does not
  invent legal policies or claim a publisher has been verified.
- Document that the plugin can inspect/change local game state and write local
  artifacts. Any data returned by MCP enters the host agent's context and is
  subject to that provider's settings and terms.
- Keep private projects, registry tokens, credentials, and local paths out of
  release archives.
