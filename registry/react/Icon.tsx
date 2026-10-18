import type { SVGProps } from "react";

/** Where the Airframe sprite is served; the `airframe` registry item puts it at ~/airframe/airframe-icons.svg. */
export const AIRFRAME_ICONS = "/airframe/airframe-icons.svg";

export type IconProps = SVGProps<SVGSVGElement> & {
  /** An Airframe icon name (`agent`, `terminal`, `fork`, `environment`, ...). */
  name: string;
  /** 16 (default), 14, 20 or 24 px. */
  size?: 14 | 16 | 20 | 24;
};

/** One icon from the Airframe sprite: stroke-only, in the text color, on the 20 px grid. */
export function Icon({ name, size, className, ...rest }: IconProps) {
  const cls = ["af-ic", size && size !== 16 ? `af-ic--${size}` : "", className].filter(Boolean).join(" ");
  return (
    <svg className={cls} aria-hidden="true" {...rest}>
      <use href={`${AIRFRAME_ICONS}#af-${name}`} />
    </svg>
  );
}
