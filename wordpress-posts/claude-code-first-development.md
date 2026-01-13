# Claude Code First Development: Building AI-Operable Systems

Most developers think about AI coding assistants as tools that help you write code faster. But there's a more interesting question: **how do you architect your systems so an AI can operate them?**

I've been running production applications for years. The traditional approach is to build admin dashboards - React UIs, Django admin, custom internal tools. You click around, run queries, check metrics, send emails to users. It works, but it's slow and requires constant context-switching.

Here's the insight: Claude Code is a command-line interface. It can run shell commands, read output, and take action based on what it sees. If you build your admin tooling as CLI commands and APIs instead of web UIs, Claude Code becomes your admin interface.

Instead of clicking through dashboards to debug a production issue, you tell Claude: "Find all users who signed up in the last 24 hours but haven't verified their email, and show me their signup source." It runs the commands, parses the output, and gives you the answer.

This is Claude Code First Development - designing your production infrastructure to be AI-operable.

## The Architecture

There are three layers to this:

**1. Admin API Layer**

Your application exposes authenticated API endpoints for admin operations. Not public APIs - internal endpoints that require admin credentials. These give you programmatic access to:

- User data (lookups, activity, state)
- System metrics (signups, WAU, churn, error rates)
- Operations (send emails, trigger jobs, toggle features, issue refunds)

**2. CLI Tooling**

Command-line tools that wrap those APIs. Claude Code can invoke these directly:

```bash
./admin users search --email "foo@example.com"
./admin metrics signups --since "7 days ago"
./admin jobs trigger welcome-sequence --user-id 12345
./admin logs errors --service api --last 1h
```

**3. Credential Management**

The CLI tools handle authentication - reading tokens from environment variables or config files. Claude Code doesn't need to know how auth works, it just runs commands.

## Building the CLI Tools

The great thing about AI Developer Agents is that you don't need to code these tools yourself.

```
Based on the data models in this application, build a command line cli tool and claude code skill to
use it. the cli tool should authticate with admin-only scoped API endpoints to be able to execude basic crud
capabilities, report on activitiy metrics, generate reports and provide insights that help control the application
in the production environment without relying on a administrator dashboard.
Build authentication into the cli tool to save credentials securely.
examples:
./admin-cli users list
./admin-cli users add user@example.com --sent-invite
./admin-cli reports DAU
./admin-cli error-log
```

## Level up

Here are prompts you can give Claude Code to build out this infrastructure for your specific application:

### Initial CLI Scaffold

```
Create a Python CLI tool using Click for admin operations on my [Django/FastAPI/Express]
application. The CLI should:
- Read API credentials from environment variables (ADMIN_API_URL, ADMIN_API_TOKEN)
- Have command groups for: users, metrics, logs, jobs
- Output JSON by default with an option for table format
- Include proper error handling for API failures

Start with the scaffold and user search command.
```

### Adding User Management

```
Add these user management commands to my admin CLI:

1. users search - find users by email, name, or ID
2. users get <id> - get full user profile including subscription status
3. users recent - list signups from last N hours/days with filters for source and verification status
4. users activity <id> - show recent actions for a user

Each command should have sensible defaults and output JSON.
```

### Adding Metrics Commands

```
Add metrics commands to my admin CLI that query our analytics:

1. metrics signups - signup counts grouped by day/week with source breakdown
2. metrics wau - weekly active users over time
3. metrics churn - churn rate and churned user counts
4. metrics health - overall system health (error rates, response times, queue depths)
5. metrics revenue - MRR, new revenue, churned revenue (if applicable)

Include --since flags for time windows and sensible output formatting.
```

### Adding Log Access

```
Add log viewing commands to my admin CLI:

1. logs errors - recent errors across services with filtering
2. logs user <id> - all log entries related to a specific user
3. logs request <id> - trace a specific request through the system
4. logs search --pattern "..." - search logs by pattern

Format output for terminal readability - timestamps, service names, messages on separate lines.
```

### Adding Actions/Jobs

```
Add commands to trigger admin actions:

1. jobs list - show available background jobs
2. jobs trigger <name> - trigger a job with optional parameters
3. jobs status <id> - check job status
4. email send <user_id> <template> - send a specific email
5. email templates - list available templates

Include --dry-run flags where destructive or user-facing operations are involved.
```

### Building the API Endpoints

```
Create admin API endpoints for my [framework] application to support the admin CLI:

1. GET /admin/users/search?email=&id=
2. GET /admin/users/<id>
3. GET /admin/users/<id>/activity
4. GET /admin/users/recent?since=&source=&verified=
5. GET /admin/metrics/signups?since=&group_by=
6. GET /admin/metrics/wau
7. GET /admin/logs?service=&level=&since=
8. POST /admin/jobs/trigger

All endpoints should require Bearer token authentication. Use our existing User and
Activity models. Return JSON responses.
```

