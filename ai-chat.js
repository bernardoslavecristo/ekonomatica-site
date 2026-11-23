/* Ekonomática AI — interface conversacional generativa OpenAI via backend próprio. */
(()=>{
'use strict';
const root=document.getElementById('eko-chat-box');
if(!root)return;
const es=document.documentElement.lang.toLowerCase().startsWith('es');
const t=es?{
title:'Ekonomática AI · Asistente virtual',intro:'Soy un asistente de inteligencia artificial. Cuénteme qué necesita automatizar.',
placeholder:'Escriba su pregunta...',send:'Enviar pregunta',working:'Pensando...',unavailable:'El asistente no está disponible ahora. Puede dejar su solicitud en el formulario de abajo.',error:'No fue posible responder. Intente nuevamente o deje su solicitud.',welcome:'Hola. Puedo ayudarle a entender soluciones de IA, automatización e integración de sistemas. ¿Qué desafío tiene su empresa?',form:'Dejar datos de contacto',note:'Asistente de IA. Sus respuestas pueden contener errores. No comparta datos sensibles ni contraseñas.',limit:'La conversación alcanzó el límite por sesión. Puede dejar su mensaje en el formulario.'}
:{
title:'Ekonomática AI · Consultor virtual',intro:'Sou um assistente de inteligência artificial. Conte o que você precisa automatizar.',
placeholder:'Escreva sua pergunta...',send:'Enviar pergunta',working:'Pensando...',unavailable:'O assistente ainda não está disponível. Você pode deixar sua solicitação no formulário abaixo.',error:'Não foi possível responder agora. Tente novamente ou deixe sua solicitação.',welcome:'Olá! Posso ajudar você a entender soluções de IA, automação e integração de sistemas. Qual desafio sua empresa enfrenta?',form:'Deixar meus dados de contato',note:'Assistente de IA: respostas podem conter erros. Não compartilhe dados sensíveis nem senhas.',limit:'Você atingiu o limite desta conversa. Pode deixar sua mensagem no formulário.'};
const style=document.createElement('style');style.textContent=`
#eko-chat-box .eko-ai-history{display:flex;flex-direction:column;gap:10px;max-height:245px;overflow-y:auto;background:#091729;border:1px solid #284b5d;border-radius:14px;padding:12px;margin:10px 0 12px;scroll-behavior:smooth}
#eko-chat-box .eko-ai-item{padding:11px 12px;border-radius:13px;max-width:94%;font:14px/1.55 system-ui,sans-serif;white-space:pre-wrap;overflow-wrap:anywhere}
#eko-chat-box .eko-ai-assistant{background:#17324a;color:#edf9ff;align-self:flex-start;border:1px solid #2b5969}
#eko-chat-box .eko-ai-user{background:#1b615f;color:#f4fffc;align-self:flex-end}
#eko-chat-box .eko-ai-send{display:flex;gap:8px;align-items:stretch}
#eko-chat-box .eko-ai-send input{flex:1;min-width:0;margin:0;border-radius:11px}
#eko-chat-box .eko-ai-send button{border:0;border-radius:11px;background:#71ead6;color:#082b31;font-weight:800;padding:11px;cursor:pointer}
#eko-chat-box .eko-ai-send button:disabled{opacity:.55;cursor:wait}
#eko-chat-box .eko-ai-note{font-size:11px;color:#aac4d0;margin-top:9px}
#eko-chat-box .eko-ai-lead-toggle{display:block;border:1px solid #4e7984;background:#153145;color:#baf8ed;border-radius:11px;padding:10px 14px;margin:12px 0;width:100%;cursor:pointer;font-weight:700}
#eko-chat-box .eko-bubble,#eko-chat-box .eko-choices{display:none}
#eko-chat-box #eko-contact-form[hidden]{display:none!important}
`;document.head.appendChild(style);
const el=(tag,attrs={},txt)=>{const n=document.createElement(tag);for(const [k,v]of Object.entries(attrs))n.setAttribute(k,v);if(txt!==undefined)n.textContent=txt;return n};
const head=root.querySelector('h2');if(head)head.textContent=t.title;
const intro=root.querySelector('.eko-top+p');if(intro)intro.textContent=t.intro;
const historyView=el('div',{'class':'eko-ai-history','role':'log','aria-live':'polite','aria-label':t.title});
const first=root.querySelector('.eko-bubble');if(first)first.before(historyView);else root.append(historyView);
const sendRow=el('form',{'class':'eko-ai-send'}),input=el('input',{type:'text',maxlength:'1200',required:'','aria-label':t.placeholder,placeholder:t.placeholder,autocomplete:'off'}),send=el('button',{type:'submit'},t.send);
sendRow.append(input,send);historyView.after(sendRow);
const note=el('div',{'class':'eko-ai-note'},t.note);sendRow.after(note);
const leadForm=root.querySelector('#eko-contact-form');
const toggle=el('button',{'class':'eko-ai-lead-toggle',type:'button','aria-expanded':'false'},t.form);
note.after(toggle);
// O visitante pode abrir o formulário diretamente após receber a orientação da IA.
root.addEventListener('click',e=>{if(e.target.closest('.eko-ai-open-contact')){leadForm.hidden=false;toggle.setAttribute('aria-expanded','true');leadForm.querySelector('input')?.focus()}});
if(leadForm){leadForm.hidden=true;toggle.addEventListener('click',()=>{leadForm.hidden=!leadForm.hidden;toggle.setAttribute('aria-expanded',String(!leadForm.hidden));if(!leadForm.hidden)leadForm.querySelector('input')?.focus()})}
function bubble(role,content){const b=el('div',{'class':'eko-ai-item '+(role==='user'?'eko-ai-user':'eko-ai-assistant')},content);historyView.append(b);historyView.scrollTop=historyView.scrollHeight;return b}
function offerContact(){if(!leadForm)return;const btn=el('button',{type:'button','class':'eko-ai-lead-toggle eko-ai-open-contact'},t.form);historyView.append(btn);historyView.scrollTop=historyView.scrollHeight;}
bubble('assistant',t.welcome);
let sessionId;
try{const array=new Uint8Array(24);crypto.getRandomValues(array);sessionId=Array.from(array,x=>x.toString(16).padStart(2,'0')).join('')}catch{sessionId='session-'+Date.now().toString(36)+'-fallback'}
const transcript=[];let count=0,pending=false;
sendRow.addEventListener('submit',async e=>{
e.preventDefault();if(pending)return;
const message=input.value.trim();if(message.length<2)return;
if(count>=12){bubble('assistant',t.limit);return}
const context=transcript.slice(-8);input.value='';bubble('user',message);const placeholder=bubble('assistant',t.working);pending=true;send.disabled=true;
try{
const controller=new AbortController();const tm=setTimeout(()=>controller.abort(),27000);
let response;try{response=await fetch('/api/ai/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message,history:context,session_id:sessionId,language:es?'es':'pt'}),signal:controller.signal})}finally{clearTimeout(tm)}
if(!response.ok){let msg=t.error;if(response.status===503)msg=t.unavailable;if(response.status===429)msg=t.limit;throw new Error(msg)}
const body=await response.json();if(typeof body.reply!=='string'||!body.reply.trim())throw new Error(t.error);
placeholder.textContent=body.reply;transcript.push({role:'user',content:message},{role:'assistant',content:body.reply});count++;
if(/(contato|formulário|formulario|proposta|orçamento|orcamento|contacto|formulario|presupuesto)/i.test(message+' '+body.reply))offerContact();
}catch(err){placeholder.textContent=err.message||t.error}
finally{pending=false;send.disabled=false;historyView.scrollTop=historyView.scrollHeight;input.focus()}
});
})();
