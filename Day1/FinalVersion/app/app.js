'use strict';
const $ = id => document.getElementById(id);
let page = 1, currentRole = null, requestToken = 0;
const filters = ['search','team','location','workplace','remote','sort'];
const elt = (tag, cls, txt) => {const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e;};
function chip(s, variant=''){const e=elt('span','chip '+variant,s);return e;}
async function loadStats(){
  const r=await fetch('/api/stats');if(!r.ok)throw new Error('Could not read database statistics');
  const data=await r.json();$('total').textContent=data.total.toLocaleString();$('types').textContent=data.workplace.length;
  for(const name of data.teams){const option=elt('option','',name);option.value=name;$('team').append(option);}
  for(const obj of data.workplace){if(obj.label==='Unknown')continue;const option=elt('option','',obj.label+' ('+obj.count+')');option.value=obj.label;$('workplace').append(option);}
}
function createRole(role){
  const card=elt('article','role');const left=elt('div');
  left.append(elt('h3','',role.title));
  left.append(elt('div','info',[role.team||'Team unknown',role.location||'Location unlisted'].join(' · ')));
  const chips=elt('div','chips');chips.append(chip(role.workplace_type||'Work arrangement unknown','work'));
  if(role.is_remote===1)chips.append(chip('is_remote: true'));
  if(role.published_at)chips.append(chip('Published: '+role.published_at.slice(0,10)));
  left.append(chips);card.append(left);
  const button=elt('button','view','Inspect role →');button.type='button';button.addEventListener('click',()=>inspect(role.id));card.append(button);
  return card;
}
async function loadRoles(){
  const thisToken=++requestToken;
  const params=new URLSearchParams({q:$('search').value,team:$('team').value,location:$('location').value,
    workplace:$('workplace').value,remote:$('remote').value,sort:$('sort').value,page:String(page)});
  const r=await fetch('/api/roles?'+params.toString());if(!r.ok)throw Error('Role query failed');
  const data=await r.json();if(thisToken!==requestToken)return;
  $('results-info').textContent=data.total.toLocaleString()+' matching roles · '+data.page_size+' per page';
  const list=$('role-list');list.replaceChildren();
  if(!data.roles.length)list.append(elt('p','empty','No matching roles. Try resetting your filters.'));
  for(const role of data.roles)list.append(createRole(role));
  const last=Math.max(1,Math.ceil(data.total/data.page_size));
  $('page-info').textContent='Page '+page+' of '+last;
  $('prev').disabled=page<=1;$('next').disabled=page>=last;
}
function setTab(tab){
  if(!currentRole)return;
  for(const name of ['description','provenance','canonical'])$('show-'+name).classList.toggle('selected',name===tab);
  const value=tab==='description'?(currentRole.description_plain||'No plain-text description provided'):
    tab==='provenance'?currentRole.provenance_json:currentRole.canonical_json;
  $('detail-text').textContent=typeof value==='string'?value:JSON.stringify(value,null,2);
}
function validLink(href){try{const u=new URL(href);return ['https:','http:'].includes(u.protocol)?u.href:null;}catch{return null;}}
async function inspect(id){
  const r=await fetch('/api/roles/'+encodeURIComponent(id));if(!r.ok)throw Error('Cannot load role');
  currentRole=await r.json();$('detail-title').textContent=currentRole.title;
  $('detail-meta').textContent=[currentRole.team,currentRole.location,currentRole.workplace_type,
    'Job ID: '+currentRole.id].filter(Boolean).join(' · ');
  const source=validLink(currentRole.job_url),apply=validLink(currentRole.apply_url);
  if(source)$('source-link').href=source;else $('source-link').removeAttribute('href');
  if(apply)$('apply-link').href=apply;else $('apply-link').removeAttribute('href');
  setTab('description');$('detail').showModal();
}
function errorMessage(e){$('results-info').textContent='Unable to load data';$('role-list').replaceChildren(elt('p','empty',String(e.message||e)));}
let debounce;
async function init(){
  try{await loadStats();await loadRoles();}catch(e){errorMessage(e)}
  for(const id of filters){$(id).addEventListener('input',()=>{page=1;clearTimeout(debounce);debounce=setTimeout(()=>loadRoles().catch(errorMessage),id==='search'||id==='location'?200:0);});}
  $('clear').addEventListener('click',()=>{for(const id of filters)$(id).value=id==='sort'?'title':'';page=1;loadRoles().catch(errorMessage);});
  $('prev').addEventListener('click',()=>{page--;loadRoles().catch(errorMessage)});
  $('next').addEventListener('click',()=>{page++;loadRoles().catch(errorMessage)});
  $('close').addEventListener('click',()=>$('detail').close());
  for(const tab of ['description','provenance','canonical'])$('show-'+tab).addEventListener('click',()=>setTab(tab));
}
init();
