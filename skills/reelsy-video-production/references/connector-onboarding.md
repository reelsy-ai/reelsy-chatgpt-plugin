# Reelsy Connector Onboarding

Use this reference when the Reelsy MCP tools are missing from the current task or a Reelsy tool reports an authorization failure. The user-facing flow must stay in plain language; the protocol details below are execution rules for Codex.

## State machine

1. **Ready**: `connector_status` and the required owner-scoped Project tools are callable. Continue the normal Foundation workflow.
2. **Needs authorization**: the tools are callable but return an OAuth/authentication error. Start the Reelsy Connector setup flow, preserve the user's original request, and do not create a paid Job.
3. **Missing from this task**: no Reelsy MCP tools appear in the current tool snapshot. Do not pretend the Connector is unauthenticated and do not open a browser fallback. Start the setup flow, then create one fresh top-level Codex task after verification because the current task cannot hot-load MCP tools. Never create a second handoff task when the task already carries the `reelsy_onboarding_handoff=1` marker; stop and explain that the Codex window must be restarted to refresh its MCP snapshot.

## Setup flow

- Resolve the Codex Desktop bundled CLI from the host environment; never use an unrelated `codex` binary from `PATH` when a bundled path is available.
- Run the bundled CLI's `mcp login reelsy` flow one attempt at a time and let the user complete the normal Reelsy OAuth page if the browser asks for consent.
- Verify the same bundled CLI reports the `reelsy` MCP server enabled with `mcp get reelsy --json` and `mcp list --json`. Do not treat a configured URL alone as proof of authorization.
- When setup succeeds but the current task still lacks Reelsy tools, use the Codex host's thread-creation and navigation capability to create one new top-level task in the same workspace. Put the original natural-language request and the marker `reelsy_onboarding_handoff=1` in the new task's initial message; do not ask the user to repeat it or type a technical “continue” command.
- In a task carrying `reelsy_onboarding_handoff=1`, do not run `mcp login reelsy` again and do not create another task. If Reelsy tools are still absent, stop before any browser or Project action and tell the user: “The Reelsy connection is complete, but this Codex window has not refreshed its tools yet. Restart Codex, then reopen the Reelsy task. Your original request will remain available.”
- The setup task is complete only after it reports the new task handoff. It must not generate video, import private media, modify a Timeline, or spend credits.
- If the host cannot run the bundled CLI or create a new task, tell the user in plain language that Reelsy connection needs to be completed in a newly opened Reelsy task. Never claim the current task can continue with tools it does not have.

## User-facing language

- Say: “The Reelsy connection is not ready yet. I will complete the connection first, then continue your video task automatically.”
- After a successful setup handoff, say: “The connection is complete. I have moved you to a new Reelsy production task. Next, I will open the Canvas and show the expected cost.”
- Do not ask users to mention MCP, Skills, OAuth scopes, Project IDs, URLs, or internal tool names.
