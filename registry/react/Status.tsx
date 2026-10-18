import type { HTMLAttributes, ReactNode } from "react";

/** The six Airframe statuses. Only approval, failed and denied carry color (the dark-cockpit rule). */
export type StatusRole = "running" | "queued" | "approval" | "failed" | "denied" | "off";

export type StatusProps = HTMLAttributes<HTMLSpanElement> & {
  role: StatusRole;
  /** The word takes the status color too: for counts and panel headers. Never on `off`. */
  lit?: boolean;
  /** A short word: Running, Queued, Needs approval, Failed, Denied, Spun down. Omit for a bare mark. */
  children?: ReactNode;
};

/** Airframe Status (airframe/components/Status): always color + shape + word. */
export function Status({ role, lit, className, children, ...rest }: StatusProps) {
  const cls = ["af-status", `af-status--${role}`, lit ? "af-status--lit" : "", className].filter(Boolean).join(" ");
  return (
    <span className={cls} aria-hidden={children ? undefined : true} {...rest}>
      <i className="af-status__mark" />
      {children}
    </span>
  );
}
