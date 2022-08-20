import requests
import json

class User:
    objs = {}

    def __new__(cls, id):
        if id in cls.objs:
            return None

        user = super().__new__(cls)
        cls.objs[id] = user

        return user


    def __init__(self, id) -> None:
        self.id = id
        self.friends = 0


    def get_friends(self, params):
        response = requests.get(f"https://api.vk.com/method/friends.get?user_id={self.id}&access_token={params['access_token']}&v={params['v']}")

        self.friends = json.loads(response.text)['response']['items'] #seems like a bad solution, but oh well

        for id in self.friends:
            User(id)
            
        #print('done', id)

    @classmethod
    def clean(cls):
        for id, user in tuple(cls.objs.items()):
            if user.friends == 0:
                del cls.objs[id]



class User_graph:
    pass


def test():
    params = {
    'access_token': 'vk1.a.3IPHvyJtO3yKCZl-yhg9Evwq8yae69-Y3g3f-f5WPzFxd6DMuEOKT4Okn677KNouhLfOPPenubDt7YQKGAKtY87ohtaeJKoN2buR0QifgJaFvi2x_kkCsCh9YJQ9IYMfszQgCXDegZBewEpWzR9OKTFgzUSavWnZp_4uWiF3SamVtpu9i8wmpe92GlWB9o0i',
    'v': 5.131
    }

    User(647027693)

    for _ in range(2):
        for user in list(User.objs.values()):
            user.get_friends(params)

    User.clean()

    edges = set()
    vertices = set()

    for user in list(User.objs.values()):
        vertices.add(user.id)

        for friend in user.friends:
            edges.add(tuple(sorted((user.id, friend))))


    print(vertices)
    print(edges)



if __name__ == '__main__': test()