# KEY
# _h means horizontal
# _v means vertcal

# VARIABLE KEY
# _action gives (rotation,translation,translation_vel,angular_vel)
# _pos gives (position_direction,distance,movement_vel)
# _vel gives (vel_h,vel_v)
# _dir gives (displacement_h,displacement_v)

# ACTION
#  receives an input of positioning

# INPUT
#  time_diff = int(x)
#  self_action = (rotation,translation,translation_vel,angular_vel)
#   self_rotation = angle the destination is
#   self_translation = distance the destination
#   self_translation_vel = (self_translation_vel_h,self_translation_vel_v)
#    self_translation_vel_h = translation horizontal velocity of self
#    self_translation_vel_v = translation vertical velocity of self
#   self_angular_vel = (self_angular_vel_h,self_angular_vel_v)
#    self_angular_vel_h = angle speed of turn
#    self_angular_vel_v = 
#  self_pos

# OUTPUT
#

def action(time_diff,self_action,self_pos,team_pos,opp1_pos,opp2_pos,ball_pos,state):
    
    
