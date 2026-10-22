# アプリ版 index.html を作る：src/exkuji.html（本体）＋ PWAの設定 ＋ Firebaseの接続
import json,pathlib
R=pathlib.Path(__file__).parent
head=(R/'src/head.html').read_text()
body=(R/'src/exkuji.html').read_text()
cfg=json.loads((R/'src/firebase-config.json').read_text())
cfg={k:cfg[k] for k in ['apiKey','authDomain','projectId','storageBucket','messagingSenderId','appId']}
import datetime
ver=(datetime.datetime.utcnow()+datetime.timedelta(hours=9)).strftime('%m/%d %H:%M')
pre='<meta name="exkuji-build" content="'+ver+'">\n<script>window.EX_SHARED=true;window.EX_BUILD="版 '+ver+'";</script>\n'
fb='''<script type="module">
// Firebase（ログインと共有データ）に接続する
(async()=>{
  const V='https://www.gstatic.com/firebasejs/10.14.1/';
  try{
    const [{initializeApp},A,F]=await Promise.all([import(V+'firebase-app.js'),import(V+'firebase-auth.js'),import(V+'firebase-firestore.js')]);
    const app=initializeApp(%s);
    const auth=A.getAuth(app);
    const fs=F.initializeFirestore(app,{experimentalAutoDetectLongPolling:true});
    const R=p=>F.doc(fs,p);
    window.FBX={
      onAuth:cb=>A.onAuthStateChanged(auth,u=>cb(u&&u.email?{email:u.email.toLowerCase()}:null)),
      signUp:(e,p)=>A.createUserWithEmailAndPassword(auth,e,p),
      signIn:(e,p)=>A.signInWithEmailAndPassword(auth,e,p),
      reset:e=>A.sendPasswordResetEmail(auth,e),
      signOut:()=>A.signOut(auth),
      watchDoc:(p,cb,err)=>F.onSnapshot(R(p),s=>cb(s.exists()?s.data():null),err),
      watchCol:(c,o,cb,err)=>{const cs=[];o=o||{};
        if(o.eq)cs.push(F.where(o.eq[0],'==',o.eq[1]));if(o.order)cs.push(F.orderBy(o.order,'desc'));if(o.limit)cs.push(F.limit(o.limit));
        return F.onSnapshot(F.query(F.collection(fs,c),...cs),s=>cb(s.docs.map(d=>({id:d.id,data:d.data()}))),err)},
      tx:(p,fn)=>F.runTransaction(fs,async t=>{const s=await t.get(R(p));const nd=fn(s.exists()?s.data():null);if(nd===undefined)return undefined;t.set(R(p),nd);return nd}),
      set:(p,d)=>F.setDoc(R(p),d),
      del:p=>F.deleteDoc(R(p))
    };
    window.dispatchEvent(new Event('fbready'));
  }catch(e){console.error('Firebaseに接続できませんでした',e)}
})();
</script>
''' % json.dumps(cfg)
sw='''<script>
if('serviceWorker' in navigator){window.addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{})})}
// 新しい版が出ていたら自動で切り替える（引いている最中は待つ）
(function(){let shown=false;
  async function check(boot){try{const t=await fetch('index.html?v='+Date.now(),{cache:'no-store'}).then(r=>r.text());const m=t.match(/EX_BUILD="([^"]*)"/);if(!m||m[1]===window.EX_BUILD)return;
    const busy=document.body.classList.contains('drawing')||document.querySelector('.fx,.stepfx,.modal:not([hidden])');
    let last=0;try{last=+sessionStorage.getItem('exk-rl')||0}catch(e){}
    if((boot||!busy)&&Date.now()-last>60000){try{sessionStorage.setItem('exk-rl',Date.now())}catch(e){}location.reload();return}
    if(shown)return;shown=true;const d=document.createElement('button');d.textContent='新しい版があります（タップで更新）';d.style.cssText='position:fixed;left:50%;bottom:calc(14px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:999;padding:12px 18px;border:0;border-radius:999px;background:#FFD25A;color:#1a1300;font-weight:800;box-shadow:0 6px 20px rgba(0,0,0,.4)';d.onclick=()=>location.reload();document.body.appendChild(d)}catch(e){}}
  window.addEventListener('load',()=>setTimeout(()=>check(true),1500));
  document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')check(false)});
  setInterval(()=>check(false),5*60*1000);
})();
</script>
'''
out=head.replace('</head>',pre+'</head>')+'\n<body>\n'+body+'\n'+fb+sw+'</body>\n</html>\n'
(R/'index.html').write_text(out)
print('index.html',len(out))
