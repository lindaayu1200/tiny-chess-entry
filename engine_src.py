import os,sys,json,urllib.request
from collections import namedtuple
MATE=60000
HTTP=os.environ.get('MAKEFUN_ENV_URL','http://localhost:8080')
Position=namedtuple('Position','board score wc bc ep kp')
values={'P':100,'N':280,'B':320,'R':479,'Q':929,'K':MATE}
tbl={}
P=(0,0,0,0,0,0,0,0,78,83,86,73,99,82,85,90,7,29,21,44,40,31,44,7,-17,16,-2,15,14,0,15,-13,-26,3,10,9,6,1,0,-23,-22,9,5,-11,-10,-2,3,-19,-31,8,-7,-37,-36,-14,3,-31,0,0,0,0,0,0,0,0)
N=(-66,-53,-75,-75,-10,-55,-58,-70,-3,-6,100,-36,4,62,-4,-14,10,67,1,74,73,27,62,-2,24,24,45,37,33,41,25,17,-1,5,31,21,22,35,2,0,-18,10,13,22,18,15,11,-14,-23,-15,2,0,2,0,-23,-20,-74,-23,-26,-24,-19,-35,-22,-69)
B=(-59,-78,-82,-76,-23,-99,-37,-50,-11,20,35,-42,-39,31,2,-22,-9,39,-32,41,52,-10,28,-14,25,17,20,34,26,25,15,10,13,10,17,23,17,16,0,7,14,25,24,15,8,25,20,15,19,20,11,6,7,6,20,16,-7,2,-15,-12,-14,-15,-10,-10)
R=(35,29,33,4,37,33,56,50,55,29,56,67,55,62,34,60,19,35,28,33,45,27,25,15,0,5,16,13,18,-4,-9,-6,-28,-35,-16,-21,-13,-29,-46,-30,-42,-28,-42,-25,-25,-35,-26,-46,-53,-38,-31,-26,-29,-43,-44,-53,-30,-24,-18,5,-2,-18,-31,-32)
Q=(6,1,-8,-99,69,24,88,26,14,32,60,-10,20,76,57,24,-2,43,32,60,72,63,43,2,1,-16,22,17,25,20,-13,-6,-14,-15,-2,-5,-1,-10,-20,-22,-30,-6,-13,-11,-16,-11,-16,-27,-36,-18,0,-19,-15,-15,-21,-38,-39,-30,-31,-13,-31,-36,-34,-42)
K=(4,54,47,-99,-99,60,83,-62,-32,10,55,56,56,55,10,3,-62,12,-57,44,-67,28,37,-31,-55,50,11,-4,-19,13,0,-49,-55,-43,-52,-28,-51,-47,-8,-50,-47,-42,-43,-79,-64,-32,-29,-32,-4,3,-14,-50,-57,-18,13,4,17,30,-3,-14,6,-1,40,18)
for n,q in zip('PNBRQK',(P,N,B,R,Q,K)):
 t=(0,)*20
 for i in range(0,64,8):t+=(0,)+q[i:i+8]+(0,)
 tbl[n]=tuple(x+values[n] for x in t+(0,)*20)
start=' '*20+''.join(' '+r+' ' for r in ('rnbqkbnr','pppppppp','........','........','........','........','PPPPPPPP','RNBQKBNR'))+' '*20
kq=(-11,-9,9,11,-10,-1,1,10)
piece_dirs={'N':(-21,-19,-12,-8,8,12,19,21),'B':(-11,-9,9,11),'R':(-10,-1,1,10),'Q':kq,'K':kq,'P':(-10,-20,-9,-11)}
def score(p):
 s=0;b=p.board
 for i,c in enumerate(b):
  if c in ' .\n':continue
  s+=tbl[c][i] if c.isupper() else -tbl[c.upper()][119-i]
 return s
def onb(j):return 21<=j<=98 and 1<=j%10<=8
def attacked(b,j,u):
 for d in ((9,11) if u else (-9,-11)):
  s=j+d
  if onb(s) and b[s]==('P' if u else 'p'):return 1
 for p in 'NK':
  q=p if u else p.lower()
  for d in piece_dirs[p]:
   s=j+d
   if onb(s) and b[s]==q:return 1
 for p in 'BRQ':
  q=p if u else p.lower()
  for d in piece_dirs[p]:
   s=j+d
   while onb(s) and b[s]=='.':s+=d
   if onb(s) and b[s]==q:return 1
 return 0
