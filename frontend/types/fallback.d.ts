// This file is a fallback to suppress IDE errors when npm dependencies are not installed.
// It does NOT replace the need to run 'npm install'.

declare module 'react' {
    export = React;
    export as namespace React;
    namespace React {
        type ReactNode = any;
        type FC<P = {}> = (props: P) => ReactNode;
        function useState<T>(initial: T): [T, (k: T) => void];
        function useEffect(cb: () => void, deps?: any[]): void;
        function useRef<T>(initialValue: T | null): { current: T | null };
        function forwardRef<T, P>(render: (props: P, ref: any) => any): any;
        interface ButtonHTMLAttributes<T> { [key: string]: any }
        interface HTMLButtonElement { }
    }
}

declare module 'react-dom' {
    export function createRoot(container: any): any;
}

declare namespace JSX {
    interface IntrinsicElements {
        [elemName: string]: any;
    }
}

declare module 'lightweight-charts' {
    export function createChart(container: any, options: any): any;
    export const ColorType: { Solid: any };
}

declare module 'lucide-react' {
    export const Check: any;
    export const X: any;
    export const User: any;
}

declare module 'clsx' {
    export default function clsx(...args: any[]): string;
}

declare module 'tailwind-merge' {
    export function twMerge(...args: any[]): string;
}
