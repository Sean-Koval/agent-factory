import type { HTMLAttributes, ReactNode } from "react";

export type CardProps = HTMLAttributes<HTMLElement> & {
  /** Only while something waits on a person (an approval, a held push). Remove it the moment it is decided. */
  lit?: boolean;
  /** 24 px padding instead of 16. */
  airy?: boolean;
  children?: ReactNode;
};

/** Airframe Card (airframe/components/Card): tonal, raised on canvas, no border, no shadow. */
export function Card({ lit, airy, className, children, ...rest }: CardProps) {
  const cls = ["af-card", lit ? "af-card--lit" : "", airy ? "af-card--airy" : "", className].filter(Boolean).join(" ");
  return (
    <article className={cls} {...rest}>
      {children}
    </article>
  );
}

const part = (cls: string, Tag: "div" | "h3" | "p" | "span" = "div") =>
  function Part({ className, children, ...rest }: HTMLAttributes<HTMLElement> & { children?: ReactNode }) {
    return (
      <Tag className={[cls, className].filter(Boolean).join(" ")} {...rest}>
        {children}
      </Tag>
    );
  };

/** Space-between row: a label (af-lbl) on the left, meta or a status on the right. */
Card.Top = part("af-card__top");
/** Mono 11 px fg-subtle, on the right of the top row. */
Card.Meta = part("af-card__meta", "span");
Card.Body = part("af-card__body");
Card.Title = part("af-card__title", "h3");
Card.Desc = part("af-card__desc", "p");
/** Pinned to the bottom on a line-subtle divider; one link or small button on the right. */
Card.Foot = part("af-card__foot");
