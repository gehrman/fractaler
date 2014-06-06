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
        #print(self.vertices)
        #print(self.faces)

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
#        print(self.vertices)
#        print(self.faces)

    def scale(self, scalar):
        pass

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
        a_faces = [set([tuple(vertex) for vertex in face]) for face in polytope_a.faces]
        b_faces = [set([tuple(vertex) for vertex in face]) for face in polytope_b.faces]

        # Shared faces to remove.
        shared_faces = [face for face in a_faces if face in b_faces]
        for face in shared_faces:
            a_faces.remove(face)
            b_faces.remove(face)

        return Polytope([list(face) for face in a_faces + b_faces])


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

    def __init__(self, stage):
        self.sub_topes = []
        for vector in Sponge.top_bot_vectors:
            for i in [-1, 1]:
                if stage == 0:
                    self.sub_topes.append(
                Sponge(stage - 1).translate([vector[0], vector[1], i]))
        for vector in Sponge.mid_vectors:
            Sponge(stage - 1).translate([vector[0], vector[1], 0])

def stage_1():
    cubes = []

if __name__ == '__main__':
    from utils import STLWriter
    i = input("file number: ")
#    p = Polytope([[[0,0,0],[1,0,0],[0,1,0]]], "triang")
#    p.translate([2,2,2]) 
#
    with open("join-test-{}.stl".format(i), "w") as f:
        tope = Polytope.join(Cube(), Cube().translate([1,0,0]))
        f.writelines(STLWriter.print_polytopes(str(tope), "join-test"))
#        f.writelines(Polytope([[[0,0,0],[1,0,0],[0,1,0]]], "triang").__str__())
#        f.writelines(Cube().__str__())
#    topes = []
#    for vector in Sponge.top_bot_vectors:
#        topes.append(Cube().translate([vector[0], vector[1], 0]))
#        topes.append(Cube().translate([vector[0], vector[1], 2]))
#    with open("coordinate_free_translate-{}.stl".format(i), 'w') as f:
#        f.writelines(STLWriter.print_polytopes(topes, "rings_test"))
#        f.writelines(s1.__str__())
