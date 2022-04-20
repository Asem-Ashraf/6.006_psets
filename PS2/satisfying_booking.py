def satisfying_booking(R):
    '''
    Input:  R | Tuple of |R| talk request tuples (s, t)
    Output: B | Tuple of room booking triples (k, s, t)
              | that is the booking schedule that satisfies R
    '''
    B = []
    max=0
    for i in range(len(R)):
        if R[i][-1]>max:
            max=R[i][-1]
    hours=[0]*max
    for i in range(len(R)):
        for n in range(R[i][0],R[i][-1]):
            hours[n]+=1
    index,inner=0,0
    while(1):
        if inner==len(hours):
            B.append((hours[index], index, inner))
            break
        if hours[index]==0:
            index+=1
            inner+=1
            continue
        if hours[index]==hours[inner]:
            inner+=1
        else:
            B.append((hours[index],index,inner))
            index=inner
    return tuple(B)
