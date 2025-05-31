
def number_to_words(num):
    if num == 0:
        return 'ноль'
    
    units = ['', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    teens = ['десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 
             'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать']
    tens = ['', '', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 
            'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']
    hundreds = ['', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот',
                'шестьсот', 'семьсот', 'восемьсот', 'девятьсот']
    
    def convert_less_than_thousand(n, is_female=False):
        if n == 0:
            return ''
        words = []
        if n >= 100:
            words.append(hundreds[n // 100])
            n %= 100
        if n >= 20:
            words.append(tens[n // 10])
            n %= 10
        if 10 <= n < 20:
            words.append(teens[n - 10])
        elif n > 0:
            if is_female and n in [1, 2]:
                words.append(['одна', 'две'][n - 1])
            else:
                words.append(units[n])
        return ' '.join(words)
    
    scales = [
        ('', '', '', False),
        ('тысяча', 'тысячи', 'тысяч', True),
        ('миллион', 'миллиона', 'миллионов', False),
        ('миллиард', 'миллиарда', 'миллиардов', False),
    ]
    
    words = []
    scale_index = 0
    remaining = num
    
    for scale in scales:
        scale_name_one, scale_name_few, scale_name_many, is_female = scale
        chunk = remaining % 1000
        remaining = remaining // 1000
        
        if chunk > 0:
            chunk_words = convert_less_than_thousand(chunk, is_female)
            if chunk_words:
                if 11 <= chunk % 100 <= 19 or chunk % 10 in [0, 5, 6, 7, 8, 9]:
                    scale_word = scale_name_many
                elif chunk % 10 == 1:
                    scale_word = scale_name_one
                else:
                    scale_word = scale_name_few
                words.append(f"{chunk_words} {scale_word}" if scale_word else chunk_words)
    
    return ' '.join(reversed(words)).strip()

def money_to_words(amount):
    rubles = int(amount)
    kopecks = round((amount - rubles) * 100)
    
    ruble_words = number_to_words(rubles)
    ruble_format = None
    kopek_num = f"{kopecks:02d}"  # Копейки числом (двузначный формат)
    
    # Склонение рублей
    if rubles % 100 in [11, 12, 13, 14] or rubles % 10 in [0, 5, 6, 7, 8, 9]:
        ruble_format = 'рублей'
    elif rubles % 10 == 1:
        ruble_format = 'рубль'
    else:
        ruble_format = 'рубля'
    
    return f"{ruble_words}", ruble_format, f"{kopek_num} копеек"  # Копейки числом