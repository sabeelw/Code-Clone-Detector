import pycparser.c_ast
from db_connector import Connector
from pycparser import parse_file, c_generator, c_ast
import os
import sys
currentDir = os.getcwd()
os.chdir("/home/anonymous/Downloads/programs/ProgramData/41")
dir_list = os.listdir()
print(dir_list)
os.chdir(currentDir)


def generate_type1(code):
    pass

def generate_type2(code):
    pass

def generate_type3(code):

     for filename in dir_list:
        source = open(f"/home/anonymous/Downloads/programs/ProgramData/41/{filename}", 'r')
        destination = open("../source_files/temp.c", 'w')
        sourceRead = source.read()
        destination.write(sourceRead)
        del sourceRead
        destination.close()
        source.close()
        code = parse_file("../source_files/temp.c", use_cpp=True,
                          cpp_path='gcc',
                          cpp_args=['-E',
                                    r'-I/home/anonymous/Downloads/pycparser/utils/fake_libc_include'])
        for i in code.ext:
            if type(i) == pycparser.c_ast.FuncDef:
                if i.decl.name != "main":
                    generator = c_generator.CGenerator()
                    print(generator.visit(i))
                    function_code = generator.visit(i)
                    dbObj = Connector('localhost', 'postgres', 'google', 'clones_db')
                    dbObj.connect("function_codes")
                    data = [
                        {
                            'code': function_code,
                            'lang': "c",

                        }
                    ]

                    dbObj.add(data)






