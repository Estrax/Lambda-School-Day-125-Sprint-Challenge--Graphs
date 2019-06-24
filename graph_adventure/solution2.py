from collections import deque, defaultdict, OrderedDict
import random
from player import Player


def solve(starting_room, room_graph, upperbound=None):
    def bfs(rooms, room):
        visited = set()
        queue = deque()
        queue.append([{room.id: None}])
        while len(queue) > 0:
            path = queue.popleft()
            vertex = list(path[-1])[0]
            if vertex not in visited:
                for news in rooms[vertex]:
                    new_path = list(path)
                    new_path.append({rooms[vertex][news]: news})
                    queue.append(new_path)
                    if rooms[vertex][news] == '?':
                        return [list(step.values())[0] for step in new_path[1:]]
                visited.add(vertex)
        return None

    tmp_traversal = []
    shortest = []
    shortest_len = upperbound if upperbound else 1000
    while True:
        player = Player("Name", starting_room)
        tmp_path = []
        rooms = dict()
        rooms[player.currentRoom.id] = OrderedDict()
        exit_dirs = player.currentRoom.getExits()
        random.shuffle(exit_dirs)
        for exit_dir in exit_dirs:
            rooms[player.currentRoom.id][exit_dir] = '?'

        while True:
            short_path = bfs(rooms, player.currentRoom)
            if not short_path:
                break
            for step in short_path:
                previous_room = player.currentRoom
                player.travel(step)
                if player.currentRoom.id not in rooms:
                    rooms[player.currentRoom.id] = dict()
                end_dirs = player.currentRoom.getExits()
                random.shuffle(end_dirs)
                for end_dir in end_dirs:
                    if end_dir not in rooms[player.currentRoom.id]:
                        rooms[player.currentRoom.id][end_dir] = '?'
                for end_dir in previous_room.getExits():
                    if end_dir == step:
                        rooms[previous_room.id][end_dir] = player.currentRoom.id
                        rooms[player.currentRoom.id][{
                            'n': 's',
                            's': 'n',
                            'e': 'w',
                            'w': 'e'
                        }[step]] = previous_room.id

            tmp_path = tmp_path + short_path
        tmp_traversal = tmp_path

        if len(tmp_traversal) < shortest_len:
            shortest = tmp_traversal
            shortest_len = len(shortest)
            break

    return shortest
