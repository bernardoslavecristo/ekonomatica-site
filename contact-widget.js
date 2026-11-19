/* Ekonomática — caixa de mensagens comerciais. Não simula atendimento humano em tempo real. */
(()=>{
const lang=document.documentElement.lang.toLowerCase().startsWith('es')?'es':'pt';
const t=lang==='es'?{
open:'Hablar con Ekonomática',title:'Contactar Ekonomática',intro:'Cuéntenos qué necesita. Su mensaje se guardará de forma segura y responderemos por el canal indicado.',name:'Su nombre',reply:'Correo o usuario de Telegram (@usuario)',topic:'Servicio',message:'¿Qué necesita automatizar o mejorar?',send:'Enviar mensaje',sending:'Enviando...',consent:'Acepto que Ekonomática utilice estos datos para responder a mi solicitud.',note:'No es un chat en vivo. No comparta contraseñas ni datos sensibles. Política de privacidad: ekonomatica.com.br/privacidade.html',success:'Mensaje recibido. Responderemos por el canal indicado.',error:'No fue posible enviar. Intente nuevamente.',validation:'Informe un correo válido o un usuario de Telegram (@usuario).',close:'Cerrar',options:['Automatización e integraciones','Agentes de IA','Datos y análisis económico','Otra consulta']
}:{
open:'Falar com a Ekonomática',title:'Contato direto',intro:'Conte o que sua empresa precisa. Sua mensagem ficará registrada e responderemos pelo canal informado.',name:'Seu nome',reply:'E-mail ou usuário do Telegram (@usuario)',topic:'Assunto',message:'O que você gostaria de automatizar ou melhorar?',send:'Enviar mensagem',sending:'Enviando...',consent:'Autorizo a Ekonomática a usar estes dados para responder à minha solicitação.',note:'Não é um chat ao vivo. Não compartilhe senhas nem dados sensíveis. Política de privacidade: ekonomatica.com.br/privacidade.html',success:'Mensagem recebida! Responderemos pelo contato informado.',error:'Não foi possível enviar. Tente novamente.',validation:'Informe um e-mail válido ou usuário do Telegram (@usuario).',close:'Fechar',options:['Automação e integrações','Agentes de IA','Dados e análise econômica','Outro assunto']
};
const style=document.createElement('style');style.textContent=`
#eko-chat-toggle{position:fixed;bottom:20px;right:18px;z-index:9997;border:1px solid #4fe2ce;background:linear-gradient(140deg,#127f80,#0e354a);color:#fff;padding:14px 19px;border-radius:99px;font:700 14px system-ui,sans-serif;box-shadow:0 10px 35px #0009;cursor:pointer}
#eko-chat-box{box-sizing:border-box;position:fixed;z-index:9998;bottom:82px;right:18px;width:min(390px,calc(100vw - 36px));max-height:min(690px,calc(100dvh - 104px));overflow:auto;color:#f3f9ff;background:#0c182a;border:1px solid #315c69;border-radius:20px;box-shadow:0 25px 85px #000c;font:15px/1.5 system-ui,sans-serif;padding:20px}
#eko-chat-box[hidden]{display:none!important}#eko-chat-box *{box-sizing:border-box}
#eko-chat-box h2{font:700 21px system-ui,sans-serif;margin:0;color:#fff}#eko-chat-box p{color:#c2d5dc;margin:8px 0 16px}
#eko-chat-box label{display:block;color:#d5eaf0;font-size:13px;margin:11px 0 5px}
#eko-chat-box input,#eko-chat-box select,#eko-chat-box textarea{width:100%;border:1px solid #365b6b;background:#12283d;color:#fff;border-radius:9px;padding:11px;font:15px system-ui,sans-serif}
#eko-chat-box textarea{min-height:105px;resize:vertical}
#eko-chat-box .eko-top{display:flex;justify-content:space-between;gap:10px;align-items:center}
#eko-chat-box .eko-close{background:transparent;border:0;color:#fff;cursor:pointer;font-size:23px}
#eko-chat-box .eko-submit{width:100%;margin-top:13px;padding:12px;border:0;border-radius:10px;background:#71ead6;color:#07212e;font-weight:800;cursor:pointer}
#eko-chat-box .eko-submit:disabled{opacity:.6;cursor:wait}
#eko-chat-box .eko-consent{display:flex;align-items:flex-start;gap:9px;font-size:12px;color:#d3e7e9;line-height:1.4}
#eko-chat-box .eko-consent input{width:auto;margin:3px 0 0}
#eko-chat-box .eko-note{font-size:12px;color:#a8c1c8}
#eko-chat-box .eko-result{min-height:1.2em;color:#80efd4;font-weight:600;margin-top:12px}
@media(max-width:480px){#eko-chat-toggle{bottom:15px;right:13px}#eko-chat-box{right:10px;bottom:76px;width:calc(100vw - 20px)}}
@media(prefers-reduced-motion:reduce){#eko-chat-box{scroll-behavior:auto}}
`;document.head.appendChild(style);
const el=(tag,attrs={},txt)=>{const n=document.createElement(tag);for(const [k,v] of Object.entries(attrs)){if(k==='className')n.className=v;else n.setAttribute(k,v)}if(txt!==undefined)n.textContent=txt;return n};
const toggle=el('button',{type:'button',id:'eko-chat-toggle','aria-expanded':'false','aria-controls':'eko-chat-box'},'✦ '+t.open);
const box=el('section',{id:'eko-chat-box',hidden:'','aria-label':t.title});
const head=el('div',{className:'eko-top'}),title=el('h2',{},t.title),close=el('button',{type:'button',className:'eko-close','aria-label':t.close},'×');head.append(title,close);
box.append(head,el('p',{},t.intro));
const form=el('form',{id:'eko-contact-form'});
const field=(label,node)=>{form.append(el('label',{for:node.id},label),node);return node};
const name=field(t.name,el('input',{id:'eko-contact-name',name:'nome',maxlength:'100',required:'',autocomplete:'name'}));
const reply=field(t.reply,el('input',{id:'eko-contact-reply',name:'contato',maxlength:'160',required:'',autocomplete:'email'}));
const select=el('select',{id:'eko-contact-topic',name:'assunto',required:''});for(const v of t.options)select.append(el('option',{value:v},v));field(t.topic,select);
const message=field(t.message,el('textarea',{id:'eko-contact-msg',name:'mensagem',maxlength:'2000',minlength:'10',required:''}));
const trap=el('input',{type:'text',name:'website',tabindex:'-1',autocomplete:'off','aria-hidden':'true'});trap.style.cssText='position:absolute;left:-9999px;opacity:0';form.append(trap);
const consentLabel=el('label',{className:'eko-consent'}),consent=el('input',{type:'checkbox',required:'',name:'consentimento'});consentLabel.append(consent,el('span',{},t.consent));form.append(consentLabel);
form.append(el('div',{className:'eko-note'},t.note));
const submit=el('button',{className:'eko-submit',type:'submit'},t.send),result=el('div',{className:'eko-result',role:'status','aria-live':'polite'});form.append(submit,result);box.append(form);
document.body.append(toggle,box);
function opened(on){box.hidden=!on;toggle.setAttribute('aria-expanded',String(on));if(on)name.focus();else toggle.focus()}
toggle.addEventListener('click',()=>opened(box.hidden));close.addEventListener('click',()=>opened(false));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!box.hidden)opened(false)});
form.addEventListener('submit',async e=>{e.preventDefault();result.textContent='';const contact=reply.value.trim();if(!(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact)||/^@[a-zA-Z0-9_]{5,32}$/.test(contact))){result.textContent=t.validation;reply.focus();return}
submit.disabled=true;submit.textContent=t.sending;
try{const response=await fetch('/api/contato',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome:name.value.trim(),contato:contact,assunto:select.value,mensagem:message.value.trim(),consentimento:consent.checked,website:trap.value,idioma:lang})});if(!response.ok)throw new Error('HTTP '+response.status);result.textContent=t.success;form.reset()}catch{result.textContent=t.error}finally{submit.disabled=false;submit.textContent=t.send}});
})();
