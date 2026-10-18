import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Icon } from "./Icon";

export type ButtonKind = "primary" | "secondary" | "ghost" | "danger";

export type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  /** primary: the one action the view exists for. secondary: every other real action. ghost: navigation-like. danger: Destroy, Deny, Revoke. */
  kind?: ButtonKind;
  /** 28 px, inside cards, banners and table rows. */
  small?: boolean;
  /** An Airframe icon before the text. Icon-only buttons need an aria-label. */
  icon?: string;
  children?: ReactNode;
};

/** Airframe Button (airframe/components/Button): DM Mono capitals on a 2px radius. Write the label in sentence case; the CSS sets the capitals. */
export function Button({ kind = "secondary", small, icon, className, children, type = "button", ...rest }: ButtonProps) {
  const cls = ["af-btn", `af-btn--${kind}`, small ? "af-btn--sm" : "", icon && !children ? "af-btn--icon" : "", className]
    .filter(Boolean)
    .join(" ");
  return (
    <button type={type} className={cls} {...rest}>
      {icon ? <Icon name={icon} /> : null}
      {children}
    </button>
  );
}
