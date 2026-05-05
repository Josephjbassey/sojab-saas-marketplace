# Design System: Code By SoJab

## 1. Visual Theme & Atmosphere
A restrained, highly engineered interface showcasing premium SaaS templates. The atmosphere is "The Obsidian Architect"—moody, technical, yet deeply luxurious. It rejects generic "SaaS-blue" aesthetics in favor of a precision-machined dark mode. With intentional asymmetry, fluid spring-physics motion, and significant tonal depth, the interface feels like high-end architectural software.

## 2. Color Palette & Roles
- **Canvas White** (#010E22) — Primary background surface. A very deep navy void.
- **Pure Surface** (#021C3B) — Card and container fill (surface-container-low).
- **Surface Variant** (#03294E) — Elevated cards or highlighted backgrounds.
- **Outline / Border** (#233E5C) — Soft, muted blue borders or section dividers.
- **Primary Accent** (#EB721B) — Vibrant orange for main actions, active states, and CTAs.
- **Secondary Accent** (#C89664) — Muted tan/gold for secondary actions or subtle highlights.
- **Tertiary Accent** (#256B97) — Brighter blue for info tags or subtle contrasts.

## 3. Typography Rules
- **Display:** Geist — Track-tight, controlled scale, weight-driven hierarchy. Used for high-impact branding and hero headers.
- **Body:** Satoshi — Relaxed leading, 65ch max-width, neutral secondary color for maximum readability.
- **Mono:** JetBrains Mono — For code snippets, price tags, and technical tags.
- **Banned:** Inter, standard system fonts, any serif fonts.

## 4. Component Stylings
* **Buttons:** 8px radius. Flat, no outer glow. Tactile -1px translate on active. Tech Azure fill for primary, ghost/outline for secondary.
* **Cards:** Generously rounded corners (12px to 24px). Diffused whisper shadow. Used only when elevation serves hierarchy. Rely on background color shifts (`surface` to `surface-container-low`) instead of thick lines.
* **Inputs:** Label above, error below. Focus ring in Tech Azure. Subdued `surface-container-lowest` background with no full borders.
* **Loaders:** Skeletal shimmer matching exact layout dimensions. No circular spinners.
* **Empty States:** Composed, technical illustrations or simple structural wireframes.

## 5. Layout Principles
- No overlapping elements — every element occupies its own clear spatial zone.
- Asymmetrical splits for Hero sections. Centered Hero sections are strictly banned.
- Strict single-column collapse below 768px. Max-width containment (1400px centered).
- No flexbox percentage math. Generous internal padding (Spacing scale 8 or 12).
- The generic "3 equal cards horizontally" feature row is banned — use 2-column Zig-Zag or asymmetric grids.

## 6. Motion & Interaction
- Spring physics for all interactive elements (stiffness: 100, damping: 20).
- Perpetual micro-interactions on active dashboard components.
- Staggered cascade reveals for grids and lists. Never mount instantly.
- Hardware-accelerated transforms only (opacity and transform).

## 7. Anti-Patterns (Banned)
- No emojis anywhere.
- No `Inter` font.
- No generic serif fonts.
- No pure black (`#000000`) or pure white (`#FFFFFF`) for large areas.
- No neon/outer glow shadows or oversaturated accents.
- No custom mouse cursors.
- No 3-column equal grids.
- No AI copywriting clichés ("Elevate", "Seamless", "Unleash").
- No fabricated data or statistics (use [metric] placeholders if no data exists).
- No broken image links (use picsum.photos or structural SVGs).
