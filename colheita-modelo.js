/* Modelo explicável de cenário fictício. Sem inferência agronômica ou chamadas de IA. */
(function(root){
'use strict';
function integer(n,min,max){return Number.isSafeInteger(n)&&n>=min&&n<=max;}
function validate(s){
 if(!s||!integer(s.capacity,0,100000)||!integer(s.fixed,0,100000))throw new Error('Informe capacidade e meta diária inteiras entre 0 e 100.000.');
 if(!Array.isArray(s.demand)||s.demand.length!==7||s.demand.some(n=>!integer(n,0,100000)))throw new Error('Informe sete pedidos inteiros entre 0 e 100.000.');
 if(!Array.isArray(s.batches)||s.batches.length!==3)throw new Error('Informe os três canteiros.');
 s.batches.forEach((b,i)=>{if(!integer(b.quantity,0,100000)||!integer(b.ready,1,7)||!integer(b.expires,b.ready,7))throw new Error('Canteiro '+String.fromCharCode(65+i)+': use quantidades inteiras e dia limite igual ou posterior ao dia inicial (1 a 7).');});
}
function run(s,planned){
 const stock=s.batches.map((b,i)=>({...b,id:String.fromCharCode(65+i),index:i,remaining:b.quantity}));
 const days=[];
 for(let day=1;day<=7;day++){
  const wanted=s.demand[day-1];let left=Math.min(s.capacity,planned?wanted:s.fixed);const picked=[];
  const available=stock.filter(b=>b.ready<=day&&b.expires>=day).sort((a,b)=>a.expires-b.expires||a.index-b.index);
  for(const b of available){const n=Math.min(left,b.remaining);if(n){picked.push({batch:b.id,quantity:n});b.remaining-=n;left-=n;}}
  const harvested=picked.reduce((n,b)=>n+b.quantity,0),delivered=Math.min(harvested,wanted),excess=harvested-delivered;
  let expired=0;for(const b of stock){if(b.expires===day){expired+=b.remaining;b.remaining=0;}}
  days.push({day,demand:wanted,picked,harvested,delivered,shortage:wanted-delivered,excess,expired,loss:excess+expired});
 }
 const totals={demand:0,harvested:0,delivered:0,shortage:0,excess:0,expired:0,loss:0};
 for(const d of days)for(const k of Object.keys(totals))totals[k]+=d[k];
 totals.production=s.batches.reduce((n,b)=>n+b.quantity,0);totals.remaining=stock.reduce((n,b)=>n+b.remaining,0);
 return {days,totals};
}
function compare(s){validate(s);return {baseline:run(s,false),planned:run(s,true)};}
const api=Object.freeze({compare});
if(typeof module==='object'&&module.exports)module.exports=api;else root.ColheitaModelo=api;
})(typeof window==='object'?window:globalThis);
