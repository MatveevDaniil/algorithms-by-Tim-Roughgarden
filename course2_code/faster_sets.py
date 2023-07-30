nums = open('algo1-programming_prob-2sum.txt').readlines()
nums = set([int(i.split('\n')[0]) for i in nums])

cnt = 0
for target in range(-10000, 10001):
    if target % 1000 == 0:
        print(target)
    for num in nums:
        num2 = target - num
        if num2 != num and num2 in nums:
            cnt += 1
            break
print(cnt)