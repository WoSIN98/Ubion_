def mean(*_ags):
    sum_val = 0
    cnt = 0                 
    for val in _ags:        
         sum_val += val      
         cnt += 1           
    result = sum_val / cnt
    return result
