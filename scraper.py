from multiprocessing import Pool
import requests
from time import sleep
import json


class User:
    def __init__(self, id, name=None, friends=None) -> None:
        self.id = id 
        self.name = name
        self.friends = friends


class User_graph:

    def __init__(self) -> None:
        self.users = {}


    def add_user(self, id, name=None, friends=None):
        if id in self.users:
            return None

        self.users[id] = User(id, name, friends)


    def save(self):
        pass

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
                    sleep(1)

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
        #print(ids)

        for id in ids:
            if self.users[id].friends:
                continue

            reqwests.append((id, f"https://api.vk.com/method/friends.get?user_id={id}&access_token={url_params['access_token']}&v={url_params['v']}"))
        
        with Pool(100) as p:
            data = p.map(User_graph.reqwest, reqwests)

        for entry in data:
            if entry == None:
                continue
            
            id, response = entry
            friends = response['response']['items']

            for friend in friends:
                self.add_user(friend)

            self.users[id].friends = friends



    """
    def get_friends(self, params):
        for _ in range(3):
            try:
                response = requests.get(f"https://api.vk.com/method/friends.get?user_id={self.id}&access_token={params['access_token']}&v={params['v']}")

                self.friends = json.loads(response.text)['response']['items'] #seems like a bad solution, but oh well

                for id in self.friends:
                    User(id)

                break

            except KeyError:
                break

        else:
            raise Exception('failed to fetch correct response')
            
        #print('done', self.id)


    def get_name(self, params):
        if self.name:
            return None

        for _ in range(3):
            try:
                response = requests.get(f"https://api.vk.com/method/users.get?user_id={self.id}&access_token={params['access_token']}&v={params['v']}")
                response = json.loads(response.text)['response'][0]

                self.name = response['first_name']
                self.name += ' ' + response['last_name']

                break

            except KeyError:
                break

        else:
            raise Exception('failed to fetch correct response')
    """


    def clean(self):
        for id, user in tuple(self.users.items()):
            if not user.friends:
                del self.users[id]


def test():
    params = {
    'access_token': 'vk1.a.ePRZ5JV63lzIh386JBs_y0BDTn1fzC8VwG8ZaxP0kva2ig_PAUUtxCMW6kZz9lJ4JwXfaDkLPqyydB9ZSWzVkpou7dQBlV-rFLavJNsqEB0zfVAoJbJC8TbH13fHzeAWomc0bePVE4LuAOPs7Q__YvoWNIKZUeuYHQ9w7Or_ICrFbF6ktrHbNsmoKW0rOR80',
    'v': 5.131
    }

    graph = User_graph()

    graph.add_user(647027693)
    graph.add_user(560230860)

    for _ in range(2):
        graph.get_friends(params, *graph.users.keys())

    graph.clean()

    edges = set()
    vertices = set()
    name_dict = {}

    for user in list(graph.users.values()):
        vertices.add(user.id)

        #user.get_name(params)
        #name_dict[user.id] = user.name

        for friend in user.friends:
            if friend in graph.users.keys():
                edges.add(tuple(sorted((user.id, friend))))


    print('{}, {}, {}'.format(list(vertices), list(edges), name_dict))


if __name__ == '__main__': test()