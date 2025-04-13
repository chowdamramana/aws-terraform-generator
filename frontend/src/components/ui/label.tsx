import * as React from "react";
import { twMerge } from "tailwind-merge";

export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {}

const cn = (...classes: (string | undefined | null | false)[]) => twMerge(...classes);

const Label = React.forwardRef<HTMLLabelElement, LabelProps>(({ className, ...props }, ref) => {
  return (
    <label
      className={cn("text-sm font-medium", className)}
      ref={ref}
      {...props}
    />
  );
});
Label.displayName = "Label";

export { Label };