(()=>{'use strict';
const $=id=>document.getElementById(id),form=$('farm-form'),status=$('form-status');
const examples={padrao:{capacity:160,fixed:100,demand:[60,150,80,140,100,160,70],batches:[{quantity:250,ready:1,expires:3},{quantity:320,ready:3,expires:5},{quantity:260,ready:5,expires:7}]},escassez:{capacity:160,fixed:100,demand:[60,150,80,140,100,160,70],batches:[{quantity:140,ready:1,expires:3},{quantity:130,ready:3,expires:5},{quantity:90,ready:5,expires:7}]},capacidade:{capacity:70,fixed:100,demand:[60,150,80,140,100,160,70],batches:[{quantity:250,ready:1,expires:3},{quantity:320,ready:3,expires:5},{quantity:260,ready:5,expires:7}]}};
let current=null;const fmt=n=>n.toLocaleString('pt-BR');
const pct=(n,total)=>total?(100*n/total).toLocaleString('pt-BR',{maximumFractionDigits:1})+'%':'sem pedidos';
function load(name){const s=examples[name];$('capacity').value=s.capacity;$('fixed').value=s.fixed;s.demand.forEach((v,i)=>$('d'+i).value=v);s.batches.forEach((b,i)=>{ $('q'+i).value=b.quantity;$('r'+i).value=b.ready;$('e'+i).value=b.expires;});form.querySelectorAll('input').forEach(n=>n.setCustomValidity(''));calculate(false);}
function input(){return{capacity:Number($('capacity').value),fixed:Number($('fixed').value),demand:Array.from({length:7},(_,i)=>Number($('d'+i).value)),batches:Array.from({length:3},(_,i)=>({quantity:Number($('q'+i).value),ready:Number($('r'+i).value),expires:Number($('e'+i).value)}))};}
function text(tag,content,className){const e=document.createElement(tag);e.textContent=content;if(className)e.className=className;return e;}
function calculate(focus){
 form.querySelectorAll('input').forEach(n=>n.setCustomValidity(''));
 for(let i=0;i<3;i++)if(Number($('e'+i).value)<Number($('r'+i).value))$('e'+i).setCustomValidity('O dia limite deve ser igual ou posterior ao dia inicial.');
 if(!form.reportValidity()){status.textContent='Revise os campos indicados para calcular.';return;}
 let result,scenario;try{scenario=input();result=ColheitaModelo.compare(scenario);}catch(error){status.textContent=error.message;return;}
 current={scenario,result};const b=result.baseline.totals,p=result.planned.totals;
 $('resultados').hidden=false;$('download').disabled=false;
 for(const [id,value]of Object.entries({'base-delivered':b.delivered,'plan-delivered':p.delivered,'base-loss':b.loss,'plan-loss':p.loss,'base-shortage':b.shortage,'plan-shortage':p.shortage}))$(id).textContent=fmt(value);
 $('coverage').textContent='Atendimento: '+pct(b.delivered,b.demand)+' na rotina fixa; '+pct(p.delivered,p.demand)+' no plano.';
 $('production-total').textContent='Produção disponível: '+fmt(p.production)+' pés. Pedidos: '+fmt(p.demand)+' pés.';
 const delta=p.delivered-b.delivered;
 $('summary').textContent=delta>0?'Neste cenário, o plano atende '+fmt(delta)+' pés a mais em pedidos, usando a mesma produção disponível.':delta<0?'Neste cenário, o plano atende '+fmt(-delta)+' pés a menos que a rotina fixa. Revise as janelas e as hipóteses: a regra não garante melhora em todo cenário.':'Neste cenário, as duas rotinas atendem o mesmo volume de pedidos. Compare também perdas e distribuição por dia.';
 if(!p.demand)$('summary').textContent='Não há pedidos neste cenário. O plano não indica colheita; a produção atinge o dia limite no canteiro.';
 const tbody=$('daily-plan');tbody.replaceChildren();
 for(const d of result.planned.days){const tr=document.createElement('tr');for(const value of ['Dia '+d.day,fmt(d.demand),d.picked.length?d.picked.map(x=>x.batch+': '+fmt(x.quantity)).join(' · '):'Não colher',fmt(d.delivered),fmt(d.shortage),fmt(d.loss)])tr.append(text('td',value));tbody.append(tr);}
 const chart=$('chart');chart.replaceChildren();const max=Math.max(1,...scenario.demand,...result.baseline.days.map(d=>d.delivered),...result.planned.days.map(d=>d.delivered));
 for(let i=0;i<7;i++){const day=text('div','', 'chart-day');day.append(text('h4','Dia '+(i+1)));const bars=text('div','', 'chart-bars');bars.setAttribute('aria-hidden','true');[scenario.demand[i],result.baseline.days[i].delivered,result.planned.days[i].delivered].forEach((n,k)=>{const bar=text('div','', 'bar '+['key-demand','key-base','key-plan'][k]);bar.style.height=(100*n/max)+'%';bars.append(bar);});day.append(bars,text('p',fmt(result.planned.days[i].delivered)+' / '+fmt(scenario.demand[i])));day.setAttribute('aria-label','Dia '+(i+1)+': pedidos '+scenario.demand[i]+', rotina fixa '+result.baseline.days[i].delivered+', plano '+result.planned.days[i].delivered);chart.append(day);}
 const alerts=$('alerts');alerts.replaceChildren();
 if(p.shortage)alerts.append(text('p','Atenção: '+fmt(p.shortage)+' pés de pedidos ficam sem atendimento. Confira os dias na tabela; o limite pode ser disponibilidade, janela de colheita ou capacidade.'));
 if(p.expired)alerts.append(text('p',fmt(p.expired)+' pés atingem o dia limite no canteiro. Avalie pedidos adicionais ou ajuste do calendário em uma análise real. O modelo não sugere antecipar plantios ou alterar maturação.'));
 if(!p.production)alerts.append(text('p','Sem produção disponível: não há colheita nem entregas sugeridas.'));
 if(scenario.fixed>scenario.capacity)alerts.append(text('p','A meta da rotina fixa supera a capacidade diária. As duas rotinas respeitam o limite de '+fmt(scenario.capacity)+' pés por dia.'));
 status.textContent='Cenário calculado. Resultados fictícios para os valores informados.';
 if(focus)$('results-title').focus();
}
form.addEventListener('submit',e=>{e.preventDefault();calculate(true);});
form.addEventListener('input',()=>{current=null;$('download').disabled=true;form.querySelectorAll('input').forEach(n=>n.setCustomValidity(''));status.textContent='Dados alterados. Clique em “Comparar e gerar plano” para atualizar.';if(!$('resultados').hidden){$('resultados').hidden=true;}});
$('cenario').addEventListener('change',()=>load($('cenario').value));$('reset').addEventListener('click',()=>{$('cenario').value='padrao';load('padrao');});
$('download').addEventListener('click',()=>{if(!current)return;const {scenario,result}=current;const rows=[['DEMONSTRACAO FICTICIA - NAO E PREVISAO AGRONOMICA'],['Capacidade diaria',scenario.capacity,'Meta fixa diaria',scenario.fixed],['Canteiro','Quantidade','Dia inicial','Dia limite'],...scenario.batches.map((b,i)=>[String.fromCharCode(65+i),b.quantity,b.ready,b.expires]),[],['Dia','Pedidos','Colher A','Colher B','Colher C','Atendidos plano','Atendidos rotina fixa','Faltam plano','Perda excedente plano','Perda canteiro plano']];for(const d of result.planned.days)rows.push([d.day,d.demand,...['A','B','C'].map(id=>d.picked.find(x=>x.batch===id)?.quantity||0),d.delivered,result.baseline.days[d.day-1].delivered,d.shortage,d.excess,d.expired]);rows.push([],['Hipoteses','Sem armazenamento apos colheita; pedidos nao passam ao dia seguinte; saldo vence no fim do dia limite.']);const content='\uFEFF'+rows.map(row=>row.map(v=>'"'+String(v).replaceAll('"','""')+'"').join(';')).join('\r\n');const url=URL.createObjectURL(new Blob([content],{type:'text/csv;charset=utf-8;'})),link=document.createElement('a');link.href=url;link.download='kaggriculture-plano-ficticio.csv';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);});
load('padrao');
})();
