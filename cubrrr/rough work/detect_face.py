
def find_squares(sq_col, sq_wh):
    # width height of a square; default to high number 
    w_h = [20000, 20000]

    # create 2D array filled with high number tuples by default
    xy = [[(20000, 20000)]*3 for i in range(3)]
    col = [["-"]*3 for i in range(3)]

    # create list of keys and then sort by y value in increasing order
    xy_keys = [*sq_col]
    xy_keys = sorted(xy_keys, key=lambda x: [x[1], x[0]])

    # insert into 2D list and sort by x value, and find the smallest width height of a square
    temp_index = 0
    for i in range(3):
        for j in range(3):
            xy[i][j] = xy_keys[temp_index]

            #set w_h to lowest width height possible
            w_h[0] = sq_wh[xy_keys[temp_index]][0] if sq_wh[xy_keys[temp_index]][0] < w_h[0] else w_h[0]
            w_h[1] = sq_wh[xy_keys[temp_index]][1] if sq_wh[xy_keys[temp_index]][1] < w_h[1] else w_h[1]

            if temp_index < len(xy_keys)-1:
                temp_index += 1
            else: 
                break
        # sort by x
        xy[i] = sorted(xy[i], key=lambda x: [x[0], x[1]])
        
        # create the 2D colour array
        for j in range(3):
            col[i][j] = sq_col[xy[i][j]] if xy[i][j] != (20000, 20000) else "-"
    
    # fix "-" spots in 2D colour array: only needed for stickered cubes
    
    # for r in range(3):
    #     for c in range(3):
    #         if xy[r][c] != (20000, 20000):
    #             colour = col[r][c]          #colour of current square

    #             w = sq_wh[xy[r][c]][0]      #width and height of current square
    #             h = sq_wh[xy[r][c]][1]

    #             ex_w = w//w_h[0]            #check if its long or wider than it should be
    #             ex_h = h//w_h[1]
    #             # print(w, ex_w, h, ex_h)
                
    #             #extend the colours in the right direction
    #             if ex_w > 1: 
    #                 col[r][c + ex_w - 1] = colour
    #                 ex_w -= 1

    #             if h//w_h[1] > 1:
    #                 col[r + ex_h - 1][c] = colour
    #                 ex_h -= 1
    #         else: 
    #             #fix the (20000, 20000) thing and give it an acc coord if you want lol
    #             pass
    return col


if __name__ == "__main__":
    # sq_col = {(185, 177): 'Red', (66, 178): 'Blue', (125, 236): 'Green', (127, 177): 'Yellow', (185, 117): 'Yellow', (63, 118): 'Orange', (68, 237): 'White', (123, 114): 'White'}
    # sq_wh = {(185, 177): (57, 116), (66, 178): (58, 61), (125, 236): (59, 57), (127, 177): (56, 59), (185, 117): (59, 59), (63, 118): (61, 60), (68, 237): (58, 56), (123, 114): (61, 63)}

    sq_col = {(120, 257): 'Red', (59, 129): 'Red', (184, 128): 'Blue', (122, 190): 'Yellow', (186, 189): 'Yellow', (187, 255): 'Orange', (121, 129): 'White'}
    sq_wh = {(120, 257): (67, 64), (59, 129): (61, 191), (184, 128): (64, 62), (122, 190): (63, 65), (186, 189): (63, 67), (187, 255): (61, 65), (121, 129): (62, 61)}

    col = find_squares(sq_col, sq_wh)

    print("-------------")    
    print(col)
    print("-------------")