def gm(p):
 b=p.board;wc,ep=p.wc,p.ep
 for i,x in enumerate(b):
  if x not in 'PNBRQK':continue
  if x=='P':
   j=i-10
   if onb(j) and b[j]=='.':
    if 21<=j<=28:
     for q in 'QRBN':yield i,j,q
    else:yield i,j,''
    j2=i-20
    if 81<=i<=88 and onb(j2) and b[j2]=='.':yield i,j2,''
   for d in (-9,-11):
    j=i+d
    if onb(j) and b[j].islower():
     if 21<=j<=28:
      for q in 'QRBN':yield i,j,q
     else:yield i,j,''
   if ep and (i-9==ep or i-11==ep) and onb(ep) and b[ep+10].islower():yield i,ep,''
  else:
   for d in piece_dirs[x]:
    j=i+d
    while onb(j) and b[j]=='.':
     yield i,j,''
     if x in 'NK':break
     j+=d
    if onb(j) and b[j].islower():yield i,j,''
 if b[95]=='K':
  if wc[1] and b[91]=='R' and b[92:95]=='...' and not any(attacked(b,s,0) for s in (95,94,93)):yield 95,93,''
  if wc[0] and b[98]=='R' and b[96:98]=='..' and not any(attacked(b,s,0) for s in (95,96,97)):yield 95,97,''
 elif b[94]=='K':
  if wc[0] and b[91]=='R' and b[92:94]=='..' and not any(attacked(b,s,0) for s in (94,93,92)):yield 94,92,''
  if wc[1] and b[98]=='R' and b[95:98]=='...' and not any(attacked(b,s,0) for s in (94,95,96)):yield 94,96,''
def ck(p):return any(p.board[m[1]]=='k' for m in gm(p))
def apply(p,m):
 i,j,q=m;b=list(p.board);x=b[i]
 if x=='K' and abs(j-i)==2:
  if i==95:
   if j>i:b[96],b[98]='R','.'
   else:b[94],b[91]='R','.'
  elif j>i:b[95],b[98]='R','.'
  else:b[93],b[91]='R','.'
 b[i]='.';b[j]=q or x
 if x=='P' and j==p.kp:b[j+10]='.'
 kp=(i+j)//2 if x=='P' and abs(j-i)==20 else 0
 wc=p.wc
 if x=='K' and i in (95,94):wc=(0,0)
 elif i==91 or j==91:wc=(wc[0],0)
 elif i==98 or j==98:wc=(0,wc[1])
 val=tbl[x][j]-tbl[x][i]
 if p.board[j]!='.':val+=values[p.board[j].upper()]
 if x=='P' and j==p.kp:val+=100
 if q:val+=values[q]-100
 if x=='K' and abs(j-i)==2:
  if j>i:val+=tbl['R'][j-1]-tbl['R'][j+1]
  else:val+=tbl['R'][j+1]-tbl['R'][j-2]
 ns=-(p.score+val);nb=''.join(b)[::-1].swapcase()
 return Position(nb,ns,p.bc,wc,0,119-kp if kp else 0)
def gen_all(p):
 for m in gm(p):
  c=apply(p,m)
  if not ck(c):yield m,c
class Timeout(Exception):pass
ML=50710;MU=69290;ER=9;LRM=64
def nullmove(p):return Position(p.board[::-1].swapcase(),-p.score,p.bc,p.wc,0,0)
class Searcher:
 def __init__(s):s.ts={};s.tm={};s.history=set();s.nodes=0;s.total=0;s.t0=0
 def ev(s,t,n):
  if len(t)>n:t.pop(next(iter(t)))
 def bound(s,p,g,d,root=0):
  s.nodes+=1
  if s.nodes%2048==0 and s.total+s.nodes>119999:raise Timeout
  if d<0:d=0
  if p.score<=-ML:return -MU
  k=(p,d,root);e=s.ts.get(k);lo,hi=e or (-MU,MU)
  if lo>=g:return lo
  if hi<g:return hi
  if d>0 and p in s.history and not root:return 0
  cm=abs(p.score)<750 and any(c in p.board for c in 'RBNQ')
  gd=(not root)and cm
  tt=s.tm.get(p)
  st=[-MU,None]
  def rec(m,sc):
   if sc>st[0]:st[0]=sc;st[1]=m
  if 2<d<6 and gd:rec(None,min(p.score+ER,-s.bound(nullmove(p),1-g,d-3)))
  if d==0:rec(None,p.score)
  if tt and (d>0 or p.board[tt[1]]!='.' or tt[2]):rec(tt,-s.bound(apply(p,tt),1-g,d-1))
  q=st[0]>=g
  for m in sorted(gm(p),key=lambda m:s.value(p,m),reverse=True):
   if q:break
   if m==tt:continue
   v=s.value(p,m)
   if d>0 or p.board[m[1]]!='.' or m[2]:
    if d==0 and v+p.score+9<g:break
    r=1 if(gd and d>=7 and v<LRM)else 0
    rec(m,-s.bound(apply(p,m),1-g,d-1-r))
    if st[0]>=g:
     if m and d:
      s.tm[p]=m
      s.ev(s.tm,999)
      q=True
  best=st[0]
  if best<g and best<0 and d>0:
   dead=lambda q:any(s.value(q,x)>=ML for x in gm(q))
   if all(dead(apply(p,x)) for x in gm(p)):
    best=-MU if dead(nullmove(p)) else 0
  s.ts[k]=(best,hi) if best>=g else (lo,best)
  s.ev(s.ts,9999)
  return best
 def value(s,p,m):
  i,j,q=m;x=p.board[i];t=p.board[j]
  v=tbl[x][j]-tbl[x][i]
  if x=='P' and j==p.kp:v+=100
  elif t.islower():v+=values[t.upper()]
  if q:v+=values[q]-100
  return v
 def search(s,pos,h):
  s.history=set(h);s.total=0;s.nodes=0;pv=0
  for d in range(1,1000):
   lo,hi=-MU,MU;rm=None
   if d>1:
    s.total+=s.nodes;s.nodes=0
    try:sc=s.bound(pos,pv,d,root=1)
    except Timeout:return
    if sc>=pv:lo=sc;rm=s.tm.get(pos)
    if sc<pv:hi=sc
   while lo<hi-ER:
    g=(lo+hi+1)//2
    s.total+=s.nodes;s.nodes=0
    try:sc=s.bound(pos,g,d,root=1)
    except Timeout:return
    if sc>=g:lo=sc
    if sc<g:hi=sc
   pv=lo
   yield d,s.tm.get(pos) or rm,lo
   if abs(lo)>=MU-100 or s.total>119999:return
