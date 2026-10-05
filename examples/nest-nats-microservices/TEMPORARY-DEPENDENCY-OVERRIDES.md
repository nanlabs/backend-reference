# Temporary dependency resolutions

## `glob` — review by 2027-01-03

The Nest NATS examples temporarily resolve `glob` to `^12.0.0` in each service.

Dependabot reports that the lowest non-vulnerable release for the `glob` advisory is
12.0.0. The legacy ESLint/Jest graph requests older major ranges; Dependabot could only
resolve glob to 10.4.5. The current Nest CLI requests glob 13, so this resolution also
forces that CLI consumer back to glob 12. A semver-major override can affect glob APIs,
so it is scoped to these examples and checked with frozen installs, Nest builds, unit
tests, and e2e tests for each service.

The resolution is limited to these three example service manifests. Glob 12 requires
Node 20 or newer, so the service Docker images now use Node 22. Remove the resolution
once the security update can be applied without crossing dependency ranges. At the
review date, recheck the advisory, upstream dependency ranges, and compatibility; remove
the resolution if it is no longer needed, or obtain renewed approval before extending it.

Evidence: Dependabot update run
https://github.com/nanlabs/backend-reference/actions/runs/37345209673 reported
`latest-resolvable-version: 10.4.5` and `lowest-non-vulnerable-version: 12.0.0`.
