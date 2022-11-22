from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value, arg):
    censor_words = ['булок', 'плюшек', 'пирожков', 'статья']  # ненормативная лексика

    ln = len(censor_words)
    filtred_text = ''
    string = ''
    pattern = '*'  # замена
    for i in value:
        string += i
        string2 = string.lower()
        flag = 0
        for j in censor_words:
            if not string2 in j:
                flag += 1
            if string2 == j:
                filtred_text += pattern * len(string)
                flag -= 1
                string = ''
        if flag == ln:
            filtred_text += string
            string = ''
    if string2 != '' and string2 not in censor_words:
        filtred_text += string
    elif string2 != '':
        filtred_text += pattern * len(string)
    return filtred_text
