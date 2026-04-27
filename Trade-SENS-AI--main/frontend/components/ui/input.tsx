import * as React from "react"
import { twMerge } from "tailwind-merge"

export interface InputProps extends React.HTMLAttributes<HTMLInputElement> {
    type?: string;
    value?: any;
    step?: string;
}

const Input = React.forwardRef<HTMLInputElement, any>(
    ({ className, type, ...props }, ref) => {
        return (
            <input
                type={type}
                className={twMerge(
                    "flex h-10 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:cursor-not-allowed disabled:opacity-50",
                    className
                )}
                ref={ref}
                {...props}
            />
        )
    }
)
Input.displayName = "Input"

export { Input }
