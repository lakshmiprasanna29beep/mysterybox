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
        self.assertIn(b"Unsolved Crime Chronicles", response.data)
        self.assertIn(b"The Blackwood Sapphire Heist", response.data)
        self.assertIn(b"The Cyanide Sonata", response.data)
        self.assertIn(b"The Silicon Vault Sabotage", response.data)

    def test_case_view(self):
        response = self.client.get('/case/case_sapphire')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The Blackwood Sapphire Heist", response.data)
        self.assertIn(b"James Thornton", response.data)
        self.assertIn(b"Madame Yvonne Delacroix", response.data)

    def test_api_case_data(self):
        response = self.client.get('/api/case/case_sapphire')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['case']['id'], 'case_sapphire')
        self.assertEqual(len(data['suspects']), 4)
        self.assertGreaterEqual(len(data['clues']), 6)
        self.assertIn('suspect_yvonne', data['dialogues'])

    def test_interrogation_api(self):
        # Fetch dialogue id for Yvonne
        res = self.client.get('/api/case/case_sapphire')
        data = json.loads(res.data)
        yvonne_dialogue = data['dialogues']['suspect_yvonne'][0]

        post_res = self.client.post('/api/interrogate', json={
            'dialogue_id': yvonne_dialogue['id']
        })
        self.assertEqual(post_res.status_code, 200)
        post_data = json.loads(post_res.data)
        self.assertTrue(post_data['success'])
        self.assertIn("Rembrandt", post_data['answer'])

    def test_evidence_contradiction(self):
        # Present train ticket to Yvonne
        res = self.client.post('/api/present-evidence', json={
            'suspect_id': 'suspect_yvonne',
            'clue_id': 'clue_train_ticket'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['is_contradiction'])
        self.assertTrue(data['breaks_alibi'])
        self.assertIn("Eurostar", data['callout_text'])

    def test_accuse_flawless(self):
        # Yvonne with wax impression and train ticket
        res = self.client.post('/api/accuse', json={
            'case_id': 'case_sapphire',
            'suspect_id': 'suspect_yvonne',
            'weapon_clue_id': 'clue_wax_impression',
            'proof_clue_id': 'clue_train_ticket',
            'motive_statement': 'Fence the gem in Geneva for 4 million euros.'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['is_flawless'])
        self.assertEqual(data['score'], 1000)
        self.assertEqual(data['verdict_type'], 'flawless')
        self.assertIn("MASTER SLEUTH", data['title'])

    def test_accuse_wrong_suspect(self):
        res = self.client.post('/api/accuse', json={
            'case_id': 'case_sapphire',
            'suspect_id': 'suspect_james',
            'weapon_clue_id': 'clue_wax_impression',
            'proof_clue_id': 'clue_train_ticket',
            'motive_statement': 'Gambling debts.'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertFalse(data['is_flawless'])
        self.assertEqual(data['verdict_type'], 'wrong_suspect')
        self.assertIn("MISCARRIAGE OF JUSTICE", data['title'])

    def test_notes_api(self):
        res = self.client.post('/api/notes', json={
            'case_id': 'case_sapphire',
            'note_text': 'Yvonne has lavender lotion matching the wax wrapper.'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()
