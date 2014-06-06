import struct

class STLWriter:
    # print_polytopes is a class, not instance method
    def print_polytopes(polytopes, name):
        polytope_string = ""
        for polytope in polytopes:
            polytope_string += polytope.__str__()
        return "solid {}\n\n".format(name) + polytope_string\
                   + "endsolid {}\n".format(name)

    def unpack(self, filename):
        triangle_unpacker = struct.Struct("3f3f3f3fH").unpack
        triangles = []
        with open(filename, 'rb') as file:
            name, triangle_count = struct.unpack("80sI", file.read(struct.calcsize("80sI")))
            for i in range(len(triangle_count)):
                triangles.append([])

def test_encoding():
    cubes = []

if __name__ == '__main__':
    test_encoding()
