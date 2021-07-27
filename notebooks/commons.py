from enum import Enum

default_stats = {
    'main_character': {
        'hp': 100,
        'mp': 100,
        'strength': 10,
        'defense': 10,
        'agility': 10
    },
    'skeleton': {
        'hp': 10,
        'mp': 10,
        'strength': 2,
        'defense': 2,
        'agility': 2
    }
}

class Node:
    def __init__(self, data):
        self.data = data # Node Value
        self.next = None # Next Node
        self.prev = None # Previous Node

class LinkedList:    
    def __init__(self):
        self.head = None # Head Node, pop from head for queue
        self.tail = None # Tail Node, pop from tail for stack
        self.indices = {} # Dictionary containing indices, key of id, value of node
    
    def printList(self):
        temp = self.head
        while(temp):
            print(temp.data)
            temp = temp.next

    def create_node(self, node_value, curr_id):
        curr_node = Node(node_value)
        self.indices[curr_id] = curr_node
        return curr_node

    def push(self, node_value_to_push, is_ll=False, curr_id=None):
        if not is_ll: # If node to push is not a LL
            curr_node = self.create_node(node_value_to_push, curr_id)
        else: # If node is already created and part of another LL, then keep existing links and nodes, and push this tail to the tail of new LL
            print('***LinkedList', node_value_to_push, is_ll, curr_id)
            curr_node = node_value_to_push

        if self.tail is not None: # If one or more blocks exist in linked list, point tail to new node
            self.tail.next = curr_node
            if self.head.next is None: # If only one block in linked list, point head to new node
                    self.head.next = curr_node
        else:
            self.head = curr_node # If tail doesn't exist, make new node the head
        curr_node.prev = self.tail
        self.tail = curr_node # Make new node the tail
   
    def pop_stack(self): # Remove last node / tail from linked list
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
    
    def pop_queue(self): # Remove first node / head from linked list
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
    
    def pop_all(self):
        temp = self.head
        while(temp):
            if temp.next is not None:
                temp.next = temp.next.next
            else:
                temp = None
                self.tail = None
                self.head = None
    
    def pop_indexed_node(self, curr_id):
        node_to_pop = self.indices[curr_id]
        next_node = node_to_pop.next
        prev_node = node_to_pop.prev
        if prev_node is not None and next_node is not None: # If node that is being popped is not the head nor tail
            print('+')
            prev_node.next = next_node
            next_node.prev = prev_node
        elif next_node is None: # If node that is being popped is the last node in the LL
            print('++')
            self.pop_stack()
        elif prev_node is None: # If node that is being popped is the first node in the LL
            print('-')
            self.pop_queue()    
        node_to_pop = None

class Point:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.point = point
    
    def move_point(self, movement):
        self.x += movement.x
        self.y += movement.y
        self.point = (self.x,self.y)

class PointCategories(Enum):
    pc = 'playable_character'
    npc = 'non_playable_character'
    item = 'item'
    path = 'path'
    obstacle = 'obstacle'

class Ids:
    class CatIds:
        def __init__(self, ids=None, max_id = 0):
            self.max_id = max_id
            self.ids = ids # Dictionary, key: personId, value: Person object

        def add_id(self, obj_to_add):
            curr_max_id = self.max_id
            if type(self.ids) is not dict:
                self.ids = {}
            self.ids[curr_max_id] = obj_to_add
            self.max_id += 1
            return curr_max_id
    
    def __init__(self):
        self.pc_Ids = self.CatIds()
        self.npc_Ids = self.CatIds()
        self.item_Ids = self.CatIds()
        self.path_Ids = self.CatIds()
        self.obstacle_Ids = self.CatIds()

class PointCategoriesObj:
    def __init__(self):
        # self.pointCategories = PointCategories
        # for name, member in self.pointCategories.__members__.items():
        #     member.queue = LinkedList()
        self.pointCategories = {}
        for name, member in PointCategories.__members__.items():
            self.pointCategories[name] = LinkedList()
    
    def add_to_pointCategories(self, dict_to_add): # Use this when adding to the LL in pointCategories, and not replacing
        for name, member in PointCategories.__members__.items():
            print('***add_to_pointCategories', name, dict_to_add[name].head, dict_to_add[name].tail)
            curr_tail = dict_to_add[name].tail
            if curr_tail is not None:
                self.pointCategories[name].push(dict_to_add[name].tail, is_ll=True)

    def remove_id_from_pointCategories(self, curr_cat, id_to_remove):
        # curr_cat_LL = obj_to_remove.pointCategories[key]
        # id_to_remove = obj_to_remove.id
        curr_cat_LL = self.pointCategories[curr_cat]
        curr_cat_LL.pop_indexed_node(id_to_remove)

    def check_pointCategories_isEmpty(self):
        isEmpty = False
        for key, item in self.pointCategories.items(): # Check if any category is empty
            if item is None or item == {}:
                isEmpty = True
                return isEmpty
        return isEmpty

