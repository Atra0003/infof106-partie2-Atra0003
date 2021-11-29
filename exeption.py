
def trace(M):
    try:
        dimention = len(M)
        res = 0
        for i in range(dimention):
            if dimention != len(M[0]):
                raise IndexError
            res += M[i][i]
    except IndexError:
        print("la matrice n'est pas carré")
        res = None
    except TypeError:
        print("M n'est pas une matrice correct")
        res = None
    except:
        print("erreur non connue")
        res = None
    return res 
        




print(trace([[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]))