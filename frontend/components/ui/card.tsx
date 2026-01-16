import * as React from "react"
import { twMerge } from "tailwind-merge"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
    ({ className, ...props }: any, ref) => (
        <div ref={ref} className={twMerge("rounded-xl border border-slate-800 bg-slate-900/50 text-slate-100 shadow-sm", className)} {...props} />
    )
)
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
    ({ className, ...props }: any, ref) => (
        <div ref={ref} className={twMerge("flex flex-col space-y-1.5 p-6", className)} {...props} />
    )
)
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
    ({ className, ...props }: any, ref) => (
        <h3 ref={ref} className={twMerge("text-lg font-semibold leading-none tracking-tight", className)} {...props} />
    )
)
CardTitle.displayName = "CardTitle"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
    ({ className, ...props }: any, ref) => (
        <div ref={ref} className={twMerge("p-6 pt-0", className)} {...props} />
    )
)
CardContent.displayName = "CardContent"

export { Card, CardHeader, CardTitle, CardContent }
