import * as React from "react";

import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, ...props }, ref) => {
  return (
    <input
      ref={ref}
      className={cn(
        "flex h-12 w-full rounded-[22px] border border-white/10 bg-white/[0.05] px-4 py-3 text-sm text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.04)] outline-none transition-all duration-300 placeholder:text-muted-foreground focus:border-white/20 focus:bg-white/[0.07] focus:ring-2 focus:ring-ring/70",
        className
      )}
      {...props}
    />
  );
});
Input.displayName = "Input";

export { Input };
