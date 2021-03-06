def compare(str, sample):
    i = 0 #нумератор строки
    j = 0 #нумератор шаблона
    if(str == ""): #проверка для пустой строки
        for s in sample:
            if(s != "%"):
                return "NO"
    length = len(sample) #найдем длину сэмпла
    k = 1
    while k < length: #превращяем все ряды процентов в один процент
        if(sample[k] == "%" and sample[k-1] == "%"):
            sample = sample[:k-1] + sample[k:]
            length -= 1
            k -= 1
        k +=1
    while i < len(str): #идем по строке
        if(j >= len(sample)): return "NO" #недопуск переполнения индекса
        if ((str[i] == sample[j] and sample[j] != "[" and sample[j] != "%") or sample[j] == "_"): #символы совпадают или есть _
            if(str[i] == chr(39) and sample[j] == "_"):
                i += 2
            else:
                i += 1
            j += 1
        elif (str[i] != sample[j] and sample[j] != "[" and sample[j] != "_" and sample[j] != "%"): #если ничего не совпадает и нет спец символов
            return "NO"
        elif (sample[j] == "%"): #обрабатываем процент
            if (i > abs(len(str) - len(sample[j:]))):
                j += 1
                length -= 1
            else:
                i += 1
        elif (sample[j] == "["):
            formula = ""
            l = j
            j += 1
            while (sample[j] != "]" and j != l):
                formula += sample[j]
                j += 1
                if j == len(sample):
                    if(sample[l] != str[i]): return "NO"
                    else:
                        j = l
                        formula = ""
            if (j == l):
                j += 1
                if (str[i] == chr(39)):
                    i += 2
                else:
                    i += 1
            else:
                length -= (len(formula) + 1)
                if (len(formula) == 1):
                    if (str[i] == formula):
                        j += 1
                        if (str[i] == chr(39)):
                            i += 2
                        else:
                            i += 1
                    else:
                        return "NO"
                elif (len(formula) == 0):
                    j += 1
                    length -= 1
                elif (len(formula) == 2):
                    if(formula[0] == "^" and formula[1] != str[i]):
                        j += 1
                        if (str[i] == chr(39)):
                            i += 2
                        else:
                            i += 1
                    elif (formula[0] == str[i] or formula[1] == str[i]):
                        j += 1
                        if (str[i] == chr(39)):
                            i += 2
                        else:
                            i += 1
                    else:
                        return "NO"
                else:
                    log = 0
                    anti = 1
                    if (formula[0] == "^"):
                        anti = 0
                        formula = formula[1:]
                    while (formula != "" and log == 0):
                        subformula = ""
                        if(len(formula)>=3):
                            if (formula[1] == "-" and formula[2] != "-"):
                                subformula = formula[:3]
                                formula = formula[3:]
                                if(anti):
                                    if (ord(subformula[0]) <= ord(str[i]) and ord(str[i]) <= ord(subformula[2])):
                                        log = 1
                                else:
                                    if (ord(subformula[0]) <= ord(str[i]) and ord(str[i]) <= ord(subformula[2])):
                                        return "NO"
                            else:
                                subformula = formula
                                formula = ""
                                if(anti):
                                    for symb in subformula:
                                        if (symb == str[i]):
                                            log = 1
                                else:
                                    for symb in subformula:
                                        if (symb == str[i]):
                                            return "NO"
                        else:
                            subformula = formula
                            formula = ""
                            if (anti):
                                for symb in subformula:
                                    if (symb == str[i]):
                                        log = 1
                            else:
                                for symb in subformula:
                                    if (symb == str[i]):
                                        return "NO"
                    if (log == 1):
                        if(str[i] == chr(39)):
                            i += 2
                        else:
                            i += 1
                        j += 1
    if(length > len(str)):
        while length != len(str):
            if(sample[length-1] == "%"):
                length -= 1
            else:
                return "NO"
    return "YES"

def pref_func(str): #просто префикс функция
    p = [0] * len(str)
    for i in range(1, len(str)):
        j = p[i - 1]
        while j > 0 and str[i] != str[j]:
            j = p[j - 1]
        if str[i] == str[j]:
            j += 1
        p[i] = j
    return p

N = int(input()) #число строк
for i in range(N):
    command = input() #вводим строку
    likes = [0]*100 #будем считать какой like наш, их может быть много, берем тот что по середнине
    p = pref_func("' like '" + chr(256) + command)
    u = 0
    for k in range(len(p)):
        if p[k] == len("' like '"):
            likes[u] = k-2*len("' like '")
            u += 1
    likes = [i for i in likes if i != 0] #позиции всех лайков в строке
    str = command[1:likes[len(likes)//2]] #выделяем что из этого строка а что шаблон
    sample = command[likes[len(likes)//2] + len("' like '"):len(command) - 1]
    if(i < N - 1):
        print(compare(str, sample)) #делаем функцию
    else:
        print(compare(str, sample), end="")