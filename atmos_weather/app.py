from flask import Flask, request, render_template_string
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime
import json

app = Flask(__name__)

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Atmos — Weather Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#171d34;--panel:#252c49;--panel2:#202741;--line:#ffffff13;--muted:#a4acc8;--white:#f6f7ff;--cyan:#62d9f4;--orange:#ff9c25}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:linear-gradient(135deg,#252b48,#171d34 48%,#202844);color:var(--white);font-family:'DM Sans',sans-serif;min-height:100vh}
.app{display:grid;grid-template-columns:278px minmax(0,1fr);min-height:100vh}.sidebar{background:#1d233bdc;border-right:1px solid #ffffff0c;padding:20px 12px;min-height:100vh}.brand{display:flex;align-items:center;gap:10px;padding:0 10px 23px;font:800 22px Manrope,sans-serif;letter-spacing:-.8px}.brand-icon{width:38px;height:38px;border-radius:13px;background:linear-gradient(135deg,#a1edff,#b7a4ff);color:#202741;display:grid;place-items:center;font-size:23px;box-shadow:0 8px 25px #72c9ff20}.brand span{color:#9deaff}.search{position:relative;margin-bottom:20px}.search input{width:100%;border:1px solid #ffffff12;background:#343b5a;color:white;border-radius:30px;padding:12px 14px 12px 38px;outline:none;font:inherit}.search input:focus{border-color:#8fe6ff88;box-shadow:0 0 0 3px #8fe6ff12}.search .glass{position:absolute;left:14px;top:11px;color:#c3c9df}.places-title{font-size:10px;letter-spacing:1.7px;color:#828cab;font-weight:700;padding:4px 10px 10px}.place{display:block;color:inherit;text-decoration:none;margin:8px 0;padding:13px 12px;border:1px solid #ffffff0e;border-radius:17px;background:#252c45;transition:transform .35s ease,background .35s ease,border-color .35s ease}.place:hover{transform:translateY(-2px);background:#303956;border-color:#ffffff26}.place.active{background:linear-gradient(145deg,#303b5e,#252d49);border-color:#a3e9ff55;box-shadow:0 8px 25px #00012}.place-top{display:flex;justify-content:space-between;gap:8px;align-items:center}.place-name{font-weight:700;font-size:15px}.place-temp{font:500 29px Manrope,sans-serif;letter-spacing:-1.5px}.place-meta{font-size:11px;color:var(--muted);margin-top:2px}.place-bottom{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:#b2bdd7;margin-top:18px}.side-note{color:#7783a4;font-size:11px;line-height:1.6;padding:18px 10px}
main{padding:28px clamp(18px,3vw,42px) 24px;min-width:0;max-width:1600px;width:100%;margin:0 auto}.topbar{display:flex;justify-content:flex-end;align-items:center;margin-bottom:10px}.live{display:inline-flex;align-items:center;gap:8px;border:1px solid #58d7b033;background:#35c9980e;color:#a5f0d2;padding:9px 13px;border-radius:30px;font-size:10px;font-weight:700;letter-spacing:1px}.dot{width:7px;height:7px;border-radius:50%;background:#62e2ae;box-shadow:0 0 10px #62e2ae;animation:pulse 2s infinite}@keyframes pulse{50%{opacity:.4}}
.hero{text-align:center;padding:4px 10px 24px;animation:rise .7s cubic-bezier(.2,.8,.2,1) both}.eyebrow{font-size:10px;letter-spacing:2px;color:#bdc5e0;font-weight:700}.hero-city{font:600 clamp(24px,3vw,34px) Manrope,sans-serif;letter-spacing:-1px;margin-top:4px}.hero-temp{font:300 clamp(62px,7vw,88px)/1.05 Manrope,sans-serif;letter-spacing:-5px;color:#f6f7ff}.hero-condition{font-size:15px}.hero-range{font-size:13px;color:#d2d7e8;margin-top:3px}.hero-icon{font-size:42px;filter:drop-shadow(0 8px 20px #91caff35);margin-bottom:2px;animation:float 6s ease-in-out infinite}@keyframes float{50%{transform:translateY(-5px)}}
.layout{display:grid;grid-template-columns:minmax(145px,.78fr) minmax(260px,1.45fr) minmax(260px,1.65fr);gap:14px;align-items:start}.stack{display:grid;gap:13px;min-width:0}.card{background:linear-gradient(145deg,#2a3150f5,#242b46f5);border:1px solid #ffffff0c;border-radius:21px;box-shadow:0 12px 35px #080d2014;min-width:0;overflow:hidden;transition:transform .35s ease,border-color .35s ease,box-shadow .35s ease}.card:hover{border-color:#ffffff1c;box-shadow:0 15px 34px #080d2026}.small{padding:16px}.card-label{display:flex;align-items:center;gap:7px;color:#8994b3;font-size:10px;letter-spacing:.6px;font-weight:700;text-transform:uppercase}.big-value{font:700 24px Manrope,sans-serif;letter-spacing:-.7px;margin-top:15px}.small-copy{font-size:11px;color:#c2c9df;line-height:1.4;margin-top:2px}.muted{color:var(--muted)}.wind-center{display:grid;place-items:center;margin:12px 0 4px}.compass{width:82px;height:82px;border-radius:50%;border:1px dashed #67718e;position:relative;display:grid;place-items:center;background:radial-gradient(circle,#343d5d,#252c48)}.compass:before{content:'N';position:absolute;top:3px;font-size:9px;color:#b6bfd7}.compass:after{content:'W';position:absolute;left:5px;top:36px;font-size:9px;color:#b6bfd7}.needle{position:absolute;width:2px;height:30px;background:linear-gradient(#f7f7ff 50%,#7d8bab 50%);top:12px;left:39px;transform-origin:bottom center;border-radius:4px}.needle:after{content:'';position:absolute;top:-3px;left:-3px;border-left:4px solid transparent;border-right:4px solid transparent;border-bottom:7px solid #fff}.wind-number{font:700 16px Manrope,sans-serif;text-align:center;z-index:1}.wind-number small{display:block;font:500 10px 'DM Sans',sans-serif;color:#c3cbe1}.wind-foot{font-size:10px;color:#b9c2da;text-align:center;margin-top:7px}.conditions{padding:15px 13px 13px}.section-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:12px}.section-head h2{font:700 15px Manrope,sans-serif;margin:0;letter-spacing:-.3px}.section-sub{font-size:10px;color:#a5afcc}.tabs{display:flex;gap:5px}.tab{font-size:13px;padding:6px 9px;border-radius:20px;background:#ffffff08;color:#aab4d0}.tab.active{background:#ffffff27;color:white}.hours{display:grid;grid-template-columns:repeat(12,minmax(42px,1fr));gap:2px;overflow-x:auto;padding-bottom:4px}.hour{text-align:center;padding:6px 2px;border-radius:12px;transition:background .25s ease,transform .25s ease}.hour:hover{background:#ffffff0b;transform:translateY(-2px)}.hour-time{font-size:10px;font-weight:700;white-space:nowrap;color:#e0e4f1}.hour-icon{font-size:19px;margin:13px 0}.hour-temp{font:700 13px Manrope,sans-serif;white-space:nowrap}.hour-rain{font-size:9px;color:#65d6f4;margin-top:6px;white-space:nowrap}.forecast{padding:15px 15px 8px}.forecast-row{display:grid;grid-template-columns:55px 20px 1fr 78px;align-items:center;gap:8px;padding:12px 0;border-bottom:1px solid #ffffff13}.forecast-row:last-child{border-bottom:0}.forecast-day{font-size:12px;font-weight:700}.forecast-icon{font-size:18px}.rain{font-size:9px;color:#64d9f3;margin-top:3px}.bar{height:5px;border-radius:9px;background:#ffffff0b;position:relative;overflow:hidden}.bar-fill{height:100%;border-radius:9px;background:linear-gradient(90deg,#ffd348,#ff8d20);min-width:8px}.temps{text-align:right;font-size:11px;white-space:nowrap}.temps span{color:#8995b5;margin-left:5px}.sun-card{min-height:142px;position:relative}.sun-path{height:60px;position:relative;margin:10px -2px 0;border-bottom:1px solid #8c98b6;background:radial-gradient(ellipse at 50% 130%,#ffffff13,transparent 55%)}.sun-path:before{content:'';position:absolute;left:8%;right:8%;top:8px;height:55px;border-top:3px solid #8d99bd;border-radius:50% 50% 0 0;opacity:.7}.sun-dot{position:absolute;left:70%;top:23px;width:10px;height:10px;border-radius:50%;background:#ffd35b;box-shadow:0 0 12px #ffbc43}.sun-times{display:flex;justify-content:space-between;font-size:10px;color:#c2c9de;margin-top:8px}.uv-bar{height:5px;border-radius:5px;background:linear-gradient(90deg,#69d99a,#e9df5b,#ff9b42,#eb69d1);margin:15px 0 10px}.map{height:218px;overflow:hidden;background:#252d42}.map iframe{width:100%;height:100%;border:0;filter:grayscale(.7) invert(.86) hue-rotate(180deg) contrast(.82) brightness(.83)}.map-label{position:absolute;left:12px;top:12px;background:#1c2337dd;padding:7px 10px;border-radius:10px;font-size:10px}.map-wrap{position:relative}.bottom-metrics{display:grid;grid-template-columns:1fr 1fr;gap:12px}.error{padding:14px 16px;margin-bottom:14px;background:#8e354533;border:1px solid #ff8a9b55;color:#ffd6dc;border-radius:14px;overflow-wrap:anywhere}.error details{margin-top:7px}.footer{text-align:center;color:#7783a2;font-size:10px;padding:24px 0 6px}.footer b{color:#b4c0de}
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:1100px){.app{grid-template-columns:220px minmax(0,1fr)}main{padding:22px 18px}.layout{grid-template-columns:minmax(130px,.8fr) minmax(230px,1.3fr)}.right-stack{grid-column:1/-1;grid-template-columns:1.2fr 1fr}.hours{grid-template-columns:repeat(12,minmax(45px,1fr))}.map{height:210px}}
@media(max-width:700px){.app{display:block}.sidebar{min-height:0;padding:13px;border-right:0;border-bottom:1px solid #ffffff12}.brand{padding-bottom:13px}.places-title{padding-top:0}.place-list{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px}.place{min-width:145px;margin:0}.side-note{display:none}main{padding:18px 12px}.layout{grid-template-columns:1fr}.left-stack,.right-stack{grid-column:auto;grid-template-columns:repeat(2,minmax(0,1fr))}.conditions{grid-column:1/-1}.forecast{grid-column:1/-1}.hours{grid-template-columns:repeat(12,minmax(45px,1fr))}.map{height:190px}.hero{padding-bottom:18px}.topbar{margin-bottom:4px}.forecast-row{grid-template-columns:50px 20px 1fr 76px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}

/* CINEMATIC MOTION LAYER */
body{background:#080f25;isolation:isolate}
.weather-scene{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none;background:radial-gradient(ellipse at 15% 8%,#244b91 0%,transparent 43%),radial-gradient(ellipse at 92% 78%,#552b88 0%,transparent 42%),linear-gradient(135deg,#101a35,#080f20 62%,#171333)}
.weather-scene:before{content:"";position:absolute;inset:-35%;background:conic-gradient(from 0deg at 50% 50%,transparent 0deg,#74cfff09 55deg,transparent 120deg,#ac8bff0b 205deg,transparent 280deg);filter:blur(36px);animation:skyRotate 55s linear infinite}
.weather-scene:after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,#8fcfff07 48%,transparent 66%);transform:translateX(-100%);animation:lightSweep 16s ease-in-out infinite}
.aurora{position:absolute;width:65vw;height:36vw;left:12%;top:-18%;border-radius:50%;filter:blur(70px);background:linear-gradient(115deg,#42c9f522,#7b5cf022,#45e0d011);animation:auroraFlow 20s ease-in-out infinite alternate}
.cloud-bank{position:absolute;width:68vw;height:28vw;left:-18vw;top:8vh;opacity:.20;filter:blur(27px);background:radial-gradient(ellipse at 22% 60%,#c7d8ff 0 7%,transparent 23%),radial-gradient(ellipse at 42% 40%,#93a9d9 0 13%,transparent 31%),radial-gradient(ellipse at 61% 64%,#b5c5ef 0 12%,transparent 29%),radial-gradient(ellipse at 78% 36%,#7c8dbd 0 10%,transparent 27%);animation:cloudDrift 48s ease-in-out infinite alternate}
.cloud-bank.two{width:55vw;height:22vw;left:auto;right:-22vw;top:48vh;opacity:.13;animation:cloudDriftTwo 58s ease-in-out infinite alternate}
.starfield{position:absolute;inset:0;opacity:.42;background-image:radial-gradient(2px 2px at 12% 22%,#fff 50%,transparent 70%),radial-gradient(1px 1px at 28% 62%,#fff 50%,transparent 70%),radial-gradient(2px 2px at 72% 18%,#d6e7ff 50%,transparent 70%),radial-gradient(1px 1px at 84% 73%,#fff 50%,transparent 70%),radial-gradient(1px 1px at 57% 42%,#fff 50%,transparent 70%),radial-gradient(2px 2px at 42% 83%,#d4e6ff 50%,transparent 70%);animation:starTwinkle 7s ease-in-out infinite alternate}
.lightning-glow{position:absolute;inset:0;background:#9ebdff00;animation:stormFlash 19s linear infinite}
@keyframes skyRotate{to{transform:rotate(360deg)}}
@keyframes lightSweep{0%,65%{transform:translateX(-100%);opacity:0}75%{opacity:1}100%{transform:translateX(100%);opacity:0}}
@keyframes auroraFlow{0%{transform:translate3d(-7%,0,0) rotate(-8deg) scale(.9);opacity:.45}50%{transform:translate3d(8%,9%,0) rotate(8deg) scale(1.12);opacity:.85}100%{transform:translate3d(-1%,14%,0) rotate(-3deg) scale(1.04);opacity:.55}}
@keyframes cloudDrift{from{transform:translate3d(-3vw,0,0) scale(1)}to{transform:translate3d(18vw,5vh,0) scale(1.15)}}
@keyframes cloudDriftTwo{from{transform:translate3d(4vw,0,0) scale(1.1)}to{transform:translate3d(-20vw,-4vh,0) scale(.95)}}
@keyframes starTwinkle{from{opacity:.15}to{opacity:.55}}
@keyframes stormFlash{0%,93%,95%,100%{background:#9ebdff00}94%{background:#9ebdff08}}
.app{position:relative;z-index:1}
.sidebar{backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);background:#171f39c9}
.card,.place{backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);box-shadow:0 10px 35px #03091812,inset 0 1px #ffffff08;transition:transform .65s cubic-bezier(.16,1,.3,1),box-shadow .6s ease,border-color .5s ease,background .5s ease}
.card{animation:cardArrive .9s cubic-bezier(.16,1,.3,1) both}
.layout .stack:nth-child(1) .card:nth-child(1){animation-delay:.08s}
.layout .stack:nth-child(1) .card:nth-child(2){animation-delay:.16s}
.layout .stack:nth-child(1) .card:nth-child(3){animation-delay:.24s}
.center-stack .card:nth-child(1){animation-delay:.14s}
.center-stack .card:nth-child(2){animation-delay:.25s}
.right-stack .card:nth-child(1){animation-delay:.2s}
.right-stack .card:nth-child(2){animation-delay:.3s}
@keyframes cardArrive{from{opacity:0;transform:translateY(22px) scale(.985);filter:blur(5px)}to{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.card:hover{transform:translateY(-5px) scale(1.008);box-shadow:0 22px 50px #03091835,0 0 26px #78caff12;border-color:#a9d8ff30}
.place:hover{transform:translateX(5px);box-shadow:0 12px 28px #0309182b}
.hero{position:relative;animation:heroArrival 1.15s cubic-bezier(.16,1,.3,1) both}
@keyframes heroArrival{from{opacity:0;transform:translateY(30px);filter:blur(8px)}to{opacity:1;transform:translateY(0);filter:blur(0)}}
.hero-icon{display:inline-block;transform-origin:50% 65%;animation:weatherIconFloat 5.5s ease-in-out infinite,iconHalo 4s ease-in-out infinite alternate;filter:drop-shadow(0 8px 25px #8bcaff36)}
@keyframes weatherIconFloat{0%,100%{transform:translateY(0) rotate(-5deg) scale(1)}50%{transform:translateY(-11px) rotate(5deg) scale(1.06)}}
@keyframes iconHalo{from{filter:drop-shadow(0 6px 12px #8bcaff20)}to{filter:drop-shadow(0 8px 28px #8bcaff65)}}
.hero-temp{background:linear-gradient(100deg,#fff 10%,#bdf5ff 42%,#c9bcff 70%,#fff 90%);background-size:220% auto;background-clip:text;-webkit-background-clip:text;color:transparent;animation:temperatureGlow 8s ease-in-out infinite}
@keyframes temperatureGlow{0%,100%{background-position:0% center}50%{background-position:100% center}}
.hour{transition:transform .45s cubic-bezier(.16,1,.3,1),background .4s ease}
.hour:hover{transform:translateY(-6px) scale(1.045);background:#ffffff0c}
.hour-icon{display:inline-block;animation:hourFloat 4s ease-in-out infinite;animation-delay:calc(var(--index,0)*-.32s)}
@keyframes hourFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.forecast-row{transition:background .4s ease,transform .45s cubic-bezier(.16,1,.3,1);border-radius:12px;padding-inline:7px}
.forecast-row:hover{background:#ffffff09;transform:translateX(5px)}
.bar-fill{transform-origin:left center;animation:forecastGrow 1.2s cubic-bezier(.16,1,.3,1) both}
@keyframes forecastGrow{from{transform:scaleX(.02);filter:brightness(1.8)}to{transform:scaleX(1);filter:brightness(1)}}
.compass{transition:box-shadow .5s ease}
.needle{transition:transform 1.4s cubic-bezier(.16,1,.3,1);filter:drop-shadow(0 0 5px #b9e7ff75)}
.card:hover .compass{box-shadow:0 0 28px #8adfff20}
.live{transition:box-shadow .4s ease}
.live:hover{box-shadow:0 0 25px #35c99820}
.dot{animation:pulse 2.4s ease-in-out infinite}
.search input{transition:box-shadow .4s ease,border-color .4s ease}
.search input:focus{box-shadow:0 0 0 4px #7edfff12,0 0 25px #7edfff10}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}

</style>
</head>
<body>
<div class="weather-scene" aria-hidden="true"><div class="aurora"></div><div class="cloud-bank"></div><div class="cloud-bank two"></div><div class="starfield"></div><div class="lightning-glow"></div></div>
<div class="app">
<aside class="sidebar">
  <div class="brand"><div class="brand-icon">☼</div> atmos<span>.</span></div>
  <form class="search" method="get" action="/"><span class="glass">⌕</span><input name="city" value="{{ city|e }}" placeholder="Search a city" aria-label="Search city" required></form>
  <div class="places-title">YOUR PLACES</div>
  <div class="place-list">
    {% for p in places %}<a class="place {% if p.name|lower == city|lower %}active{% endif %}" href="/?city={{ p.query|urlencode }}"><div class="place-top"><div><div class="place-name">{{ p.name }}</div><div class="place-meta">{{ p.condition }}</div></div><div class="place-temp">{{ p.temp }}°</div></div><div class="place-bottom"><span>{{ p.time }}</span><span>H:{{ p.max }}° &nbsp; L:{{ p.min }}°</span></div></a>{% endfor %}
  </div>
  <div class="side-note">Weather data updates automatically every 5 minutes.<br>Search any city or town to explore its forecast.</div>
</aside>
<main>
  <div class="topbar"><div class="live"><span class="dot"></span> LIVE WEATHER</div></div>
  {% if error %}<div class="error">⚠ <b>Weather data could not be loaded.</b><br>{{ error }}</div>{% endif %}
  {% if weather %}
  <section class="hero"><div class="hero-icon">{{ icon }}</div><div class="eyebrow">{{ country|upper }}</div><div class="hero-city">{{ city }}</div><div class="hero-temp">{{ temp|round(0)|int }}°</div><div class="hero-condition">{{ condition }}</div><div class="hero-range">H:{{ today_max|round(0)|int }}° &nbsp; L:{{ today_min|round(0)|int }}°</div></section>
  <div class="layout">
    <div class="stack left-stack">
      <section class="card small"><div class="card-label">⌁ &nbsp; Averages</div><div class="big-value">{{ average_delta }}°</div><div class="small-copy">{{ average_label }}<br>daily high</div><div class="small-copy muted" style="margin-top:14px">Today <span style="float:right;color:#e4e8f5">H:{{ today_max|round(0)|int }}°</span><br>Forecast avg <span style="float:right;color:#e4e8f5">H:{{ average_high|round(0)|int }}°</span></div></section>
      <section class="card small"><div class="card-label">◌ &nbsp; Wind</div><div class="wind-center"><div class="compass"><div class="needle" style="transform:rotate({{ wind_direction }}deg)"></div><div class="wind-number">{{ wind|round(0)|int }}<small>km/h</small></div></div></div><div class="wind-foot">Gusts {{ gusts|round(0)|int }} km/h {{ wind_direction_label }}</div></section>
      <section class="card small"><div class="card-label">☀ &nbsp; UV index</div><div class="big-value">{{ uv|round(0)|int }}</div><div class="small-copy">{{ uv_label }}</div><div class="uv-bar"></div><div class="small-copy muted">Today's maximum UV index.</div></section>
      <section class="card small sun-card"><div class="card-label">☼ &nbsp; Sunrise / sunset</div><div class="big-value" style="font-size:21px">{{ sunrise }}</div><div class="sun-path"><span class="sun-dot"></span></div><div class="sun-times"><span>Sunrise</span><span>Sunset {{ sunset }}</span></div></section>
    </div>
    <div class="stack center-stack">
      <section class="card conditions"><div class="section-head"><h2>Conditions</h2><div class="tabs"><span class="tab active">☁</span><span class="tab">♟</span><span class="tab">≋</span></div></div><div class="section-sub" style="margin:-6px 0 6px">Temperature (°C) · Rain probability</div><div class="hours">
      {% for h in hourly %}<div class="hour"><div class="hour-time">{{ h.time }}</div><div class="hour-icon">{{ h.icon }}</div><div class="hour-temp">{{ h.temp|round(0)|int }}°</div><div class="hour-rain">{{ h.rain }}%</div></div>{% endfor %}
      </div></section>
      <section class="card forecast"><div class="section-head"><h2>7-day forecast</h2><div class="section-sub">Next 7 days</div></div>
      {% for d in daily %}<div class="forecast-row"><div><div class="forecast-day">{{ d.day }}</div><div class="rain">{{ d.rain }}% rain</div></div><div class="forecast-icon">{{ d.icon }}</div><div class="bar"><div class="bar-fill" style="width:{{ d.bar }}%"></div></div><div class="temps">{{ d.max|round(0)|int }}° <span>{{ d.min|round(0)|int }}°</span></div></div>{% endfor %}
      </section>
    </div>
    <div class="stack right-stack">
      <section class="card small"><div class="card-label">☾ &nbsp; Feels like</div><div class="big-value">{{ feels|round(0)|int }}°</div><div class="small-copy" style="margin-top:12px">{{ feel_note }}</div></section>
      <section class="card small"><div class="card-label">◉ &nbsp; Precipitation</div><div class="big-value">{{ precipitation|round(1) }} <span style="font-size:12px;color:#9da9c7">mm</span></div><div class="small-copy">Rain so far today</div><div class="small-copy muted" style="margin-top:12px">Chance now: {{ rain_now }}%</div></section>
      <section class="card"><div class="section-head" style="padding:15px 15px 0;margin-bottom:10px"><h2>Location</h2><div class="section-sub">{{ city }}</div></div><div class="map-wrap"><div class="map"><iframe title="Map showing {{ city }}" loading="lazy" src="{{ map_url }}"></iframe></div><div class="map-label">📍 {{ city }}</div></div></section>
      <div class="bottom-metrics">
        <section class="card small"><div class="card-label">💧 &nbsp; Humidity</div><div class="big-value">{{ humidity }}%</div><div class="small-copy muted" style="margin-top:15px">Relative humidity</div></section>
        <section class="card small"><div class="card-label">◉ &nbsp; Pressure</div><div class="big-value" style="font-size:22px">{{ pressure|round(0)|int }}</div><div class="small-copy">hPa · sea level</div></section>
        <section class="card small"><div class="card-label">◌ &nbsp; Visibility</div><div class="big-value">{{ visibility|round(1) }} <span style="font-size:12px">km</span></div><div class="small-copy muted" style="margin-top:12px">Current visibility</div></section>
        <section class="card small"><div class="card-label">🌧 &nbsp; Rain today</div><div class="big-value">{{ rain_today }}%</div><div class="small-copy muted" style="margin-top:12px">Max chance today</div></section>
      </div>
    </div>
  </div>
  {% endif %}
  <div class="footer">Atmos · Built with <b>Python + Flask</b> · Weather data by Open-Meteo · Refreshes every 5 minutes</div>
</main>
</div>

<script>
(() => {
 const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 document.querySelectorAll('.hour-icon').forEach((el,i)=>el.style.setProperty('--index',i));
 // The page transitions on city search without delaying form submission.
 const form=document.querySelector('.search');
 if(form) form.addEventListener('submit',()=>{
   if(reduced)return;
   document.querySelector('main').style.transition='opacity .18s ease, transform .18s ease';
   document.querySelector('main').style.opacity='.55';
   document.querySelector('main').style.transform='translateY(6px)';
 });
 // Gentle cursor lighting on cards; does not affect layout or weather data.
 if(!reduced && matchMedia('(pointer:fine)').matches){
   document.querySelectorAll('.card').forEach(card=>{
     card.addEventListener('pointermove',e=>{
       const r=card.getBoundingClientRect();
       card.style.backgroundImage=`radial-gradient(260px circle at ${e.clientX-r.left}px ${e.clientY-r.top}px, #9ddcff0b, transparent 72%)`;
     });
     card.addEventListener('pointerleave',()=>card.style.backgroundImage='');
   });
 }
})();
</script>

</body></html>'''


def fetch_json(url, params):
    query = urlencode(params)
    with urlopen(url + "?" + query, timeout=18) as response:
        return json.loads(response.read().decode("utf-8"))


def describe(code):
    mapping = {
        0: ("Clear sky", "☀️"), 1: ("Mainly clear", "🌤️"), 2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"), 45: ("Fog", "🌫️"), 48: ("Freezing fog", "🌫️"),
        51: ("Light drizzle", "🌦️"), 53: ("Drizzle", "🌦️"), 55: ("Heavy drizzle", "🌧️"),
        56: ("Freezing drizzle", "🌧️"), 57: ("Freezing drizzle", "🌧️"), 61: ("Light rain", "🌦️"),
        63: ("Moderate rain", "🌧️"), 65: ("Heavy rain", "🌧️"), 66: ("Freezing rain", "🌧️"),
        67: ("Heavy freezing rain", "🌧️"), 71: ("Light snow", "🌨️"), 73: ("Snow", "❄️"),
        75: ("Heavy snow", "❄️"), 77: ("Snow grains", "🌨️"), 80: ("Rain showers", "🌦️"),
        81: ("Rain showers", "🌧️"), 82: ("Heavy showers", "🌧️"), 85: ("Snow showers", "🌨️"),
        86: ("Heavy snow showers", "❄️"), 95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with hail", "⛈️"), 99: ("Severe thunderstorm", "⛈️")
    }
    return mapping.get(int(code), ("Variable conditions", "🌤️"))


def get_weather(city):
    geo = fetch_json("https://geocoding-api.open-meteo.com/v1/search", {"name": city, "count": 1, "language": "en"})
    results = geo.get("results", [])
    if not results:
        raise ValueError("City or town not found. Check the spelling and try again.")
    place = results[0]
    data = fetch_json("https://api.open-meteo.com/v1/forecast", {
        "latitude": place["latitude"], "longitude": place["longitude"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl",
        "hourly": "temperature_2m,precipitation_probability,weather_code,wind_speed_10m,visibility",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset,uv_index_max,wind_gusts_10m_max",
        "forecast_days": 7, "timezone": "auto"
    })
    return place, data


def safe_time(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M").strftime("%-I:%M %p")
    except (ValueError, TypeError):
        return "—"


def dashboard(city):
    place, data = get_weather(city)
    current, hours, days = data["current"], data["hourly"], data["daily"]
    condition, icon = describe(current["weather_code"])
    current_hour = current["time"][:13]
    start = next((i for i, t in enumerate(hours["time"]) if t[:13] >= current_hour), 0)
    hourly = []
    for i in range(start, min(start + 12, len(hours["time"]))):
        _, hi = describe(hours["weather_code"][i])
        hourly.append({"time": safe_time(hours["time"][i]).replace(" AM", "a").replace(" PM", "p"),
                       "temp": hours["temperature_2m"][i], "rain": hours["precipitation_probability"][i] or 0, "icon": hi})
    daily = []
    maxes = [v for v in days["temperature_2m_max"] if v is not None]
    average_high = sum(maxes) / len(maxes) if maxes else 0
    for i, date in enumerate(days["time"]):
        desc, di = describe(days["weather_code"][i])
        day_label = "Today" if i == 0 else datetime.strptime(date, "%Y-%m-%d").strftime("%a")
        rain = days["precipitation_probability_max"][i] or 0
        daily.append({"day": day_label, "icon": di, "condition": desc, "max": days["temperature_2m_max"][i],
                      "min": days["temperature_2m_min"][i], "rain": rain,
                      "bar": max(8, min(100, int((days["temperature_2m_max"][i] or 0) / max(max(maxes, default=1), 1) * 100)))})
    uv = days.get("uv_index_max", [0])[0] or 0
    uv_label = "Low" if uv < 3 else "Moderate" if uv < 6 else "High" if uv < 8 else "Very high" if uv < 11 else "Extreme"
    wind = current.get("wind_speed_10m") or 0
    direction = current.get("wind_direction_10m") or 0
    direction_label = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")[round(direction / 45) % 8]
    lat, lon = place["latitude"], place["longitude"]
    bbox = f"{lon-0.12}%2C{lat-0.08}%2C{lon+0.12}%2C{lat+0.08}"
    map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}&layer=mapnik&marker={lat}%2C{lon}"
    feels = current.get("apparent_temperature") or current.get("temperature_2m") or 0
    temp = current.get("temperature_2m") or 0
    feel_note = "It feels warmer than the actual temperature." if feels > temp + 1 else "It feels cooler than the actual temperature." if feels < temp - 1 else "Feels close to the actual temperature."
    # Sidebar places are shortcuts; only the selected city's measurements are displayed to avoid inventing data.
    shortcuts = []
    for name in [place["name"], "Khuntuni", "Burla", "Bhubaneswar"]:
        if not any(x["name"].lower() == name.lower() for x in shortcuts):
            shortcuts.append({"name": name, "query": name, "condition": condition if name.lower() == place["name"].lower() else "Search forecast",
                              "temp": round(temp) if name.lower() == place["name"].lower() else "—",
                              "time": "Now" if name.lower() == place["name"].lower() else "Open city",
                              "max": round(days["temperature_2m_max"][0]) if name.lower() == place["name"].lower() else "—",
                              "min": round(days["temperature_2m_min"][0]) if name.lower() == place["name"].lower() else "—"})
    return dict(city=place["name"], country=place.get("country", "India"), weather=True, condition=condition, icon=icon,
                temp=temp, feels=feels, feel_note=feel_note, humidity=current.get("relative_humidity_2m") or 0,
                wind=wind, wind_direction=direction, wind_direction_label=direction_label,
                gusts=days.get("wind_gusts_10m_max", [wind])[0] or wind,
                precipitation=current.get("precipitation") or 0,
                rain_now=hours["precipitation_probability"][start] or 0,
                rain_today=days["precipitation_probability_max"][0] or 0,
                pressure=current.get("pressure_msl") or 0,
                visibility=(hours.get("visibility", [0])[start] or 0) / 1000,
                uv=uv, uv_label=uv_label,
                sunrise=safe_time(days.get("sunrise", [""])[0]), sunset=safe_time(days.get("sunset", [""])[0]),
                today_max=days["temperature_2m_max"][0] or 0, today_min=days["temperature_2m_min"][0] or 0,
                average_high=average_high, average_delta=round((days["temperature_2m_max"][0] or 0)-average_high),
                average_label="above" if (days["temperature_2m_max"][0] or 0) >= average_high else "below",
                hourly=hourly, daily=daily, places=shortcuts, map_url=map_url)


@app.route("/")
def home():
    city = request.args.get("city", "Khuntuni").strip() or "Khuntuni"
    try:
        values = dashboard(city)
        return render_template_string(PAGE, error="", **values)
    except Exception as exc:
        return render_template_string(PAGE, city=city, weather=False, places=[], error=str(exc)), 502


if __name__ == "__main__":
    print("\nAtmos Weather Dashboard is starting")
    print("Open http://127.0.0.1:8001 in your browser\n")
    app.run(host="127.0.0.1", port=8001, debug=False)
