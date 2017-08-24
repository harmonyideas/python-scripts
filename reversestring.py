str1 = raw_input('Enter your name ')
print ('Length  = ', str1[1:])


def reverse(string):
    print ("STRING:" + string)
    if len(string) <= 1:
        return string
    return reverse(string[1:]) + string[0]


print reverse(str1)