movel(rel=False) = rb.optline(pick_point4) or rb.move(pick_point4)
# 위의 line 실행시 posture 최적으로 주는것 유의.
movel(rel=True) = rb.relline(dx=dist_angle_data)

movej(rel=True) = rb.reljntmove(dj1=dist_angle_data)
movej(rel=False) = rb.move(Joint(90, 90, -100, 180, 0, 0))

getl()= current_xy_coordi()
getj() = current_joint_coordi()

open_gripper = clamp_(2)
close_gripper = clamp_(1)
# gripper 중간 적절한 조절은 안됨.
# 패스토 사가 그리퍼 만든건데 궁금하면 물어보셈


xy좌표를 joint로 변환할때  = rb.Position2Joint
반대로 joint to xy좌표 = rb.Joint2Position

###
# normal 에러면 try except로 올리면 처리 가능한데,
# e-stop 뜰만한 critical 이슈이면, try except도 안걸림 걍 껐다켜야함.

