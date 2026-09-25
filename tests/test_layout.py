import sys, unittest, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import generate as g
class LayoutTests(unittest.TestCase):
    def test_inventory(self):
        g.validate()
        self.assertEqual(len(g.RULES),233)
        self.assertEqual(sum(r['group']=='symbols' for r in g.RULES),55)
    def test_every_rule_round_trips(self):
        for rule in g.RULES:
            with self.subTest(rule=rule['id']): self.assertEqual(g.decode(rule['keys']),rule['output'])
    def test_prefix_boundaries(self):
        for keys,text in [('wer','わから'),('ehk','かい'),('qwe','ぁわか'),('qn','ぁん'),('qp','ゎ'),('wjh','ゔぁ'),('wjj','ゔ'),('en','かん'),('em','かっ'),('ey','かー'),('ci','どぅ'),('xo','てゅ')]:
            self.assertEqual(g.decode(list(keys)),text)
    def test_nasal_and_geminate_keep_the_v1_keys(self):
        # 2.0.0-beta.2 put ん back on N and っ on M under the v1 rule IDs.
        self.assertEqual(g.BY_KEYS[('n',)]['id'],'n-n');self.assertEqual(g.BY_KEYS[('n',)]['output'],'ん')
        self.assertEqual(g.BY_KEYS[('m',)]['id'],'m-small-tsu');self.assertEqual(g.BY_KEYS[('m',)]['output'],'っ')
        self.assertEqual(g.BY_KEYS[('p','n')]['output'],'′');self.assertEqual(g.BY_KEYS[('p','m')]['output'],'″')
    def test_all_lessons_use_current_rules(self):
        data=g.practice_data()
        self.assertEqual(len(data['lessons']),12)
        for lesson in data['lessons']:
            for x in lesson['exercises']: self.assertEqual(g.decode(x['keys']),x['text'])
    def test_no_shortcuts_in_beginner_lessons(self):
        for lesson in g.practice_data()['lessons']:
            if lesson['id']!='special':
                for x in lesson['exercises']:
                    self.assertNotIn('p',x['keys']) if 'ゎ' not in x['text'] else None
    def test_generated_adapters_have_unique_inputs_and_no_controls(self):
        for table in g.tables():
            lines=table.splitlines();self.assertEqual(len(lines),len({x.split('\t')[0] for x in lines}))
            self.assertFalse(any(ord(c)<32 and c not in '\t\n' for c in table))
    def test_unsupported_target_rejected(self):
        with self.assertRaises(ValueError):g.encode('未対応')
if __name__=='__main__':unittest.main()
