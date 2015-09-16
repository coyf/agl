import os
import json
from passerelles.use_case import UsecaseParser
from kivy.uix.treeview import TreeViewLabel, TreeView

class Reference(object):
    """
        Represent the reference document
    """

    referentiel_tree = None
    ref_path = ""
    project_name = ""

    def __init__(self, absolute_path="", project_name="New project"):
        # self.ref_path = os.path.join(absolute_path, 'referentiel', project_name + '.ref.json')
        # STUB : example's ref.json
        self.ref_path = os.path.join(absolute_path, 'referentiel', project_name + '.ref.json')

        self.project_name = project_name
        self.referentiel_tree = TreeView(hide_root=True)
        if os.path.isfile(self.ref_path):
            self.load_json()
        else:
            self.create_json()

    def create_json(self):
        """
        Create the json file
        :return: void
        """
        ref = open(self.ref_path, 'a+')
        json.dump({"name" : self.project_name, "children" : []}, ref, sort_keys=True, indent=4, separators=(',', ': '))
        ref.close()

    def insert_use_cases(self, uc_list):
        """
        Insert all use cases given in parameter inside the ref.json
        :param uc_list: list of use_case which have to be insert into the file
        :return: 1 if something changed, 0 if not
        """
        change = 0

        ref = open(self.ref_path, 'r')
        data = json.load(ref)
        ref.close()

        for uc in uc_list:
            if not any(d['name'] == uc for d in data['children']):
                change = 1
                data['children'].append({'name' : uc, 'type' : 'Use-case', 'children' : []})
            else:
                pass

        if change == 1:
            ref = open(self.ref_path, 'w')
            print data
            json.dump(data, ref, sort_keys=True, indent=4, separators=(',', ': '))
            ref.close()

        return change



    def insert_diag_concept(self, dc_list):
        """
        Insert all design diagrams given in parameter inside the ref.json
        :param uc_list: list of diagrams which have to be insert into the file
        :return: 1 if something changed, 0 if not
        """
        change = 0

        ref = open(self.ref_path, 'r')
        data = json.load(ref)
        ref.close()

        for dc in dc_list:
            uc_name = dc[0]

            for uc in data['children']:
                if uc['name'] == uc_name:
                    for dc_e in dc[1:]:
                        if not any(d['name'] == dc_e for d in uc['children']):
                            change = 1
                            uc['children'].append({'name' : dc_e, 'type' : 'Class', 'children' : []})

        if change == 1:
            ref = open(self.ref_path, 'w')
            print data
            json.dump(data, ref, sort_keys=True, indent=4, separators=(',', ': '))
            ref.close()

        return change

    def load_json(self):
        """
        Load the ref.json on memory to make the print easier and improve the program speed
        :return:
        """
        self.referentiel_tree = TreeView(hide_root=True)
        ref = open(self.ref_path, 'r')
        data = json.load(ref)
        ref.close()
        Reference.populate_tree(self.referentiel_tree, None, data)
        return self.referentiel_tree

    def get_tree(self):
        return self.referentiel_tree

    @classmethod
    def populate_tree(cls, tree_view, parent, node):
        try:
            if parent is None:
                tree_node = tree_view.add_node(TreeViewLabel(text=node['name'], is_open=True))
            else:
                tree_node = tree_view.add_node(TreeViewLabel(text=node['name'], is_open=True), parent)
            for child_node in node['children']:
                Reference.populate_tree(tree_view, tree_node, child_node)
        except KeyError as e:
            print "ref populate tree error : {}".format(e.message)

