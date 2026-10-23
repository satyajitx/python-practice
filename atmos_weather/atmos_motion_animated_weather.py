from flask import Flask, request, render_template_string
import requests
from datetime import datetime
import random

app = Flask(__name__)

# Atmos Motion: a single-file animated weather website.
# Weather data is provided by the free Open-Meteo API (no API key required).

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atmos Motion — Live Weather</title>
<style>
:root {
  --ink:#f4f7ff; --muted:#aab7d5; --panel:rgba(24,34,65,.64);
  --line:rgba(255,255,255,.11); --cyan:#78e8ff; --violet:#b69aff;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; min-height:100vh; color:var(--ink);
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:#070d20; overflow-x:hidden;
}
button,input{font:inherit}
button{cursor:pointer}
#sky{position:fixed;inset:0;overflow:hidden;z-index:-5;background:
  radial-gradient(ellipse at 15% 15%,rgba(48,105,201,.42),transparent 42%),
  radial-gradient(ellipse at 90% 80%,rgba(126,48,185,.30),transparent 38%),
  linear-gradient(140deg,#0b1733,#080d20 55%,#10152e);
  transition:background 1.8s ease}
#sky:before,#sky:after{content:"";position:absolute;width:70vw;height:70vw;border-radius:50%;
  filter:blur(65px);opacity:.24;animation:aurora 20s ease-in-out infinite alternate}
