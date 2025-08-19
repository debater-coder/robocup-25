export class Robot {
  x: number = 0;
  y: number = 0;
  angle: number = 0;
  socket: WebSocket;
  callback: (() => void) | null = null;

  constructor(socket: WebSocket) {
    this.socket = socket;
    this.socket.onmessage = this.onmessage;
    this.socket.onopen = () =>
      console.log(`Successfully connected to {$this.socket.url}`);
  }

  onmessage = (event: MessageEvent) => {
    const msg = JSON.parse(event.data);

    this.x = msg.x * 1000;
    this.y = msg.y * 1000;
    this.angle = msg.w;

    this.callback?.();
  };

  close() {
    this.socket.close();
  }
}

export class FieldCanvas {
  ctx: CanvasRenderingContext2D;
  robots: Robot[];

  constructor(ctx: CanvasRenderingContext2D, robots: Robot[]) {
    this.ctx = ctx;
    this.robots = robots;

    for (const robot of this.robots) {
      robot.callback = this.draw;
    }

    this.draw();
  }

  close() {
    this.robots.forEach((robot) => robot.close());
  }

  circle(x: number, y: number, radius: number, bg: string) {
    this.ctx.fillStyle = bg;
    this.ctx.beginPath();
    this.ctx.arc(x, y, radius, 0, Math.PI * 2, true);
    this.ctx.fill();
  }

  drawRobot({ x, y, angle }: Robot) {
    this.ctx.save();
    this.ctx.translate(x, y);
    this.ctx.rotate(angle);

    // Robot
    this.ctx.fillStyle = "#fef9c3";
    this.ctx.beginPath();
    this.ctx.arc(0, 0, 100, 0, Math.PI * 2, true);
    this.ctx.fill();

    this.ctx.fillStyle = "black";
    this.ctx.beginPath();
    this.ctx.moveTo(50, 0);
    this.ctx.lineTo(-25, +37);
    this.ctx.lineTo(-25, -37);
    this.ctx.fill();

    this.ctx.restore();
  }

  draw = () => {
    const width = 2430;
    const height = 1820;
    // Green background (whole field)
    this.ctx.fillStyle = "#37700C";
    this.ctx.fillRect(0, 0, width, height);

    // Neutral points
    const neutral_point = (x: number, y: number) =>
      this.circle(x, y, 15, "black");

    neutral_point(width / 2, height / 2 - 300);
    neutral_point(width / 2, height / 2);
    neutral_point(width / 2, height / 2 + 300);

    // Penalty boxes
    this.ctx.strokeStyle = "#000000";
    this.ctx.lineWidth = 25;
    this.ctx.strokeRect(
      250 + 25 / 2,
      height / 2 - 900 / 2 + 25 / 2,
      300 - 25 / 2,
      900 - 25 / 2,
    );
    this.ctx.strokeRect(
      width - 250 - 300,
      height / 2 - 900 / 2 + 25 / 2,
      300 - 25 / 2,
      900 - 25 / 2,
    );

    // White border (250mm from all sides)
    const outerOffset = 250 + 50 / 2; // JS stroke is centre-aligned
    this.ctx.strokeStyle = "#ffffff";
    this.ctx.lineWidth = 50;
    this.ctx.strokeRect(
      outerOffset,
      outerOffset,
      width - 2 * outerOffset,
      height - 2 * outerOffset,
    );

    // Goals
    this.ctx.fillStyle = "cyan";
    this.ctx.fillRect(300 - 74, (height - 450) / 2, 74, 450);
    this.ctx.fillStyle = "yellow";
    this.ctx.fillRect(width - 300, (height - 450) / 2, 74, 450);

    this.robots.forEach((robot) => this.drawRobot(robot));
  };
}
