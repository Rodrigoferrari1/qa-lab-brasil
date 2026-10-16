/* 3.4.0 mobile route focus: never change desktop layout or existing navigation. */
(function(){
  'use strict';
  if(!window.matchMedia)return;
  let seq=0;
  const mobile=()=>window.matchMedia('(max-width:820px)').matches;
  function focus(path){
    if(!mobile())return;
    const token=++seq;
    const targetPath=path||location.pathname;
    const align=()=>{
      if(token!==seq || !mobile() || location.pathname!==targetPath)return;
      const main=document.getElementById('main');
      if(!main)return;
      const target=main.querySelector('.qag-root .topic-head, .topic-head');
      if(!target)return;
      const y=Math.max(0,window.scrollY+target.getBoundingClientRect().top-8);
      window.scrollTo({top:y,behavior:'instant'});
    };
    requestAnimationFrame(()=>requestAnimationFrame(align));
    [100,280,550,850].forEach(ms=>setTimeout(align,ms));
  }
  const oldNavigate=window.qaNavigate;
  if(typeof oldNavigate==='function')window.qaNavigate=function(){
    const result=oldNavigate.apply(this,arguments);
    const key=String(arguments[0]||'');
    if(key && key!=='home' && key!=='/')focus(location.pathname);
    return result;
  };
  const oldGames=window.qagNavigate;
  if(typeof oldGames==='function')window.qagNavigate=function(){
    const result=oldGames.apply(this,arguments);
    focus(location.pathname);
    return result;
  };
  // MOB-003: the application also navigates through internal handlers that do
  // not call window.qaNavigate. Align only on an actual route change, never on
  // filter changes, puzzle moves, or ordinary scrolling.
  let lastRoute=location.pathname;
  const scheduleRouteFocus=()=>{
    const next=location.pathname;
    if(next===lastRoute)return;
    lastRoute=next;
    if(next!=='/' && next!=='/index.html')focus(next);
  };
  ['pushState','replaceState'].forEach(method=>{
    const original=history[method];
    history[method]=function(){
      const result=original.apply(this,arguments);
      scheduleRouteFocus();
      return result;
    };
  });
  document.addEventListener('click',event=>{
    if(!mobile())return;
    const link=event.target.closest('a[href]');
    if(!link || link.origin!==location.origin)return;
    setTimeout(scheduleRouteFocus,0);
  },true);
  window.addEventListener('popstate',()=>focus(location.pathname));
  if(location.pathname!=='/' && location.pathname!=='/index.html')window.addEventListener('load',()=>focus(location.pathname),{once:true});
})();
