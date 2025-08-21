import { LineChart, CartesianGrid, XAxis, Line } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "./ui/chart";
import { useEffect, useState } from "react";

const chartConfig = {
  vx: {
    label: "Velocity X",
    color: "red",
  },
  vy: {
    label: "Velocity Y",
    color: "green",
  },
  vw: {
    label: "Angular Velocity",
    color: "blue",
  },
} satisfies ChartConfig;

export default function VelocityChart({ robot }: { robot: string }) {
  const [chartData, setChartData] = useState<
    { time: number; vx: number; vy: number; vw: number }[]
  >([]);

  const [start_time] = useState(() => Date.now());

  useEffect(() => {
    try {
      const socket = new WebSocket(robot + "/vel");

      socket.onmessage = (e) => {
        const msg = JSON.parse(e.data);

        setChartData((data) => {
          if (
            data.length > 0 &&
            Date.now() - data[data.length - 1].time < 100
          ) {
            return data;
          }
          return [
            ...data,
            {
              time: Date.now() - start_time,
              ...msg,
            },
          ].slice(-100);
        });
      };

      return () => socket.close();
    } catch {
      return () => {};
    }
  }, [robot, start_time]);

  return (
    <ChartContainer config={chartConfig}>
      <LineChart
        accessibilityLayer
        data={chartData}
        margin={{
          left: 12,
          right: 12,
        }}
      >
        <CartesianGrid vertical={false} />
        <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
        <Line dataKey="vx" type="monotone" stroke="#ff0000" strokeWidth={2} />
        <Line dataKey="vy" type="monotone" stroke="#00ff00" strokeWidth={2} />
        <Line dataKey="vw" type="monotone" stroke="#0000ff" strokeWidth={2} />
      </LineChart>
    </ChartContainer>
  );
}
