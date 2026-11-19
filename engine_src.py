import os,sys,json,urllib.request
from collections import namedtuple
MATE=60000;INF=40000;A0,A1=40,140
HTTP=os.environ.get('HTTP_URL','http://localhost:8000')
Position=namedtuple('Position','board score wc bc ep kp')
values={'P':100,'N':280,'B':320,'R':479,'Q':929,'K':MATE}
tbl={}
P=(0,0,0,0,0,0,0,0,78,83,86,73,102,82,85,90,7,29,21,44,40,31,44,7,-17,16,-2,15,14,0,15,-13,-26,3,10,9,6,1,0,-23,-22,9,5,-11,-10,-2,3,-19,-31,8,-7,-37,-36,-14,3,-31,0,0,0,0,0,0,0,0)
N=(-66,-53,-75,-75,-10,-55,-58,-70,-3,-6,100,-36,4,62,-4,-14,10,67,1,74,73,27,62,-2,24,24,45,37,33,41,25,17,-1,5,31,21,22,35,2,0,-18,10,13,22,18,15,11,-14,-23,-15,2,0,2,0,-23,-20,-74,-23,-26,-24,-19,-35,-22,-69)
B=(-59,-78,-82,-76,-23,-107,-37,-50,-11,20,35,-42,-39,31,2,-22,-9,39,-32,41,52,-10,28,-14,25,17,20,34,26,25,15,10,13,10,17,23,17,16,0,7,14,25,24,15,8,25,20,15,19,20,11,6,7,6,20,16,-7,2,-15,-12,-14,-15,-10,-10)
R=(35,29,33,4,37,33,56,50,55,29,56,67,55,62,34,60,19,35,28,33,45,27,25,15,0,5,16,13,18,-4,-9,-6,-28,-35,-16,-21,-13,-29,-46,-30,-42,-28,-42,-25,-25,-35,-26,-46,-53,-38,-31,-26,-29,-43,-44,-53,-30,-24,-18,5,-2,-18,-31,-32)
Q=(6,1,-8,-104,69,24,88,26,14,32,60,-10,20,76,57,24,-2,43,32,60,72,63,43,2,1,-16,22,17,25,20,-13,-6,-14,-15,-2,-5,-1,-10,-20,-22,-30,-6,-13,-11,-16,-11,-16,-27,-36,-18,0,-19,-15,-15,-21,-38,-39,-30,-31,-13,-31,-36,-34,-42)
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
def gen_moves(p):
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
def can_capture_king(p):return any(p.board[m[1]]=='k' for m in gen_moves(p))
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
 if x=='P' and j==p.kp:val+=100
 if q:val+=values[q]-100
 if x=='K' and abs(j-i)==2:
  if j>i:val+=tbl['R'][j-1]-tbl['R'][j+1]
  else:val+=tbl['R'][j+1]-tbl['R'][j-2]
 ns=-(p.score-val);nb=''.join(b)[::-1].swapcase()
 return Position(nb,ns,p.bc,wc,0,119-kp if kp else 0)
def gen_all(p):
 for m in gen_moves(p):
  c=apply(p,m)
  if not can_capture_king(c):yield m,c
