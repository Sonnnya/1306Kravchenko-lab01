#ставит в соотвествие русской букве ее номер в алфавите
def letter_to_number(char):
    char = char.lower()
    if char in 'её':
        return 6
    if ord('а') <= ord(char) <= ord('я'):
        return ord(char) - ord('а') + 1
    else:
        return -1

#получение буквы по ее номеру в алфавите
def number_to_letter(n):
    char = chr(ord('а') + n - 1)
    if char == 'ё':
        char = 'е'
    if not(ord('а') <= ord(char) <= ord('я')):
        return -1
    return char.upper()

#возвращает n-ный член последовательности Фибоначчи
def fib(n):
    if n in (1, 2):
        return 1
    return fib(n - 1) + fib(n - 2)

#переводит десятичное число в Фибоначчиеву систему счисления
def dec_to_fib(n):
    x = 0
    i = 0
    j = 0
    s = 0
    while True:
        i += 1
        if fib(i) >= n:
            break
    a = [fib(j) for j in range(2, i)]
    
    i -= 1
    while s != n:
        i -= 1
        if s + a[i-1] <= n:
            s += a[i-1]
            x += 10**(i-1)
    return str(x)

#переводит число из Фибоначчиевой системы в десятичную
def fib_to_dec(n):
    x = 0
    i = 0
    a = [fib(i) for i in range(2, fib(len(n)))]
    for i in range(len(n)):
        if n[i] == "1":
            x += a[len(n)-i-1]
    return x

#переводит число из десятичной системы в систему с основанием base
#ctroka
def dec_to_base(n, base):
    x = ''
    while n > 0:
        a = n % base
        n //= base
        if a < 10:
            x = str(a) + x
        else:
            x = chr(ord('A') + a - 10) + x
    return x
    
#переводит число из системы с основанием base в десятичную   
def base_to_dec(n, base):
    x = 0
    for i in range(len(n)):
        x += int(n[i], base) * base**(len(n)-i-1)
    return x

#переводит дробь из системы с основанием base в десятичную
def base_fract_to_dec(n, base):
    x = 0
    for i in range(1, len(n) + 1):
        x += int(n[i-1], base)*base**(-i)
    return x

#переводит дробь из десятичной в систему с основанием base
def dec_to_base_fract(n, base, len_):
    i = 0
    x = ''
    for i in range(len_):
        n *= base
        n = round(n,len_)
        if int(n) < 10:
            x += str(int(n))
        else:
            x += chr(ord('A') + int(n) - 10)
        n -= int(n)
    return x

СODELEN = 21 #длина кода
THIRDLEN = 7 #количество ячеек в конце кода, предназначеных для 3-его числа


#кодирование слова из 3-х русских букв
def encode(letters):
    if len(letters) != 3:
        print('Введите слово из 3-х русских букв. ')
    else:
        code = [0]*СODELEN
        numbers = []
        for i in range(3):
            numbers.append(letter_to_number(letters[i]))
        #кодирование первого числа
        if numbers[1] != 1:
            x1 = dec_to_base(numbers[0], numbers[1])
        else:
            x1 = str(numbers[1])
        for i in range(len(x1)):
            code[i] = x1[i]
        code[len(x1)] = '#'
        
        #кодирование третьего числа
        x3 = dec_to_fib(numbers[2])
        while len(x3) != THIRDLEN:
            x3 = '0' + x3
        for i in range(THIRDLEN):
            code[СODELEN-i-1] = x3[i]
        
        #кодирование второго числа
        #количество ячеек для закодированного второго числа
        len_ = СODELEN - code.index('#') - THIRDLEN - 1
        x2 = dec_to_base_fract(numbers[1]/10**len(str(numbers[1])), numbers[2], len_)
        for i in range(len_):
            code[code.index('#') + i + 1] = x2[i]
        print(code)
        return code

#декодирование последовательности из СODELEN (т.е. 21) символов
def decode(code):
    if len(code) != СODELEN:
        printf("Введите 21 символ.")
    elif code.count('#') == 0 or code.count('#') > 1:
        printf("В коде должен быть ровно 1 символ #")
    else:
        letters = ['']*3
        numbers = [0]*3
        #декодирование третьего символа
        x3 = code[-7:]
        numbers[2] = fib_to_dec(x3)
        
        #декодирование второго символа
        x2 = code[code.index('#')+1:14]
        print(x2)
        numbers[1] = int(str(base_fract_to_dec(x2, numbers[2]))[2:])
        
        #декодирование первого символа
        x1 = code[:code.index('#')]
        if numbers[1] == 1:
            numbers[0] = int(x1)
        else:
            numbers[0] = base_to_dec(x1, numbers[1])
            
        #восстанавливаем слово
        letters = [number_to_letter(numbers[i]) for i in range(3)]
        print(*letters, sep = '')
    return letters
    
decode('12#1C0000000000100010')



