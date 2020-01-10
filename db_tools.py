from random import randint
from neo4j import GraphDatabase as GDB
from packages.cleaning.data_object import DataObj

class GDBCom():

    verbosity = True
    cache_commands = []
    graphDB_Driver = None


    def __init__(self):
        pass

    def setup(self):
        uri             = "bolt://localhost:7687"
        user_name        = "neo4j"
        password        = "morphius4j"
        self.graphDB_Driver  = GDB.driver(uri, auth=(user_name, password))

    def print_progress(self, _msg):
        if self.verbosity: print(f'progress: {_msg}')

   
    def delete_all(self):
        self.cache_commands.append('match (x) detach delete x')


    def cache_execute(self, _single_transaction):
        with self.graphDB_Driver.session() as GDBS:

            if _single_transaction:
                cmd = ""
                for item in self.cache_commands:
                    cmd += f" {item} "
                GDBS.run(cmd)
                self.print_progress(f"executed: \n {cmd}")
            else:
                for cmd in self.cache_commands:
                    GDBS.run(cmd)
                    self.print_progress(f"executed: \n {cmd}")
                self.cache_commands.clear()
            GDBS.close()

    def execute_return(self, cmd):
        with self.graphDB_Driver.session() as GDBS:
            result: neo4j.BoltStatementResult = GDBS.run(cmd)
            return result.data()

    def create_tweet_node(self, alias:str, obj:DataObj, level:int, mode="queue"):
        command = f'''
            CREATE (alias{alias}:level_{level})
            SET alias{alias}.unique_id = '{obj.unique_id}'
            SET alias{alias}.name = '{obj.name}'
            SET alias{alias}.text = '{obj.text}'
        '''

        # // Be able to either send cmd to queue or return for further processing.
        valid_modes = ["queue", "return"]
        if mode not in valid_modes: 
            print_progress(f"Invalid mode: {mode}. Aborting.")
            return
        if mode == "queue":
            self.cache_commands.append(command)
        elif mode == "return":
            return command

    def convert_n4jdata_to_dataobj(self, data, label):
        neo4j_node = data.get(label)
        unique_id = neo4j_node["unique_id"]
        name = neo4j_node["name"]
        text = neo4j_node["text"]

        new_dataobj = DataObj()
        new_dataobj.unique_id = unique_id
        new_dataobj.name = name
        new_dataobj.text = text
        return new_dataobj


    def get_dataobjects_from_node_by_id(self, ids:list) -> list:
        default_label = "node"
        collection = []

        for id in ids:
            command = f"""
                MATCH (node)
                WHERE ID(node) = {id}
                RETURN {node}
            """
            neo4j_data = self.execute_return()
            new_dataobj = self.convert_n4jdata_to_dataobj(neo4j_data,default_label)

        return collection





    def create_initial_ring(self, dataobjects: list) -> None:
        # // Note about connecting nodes:
        #   - Could be done by creating nodes here
        #   - Could be done by merging create string with connector string
        #   - Could be done by doing match. Might be slow though..

        cmd = ""
        id_last = None
        for i, obj in enumerate(dataobjects):
            cmd += self.create_tweet_node(str(i), obj, 0, "return")
            if id_last != None:
                cmd += f"\tCREATE (alias{id_last})-[con{i}:TICK]->(alias{i})"
            id_last = i
            cmd += "\n"

        # // connect last to first
        cmd += f"\tCREATE (alias{0})-[con{len(dataobjects)}:TIE]->(alias{id_last})"

        self.cache_commands.append(cmd)

    def get_ring_root(self):
        cmd = """
            MATCH (strt:level_0)-[tie_r:TIE]->(last:level_0)
            MATCH (strt)-[tick_r:TICK*]-(connected)
            RETURN connected
        """
        result = self.execute_return(cmd)
        return result



    def get_ring_below_node(self, connector_id):
        pass

    def create_node_adjacent(self, obj_last, obj_new):
        # // consider ties also @@@
        # // Find node.
        cmd = f"""
            MATCH (aliasnode_last)
            WHERE aliasnode_last.unique_id = '{obj_last.unique_id}'

        """
        # // new node.
        ### @@@ FIX LEVEL
        cmd += self.create_tweet_node("node_new", obj_new, 1, "return")
        # // Connect
        cmd += f"\tCREATE (aliasnode_last)-[con:TICK]->(aliasnode_new)"
        self.cache_commands.append(cmd)

    def create_node_below(self, obj_above, new_obj):
        cmd = f"""
            MATCH (node_above)
            WHERE node_above.unique_id = '{obj_above.unique_id}'

        """
        ### @@@ FIX LEVEL 
        cmd += self.create_tweet_node("node_below", new_obj, 1, "return")
                                    
        cmd += f"""
            CREATE (node_above)-[_:DOWN]->(aliasnode_below)
        """
        self.cache_commands.append(cmd)


    def get_node_below(self, obj, mode="dataobj"):
        cmd = f"""
            MATCH (node_above), (node_below)
            WHERE node_above.unique_id = '{obj.unique_id}'
            AND (node_above)-[:DOWN]->(node_below)
            RETURN node_below
        """
        result = self.execute_return(cmd)

        valid_modes = ["dataobj", "neo4jobj"]
        if mode not in valid_modes:
            print_progress(f"Invalid mode: {mode}. Aborting.")
            return 
        if mode == "dataobj":
            if result:
                return self.convert_n4jdata_to_dataobj(result[0], "node_below")
            else:
                return None
        elif mode == "neo4jobj":
            # // return a list of neo4j dict
            return result


    def get_ring_from_top_obj(self, obj):
        cmd = f"""
            MATCH (strt)
            WHERE strt.unique_id = '{obj.unique_id}'
            MATCH (strt)-[tick_r:TICK*]-(connected)
            RETURN connected
        """
        # // return list of dataobjects
        result = self.execute_return(cmd)
        return [self.convert_n4jdata_to_dataobj(o, "connected") for o in result ]
        

    def assign_new_node(self, new_obj):
        pass
        # // probably recursive?
        
        # // high_node = Find node with highest score
        # // node_below = Get node below hight_node.
        # // Does it exist?
        # // No:
        # //    create node_below and return
        # // Yes: 
        # //     ring_size = get ring size of node_below
        # //     is ringsize > size limit?
        # //     No:
        # //        Attach new node at the end of current ring
        # //     Yes:
        # //        Do recursion with this ring




    




        


  



def test():
    db = GDBCom()
    db.setup()
    db.delete_all()
    db.test_combine()
    #db.test_ring(1000)
    db.cache_execute(_single_transaction = False)