class Timeout(Exception):pass
class Searcher:
 def __init__(s):s.tp_score={};s.tp_move={};s.history=set();s.nodes=0
 def bound(s,p,g,d,root=0):
  s.nodes+=1
  if s.nodes%2048==0 and s.nodes>50000:raise Timeout
  if p.score<=-MATE:return -g
  k=(p,d,root);e=s.tp_score.get(k)
  if e:
   lo,hi=e
   if lo>=g:return lo
   if hi<g:return hi
  if d>0 and p in s.history and not root:return 0
  ms=[]
  if d>2 and not root and abs(p.score)<500:
   np=Position(p.board[::-1].swapcase(),-p.score,p.bc,p.wc,0,119-p.kp if p.kp else 0)
   v=-s.bound(np,1-g,d-3)
   if v>=g:ms.append((None,v))
  if d==0:
   for m in gen_moves(p):
    if not can_capture_king(apply(p,m)):break
   else:
    q=p.board.find('K')
    if q>=0 and attacked(p.board,q,0):return -MATE
   ms.append((None,p.score))
  else:
   if d>2:
    s.bound(p,g,d-3);tt=s.tp_move.get(p)
   else:tt=None
   lo=A0-d*A1
   if tt and s.value(p,tt)>=lo:ms.append((tt,-s.bound(apply(p,tt),1-g,d-1)))
   g2=[(m,s.value(p,m)) for m,_ in gen_all(p)]
   g2.sort(key=lambda x:-x[1])
   for m,v in g2:
    if tt and m==tt:continue
    if d<=1 and not root and p.score+v<g:
     ms.append((None,p.score+v if v>=0 else p.score));break
    c=apply(p,m)
    if c in s.history:continue
    if m[1]==p.kp or m[2]:mv=-s.bound(c,1-g,d-1)
    elif d>=2 and v>=lo and p.score+v>=g:mv=-s.bound(c,1-g,d-2)
    else:mv=-s.bound(c,1-g,d-1)
    ms.append((m,mv))
  best=-INF;bm=None;ab=1
  for m,v in ms:
   if v>best:best=v;bm=m
   if m is not None:ab=0
   if best>=g and not root:break
  if bm is not None and best>=g:s.tp_move[p]=bm
  if d and ab:
   best=0
   if not any(not can_capture_king(apply(p,m)) for m in gen_moves(p)):
    q=p.board.find('K')
    if q>=0 and attacked(p.board,q,0):best=-MATE
  s.tp_score[k]=(best,best)
  return best
 def value(s,p,m):
  i,j,q=m;x=p.board[i];t=p.board[j]
  v=tbl[x][j]-tbl[x][i]
  if x=='P' and j==p.kp:v+=100
  elif t.islower():v+=values[t.upper()]
  if q:v+=values[q]-100
  return v
 def search(s,h):
  s.history=set(h);s.nodes=0;r=h[-1];g=0
  for d in range(1,1000):
   lo,hi=-INF,INF
   while lo<hi:
    s.nodes=0
    try:sc=s.bound(r,g,d,root=1)
    except Timeout:return
    if sc>=g:lo=sc
    else:hi=sc
    g=(lo+hi+1)//2 if lo<hi else lo
    if g<=-INF or g>=INF:break
   g=lo;b=s.tp_move.get(r,(0,0,''))
   yield d,g,b
   if abs(g)>=MATE-100:return
def perft(p,d):
 if not d:return 1
 n=0
 for m in gen_moves(p):
  c=apply(p,m)
  if not can_capture_king(c):n+=perft(c,d-1)
 return n
def legal_moves(p):return [m for m in gen_moves(p) if not can_capture_king(apply(p,m))]
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
def parse_square(n):return (9-int(n[1]))*10+ord(n[0])-96
def move_to_uci(m,f):
 i,j,q=m
 if f:i,j=119-i,119-j
 return square_name(i)+square_name(j)+q
def uci_to_move(u,f):
 i=parse_square(u[:2]);j=parse_square(u[2:4]);q=u[4:]
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
  assert (perft(p,1),perft(p,2),perft(p,3))==(20,400,8902)
  m=parse_fen('7k/5Q2/5K2/8/8/8/8/8 w - - 0 1')
  assert next(Searcher().search([m]))[1]>=MATE-100
  st=parse_fen('7k/5Q2/6K1/8/8/8/8/8 b - - 0 1')
  assert next(Searcher().search([st]))[1]==0
  print('OK');sys.exit(0)
 gid=None
 while 1:
  r=post('/game',{})
  if r.get('status')=='done':print('GAME DONE',r);break
  if r.get('status')!='your_move':continue
  sf=r.get('start_fen');mv=r.get('moves',[])
  if gid!=r.get('game_id'):gid=r.get('game_id')
  p=parse_fen(sf);h=[p]
  for u in mv:p=apply(p,uci_to_move(u,0));h.append(p)
  s=Searcher();s.history=set(h);legal=r.get('legal_moves',[]);best=None
  try:
   for d,sc,m in s.search(h):best=m;break
  except Exception:pass
  if best is None:best=uci_to_move(legal[0],0)
  u=move_to_uci(best,len(mv)%2==1)
  if u not in legal:u=legal[0]
  post('/move',{'game_id':gid,'move':u})
  h.append(apply(p,best))
if __name__=='__main__':main()