## Making Tools Work Well With Claude Code

Claude Code reads text output. The better your tools format their output, the more effectively Claude can interpret and act on the results.

### Principle 1: JSON for Data, Text for Logs

Return structured data as JSON - Claude parses it accurately:

```bash
$ ./admin users get 12345
{
  "id": 12345,
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z",
  "subscription": "pro",
  "verified": true
}
```

But format logs for human readability - Claude understands context better:

```bash
$ ./admin logs errors --last 1h
[2024-01-15 10:45:23] api: Failed to process payment for user 12345: card_declined
[2024-01-15 10:47:01] worker: Job send_welcome_email failed: SMTP timeout
[2024-01-15 10:52:18] api: Rate limit exceeded for IP 192.168.1.1
```

### Principle 2: Include Context in Output

When something fails, include enough context for Claude to suggest fixes:

```bash
$ ./admin jobs trigger welcome-email --user-id 99999
{
  "error": "user_not_found",
  "message": "No user with ID 99999",
  "suggestion": "Use 'admin users search' to find the correct user ID"
}
```

### Principle 3: Support Filtering at the Source

Don't make Claude grep through huge outputs. Add filters to your commands:

```bash
# Bad - returns everything, Claude has to parse
$ ./admin logs errors --last 24h

# Good - filtered at the API level
$ ./admin logs errors --last 24h --service api --level error --limit 20
```

### Principle 4: Dry Run Everything Destructive

Any command that modifies state should support `--dry-run`:

```bash
$ ./admin email send 12345 password-reset --dry-run
{
  "would_send": true,
  "recipient": "user@example.com",
  "template": "password-reset",
  "subject": "Reset your password",
  "preview_url": "https://admin.yourapp.com/email/preview/abc123"
}
```

This lets Claude verify actions before executing them, and lets you review what it's about to do.

### Principle 5: Exit Codes Matter

Use proper exit codes so Claude knows when commands fail:

```python
@users.command()
def get(user_id: str):
    try:
        result = api_request("GET", f"/admin/users/{user_id}")
        output(result)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            click.echo(f"User {user_id} not found", err=True)
            raise SystemExit(1)
        raise
```

** Note ** When the commands crash out - the app can immediate fix itself!

## Integrating With Claude Code Skills

Claude Code supports Skills - custom commands that extend its capabilities. You can create a Skill that wraps your admin CLI and provides context about your specific system.

Just tell Claude code to document your new cli into a skill:

```
Create a claude code skill to document how to use admin-cli, then give me examples of what I can do with this new skill.
```

Now Claude Code has context about your admin tools and can use them appropriately.

## MCP Tool Integration

For deeper integration, you can expose your admin API as an MCP (Model Context Protocol) server. This lets Claude call your admin functions directly as tools rather than shelling out to CLI commands. (so it can be used by more people than terminal centric administrators)

## Security Considerations

A few things to keep in mind:

**1. Scope your tokens.** Create admin API tokens with the minimum permissions needed. Don't use your personal account credentials.

**2. Audit everything.** Log every admin API call with the token used, timestamp, and parameters. You want a trail of what Claude (or you) did.

**3. Require confirmation for destructive operations.** Either use `--dry-run` flags or build confirmation into your workflow. Claude should show you what it's about to do before doing it.

**4. Separate read and write access.** Consider having read-only tokens for investigation and separate tokens for operations that modify state.

**5. Don't expose production databases directly.** Always go through your application layer. This gives you validation, audit logging, and the ability to revoke access.

## Putting It Together

Here's what a typical debugging session looks like with this setup:

```
You: "Users are complaining about not receiving welcome emails. Investigate."

Claude: Let me check recent signups and email job status.

$ ./admin users recent --since 24h --verified
[shows recent verified users]

$ ./admin logs errors --service email --last 24h
[2024-01-15 08:15:00] email: SMTP connection timeout to smtp.sendgrid.net
[2024-01-15 08:15:01] email: Failed to send welcome-email to user 12340
[2024-01-15 08:15:01] email: Failed to send welcome-email to user 12341
...

Looks like the email service had SMTP connection issues starting at 8:15 AM.
Let me check how many users were affected:

$ ./admin metrics health
{
  "email_queue_depth": 847,
  "email_error_rate": 0.94,
  ...
}

There are 847 emails stuck in the queue with a 94% error rate. The issue appears
to be SMTP connectivity. Once that's resolved, you may want to replay the failed
jobs. I can show you the affected users if you'd like to manually trigger their
welcome emails.
```

This is the power of Claude Code First Development. You're not clicking through dashboards or writing one-off SQL queries. You're having a conversation with an AI that has direct access to your systems through well-designed tooling.

Build the CLI tools. Expose the APIs. Give Claude the access it needs to help you operate your systems. That's the future of production debugging.
