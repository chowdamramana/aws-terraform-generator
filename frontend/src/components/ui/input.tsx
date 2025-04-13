import * as React from "react";
import { twMerge } from "tailwind-merge";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const cn = (...classes: (string | undefined | null | false)[]) => twMerge(...classes);

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, ...props }, ref) => {
  return (
    <input
      className={cn("border rounded-md px-3 py-2 w-full", className)}
      ref={ref}
      {...props}
    />
  );
});
Input.displayName = "Input";

export { Input };