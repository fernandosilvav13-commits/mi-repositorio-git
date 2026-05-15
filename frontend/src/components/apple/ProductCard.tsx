import React from "react";
import { cn } from "@/lib/utils";

interface ProductCardProps {
  title: string;
  description?: string;
  imageUrl?: string;
  className?: string;
  children?: React.ReactNode;
}

/**
 * ProductCard component for displaying artifacts (CVs, results).
 * Follows Apple's "museum pedestal" design.
 */
const ProductCard = ({ title, description, imageUrl, className, children }: ProductCardProps) => {
  return (
    <div
      className={cn(
        "bg-white rounded-lg border border-[#e0e0e0] p-6 flex flex-col gap-4 overflow-hidden",
        className
      )}
    >
      {imageUrl && (
        <div className="relative w-full aspect-square mb-4 flex items-center justify-center bg-transparent">
          <img
            src={imageUrl}
            alt={title}
            className="max-w-[85%] max-h-[85%] object-contain shadow-product"
          />
        </div>
      )}
      
      <div className="flex flex-col gap-1">
        <h3 className="text-[17px] font-semibold leading-[1.24] tracking-[-0.374px] text-ink">
          {title}
        </h3>
        {description && (
          <p className="text-[14px] font-normal leading-[1.43] tracking-[-0.224px] text-ink/60">
            {description}
          </p>
        )}
      </div>
      
      {children && <div className="mt-2">{children}</div>}
    </div>
  );
};

export default ProductCard;
