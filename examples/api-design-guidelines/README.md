# API Design Guidelines

Design, document, version, and error-handle HTTP APIs so consumers never have to guess. Distilled from backend quality indicators: documentation, versioning, error handling, scalability, and dependency discipline.

## 1. API Documentation (Score 5 Target)

- Every endpoint documented: method, path, auth, parameters, request/response schemas, status codes, and at least one example each way.
- Publish OpenAPI (or equivalent) from code annotations — docs generated from code never drift.
- Document error responses with the same rigor as success responses.
- Keep a changelog per API version; breaking changes get migration notes.

## 2. API Versioning

- Version from day one (`/v1/...`), even with a single consumer.
- Rules: additive changes (new fields, new endpoints) stay in-version; renames, removals, and semantic changes bump the version.
- Sunset policy: announce deprecations with a removal date ≥ 2 minor versions out; emit `Deprecation`/`Sunset` headers.
- Never version by environment (`/staging/...`) or by client.

## 3. Error Handling

- Stable error envelope everywhere:

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "No order exists with id 42.",
    "details": { "orderId": 42 },
    "requestId": "req-9f3a"
  }
}
```

- Machine-readable `code` (SCREAMING_SNAKE, documented catalog) + human `message` + correlation `requestId`.
- Map codes to HTTP status honestly: 400 validation, 401 auth, 403 permission, 404 missing, 409 conflict, 422 semantic, 429 throttled, 500 unexpected.
- Never leak internals: stack traces, SQL, and file paths stay server-side; log them with the `requestId`.
- Retry guidance: mark idempotent operations; document `Retry-After` on 429/503.

## 4. Design for Scale

- Stateless handlers; paginate every list endpoint (cursor > offset at scale).
- Timeouts and payload limits on every route; stream large responses.
- Cache deliberately (`ETag`/`Cache-Control`); invalidate on write paths.
- Rate-limit per consumer with documented quotas and headers (`X-RateLimit-*`).

## 5. Dependency Discipline

- Pin and audit third-party API clients; monitor advisories (Dependabot/Renovate).
- Wrap external APIs behind internal clients: timeouts, retries with backoff, circuit breakers, and typed errors at the boundary.
- Contract-test integrations; never let an upstream schema change surprise production.

## Review Checklist

- [ ] OpenAPI complete and generated from code
- [ ] Versioned routes + sunset policy documented
- [ ] Uniform error envelope with code catalog and request IDs
- [ ] Pagination, timeouts, and rate limits in place
- [ ] External dependencies wrapped, pinned, and contract-tested

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [Stripe API Design (versioning reference)](https://docs.stripe.com/api/versioning)
