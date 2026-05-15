import React from "react";
import { cn } from "@/lib/utils";

interface TileProps {
  variant?: "white" | "parchment" | "dark" | "dark-2" | "dark-3";
  className?: string;
  children?: React.ReactNode;
}

const Tile = ({ variant = "white", className, children }: TileProps) => {
  const backgrounds = {
    white: "bg-white text-ink",
    parchment: "bg-parchment text-ink",
    dark: "bg-near-black text-white",
    "dark-2": "bg-near-black-2 text-white",
    "dark-3": "bg-near-black-3 text-white",
  };

  return (
    <section
      className={cn(
        "relative w-full px-0 py-20 rounded-none overflow-hidden flex flex-col items-center justify-center text-center",
        backgrounds[variant],
        className
      )}
    >
      <div className="max-w-7xl w-full px-6 flex flex-col items-center">
        {children}
      </div>
    </section>
  );
};

export default Tile;
