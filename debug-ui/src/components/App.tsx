import { useState } from "react";
import { Input } from "@/components/ui/input";
import FieldView from "./FieldView";
import VelocityControl from "./VelocityControl";
import VelocityChart from "./VelocityChart";

function App() {
  const [robot1, setRobot1] = useState("");

  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-2xl">Field view</h1>
      <FieldView robot1={robot1} />
      <Input
        value={robot1}
        onChange={(e) => setRobot1(e.target.value)}
        type="url"
        placeholder="Robot 1 Debug URI"
      />
      <h1 className="text-2xl">Robot 1</h1>
      <h2 className="text-xl">Velocity control</h2>
      <VelocityControl robot={robot1} />
      <h2 className="text-2xl">Velocity</h2>
      <VelocityChart robot={robot1} />
    </div>
  );
}

export default App;
