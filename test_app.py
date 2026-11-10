import unittest
import json
from app import app
from database import init_db
from seed_data import seed

class MysteryBoxTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Case 1: The Stolen Blue Diamond", response.data)
        self.assertIn(b"Case 2: The Poisoned Tea", response.data)
        self.assertIn(b"Case 3: The Stolen Computer Chip", response.data)

    def test_case_view(self):
        response = self.client.get('/case/case_sapphire')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Case 1: The Stolen Blue Diamond", response.data)
        self.assertIn(b"James (The Butler)", response.data)
        self.assertIn(b"Madame Yvonne", response.data)

    def test_api_case_data(self):
        response = self.client.get('/api/case/case_sapphire')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['case']['id'], 'case_sapphire')
        self.assertEqual(len(data['suspects']), 4)
        self.assertGreaterEqual(len(data['clues']), 6)
        self.assertIn('suspect_yvonne', data['dialogues'])

    def test_interrogation_api(self):
        res = self.client.get('/api/case/case_sapphire')
        data = json.loads(res.data)
        yvonne_dialogue = data['dialogues']['suspect_yvonne'][0]

        post_res = self.client.post('/api/interrogate', json={
            'dialogue_id': yvonne_dialogue['id']
        })
        self.assertEqual(post_res.status_code, 200)
        post_data = json.loads(post_res.data)
        self.assertTrue(post_data['success'])
        self.assertIn("paintings", post_data['answer'])

    def test_evidence_contradiction(self):
        res = self.client.post('/api/present-evidence', json={
            'suspect_id': 'suspect_yvonne',
            'clue_id': 'clue_train_ticket'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['is_contradiction'])
        self.assertTrue(data['breaks_alibi'])
        self.assertIn("train ticket", data['callout_text'])

    def test_accuse_flawless(self):
        res = self.client.post('/api/accuse', json={
            'case_id': 'case_sapphire',
            'suspect_id': 'suspect_yvonne',
            'weapon_clue_id': 'clue_wax_impression',
            'proof_clue_id': 'clue_train_ticket',
            'motive_statement': 'Sell it in Paris for 4 million dollars.'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['is_flawless'])
        self.assertEqual(data['score'], 1000)
        self.assertEqual(data['verdict_type'], 'flawless')

    def test_accuse_wrong_suspect(self):
        res = self.client.post('/api/accuse', json={
            'case_id': 'case_sapphire',
            'suspect_id': 'suspect_james',
            'weapon_clue_id': 'clue_wax_impression',
            'proof_clue_id': 'clue_train_ticket',
            'motive_statement': 'Debts.'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertFalse(data['is_flawless'])
        self.assertEqual(data['verdict_type'], 'wrong_suspect')

    def test_notes_api(self):
        res = self.client.post('/api/notes', json={
            'case_id': 'case_sapphire',
            'note_text': 'Yvonne has lavender cream matching the wax.'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()
