# Architecture

## Purpose

Carpet Commerce is a white-label commerce backend intended to power a real carpet retailer,
not a static portfolio demo. The frontend can be replaced or branded without rewriting domain
logic.

## Architectural boundaries

The project starts as a modular Django monolith. This is intentional: transactional commerce
workflows such as inventory reservation, pricing, checkout, payment verification, and order
creation benefit from one transactional boundary while the product is still evolving.

Planned domain apps:

- `identity` — customers, OTP authentication, roles and permissions.
- `catalog` — categories, brands, collections, carpets, attributes, media and variants.
- `inventory` — branch stock, reservations and adjustments.
- `cart` — carts and server-authoritative pricing.
- `checkout` — address and shipping selection.
- `payments` — provider abstraction, callbacks, verification and reconciliation.
- `orders` — order lifecycle, invoice, cancellation and refund orchestration.
- `promotions` — coupons and campaign rules.
- `engagement` — wishlist, compare, reviews, Q&A and notifications.
- `stores` — branches, consultations, in-store reservations and leads.
- `content` — pages, FAQ, blog, banners and SEO metadata.
- `intelligence` — rug finder, size guide, carpet sets and custom-size requests.

Cross-cutting code belongs in `core` only when it is genuinely shared.

## API

- Versioned business endpoints will live under `/api/v1/`.
- OpenAPI is generated from code and validated in CI.
- Public endpoints explicitly opt into `AllowAny`; authenticated access is the default.
- Price, stock, payment and order state remain backend-authoritative.

## Data

Production database: PostgreSQL 17.

Redis is used for cache, ephemeral coordination, rate limiting primitives and Celery transport.
Durable business truth must not exist only in Redis.

## Background work

Celery handles work that should not block an HTTP request, such as notifications, media jobs
and later reconciliation tasks. Business transactions are committed before non-critical
background side effects are dispatched.

## Deployment model

The target is an Ubuntu server behind Nginx with separate processes for:

- Django/Gunicorn API
- Celery worker
- PostgreSQL
- Redis

Server deployment is intentionally deferred until application release-candidate phases.
