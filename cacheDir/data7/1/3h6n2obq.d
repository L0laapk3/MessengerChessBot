   �      ;https://static.xx.fbcdn.net/rsrc.php/v2/yI/r/9rzgtUz6Ued.js %��2�� %i��t          
     O K           �     if (self.CavalryLogger) { CavalryLogger.start_js(["Bid7h"]); }

__d("XConsentCookieController",["XController"],function a(b,c,d,e,f,g){c.__markCompiled&&c.__markCompiled();f.exports=c("XController").create("\/cookie\/consent\/",{pv:{type:"Enum",enumType:0}});},null);
__d('DeferredCookie',['Cookie','Map','MRequest','XConsentCookieController'],function a(b,c,d,e,f,g,h,i,j,k){'use strict';if(c.__markCompiled)c.__markCompiled();var l=new i(),m={shouldAddDefaultListener:true,defaultHandler:null,autoFlushCookies:false,sentConsentToServer:false,addToQueue:function(n,o,p,q,r,s,t){if(this.autoFlushCookies){if(s){h.setIfFirstPartyContext(n,o,p,q,r);}else h.set(n,o,p,q,r);return;}if(l.has(n))return;l.set(n,{name:n,value:o,nMilliSecs:p,path:q,secure:r,firstPartyOnly:s});if(t)this.addDefaultInteractionListener();},flushAllCookies:function(){l.forEach(function(o,p){if(o.firstPartyOnly){h.setIfFirstPartyContext(o.name,o.value,o.nMilliSecs,o.path,o.secure);}else h.set(o.name,o.value,o.nMilliSecs,o.path,o.secure);});this.autoFlushCookies=true;l=new i();if(!this.sentConsentToServer){this.sentConsentToServer=true;var n=k.getURIBuilder().setEnum('pv',this.getNoticePolicyVersion()).getURI();new j(n).send();}this.removeDefaultInteractionListener();},getNoticePolicyVersion:function(){try{var o=document.getElementById('cpn-pv-link');if(!o)return '1';return o.getAttribute('data-pv');}catch(n){return '1';}},removeDefaultInteractionListener:function(){if(this.defaultHandler){if(window.removeEventListener){window.removeEventListener('click',this.defaultHandler,true);}else if(document.detachEvent)document.detachEvent('onclick',this.defaultHandler);this.defaultHandler=null;}},addDefaultInteractionListener:function(){if(this.shouldAddDefaultListener){this.shouldAddDefaultListener=false;this.defaultHandler=this.baseInteractionHandler.bind(this);if(window.addEventListener){window.addEventListener('click',this.defaultHandler,true);}else if(document.attachEvent)document.attachEvent('onclick',this.defaultHandler);}},baseInteractionHandler:function(){this.flushAllCookies();}};f.exports=m;},null);
__d('MCookieUseBannerController',['DeferredCookie','DOM','Parent'],function a(b,c,d,e,f,g,h,i,j){'use strict';if(c.__markCompiled)c.__markCompiled();var k={init:function(l,m){this.banner=l;this.closeButton=m;this.addPageInteractionListeners();if(m){var n=function(){i.remove(l);};if(m.addEventListener){m.addEventListener('click',n);}else if(m.attachEvent)m.attachEvent('onclick',n);}},addPageInteractionListeners:function(){var l=function(m){if(this.targetShouldNotBeConsideredConsent(m.target))return;h.flushAllCookies();if(window.removeEventListener){window.removeEventListener('click',l,true);}else if(document.detachEvent)document.detachEvent('onclick',l);}.bind(this);if(window.addEventListener){window.addEventListener('click',l,true);}else if(document.attachEvent)document.attachEvent('onclick',l);h.removeDefaultInteractionListener();},targetShouldNotBeConsideredConsent:function(l){if(this.closeButton&&(l===this.closeButton||this.closeButton.contains(l)))return false;if(this.banner===l||this.banner.contains(l))return true;var m=j.byAttribute(l,'data-nocookies');if(m)return true;if(l.tagName.toLowerCase()!=='a')l=j.byTag(l,'a');if(l&&l.href&&l.href.indexOf('/help/cookies')>-1)return true;return false;}};f.exports=k;},null);
__d('MVideoUploadingNux',['DOM','Stratcom','MRequest'],function a(b,c,d,e,f,g,h,i,j){if(c.__markCompiled)c.__markCompiled();var k,l;function m(o,p){k=o;l=p;i.listen('click','hide-video-uploading-nux',function(q){n();});}function n(){h.remove(k);new j(l.dismiss_uri).send();}f.exports={init:m};},null);