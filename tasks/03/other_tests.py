import datetime
import unittest
from time import sleep
import solution


class TestSocialGraph(unittest.TestCase):
    def setUp(self):
        self.terry = solution.User("Terry Gilliam")
        self.eric = solution.User("Eric Idle")
        self.graham = solution.User("Graham Chapman")
        self.john = solution.User("John Cleese")
        self.michael = solution.User("Michael Palin")
        self.graph = solution.SocialGraph()
        self.graph.add_user(self.terry)
        self.graph.add_user(self.eric)
        self.graph.add_user(self.graham)
        self.graph.add_user(self.john)
        self.graph.add_user(self.michael)

    def test_add_get_and_delete_user(self):
        with self.assertRaises(solution.UserAlreadyExistsError):
            self.graph.add_user(self.terry)
        self.graph.delete_user(self.terry.uuid)
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.get_user(self.terry.uuid)
        with self.assertRaises(solution.UserDoesNotExistError):
            self.graph.delete_user(self.terry.uuid)
        self.graph.add_user(self.terry)
        self.assertEqual(self.graph.get_user(self.terry.uuid), self.terry)

    def test_following(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.assertTrue(
            self.graph.is_following(self.terry.uuid, self.eric.uuid))
        self.assertFalse(
            self.graph.is_following(self.eric.uuid, self.terry.uuid))
        self.assertTrue(
            self.graph.following(self.terry.uuid) == {self.eric.uuid})
        self.assertTrue(
            self.graph.followers(self.eric.uuid) == {self.terry.uuid})

    def test_friends(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.assertNotIn(self.eric.uuid, self.graph.friends(self.terry.uuid))
        self.assertNotIn(self.terry.uuid, self.graph.friends(self.eric.uuid))
        self.graph.follow(self.eric.uuid, self.terry.uuid)
        self.assertIn(self.eric.uuid, self.graph.friends(self.terry.uuid))
        self.assertIn(self.terry.uuid, self.graph.friends(self.eric.uuid))

    def test_distnaces(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.graham.uuid)
        self.graph.follow(self.eric.uuid, self.michael.uuid)
        self.graph.follow(self.eric.uuid, self.john.uuid)
        self.graph.follow(self.john.uuid, self.graham.uuid)
        self.assertEqual(self.graph.max_distance(self.terry.uuid), 2)
        self.assertEqual(self.graph.max_distance(self.eric.uuid), 2)
        self.assertEqual(
            self.graph.min_distance(self.terry.uuid, self.graham.uuid), 1)
        self.assertEqual(
            self.graph.min_distance(self.eric.uuid, self.graham.uuid), 2)

    def test_layer_followings(self):
        self.graph.follow(self.eric.uuid, self.terry.uuid)
        self.graph.follow(self.terry.uuid, self.john.uuid)
        self.assertEqual(
            list(self.graph.nth_layer_followings(self.eric.uuid, 2)),
            [self.john.uuid])

    def test_feed(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.graph.follow(self.terry.uuid, self.graham.uuid)
        self.graph.follow(self.terry.uuid, self.john.uuid)
        self.graph.follow(self.terry.uuid, self.michael.uuid)
        for i in range(10):
            self.eric.add_post(str(i))
            sleep(0.000001)
            self.graham.add_post(str(10 + i))
            sleep(0.000001)
            self.john.add_post(str(20 + i))
            sleep(0.000001)
            self.michael.add_post(str(30 + i))
            sleep(0.000001)
        self.assertEqual(
            [post.content
             for post in self.graph.generate_feed(self.terry.uuid, 0, 10)],
            ["39", "29", "19", "9", "38", "28", "18", "8", "37", "27"])
        self.assertEqual(
            [post.content
             for post in self.graph.generate_feed(self.terry.uuid, 10, 10)],
            ["17", "7", "36", "26", "16", "6", "35", "25", "15", "5"])
        self.assertEqual(
            [post.content
             for post in self.graph.generate_feed(self.terry.uuid, 20, 10)],
            ["34", "24", "14", "4", "33", "23", "13", "3", "32", "22"])
        self.assertEqual(
            [post.content
             for post in self.graph.generate_feed(self.terry.uuid, 30, 10)],
            ["12", "2", "31", "21", "11", "1", "30", "20", "10", "0"])
        self.assertEqual([post.content for post in self.eric.get_post()],
                         [str(i) for i in range(10)])
        self.assertEqual([post.content for post in self.graham.get_post()],
                         [str(i) for i in range(10, 20)])
        self.assertEqual([post.content for post in self.john.get_post()],
                         [str(i) for i in range(20, 30)])
        self.assertEqual([post.content for post in self.michael.get_post()],
                         [str(i) for i in range(30, 40)])


class TestUser(unittest.TestCase):
    def setUp(self):
        self.michael = solution.User("Michael Palin")
        self.terry = solution.User("Terry Gilliam")

    def test_has_uuid(self):
        self.assertIsNotNone(getattr(self.michael, 'uuid'))

    def test_add_post(self):
        self.michael.add_post("larodi")
        post = next(self.michael.get_post())
        self.assertEqual(post.author, self.michael.uuid)
        self.assertEqual(post.content, "larodi")
        self.assertTrue(isinstance(post.published_at, datetime.datetime))
        for i in range(102):
            self.terry.add_post("spam")
        count = 0
        for post in self.terry.get_post():
            self.assertEqual(post.content, "spam")
            count += 1
        self.assertEqual(count, 50)

if __name__ == '__main__':
    unittest.main()
