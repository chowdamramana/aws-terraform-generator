import * as React from "react";
import { Select as RadixSelect, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@radix-ui/react-select";
import { twMerge } from "tailwind-merge";

export interface SelectProps {
  options: { value: string; label: string }[];
  value?: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  className?: string;
}

const cn = (...classes: (string | undefined | null | false)[]) => twMerge(...classes);

const Select: React.FC<SelectProps> = ({ options, value, onChange, placeholder, className }) => {
  return (
    <RadixSelect value={value} onValueChange={onChange}>
      <SelectTrigger className={cn("border rounded-md px-3 py-2", className)}>
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent>
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </RadixSelect>
  );
};

export { Select };