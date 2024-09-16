PACKMAN = 4
MONSTER = 3 # 여러 개 일수도 있어서 몬스터 배열 만들어 둔 것
MONSTER_EGG = 2
DEAD_MONSTER = 1

directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
matrix = [[0 for _ in range(5)] for _ in range(5)]

monster_cnt, turn = map(int, input().split())
packman_r, packman_c = list(map(int, input().split()))
matrix[packman_r][packman_c] = 4

monsters = [] # [r, c, d] - d: direction - 그래프로 할걸 그랬나
eggs = [] # [r, c, d, t] - turn: egg가 된 턴
dead_monsters = [] # [r, c, t, TorF] - turn: 시체가 된 턴, TorF: 존재하는 시체면 1, 사라진 시체면 0

def monster_movable(r, c): #(r, c)로 이동할 수 있으면 True 리턴
    if not(0 < r < 5 and 0 < c < 5):
        return False
    # r, c
    # 팩맨 있으면 안됨
    if r == packman_r and c == packman_c:
        return False
    # 몬스터시체 있으면 안됨
    for dmr, dmc, dmt, dmTorF in dead_monsters:
        if dmTorF and r == dmr and c == dmc:
            return False
    return True

for i in range(monster_cnt):
    r, c, d = map(int, input().split())
    monsters.append([r, c, d])
    matrix[r][c] = 3

for t in range(turn):
    # 1. 몬스터 복제 시도
    for mr, mc, md in monsters:
        eggs.append([mr, mc, md, t])
        matrix[mr][mc] = 2
    # for _ in monsters:
    #     print(_)
    # for _ in eggs:
    #     print(_)
    # print('====================')
    # print('===2.몬스터 이동===')
    # 2. 몬스터 이동
    # directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    del_monsters = [] # 삭제할 몬스터 [r, c, d]
    add_monsters = [] # 추가할 몬스터
    for i in range(len(monsters)):
        mr, mc, md = monsters[i]
        #방향으로 갈 수 있으면 가고(팩맨, 시체, 범위 밖 아니면 가능)
        nmr = mr + directions[md-1][0]
        nmc = mc + directions[md-1][1]
        if monster_movable(nmr, nmc):
            # monsters에서 빼고 다시 넣어야 됨
            del_monsters.append([mr, mc, md])
            add_monsters.append([nmr, nmc, md])
        else: #아니면 최대 7번 검사
            for i in range(1, 8):
                nmd = (md + i)%9
                nmr = mr + directions[nmd-1][0]
                nmc = mc + directions[nmd-1][1]
                if monster_movable(nmr, nmc):
                    del_monsters.append([mr, mc, md])
                    add_monsters.append([nmr, nmc, nmd])
                    break
            # 이동 불가능한 경우, 그냥 이동 안 하면 됨
    for dm in del_monsters:
        monsters.remove(dm)
    # print()
    for am in add_monsters:
        monsters.append(am)

    # 3. 팩맨 이동 - 64번 이동하고 몬스터 먹은 개수 확인 - 상좌하우: 0246 - 먹고 시체 남겨
    # 0, 2, 4, 6의 조합
    max_route = (0, 0, 0) #이용한 루트
    max_score = 0 #잡아먹은 몬스터 개수
    # 해야되는 거: 040, 404, 626, 262
    for a in range(0, 7, 2):
        for b in range(0, 7, 2):
            if (a, b) == (0, 4) or (a, b) == (4, 0) or (a, b) == (2, 6) or (a, b) == (6, 2):
                continue
            for c in range(0, 7, 2):
                if (b, c) == (0, 4) or (b, c) == (4, 0) or (b, c) == (2, 6) or (b, c) == (6, 2):
                    continue
                eat_monster_cnt = 0
                # 첫번째
                npr1 = packman_r + directions[a][0]
                npc1 = packman_c + directions[a][1]
                if 0 < npc1 < 5 and 0 < npr1 < 5:
                    # 그 자리에 몬스터 있으면 다 먹어
                    for mr, mc, md in monsters:
                        if mr == npr1 and mc == npc1:
                            eat_monster_cnt += 1
                else:
                    continue
                # 두번째
                npr2 = npr1 + directions[b][0]
                npc2 = npc1 + directions[b][1]
                if 0 < npc2 < 5 and 0 < npr2 < 5:
                    # 그 자리에 몬스터 있으면 다 먹어
                    for mr, mc, md in monsters:
                        if mr == npr2 and mc == npc2:
                            eat_monster_cnt += 1
                else:
                    continue
                # 세번째
                npr3 = npr2 + directions[c][0]
                npc3 = npc2 + directions[c][1]
                if 0 < npc3 < 5 and 0 < npr3 < 5:
                    # 그 자리에 몬스터 있으면 다 먹어
                    for mr, mc, md in monsters:
                        if mr == npr3 and mc == npc3:
                            eat_monster_cnt += 1
                else:
                    continue

                if max_score < eat_monster_cnt:
                    max_route = (a, b, c)
                    max_score = eat_monster_cnt

    # 위에서 검사 끝났으니 이제 그 루트따라 이동하면서 몬스터 먹고 시체 남기고
    del_monsters = [] # 삭제할 몬스터 [r, c, d]
    for i in max_route:
        npr = packman_r + directions[i][0]
        npc = packman_c + directions[i][1]
        for mr, mc, md in monsters:
            if mr == npr and mc == npc:
                eat_monster_cnt += 1
                del_monsters.append([mr, mc, md])
                dead_monsters.append([mr, mc, t, True])
        packman_r = npr
        packman_c = npc
    for dm in del_monsters:
        monsters.remove(dm)

    # 4. 몬스터 시체 소멸
    for i in range(len(dead_monsters)):
        dmr, dmc, dt, TorF = dead_monsters[i]
        if dt + 2 == t:
            dead_monsters[i][3] = False       

    # 5. 몬스터 복제 완성
   
    for i in range(len(eggs)):
        er, ec, ed, et = eggs.pop()
        monsters.append([er, ec, ed])
    
print(len(monsters))