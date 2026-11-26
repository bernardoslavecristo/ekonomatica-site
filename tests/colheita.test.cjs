const test=require('node:test');
const assert=require('node:assert/strict');
const {compare}=require('../colheita-modelo.js');
const example=()=>({capacity:160,fixed:100,demand:[60,150,80,140,100,160,70],batches:[{quantity:250,ready:1,expires:3},{quantity:320,ready:3,expires:5},{quantity:260,ready:5,expires:7}]});
test('example conserves production and fulfills the shown daily plan',()=>{
 const s=example(),original=JSON.stringify(s),r=compare(s);
 assert.equal(r.baseline.totals.delivered,610);assert.equal(r.planned.totals.delivered,760);
 assert.equal(r.planned.totals.loss,70);assert.equal(r.baseline.totals.loss,220);
 for(const run of [r.baseline,r.planned]){assert.equal(run.totals.delivered+run.totals.loss+run.totals.remaining,830);assert.equal(run.totals.delivered+run.totals.shortage,760);}
 assert.equal(JSON.stringify(s),original);
 assert.deepEqual(r.planned.days[2].picked,[{batch:'A',quantity:40},{batch:'B',quantity:40}]);
});
test('capacity, zero production, zero demand and no labor remain meaningful',()=>{
 for(const modify of [s=>{s.capacity=0},s=>{s.demand.fill(0)},s=>{s.batches.forEach(b=>b.quantity=0)},s=>{s.capacity=70},s=>{s.fixed=0}]){
  const s=example();modify(s);const r=compare(s);
  for(const run of [r.baseline,r.planned]){
   assert.equal(run.totals.production,run.totals.delivered+run.totals.loss+run.totals.remaining);
   assert.equal(run.totals.demand,run.totals.delivered+run.totals.shortage);
   for(const d of run.days){assert.ok(d.harvested<=s.capacity);assert.ok(d.delivered<=d.demand);assert.ok(d.loss>=0);}
  }
  if(!s.capacity||!s.batches.some(b=>b.quantity))assert.equal(r.planned.totals.delivered,0);
 }
});
test('unready and expired batches cannot be harvested; earliest expiry wins',()=>{
 const s=example();s.batches=[{quantity:100,ready:7,expires:7},{quantity:100,ready:1,expires:1},{quantity:200,ready:1,expires:3}];
 const r=compare(s).planned;assert.deepEqual(r.days[0].picked,[{batch:'B',quantity:60}]);assert.equal(r.days[0].expired,40);
 assert.ok(r.days.slice(0,6).every(d=>d.picked.every(b=>b.batch!=='A')));assert.equal(r.days[6].picked[0].batch,'A');
});
test('invalid windows, nonintegers and nonfinite values are rejected',()=>{
 for(const modify of [s=>{s.batches[0].expires=0},s=>{s.batches[0].ready=4},s=>{s.demand[0]=NaN},s=>{s.capacity=-1},s=>{s.fixed=Infinity},s=>{s.demand[0]=1.5},s=>{s.batches[0].quantity=100001}]){const s=example();modify(s);assert.throws(()=>compare(s));}
});
test('a pre-collected stock can win when the daily rule intentionally excludes storage',()=>{
 // Both rules have no storage: the report must not claim global optimality.
 const s=example();s.demand.fill(0);s.demand[6]=100;s.batches=[{quantity:100,ready:1,expires:1},{quantity:0,ready:3,expires:5},{quantity:0,ready:5,expires:7}];
 const r=compare(s);assert.equal(r.planned.totals.delivered,0);assert.equal(r.planned.totals.shortage,100);assert.equal(r.planned.totals.expired,100);
});
