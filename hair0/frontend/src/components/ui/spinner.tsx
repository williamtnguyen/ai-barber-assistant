import { cn } from "@/lib/utils";

interface SpinnerProps {
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
  color?: "primary" | "secondary" | "accent" | "white";
}

const sizeClasses = {
  sm: "h-4 w-4",
  md: "h-6 w-6", 
  lg: "h-8 w-8",
  xl: "h-12 w-12"
};

const colorClasses = {
  primary: "text-blue-600",
  secondary: "text-gray-600", 
  accent: "text-purple-600",
  white: "text-white"
};

export function Spinner({ size = "md", className, color = "primary" }: SpinnerProps) {
  return (
    <div className={cn("animate-spin", sizeClasses[size], colorClasses[color], className)}>
      <svg
        className="w-full h-full"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </div>
  );
}

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg" | "xl";
  text?: string;
  className?: string;
  color?: "primary" | "secondary" | "accent" | "white";
  centered?: boolean;
}

export function LoadingSpinner({ 
  size = "md", 
  text, 
  className, 
  color = "primary",
  centered = false 
}: LoadingSpinnerProps) {
  const content = (
    <div className={cn("flex items-center gap-3", className)}>
      <Spinner size={size} color={color} />
      {text && (
        <span className={cn(
          "text-sm font-medium",
          color === "white" ? "text-white" : "text-gray-700"
        )}>
          {text}
        </span>
      )}
    </div>
  );

  if (centered) {
    return (
      <div className="flex items-center justify-center p-8">
        {content}
      </div>
    );
  }

  return content;
}

interface PageLoadingProps {
  title?: string;
  subtitle?: string;
  className?: string;
}

export function PageLoading({ 
  title = "Loading...", 
  subtitle,
  className 
}: PageLoadingProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center min-h-[400px] space-y-4", className)}>
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full blur-lg opacity-20 animate-pulse"></div>
        <Spinner size="xl" color="primary" />
      </div>
      <div className="text-center space-y-2">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {subtitle && (
          <p className="text-sm text-gray-600 max-w-md">{subtitle}</p>
        )}
      </div>
    </div>
  );
}