import React from "react";
import { cn } from "@/lib/utils";

interface ConfiguratorCardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
}

const ConfiguratorCard = ({
  children,
  className,
  title,
  subtitle,
}: ConfiguratorCardProps) => {
  return (
    <div
      className={cn(
        "bg-white rounded-lg border border-[#e0e0e0] p-6 w-full max-w-2xl mx-auto mb-6 transition-all duration-500 step-transition-enter",
        className
      )}
    >
      {(title || subtitle) && (
        <div className="mb-6">
          {title && (
            <h3 className="text-[21px] font-semibold tracking-tight text-ink">
              {title}
            </h3>
          )}
          {subtitle && (
            <p className="text-[14px] text-[#7a7a7a] mt-1">
              {subtitle}
            </p>
          )}
        </div>
      )}
      {children}
    </div>
  );
};

export default ConfiguratorCard;
