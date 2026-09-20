const {test}=require('node:test');const assert=require('node:assert/strict');const {clean,complete}=require('./core.js');
test('storage allowlist drops input, timestamps, unexpected lessons and invalid values',()=>{
 const p=clean({schemaVersion:1,layoutVersion:'2',text:'example',time:123,lessons:{a:{completed:2,bestAccuracy:94,wrong:'example',keys:['x'],time:1},b:{completed:-1,bestAccuracy:100},unknown:{completed:1,bestAccuracy:100}}},['a','b'],'2');
 assert.deepEqual(p,{schemaVersion:1,layoutVersion:'2',lessons:{a:{completed:2,bestAccuracy:94}}});
});
test('separate versions, corruption, arrays and unbounded counters are not restored',()=>{
 for(const input of [null,{},[],{schemaVersion:1,layoutVersion:'old',lessons:{a:{completed:1,bestAccuracy:100}}},{schemaVersion:1,layoutVersion:'2',lessons:{a:{completed:Infinity,bestAccuracy:100}}}])assert.deepEqual(clean(input,['a'],'2').lessons,{});
});
test('completed lessons only accumulate bounded anonymous aggregates',()=>{let p=clean(null,['a'],'2');complete(p,'a',80);complete(p,'a',72);assert.deepEqual(p.lessons.a,{completed:2,bestAccuracy:80});p.lessons.a.completed=1000000;complete(p,'a',95.7);assert.deepEqual(p.lessons.a,{completed:1000000,bestAccuracy:96});});
