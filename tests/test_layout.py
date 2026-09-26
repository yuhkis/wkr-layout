import sys, unittest, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import generate as g
class LayoutTests(unittest.TestCase):
    def test_inventory(self):
        g.validate()
        self.assertEqual(len(g.RULES),171)
        # 2.0.0-beta.4 removed the symbols and arrows: every rule is kana sent as romaji.
        self.assertTrue(all(r['group']=='kana' and r['delivery']=='romaji' for r in g.RULES))
    def test_every_rule_round_trips(self):
        for rule in g.RULES:
            with self.subTest(rule=rule['id']): self.assertEqual(g.decode(rule['keys']),rule['output'])
    def test_prefix_boundaries(self):
        for keys,text in [('wer','わから'),('ehk','かい'),('qhwe','ぁわか'),('qwe','ゎか'),('qn','ぁいぇ'),('qu','ぁっ'),('qq','ぁぁ'),('qp','ゃ'),('qw','ゎ'),
                          ('wjh','ゔぁ'),('wjj','ゔ'),('wjp','ゔゃ'),('wju','ゔっ'),('wjn','ゔいぇ'),('wn','わいぇ'),
                          ('en','きぇ'),('eu','かっ'),('em','かん'),('ey','かー'),('ehn','かいぇ'),('sn','しぇ'),('cn','ぢぇ'),('xn','ふぇ'),('x;','ふぇ'),
                          ('ep','きゃ'),('ehp','かや'),('ci','どぅ'),('cp','でぃ'),('xo','てゅ'),('xp','てぃ'),('mm','んん'),('uu','っっ'),('nn','いぇいぇ')]:
            self.assertEqual(g.decode(list(keys)),text)
    def test_nasal_on_m_geminate_on_u_and_n_is_ye(self):
        # 2.0.0-beta.4: ん has one key, M (as in 2.0.0-beta.1), っ is on U, and N gives いぇ.
        self.assertEqual(g.BY_KEYS[('m',)]['id'],'m-n');self.assertEqual(g.BY_KEYS[('m',)]['output'],'ん')
        self.assertEqual(g.BY_KEYS[('u',)]['id'],'u-small-tsu');self.assertEqual(g.BY_KEYS[('u',)]['output'],'っ')
        self.assertEqual(g.BY_KEYS[('n',)]['id'],'n-ye');self.assertEqual(g.BY_KEYS[('n',)]['output'],'いぇ')
        self.assertEqual([r['keys'] for r in g.RULES if r['output']=='ん'],[['m']])
        self.assertEqual([r['keys'] for r in g.RULES if r['output']=='っ'],[['u']])
    def test_n_is_the_ye_column_after_a_row(self):
        expected={'e':'きぇ','s':'しぇ','f':'ちぇ','d':'にぇ','g':'ひぇ','v':'みぇ','r':'りぇ','a':'ぎぇ','z':'じぇ','c':'ぢぇ','b':'びぇ','t':'ぴぇ','x':'ふぇ'}
        self.assertEqual({ks[0]:r['output'] for ks,r in g.BY_KEYS.items() if len(ks)==2 and ks[1]=='n'},expected)
        self.assertNotIn(('w','j','n'),g.BY_KEYS)
    def test_ya_column_is_on_p_and_no_rule_follows_q_q(self):
        # 2.0.0-beta.3: や alone and the ゃ column after a row key are on P.
        # 2.0.0-beta.4 removed the symbol layer behind Q Q: Q Q is ぁぁ.
        self.assertEqual(g.BY_KEYS[('p',)]['output'],'や')
        rows=[k for (k,) in [r for r in g.BY_KEYS if len(r)==1] if (k,'p') in g.BY_KEYS]
        self.assertEqual(len(rows),15)
        for row in rows:
            self.assertNotIn((row,'u'),g.BY_KEYS);self.assertNotIn((row,'y'),g.BY_KEYS)
        self.assertFalse(any(r['keys'][0]=='p' and len(r['keys'])>1 for r in g.RULES))
        self.assertFalse(any(r['keys'][:2]==['q','q'] for r in g.RULES))
    def test_all_lessons_use_current_rules(self):
        data=g.practice_data()
        self.assertEqual(len(data['lessons']),11)
        for lesson in data['lessons']:
            for x in lesson['exercises']: self.assertEqual(g.decode(x['keys']),x['text'])
    def test_no_rule_gives_two_kana(self):
        # 2.0.0-beta.3 removed the special column, the only rules that did.
        self.assertFalse(any(r['group']=='shortcuts' for r in g.RULES))
    def test_lessons_type_n_on_m_and_small_tsu_on_u(self):
        exercises=[x for l in g.practice_data()['lessons'] for x in l['exercises']]
        for kana,key in [('ん','m'),('っ','u')]:
            keys=[x['keys'] for x in exercises if kana in x['text']]
            with self.subTest(kana=kana):self.assertTrue(keys);self.assertTrue(all(key in k for k in keys))
    def test_generated_adapters_have_unique_inputs_and_no_controls(self):
        for table in g.tables():
            lines=table.splitlines();self.assertEqual(len(lines),len({x.split('\t')[0] for x in lines}))
            self.assertFalse(any(ord(c)<32 and c not in '\t\n' for c in table))
    def test_unsupported_target_rejected(self):
        with self.assertRaises(ValueError):g.encode('未対応')
if __name__=='__main__':unittest.main()
