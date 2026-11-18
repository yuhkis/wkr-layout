const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');

// Execute the shipped UI and real core/engine with synthetic DOM events only.
// These fixtures contain no captured input, event logs or personal progress.
class Element {
  constructor(document){this.document=document;this.listeners={};this.children=[];this.value='';this.textContent='';this.disabled=false;this.checked=false;}
  addEventListener(type,listener){(this.listeners[type]??=[]).push(listener);}
  fire(type,values={}){
    const event={key:'',code:'',keyCode:0,isComposing:false,repeat:false,metaKey:false,ctrlKey:false,altKey:false,...values,
      defaultPrevented:false,preventDefault(){this.defaultPrevented=true;}};
    for(const listener of this.listeners[type]??[])listener(event);
    return event;
  }
  append(...nodes){this.children.push(...nodes);}
  replaceChildren(...nodes){this.children=[...nodes];}
  setAttribute(){}
  setSelectionRange(){}
  focus(){this.document.activeElement=this;}
}
function app({native=false}={}){
  const elements=new Map(),document={};
  for(const id of fs.readFileSync(path.join(__dirname,'index.html'),'utf8').matchAll(/id="([^"]+)"/g))elements.set(id[1],new Element(document));
  document.getElementById=id=>{assert.ok(elements.has(id),'UI element must exist: '+id);return elements.get(id);};
  document.createElement=()=>new Element(document);
  const modes=['trial','ime'].map(value=>Object.assign(new Element(document),{value}));
  document.querySelectorAll=selector=>{assert.equal(selector,'input[name=mode]');return modes;};
  const store=new Map(),messages=[],window=new Element(document);
  if(native)window.webkit={messageHandlers:{wkrProgress:{postMessage:message=>messages.push(JSON.parse(JSON.stringify(message)))}}};
  const localStorage={getItem:key=>store.get(key)??null,setItem:(key,value)=>store.set(key,value),removeItem:key=>store.delete(key)};
  const context=vm.createContext({window,document,localStorage});
  for(const file of ['engine.js','core.js','data.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,file),'utf8'),context,{filename:file});
  // One public kana target makes every successful submission observable.
  window.WKR_DATA.lessons=[{id:'vowels',title:'合成課題',tip:'',stage:'基本',exercises:[{text:'あ',keys:['h']}]}];
  vm.runInContext(fs.readFileSync(path.join(__dirname,'app.js'),'utf8'),context,{filename:'app.js'});
  const el=id=>document.getElementById(id),input=el('typing');
  return {el,input,store,messages,window,
    mode:value=>modes.find(n=>n.value===value).fire('change'),
    start:()=>input.fire('compositionstart'),end:()=>input.fire('compositionend'),update:()=>input.fire('compositionupdate'),
    down:values=>input.fire('keydown',{key:'Enter',code:'Enter',keyCode:13,...values}),
    up:values=>input.fire('keyup',{key:'Enter',code:'Enter',keyCode:13,...values}),
    answer:()=>{input.value='あ';},
    button:()=>el('grade').fire('click'),
    completed:()=>el('score').textContent.includes('課題完了'),
    save:()=>{el('save').checked=true;el('save').fire('change');}
  };
}
function ime(){const h=app();h.mode('ime');h.start();h.answer();return h;}
function notGraded(h){assert.equal(h.completed(),false);assert.equal(h.el('next').disabled,true);assert.equal(h.input.value,'あ');}
function gradedOnce(h){assert.equal(h.completed(),true);assert.equal(h.el('grade').disabled,true);assert.equal(h.el('next').disabled,false);assert.match(h.el('score').textContent,/正答率 100%/);assert.equal(h.el('lessons').children[0].children[0].textContent,'1回完了 · 最高100%');}

test('IME confirmation down/end/up does not grade; the next explicit Enter does',()=>{
 const h=ime();h.down({isComposing:true});h.end();notGraded(h);h.up();notGraded(h);h.down();gradedOnce(h);
});
test('confirmation keyup before compositionend is not overwritten by a new guard',()=>{
 const h=ime();h.down({isComposing:true});h.up({isComposing:true});h.end();notGraded(h);h.down();gradedOnce(h);
});
test('Process/229 with Enter code identifies the same confirmation and release',()=>{
 const h=ime();h.down({key:'Process',code:'Enter',keyCode:229,isComposing:true});h.up({key:'Process',code:'Enter',keyCode:229,isComposing:true});h.end();notGraded(h);h.down();gradedOnce(h);
});
test('late confirmation down after end stays guarded until its identified release',()=>{
 const h=ime();h.end();h.down();notGraded(h);h.down();notGraded(h);h.up();h.down();gradedOnce(h);
});
test('repeat after confirmation cannot submit or release the guard',()=>{
 const h=ime();h.down({isComposing:true});h.end();h.down({repeat:true});notGraded(h);h.up({repeat:true});h.down();notGraded(h);h.up();h.down();gradedOnce(h);
});
test('candidate Enter proof is discarded when composition continues with another key',()=>{
 const h=ime();h.down({isComposing:true});h.up({isComposing:true});h.down({key:'Process',code:'KeyA',keyCode:229,isComposing:true});h.end();h.down();notGraded(h);h.up();h.down();gradedOnce(h);
});
test('a final update after release conservatively keeps the guard; explicit grading works',()=>{
 const h=ime();h.down({isComposing:true});h.up({isComposing:true});h.update();h.end();h.down();notGraded(h);h.button();gradedOnce(h);
});
test('unknown 229 down and keyup alone never release a confirmation guard',()=>{
 const h=ime();h.end();h.down({key:'Process',code:'',keyCode:229});h.up({key:'Process',code:'',keyCode:229});h.down();notGraded(h);h.up();h.down();gradedOnce(h);
});
test('Enter, NumpadEnter and legacy13 release evidence is accepted independently',()=>{
 for(const release of [{key:'Process',code:'Enter',keyCode:229},{key:'Unidentified',code:'NumpadEnter',keyCode:0},{key:'Unidentified',code:'',keyCode:13}]){
  const h=ime();h.end();h.up(release);h.down({key:'Unidentified',code:'',keyCode:13});gradedOnce(h);
 }
});
test('missing release evidence stays guarded; the confirmed-input button is a fallback',()=>{
 const h=ime();h.end();h.down({key:'Process',code:'',keyCode:0});h.down();notGraded(h);h.down();notGraded(h);h.button();gradedOnce(h);
});
test('stale isComposing after end never latches composition; an identified release permits the next Enter',()=>{
 const h=ime();h.end();h.down({isComposing:true});notGraded(h);assert.equal(h.el('grade').disabled,false);h.up({isComposing:true});h.down();gradedOnce(h);
 const button=ime();button.end();button.down({isComposing:true});button.button();gradedOnce(button);
});
test('shortcut/repeated confirmation is not treated as released confirmation proof',()=>{
 for(const excluded of [{metaKey:true},{ctrlKey:true},{altKey:true},{repeat:true}]){
  const h=ime();h.down({isComposing:true,...excluded});h.up({isComposing:true,...excluded});h.end();h.down();notGraded(h);h.up();h.down();gradedOnce(h);
 }
});
test('grading button refuses composition and completed items and does not submit empty input',()=>{
 const h=ime();assert.equal(h.el('grade').disabled,true);h.button();notGraded(h);h.end();h.button();gradedOnce(h);h.button();gradedOnce(h);
 const empty=app();empty.mode('ime');empty.button();assert.equal(empty.completed(),false);assert.equal(empty.el('score').textContent,'');
});
test('retry, mode and lesson changes clear pending IME state',()=>{
 for(const reset of [h=>h.el('retry').fire('click'),h=>h.el('lessons').children[0].fire('click')]){
  const h=ime();h.end();reset(h);h.answer();h.down();gradedOnce(h);
 }
 const h=ime();h.end();h.mode('trial');h.down({key:'h',code:'KeyH',keyCode:72});h.button();gradedOnce(h);
});
test('pagehide clears transient composition and restores the explicit grading button',()=>{
 const h=ime();assert.equal(h.el('grade').disabled,true);h.window.fire('pagehide');assert.equal(h.input.value,'');assert.equal(h.el('grade').disabled,false);h.answer();h.button();gradedOnce(h);
});
test('identified editing keys begin new input but unknown events retain the guard',()=>{
 for(const key of ['a','Backspace','Delete']){const h=ime();h.end();h.down({key,code:'',keyCode:0});h.down();gradedOnce(h);}
 for(const key of ['Process','Unidentified','']){const h=ime();h.end();h.down({key,code:'',keyCode:0});h.down();notGraded(h);h.button();gradedOnce(h);}
});
test('QWERTY Enter and explicit button share the real engine and grade once',()=>{
 for(const submit of [h=>h.down(),h=>h.button()]){
  const h=app();h.down({key:'h',code:'KeyH',keyCode:72});assert.equal(h.input.value,'あ');submit(h);gradedOnce(h);h.button();gradedOnce(h);assert.equal(h.store.size,0);
 }
 const h=app();h.down({key:'d',code:'KeyD',keyCode:68});assert.equal(h.input.value,'た');h.button();assert.equal(h.completed(),false);assert.equal(h.input.value,'');
});
test('IME state and entered text do not reach storage or the native progress bridge',()=>{
 const h=app({native:true});h.mode('ime');h.save();h.start();h.answer();h.down({isComposing:true});h.up({isComposing:true});h.end();h.button();gradedOnce(h);
 const saves=h.messages.filter(m=>m.action==='save');assert.equal(saves.length,2);
 for(const m of saves){assert.deepEqual(Object.keys(m).sort(),['action','progress']);assert.deepEqual(Object.keys(m.progress).sort(),['layoutVersion','lessons','schemaVersion']);}
 assert.deepEqual(saves[1].progress.lessons,{vowels:{completed:1,bestAccuracy:100}});
 h.button();assert.equal(h.messages.filter(m=>m.action==='save').length,2);assert.equal(h.store.size,0);
});
