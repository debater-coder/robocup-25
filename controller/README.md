# Robocup 2025 Controller

This is the main controller, running on the both of the Raspberry Pis and executing strategies.

## Components
- Kinematics
  - Command: send commands to Pi Pico to control motors over serial (vx, vy, vw) (vw means angular velocity)
  - Control: Use PID control to determine keep robot at the desired velocity
- Vision (Opencv)
  - Ball: has known size, so can use observed size + camera properties to calculate distance
  - Other robots: idk how, but theres a size limit of robot so we know rough size + epipolar geometry between two cameras + contrast against background
  - Goal and boundary: boundary is a bold white line (made of tape) so we can use corners to localise, colour of goal helps us know which way we are facing
- Communication: Send data packets over BLE
  - Allocation of host and client
  - Fallback to designated roles on disconnect
  - Share vision information/coordinates
- Strategy: Uses behaviour trees
- Debugging: Send data over HTTP to React debug UI
