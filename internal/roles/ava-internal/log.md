# Ava Internal Maintainer Update Log

This log records major conceptual changes to the Ava Internal Maintainer role. It does not record routine edits or replace Git history.

## 2026-07-26

* **Scoped specialist delegation**: Allowed the Ava Internal Maintainer to load one matching role from the generated base catalog as specialist instructions for a bounded subtask while remaining the single active primary role.
* **Delegation boundaries**: Limited effective authority to shared capabilities, preserved constraints from both roles, prohibited recursive delegation, and returned repository-wide integration to the internal maintainer.
* **Instruction ownership**: Removed the internal role's duplicated claim to define role responsibilities, capabilities, constraints, and context paths. Specialist workflows now remain authoritative in the matching base role.
* **Navigation scope**: Kept repository-wide direct-child index maintenance as an internal coordination rule while deferring stricter scoped navigation and knowledge rules to delegated roles or shared instructions.
* **Activation visibility**: Standardized the internal bootstrap announcement as `Active primary role: Ava Internal Maintainer` and required every delegated specialist to be announced before its instructions affect the work.

## 2026-07-25

* **Git workflow removal**: Removed role-level instructions for commits, branches, pull requests, issues, reviews, merges, and Git history inspection. Repository tooling now determines how Git and GitHub operations are performed.

## 2026-07-23

* **Creation**: Defined the Ava Internal Maintainer as an explicitly activated repository-only role.
* **Authority**: Allowed direct file modification and commits while excluding branches, pull requests, and autonomous architectural decisions.
* **Separation**: Required strict isolation between Ava's internal development instructions and user-generated agent platforms.
