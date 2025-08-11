import { useEffect, useRef, type RefObject } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

function draw(
  ctx: CanvasRenderingContext2D,
  frameRef: RefObject<number | null>,
) {
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

  const now = new Date();
  const time = (now.getSeconds() + now.getMilliseconds() / 1000) % 10;

  const robot: [number, number, number] = [
    width / 2 + time * 100,
    height / 2 + time * 100,
    time,
  ];

  ctx.save();
  ctx.translate(robot[0], robot[1]);
  ctx.rotate(time);

  // Robot
  ctx.fillStyle = "#fef9c3";
  ctx.beginPath();
  ctx.arc(0, 0, 100, 0, Math.PI * 2, true);
  ctx.fill();

  ctx.fillStyle = "black";
  ctx.beginPath();
  ctx.moveTo(50, 0);
  ctx.lineTo(-25, +37);
  ctx.lineTo(-25, -37);
  ctx.fill();

  ctx.restore();

  // Next frame
  frameRef.current = requestAnimationFrame(() => draw(ctx, frameRef));
}

function App() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationFrameRef = useRef<number | null>(null);

  useEffect(() => {
    if (!canvasRef.current) {
      return;
    }
    const ctx = canvasRef.current.getContext("2d");

    if (!ctx) {
      return;
    }

    animationFrameRef.current = requestAnimationFrame(() =>
      draw(ctx, animationFrameRef),
    );

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
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
