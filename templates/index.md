# Generated Project Templates

Files under [`base/`](base/) define the initial filesystem content copied into a project by `ava init`.

- [Agent router](base/AGENTS.md) - Root entry point that automatically selects and loads the role best matching the user's request.
- [Role registry](base/roles/index.md) - Registry used by the router to discover and select available roles.
- [Role Generator](base/roles/role-generator/) - Built-in role for creating and maintaining project roles through an agent.

Repository-development instructions under `/internal/` are not part of generated project templates.
