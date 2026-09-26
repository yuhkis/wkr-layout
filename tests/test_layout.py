import sys, unittest, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import generate as g
class LayoutTests(unittest.TestCase):
    def test_inventory(self):
        g.validate()
        self.assertEqual(len(g.RULES),220)
        self.assertEqual(sum(r['group']=='symbols' for r in g.RULES),55)
        self.assertEqual(sum(r['group']=='arrows' for r in g.RULES),4)
    def test_every_rule_round_trips(self):
        for rule in g.RULES:
            with self.subTest(rule=rule['id']): self.assertEqual(g.decode(rule['keys']),rule['output'])
    def test_prefix_boundaries(self):
        for keys,text in [('wer','わから'),('ehk','かい'),('qhwe','ぁわか'),('qwe','ゎか'),('qn','ぁん'),('qu','ぁん'),('qp','ゃ'),('qw','ゎ'),
                          ('wjh','ゔぁ'),('wjj','ゔ'),('wjp','ゔゃ'),('wju','ゔん'),('en','かん'),('eu','かん'),('em','かっ'),('ey','かー'),
                          ('ep','きゃ'),('ehp','かや'),('ci','どぅ'),('cp','でぃ'),('xo','てゅ'),('xp','てぃ'),('qql','→'),('eqql','か→'),('qqp','～')]:
            self.assertEqual(g.decode(list(keys)),text)
    def test_nasal_and_geminate_keep_the_v1_keys(self):
        # 2.0.0-beta.2 put ん back on N and っ on M under the v1 rule IDs;
        # 2.0.0-beta.3 gives ん a second key, U.
        self.assertEqual(g.BY_KEYS[('n',)]['id'],'n-n');self.assertEqual(g.BY_KEYS[('n',)]['output'],'ん')
        self.assertEqual(g.BY_KEYS[('u',)]['id'],'u-n');self.assertEqual(g.BY_KEYS[('u',)]['output'],'ん')
        self.assertEqual(g.BY_KEYS[('m',)]['id'],'m-small-tsu');self.assertEqual(g.BY_KEYS[('m',)]['output'],'っ')
        self.assertEqual(g.BY_KEYS[('q','q','n')]['output'],'′');self.assertEqual(g.BY_KEYS[('q','q','m')]['output'],'″')
    def test_ya_column_is_on_p_and_symbols_follow_q_q(self):
        # 2.0.0-beta.3: や alone and the ゃ column after a row key are on P,
        # and the symbol layer keeps its selectors behind Q Q.
        self.assertEqual(g.BY_KEYS[('p',)]['output'],'や')
        rows=[k for (k,) in [r for r in g.BY_KEYS if len(r)==1] if (k,'p') in g.BY_KEYS]
        self.assertEqual(len(rows),15)
        for row in rows:
            self.assertNotIn((row,'u'),g.BY_KEYS);self.assertNotIn((row,'y'),g.BY_KEYS)
        self.assertFalse(any(r['keys'][0]=='p' and len(r['keys'])>1 for r in g.RULES))
        self.assertTrue(all(r['keys'][:2]==['q','q'] for r in g.RULES if r['group'] in ('symbols','arrows')))
    def test_all_lessons_use_current_rules(self):
        data=g.practice_data()
        self.assertEqual(len(data['lessons']),11)
        for lesson in data['lessons']:
            for x in lesson['exercises']: self.assertEqual(g.decode(x['keys']),x['text'])
    def test_no_rule_gives_two_kana(self):
        # 2.0.0-beta.3 removed the special column, the only rules that did.
        self.assertFalse(any(r['group']=='shortcuts' for r in g.RULES))
    def test_lessons_show_u_for_n(self):
        keys=[x['keys'] for l in g.practice_data()['lessons'] for x in l['exercises'] if 'ん' in x['text']]
        self.assertTrue(keys);self.assertTrue(all('n' not in k for k in keys))
    def test_generated_adapters_have_unique_inputs_and_no_controls(self):
        for table in g.tables():
            lines=table.splitlines();self.assertEqual(len(lines),len({x.split('\t')[0] for x in lines}))
            self.assertFalse(any(ord(c)<32 and c not in '\t\n' for c in table))
    def test_unsupported_target_rejected(self):
        with self.assertRaises(ValueError):g.encode('未対応')
if __name__=='__main__':unittest.main()
