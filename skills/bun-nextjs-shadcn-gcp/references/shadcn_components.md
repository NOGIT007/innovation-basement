# Shadcn/UI Components Reference

## Installation

```bash
bunx shadcn@latest init
bunx shadcn@latest add [component-name]
```

## Components

### Form

```bash
bunx shadcn@latest add button input textarea select checkbox radio-group switch slider form label
```

### Layout

```bash
bunx shadcn@latest add card separator scroll-area collapsible accordion tabs table
```

### Feedback

```bash
bunx shadcn@latest add alert toast progress skeleton badge
```

### Overlay

```bash
bunx shadcn@latest add dialog sheet drawer popover tooltip hover-card context-menu dropdown-menu
```

### Navigation

```bash
bunx shadcn@latest add navigation-menu breadcrumb pagination command
```

## Usage Example

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Title</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  );
}
```

## Button Variants

```tsx
<Button variant="default">Default</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
```
