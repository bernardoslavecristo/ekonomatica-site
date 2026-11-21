import * as THREE from 'https://esm.sh/three@0.170.0';
const stage=document.getElementById('chef-stage');
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.8));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;stage.prepend(renderer.domElement);
const scene=new THREE.Scene();const camera=new THREE.PerspectiveCamera(35,1,.1,100);camera.position.set(0,0,7.6);
scene.add(new THREE.HemisphereLight(0xffe4e5,0x3c162d,2));const key=new THREE.DirectionalLight(0xffebcc,3);key.position.set(-3,5,7);scene.add(key);const rim=new THREE.DirectionalLight(0xff9a69,3);rim.position.set(4,2,-4);scene.add(rim);
const object=new THREE.Group();scene.add(object);
const gold=new THREE.MeshStandardMaterial({color:0xc68a3c,metalness:.78,roughness:.24});const pink=new THREE.MeshStandardMaterial({color:0xa73964,metalness:.38,roughness:.3});
const ring=new THREE.Mesh(new THREE.CylinderGeometry(2.13,2.13,.32,96),[pink,gold,gold]);ring.rotation.x=Math.PI/2;object.add(ring);
const border=new THREE.Mesh(new THREE.TorusGeometry(2.04,.065,16,120),gold);border.position.z=.19;object.add(border);
const borderBack=border.clone();borderBack.position.z=-.19;object.add(borderBack);
const faceGeometry=new THREE.CircleGeometry(1.98,96);const front=new THREE.Mesh(faceGeometry,new THREE.MeshStandardMaterial({color:0xffe3dc,side:THREE.DoubleSide,roughness:.55}));front.position.z=.169;object.add(front);
const back=new THREE.Mesh(faceGeometry,new THREE.MeshStandardMaterial({color:0xf1cad6,side:THREE.DoubleSide,roughness:.45}));back.position.z=-.169;back.rotation.y=Math.PI;object.add(back);
// A marca original permanece como textura frontal temporária, sem fingir que uma foto é um modelo 3D.
const loader=new THREE.TextureLoader();loader.load('chef-lu-logo.svg',texture=>{texture.colorSpace=THREE.SRGBColorSpace;front.material.map=texture;front.material.needsUpdate=true;},undefined,()=>{});
// Elementos volumétricos reais acrescentados à face da peça.
const pinkGloss=new THREE.MeshPhysicalMaterial({color:0xd94484,metalness:.22,roughness:.2,clearcoat:1,clearcoatRoughness:.12});
const cream=new THREE.MeshPhysicalMaterial({color:0xfff1e6,roughness:.35,clearcoat:.3});
const strawberry=new THREE.MeshStandardMaterial({color:0xc92348,roughness:.35});
const pedestal=new THREE.Mesh(new THREE.CylinderGeometry(.52,.57,.12,40),gold);pedestal.rotation.x=Math.PI/2;pedestal.position.set(-.91,-1.09,.38);object.add(pedestal);
const cake=new THREE.Mesh(new THREE.CylinderGeometry(.43,.44,.46,48),cream);cake.rotation.x=Math.PI/2;cake.position.set(-.91,-.68,.41);object.add(cake);
const glaze=new THREE.Mesh(new THREE.CylinderGeometry(.45,.45,.09,48),pinkGloss);glaze.rotation.x=Math.PI/2;glaze.position.set(-.91,-.68,.67);object.add(glaze);
for(let i=0;i<7;i++){const a=i*Math.PI*2/7;const berry=new THREE.Mesh(new THREE.SphereGeometry(.105,12,10),strawberry);berry.position.set(-.91+Math.cos(a)*.28,-.68+Math.sin(a)*.28,.76);object.add(berry)}
const chefHat=new THREE.Group();chefHat.position.set(0,1.12,.33);object.add(chefHat);
const hatBase=new THREE.Mesh(new THREE.CylinderGeometry(.36,.36,.24,40),cream);hatBase.rotation.x=Math.PI/2;chefHat.add(hatBase);
for(const [x,y,r] of [[-.23,.18,.27],[0,.26,.33],[.25,.16,.26]]){const puff=new THREE.Mesh(new THREE.SphereGeometry(r,20,14),cream);puff.position.set(x,y,.12);chefHat.add(puff)}
const pastryBag=new THREE.Mesh(new THREE.ConeGeometry(.27,.73,32),pinkGloss);pastryBag.rotation.z=-.48;pastryBag.position.set(1.28,.65,.37);object.add(pastryBag);
const pipingTip=new THREE.Mesh(new THREE.ConeGeometry(.095,.23,24),gold);pipingTip.rotation.z=Math.PI-.48;pipingTip.position.set(1.5,.3,.38);object.add(pipingTip);
const sweet=new THREE.Mesh(new THREE.SphereGeometry(.24,24,18),strawberry);sweet.position.set(1.06,-1.02,.42);object.add(sweet);
const bonbon=new THREE.Mesh(new THREE.SphereGeometry(.19,24,18),pinkGloss);bonbon.scale.y=.72;bonbon.position.set(1.43,-1.06,.38);object.add(bonbon);
const rearCanvas=document.createElement('canvas');rearCanvas.width=512;rearCanvas.height=512;const ctx=rearCanvas.getContext('2d');ctx.fillStyle='#f8dce2';ctx.fillRect(0,0,512,512);ctx.fillStyle='#ad3970';ctx.textAlign='center';ctx.font='bold 70px Georgia';ctx.fillText('Chef Lú',256,255);ctx.font='22px sans-serif';ctx.fillText('BOLOS E DOCES GOURMET',256,303);const rearTex=new THREE.CanvasTexture(rearCanvas);rearTex.colorSpace=THREE.SRGBColorSpace;back.material.map=rearTex;back.material.needsUpdate=true;
let dragging=false,previous=null,auto=false;const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function pointerDown(e){dragging=true;previous={x:e.clientX,y:e.clientY};stage.setPointerCapture(e.pointerId)}function pointerMove(e){if(!dragging||!previous)return;object.rotation.y+=(e.clientX-previous.x)*.009;object.rotation.x+=(e.clientY-previous.y)*.009;previous={x:e.clientX,y:e.clientY}}function pointerUp(){dragging=false;previous=null}stage.addEventListener('pointerdown',pointerDown);stage.addEventListener('pointermove',pointerMove);stage.addEventListener('pointerup',pointerUp);stage.addEventListener('pointercancel',pointerUp);
document.getElementById('reset').addEventListener('click',()=>{object.rotation.set(-.12,-.28,0);auto=false;sync()});document.getElementById('spin').addEventListener('click',()=>{auto=!auto;sync()});function sync(){const b=document.getElementById('spin');b.setAttribute('aria-pressed',String(auto));b.textContent=auto?'Pausar rotação automática':'Ativar rotação automática'}
object.rotation.set(-.12,-.28,0);const resize=()=>{const w=stage.clientWidth,h=stage.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.position.z=w<550?10:7.6;camera.updateProjectionMatrix()};new ResizeObserver(resize).observe(stage);resize();let visible=true;new IntersectionObserver(entries=>{visible=entries[0].isIntersecting}).observe(stage);function animate(){requestAnimationFrame(animate);if(!visible)return;if(auto&&!dragging&&!reduced)object.rotation.y+=.006;renderer.render(scene,camera)}animate();