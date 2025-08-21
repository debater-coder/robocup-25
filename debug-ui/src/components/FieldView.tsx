import { FieldCanvas, Robot } from "@/lib/FieldCanvas";
import { useEffect, useRef } from "react";

export default function FieldView({ robot1 }: { robot1: string }) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    if (!canvasRef.current) {
      return;
    }
    const ctx = canvasRef.current.getContext("2d");

    if (!ctx) {
      return;
    }

    try {
      const socket = new WebSocket(robot1 + "/pose");

      const field = new FieldCanvas(ctx, [new Robot(socket)]);

      return () => field.close();
    } catch {
      return () => {};
    }
  }, [robot1]);

  return (
    <canvas width="2430" height="1820" ref={canvasRef} className="w-2xl" />
  );
}
