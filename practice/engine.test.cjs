const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');const vm=require('node:vm');
const {create,token}=require('./engine.js');
const context={window:{}};vm.runInNewContext(fs.readFileSync(__dirname+'/data.js','utf8'),context);
const data=context.window.WKR_DATA;
test('every canonical rule produces its specified output at a boundary',()=>{
 for(const r of data.rules){const e=create(data.rules);r.keys.forEach(k=>e.feed(k));assert.equal(e.flush(),r.output);}
});
test('all lesson spellings produce the target without WKR or an IME',()=>{
 for(const l of data.lessons)for(const x of l.exercises){const e=create(data.rules);x.keys.forEach(k=>e.feed(k));assert.equal(e.flush(),x.text);}
});
test('prefix replacement, fallback, explicit vowel and triple sequence',()=>{
 const e=create(data.rules);assert.equal(e.feed('e'),'か');assert.equal(e.feed('k'),'き');
 e.reset();for(const k of 'ehk')e.feed(k);assert.equal(e.flush(),'かい');
 e.reset();for(const k of 'wer')e.feed(k);assert.equal(e.flush(),'わから');
 e.reset();for(const k of 'wjh')e.feed(k);assert.equal(e.flush(),'ゔぁ');
});
test('backspace discards a provisional group or deletes a completed character',()=>{
 const e=create(data.rules);e.feed('w');e.feed('j');assert.equal(e.backspace(),'');
 e.feed('e');e.feed('k');assert.equal(e.backspace(),'');
 e.feed('q');e.feed('q');assert.equal(e.backspace(),'');e.feed('h');assert.equal(e.flush(),'あ');
});
test('current text is bounded and reset forgets pending state',()=>{
 const e=create(data.rules,4);for(let i=0;i<20;i++)e.feed('h');assert.equal(e.text(),'ああああ');
 e.reset();assert.equal(e.text(),'');assert.equal(e.pending(),false);
});
test('QWERTY positions, Shift symbols and composition/shortcut exclusion',()=>{
 assert.equal(token({code:'KeyH',key:'h'}),'h');assert.equal(token({code:'Semicolon',key:';'}),';');
 assert.equal(token({code:'Digit1',key:'!',shiftKey:true}),'Shift+1');
 for(const flag of ['metaKey','ctrlKey','altKey','isComposing'])assert.equal(token({code:'KeyH',key:'h',[flag]:true}),null);
});
