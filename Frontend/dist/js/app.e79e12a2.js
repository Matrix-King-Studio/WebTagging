(function(e){function n(n){for(var a,o,u=n[0],l=n[1],i=n[2],c=0,f=[];c<u.length;c++)o=u[c],Object.prototype.hasOwnProperty.call(r,o)&&r[o]&&f.push(r[o][0]),r[o]=0;for(a in l)Object.prototype.hasOwnProperty.call(l,a)&&(e[a]=l[a]);d&&d(n);while(f.length)f.shift()();return s.push.apply(s,i||[]),t()}function t(){for(var e,n=0;n<s.length;n++){for(var t=s[n],a=!0,o=1;o<t.length;o++){var u=t[o];0!==r[u]&&(a=!1)}a&&(s.splice(n--,1),e=l(l.s=t[0]))}return e}var a={},o={app:0},r={app:0},s=[];function u(e){return l.p+"js/"+({"home~workBench":"home~workBench",home:"home",workBench:"workBench",loginPage:"loginPage"}[e]||e)+"."+{"chunk-2bc476de":"7c1333a6","home~workBench":"5ecda8d4",home:"dd90408a",workBench:"918277d4",loginPage:"6150eed4"}[e]+".js"}function l(n){if(a[n])return a[n].exports;var t=a[n]={i:n,l:!1,exports:{}};return e[n].call(t.exports,t,t.exports,l),t.l=!0,t.exports}l.e=function(e){var n=[],t={home:1,workBench:1,loginPage:1};o[e]?n.push(o[e]):0!==o[e]&&t[e]&&n.push(o[e]=new Promise((function(n,t){for(var a="css/"+({"home~workBench":"home~workBench",home:"home",workBench:"workBench",loginPage:"loginPage"}[e]||e)+"."+{"chunk-2bc476de":"31d6cfe0","home~workBench":"31d6cfe0",home:"551d83e7",workBench:"db0d2788",loginPage:"c5d27a19"}[e]+".css",r=l.p+a,s=document.getElementsByTagName("link"),u=0;u<s.length;u++){var i=s[u],c=i.getAttribute("data-href")||i.getAttribute("href");if("stylesheet"===i.rel&&(c===a||c===r))return n()}var f=document.getElementsByTagName("style");for(u=0;u<f.length;u++){i=f[u],c=i.getAttribute("data-href");if(c===a||c===r)return n()}var d=document.createElement("link");d.rel="stylesheet",d.type="text/css",d.onload=n,d.onerror=function(n){var a=n&&n.target&&n.target.src||r,s=new Error("Loading CSS chunk "+e+" failed.\n("+a+")");s.code="CSS_CHUNK_LOAD_FAILED",s.request=a,delete o[e],d.parentNode.removeChild(d),t(s)},d.href=r;var h=document.getElementsByTagName("head")[0];h.appendChild(d)})).then((function(){o[e]=0})));var a=r[e];if(0!==a)if(a)n.push(a[2]);else{var s=new Promise((function(n,t){a=r[e]=[n,t]}));n.push(a[2]=s);var i,c=document.createElement("script");c.charset="utf-8",c.timeout=120,l.nc&&c.setAttribute("nonce",l.nc),c.src=u(e);var f=new Error;i=function(n){c.onerror=c.onload=null,clearTimeout(d);var t=r[e];if(0!==t){if(t){var a=n&&("load"===n.type?"missing":n.type),o=n&&n.target&&n.target.src;f.message="Loading chunk "+e+" failed.\n("+a+": "+o+")",f.name="ChunkLoadError",f.type=a,f.request=o,t[1](f)}r[e]=void 0}};var d=setTimeout((function(){i({type:"timeout",target:c})}),12e4);c.onerror=c.onload=i,document.head.appendChild(c)}return Promise.all(n)},l.m=e,l.c=a,l.d=function(e,n,t){l.o(e,n)||Object.defineProperty(e,n,{enumerable:!0,get:t})},l.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},l.t=function(e,n){if(1&n&&(e=l(e)),8&n)return e;if(4&n&&"object"===typeof e&&e&&e.__esModule)return e;var t=Object.create(null);if(l.r(t),Object.defineProperty(t,"default",{enumerable:!0,value:e}),2&n&&"string"!=typeof e)for(var a in e)l.d(t,a,function(n){return e[n]}.bind(null,a));return t},l.n=function(e){var n=e&&e.__esModule?function(){return e["default"]}:function(){return e};return l.d(n,"a",n),n},l.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)},l.p="/",l.oe=function(e){throw console.error(e),e};var i=window["webpackJsonp"]=window["webpackJsonp"]||[],c=i.push.bind(i);i.push=n,i=i.slice();for(var f=0;f<i.length;f++)n(i[f]);var d=c;s.push([0,"chunk-vendors"]),t()})({0:function(e,n,t){e.exports=t("56d7")},"56d7":function(e,n,t){"use strict";t.r(n);t("0fae");var a=t("9e2f"),o=t.n(a),r=(t("e260"),t("e6cf"),t("cca6"),t("a79d"),t("2b0e")),s=function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{attrs:{id:"app"}},[t("router-view")],1)},u=[],l={},i=l,c=t("2877"),f=Object(c["a"])(i,s,u,!1,null,null,null),d=f.exports,h=(t("d3b7"),t("8c4f")),p=function(){return t.e("loginPage").then(t.bind(null,"48ca"))},m=function(){return Promise.all([t.e("home~workBench"),t.e("home")]).then(t.bind(null,"bb51"))},g=function(){return Promise.all([t.e("home~workBench"),t.e("home")]).then(t.bind(null,"2a7d"))},b=function(){return Promise.all([t.e("home~workBench"),t.e("home")]).then(t.bind(null,"eaff"))},v=function(){return t.e("chunk-2bc476de").then(t.bind(null,"15a4"))},w=function(){return Promise.all([t.e("home~workBench"),t.e("home")]).then(t.bind(null,"72bd"))},k=function(){return Promise.all([t.e("home~workBench"),t.e("workBench")]).then(t.bind(null,"94c7"))},y=function(){return Promise.all([t.e("home~workBench"),t.e("workBench")]).then(t.bind(null,"77d8"))},j=function(){return Promise.all([t.e("home~workBench"),t.e("workBench")]).then(t.bind(null,"fcb1"))};r["default"].use(h["a"]);var I=[{path:"/",redirect:"login"},{path:"/login",component:p},{path:"/home",redirect:"/home/project",component:m,children:[{path:"project",component:g},{path:"user",component:b},{path:"logAnalysis",component:v},{path:"newproject",component:w}]},{path:"/workbench",component:k,children:[{path:"task/:index",component:y},{path:"task/:index/job/:jobIndex",component:y},{path:"setting/:index",component:j},{path:"setting/:index/job/:jobIndex",component:j}]}],B=new h["a"]({routes:I});B.beforeEach((function(e,n,t){if("/login"===e.path)return t();var a=window.sessionStorage.getItem("token");if(!a)return t("/login");t()}));var P=B,T=(t("c975"),t("a434"),t("b0c0"),t("b85c")),L=t("2f62");r["default"].use(L["a"]);var _=new L["a"].Store({state:{userInfo:"",jobInfo:{},allJobs:[],userChoiceModel:1,projectInfo:{name:"",describe:"",labels:[],z_order:!1},allFileList:[],allFileList02:[],treeCheckedKeyList:[],image_quality:70,imageTags:{shapes:[],tracks:[],tags:[],version:26},allUsers:[]},mutations:{saveUserInfo:function(e,n){e.userInfo=n},saveIfOwnerToUserInfo:function(e,n){e.userInfo.ifOwner=n},saveJobInfo:function(e,n){e.jobInfo.jobId=n},saveAllJobs:function(e,n){e.allJobs=n},changeUserChoiceModel:function(e,n){e.userChoiceModel=n},addToStore:function(e,n){e.projectInfo.labels=[];for(var t=0;t<n.length;t++){var a={};a.name=n[t].name,a.id=n[t].id,a.attributes=n[t].attributes,e.projectInfo.labels.push(a)}},updateLabels:function(e,n){e.projectInfo.labels=[],e.projectInfo.labels=JSON.parse(n)},addImageQuality:function(e,n){e.image_quality=n},cleanStore:function(){this.state.projectInfo={name:"",describe:"",labels:[],z_order:!1}},cleanFileList:function(){this.state.allFileList=[],this.state.allFileList02=[],this.state.treeCheckedKeyList=[],this.state.userChoiceModel=1,this.state.image_quality=70},saveFileList:function(e,n){e.allFileList=n},saveFileList02:function(e,n){e.allFileList02=n},saveTreeCheckedKeyList:function(e,n){e.treeCheckedKeyList=n},saveTagsInfo:function(e,n){e.imageTags.shapes.push(n)},changeTagInfo:function(e,n){for(var t=0;t<e.imageTags.shapes.length;t++)e.imageTags.shapes[t].id===n.id&&(e.imageTags.shapes[t]=n)},delTagInfo:function(e,n){var t,a=Object(T["a"])(e.imageTags.shapes);try{for(a.s();!(t=a.n()).done;){var o=t.value;o.id===n&&e.imageTags.shapes.splice(e.imageTags.shapes.indexOf(o),1)}}catch(r){a.e(r)}finally{a.f()}},cleanTagsInfo:function(e){e.imageTags={shapes:[],tracks:[],tags:[],version:26}},saveAllUsers:function(e,n){e.allUsers=n,0===e.allUsers.length?delete e.projectInfo.segment_size:e.projectInfo["segment_size"]=e.allUsers.length},saveSeg:function(e,n){e.projectInfo["segment_size"]=n},cleanUsersInfo:function(e){e.allUsers=[]}},actions:{},modules:{}}),O=(t("aede"),t("a342"),t("bc3a")),x=t.n(O),S=t("6ed5"),C=t.n(S),U=t("f529"),E=t.n(U),A=t("7fc1"),F=t.n(A),M=t("1599"),J=t.n(M),$=t("dcdc"),q=t.n($),z=t("18ff"),N=t.n(z),K=t("defb"),D=t.n(K),H=t("b370"),Q=t.n(H),R=t("dd3d"),G=t.n(R),V=t("101e"),W=t.n(V),X=t("299c"),Y=t.n(X),Z=t("486c"),ee=t.n(Z),ne=t("e772"),te=t.n(ne),ae=t("4e4b"),oe=t.n(ae),re=t("20cf"),se=t.n(re),ue=t("f3ad"),le=t.n(ue),ie=t("8bbc"),ce=t.n(ie),fe=t("89a9"),de=t.n(fe),he=t("3803"),pe=t.n(he),me=t("4cb2"),ge=t.n(me),be=t("f58e"),ve=t.n(be),we=t("443e"),ke=t.n(we),ye=t("72aa"),je=t.n(ye),Ie=t("dd87"),Be=t.n(Ie),Pe=t("c216"),Te=t.n(Pe),Le=t("76b9"),_e=t.n(Le),Oe=t("c2cc"),xe=t.n(Oe),Se=t("0f6c"),Ce=t.n(Se),Ue=t("c69e"),Ee=t.n(Ue),Ae=t("5cc3"),Fe=t.n(Ae),Me=t("7b31"),Je=t.n(Me),$e=t("b35b"),qe=t.n($e),ze=t("3d2d"),Ne=t.n(ze),Ke=t("eedf"),De=t.n(Ke);r["default"].use(De.a),r["default"].use(Ne.a),r["default"].use(qe.a),r["default"].use(Je.a),r["default"].use(Fe.a),r["default"].use(Ee.a),r["default"].use(Ce.a),r["default"].use(xe.a),r["default"].use(_e.a),r["default"].use(Te.a),r["default"].use(Be.a),r["default"].use(je.a),r["default"].use(ke.a),r["default"].use(ve.a),r["default"].use(ge.a),r["default"].use(pe.a),r["default"].use(de.a),r["default"].use(ce.a),r["default"].use(le.a),r["default"].use(se.a),r["default"].use(oe.a),r["default"].use(te.a),r["default"].use(ee.a),r["default"].use(Y.a),r["default"].use(W.a),r["default"].use(G.a),r["default"].use(Q.a),r["default"].use(D.a),r["default"].use(N.a),r["default"].use(q.a),r["default"].use(J.a),r["default"].use(F.a),r["default"].prototype.$message=E.a,r["default"].prototype.$msgbox=C.a,r["default"].prototype.$alert=C.a.alert,r["default"].prototype.$confirm=C.a.confirm,r["default"].prototype.$prompt=C.a.prompt,r["default"].use(o.a),x.a.defaults.baseURL="http://alexking.site:8080/api/",x.a.interceptors.request.use((function(e){return window.sessionStorage.getItem("token")&&(e.headers.Authorization="Token "+window.sessionStorage.getItem("token")),e})),r["default"].prototype.$http=x.a,r["default"].config.productionTip=!1,new r["default"]({el:"#app",router:P,store:_,render:function(e){return e(d)}})},a342:function(e,n,t){},aede:function(e,n,t){}});
//# sourceMappingURL=app.e79e12a2.js.map