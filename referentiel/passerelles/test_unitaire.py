# -*- coding: utf-8 -*-

import tkFileDialog
import plyj.parser as plyj
import plyj.model as m
from referentiel.passerelles.threaded_file_parser import ThreadedFileParser

class JunitParser():

    def parse(self, path_value):

        if path_value == "":
            file_path_string = tkFileDialog.askopenfilename()
            files = [file_path_string]
        else:
            files = path_value
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
            parser = ThreadedFileParser(file(fil))
            tree = parser.run()
            if tree is not None:
                for type_decl in tree.type_declarations:
                    for method_decl in [decl for decl in type_decl.body if type(decl) is m.MethodDeclaration]:
                        data.append(method_decl.name)
                        for body in method_decl.body:
                            if body:
                                self.recurse(body, data)
                        json.append(data)
                        data = []
        print json
        return json

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
                            self.recurse(attr, data)

        else:
            return data



if __name__ == '__main__':
    jp = JunitParser()
    JunitParser.parse(jp,"")