class Polytope:
    def __init__(self, faces):
        self.vertices = []
        for face in faces:
            for vertex in face:
                if vertex not in self.vertices:
                    self.vertices.append(vertex)
        self.faces = [
            [self.vertices[self.vertices.index(vertex)]  for vertex in face]
            for face in faces]

    def __str__(self):
        facet_string = ""
        for face in self.faces:
            # Ugly as sin, but it works.
            facet_string += "facet_normal 0 0 0\n\touter loop\n"\
                    "\t\tvertex {}\n\t\tvertex {}\n\t\tvertex {}\n"\
                    "\tendloop\nendfacet\n".format(face[0], face[1],
                    face[2]).replace(",", "").replace("(", "")\
                    .replace(")","").replace("[","").replace("]","")
        return facet_string

    def translate(self, vector):
        # Can this be done coordinate free?
        dimension = len(vector)
        for vertex in self.vertices:
            for i in range(dimension):
                vertex[i] += vector[i]

    def scale(self, scalar):
        pass

    def __cyclic_permutations(vertex):
        return [[vertex[0], vertex[1], vertex[2]],
                [vertex[1], vertex[2], vertex[0]],
                [vertex[2], vertex[0], vertex[1]]]

    @classmethod
    def join(self, polytope_a, polytope_b):
        '''
        Given a pair of polytopes, glue them together along matching faces. Since matching
        faces are necessarily internal, we remove these faces from the resultant polytope.
        Two faces match if and only if they contain exactly the same vertices, i.e., if
        set(face_1) = set(face_2).

        FIX ME: prevent joining from creating problems with the right-hand rule.
        FIX ME: why does this need self when it's decorated as a classmethod?
        '''
        # Comput the shared faces to remove.
        a_rotations = []
        for face in polytope_a.faces:
            a_rotations += self.__cyclic_permutations(face)
        shared_faces = [face for face in polytope_b.faces if face in a_rotations]
        for face in shared_faces:
            polytope_a.faces.remove(face)
            polytope_b.faces.remove(face)

        return Polytope([[list(vertex) for vertex in list(face)] for face in polytope_a.faces + polytope_b.faces])


class Cube(Polytope):
    def __init__(self):
        faces = [ # 6 face. This is dumb, and should be done programmatically.
            [[0,0,0], [1,0,0], [0,1,0]], [[0,1,0], [1,0,0], [1,1,0]], # xy0
            [[0,0,1], [1,0,1], [0,1,1]], [[0,1,1], [1,0,1], [1,1,1]], # xy1
            [[0,0,0], [1,0,0], [0,0,1]], [[0,0,1], [1,0,0], [1,0,1]], # x0z
            [[0,1,0], [1,1,0], [0,1,1]], [[0,1,1], [1,1,0], [1,1,1]], # x1z
            [[0,0,0], [0,1,0], [0,0,1]], [[0,0,1], [0,1,0], [0,1,1]], # 0yz
            [[1,0,0], [1,1,0], [1,0,1]], [[1,0,1], [1,1,0], [1,1,1]], # 0yz
        ]
        Polytope.__init__(self, faces)

class Sponge(Polytope):
    top_bot_vectors = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0)]
    mid_vectors = [(-1,-1), (1,-1), (1,1), (-1,1)]

    all_base_vectors = []
    for vector in top_bot_vectors:
        for i in [-1, 1]:
            all_base_vectors.append([vector[0], vector[1], i])
    for vector in mid_vectors:
        all_base_vectors.append([vector[0], vector[1], 0])

    def __init__(self, stage):
        if stage > 1:
            # We need 20 n-sponges to make an (n+1)-sponge.
            pre_topes = [Sponge(stage - 1) for i in range(20)]
        else:
            # Unless we're making a 1-sponge. Then we need 20 cubes.
            pre_topes = [Cube() for i in range(20)]
        sub_topes = []
        # FIX ME: All this shifting should really be a single list comprehension/map.
        for vector in Sponge.top_bot_vectors:
            for i in [-1, 1]:
                tope = pre_topes.pop()
                tope.translate([vector[0], vector[1], i])
                sub_topes.append(tope)
        for vector in Sponge.mid_vectors:
            tope = pre_topes.pop()
            tope.translate([vector[0], vector[1], 0])
            sub_topes.append(tope)

        # We should also join and shift at the same time. This is also the dumb way to do the joining.
        tope = Polytope([])
        while sub_topes != []:
            tope = Polytope.join(tope, sub_topes.pop())

        Polytope.__init__(self, tope.faces)

if __name__ == '__main__':
    pass
#    from utils import STLWriter
#    i = input("file number: ")
#    p = Polytope([[[0,0,0],[1,0,0],[0,1,0]]], "triang")
#    p.translate([2,2,2]) 
#
#    with open("join-test-{}.stl".format(i), "w") as f:
#        tope = Polytope.join(Cube(), Cube().translate([1,0,0]))
#        f.writelines(STLWriter.print_polytopes(str(tope), "join-test"))
#        f.writelines(Polytope([[[0,0,0],[1,0,0],[0,1,0]]], "triang").__str__())
#        f.writelines(Cube().__str__())
#    topes = []
#    for vector in Sponge.top_bot_vectors:
#        topes.append(Cube().translate([vector[0], vector[1], 0]))
#        topes.append(Cube().translate([vector[0], vector[1], 2]))
#    with open("coordinate_free_translate-{}.stl".format(i), 'w') as f:
#        f.writelines(STLWriter.print_polytopes(topes, "rings_test"))
#        f.writelines(s1.__str__())
