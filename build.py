# アプリ版 index.html を作る：src/exkuji.html（本体）＋ PWAの設定 ＋ Firebaseの接続
import json,pathlib
R=pathlib.Path(__file__).parent
head=(R/'src/head.html').read_text()
body=(R/'src/exkuji.html').read_text()
cfg=json.loads((R/'src/firebase-config.json').read_text())
cfg={k:cfg[k] for k in ['apiKey','authDomain','projectId','storageBucket','messagingSenderId','appId']}
pre='<script>window.EX_SHARED=true;</script>\n'
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
</script>
'''
out=head.replace('</head>',pre+'</head>')+'\n<body>\n'+body+'\n'+fb+sw+'</body>\n</html>\n'
(R/'index.html').write_text(out)
print('index.html',len(out))
