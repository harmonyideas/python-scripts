integer_list = [1,1,2,3,4,4,4,5,6,7,7,7,7,7,8,9,10]
integer_counter = {}

for number in integer_list:
    if number in integer_counter:
        integer_counter[number] += 1
    else:
        integer_counter[number] = 1

top_integers = sorted(integer_counter, key=integer_counter.get, reverse=True)

print top_integers[:1]
