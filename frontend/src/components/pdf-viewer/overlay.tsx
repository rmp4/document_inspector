"use client";

type BBox = {
  x: number;
  y: number;
  w: number;
  h: number;
};

type OverlayProps = {
  boxes: BBox[];
  scale: number;
};

export function BboxOverlay({ boxes, scale }: OverlayProps) {
  return (
    <div className="pointer-events-none absolute inset-0">
      {boxes.map((box, index) => {
        const style = {
          left: `${box.x * scale}px`,
          top: `${box.y * scale}px`,
          width: `${box.w * scale}px`,
          height: `${box.h * scale}px`,
        };
        return (
          <div
            key={`${index}-${box.x}-${box.y}`}
            className="absolute rounded-sm border border-red-500/80 bg-red-500/20"
            style={style}
          />
        );
      })}
    </div>
  );
}
