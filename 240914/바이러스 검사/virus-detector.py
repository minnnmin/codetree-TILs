REST = int(input())
restaurants = list(map(int, input().split()))
LDR, MBR = map(int, input().split())

answer = 0
for customer in restaurants:
    customer -= LDR
    answer += 1
    if customer > 0:
        answer += customer // MBR + 1

print(answer)