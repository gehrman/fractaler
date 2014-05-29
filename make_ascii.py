# FIX ME!
def orient(triangle):
    v1, v2, ref_axis = [], [], []
    for i in range(len(triangle[0])):
        v1.append(triangle[1][i] - triangle[0][i])
        v2.append(triangle[2][i] - triangle[0][i])
        ref_axis.append(0)
    # Reference axis is the zero vector, we want [1, 0, …]. Fix that.
    ref_axis[0] = 1

    # Recall that <x, y> = |x| |y| cos a.

def faces(points):
    def face(triangle):
        return "facet normal 0 0 0\n\touter loop\n{0}\n\tendloop"\
               "\nendfacet".format(vertices(triangle))

    for i in range(len(points))
