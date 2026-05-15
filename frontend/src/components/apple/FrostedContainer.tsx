import React from "react";
import { cn } from "@/lib/utils";

interface FrostedContainerProps {
  variant?: "white" | "parchment";
  className?: string;
  children?: React.ReactNode;
}

/**
 * FrostedContainer primitive that implements the Apple blur effect.
 * Uses backdrop-blur-md (12px).
 */
const FrostedContainer = ({
  variant = "white",
  className,
  children,
}: FrostedContainerProps) => {
  const backgrounds = {
    white: "bg-white/80",
    parchment: "bg-parchment/80",
  };

  return (
    <div
      className={cn(
        "backdrop-blur-md",
        backgrounds[variant],
        className
      )}
    >
      {children}
    </div>
  );
};

export default FrostedContainer;
