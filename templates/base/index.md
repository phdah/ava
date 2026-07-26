# Base Project Template

This directory defines the initial filesystem content copied into a project by `ava init`.

## Contents

- [Agent router](AGENTS.md) - Root entry point that selects and loads the role best matching a request.
- [Inbox](inbox/) - Intake and lifecycle for untrusted or unclassified source material.
- [Knowledge](knowledge/) - Minimal root for trusted, durable context that grows from real information.
- [Roles](roles/) - Role registry and built-in project roles.
- [Workflows](workflows/) - Registry for reusable procedures that activate one primary role.
- [Shared context](shared/) - Project-wide instructions and context shared across roles and workflows.
