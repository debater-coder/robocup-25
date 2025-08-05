import { useEffect, useRef } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

function App() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    if (!canvasRef.current) {
      return;
    }
    const ctx = canvasRef.current.getContext("2d");

    if (!ctx) {
      return;
    }

    const width = 2430;
    const height = 1820;
    // Green background (whole field)
    ctx.fillStyle = "#37700C";
    ctx.fillRect(0, 0, width, height);

    // Neutral points
    const neutral_point = (x: number, y: number) => {
      ctx.fillStyle = "#000000";
      ctx.beginPath();
      ctx.arc(x, y, 15, 0, Math.PI * 2, true);
      ctx.fill();
    };

    neutral_point(width / 2, height / 2 - 300);
    neutral_point(width / 2, height / 2);
    neutral_point(width / 2, height / 2 + 300);

    // Penalty boxes
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 25;
    ctx.strokeRect(
      250 + 25 / 2,
      height / 2 - 900 / 2 + 25 / 2,
      300 - 25 / 2,
      900 - 25 / 2,
    );
    ctx.strokeRect(
      width - 250 - 300,
      height / 2 - 900 / 2 + 25 / 2,
      300 - 25 / 2,
      900 - 25 / 2,
    );

    // White border (250mm from all sides)
    const outerOffset = 250 + 50 / 2; // JS stroke is centre-aligned
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 50;
    ctx.strokeRect(
      outerOffset,
      outerOffset,
      width - 2 * outerOffset,
      height - 2 * outerOffset,
    );

    // Goals
    ctx.fillStyle = "cyan";
    ctx.fillRect(300 - 74, (height - 450) / 2, 74, 450);
    ctx.fillStyle = "yellow";
    ctx.fillRect(width - 300, (height - 450) / 2, 74, 450);
  }, []);

  return (
    <>
      <h1 className="text-2xl">Field view</h1>
      <canvas width="2430" height="1820" ref={canvasRef} className="w-2xl" />
      <div className="flex gap-2">
        <Input type="number" placeholder="Velocity X (m/s)" />
        <Input type="number" placeholder="Velocity Y (m/s)" />
        <Input type="number" placeholder="Angular velocity (rad/s)" />
        <Button type="submit" variant="outline">
          Send velocity command
        </Button>
      </div>
    </>
  );
}

export default App;