#sky:before{background:#3979d9;top:-40vw;left:-12vw}
#sky:after{background:#7b42b9;right:-35vw;bottom:-45vw;animation-delay:-8s}
@keyframes aurora{to{transform:translate(8vw,10vh) scale(1.22)}}
.stars{position:absolute;inset:0;pointer-events:none}
.star{position:absolute;width:2px;height:2px;background:#fff;border-radius:50%;opacity:.25;animation:twinkle 3.5s ease-in-out infinite}
@keyframes twinkle{0%,100%{opacity:.12;transform:scale(.7)}50%{opacity:.9;transform:scale(1.6)}}
.cloud{
  position:absolute;width:210px;height:62px;border-radius:100px;
  background:linear-gradient(180deg,rgba(222,235,255,.28),rgba(113,139,183,.10));
  filter:blur(1px);opacity:.43;animation:cloudDrift 42s linear infinite;
  box-shadow:inset 0 1px 3px rgba(255,255,255,.13),0 14px 38px rgba(4,10,30,.12)
}
.cloud:before,.cloud:after{content:"";position:absolute;border-radius:50%;
  background:inherit}
.cloud:before{width:86px;height:86px;left:28px;top:-38px}
.cloud:after{width:112px;height:112px;left:80px;top:-58px}
.cloud.c1{top:13%;left:-260px;transform:scale(1.15);animation-duration:58s}
.cloud.c2{top:40%;left:-300px;transform:scale(.72);opacity:.24;animation-duration:72s;animation-delay:-27s}
.cloud.c3{top:72%;left:-240px;transform:scale(1.35);opacity:.16;animation-duration:80s;animation-delay:-45s}
.cloud.c4{top:25%;left:-280px;transform:scale(.55);opacity:.19;animation-duration:49s;animation-delay:-13s}
@keyframes cloudDrift{from{translate:0 0}to{translate:calc(100vw + 500px) 0}}
.weather-sun{position:absolute;right:13%;top:13%;width:110px;height:110px;opacity:0;transition:opacity 1s}
.sun-core{position:absolute;inset:25px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff8bf,#ffc35d 55%,#ff8c48);box-shadow:0 0 35px #ffcb6b,0 0 95px #ffb64b88;animation:sunPulse 4s ease-in-out infinite}
.sun-rays{position:absolute;inset:0;border:2px dashed #ffd47d;border-radius:50%;animation:spin 35s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes sunPulse{50%{transform:scale(1.06);box-shadow:0 0 55px #ffcb6b,0 0 120px #ffb64b99}}
.moon{position:absolute;right:17%;top:15%;font-size:82px;filter:drop-shadow(0 0 24px #d9e4ff77);animation:moonFloat 6s ease-in-out infinite}
@keyframes moonFloat{50%{transform:translateY(-12px) rotate(-5deg)}}
.rain-layer{position:absolute;inset:-10%;pointer-events:none;opacity:0;transition:opacity 1s}
.drop{position:absolute;top:-15%;width:1px;height:70px;background:linear-gradient(transparent,#a8d9ffb0);animation:rainFall linear infinite}
@keyframes rainFall{to{transform:translate3d(-70px,120vh,0)}}
.lightning{position:absolute;inset:0;background:#dceaff;opacity:0;pointer-events:none}
.lightning.flash{animation:flash .55s ease-out}
@keyframes flash{0%,25%,48%{opacity:.55}15%,38%,100%{opacity:0}}
.page{width:min(1500px,100%);margin:auto;padding:24px 28px 48px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:24px;animation:rise .8s both}
.brand{display:flex;align-items:center;gap:12px;font-size:23px;font-weight:800;letter-spacing:-.7px}
.brand-icon{display:grid;place-items:center;width:44px;height:44px;border-radius:15px;background:linear-gradient(135deg,#7be9ff,#aa8aff);color:#102041;box-shadow:0 8px 30px #8da9ff44;font-size:23px}
.brand .dot{color:var(--cyan)}
.live-pill{display:flex;align-items:center;gap:8px;padding:10px 14px;border:1px solid #3acaa84d;border-radius:99px;background:#0eaf7c12;color:#9df5d4;font-size:11px;font-weight:800;letter-spacing:1px}
.live-dot{width:7px;height:7px;border-radius:50%;background:#50e3ad;box-shadow:0 0 12px #50e3ad;animation:livePulse 1.8s infinite}
@keyframes livePulse{50%{opacity:.35;transform:scale(.7)}}
.search{display:flex;gap:12px;margin-bottom:20px;animation:rise .9s .08s both}
.search input{flex:1;min-width:0;border:1px solid var(--line);outline:none;border-radius:18px;padding:17px 20px;background:#101a32d9;color:#fff;box-shadow:inset 0 1px 0 #ffffff08;transition:border .25s,box-shadow .25s}
.search input:focus{border-color:#7be9ff99;box-shadow:0 0 0 4px #7be9ff12}
.search button{border:0;border-radius:17px;padding:0 26px;font-weight:800;color:#101b37;background:linear-gradient(120deg,#8cecff,#b5a0ff);box-shadow:0 8px 25px #91baff24;transition:transform .25s,filter .25s}
.search button:hover{transform:translateY(-3px);filter:brightness(1.08)}
.search button:active{transform:scale(.97)}
.notice{color:var(--muted);font-size:12px;text-align:center;margin:0 0 22px;min-height:18px}
.layout{display:grid;grid-template-columns:220px minmax(0,1fr);gap:22px}
.sidebar{border:1px solid var(--line);border-radius:24px;background:#101a32a8;padding:18px;height:max-content;backdrop-filter:blur(18px);animation:slideIn .9s .15s both}
.side-title{font-size:10px;letter-spacing:1.7px;color:#7f91b9;font-weight:800;margin:8px 0 14px}
.city-button{display:block;width:100%;text-align:left;color:#eaf0ff;border:1px solid transparent;background:#ffffff07;border-radius:16px;padding:13px;margin-bottom:9px;transition:background .3s,border .3s,transform .3s}
.city-button:hover{background:#ffffff12;transform:translateX(3px)}
.city-button.active{background:#a6c9ff18;border-color:#9dcaff4a}
.city-button strong{display:block;font-size:14px;margin-bottom:4px}
.city-button span{font-size:11px;color:#aab7d5}
.side-note{color:#8392b5;font-size:11px;line-height:1.7;margin-top:22px}
.main{min-width:0}
.hero{position:relative;min-height:310px;overflow:hidden;border:1px solid var(--line);border-radius:30px;padding:28px 34px;background:linear-gradient(120deg,#ffffff0d,#ffffff04);backdrop-filter:blur(18px);box-shadow:0 24px 80px #00000013;animation:rise .85s .12s both}
.hero:before{content:"";position:absolute;width:330px;height:330px;right:-80px;top:-120px;border-radius:50%;background:radial-gradient(circle,#8be8ff24,transparent 68%);animation:heroGlow 8s ease-in-out infinite alternate}
@keyframes heroGlow{to{transform:translate(-50px,70px) scale(1.25);opacity:.55}}
.hero-top{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;position:relative}
.eyebrow{font-size:10px;letter-spacing:2px;color:#a5b5d7;font-weight:800}
.city-name{font-size:clamp(25px,3vw,38px);font-weight:750;letter-spacing:-1.4px;margin:9px 0 5px}
.condition{color:#b8c5df;font-size:15px}
.weather-icon{font-size:72px;filter:drop-shadow(0 8px 22px #c4ddff36);animation:iconFloat 5s ease-in-out infinite;transform-origin:center}
@keyframes iconFloat{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-11px) rotate(4deg)}}
.temperature{display:flex;align-items:flex-start;gap:8px;margin-top:20px;font-size:clamp(70px,9vw,116px);line-height:.98;font-weight:650;letter-spacing:-7px;background:linear-gradient(115deg,#fff 20%,#b7f3ff 52%,#d2bfff 82%);-webkit-background-clip:text;background-clip:text;color:transparent;animation:tempIn 1s cubic-bezier(.2,.8,.2,1) both}
.temperature small{font-size:25px;letter-spacing:0;margin-top:12px;color:#b8c5df}
.hero-foot{display:flex;flex-wrap:wrap;gap:10px 18px;color:#9fafd0;font-size:12px;margin-top:18px}
.hero-foot span{display:flex;align-items:center;gap:6px}
@keyframes tempIn{from{opacity:0;transform:translateY(18px);filter:blur(8px)}to{opacity:1;transform:translateY(0);filter:blur(0)}}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin:16px 0}
.metric,.panel{border:1px solid var(--line);border-radius:22px;background:var(--panel);backdrop-filter:blur(18px);box-shadow:0 12px 38px #0000000b}
.metric{padding:18px;min-height:118px;animation:rise .7s both;transition:transform .35s,border-color .35s,background .35s}
.metric:nth-child(2){animation-delay:.07s}.metric:nth-child(3){animation-delay:.14s}.metric:nth-child(4){animation-delay:.21s}
.metric:hover{transform:translateY(-5px);border-color:#a8dfff44;background:#263657b8}
.metric-label{color:#a0b0d0;font-size:11px;display:flex;align-items:center;gap:8px}
.metric-label i{font-style:normal;font-size:18px}
.metric-value{font-size:26px;font-weight:750;margin-top:13px;letter-spacing:-.8px}
.metric-unit{font-size:12px;color:#9fafd0;font-weight:500}
.dashboard{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(230px,1fr);gap:16px}
.panel{padding:20px;animation:rise .8s .25s both;min-width:0}
.panel-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:18px}
.panel h2{font-size:15px;margin:0;letter-spacing:-.3px}
.panel-sub{color:#8494b8;font-size:11px}
.hourly{display:flex;gap:10px;overflow-x:auto;padding:3px 2px 12px;scrollbar-width:thin;scrollbar-color:#6475a2 transparent}
.hour{flex:0 0 88px;text-align:center;border:1px solid #ffffff0b;border-radius:16px;padding:13px 8px;background:#ffffff04;transition:transform .3s,background .3s}
.hour:hover{transform:translateY(-5px);background:#ffffff0d}
.hour-time{font-size:11px;color:#a8b6d5}
.hour-icon{font-size:25px;margin:13px 0;animation:iconFloat 5s ease-in-out infinite}
.hour-temp{font-weight:750;font-size:15px}
.hour-rain{font-size:10px;color:#77dff7;margin-top:7px}
.days{display:grid;gap:2px}
.day{display:grid;grid-template-columns:minmax(68px,.8fr) 28px minmax(45px,1fr) 38px;gap:9px;align-items:center;padding:13px 2px;border-bottom:1px solid #ffffff0d}
.day:last-child{border-bottom:0}
.day-name{font-size:12px;font-weight:650}
.day-rain{font-size:10px;color:#76dcf7;margin-top:4px}
.day-icon{font-size:20px}
.bar-track{height:6px;border-radius:99px;background:#ffffff0c;overflow:hidden}
.bar{height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,#ffe36e,#ff9b50,#ff6d91);animation:barGrow 1.4s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes barGrow{to{width:var(--bar-width)}}
.day-temps{text-align:right;font-size:11px;color:#aebbd7;white-space:nowrap}
.right-stack{display:grid;gap:16px;align-content:start}
.feels-big{font-size:37px;font-weight:750;letter-spacing:-1.5px;margin:12px 0}
.detail{color:#a4b2d0;font-size:12px;line-height:1.7}
.sunpath{height:75px;position:relative;margin-top:12px;overflow:hidden}
.sunpath:before{content:"";position:absolute;left:8%;right:8%;bottom:-55px;height:115px;border:1px dashed #a7b6d84d;border-bottom:0;border-radius:100% 100% 0 0}
.sunpath-dot{position:absolute;width:13px;height:13px;border-radius:50%;background:#ffdc78;box-shadow:0 0 18px #ffdc78;left:50%;top:14px;animation:sunPath 8s ease-in-out infinite alternate}
@keyframes sunPath{to{left:84%;top:45px}}
.wind-compass{width:112px;height:112px;border:1px dashed #a6b7db55;border-radius:50%;margin:16px auto 10px;display:grid;place-items:center;position:relative}
.wind-compass:before{content:"N";position:absolute;top:8px;font-size:9px;color:#a6b7d5}
.wind-arrow{font-size:32px;transform:rotate(20deg);color:#d6e8ff;animation:windTurn 7s ease-in-out infinite alternate}
@keyframes windTurn{to{transform:rotate(80deg)}}
.footer{text-align:center;color:#68799f;font-size:11px;padding:26px 0 0}
.loading{display:none;align-items:center;gap:8px;color:#a8dfff;font-size:12px}
.loading.show{display:flex}
.spinner{width:14px;height:14px;border:2px solid #ffffff30;border-top-color:#8cecff;border-radius:50%;animation:spin .7s linear infinite}
.error{border:1px solid #ff9e9e44;background:#ff6c6c12;color:#ffc3c3;border-radius:15px;padding:14px;margin:12px 0}
.empty{padding:38px 15px;text-align:center;color:#a7b6d5}
.empty strong{display:block;color:#f0f5ff;font-size:18px;margin-bottom:8px}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-18px)}to{opacity:1;transform:translateX(0)}}
@media(max-width:1050px){.layout{grid-template-columns:180px minmax(0,1fr)}.dashboard{grid-template-columns:1fr}.right-stack{grid-template-columns:repeat(2,minmax(0,1fr))}.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:680px){.page{padding:16px 13px 32px}.layout{grid-template-columns:1fr}.sidebar{order:2}.main{order:1}.hero{padding:22px;min-height:280px}.weather-icon{font-size:55px}.temperature{font-size:82px}.search{gap:7px}.search input{padding:15px 13px}.search button{padding:0 17px}.metrics{gap:9px}.metric{padding:14px;min-height:105px}.metric-value{font-size:23px}.right-stack{grid-template-columns:1fr}.topbar{margin-bottom:17px}.live-pill{font-size:9px;padding:9px}.sidebar{padding:14px}.city-button{display:inline-block;width:calc(50% - 6px);vertical-align:top;margin-right:4px}.side-note{margin-top:10px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}
</style>
</head>
<body>
<div id="sky">
  <div class="stars" id="stars"></div>
  <div class="cloud c1"></div><div class="cloud c2"></div><div class="cloud c3"></div><div class="cloud c4"></div>
  <div class="weather-sun" id="sun"><div class="sun-rays"></div><div class="sun-core"></div></div>
  <div class="moon" id="moon">☾</div>
  <div class="rain-layer" id="rain"></div>
  <div class="lightning" id="lightning"></div>
</div>
<div class="page">
  <header class="topbar">
    <div class="brand"><div class="brand-icon">✳</div><span>atmos<span class="dot">.</span></span></div>
    <div class="live-pill"><span class="live-dot"></span> LIVE WEATHER</div>
  </header>
  <form class="search" action="/" method="get" id="searchForm">
    <input name="city" id="cityInput" value="{{ city }}" placeholder="Search any city — e.g. Bhubaneswar" aria-label="City name" autocomplete="off">
    <button type="submit">Search ↗</button>
  </form>
  <div class="notice"><span class="loading" id="loading"><span class="spinner"></span> Updating the forecast…</span><span id="noticeText">Live conditions · Powered by Open-Meteo · No API key required</span></div>

  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}

  {% if weather %}
  <div class="layout">
    <aside class="sidebar">
      <div class="side-title">YOUR PLACES</div>
      {% for place in places %}
      <button class="city-button {% if place|lower == city|lower %}active{% endif %}" type="button" data-city="{{ place }}">
        <strong>{{ place }}</strong><span>Tap to view forecast</span>
      </button>
      {% endfor %}
      <div class="side-note">The sky moves with the weather. Search a city to explore its live conditions and 7-day forecast.</div>
    </aside>
    <main class="main">
      <section class="hero">
        <div class="hero-top">
          <div>
            <div class="eyebrow">CURRENT WEATHER · {{ weather.country|upper }}</div>
            <div class="city-name">{{ weather.name }}</div>
            <div class="condition">{{ weather.description }}</div>
          </div>
          <div class="weather-icon" id="heroIcon">{{ weather.icon }}</div>
        </div>
        <div class="temperature"><span id="tempValue">{{ weather.temp|round|int }}</span><small>°C</small></div>
        <div class="hero-foot">
          <span>🌡 Feels like <b>{{ weather.feels|round|int }}°C</b></span>
          <span>↻ Updated <b>{{ weather.updated }}</b></span>
        </div>
      </section>

      <section class="metrics">
        <article class="metric"><div class="metric-label"><i>💧</i> HUMIDITY</div><div class="metric-value">{{ weather.humidity }}<span class="metric-unit"> %</span></div></article>
        <article class="metric"><div class="metric-label"><i>🌬</i> WIND SPEED</div><div class="metric-value">{{ weather.wind|round|int }}<span class="metric-unit"> km/h</span></div></article>
        <article class="metric"><div class="metric-label"><i>🌧</i> PRECIPITATION</div><div class="metric-value">{{ weather.precip|round(1) }}<span class="metric-unit"> mm</span></div></article>
        <article class="metric"><div class="metric-label"><i>☔</i> RAIN CHANCE</div><div class="metric-value">{{ weather.rain }}<span class="metric-unit"> %</span></div></article>
      </section>

      <section class="dashboard">
        <div>
          <article class="panel">
            <div class="panel-head"><h2>Conditions</h2><span class="panel-sub">Next 24 hours</span></div>
            <div class="hourly">
              {% for h in weather.hourly %}
              <div class="hour">
                <div class="hour-time">{{ h.time }}</div>
                <div class="hour-icon">{{ h.icon }}</div>
                <div class="hour-temp">{{ h.temp|round|int }}°</div>
                <div class="hour-rain">{{ h.rain }}% rain</div>
              </div>
              {% endfor %}
            </div>
          </article>
          <article class="panel" style="margin-top:16px">
            <div class="panel-head"><h2>7-day forecast</h2><span class="panel-sub">Daily outlook</span></div>
            <div class="days">
              {% for d in weather.daily %}
              <div class="day">
                <div><div class="day-name">{{ d.day }}</div><div class="day-rain">{{ d.rain }}% rain</div></div>
                <div class="day-icon">{{ d.icon }}</div>
                <div class="bar-track"><div class="bar" style="--bar-width:{{ d.bar }}%"></div></div>
                <div class="day-temps">{{ d.max|round|int }}° <span style="color:#7788aa">{{ d.min|round|int }}°</span></div>
              </div>
              {% endfor %}
            </div>
          </article>
        </div>
        <div class="right-stack">
          <article class="panel">
            <div class="panel-head"><h2>Feels like</h2><span>🌡</span></div>
            <div class="feels-big">{{ weather.feels|round|int }}°</div>
            <div class="detail">Apparent temperature, accounting for how warm or cool the air may feel.</div>
          </article>
          <article class="panel">
            <div class="panel-head"><h2>Wind</h2><span>➤</span></div>
            <div class="wind-compass"><div class="wind-arrow">➤</div></div>
            <div class="detail" style="text-align:center">{{ weather.wind|round|int }} km/h · {{ weather.wind_dir }}</div>
          </article>
          <article class="panel">
            <div class="panel-head"><h2>Daylight</h2><span>☀</span></div>
            <div class="detail">Sunrise <b style="color:#f4f7ff">{{ weather.sunrise }}</b></div>
            <div class="sunpath"><div class="sunpath-dot"></div></div>
            <div class="detail">Sunset <b style="color:#f4f7ff">{{ weather.sunset }}</b></div>
          </article>
          <article class="panel">
            <div class="panel-head"><h2>Atmosphere</h2><span>✧</span></div>
            <div class="detail">Current conditions are fetched live from the weather service. Background effects are animated locally in your browser.</div>
          </article>
        </div>
      </section>
    </main>
  </div>
  {% else %}
    <section class="hero empty"><strong>Explore the sky.</strong>Search for a city above to load its current weather and forecast.</section>
  {% endif %}
  <footer class="footer">ATMOS MOTION · Built with Python + Flask · Weather by Open-Meteo</footer>
</div>
<script>
(function(){
  const stars=document.getElementById('stars');
  for(let i=0;i<95;i++){const s=document.createElement('span');s.className='star';s.style.left=Math.random()*100+'%';s.style.top=Math.random()*100+'%';s.style.animationDelay=(Math.random()*4)+'s';s.style.animationDuration=(2+Math.random()*4)+'s';stars.appendChild(s)}
  const rain=document.getElementById('rain');
  for(let i=0;i<100;i++){const d=document.createElement('span');d.className='drop';d.style.left=Math.random()*100+'%';d.style.animationDuration=(.55+Math.random()*.75)+'s';d.style.animationDelay=(-Math.random()*2)+'s';d.style.opacity=(.2+Math.random()*.6);rain.appendChild(d)}
  const condition={{ weather.code if weather else -1 }};
  const sun=document.getElementById('sun'), moon=document.getElementById('moon');
  const clouds=document.querySelectorAll('.cloud');
  const rainy=[51,53,55,56,57,61,63,65,66,67,80,81,82,95,96,99].includes(condition);
  const cloudy=[1,2,3,45,48].includes(condition);
  const night=new Date().getHours()<6||new Date().getHours()>18;
  if(rainy){rain.style.opacity='.72';clouds.forEach(c=>{c.style.opacity='.72';c.style.filter='blur(2px)'});document.getElementById('sky').style.background='radial-gradient(ellipse at 70% 20%,#344b70,transparent 45%),linear-gradient(145deg,#101a31,#070b18)'}
  else if(cloudy){clouds.forEach(c=>c.style.opacity='.52')}
  else if(!night){sun.style.opacity='.95';moon.style.opacity='0'}
  if(night&&!rainy){moon.style.opacity='.85';sun.style.opacity='0'}
  if([95,96,99].includes(condition)){setInterval(()=>{const l=document.getElementById('lightning');l.classList.remove('flash');void l.offsetWidth;l.classList.add('flash')},6500+Math.random()*7000)}
  document.querySelectorAll('[data-city]').forEach(btn=>btn.addEventListener('click',()=>{document.getElementById('cityInput').value=btn.dataset.city;document.getElementById('loading').classList.add('show');document.getElementById('noticeText').textContent='';document.getElementById('searchForm').requestSubmit()}));
  document.getElementById('searchForm').addEventListener('submit',()=>{document.getElementById('loading').classList.add('show');document.getElementById('noticeText').textContent=''});
  // Reveal cards with a gentle stagger when they enter the viewport.
  if('IntersectionObserver' in window){const obs=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.style.animationPlayState='running';obs.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('.panel,.metric').forEach(el=>{el.style.animationPlayState='paused';obs.observe(el)})}
})();
</script>
</body>
</html>
"""

WEATHER_CODES = {
    0: ("Clear sky", "☀️"), 1: ("Mainly clear", "🌤️"), 2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"), 45: ("Fog", "🌫️"), 48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"), 53: ("Drizzle", "🌦️"), 55: ("Dense drizzle", "🌧️"),
    56: ("Freezing drizzle", "🌧️"), 57: ("Freezing drizzle", "🌧️"),
    61: ("Light rain", "🌦️"), 63: ("Rain", "🌧️"), 65: ("Heavy rain", "🌧️"),
    66: ("Freezing rain", "🌧️"), 67: ("Heavy freezing rain", "🌧️"),
    71: ("Light snow", "🌨️"), 73: ("Snow", "🌨️"), 75: ("Heavy snow", "❄️"),
    77: ("Snow grains", "🌨️"), 80: ("Rain showers", "🌦️"), 81: ("Rain showers", "🌧️"),
    82: ("Heavy showers", "⛈️"), 85: ("Snow showers", "🌨️"), 86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm with hail", "⛈️"), 99: ("Severe thunderstorm", "⛈️")
}

def get_json(url, params):
    response = requests.get(url, params=params, timeout=12)
    response.raise_for_status()
    return response.json()

def build_weather(city):
    geo = get_json("https://geocoding-api.open-meteo.com/v1/search",
                   {"name": city, "count": 1, "language": "en", "format": "json"})
    results = geo.get("results") or []
    if not results:
        raise ValueError(f"Couldn't find “{city}”. Check the spelling or try a nearby city.")
    place = results[0]
    params = {
        "latitude": place["latitude"], "longitude": place["longitude"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,weather_code,wind_speed_10m,wind_direction_10m",
        "hourly": "temperature_2m,precipitation_probability,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset",
        "forecast_days": 7, "timezone": "auto"
    }
    data = get_json("https://api.open-meteo.com/v1/forecast", params)
    current = data["current"]
    hourly = data.get("hourly", {})
    daily = data.get("daily", {})
    code = int(current.get("weather_code", 0))
    desc, icon = WEATHER_CODES.get(code, ("Weather conditions", "🌤️"))
    now = current.get("time", "")
    times = hourly.get("time", [])
    start = 0
    if now in times:
        start = times.index(now)
    else:
        now_hour = now[-5:] if len(now) >= 5 else ""
        start = next((i for i,t in enumerate(times) if t[-5:] >= now_hour), 0)
    hours = []
    for i in range(start, min(start + 12, len(times))):
        hcode = int(hourly.get("weather_code", [0]*len(times))[i])
        hdesc, hicon = WEATHER_CODES.get(hcode, ("Weather", "🌤️"))
        hours.append({
            "time": times[i][-5:], "temp": hourly["temperature_2m"][i],
            "rain": hourly["precipitation_probability"][i] or 0, "icon": hicon
        })
    days = []
    dates = daily.get("time", [])
    maxes = daily.get("temperature_2m_max", [])
    mins = daily.get("temperature_2m_min", [])
    rains = daily.get("precipitation_probability_max", [])
    codes = daily.get("weather_code", [])
    max_high = max(maxes) if maxes else 1
    min_low = min(mins) if mins else 0
    spread = max(max_high-min_low, 1)
    for i, date in enumerate(dates):
        dcode = int(codes[i])
        ddesc, dicon = WEATHER_CODES.get(dcode, ("Weather", "🌤️"))
        try:
            day = datetime.strptime(date, "%Y-%m-%d").strftime("%a, %d %b")
        except ValueError:
            day = date
        days.append({
            "day": "Today" if i == 0 else day, "icon": dicon,
            "max": maxes[i], "min": mins[i], "rain": rains[i] or 0,
            "bar": max(8, min(100, int((maxes[i]-min_low)/spread*100)))
        })
    wind_deg = current.get("wind_direction_10m", 0) or 0
    compass = ["N","NE","E","SE","S","SW","W","NW"][round(wind_deg/45)%8]
    sunrise = daily.get("sunrise", [""])[0][-5:] if daily.get("sunrise") else "—"
    sunset = daily.get("sunset", [""])[0][-5:] if daily.get("sunset") else "—"
    return {
        "name": place.get("name", city), "country": place.get("country", ""),
        "temp": current.get("temperature_2m", 0), "feels": current.get("apparent_temperature", 0),
        "humidity": current.get("relative_humidity_2m", 0), "wind": current.get("wind_speed_10m", 0),
        "wind_dir": compass, "precip": current.get("precipitation", 0),
        "rain": (hourly.get("precipitation_probability", [0])[start] or 0) if hourly.get("precipitation_probability") else 0,
        "description": desc, "icon": icon, "code": code,
        "updated": now.replace("T", " ") if now else "now",
        "hourly": hours, "daily": days, "sunrise": sunrise, "sunset": sunset
    }

@app.route("/")
def home():
    city = (request.args.get("city") or "Khuntuni").strip()[:80]
    places = ["Khuntuni", "Bhubaneswar", "Cuttack", "Burla"]
    try:
        weather = build_weather(city)
        if weather["name"] not in places:
            places.insert(0, weather["name"])
        error = None
    except (requests.RequestException, ValueError, KeyError, IndexError) as exc:
        weather = None
        error = str(exc) if isinstance(exc, ValueError) else "Weather service could not be reached. Check your internet connection and refresh."
    return render_template_string(PAGE, city=city, places=places, weather=weather, error=error)

if __name__ == "__main__":
    print("\n🌌 Atmos Motion is starting!")
    print("Open this address in your browser: http://127.0.0.1:8050")
    app.run(host="127.0.0.1", port=8050, debug=False)
