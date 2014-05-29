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

    def join(self, polytope):
        '''Given a polytope, glue together along matching faces. Since matching
           faces are necessarily internal, we remove these faces from the
           resultant polytope.
        '''
        self.faces.sort()
        polytope.faces.sort()
        new_faces = []

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
    top_bot_vectors = [(0,0), (1,0), (2,0), (2,1), (2,2), (1,2), (0,2), (0,1)]
    mid_vectors = [(0,0), (2,0), (2,2), (0,2)]

    def __init__(self, stage):
        self.sub_topes = []
        for vector in Sponge.top_bot_vectors:
            for i in [0, 2]:
                if stage == 0:
                    self.sub_topes.append(
                Sponge(stage - 1).translate([vector[0], vector[1], i])
        for vector in Sponge.mid_vectors:
            Sponge(stage - 1).translate([vector[0], vector[1], 1])

def stage_1():
    cubes = []
if __name__ == '__main__':
    i = input("file number: ")
#    p = Polytope([[[0,0,0],[1,0,0],[0,1,0]]], "triang")
#    p.translate([2,2,2]) 
#
#    with open("cube-test-{}.stl".format(i), "w") as f:
#        f.writelines(Polytope([[[0,0,0],[1,0,0],[0,1,0]]], "triang").__str__())
#        f.writelines(Cube().__str__())    
    s1 = Sponge(1)
    with open("menger-test-stage-one-run-{}.stl".format(i), 'w') as f:
#        f.writelines(print_polytopes(s1, "menger-sponge-1"))
        f.writelines(s1.__str__())
