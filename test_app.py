from unittest import TestCase

from app import app, games
from boggle import BoggleGame

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!--Home page comment for testing', html)

            ...
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:

            response = client.post('/api/new-game')
            data = response.get_json()
            # TODO: remove this.
            # print(f"\n\n data from POST is: {data} \n\n")
            print(f"\n\n games object is: {games}")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(type(data["gameId"]), str)
            self.assertEqual(type(data["board"]), list)
            self.assertIn(data["gameId"], games)

            # DONE: make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)

    def test_score_word(self):
        """Test if word:
            is a valid word
            is on board
            """

        with self.client as client:

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            response = client.post('/api/new-game')
            new_game_data = response.get_json()
            #data should be:
            #{"gameId": game_id, "board": game.board}

            #now that we have JSON, we need to send a POST request to /api/score-word

            # find that game in the dictionary of games (imported from app.py above)
            game_id = new_game_data["gameId"]
            game = games[game_id]
            # manually change the game board's rows so they are not random
            game.board[0] = ["C", "A", "T", "E", "E"]
            test_success = {"gameId": game_id, "word": "CAT"}

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # /api/score-word
            response = client.post('/api/score-word', json=test_success)
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["result"], "ok")


            # test to see that a valid word not on the altered board returns
            # {'result': 'not-on-board'}
            test_not_on_board = {"gameId": game_id, "word": "DINNERS"}

            response = client.post('/api/score-word', json=test_not_on_board)
            data = response.get_json()
            #better pattern: data, {"result", "not-on-board"}
            self.assertEqual(data["result"], "not-on-board")

            # test to see that an invalid word returns {'result': 'not-word'}
            test_not_word = {"gameId": game_id, "word": "asldkjasld"}

            response = client.post('/api/score-word', json=test_not_word)
            data = response.get_json()
            self.assertEqual(data["result"], "not-word")

