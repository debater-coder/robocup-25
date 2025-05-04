# KEY
# SUFFIX    MEANING                 STRUCTURE
#
# '_info'   information             (_action,_pos,_state)
# '_diff'   difference              (_interger_)
# '_action' describes the move
# 
# '_h'      horizontal component    
# '_v'      vertcal component       
# 
# '_ang' means the angle (clockwise)
# '_trans' means the translation distance
# ''
# '_pos' means position             (pos_ang,distance,movement_vel)
# '_disp' means displacment 
#

# VARIABLE KEY
# _action gives (angle,trans,trans_vel,angular_vel)
# _pos gives (pos_ang,distance,movement_vel)
# _vel gives (vel_h,vel_v)
# _dir gives (disp_h,disp_v)


# INPUT
#   time_diff = int(x)
#   self_action = (angle,trans,trans_vel,angular_vel)
#       self_ang
#       self_trans
#       self_trans_vel = (self_trans_vel_h,self_trans_vel_v)
#           self_trans_vel_h
#           self_trans_vel_v
#       self_angular_vel = (self_angular_vel_h,self_angular_vel_v)
#           self_angular_vel_h
#           self_angular_vel_v 
#       self_pos = (pos_ang,distance,movement_vel)
#           self_pos_ang
#       state = int(y)
#   team_pos
#       
#   opp1_pos
#       
#   opp2_pos
#       
#   ball_pos
#       
#   

# OUTPUT
# drib_vel

def action(time_diff, self_info, team_pos, opp1_pos, opp2_pos, ball_pos):
    (self_action,self_pos,state) = self_info

    