class Map:        
    def __init__(self, max_x=200, max_y=200, points={}):
        self.max_x = max_x
        self.max_y = max_y
        self.points = points # Dictionary with format, {Point(n,n): self.pointCategories.pc: mapPoint.persons ..., ...}
        print('***self.points', self.points)
    
    def add_to_points(self, obj_to_add):
        curr_point = obj_to_add.curr_pos
        curr_cat = obj_to_add.pointCategory
        curr_id = obj_to_add.id
        if self.points.get(curr_point.point) is None:
            mapPoint = PointCategoriesObj()
            print('***mapPoint', mapPoint)
            self.points[curr_point.point] = mapPoint # Map.points[(101,101)].PointCategoriesOb()
        print('***add_to_points', curr_point.point, curr_cat.name, curr_id)
        self.points[curr_point.point].pointCategories[curr_cat.name].push(obj_to_add, curr_id=curr_id)
    
    def remove_from_points(self, obj_to_remove):
        curr_point = obj_to_remove.curr_pos.point
        curr_cat = obj_to_remove.pointCategory.name
        curr_id = obj_to_remove.id
        self.points[curr_point].remove_id_from_pointCategories(curr_cat, curr_id)
        point_isEmpty = self.points[curr_point].check_pointCategories_isEmpty()
        return point_isEmpty

class Encounter:
    def __init__(self, encounterCategories=None, curr_map=None, curr_point=None):
        # These will be specific to each person as it's a parameter in the person class
        # self.encounterCategories = PointCategoriesObj()
        self.encounterCategories = curr_map.points.get(curr_point) # PointCategoriesObj

    def add_to_encounter(self, dict_to_add):
        # self.encounterCategories[curr_cat].push(LL_to_add.head) # Add the head of the LL to add to the existing encounter LL
        self.encounterCategories.add_to_pointCategories(dict_to_add)
    
    # TODO: Create a shared function between Map and Encounter to remove an id from the LL
    def remove_from_encounter(self, obj_to_remove):
        curr_point = obj_to_remove.curr_pos.point
        curr_cat = obj_to_remove.pointCategory.name
        curr_id = obj_to_remove.id
        self.points[curr_point].pointCategories.remove_id_from_pointCategories(curr_cat, curr_id)
        point_isEmpty = self.points[curr_point].pointCategories[curr_cat].check_pointCategories_isEmpty()
        return point_isEmpty

    def check_for_encounter(self, curr_map, person):
        curr_point = person.curr_pos.point
        person.encounter.encounterCategories = curr_map.points.get(curr_point) # Points the person.encounter.encounterCategories to curr_map.points.get(curr_point) LinkedList. This allows the encounter to always stay updated on the mapPoint.
        # check_npc = curr_map.points.get(curr_point)
        if curr_point in curr_map.points: # Check if pc current point is a key in the Map points dictionary
            # person.encounter.add_to_encounter(curr_map.points[curr_point].pointCategories)
            return True
        else:
            return False

class Person:
    class stats:
        def __init__(self, curr_pos, hp, mp, strength, defense, agility):
                self.hp = hp
                self.mp = mp
                self.strength = strength
                self.defense = defense
                self.agility = agility
    
    def __init__(self, name, curr_pos, curr_map, pointCategory, ids, hp=100, mp=100, strength=10, defense=10, agility=10, encounter=None):
        self.name = name
        self.curr_pos = Point(curr_pos) # Point(n,n)
        curr_point = self.curr_pos.point
        self.stats = self.stats(curr_pos, hp, mp, strength, defense, agility)
        self.pointCategory = pointCategory
        self.encounter = Encounter(curr_map=curr_map, curr_point=curr_point)
        
        # CHANGE THIS: Make separate classes for pc, npc, item, path, obstacle, etc.
        # Can share common traits but class should be separate
        if pointCategory == PointCategories.pc:
            self.id = ids.pc_Ids.add_id(self)
        elif pointCategory == PointCategories.npc:
            self.id = ids.npc_Ids.add_id(self)
        print(self.pointCategory)
        curr_map.add_to_points(self)
        
    def move_spaces(self, movement, curr_map):
        curr_map.remove_from_points(self)
        movement = Point(movement)
        self.curr_pos.move_point(movement)
        if self.pointCategory == PointCategories.pc: # Check for encounter if person is a pc
            # curr_encounter = Encounter()
            self.encounter = Encounter(curr_map=curr_map, curr_point=self.curr_pos.point)
            if self.encounter.check_for_encounter(curr_map, self):
                curr_map.add_to_points(self)
                return True
            else:
                return False

def create_default_person(name, starting_pos, char_type, curr_map, pointCategory, ids):
    def_stats = default_stats[char_type]
    person = Person(name, starting_pos, curr_map, pointCategory, ids, def_stats['hp'], def_stats['mp'], 
                    def_stats['strength'], def_stats['defense'], def_stats['agility'])
    return person