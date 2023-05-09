from . import jalali

def jalali_converter(time):
    shamsi_months=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']
    time_to_str=f'{time.year},{time.month},{time.day}'
    time_to_tpl=jalali.Gregorian(time_to_str).persian_tuple()
    time_to_lis=list(time_to_tpl)
    for index,month in enumerate(shamsi_months):
        if time_to_lis[1]==index+1:
            time_to_lis[1]=month
            break
    converted_time=f'{time_to_lis[2]} {time_to_lis[1]} {time_to_lis[0]} ساعت {time.hour}:{time.minute}'

    return converted_time