from uuid import uuid4
from collections import defaultdict
import datetime
from math import inf


class UsersNotConnectedError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserDoesNotExistError(Exception):
    pass


class PostList:
    def __init__(self, limit):
        self.limit = limit
        self.posts = []

    def append(self, post):
        if len(self.posts) == self.limit:
            self.posts.pop(0)
        self.posts.append(post)

    def __iter__(self):
        return iter(self.posts)


class Post:
    def __init__(self, content, author):
        self.content = content
        self.author = author
        self.published_at = datetime.datetime.now()

    def __repr__(self):
        return self.content


class User:
    LIMIT = 50

    def __init__(self, full_name):
        self.full_name = full_name
        self.uuid = uuid4()
        self.posts = PostList(type(self).LIMIT)

    def add_post(self, post_content):
        self.posts.append(Post(post_content, self.uuid))

    def get_post(self):
        return iter(self.posts)

    def __repr__(self):
        return self.full_name


class SocialGraph:
    def __init__(self):
        self.users = {}
        self.__following = defaultdict(set)
        self.__followers = defaultdict(set)

    def __initialize_user(self, user):
        self.users[user.uuid] = user
        self.__followers[user.uuid] = set()
        self.__following[user.uuid] = set()

    def __check(self, *args):
        for user_uuid in args:
            if user_uuid not in self.users.keys():
                raise UserDoesNotExistError

    def add_user(self, user):
        if user.uuid in self.users.keys():
            raise UserAlreadyExistsError
        self.__initialize_user(user)

    def get_user(self, user_uuid):
        self.__check(user_uuid)
        return self.users[user_uuid]

    def delete_user(self, user_uuid):
        self.__check(user_uuid)
        del self.users[user_uuid]

        for user in self.__following[user_uuid]:
            self.__followers[user].remove(user_uuid)
        for user in self.__followers[user_uuid]:
            self.__following[user].remove(user_uuid)

        del self.__following[user_uuid]
        del self.__followers[user_uuid]

    def follow(self, follower, followee):
        self.__check(follower, followee)

        self.__following[follower].add(followee)
        self.__followers[followee].add(follower)

    def unfollow(self, follower, followee):
        self.__check(follower, followee)
        try:
            self.__following[follower].remove(followee)
            self.__followers[followee].remove(follower)
        except KeyError:
            pass

    def is_following(self, follower, followee):
        self.__check(follower, followee)
        return followee in self.__following[follower]

    def followers(self, user_uuid):
        self.__check(user_uuid)
        return self.__followers[user_uuid]

    def following(self, user_uuid):
        self.__check(user_uuid)
        return self.__following[user_uuid]

    def friends(self, user_uuid):
        self.__check(user_uuid)
        return self.__following[user_uuid] & self.__followers[user_uuid]

    def max_distance(self, user_uuid):
        self.__check(user_uuid)
        farthest = 0
        visited = []
        to_be_visited = [(user_uuid, 0)]
        while to_be_visited:
            current, level = to_be_visited.pop(0)
            farthest = max(level, farthest)
            visited.append(current)
            for next_user in self.__following[current]:
                if next_user not in visited:
                    to_be_visited.append((next_user, level + 1))
        if farthest == 0:
            return inf
        return farthest

    def min_distance(self, from_user_uuid, to_user_uuid):
        self.__check(to_user_uuid, to_user_uuid)

        min_dist = self.__djiikstra(from_user_uuid)[to_user_uuid]
        if min_dist == inf:
            raise UsersNotConnectedError
        return min_dist

    def __djiikstra(self, from_user_uuid):
        distances = {user: inf for user in self.users.keys()}
        to_be_visited = list(self.users.keys())
        distances[from_user_uuid] = 0
        while to_be_visited:
            closest = min(to_be_visited, key=distances.get)
            to_be_visited.remove(closest)
            for user in self.__following[closest]:
                if distances[closest] + 1 < distances[user]:
                    distances[user] = distances[closest] + 1
        return distances

    def nth_layer_followings(self, user_uuid, n):
        self.__check(user_uuid)
        visited = [user_uuid]
        level = 0
        to_be_visited = [(user_uuid, level)]
        nthlevel = []

        while to_be_visited:
            current, level = to_be_visited.pop(0)
            if level == n and current not in visited:
                nthlevel.append(current)
            else:
                visited.append(current)
                for next_user in self.__following[current]:
                    if next_user not in visited:
                        to_be_visited.append((next_user, level + 1))
        return nthlevel

    def generate_feed(self, user_uuid, offset=0, limit=10):
        self.__check(user_uuid)
        all_posts = list(map(lambda x: self.users[x].posts.posts,
                             self.__following[user_uuid]))
        all_posts = [post for posts in all_posts for post in posts]
        all_posts.sort(key=lambda post: post.published_at, reverse=True)
        return all_posts[offset:offset + limit]


graph = SocialGraph()
maria = User('maria')
ivan = User('ivan')
pesho = User('pesho')
gosho = User('gosho')
desi = User('desi')
beli = User('beli')
a = User('a')
graph.add_user(maria)
graph.add_user(ivan)
graph.add_user(gosho)
graph.add_user(pesho)
graph.add_user(desi)
graph.add_user(beli)
graph.add_user(a)



'''graph.follow(maria.uuid, ivan.uuid)
graph.follow(ivan.uuid, pesho.uuid)
graph.follow(pesho.uuid, desi.uuid)
graph.follow(desi.uuid, pesho.uuid)
graph.follow(desi.uuid, beli.uuid)
graph.follow(pesho.uuid, gosho.uuid)
graph.follow(pesho.uuid, maria.uuid)'''

'''print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(maria.uuid, 1))))
print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(maria.uuid, 2))))
print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(maria.uuid, 3))))
print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(maria.uuid, 4))))

print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(maria.uuid, 5))))
print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(maria.uuid, 0))))

'''
b = User('b')
c = User('c')
d = User('d')
e = User('e')
f = User('f')
g = User('g')

graph.add_user(b)
graph.add_user(c)
graph.add_user(d)
graph.add_user(e)
graph.add_user(f)
graph.add_user(g)

graph.follow(a.uuid, b.uuid)
graph.follow(a.uuid, e.uuid)
graph.follow(b.uuid, c.uuid)
graph.follow(c.uuid, a.uuid)
graph.follow(c.uuid, d.uuid)
graph.follow(e.uuid, f.uuid)
graph.follow(f.uuid, e.uuid)

print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(a.uuid, 1))))
print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(a.uuid, 2))))
print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(a.uuid, 3))))
print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(a.uuid, 4))))

print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(a.uuid, 5))))
print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(a.uuid, 0))))


print(graph.max_distance(a.uuid))
print(graph.min_distance(a.uuid, b.uuid))
print(graph.min_distance(a.uuid, c.uuid))

graph.follow(maria.uuid, ivan.uuid)
graph.follow(maria.uuid, pesho.uuid)
graph.follow(ivan.uuid, pesho.uuid)

print(list(map(lambda x: graph.users.get(x), graph.nth_layer_followings(maria.uuid, 2))))
print(graph.max_distance(g.uuid))
