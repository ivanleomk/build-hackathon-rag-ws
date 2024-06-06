def get_rr_at_index(desired_index,length=20):
    return rr([0 if i != desired_index else 1 for i in range(length)],1)

prev_rr = 1.0
for i in range(5):
    curr_rr = get_rr_at_index(i)
    decrease = prev_rr - curr_rr
    print(f"{' '*(7*i)}{curr_rr:.2f} ---|(-{decrease:.2f}){'another':(7*(i+1))}")
    print("|".rjust(35))    
    prev_rr = curr_rr

