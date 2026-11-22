/* Ekonomática / Neural Core: cena Three.js 3D verdadeira. Sem chaves nem chamadas à OpenAI aqui. */
(()=>{'use strict';
document.getElementById('year').textContent=new Date().getFullYear();
const canvas=document.getElementById('ek3d');
if(!canvas||matchMedia('(prefers-reduced-motion: reduce)').matches||navigator.connection?.saveData)return;
const small=()=>window.innerWidth<900;
const low=()=>window.innerWidth<540||navigator.hardwareConcurrency<=4;
const state={scene:0,progress:0,target:0,drag:0,tilt:0,mx:0,my:0,active:true};
const sections=[...document.querySelectorAll('[data-scene]')];
let width=innerWidth,height=innerHeight,renderer=null;
function scrollState(){
  let idx=0,best=Infinity;
  sections.forEach((section,i)=>{const d=Math.abs(section.getBoundingClientRect().top);if(d<best){best=d;idx=i}});
  state.scene=idx;
  const rect=sections[idx]?.getBoundingClientRect(),span=Math.max(1,rect?.height||height);
  state.target=idx+Math.max(0,Math.min(1,-(rect?.top||0)/span));
  document.querySelector('.rail-label').textContent=String(Math.min(4,idx+1)).padStart(2,'0')+' / 04';
}
let queued=false;addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(()=>{scrollState();queued=false})}},{passive:true});
let touchStart=null;
document.addEventListener('pointerdown',e=>{if(e.target.closest('a,button,input,textarea,select,#eko-chat-box'))return;touchStart={x:e.clientX,y:e.clientY};},{passive:true});
document.addEventListener('pointermove',e=>{
  if(!touchStart&&e.pointerType==='touch')return;
  state.mx=(e.clientX/Math.max(1,width)-.5)*2;
  state.my=(e.clientY/Math.max(1,height)-.5)*2;
  if(touchStart){
    const dx=e.clientX-touchStart.x,dy=e.clientY-touchStart.y;
    if(e.pointerType!=='touch'||Math.abs(dx)>Math.abs(dy)*1.2)state.drag+=dx*.006;
    state.tilt=Math.max(-.6,Math.min(.6,state.tilt+(e.pointerType==='touch'?0:dy*.002)));
    touchStart={x:e.clientX,y:e.clientY};
  }
},{passive:true});
document.addEventListener('pointerup',()=>{touchStart=null},{passive:true});
document.addEventListener('pointercancel',()=>{touchStart=null},{passive:true});
document.addEventListener('visibilitychange',()=>{state.active=!document.hidden},{passive:true});
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function lerp(a,b,t){return a+(b-a)*t}
import('https://cdn.jsdelivr.net/npm/three@0.168.0/build/three.module.js').then(THREE=>{
  if(!THREE.WebGLRenderer)return;
  let deviceLow=low();
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(42,width/height,.1,100);
  camera.position.set(0,0,11.5);
  renderer=new THREE.WebGLRenderer({canvas,antialias:!deviceLow,alpha:true,powerPreference:deviceLow?'low-power':'high-performance',precision:'mediump'});
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,deviceLow?1.15:1.65));
  renderer.setSize(width,height,false);
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.65;
  const assembly=new THREE.Group();scene.add(assembly);
  // Modelo original: icosaedro metálico facetado, núcleo emissivo, cascas transparentes e órbitas reais.
  const geo=new THREE.IcosahedronGeometry(1.46,deviceLow?3:5);
  const metal=new THREE.MeshPhysicalMaterial({color:0x052937,metalness:.75,roughness:.23,clearcoat:1,clearcoatRoughness:.12,flatShading:true,transparent:true,opacity:.90,side:THREE.DoubleSide});
  const core=new THREE.Mesh(geo,metal);assembly.add(core);
  const inner=new THREE.Mesh(new THREE.IcosahedronGeometry(.95,deviceLow?2:3),new THREE.MeshPhysicalMaterial({color:0x28c6dc,emissive:0x0084a3,emissiveIntensity:.64,metalness:.45,roughness:.12,transparent:true,opacity:.75}));
  assembly.add(inner);
  const shell=new THREE.Mesh(new THREE.IcosahedronGeometry(1.72,deviceLow?2:3),new THREE.MeshBasicMaterial({color:0x73f8e8,wireframe:true,transparent:true,opacity:.22,depthWrite:false}));assembly.add(shell);
  const shell2=new THREE.Mesh(new THREE.IcosahedronGeometry(2.09,1),new THREE.MeshBasicMaterial({color:0x38badd,wireframe:true,transparent:true,opacity:.17,depthWrite:false}));assembly.add(shell2);
  const rings=[];for(let i=0;i<3;i++){
    const radius=[2.36,2.72,3.04][i];
    const ring=new THREE.Mesh(new THREE.TorusGeometry(radius,i===0?.016:.011,6,100),new THREE.MeshBasicMaterial({color:[0x7cfff0,0x219bbf,0x6190fa][i],transparent:true,opacity:[.74,.44,.28][i],depthWrite:false}));
    ring.rotation.set([.7,1.12,.28][i],[.3,-.5,1.35][i],[0,.4,.7][i]);rings.push(ring);assembly.add(ring);
  }
  const spikesCount=deviceLow?140:320;
  const points=new Float32Array(spikesCount*3);
  const sphere=new Float32Array(spikesCount*3);
  for(let i=0;i<spikesCount;i++){
    const a=i*2.3999632297,yy=1-2*(i+.5)/spikesCount,rr=Math.sqrt(Math.max(0,1-yy*yy)),r=2.12+.18*Math.sin(i*4.22);
    points[3*i]=r*rr*Math.cos(a);points[3*i+1]=r*yy;points[3*i+2]=r*rr*Math.sin(a);
    sphere[3*i]=rr*Math.cos(a);sphere[3*i+1]=yy;sphere[3*i+2]=rr*Math.sin(a);
  }
  const pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(points,3));
  const pmat=new THREE.PointsMaterial({color:0x8dfcf1,size:deviceLow?.05:.055,transparent:true,opacity:.98,depthWrite:false,blending:THREE.AdditiveBlending});
  const satellites=new THREE.Points(pg,pmat);assembly.add(satellites);
  const curveVertices=[];
  for(let i=0;i<spikesCount;i++){
     const j=(i*37+11)%spikesCount;const a=new THREE.Vector3(points[i*3],points[i*3+1],points[i*3+2]),b=new THREE.Vector3(points[j*3],points[j*3+1],points[j*3+2]);
     if(a.distanceTo(b)<2.6){curveVertices.push(a.x,a.y,a.z,b.x,b.y,b.z)}
  }
  const linesGeometry=new THREE.BufferGeometry();linesGeometry.setAttribute('position',new THREE.Float32BufferAttribute(curveVertices,3));
  const lines=new THREE.LineSegments(linesGeometry,new THREE.LineBasicMaterial({color:0x52c8da,transparent:true,opacity:.18,depthWrite:false}));assembly.add(lines);
  const starCount=deviceLow?170:480,starPositions=new Float32Array(starCount*3);for(let i=0;i<starCount;i++){starPositions[i*3]=(Math.random()-.5)*24;starPositions[i*3+1]=(Math.random()-.5)*15;starPositions[i*3+2]=-4-Math.random()*15}
  const starGeo=new THREE.BufferGeometry();starGeo.setAttribute('position',new THREE.BufferAttribute(starPositions,3));
  const stars=new THREE.Points(starGeo,new THREE.PointsMaterial({color:0x6bbccf,size:deviceLow?.026:.032,transparent:true,opacity:.65,depthWrite:false}));scene.add(stars);
  const keyLight=new THREE.PointLight(0x93fff4,64,30,2);keyLight.position.set(-4,4,5);scene.add(keyLight);
  const blueLight=new THREE.PointLight(0x336aff,38,25,2);blueLight.position.set(5,-3,2);scene.add(blueLight);
  const ambient=new THREE.AmbientLight(0x83bdda,1.3);scene.add(ambient);
  function resize(){
    width=innerWidth;height=innerHeight;deviceLow=low();
    camera.aspect=width/Math.max(1,height);camera.fov=small()?47:42;camera.updateProjectionMatrix();
    renderer.setPixelRatio(Math.min(devicePixelRatio||1,deviceLow?1.15:1.65));renderer.setSize(width,height,false);
  }
  addEventListener('resize',resize,{passive:true});
  let last=0,animation=0;const timeOrigin=performance.now();
  function render(now){
    animation=requestAnimationFrame(render);
    if(!state.active)return;
    if(deviceLow&&now-last<33)return; // ~30fps em celulares simples
    last=now;
    const t=(now-timeOrigin)*.001;
    state.progress=lerp(state.progress,state.target,.045);
    const phase=state.progress,step=Math.floor(phase),fraction=phase-step;
    const mobile=small(),xBase=mobile?0:2.8,yBase=mobile?1.15:.15;
    const cycle=phase*1.1;
    assembly.position.x=lerp(assembly.position.x,xBase+(mobile?0:.24*Math.sin(cycle)),.05);
    assembly.position.y=lerp(assembly.position.y,yBase+.13*Math.sin(t*.7)+(mobile?.1*Math.sin(cycle):0),.05);
    assembly.rotation.y=t*.14+phase*.91+state.drag+state.mx*.12;
    assembly.rotation.x=Math.sin(t*.27)*.09+phase*.21+state.tilt+state.my*.07;
    assembly.rotation.z=Math.sin(t*.13)*.04+phase*.17;
    // Cada capítulo transforma de verdade o objeto: núcleo, cascas e órbitas.
    // 0 núcleo / 1 automação / 2 agente / 3 conexões globais.
    const scale=mobile?(width<400?.61:.71):clamp(width/1500,.76,1.16);
    const pulse=1+Math.sin(fraction*Math.PI)*.09;
    const isFlow=clamp(1-Math.abs(phase-1.42),0,1);
    const isAgents=clamp(1-Math.abs(phase-2.42),0,1);
    const isNetworks=clamp(1-Math.abs(phase-3.30),0,1);
    const sceneScale=scale*pulse*(1-.12*isFlow+.18*isNetworks);
    assembly.scale.setScalar(lerp(assembly.scale.x,sceneScale,.04));
    inner.scale.setScalar(lerp(inner.scale.x,1+.25*isAgents-.18*isFlow,.06));
    core.scale.setScalar(lerp(core.scale.x,1-.21*isAgents+.12*isFlow,.06));
    shell.scale.setScalar(lerp(shell.scale.x,1+.20*isNetworks+.08*isAgents,.05));
    shell2.scale.setScalar(lerp(shell2.scale.x,1+.26*isNetworks,.05));
    shell.material.opacity=lerp(shell.material.opacity,.22+.23*isFlow+.12*isNetworks,.05);
    shell2.material.opacity=lerp(shell2.material.opacity,.17+.19*isNetworks,.05);
    lines.material.opacity=lerp(lines.material.opacity,.18+.24*isFlow+.28*isNetworks,.05);
    pmat.opacity=lerp(pmat.opacity,.83+.15*isAgents,.05);
    inner.rotation.set(-t*.15,t*.3,t*.07);
    shell.rotation.set(t*.13,-t*.19,0);
    shell2.rotation.set(-t*.07,t*.11,0);
    rings.forEach((ring,i)=>{
      ring.rotation.z+=.0015*(i%2?1:-1);ring.rotation.y+=.0009*(i+1);
      const spread=1+(.25*isFlow)+(.11*isNetworks*i);
      ring.scale.setScalar(lerp(ring.scale.x,spread,.045));
      ring.material.opacity=lerp(ring.material.opacity,[.74,.44,.28][i]*(1-.36*isAgents+.24*isNetworks),.05);
    });
    satellites.rotation.y=-t*.06;
    lines.rotation.y=-t*.04;
    const cameraTarget=mobile?11.7:11.5;
    camera.position.z=lerp(camera.position.z,cameraTarget-Math.sin(phase*.9)*.5,.04);
    camera.position.x=lerp(camera.position.x,phase*.08,.02);
    camera.lookAt(0,0,0);
    renderer.render(scene,camera);
  }
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();cancelAnimationFrame(animation);document.body.classList.remove('webgl-ready')},{passive:false});
  scrollState();document.body.classList.add('webgl-ready');animation=requestAnimationFrame(render);
}).catch(error=>{console.warn('Ekonomática 3D: usando visual alternativo',error?.message||error);document.body.classList.add('webgl-fallback')});
})();
