chair1 = list(input())
chair2 = list(input())
chair3 = list(input())
chair4 = list(input())
k = int(input())
rotate = [] #[회전시킬 의자 번호, 방향(1: 시계, -1: 반시계)]
for i in range(k):
    rotate.append(list(map(int, input().split())))

# 의자 회전
def rotate_chair(chair_num, r_dir):
    global chair1, chair2, chair3, chair4
    if chair_num == 1:
        if r_dir == 1: # 시계
            chair1 = [chair1[-1]] + chair1[0:7]
        else: # 반시계
            chair1 = chair1[1:8] + [chair1[0]]
    elif chair_num == 2:
        if r_dir == 1: # 시계
            chair2 = [chair2[-1]] + chair2[0:7]
        else: # 반시계
            chair2 = chair2[1:8] + [chair2[0]]
    elif chair_num == 3:
        if r_dir == 1: # 시계
            chair3 = [chair3[-1]] + chair3[0:7]
        else: # 반시계
            chair3 = chair3[1:8] + [chair3[0]]
    elif chair_num == 4:
        if r_dir == 1: # 시계
            chair4 = [chair4[-1]] + chair4[0:7]
        else: # 반시계
            chair4 = chair4[1:8] + [chair4[0]]


for chair_num, r_dir in rotate:
    if chair_num == 1:
        a, b, c = chair1[2] != chair2[6], chair2[2] != chair3[6], chair3[2] != chair4[6]
        rotate_chair(1, r_dir)
        if a:
            rotate_chair(2, r_dir*-1)
            if b:
                rotate_chair(3, r_dir)
                if c:
                    rotate_chair(4, r_dir*-1)
    elif chair_num == 2:
        a, b, c = chair1[2] != chair2[6], chair2[2] != chair3[6], chair3[2] != chair4[6]
        rotate_chair(2, r_dir)
        if a:
            rotate_chair(1, r_dir*-1)
        if b:
            rotate_chair(3, r_dir*-1)
            if c:
                rotate_chair(4, r_dir)
    elif chair_num == 3:
        a, b, c = chair1[2] != chair2[6], chair2[2] != chair3[6], chair3[2] != chair4[6]
        rotate_chair(3, r_dir)
        if b:
            rotate_chair(2, r_dir*-1)
            if a:
                rotate_chair(1, r_dir)
        if c:
            rotate_chair(4, r_dir*-1)
    elif chair_num == 4:
        a, b, c = chair1[2] != chair2[6], chair2[2] != chair3[6], chair3[2] != chair4[6]
        rotate_chair(4, r_dir)
        if c:
            rotate_chair(3, r_dir*-1)
            if b:
                rotate_chair(2, r_dir)
                if a:
                    rotate_chair(1, r_dir*-1)   
    


print(1*int(chair1[0]) + 2*int(chair2[0]) + 4*int(chair3[0]) + 8*int(chair4[0]))