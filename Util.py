##############################################################################
##|   |   |   . | .   |           |---       __   ___   |   .  __   __   __ ##
##|   | --|-- | | | --|-- \   /   |--  |  | |  | |    --|-- | |  | |  | |__ ##
##|___|   |_  | | |   |_   \_/    |    |__| |  | |___   |_  | |__| |  |  __|##
##__________________________/_______________________________________________##
##############################################################################


#Function returns unit squares that are within the bounds of matrix.
#INPUT: @rs : int-ndarray = row coordinates of polyomino(es) within matrix
#       @cs : int-ndarray = column coordinates of polyomino(es) within matrix
#       @size : int = size in terms of n of the surrounding nxn matrix
#       @flat : bool = if true -> return coordinates of flattened matrix,
#                       if false -> return coordinates of the nxn matrix
def rm_oob_idxs(rs,cs,size):
    oob_up = np.where(rs < 0)[0]
    oob_dn = np.where(rs >= size)[0]
    oob_lf = np.where(cs < 0)[0]
    oob_rt = np.where(cs >= size)[0]

    if (len(oob_up) == 0
        and len(oob_dn) == 0
        and len(oob_lf) == 0
        and len(oob_rt) == 0):
        return rs*size+cs

    oob_idxs = np.unique(np.concatenate((oob_up,oob_dn,oob_lf,oob_rt)))
    new_rs = np.delete(rs,oob_idxs)
    new_cs = np.delete(cs,oob_idxs)

    return new_rs*size+new_cs

#Function returns unit squares that are adjacent to polyomino(es).
#INPUT: @rs : int-ndarray = row indices of polyomino(es) within matrix
#       @cs : int-ndarray = column indices of polyomino(es) within matrix
#       @size : int = size in terms of n of the surrounding nxn matrix
#       @flat : bool = if true -> return indices of flattened matrix,
#                       if false -> return indices of the nxn matrix
#       @check_oob : bool = if true -> return adjacencies with inbound indices
#                           if false -> return all adjacencies regardless
def adjacent(rs,cs,size,flat=True,check_oob=True):
    up = rs-1
    dn = rs+1
    lf = cs-1
    rt = cs+1

    if check_oob:
        u = rm_oob_idxs(up,cs)
        d = rm_oob_idxs(dn,cs)
        l = rm_oob_idxs(rs,lf)
        r = rm_oob_idxs(rs,rt)
    else:
        u = up*size+lf
        d = up*size+rt
        l = dn*size+lf
        r = dn*size+rt

    flat_plymno_idxs = rs*size+cs
    adj_idxs = np.unique(np.concatenate((u,l,r,d)))
    final = adj_idxs[np.isin(adj_idxs,flat_plymno_idxs,invert=True)]
    final.sort()

    if flat:
        return final
    return (final//size,final%size)

#Function returns unit squares that are vertically adjacent to polyomino(es).
#INPUT: @rs : int-ndarray = row indices of polyomino(es) within matrix
#       @cs : int-ndarray = column indices of polyomino(es) within matrix
#       @size : int = size in terms of n of the surrounding nxn matrix
#       @flat : bool = if true -> return indices of flattened matrix,
#                       if false -> return indices of the nxn matrix
#       @check_oob : bool = if true -> return adjacencies with inbound coords
#                           if false -> return all adjacencies regardless
def diagonal(rs,cs,size,flat=True,check_oob=True):
    up = rs-1
    dn = rs+1
    lf = cs-1
    rt = cs+1

    if check_oob:
        up_lf = rm_oob_idxs(up,lf)
        up_rt = rm_oob_idxs(up,rt)
        dn_lf = rm_oob_idxs(dn,lf)
        dn_rt = rm_oob_idxs(dn,rt)
    else:
        up_lf = up*size+lf
        up_rt = up*size+rt
        dn_lf = dn*size+lf
        dn_rt = dn*size+rt

    flat_plymno_idxs = rs*size+cs
    all_idxs = np.unique(np.concatenate((up_lf,up_rt,dn_lf,dn_rt)))
    no_plymno_idxs = all_idxs[np.isin(all_idxs,board_pstns,invert=True)]
    adj_idxs = adjacent(rs,cs)
    final = no_block_pstns[np.isin(no_plymno_idxs,adj_idxs,invert=True)]
    final.sort()

    if flat:
        return final
    return (final//size,final%size)
