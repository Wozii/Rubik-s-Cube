
def double_turns(move):
    bruh = ["r'", "r", "l", "l'", "M", "M'"]
    convert = [{'R': 1, 'L': 2, 'U': 6, 'D': 5, 'F': 3, 'B': 4},
               {'R': 1, 'L': 2, 'U': 5, 'D': 6, 'F': 4, 'B': 3}]
    return convert[bruh.index(move)]



def notation(algo):
    solution = []
    bruh = ['r', 'l', 'u', 'd', 'f', 'b']

    moves = algo.split()

    for i in range (len(moves)):        
        ard_algo = {'R': 1, 'L': 2, 'U': 3, 'D': 4, 'F': 5, 'B': 6}
        mult = 1
        move = moves[i][0]

        try: 
            index = bruh.index(move)
        except:
            index = -1
        
        if len(moves[i]) > 1:
            if moves[i][1] == '2':
                mult = 2
            else: 
                mult = -1
        
        if index != -1:
            if mult == -1: 
                ard_algo = double_turns(moves[i])
            else: 
                ard_algo = double_turns(move)
        
        solution.append(str((ard_algo[move]*1000 + abs(mult)*100) * mult//abs(mult)))

    return solution

    # print(move, mult)
    # print(ard_algo[cube_algo.index(move)])
    # print(str(int(mult)*100))
    # print(int(ard_algo[cube_algo.index(move)] + str(int(mult)*100)))

if __name__ == "__main__":
    print(notation("R' U' L' B' D' R2 L2"))