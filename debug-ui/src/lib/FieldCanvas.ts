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

    this.x = msg.x;
    this.y = msg.y;
    this.angle = msg.w;

    this.callback?.();
  };

  close() {
    this.socket.close();
  }
}

const WIDTH = 2430;
const HEIGHT = 1820;

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
    this.ctx.translate(x * 1000 + WIDTH / 2, y * 1000 + HEIGHT / 2);
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
    // Green background (whole field)
    this.ctx.fillStyle = "#37700C";
    this.ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Neutral points
    const neutral_point = (x: number, y: number) =>
      this.circle(x, y, 15, "black");

    neutral_point(WIDTH / 2, HEIGHT / 2 - 300);
    neutral_point(WIDTH / 2, HEIGHT / 2);
    neutral_point(WIDTH / 2, HEIGHT / 2 + 300);

    // Penalty boxes
    this.ctx.strokeStyle = "#000000";
    this.ctx.lineWidth = 25;
    this.ctx.strokeRect(
      250 + 25 / 2,
      HEIGHT / 2 - 900 / 2 + 25 / 2,
      300 - 25 / 2,
      900 - 25 / 2,
    );
    this.ctx.strokeRect(
      WIDTH - 250 - 300,
      HEIGHT / 2 - 900 / 2 + 25 / 2,
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
      WIDTH - 2 * outerOffset,
      HEIGHT - 2 * outerOffset,
    );

    // Goals
    this.ctx.fillStyle = "cyan";
    this.ctx.fillRect(300 - 74, (HEIGHT - 450) / 2, 74, 450);
    this.ctx.fillStyle = "yellow";
    this.ctx.fillRect(WIDTH - 300, (HEIGHT - 450) / 2, 74, 450);

    this.robots.forEach((robot) => this.drawRobot(robot));
  };
}
