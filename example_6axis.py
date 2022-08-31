#!/usr/bin/python
# -*- coding: utf-8 -*-
## 1. 초기 설정① #######################################
# 라이브러리 가져오기
## 1．초기 설정 ①　모듈 가져오기 ######################
from i611_MCS import * # 로봇제어 기본기능
from teachdata import * # 티칭데이터 사용
from i611_extend import * # 확장기능 사용 (pallet)
from rbsys import * # 관리 프로그램 사용
from i611_common import * # i611Robot 클래스 메소드의 예외처리
from i611_io import * # I/O 신호를 제어
from i611shm import *  # 공유메모리에 액세스
from threading import Event # event 모듈
import threading # thread 모듈
import pdb # 1줄씩 확인 모듈
import time # 시간관련 모듈
import os # 운영체제 모듈
import math # 계산관련 모듈

def shm_din(port): # 입력신호 읽기, port = in_signal number
    return (int(shm_read(0x0100,1))>>port) & 0x01

def th_stop(event):   # thread 함수
    while True:
        if event.is_set():
            return
        if din(9) == '1': # din(9) = 1일 때 프로그램 종료
            print("User Program Stop!")
            pid = os.getpid()
            os.kill(pid, signal.SIGTERM)    #os signal.SIGKILL
        time.sleep(0.1)

def clamp_(_mode): # clamp 가 1이라면 dout(48) 출력, 그 외 값은 dout(50) 출력
    if _mode == 1:
        dout(48, '1')
        # dout(48, '001')
    else:
        dout(50, '1')
        # dout(48, '100')
    time.sleep(0.25)

def clamp_clear(): # dout 48~50번 초기화
    dout(48,'000')
    time.sleep(0.25)

def current_joint_coordi():
    joint_list = shm_read( 0x3050, 6 ).split( ',' ) 
    joint_list[0] = round(math.degrees(float(joint_list[0])),3) # Joint 좌표계 J1 위치
    joint_list[1] = round(math.degrees(float(joint_list[1])),3) # Joint 좌표계 J2 위치
    joint_list[2] = round(math.degrees(float(joint_list[2])),3) # Joint 좌표계 J3 위치
    joint_list[3] = round(math.degrees(float(joint_list[3])),3) # Joint 좌표계 J4 위치
    joint_list[4] = round(math.degrees(float(joint_list[4])),3) # Joint 좌표계 J5 위치
    joint_list[5] = round(math.degrees(float(joint_list[5])),3) # Joint 좌표계 J6 위치
    # print joint_list # joint location 출력 
    print("j1={0}, j2={1}, j3={2}, j4={3}, j5={4}, j6={5}".format(\
        joint_list[0], joint_list[1], joint_list[2], joint_list[3], joint_list[4], joint_list[5]))

def current_xy_coordi():
    position_list = shm_read( 0x3000, 6).split(',')
    position_list[0] = round(float(position_list[0])*1000,3) # XY 좌표계 X 위치
    position_list[1] = round(float(position_list[1])*1000,3) # XY 좌표계 Y 위치
    position_list[2] = round(float(position_list[2])*1000,3) # XY 좌표계 Z 위치
    position_list[3] = round(math.degrees(float(position_list[3])),3) # XY 좌표계 Rz 위치
    position_list[4] = round(math.degrees(float(position_list[4])),3) # XY 좌표계 Ry 위치
    position_list[5] = round(math.degrees(float(position_list[5])),3) # XY 좌표계 Rx 위치
    posture = shm_read( 0x3040, 1).split(',')
    position_list.append(int(posture[0])) # posture 값, list에 추가
    # print position_list # position location 출력
    print("x={0}, y={1}, z={2}, rz={3}, ry={4}, rx={5}, posture={6}".format(\
        position_list[0], position_list[1], position_list[2], position_list[3], position_list[4], position_list[5], position_list[6]))
    return position_list

