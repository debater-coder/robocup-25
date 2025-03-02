use bevy::prelude::*;
use bevy_rapier3d::prelude::*;

pub struct SimulatorPlugin;

impl Plugin for SimulatorPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup);
    }
}

fn setup(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
    // light
    commands.spawn((PointLight::default(), Transform::from_xyz(4.0, 8.0, 4.0)));

    // floor
    commands.spawn((
        Mesh3d(meshes.add(Cuboid::new(2.43, 0.1, 1.82))),
        MeshMaterial3d(materials.add(Color::linear_rgb(0.1, 0.7, 0.0))),
        Transform::from_translation(Vec3::ZERO),
    ));

    // camera
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(-2.5, 4.5, 9.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));
}
