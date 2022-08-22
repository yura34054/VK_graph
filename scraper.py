from multiprocessing import Pool
from random import random
import requests
from time import sleep
import json


def split_list(lst: list, n: int):
    
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


class User:
    def __init__(self, id, name=None, friends=[]) -> None:
        self.id = id 
        self.name = name
        self.friends = friends


class User_graph:

    def __init__(self) -> None:
        self.users = {}


    def add_user(self, id, name=None, friends=[]):
        if id in self.users:
            return None

        self.users[id] = User(id, name, friends)


    @staticmethod
    def reqwest(args):
        id, url = args
        tries = 0

        while tries <= 3:
            try:
                response = requests.get(url)
                response = json.loads(response.text)

            except Exception as e:
                print(e)
                tries += 1
                continue


            if 'error' in response:
                error_code = response['error']['error_code']

                if error_code == 5: #user authentication failed
                    raise Exception('wrong access_token')

                elif error_code == 6: #too many requests per second
                    sleep(random()*2)

                elif error_code == 15: #access denied
                        return None

                elif error_code == 18: #page delited
                    return None

                elif error_code == 30: #profile is privet
                    return None

                else:
                    print(f'unknown error code - {error_code}')
                    print(url)

            else:
                return id, response
                
            
        raise Exception('failed to fetch correct response')


    def get_friends(self, url_params, *ids):
        reqwests = []

        for id in ids:
            if len(self.users[id].friends) != 0:
                continue

            reqwests.append((id, f"https://api.vk.com/method/friends.get?user_id={id}&access_token={url_params['access_token']}&v={url_params['v']}"))
        
        with Pool(50) as p:
            data = p.map(self.__class__.reqwest, reqwests)

        for entry in data:
            if entry == None:
                continue
            
            id, response = entry
            friends = response['response']['items']

            for friend in friends:
                self.add_user(friend)

            self.users[id].friends = friends


    def get_names(self, url_params, *ids):
        reqwests = []
        
        for chunk in list(split_list(ids, 5)):
            reqwests.append((0, f"https://api.vk.com/method/users.get?user_id={','.join(map(str, chunk))}&access_token={url_params['access_token']}&v={url_params['v']}"))


        with Pool(50) as p:
            data = p.map(self.__class__.reqwest, reqwests)

        for chunk in data:
            chunk = chunk[1]

            response = chunk['response']

            for entry in response:
                id = entry['id']
                self.users[id].name = f"{entry['first_name']} {entry['last_name']}"


    def clean(self):
        for id, user in tuple(self.users.items()):
            if not user.friends:
                del self.users[id]


    def save(self):
        edges = set()
        vertices = set()
        name_dict = {}


        for user in list(self.users.values()):
            vertices.add(user.id)

            name_dict[user.id] = user.name

            for friend in user.friends:
                if friend in self.users.keys():
                    edges.add(tuple(sorted((user.id, friend))))


        edges, vertices = map(list, (edges, vertices))
        data = {'edges': edges, 'vertices': vertices, 'name_dict': name_dict}

        with open("data.json", "w") as file:
            file.write(json.dumps(data, indent=4))


    def load(self):
        with open("data.json", "r") as file:
            data = json.load(file)

            edges = data['edges']
            vertices = data['vertices']
            name_dict = data['name_dict']


        for id in vertices:
            self.add_user(id, name_dict[str(id)], [])

        for relation in edges:
            self.users[relation[0]].friends.append(relation[1])
            self.users[relation[1]].friends.append(relation[0])



def test():
    params = {
    'access_token': '!access_token',
    'v': 5.131
    }

    graph = User_graph()

    graph.add_user(647027693)
    graph.add_user(560230860)

    for _ in range(2):
        graph.get_friends(params, *graph.users.keys())

    graph.clean()
    graph.get_names(params, *graph.users.keys())
    graph.save()


if __name__ == '__main__': test()
