# Semver Bump

Safely update a repository's release version when version data may be declared, mirrored, derived, or independently projected across manifests and build metadata.

## Installation

```bash
npx skills add dlimkin/agent-skills --skill semver-bump
```

## What this skill does

- Establishes the release unit and scope before editing, including independently versioned monorepo packages
- Finds authoritative version literals, documented mirrors, derived values, generated metadata, and unrelated version fields
- Validates explicit targets as strict SemVer and applies the smallest correct diff
- Handles major, minor, patch, explicit prerelease, and prerelease-finalization requests according to repository policy
- Preserves dependency constraints, lockfile contents, projections, templates, and independent release units unless they are explicitly in scope
- Verifies mapped versions, relevant structured files, remaining old-version references, and repository checks

The skill edits version data only. It does not publish, tag, push, or create a release commit unless separately authorized.

## Example requests

- `$semver-bump set the application version to 2.4.0`
- `Bump only packages/api to 1.8.0 in this monorepo; leave sibling packages unchanged.`
- `Finalize the current 3.0.0-rc.2 prerelease as 3.0.0 without advancing to the next patch.`
- `Prepare a patch release for the library and update only its documented version mirrors.`
