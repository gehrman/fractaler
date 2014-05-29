class STLWriter:
    def print_polytopes(polytopes, name):
        polytope_string = ""
        for polytope in polytopes:
            polytope_string += polytope.__str__()
        return "solid {}\n\n".format(name) + polytope_string\
                   + "endsolid {}\n".format(name)
    

def test_encoding:
    cubes = []

if __name__ == '__main__':
    test_encoding()
