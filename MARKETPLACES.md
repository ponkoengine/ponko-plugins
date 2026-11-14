# Publishing Ponko plugins

Verified against the linked vendor documentation on 2026-11-09; Claude
directory findings updated 2026-11-14. A repository
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

Submit the repository root (`.`) in `ponkoengine/ponko-plugins`, branch `main`.
It is the same full package used for direct installation: all four skills,
documentation, the official icon, and a local MCP server entry. The release
archive is `dist/ponko-<version>.zip`.

`.mcp.json` runs the user's installed `ponko-mcp` directly (generated from the
canonical `mcp.json`). The plugin bundles no scripts, hooks, or executables, and
it reads no credentials: `ponko-mcp` needs no API key or token.

What to expect from the directory's review, for an organization that is not
Verified:

| Finding | Status |
| --- | --- |
| Scripts the validator couldn't follow; files outside the allowed types | Fixed in 0.1.3: the Node.js launcher was removed. |
| Uses a credential from the user's machine | Nothing in the plugin reads or sends one. If the hold remains, reply that the only command is the user's own `ponko-mcp`, which talks to games on `localhost` only. |
| Image or font file that the plugin's code could run | `assets/icon.png` is only the listing icon; nothing runs it. It stays held until a reviewer confirms that. |
| Field from another tool's manifest (`icon`) | No action needed; the directory uses it for the listing. |
| agent-plugins manifest detected (root `plugin.json`) | Informational; it serves other hosts. |
| Local MCP server not on claude.ai; accepted only from Verified organizations | Informational for now. If the directory starts refusing local MCP servers from unverified organizations, verify the organization, or submit a copy without `.mcp.json` (skills only; users then run `claude mcp add --scope user ponko -- ponko-mcp`). |

1. Run `claude plugin validate . --profile directory --strict` and test the plugin in Claude Code
   against a disposable game. Check the current
   [pre-submission requirements](https://code.claude.com/docs/en/plugins/publish).
2. Open [Anthropic's developer portal](https://claude.ai/directory/manage) and
   submit the plugin using its current upload flow. A paid Claude plan and
   the appropriate account/organization permission are required.
3. Supply the requested publisher details, listing text, demonstrations, and
   support information. The plugin's local MCP runs in Claude Code and Cowork, not claude.ai.
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
