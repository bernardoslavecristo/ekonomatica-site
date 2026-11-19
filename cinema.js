/* Visual cinematográfico progressivo: Canvas 2D sem WebGL para compatibilidade Android. */
(()=>{'use strict';
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const small=matchMedia('(max-width: 780px)').matches;
const hero=document.querySelector('.hero')||document.querySelector('.intro');
if(!hero)return;
if(!document.querySelector('.eko-cinema-tag')){
 const tag=document.createElement('div');tag.className='eko-cinema-tag';tag.textContent=document.documentElement.lang.toLowerCase().startsWith('es')?'TECNOLOGÍA • IA • AUTOMATIZACIÓN':'TECNOLOGIA • IA • AUTOMAÇÃO';
 const target=hero.querySelector('h1');if(target)target.before(tag);
}
if('IntersectionObserver'in window&&!reduced){
 const obs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('eko-visible');obs.unobserve(e.target)}})},{rootMargin:'0px 0px -35px 0px',threshold:.02});
 document.querySelectorAll('.sectionhead,.work,.section .card,.section .tile,.panel').forEach(e=>{e.classList.add('eko-reveal');obs.observe(e)});
}
const surface=hero.querySelector('.visual');if(surface){const orb=document.createElement('div');orb.className='eko-holo';orb.setAttribute('aria-hidden','true');orb.innerHTML='<div class="eko-holo-core"></div><div class="eko-holo-ring"></div><div class="eko-holo-ring"></div>';surface.prepend(orb)}
if(reduced)return;
const canvas=document.createElement('canvas');canvas.id='eko-cinema-canvas';canvas.setAttribute('aria-hidden','true');document.body.prepend(canvas);
const ctx=canvas.getContext('2d',{alpha:true});if(!ctx)return;
let w=0,h=0,dpr=1,t=0,raf=0;const count=small?27:70;let pts=[];
function resize(){
 dpr=Math.min(devicePixelRatio||1,1.5);w=Math.max(1,innerWidth);h=Math.min(850,Math.max(440,innerHeight*1.15));
 canvas.style.height=h+'px';canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);
 pts=Array.from({length:count},(_,i)=>{const a=i*2.399963;const r=Math.sqrt((i+.5)/count);return {x:w*(.63+.28*r*Math.cos(a)),y:h*(.45+.37*r*Math.sin(a)),z:Math.sin(i*1.94),a:.4+.6*(i%7)/7}});
}
function draw(){
 if(document.hidden){raf=0;return}
 t+=.013;ctx.clearRect(0,0,w,h);
 const x0=w*(small?.72:.70),y0=h*.43,r=Math.min(w*.23,h*.32);
 const glow=ctx.createRadialGradient(x0,y0,3,x0,y0,r*1.4);glow.addColorStop(0,'rgba(42,240,222,.14)');glow.addColorStop(.4,'rgba(26,153,190,.075)');glow.addColorStop(1,'rgba(18,53,110,0)');ctx.fillStyle=glow;ctx.fillRect(x0-r*1.4,y0-r*1.4,r*2.8,r*2.8);
 for(let i=0;i<pts.length;i++){const p=pts[i],px=p.x+Math.sin(t+p.z)*9,py=p.y+Math.cos(t*.8+p.z)*8;
 for(let j=i+1;j<pts.length;j++){const q=pts[j];const dx=px-q.x,dy=py-q.y,dist=Math.hypot(dx,dy);if(dist<Math.min(w*.18,155)){ctx.strokeStyle='rgba(88,234,223,'+(.11*(1-dist/155)).toFixed(3)+')';ctx.lineWidth=.7;ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(q.x,q.y);ctx.stroke();}}
 ctx.fillStyle='rgba(121,249,231,'+(.28+p.a*.55)+')';ctx.beginPath();ctx.arc(px,py,small?1.5:2,0,Math.PI*2);ctx.fill();
 }raf=requestAnimationFrame(draw);
}
const visible=new IntersectionObserver(e=>{if(e[0].isIntersecting&&!raf)draw();else if(!e[0].isIntersecting&&raf){cancelAnimationFrame(raf);raf=0}},{threshold:0});visible.observe(canvas);
addEventListener('resize',()=>{resize()},{passive:true});document.addEventListener('visibilitychange',()=>{if(!document.hidden&&!raf)draw()});
resize();
})();
