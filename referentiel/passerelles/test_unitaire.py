# -*- coding: utf-8 -*-

import plyj.parser as plyj
import tkFileDialog
import plyj.model as m
from referentiel.passerelles.threaded_file_parser import ThreadedFileParser

class JunitParser():

    @classmethod
    def parse(self, files_list):

        if files_list == "":
            file_path_string = tkFileDialog.askopenfilename()
            files = [file_path_string]
        else:
            files = files_list
            files2 = []
            for fil in files:
                files2.append(fil)
            for fil in files:
                if not fil.endswith(".java"):
                    files2.remove(fil)
            files = files2

        json = []
        data = []
        for fil in files:
            parser = plyj.Parser()
            tree = parser.parse_file(file(fil))
            if tree is not None:
                for type_decl in tree.type_declarations:
                    for method_decl in [decl for decl in type_decl.body if type(decl) is m.MethodDeclaration]:
                        data.append(method_decl.name)
                        for body in method_decl.body:
                            if body:
                                JunitParser.recurse(body, data)
                        json.append(data)
                        data = []
        print json
        return json

    @classmethod
    def recurse(self, ast, data):
        if ast:
            # print ast
            if type(ast) == m.MethodInvocation:
                # print "method invoc  " + ast.name
                data.append(ast.name)
            if not isinstance(ast, str):
                for grandchildren in ast.__dict__:
                    if grandchildren[0] != "_":
                        attr = getattr(ast, grandchildren)
                        if attr and str(attr)[0] == "[":
                            attr = m.VariableDeclarator(str(attr)[1:-1])
                        if attr and str(attr)[0] != "[":
                            JunitParser.recurse(attr, data)

        else:
            return data



if __name__ == '__main__':
    jp = JunitParser()
    JunitParser.parse(jp,"")