class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices

    def subdivide(self):
        pass

    def to_ascii_stl(self):
        return "facet normal 0 0 0\n\touter loop\n\t\tvertex {0}\n" \
              "\t\tvertex {3}\n\t\tvertex {6}\n\tendloop"\
              "endfacet".format(self.vertices[0], self.vertices[1],
                                self.vertices[2])
            
