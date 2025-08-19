import { useEffect, useRef, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FieldCanvas, Robot } from "@/lib/FieldCanvas";

function App() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const [robot1, setRobot1] = useState("");
  const [vx, setVx] = useState(0);
  const [vy, setVy] = useState(0);
  const [vw, setVw] = useState(0);

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
    <div className="flex flex-col gap-2">
      <h1 className="text-2xl">Field view</h1>
      <canvas width="2430" height="1820" ref={canvasRef} className="w-2xl" />
      <Input
        value={robot1}
        onChange={(e) => setRobot1(e.target.value)}
        type="url"
        placeholder="Robot 1 Debug URI"
      />
      <div className="flex gap-2">
        <Input
          value={vx}
          onChange={(e) => setVx(parseFloat(e.target.value))}
          type="number"
          placeholder="Velocity X (m/s)"
        />
        <Input
          value={vy}
          onChange={(e) => setVy(parseFloat(e.target.value))}
          type="number"
          placeholder="Velocity Y (m/s)"
        />
        <Input
          value={vw}
          onChange={(e) => setVw(parseFloat(e.target.value))}
          type="number"
          placeholder="Angular velocity (rad/s)"
        />
        <Button
          type="submit"
          variant="outline"
          onClick={() => {
            fetch(robot1 + "/target_vel", {
              method: "POST",
              headers: {
                "Content-Type": "application/json;charset=utf-8",
              },
              body: JSON.stringify({ x: vx, y: vy, w: vw }),
            });
          }}
        >
          Send velocity command
        </Button>
      </div>
    </div>
  );
}

export default App;