def main():
    ## 2. 초기 설정② ####################################
    # i611 로봇 생성자
    rb = i611Robot()
    # 좌표계의 정의
    _BASE = Base()
    # 로봇과 연결 시작 초기화
    rb.open()
    # I/O 입출력 기능의 초기화
    IOinit( rb )
    # 티칭 데이터 파일 읽기
    data = Teachdata( "teach_data" )
    # teach file 에선 x,y,z rz, ry, rx로 줘야함.

    ## 1. 티칭 포인트 불러오기 ###########################
    # 변수명은 임의로 지정이 가능하고 위에서 import해온 teachdata에서 꺼내쓰는것으로 보면 된다.
    pick_point1 = data.get_position("pos1",0) # 픽업 1번 포인트 pos1[0]
    pick_point2 = data.get_position("pos1",1) # 픽업 2번 포인트 pos1[1]
    pick_point3 = data.get_position("pos1",2) # 픽업 3번 포인트 pos1[2]
    pick_point4 = data.get_position("pos1",3) # 픽업 4번 포인트 pos1[3]

    place_point1 = data.get_position("pos1",4) # 픽업 1번 포인트 pos1[0]
    place_point2 = data.get_position("pos1",5) # 픽업 2번 포인트 pos1[1]
    place_point3 = data.get_position("pos1",6) # 픽업 3번 포인트 pos1[2]
    place_point4 = data.get_position("pos1",7) # 픽업 4번 포인트 pos1[3]
    
    pick_point11 = pick_point1.offset(dz=30) # 픽업 1번 포인트 + z offset
    place_point11 = place_point1.offset(dz=50) # 플레이스 1번 포인트 + z offset 
    
    #### 1.1 티칭 포인트 입력해서 사용 #####################
    #      Position(x, y, z, rz, ry, rx)
    # p1 = Position( 95, -280, 425, -120, 0, 180, posture = 7) # 1번 positioin
    # p2 = Position( 95, -280, 240, 154, 80, -114 ) # 2번 position
    # p3 = Position( 300, -280, 240, 159, 86, -156 ) # 3번 position
    #      Joint(j1, j2, j3, j4, j5, j6)
    # J1 = Joint(90, 90, -100, 180, 0, 0) # 1번 Joint
    # J2 = Joint(90, 0, -50, 90, 0, 0) # 2번 Joint
    # J3 = Joint(0, 0, -75, 0, 0, 0) # 3번 Joint

    ## 2. 동작 조건 설정 ########################
    # jnt_speed, lin_speed 설명, 한계값 jnt는 %개념이기에 100이 max, line_speed는 매뉴얼에 표기되어있음
    # acctime, dactime 설명_ 가속값, 감속값 설정한 속도까지 도달하기 위한 속도
    # 가감속 시간이 빠를수록 로봇의 택트는 감소하나 진동이나 부하가 심할수 있음.
    # motionparam을 설정해서 로봇에 적용해야 원하는 퍼포먼스가 나온다.
    # 설정안할시 mcs 내부파일에 지정된 값으로 동작한다.

     # 동작조건 초기설정
    motion = MotionParam(jnt_speed=10, lin_speed=150, pose_speed=20, acctime=0.4, dacctime=0.4, overlap=20)
    rb.motionparam(motion) # 위에서 설정한 motionparameter -> 로봇 적용

    rb.enable_interrupt(0,True) # 동작 중에 감속 정지 입력 시의 예외 발생을 활성화
    rb.enable_interrupt(1,True) # 동작 중에 비상 정지 입력 시의 예외 발생을 활성화
    rb.enable_interrupt(2,True) # 일시정지 중에 감속 정지 입력 시의 예외 발생을 활성화
    rb.enable_interrupt(3,True) # 일시정지 중에 비상 정지 입력 시의 예외 발생을 활성화
    
    event=Event()
    th = threading.Thread(target=th_stop, args=(event, )) # def된 함수를 thread 생성
    th.setDaemon(True) # main 함수와 같이 시작하고 끝나도록 daemon 함수로 설정 (병렬동작이 가능하도록 하는 기능)
    th.start() # thread 동작
    
    ## 3. 로봇 동작을 정의 ##############################
    # 작업 시작
    clamp_(2) # gripper open
    clamp_clear() # 이거 항상 커플로 줘야함
    # gripper close 가 1번
    clamp_(1)
    clamp_clear()

    cnt = 0
    cycle = 0
    try:
        while True: # 반복문
            input_data = raw_input("[Main] 실행하고자 하는 Mode 입력 (도움말 = h or help) : ")
            if input_data == 'h' or input_data == 'help': # 예제출력
                print ("""
                ----------------------------------------------------------
                   Mode            |   설명 
                ----------------------------------------------------------
                   movement        |   로봇 동작
                   motion_param    |   모션파라미터
                   relmove         |   상대이동
                   pallet          |   Pallet
                   io_pass         |   IO를 활용한 동작 제어
                   mdo             |   bit_field
                   pdb             |   프로그램 디버깅
                   status          |   상태 불러오기
                   location        |   위치값 불러오기
                   tr_coordi       |   좌표값 변환 (Joint <-> Position)
                   get_motion      |   모션파라미터 불러오기
                   get_location    |   티치데이터 불러오기
                   set_location    |   티치데이터 저장하기
                   goto_location   |   티치데이터 위치 이동
                   exit            |   프로그램 종료
                ----------------------------------------------------------
                """)
                continue

            if input_data == 'movement': # 로봇 동작
                while True:
                    move_type = raw_input("[movement] 실행하고자 하는 Mode 입력 (도움말 : h or help) : ")
                    if move_type == 'h' or move_type == 'help':
                        print("""
                -----------------------------------------------------------
                    Mode            |   설명 
                -----------------------------------------------------------
                    home            |   Home 위치 이동 (각 Joint 0 위치)
                    move            |   PTP 동작 (jnt_speed 적용)
                    line            |   직선 보간 동작 (lin_speed 적용)
                    optline         |   최적 직선 보간 동작 (jnt_speed 적용)
                    back            |   뒤로가기
                -----------------------------------------------------------
                        """)
                        continue

                    if move_type == 'back':
                        break

                    if move_type == 'home':
                        rb.home()

                    if move_type == 'move':
                        rb.move(pick_point1) # p2p로 움직임
                        rb.sleep(0.5)
                        rb.move(pick_point4)

                    if move_type == 'line': # line이 일반적으로 p2p 보다 느림
                        rb.line(pick_point1) # line 으로 움직임
                        rb.sleep(0.5)
                        rb.line(pick_point4)

                    if move_type == 'optline': # 그래서 좀더 빠르게 line을 쓰고 싶을때 이걸 쓰면됨.
                                                # joint speed가 반영됨
                        rb.optline(pick_point1)
                        rb.sleep(0.5)
                        rb.optline(pick_point4)

                    rb.sleep(0.001)
                continue
            
            if input_data == 'motion_param': # 모션 파라미터
                while True:
                    param_type = raw_input("[motion_param] 실행하고자 하는 Mode 입력 (도움말 : h or help) : ")
                    if param_type == 'h' or param_type == 'help': #명령예제 출력
                        print("""
                -----------------------------------------------------------------------
                    Mode            |   설명                           
                -----------------------------------------------------------------------
                    lin_speed       |   직선 보간 동작 속도 (default = 5.0 mm/s)
                    jnt_speed       |   PTP 및 최적 직선 보간 동작 속도 (default = 5.0 %)
                    acctime         |   가속 시간 (default = 0.4 s)
                    dacctime        |   감속 시간 (default = 0.4 s)
                    overlap         |   오버랩 거리 (default = 0.0 mm)
                    back            |   뒤로가기
                -----------------------------------------------------------------------
                        """)
                        continue

                    if param_type == 'back':
                        break

                    mp_default = rb.getmotionparam() # motion_parameter 획득
                    mp = mp_default.mp2list() # parameter -> list 변환

                    if param_type == 'lin_speed':
                        print("현재 lin_speed = {}".format(mp[0]))
                        value = float(raw_input("[lin_speed] 속도값 입력 (mm/s) : "))
                        mcopy = mp_default.copy(lin_speed = value)
                        rb.motionparam(mcopy) # 위에서 설정한 motionparameter -> 로봇 적용
                        rb.line(pick_point1)
                        rb.line(pick_point4)

                    if param_type == 'jnt_speed':
                        print("현재 jnt_speed = {}".format(mp[1]))
                        value = float(raw_input("[jnt_speed] 속도값 입력 (%) : "))
                        mcopy = mp_default.copy(jnt_speed = value)
                        rb.motionparam(mcopy) # 위에서 설정한 motionparameter -> 로봇 적용
                        rb.move(pick_point1)
                        rb.move(pick_point4)

                    if param_type == 'acctime' or param_type == 'dacctime':
                        print("현재 acctime = {}, dacctime = {}".format(mp[2], mp[3]))
                        value = float(raw_input("[acctime and dacctime] 가감속값 입력 (s) : "))
                        mcopy = mp_default.copy(acctime = value, dacctime = value)
                        rb.motionparam(mcopy) # 위에서 설정한 motionparameter -> 로봇 적용
                        rb.move(pick_point1)
                        rb.move(pick_point4)

                    if param_type == 'overlap': # 로봇 예측동작 사용, tact 감축관련 중요 method
                        print("현재 overlap = {}".format(mp[6]))
                        value = float(raw_input("[overlap] 오버랩 거리 입력 (mm) : "))
                        mcopy = mp_default.copy(overlap = value)
                        rb.motionparam(mcopy) # 위에서 설정한 motionparameter -> 로봇 적용
                        rb.move( pick_point4.offset(dz = 150))
                        rb.sleep(0.1)
                        # tact 계산시작
                        non_overlap_start_time = time.time()
                        # overlap 미적용
                        # Pos1 GET
                        rb.move( pick_point1.offset(dz = 150))
                        rb.line( pick_point1)
                        rb.line( pick_point1.offset(dz = 150))
                        # Pos2 PUT
                        rb.move( pick_point4.offset(dz = 150))
                        rb.line( pick_point4)
                        rb.line( pick_point4.offset(dz = 150))
                        # tact 계산종료, 출력
                        non_overlap_tact_time = time.time() - non_overlap_start_time
                        non_overlap_tact_time = round(non_overlap_tact_time,3) # 소숫점 3자리까지만 출력
                        print("Overlap 미적용 T/T : {}".format(non_overlap_tact_time))

                        # tact 계산시작
                        overlap_start_time = time.time()
                        # overlap 적용, 시작
                        rb.asyncm(1)
                        # Pos1 GET 
                        rb.move( pick_point1.offset(dz = 150))
                        rb.line( pick_point1)
                        rb.line( pick_point1.offset(dz = 150))
                        # Pos2 PUT
                        rb.move( pick_point4.offset(dz = 150))
                        rb.line( pick_point4)
                        rb.line( pick_point4.offset(dz = 150))
                        # overlap 멈춤, 종료
                        rb.join()
                        rb.asyncm(2)
                        # tact 계산종료, 출력
                        overlap_tact_time = time.time() - overlap_start_time
                        overlap_tact_time = round(overlap_tact_time,3) # 소숫점 3자리까지만 출력
                        print("Overlap 적용 T/T : {}".format(overlap_tact_time))
                    
                    rb.sleep(0.001)
                continue

            if input_data == 'relmove': # 좌표계 상대이동
                while True:
                    current_joint_coordi()
                    current_xy_coordi()

                    coordi_type = raw_input("[relmove] 움직이고자 하는 Coordinate 입력 (도움말 = h or help) : ")
                    if coordi_type == 'h' or coordi_type == 'help':
                        print("""
                -----------------------------------------------------------
                    Coordinate      |   설명 
                -----------------------------------------------------------
                    x               |   x 축 이동
                    y               |   y 축 이동
                    z               |   z 축 이동
                    rz              |   rz 축 이동
                    ry              |   ry 축 이동
                    rx              |   rx 축 이동
                    j1              |   j1 축 이동
                    j2              |   j2 축 이동
                    j3              |   j3 축 이동
                    j4              |   j4 축 이동
                    j5              |   j5 축 이동
                    j6              |   j6 축 이동
                    back            |   뒤로가기
                -----------------------------------------------------------
                        """)
                        continue

                    if coordi_type == 'back':
                        break

                    dist_angle_data = float(raw_input("[relmove] 움직이고자 하는 거리 또는 각도 입력 (뒤로가기 = back): "))

                    if dist_angle_data == 'back':
                        continue
                    
                    if coordi_type == 'x':
                        rb.relline(dx=dist_angle_data)
                    if coordi_type == 'y':
                        rb.relline(dy=dist_angle_data)
                    if coordi_type == 'z':
                        rb.relline(dz=dist_angle_data)
                    if coordi_type == 'rz':
                        rb.relline(drz=dist_angle_data)
                    if coordi_type == 'ry':
                        rb.relline(dry=dist_angle_data)
                    if coordi_type == 'rx':
                        rb.relline(drx=dist_angle_data)

                    if coordi_type == 'j1':
                        rb.reljntmove(dj1=dist_angle_data)
                    if coordi_type == 'j2':
                        rb.reljntmove(dj2=dist_angle_data)
                    if coordi_type == 'j3':
                        rb.reljntmove(dj3=dist_angle_data)
                    if coordi_type == 'j4':
                        rb.reljntmove(dj4=dist_angle_data)
                    if coordi_type == 'j5':
                        rb.reljntmove(dj5=dist_angle_data)
                    if coordi_type == 'j6':
                        rb.reljntmove(dj6=dist_angle_data)

                    rb.sleep(0.001)
                continue

            if input_data == 'pallet': # pallet 동작, 20개 반송 
                # pallet 1번 생성
                pal1 = Pallet() # pallet 생성 method
                pal1.init_4(pick_point1, pick_point2, pick_point3, pick_point4, 5, 4) # 4점 포인트 바운더리 생성_i=5/j=4, total 20cell 구역
                pal1.adjust( 3, 2, 0.4, -0.3 ) # 3,2번 셀 x축 +0.4mm/ y축 -0.3mm 보정

                # pallet 2번 생성
                pal2 = Pallet() # pallet 생성 method
                pal2.init_4(place_point1, place_point2, place_point3, place_point4, 5, 4) # 4점 포인트 바운더리 생성_i=5/j=4, total 20cell 구역
                pal2.adjust( 1, 0, 0.4, -0.3 ) # 1,0번 셀 x축 +0.4mm/ y축 -0.3mm 보정
                print("pallet 동작 시작!")
                rb.sleep(1)
                for i in range(5): # i열 5줄
                    for j in range(4): # j열 4줄
                        ## 픽업부 #########################
                        print("i = {0}, j = {1}".format(i,j)) # 작업할 i, j열 위치값 출력
                        pallet1 = pal1.get_pos(i,j) # 상단부 생성 pallet1번 불러오기
                        rb.move(pallet1.offset(dz=30)) # 목표위치 z.offset +30mm
                        rb.line(pallet1) # 목표위치 도달

                        # clamp close
                        clamp_(1)
                        clamp_clear()

                        rb.line(pallet1.offset(dz=60))

                        ## 플레이스부 ######################
                        pallet2 = pal2.get_pos(i,j) # 상단부 생성 pallet2번 불러오기
                        rb.move(pallet2.offset(dz=60)) # 목표위치 z.offset +60mm
                        rb.line(pallet2) # 목표위치 도달

                        # clamp open
                        clamp_(2)
                        clamp_clear()

                        rb.line(pallet2.offset(dz=30))
                print("pallet 동작 종료!")
                continue

            if input_data == 'io_pass': # in 신호 확인 후 다음 스텝 진행, 조건문 활용
                print("io_pass 동작 시작!")
                rb.sleep(1)
                while shm_din(7) == 0:
                    ############### 기본 동작 1 cycle  #############################
                    rb.move(pick_point11)
                    rb.line(pick_point1)

                    clamp_(1)
                    time.sleep(0.3)
                    clamp_clear()

                    print("8번 입력이 1이 되면 다음 동작을 진행합니다.")
                    while shm_din(8) == 0: # 8번 in_signal on시 다음 step 진행
                        pass

                    rb.line(pick_point11)
                    rb.move(place_point11)
                    rb.line(place_point1)

                    clamp_(2)
                    time.sleep(0.3)
                    clamp_clear()

                    print("8번 입력이 0이 되면 다음 동작을 진행합니다.")
                    while shm_din(8) == 1: # 8번 in_signal off시 다음 step 진행
                        pass

                    rb.line(place_point11)

                    cnt +=1 # count 증가
                    print(cnt)

                    if not cnt == 2: 
                        # 1cycle 반복할 때마다 좌표값 변경
                        pick_point1 = pick_point1.offset(dz=-15)
                        pick_point11 = pick_point11.offset(dz=-15)
                        place_point1 = place_point1.offset(dz=15)
                        place_point11 = place_point11.offset(dz=15)

                    if cnt == 2 :
                        pick_point1 = pick_point1.offset(dy=-75, dz=15)
                        pick_point11 = pick_point11.offset(dy=-75, dz=15)
                        place_point1 = place_point1.offset(dz=15)
                        place_point11 = place_point11.offset(dz=15)
                        cnt = 0
                        cycle +=1
                        print(cycle)

                    if cycle == 4:
                        cnt = 0
                        cycle = 0
                        pick_point1 = data.get_position("pos1",0) # 픽업 1번 포인트 pos1[0]
                        pick_point11 = pick_point1.offset(dz=30) # 픽업 1번 포인트 + z offset
                        place_point1 = data.get_position("pos1",4) # 픽업 1번 포인트 pos1[0]
                        place_point11 = place_point1.offset(dz=50) # 플레이스 1번 포인트 + z offset 
                        rb.home()
                        break

                    rb.sleep(0.001)

                else:
                    cnt = 0
                    cycle = 0
                    pick_point1 = data.get_position("pos1",0) # 픽업 1번 포인트 pos1[0]
                    pick_point11 = pick_point1.offset(dz=30) # 픽업 1번 포인트 + z offset
                    place_point1 = data.get_position("pos1",4) # 픽업 1번 포인트 pos1[0]
                    place_point11 = place_point1.offset(dz=50) # 플레이스 1번 포인트 + z offset 
                continue

            if input_data == 'mdo': # mdo 기능, 특정구간에서 출력신호 제어
                print("mdo 동작 준비위치 이동")
                rb.sleep(1)
                rb.move(pick_point1)
                dout(24, '1')
                # 미리 MDO 동작 설정을 해둡니다
                rb.set_mdo( 1, 24, 0, 1, 100 ) # 출발 후 100mm 구간 24번 dout(24, "0") 출력 [관리번호 1번에 등록]
                rb.set_mdo( 8, 24, 1, 2, 100 ) # 도착 전 100mm 구간 24번 dout(24, "1") 출력 [관리번호 8번에 등록]
                rb.enable_mdo(129) # MDO 관리 번호 1, 8 활성화  1000 0001
                print("mdo동작 시작!")
                rb.sleep(1)
                # 실동작 구간
                rb.move(place_point4)
                # MDO 동작을 비활성화합니다
                # rb.disable_mdo( 129 ) # MDO 관리 번호 1, ８ 비활성화
                rb.disable_mdo( bitfield=129 ) # MDO 관리 번호１, ８ 비활성화
                continue

            if input_data == 'pdb': # 프로그램 디버깅용 메소드
                print("한스텝씩 동작하려면 'n', 연속 동작하려면 'c' 를 입력하세요.")
                pdb.set_trace() # pdb 기능/ 입력값_ c = continue (전체동작), n = next (한라인씩 스텝동작)
                clamp_clear()
                clamp_(1)
                clamp_clear()
                clamp_(2)
                clamp_clear()
                continue
 
            if input_data == 'status': # 로봇 시스템 상태확인
                system_list = rb.get_system_port()
                print("Running={0}, Svon={1}, Emo={2}, Hw_error={3}, Sw_error={4}, Abs_lost={5}, In_pause={6}, Error={7}".format(\
                    system_list[0], system_list[1], system_list[2], system_list[3], system_list[4], system_list[5], system_list[6], system_list[7]))
                continue
                
            if input_data == 'location': # 현재 매니퓰레이터 좌표 출력
                print("Joint 좌표")
                current_joint_coordi()
                print("XY 좌표")
                current_xy_coordi()
                continue
        
            if input_data == 'tr_coordi': # coordinate 변환 -- 현재위치 좌표 변환으로 변경 할 것
                print("현재위치를 좌표 변환")
                tr_pos = rb.getpos()
                jnt = rb.Position2Joint(tr_pos) # position -> joint 변환
                print("joint 좌표 : {}".format(jnt.jnt2list()))
                pos = rb.Joint2Position(jnt)         # joint    -> position 변환
                print("xy 좌표 : {}".format(pos.pos2list()))
                continue
                    
            if input_data == 'get_motion': # motion_parameter 불러오기
                mp = rb.getmotionparam() # motion_parameter 획득
                mp = mp.mp2list() # parameter -> list 변환
                print("lin_speed={0}, jnt_speed={1}, acctime={2}, dacctime={3}, posture={4}".format(round(mp[0],1), round(mp[1],1), round(mp[2],1), round(mp[3],1), int(mp[4])))
                print("passm={0}, overlap={1}, zone={2}, pose_speed={3}, ik_solver_option={4}".format(int(mp[5]), round(mp[6],1), int(mp[7]), round(mp[8],1), mp[9]))
                continue

            if input_data == 'get_location': # 티치데이터 불러오기
                input_data = raw_input("[get_location] 불러올 포지션 위치 입력 (예시 : pos1,0): ")
                read_data = input_data.split(',')
                # [ key, index, tool, base, comment ]
                #[key, index, tool offset, base offset, comment]
                read_pos, toolid, baseid, comment = data.get_position(read_data[0],int(read_data[1]),True,True,True)
                read_pos = read_pos.pos2list()
                read_pos_x = round(read_pos[0],3)
                read_pos_y = round(read_pos[1],3)
                read_pos_z = round(read_pos[2],3)
                read_pos_rz = round(read_pos[3],3)
                read_pos_ry = round(read_pos[4],3)
                read_pos_rx = round(read_pos[5],3)
                read_posture = read_pos[7]
                print("{0}[{1}] = ({2}, {3}, {4}, {5}, {6}, {7}, posture={8})".format(\
                    read_data[0], read_data[1], read_pos_x, read_pos_y, read_pos_z, read_pos_rz, read_pos_ry, read_pos_rx, read_posture))
                continue

            if input_data == 'set_location': # 티치데이터 저장하기
                data.close()
                data.open(False)
                input_data = raw_input("[set_location] 저장할 포지션 위치 입력 (예시 : pos1,0): ")
                write_data = input_data.split(',')
                write_pos_list = current_xy_coordi()
                write_pos = Position( write_pos_list[0], write_pos_list[1], write_pos_list[2], write_pos_list[3], write_pos_list[4], write_pos_list[5], posture = write_pos_list[6])
                # [ key, index, tool, base, comment ]
                data.set_position(write_data[0],int(write_data[1]),write_pos,0,0,"")
                data.flush()
                continue

            if input_data == 'goto_location': # 티치데이터 이동하기
                input_data = raw_input("[goto_location] 이동하려는 포지션 위치 입력 (예시 : pos1,0): ")
                goto_data = input_data.split(',')
                print("{0}[{1}] 위치로 이동".format(goto_data[0], int(goto_data[1])))
                goto_pos = data.get_position(goto_data[0],int(goto_data[1]))
                rb.move(goto_pos)
                continue

            if input_data == 'exit': # 메인 프로그램 종료
                break

    except KeyboardInterrupt:           # "ctrl" + "c" 버튼 입력
        print("KeyboardInterrupt")
        dout(48, '000')
    except Robot_emo:
        print("Robot_emo")
        dout(48, '000')
    except Exception as e:
        print("Error name is : {}".format(e))
    finally:
        print("finally")
        dout(48, '000')
    
    ## 4. 종료 ######################################
    # 로봇과의 연결을 종료
    event.set()
    rb.close()
if __name__ == '__main__':
    main()