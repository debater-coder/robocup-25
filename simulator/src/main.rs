use bevy::prelude::*;
use bevy_rapier3d::prelude::*;
use simulator::SimulatorPlugin;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(RapierPhysicsPlugin::<NoUserData>::default())
        .add_plugins(SimulatorPlugin)
        .run();
}
