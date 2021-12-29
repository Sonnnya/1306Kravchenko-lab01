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
#возвращает строку
def dec_to_fib(n):
    if n == 1:
        return '1'
    x = 0
    i = 0
    j = 0
    s = 0
    while True:
        i += 1
        if fib(i) > n:
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
#возвращает 0, если введены не 3 русские буквы
def encode(letters):
    global CODELEN, THIRDLEN
    if len(letters) != 3:
        return '0'
    else:
        code = [0]*СODELEN
        numbers = []
        for i in range(3):
            numbers.append(letter_to_number(letters[i]))
            if numbers[i] == -1:
                return '0'
        #кодирование первого числа
        if numbers[1] != 1:
            x1 = dec_to_base(numbers[0], numbers[1])
        else:
            x1 = dec_to_base(numbers[0], 33)
        for i in range(len(x1)):
            code[i] = x1[i]
        code[len(x1)] = '#'
        
        #кодирование третьего числа
        x3 = dec_to_fib(numbers[2])
        while len(x3) != THIRDLEN:
            x3 = '0' + x3
        for i in range(THIRDLEN):
            code[СODELEN-i-1] = x3[THIRDLEN - i - 1]
        
        #кодирование второго числа
        #количество ячеек для закодированного второго числа
        len_ = СODELEN - code.index('#') - THIRDLEN - 1
        if numbers[2] != 1:
            x2 = dec_to_base_fract(numbers[1]/100, numbers[2], len_)
        else:
            x2 = dec_to_base_fract(numbers[1]/100, 33, len_)
        for i in range(len_):
            code[code.index('#') + i + 1] = x2[i]
        return "".join(code)

#декодирование последовательности из СODELEN (т.е. 21) символов
#возвращает строку из 3-х русских букв, если последовательность декодируется
#возвращает 0, если формат кода неверный. 1, если код не мог получится
def decode(code):
    global CODELEN
    if len(code) != СODELEN:
        return '0'
    elif code.count('#') == 0 or code.count('#') > 1:
        return '0'
    else:
        letters = ['']*3
        numbers = [0]*3
        #декодирование третьего символа
        x3 = code[-7:]
        if x3.count('0') + x3.count('1') != len(x3):
            return '1'
        numbers[2] = fib_to_dec(x3)
        
        #декодирование второго символа
        try:
            x2 = code[code.index('#')+1:14]
            if numbers[2] != 1:
                numbers[1] = int(round(base_fract_to_dec(x2, numbers[2]), 2)*100)
            else:
                numbers[1] = int(round(base_fract_to_dec(x2, 33), 2)*100)
        
            #декодирование первого символа
            x1 = code[:code.index('#')]
            if numbers[1] == 1:
                numbers[0] = base_to_dec(x1, 33)
            else:
                numbers[0] = base_to_dec(x1, numbers[1])
        except:
            return '1'

        #восстанавливаем слово
        letters = [number_to_letter(numbers[i]) for i in range(3)]
    return "".join(letters)


alg = 'Каждой букве русского алфавита ставится в соотвествие ее порядковый номер в нем. Длина \
кода для кодового замка – 21 символ (количество ячеек). Длина слова-ключа – 3 символа. В полученном \
списке цифр-номеров букв русского алфавита:\n1. Первое число переводим в систему счисления с основанием,\
равным второму числу (если второе число 1 – оставляем как есть). Запишем, начиная с первой ячейки кода. \
После поставим символ #.\n2. Последнее число переводим из десятичной в Фибоначчиеву систему счисления. На \
эту часть кода используется 7 последних ячеек. Слева могут быть незначащие нули.\n3. Второе число представим \
как дробную часть десятичной дроби, и переведем в систему счисления с основанием, равному третьему числу. \
Занимает ячейки между уже записанными числами. Если знаков меньше – заполним незначащими нулями.'

#реализация бота
import telebot

from telebot import types

bot = telebot.TeleBot('5088450087:AAGzEwXre-oIW2wlUqhk-LkX85ly1bBzU5Y')

@bot.message_handler(commands=['start'])
def welcome(message):
    #клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    button1 = types.KeyboardButton("Кодировать")
    button2 = types.KeyboardButton("Декодировать")

    markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Здравствуйте! Я могу превратить слово их 3-х русских букв \
в код для кодового замка, состоящего из латинских символов, цифр и символа \
#, а также декодировать код составленный таким образом. Введите "/alg" для вывода алгоритма кодирования.\n\
Доступно 2 команды: кодировать и декодировать. При помощи меню введите одну из них.',
                     reply_markup=markup)

@bot.message_handler(commands=['alg'])
def algorythm(message):
    global alg;
    bot.send_message(message.chat.id, alg)
  
@bot.message_handler(content_types=['text'])
def get_comand(message):
    if message.text.lower() == "кодировать":
        bot.register_next_step_handler(message, encode_message);
        bot.send_message(message.chat.id, "Введите слово из 3х русских букв")
    elif message.text.lower() == "декодировать":
        bot.send_message(message.chat.id, "Введите строку из 21го символа( латинские буквы, цифры, #)")
        bot.register_next_step_handler(message, decode_message);
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите одну из команд. "/alg" - вывод алгоритма')
            
def encode_message(message):
    if encode(message.text) == '0':
        bot.send_message(message.chat.id, 'Вы ввели не слово из 3х русских букв. Введите следующую команду.')
    else:
        bot.send_message(message.chat.id, encode(message.text))
    
def decode_message(message):
    if decode(message.text) == '0':
        bot.send_message(message.chat.id, 'В коде должен быть 21 символ (латинский алфавит и цифры) и ровно 1 символ #. Введите следующую команду.')
    elif decode(message.text) == '1':
        bot.send_message(message.chat.id, 'Данный код не мог получится по алгоритму. Введите следующую команду.')
    else:
        bot.send_message(message.chat.id, decode(message.text))


bot.polling(none_stop = True)




