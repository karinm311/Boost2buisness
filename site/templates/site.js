(function(){
  var root=document.documentElement, motion=root.classList.contains('js');
  var RM=false; try{RM=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
  var $=function(s,c){return (c||document).querySelector(s)}, $$=function(s,c){return [].slice.call((c||document).querySelectorAll(s))};
  var nis=function(n){return '₪'+Math.round(n).toLocaleString('en-US')};

  // measurement hook: reports which button was used once GA4 / GTM / Clarity is installed
  $$('[data-cta]').forEach(function(a){a.addEventListener('click',function(){
    var where=a.getAttribute('data-cta'), name=where==='phone'?'phone_click':'whatsapp_click';
    try{ if(window.gtag) gtag('event',name,{cta_location:where});
         if(window.dataLayer) dataLayer.push({event:name,cta_location:where});
         if(window.clarity) clarity('event',name+'_'+where); }catch(e){}
  })});

  // copy phone
  var cb=$('#copyBtn');
  if(cb){cb.addEventListener('click',function(){
    function done(){var st=$('#copyMsg');if(st)st.textContent='המספר הועתק';cb.textContent='הועתק ✓';setTimeout(function(){cb.textContent='העתקה'},1800)}
    function fallback(){try{var r=document.createRange();r.selectNodeContents($('#phone'));var s=getSelection();s.removeAllRanges();s.addRange(r);cb.textContent='סימנתי'}catch(e){}}
    try{navigator.clipboard.writeText(cb.getAttribute('data-copy')).then(done,fallback)}catch(e){fallback()}
  })}

  // mobile action bar: hidden while the hero CTA or the final CTA is on screen
  var bar=$('#bar'), heroCta=$('[data-cta="hero"]'), fin=$('#final-cta');
  if(bar){
    if('IntersectionObserver' in window&&heroCta){
      var heroVis=true, finVis=false;
      var upd=function(){bar.classList.toggle('off',heroVis||finVis)};
      new IntersectionObserver(function(e){heroVis=e[0].isIntersecting&&e[0].intersectionRatio>=0.85;upd()},{threshold:[0,0.85,1],rootMargin:'-64px 0px 0px 0px'}).observe(heroCta);
      if(fin) new IntersectionObserver(function(e){finVis=e[0].isIntersecting;upd()},{threshold:0}).observe(fin);
    } else bar.classList.remove('off');
  }

  // reveal on scroll (content is visible without JS; CSS has a 4s failsafe)
  $$('.rv').forEach(function(el){
    var sib=[].filter.call(el.parentElement.children,function(c){return c.classList.contains('rv')});
    var i=sib.indexOf(el); if(i>0) el.style.setProperty('--d',(Math.min(i,5)*0.08)+'s');
  });
  if(motion){
    root.classList.add('ready');
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:0,rootMargin:'0px 0px -8% 0px'});
    $$('.rv').forEach(function(el){io.observe(el)});
    var uo=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');uo.unobserve(e.target)}})},{threshold:.6});
    $$('u').forEach(function(el){uo.observe(el)});
    var revealAbove=function(){$$('.rv').forEach(function(el){if(el.getBoundingClientRect().top<innerHeight)el.classList.add('in')})};
    addEventListener('hashchange',function(){setTimeout(revealAbove,60)}); addEventListener('pageshow',revealAbove);
    var rq=0; addEventListener('scroll',function(){if(!rq){rq=requestAnimationFrame(function(){rq=0;revealAbove()})}},{passive:true});
    setTimeout(revealAbove,4000);
    addEventListener('beforeprint',function(){$$('.rv,u').forEach(function(el){el.classList.add('in')})});
  }

  // ---------- calculator ----------
  var calc=$('#calc');
  if(calc){
    var rs=$$('input[type=range]',calc);
    var paint=function(r){var p=(r.value-r.min)/(r.max-r.min)*100;r.style.setProperty('--p',p+'%')};
    var run=function(){
      var hrs=0, rate=150;
      rs.forEach(function(r){paint(r);var o=$('output[for="'+r.id+'"]');
        if(r.id==='rate'){rate=+r.value; if(o) o.textContent=nis(r.value)} else {hrs+=+r.value; if(o) o.textContent=r.value+' ש׳'}});
      var month=hrs*52/12;
      $('#c-hours').textContent=Math.round(month);
      $('#c-money').textContent=nis(month*rate);
    };
    rs.forEach(function(r){r.addEventListener('input',run)}); run();
  }

  // ---------- demos ----------
  function h(tag,cls,html){var e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e}
  function btn(label,cls,fn){var b=h('button','dbtn'+(cls?' '+cls:''),label);b.type='button';b.addEventListener('click',fn);return b}
  function Demo(el){
    this.el=el; this.stage=$('.dstage',el); this.status=$('.dstatus',el); this.steps=$$('.dsteps i',el); this.tok=0;
    var self=this; $('.restart',el).addEventListener('click',function(){self.start()});
    this.status.setAttribute('tabindex','-1');
    this.stage.addEventListener('click',function(ev){if(ev.target.closest('button'))setTimeout(function(){if(!self.stage.contains(document.activeElement)||document.activeElement.disabled)self.status.focus({preventScroll:true})},0)});
  }
  Demo.prototype.wait=function(ms){var self=this,t=this.tok;return new Promise(function(res,rej){setTimeout(function(){t===self.tok?res():rej('stop')},RM?Math.min(ms,80):ms)})};
  Demo.prototype.step=function(n){this.steps.forEach(function(s,i){s.classList.toggle('on',i<n)})};
  Demo.prototype.say=function(t){this.status.textContent=t};
  Demo.prototype.clear=function(){this.stage.innerHTML=''};
  Demo.prototype.start=function(){this.tok++;this.clear();this.step(0);DEMOS[this.el.getAttribute('data-demo')](this)};
  Demo.prototype.ask=function(q,opts){
    var self=this, t=this.tok;
    return new Promise(function(res){
      var box=h('div','ask fadein','<b>'+q+'</b>'), row=h('div','row');
      opts.forEach(function(o,i){row.appendChild(btn(o,i===0?'solid':'',function(){if(t!==self.tok)return;box.remove();res(i)}))});
      box.appendChild(row); self.stage.appendChild(box);
      var f=row.querySelector('button'); if(f&&self.started) f.focus({preventScroll:true});
    });
  };
  function stop(e){if(e!=='stop') throw e}

  var VAT=0.18;
  var DEMOS={
    chani:function(d){
      var seen=[{s:'חשמל לדוגמה בע״מ',dt:'03/10',net:1200},{s:'ניקיון לדוגמה',dt:'01/10',net:300}];
      var invs=[{s:'ציוד משרדי לדוגמה',dt:'15/10',net:850},{s:'חשמל לדוגמה בע״מ',dt:'03/10',net:1200,dup:true},{s:'הדפסות לדוגמה',dt:'18/10',net:500}];
      d.say('בחרו חשבונית לדוגמה ששלחו לחני בוואטסאפ.');
      var pick=h('div','inv-pick');
      invs.forEach(function(v,i){var b=h('button','inv','<small>📎 חשבונית '+(i+1)+' · מוואטסאפ</small><b>'+v.s+'</b><span class="amt ltr">'+nis(v.net*(1+VAT))+'</span>');b.type='button';b.setAttribute('aria-pressed','false');
        b.addEventListener('click',function(){d.started=true;$$('.inv',pick).forEach(function(x){x.disabled=true;x.setAttribute('aria-pressed',x===b?'true':'false')});go(v).catch(stop)});pick.appendChild(b)});
      d.stage.appendChild(pick);
      var tw=h('div','',''), tbl=h('table','tbl','<caption class="vh">חשבוניות שנרשמו</caption><thead><tr><th scope="col">ספק</th><th scope="col">תאריך</th><th scope="col">סה״כ</th></tr></thead><tbody></tbody>');
      var tb=$('tbody',tbl);
      function row(v,cls){var r=h('tr',cls||'','<td>'+v.s+'</td><td class="ltr">'+v.dt+'</td><td class="ltr">'+nis(v.net*(1+VAT))+'</td>');tb.appendChild(r);return r}
      seen.forEach(function(v){row(v)});
      tw.appendChild(h('div','tcap','נרשם עד עכשיו:'));tw.appendChild(tbl);
      async function go(v){
        d.step(1);d.say('חני קוראת את החשבונית…');
        var f=h('div','fields fadein'); d.stage.insertBefore(f,tw);
        var vals=[['ספק',v.s],['תאריך','<span class="ltr">'+v.dt+'</span>'],['לפני מע״מ','<span class="ltr">'+nis(v.net)+'</span>'],['מע״מ 18%','<span class="ltr">'+nis(v.net*VAT)+'</span>'],['סה״כ','<span class="ltr">'+nis(v.net*(1+VAT))+'</span>']];
        var boxes=vals.map(function(x){var b=h('div','fld','<small>'+x[0]+'</small><b>…</b>');f.appendChild(b);return b});
        for(var i=0;i<vals.length;i++){await d.wait(520);boxes[i].classList.add('on');$('b',boxes[i]).innerHTML=vals[i][1]}
        d.step(2);d.say('בודקת כפילויות מול מה שכבר נרשם…');
        await d.wait(900);
        if(v.dup){
          $$('tr',tb)[0].className='dup';
          var a=await d.ask('⚠️ נמצאה כפילות: החשבונית הזו כבר נרשמה ב-03/10. מה עושים?',['לא לרשום פעמיים','לרשום בכל זאת']);
          d.step(3);
          if(a===0){d.say('מצוין. חני לא רשמה כלום, וסימנה לכם את הכפילות. כסף שלא שולם פעמיים.');}
          else{row(v,'new');d.say('נרשם, כי אתם החלטתם. חני רק מציגה, אתם מחליטים.');}
        } else {
          var b=await d.ask('✓ לא נמצאה כפילות. לרשום בטבלה?',['✅ מאשרים','לא עכשיו']);
          d.step(3);
          if(b===0){row(v,'new');d.say('נרשם ✅ אתם רק אישרתם. רוצים לנסות חשבונית אחרת? לחצו "מהתחלה".')}
          else d.say('שום דבר לא נרשם בלי האישור שלכם. החשבונית מחכה בתור.');
        }
      }
      d.stage.appendChild(tw);
    },

    dana:function(d){
      var cats=[['דלק',4140,3000],['חומרי גלם',11800,12400],['שכירות',9000,9000],['פרסום',2300,2600]];
      var max=Math.max.apply(null,cats.map(function(c){return Math.max(c[1],c[2])}))*1.08;
      d.say('דשבורד ההוצאות של החודש, מול הממוצע של 3 החודשים הקודמים.');
      var bars=h('div','bars');
      var rows=cats.map(function(c){var r=h('div','bar-row','<span>'+c[0]+'</span><span class="tr"><span class="fl" style="--v:'+(c[1]/max).toFixed(3)+'"></span><span class="avg" style="--m:'+(c[2]/max*100).toFixed(1)+'%"></span></span><span class="val ltr">'+nis(c[1])+'</span>');bars.appendChild(r);return r});
      d.stage.appendChild(bars);
      d.stage.appendChild(h('div','legend','<span><i></i>ממוצע 3 חודשים</span><span>עמודה = החודש</span>'));
      var go=btn('🔍 הריצי בדיקה','solid',function(){d.started=true;go.disabled=true;run().catch(stop)});
      var gw=h('div','row');gw.appendChild(go);d.stage.appendChild(gw);
      async function run(){
        d.step(1);d.say('דנה בודקת כל קטגוריה מול הממוצע…');
        var sc=h('div','scan');d.stage.insertBefore(sc,gw);
        await d.wait(1700);sc.remove();gw.remove();
        var hot=cats.map(function(c){return (c[1]-c[2])/c[2]});
        var k=hot.indexOf(Math.max.apply(null,hot)), pct=Math.round(hot[k]*100);
        rows[k].classList.add('hot');
        d.step(2);
        d.stage.appendChild(h('div','alert fadein','<b>⚠️ הוצאות ה'+cats[k][0]+' גבוהות מהממוצע</b><p>החודש: <span class="ltr">'+nis(cats[k][1])+'</span>. ממוצע 3 החודשים הקודמים: <span class="ltr">'+nis(cats[k][2])+'</span>. זה <span class="ltr">+'+pct+'%</span>.</p><p>💡 רוב העלייה מתדלוקים בסופי שבוע. שווה לבדוק למה.</p>'));
        d.say('דנה מצאה חריגה אחת, והסבירה אותה במשפט.');
        var a=await d.ask('מה עושים עם זה?',['📌 לסמן לבדיקה','זה תקין']);
        d.step(3);
        await d.wait(400);
        d.stage.appendChild(h('div','summary fadein','<b>📝 הסיכום השבועי של דנה</b>• ההכנסות יציבות מול שבוע שעבר<br>• חריגה אחת: '+cats[k][0]+' (<span class="ltr">+'+pct+'%</span>) · '+(a===0?'סומנה לבדיקה':'אושרה כתקינה')+'<br>• שאר ההוצאות בטווח הרגיל'));
        d.say('ככה נראה סיכום שבועי: קצר, בעברית, בלי לחפור בטבלאות.');
      }
    },

    shira:function(d){
      var chat=h('div','chat','<span class="meta">שירה · סוכנות ביטוח לדוגמה · היום</span>');
      d.stage.appendChild(chat);
      var tm=['23:41','23:42','23:42','23:43','23:44','23:45'], ti=0;
      function add(cls,t){var m=h('div','msg '+cls,t+(cls==='sys'?'':'<small class="ltr">'+tm[Math.min(ti++,tm.length-1)]+'</small>'));chat.appendChild(m);return m}
      async function say(t){var ty=h('div','typing','<i></i><i></i><i></i>');ty.setAttribute('aria-hidden','true');chat.appendChild(ty);await d.wait(900);ty.remove();add('bot',t)}
      add('bot','היי! אני שירה 🙂 במה אפשר לעזור?');
      d.say('השעה כמעט חצות. בחרו שאלה של לקוח:');
      var qs=h('div','qs');
      var Q=[['באילו שעות אתם זמינים?',qa],['אני רוצה הצעה לביטוח רכב',meet],['אני רוצה לבטל את הפוליסה',cancel]];
      Q.forEach(function(q){qs.appendChild(btn(q[0],'',function(){d.started=true;$$('button',qs).forEach(function(b){b.disabled=true});add('them',q[0]);q[1]().catch(stop)}))});
      d.stage.appendChild(qs);
      async function qa(){d.step(1);await say('אני עונה בכל שעה, כל יום. נציג אנושי זמין בימים א׳–ה׳, <span class="ltr">9:00–17:00</span>. רוצה שאעביר את הפרטים שלך, ויחזרו אלייך?');d.step(2);
        await d.wait(700);add('them','כן, תודה');await say('העברתי ✅ יחזרו אלייך מחר בבוקר.');d.step(3);d.say('שאלה חוזרת קיבלה תשובה, באמצע הלילה, בלי שאף אחד התעורר.')}
      async function meet(){d.step(1);await say('בשמחה! איך קוראים לך ומה מספר הטלפון?');await d.wait(900);add('them','מיכל, <span class="ltr">050-0000000</span>');d.step(2);
        await say('תודה מיכל! העברתי את הפרטים, ויחזרו אלייך עם הצעה ✅');d.step(3);d.say('ליד חדש: השם, הטלפון ומה היא צריכה כבר מחכים לכם בבוקר.')}
      async function cancel(){d.step(1);await say('אני מבינה. בקשה כזו מטופלת אישית, אז אני מעבירה אותה עכשיו לבעלי העסק.');
        add('sys','🙋 הועבר לבעלי העסק · יחזרו אלייך היום');d.step(2);
        var a=await d.ask('📲 התראה אליכם: לקוחה מבקשת לבטל פוליסה. שירה לא ענתה בעצמה, כי זה רגיש.',['✅ לחזור אליה בבוקר','📞 להתקשר עכשיו']);
        d.step(3);add('sys',a===0?'✅ אושר: יחזרו אלייך בבוקר':'✅ מתקשרים אלייך עכשיו');
        d.say('בדבר רגיש שירה לא מנחשת. היא עוצרת ומעבירה אליכם.')}
    },

    noga:function(d){
      var kan=h('div','kan'), cols=['חדש','שובץ ספק','נסגר'].map(function(n){var c=h('div','col','<h4><span>'+n+'</span></h4>');kan.appendChild(c);return c});
      cols[2].appendChild(h('div','tk ghost','<b>מזגן · דירה 7</b>נסגר אתמול'));
      var ten=h('div','tenant');
      d.say('דייר שולח הודעה. בחרו מה הוא כותב:');
      var qs=h('div','qs');
      var M=[['💧 יש נזילה בדירה 4','נזילה','דירה 4','דחוף','אינסטלציה לדוגמה'],['❄️ המזגן לא עובד בדירה 2','מזגן','דירה 2','רגיל','מיזוג לדוגמה'],['💡 נורה שרופה בלובי','תאורה','לובי','רגיל','חשמלאי לדוגמה']];
      M.forEach(function(m){qs.appendChild(btn(m[0],'',function(){d.started=true;$$('button',qs).forEach(function(b){b.disabled=true});go(m).catch(stop)}))});
      d.stage.appendChild(qs);d.stage.appendChild(kan);d.stage.appendChild(ten);
      function tmsg(cls,t){var x=h('div','msg '+cls,t);ten.appendChild(x);return x}
      async function go(m){
        tmsg('them','<b>דייר:</b> '+m[0].slice(m[0].indexOf(' ')+1));
        d.step(1);await d.wait(700);
        var card=h('div','tk','<b>'+m[1]+' · '+m[2]+'</b>קריאה <span class="ltr">#1042</span><br><span class="pr">'+m[3]+'</span>');
        cols[0].appendChild(card);
        await d.wait(500);tmsg('bot','<b>נגה:</b> קיבלתי! פתחתי קריאה מספר <span class="ltr">1042</span>. אעדכן אותך בכל שלב.');
        d.say('נגה פתחה קריאה ושייכה אותה לנכס.');
        var a=await d.ask('לשבץ את "'+m[4]+'"? יכול להגיע מחר <span class="ltr">8:00–10:00</span>',['✅ לשבץ','ספק אחר']);
        var sup=a===0?m[4]:'שיפוצים לדוגמה';
        d.step(2);card.remove();card=h('div','tk','<b>'+m[1]+' · '+m[2]+'</b>'+sup+'<br><span class="pr">מחר <span class="ltr">8:00–10:00</span></span>');cols[1].appendChild(card);
        await d.wait(500);tmsg('bot','<b>נגה:</b> '+sup+' בדרך אליך: מחר בין <span class="ltr">8:00</span> ל-<span class="ltr">10:00</span>.');
        d.say('הספק שובץ. עכשיו נגה עוקבת.');
        await d.wait(1600);
        d.step(3);card.remove();cols[2].insertBefore(h('div','tk','<b>'+m[1]+' · '+m[2]+'</b>הספק דיווח: תוקן ✅'),cols[2].children[1]);
        await d.wait(400);tmsg('bot','<b>נגה:</b> התקלה טופלה ✅ איך היה השירות, מ-1 עד 5?');
        d.say('מההודעה ועד הסגירה. אתם לחצתם פעם אחת.');
      }
    },

    gal:function(d){
      var N=[['📝','טופס הזמנה','הלקוח ממלא'],['🗃️','CRM','לקוח נפתח'],['🧾','חשבונית','נשלחת ללקוח'],['⏰','תזכורת תשלום','בזמן']];
      var flow=h('div','flow'), nodes=N.map(function(n){var x=h('div','node','<span class="ic" aria-hidden="true">'+n[0]+'</span><b'+(n[1]==='CRM'?' class="ltr"':'')+'>'+n[1]+'</b><small>'+n[2]+'</small>');flow.appendChild(x);return x});
      var cn=h('div','counters','<div class="cnt"><b class="ltr" id="gal-a">0</b><small>פעולות שגל עשה</small></div><div class="cnt zero"><b class="ltr">0</b><small>הקלדות ידניות</small></div>');
      d.stage.appendChild(flow);d.stage.appendChild(cn);
      d.say('לקוח ממלא טופס הזמנה. מה קורה מכאן?');
      var go=btn('📝 שלחו הזמנה לדוגמה','solid',function(){d.started=true;go.disabled=true;run().catch(stop)});
      var gw=h('div','row');gw.appendChild(go);d.stage.appendChild(gw);
      var acts=0;function tick(){acts++;$('#gal-a',cn).textContent=acts}
      var total=3*500*(1+VAT);
      async function run(){
        gw.remove();
        nodes[0].classList.add('on');tick();d.step(1);d.say('התקבלה הזמנה: 3 מארזים, '+nis(total)+' כולל מע״מ.');
        await d.wait(1100);nodes[1].classList.add('on');tick();d.say('הלקוח נפתח ב-CRM לבד. אף אחד לא הקליד.');
        await d.wait(900);nodes[2].classList.add('wait');d.step(2);
        var a=await d.ask('החשבונית מוכנה: '+nis(total)+' כולל מע״מ. לשלוח ללקוח?',['✅ לשלוח','לבדוק קודם']);
        if(a===1){d.step(3);d.say('החשבונית מחכה לבדיקה שלכם. שום דבר לא נשלח בלי האישור שלכם.');return}
        nodes[2].classList.remove('wait');nodes[2].classList.add('on');tick();d.say('החשבונית נשלחה ללקוח, אחרי האישור שלכם.');
        await d.wait(1100);nodes[3].classList.add('on');tick();d.step(3);
        d.say('תזכורת תשלום תצא לבד אם לא ישולם בזמן. 4 פעולות, 0 הקלדות.');
      }
    },

    office:function(d){
      var NM={chani:'חני',dana:'דנה',shira:'שירה',noga:'נגה',gal:'גל'};
      var O={
        'משרד רואי חשבון':[['📥','חשבוניות שלקוחות שולחים בוואטסאפ','chani'],['📨','תזכורות ללקוחות על מסמכים חסרים','gal'],['💬','מענה לשאלות חוזרות של לקוחות','shira'],['📊','התראה על חריגה בנתונים של לקוח','dana']],
        'משרד עורכי דין':[['💬','מענה ראשוני לפניות של לקוחות חדשים','shira'],['🧾','חשבוניות ספקים והוצאות המשרד','chani'],['⏰','חשבונית ותזכורת תשלום ללקוח','gal'],['📊','תמונת הכנסות והוצאות חודשית','dana']],
        'ניהול נכסים':[['🔧','קריאות שירות מדיירים','noga'],['💬','שאלות דיירים, גם בלילה','shira'],['🧾','חשבוניות של ספקים','chani'],['📊','הוצאות לכל בניין, עם התראה על חריגה','dana']],
        'סוכנות ביטוח':[['💬','שאלות של לקוחות, בכל שעה','shira'],['🔗','לידים מהאתר ישר ל-<span class="ltr">CRM</span>','gal'],['📨','תזכורות על מסמכים חסרים','gal'],['📊','מעקב הכנסות וחריגות','dana']]
      };
      var base=location.pathname.indexOf('/team/')>=0?'':'team/';
      d.say('בחרו את סוג המשרד שלכם:');
      var qs=h('div','qs'), map=h('div','omap');
      Object.keys(O).forEach(function(k){var b=btn(k,'',function(){d.started=true;d.tok++;$$('button',qs).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});map.innerHTML='';$$('.youbox,.kbox',d.stage).forEach(function(x){x.remove()});go(k).catch(stop)});b.setAttribute('aria-pressed','false');qs.appendChild(b)});
      d.stage.appendChild(qs);d.stage.appendChild(map);
      async function go(k){
        d.step(1);d.say('אלה משימות שחוזרות ב'+k+'. מי לוקח מה?');
        for(var i=0;i<O[k].length;i++){var t=O[k][i];
          map.appendChild(h('div','orow','<span class="tk2"><span class="e" aria-hidden="true">'+t[0]+'</span><span>'+t[1]+'</span></span><span class="ar" aria-hidden="true">←</span><a class="who" href="'+base+t[2]+'.html"><svg aria-hidden="true" viewBox="0 0 200 204"><use href="#ch-'+t[2]+'"/></svg>'+NM[t[2]]+'</a>'));
          await d.wait(650)}
        d.say(O[k].map(function(t){return NM[t[2]]+': '+t[1].replace(/<[^>]+>/g,'')}).join(' · '));
        d.step(2);await d.wait(900);
        d.stage.appendChild(h('div','youbox','<b>👑 ומה נשאר אצלכם?</b><span>לאשר את מה שרגיש, ולנהל.</span>'));
        await d.wait(700);d.step(3);
        d.stage.appendChild(h('div','kbox','<svg aria-hidden="true" viewBox="0 0 200 204"><use href="#ch-karin"/></svg><span><b>וכל השאר?</b> אני בונה ומחברת לפי מה שכבר יש אצלכם.</span>'));
        d.say('זו דוגמה. אפשר לבחור משרד אחר. את המפה האמיתית שלכם בונים יחד בשיחת האפיון.');
      }
    },

    training:function(d){
      var T={
        'מיילים ללקוחות':[['פותחים צ׳אט חדש','מסבירים מהתחלה מי אתם','מעתיקים, מתקנים, מדביקים','מחר? אותו דבר שוב'],['הוראות קבועות שכתבנו יחד, בסגנון שלכם','מדביקים את המייל ומקבלים טיוטה','עוברים ומאשרים','ובשלב הבא: סוכן שעושה את זה לבד']],
        'סיכום פגישות':[['מקליטים, ושוכחים מההקלטה','מנסים לסכם מהזיכרון','משימות הולכות לאיבוד','אותו בלגן בכל פגישה'],['תבנית סיכום אחת לכל פגישה','משימות עם אחראי ותאריך','נשלח לכולם בסוף היום','ובשלב הבא: סוכן שעושה את זה לבד']],
        'הצעות מחיר':[['מחפשים את ההצעה הקודמת','משנים ידנית שמות ומספרים','שוכחים סעיף','כל הצעה מתחילה מאפס'],['תבנית אחת עם הסעיפים שלכם','ממלאים פרטים, מקבלים טיוטה','בודקים ושולחים','ובשלב הבא: סוכן שעושה את זה לבד']]
      };
      d.say('בחרו משימה שחוזרת אצלכם כל שבוע:');
      var qs=h('div','tr-pick'), vs=h('div','vs');
      Object.keys(T).forEach(function(k){qs.appendChild(btn(k,'',function(){d.started=true;$$('button',qs).forEach(function(b){b.disabled=true});go(k).catch(stop)}))});
      d.stage.appendChild(qs);d.stage.appendChild(vs);
      async function go(k){
        vs.innerHTML='';
        var bad=h('div','bad fadein','<h4>היום: עוד שיחה עם ה-<span class="ltr">AI</span></h4><ol></ol>'), good=h('div','good fadein','<h4>אחרי ההדרכה: דרך עבודה קבועה</h4><ol></ol>');
        vs.appendChild(bad);vs.appendChild(good);
        d.step(1);
        for(var i=0;i<4;i++){$('ol',bad).appendChild(h('li','fadein',T[k][0][i]));await d.wait(380)}
        d.step(2);d.say('ועכשיו, אותה משימה אחרי הדרכה:');
        for(i=0;i<4;i++){$('ol',good).appendChild(h('li','fadein',T[k][1][i]));await d.wait(560)}
        d.step(3);d.say('זה ההבדל בין לדבר עם ה-AI לבין לעבוד איתו.');
      }
    }
  };

  var demos={};
  function boot(el){var k=el.getAttribute('data-demo');if(demos[el.id])return;demos[el.id]=new Demo(el);demos[el.id].start()}
  $$('.demo[data-demo]').forEach(function(el){if(!el.hidden)boot(el)});

  // tabs (home): demos per agent
  var tl=$('[role="tablist"]');
  if(tl){
    var tabs=$$('[role="tab"]',tl);
    var sel=function(t,focus){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute('aria-controls'));p.hidden=!on;if(on)boot(p)});if(focus)t.focus()};
    tabs.forEach(function(t,i){
      t.addEventListener('click',function(){sel(t)});
      t.addEventListener('keydown',function(e){var k=e.key,n=null;
        if(k==='ArrowLeft')n=tabs[(i+1)%tabs.length]; else if(k==='ArrowRight')n=tabs[(i-1+tabs.length)%tabs.length];
        else if(k==='Home')n=tabs[0]; else if(k==='End')n=tabs[tabs.length-1];
        if(n){e.preventDefault();sel(n,true)}});
    });
  }
})();
