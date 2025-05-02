import random
import math
import rat
import discord
from datetime import datetime
from pytz import timezone

def get_response(msg_data, message: str) -> str:
    p_message = message.lower()
    
    if p_message == '!rat':

        number = random.randint(1, 2)
        rat_gif = rat.get_rat(number) # roll random number, choose random rat gif

        return rat_gif

    if p_message == '!randrat':

        # roll number, check if it matches today date, win if does, lose if not
        number = random.randint(1, 2)
        pst_timezone = timezone('US/Pacific')
        datetime_pst = datetime.now(pst_timezone)
        curr_day = datetime_pst.day
        
        prelim_msg = ''
        if f'{number}' == curr_day:
            prelim_msg = f'CONGRATS YOU GOT THE CORRECT DAY!!!! TODAY IS THE {number}ST OF THE MONTH'
        else:
            prelim_msg = f'unfortunately it is not the {number}nd of the month.... here is the rat gif anyways!!'

        rat_gif = rat.get_rat(number)
        final_msg = f'{prelim_msg} {rat_gif}'

        return rat_gif