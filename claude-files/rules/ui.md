<!-- Rule Indicator: Add 🎨 when UI work -->

# UI Rules

## Stack (Non-Negotiable)

- **Framework:** React or Next.js
- **Package manager:** Bun (never npm/yarn)
- **Components:** Shadcn UI only
- **Language:** TypeScript (never JavaScript)
- **Styling:** Tailwind via Shadcn conventions

## Shadcn Setup

```bash
bunx shadcn@latest init
bunx shadcn@latest add button card dialog ...
```

Reference: https://ui.shadcn.com/

## Component Rules

- Use Shadcn components before building custom
- Follow Shadcn color tokens (`--primary`, `--secondary`, etc.)
- Use Shadcn font conventions (Inter default)
- Import from `@/components/ui/*`

| Need     | Use                           |
| -------- | ----------------------------- |
| Buttons  | `<Button variant="...">`      |
| Forms    | Shadcn Form + react-hook-form |
| Modals   | `<Dialog>`                    |
| Lists    | `<Card>` or `<Table>`         |
| Feedback | `<Toast>` via sonner          |

## File Structure

```
src/
  components/
    ui/          # Shadcn components (don't edit)
    custom/      # Your components
  app/           # Next.js app router
  lib/
    utils.ts     # cn() helper
```

## Flags

- ❗ Using npm/yarn instead of Bun
- ❗ Custom component when Shadcn has one
- ❗ Inline styles instead of Tailwind
- ❗ JavaScript files (.js/.jsx)
- ❗ UI code in Python project