def legal_moves(p):return [m for m in gm(p) if not ck(apply(p,m))]
def parse_fen(f):
 a=f.split();rows=[]
 for r in a[0].split('/'):
  line=' '
  for c in r:line+='.'*int(c) if c.isdigit() else c
  rows.append(line+' ')
 b=' '*20+''.join(rows)+' '*20
 ca=a[2] if len(a)>2 else '-';ep=a[3] if len(a)>3 else '-'
 wc=('K' in ca,'Q' in ca);bc=('k' in ca,'q' in ca)
 p=Position(b,0,wc,bc,0,0);p=Position(b,score(p),wc,bc,0,0)
 if ep!='-' and len(ep)==2:
  i=(10-int(ep[1]))*10+ord(ep[0])-96
  p=Position(b,p.score,wc,bc,0,i)
 if len(a)>1 and a[1]=='b':p=Position(b[::-1].swapcase(),-p.score,bc,wc,0,119-p.kp if p.kp else 0)
 return p
def square_name(i):return 'abcdefgh'[i%10-1]+str(8-(i//10-2))
def parse_square(n):return (10-int(n[1]))*10+ord(n[0])-96
def move_to_uci(m,f):
 i,j,q=m
 if f:i,j=119-i,119-j
 return square_name(i)+square_name(j)+q.lower()
def uci_to_move(u,f):
 i=parse_square(u[:2]);j=parse_square(u[2:4]);q=u[4:].upper()
 if f:i,j=119-i,119-j
 return i,j,q
def post(path,payload):
 q=urllib.request.Request(HTTP+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(q) as r:return json.loads(r.read())
 except urllib.error.HTTPError as e:
  if e.code==400:return {}
  raise
def main():
 if '--selftest' in sys.argv:
  p=parse_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -')
  assert len(legal_moves(p))==20
  m=parse_fen('7k/5Q2/5K2/8/8/8/8/8 w - - 0 1')
  assert any(v[2]>=MATE-100 for v in Searcher().search(m,[m]))
  print('OK');sys.exit(0)
 gid=-1;pl=-1;S=None
 while 1:
  r=post('/game',{})
  if r.get('status')=='done':print('GAME DONE',r);break
  if r.get('status')!='your_move':continue
  key=(r.get('game'),r.get('plies'))
  if key==(gid,pl):
   post('/resign',{'game':r.get('game',0)});continue
  if r.get('game')!=gid:S=None
  mv=r.get('moves',[]);legal=r.get('legal_moves',[])
  if not legal:continue
  try:
   h=[];p=parse_fen(r['start_fen'])
   for k,u in enumerate(mv):
    p=apply(p,uci_to_move(u,k%2));h.append(p)
   fl=len(mv)%2==1
   fen=r.get('fen','')
   if fen:fl=fen.split()[1]=='b';p=parse_fen(fen)
   h.append(p)
   if S is None:S=Searcher()
   s=S;s.history=set(h);best=None
   try:
    for d,m,sc in s.search(p,h):best=m
   except Exception:pass
   lm=[uci_to_move(u,fl) for u in legal]
   if best not in lm:
    best=lm[0]
    for m in lm:
     try:
      if not ck(apply(p,m)):best=m;break
     except Exception:pass
   u=move_to_uci(best,fl)
  except Exception:u=legal[0]
  if u not in legal:u=legal[0]
  gid,pl=key
  post('/move',{'game':gid,'move':u})
if __name__=='__main__':main()
