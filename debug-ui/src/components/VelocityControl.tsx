import { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";

export default function VelocityControl({ robot: robot1 }: { robot: string }) {
  const [vx, setVx] = useState(0);
  const [vy, setVy] = useState(0);
  const [vw, setVw] = useState(0);

  return (
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
  );
}
