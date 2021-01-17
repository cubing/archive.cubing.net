from mod_python import apache
from time import localtime
import re

def handlehi(req, **args):
	reloadConstants()
	
	global UC, UPC, U2C, uC, uPC, u2C
	global DC, DPC, D2C, dC, dPC, d2C
	global FC, FPC, F2C, fC, fPC, f2C
	global BC, BPC, B2C, bC, bPC, b2C
	global RC, RPC, R2C, rC, rPC, r2C
	global XC, YC, ZC, XPC, YPC, ZPC, X2C, Y2C, Z2C
	global SGC, RGC, maxRots, lpenalty
	
	#save this search
	f=open("C:/wamp/www/cgitests/logfile.txt", "a")
	f.write(`localtime()[0:5]` + "|" + req.connection.remote_ip + "|" + `args` + "\n")
	f.close()
	
	req.content_type = 'text/html'
	str = open('C:/wamp/www/cgitests/theform.html', 'r').read() #its missing /body /html
	
	try:
		UC = float(args.get("UC", UC))
		UPC = float(args.get("UPC", UPC))
		U2C = float(args.get("U2C", U2C))
		uC = float(args.get("uC", uC))
		uPC = float(args.get("uPC", uPC))
		u2C = float(args.get("u2C", u2C))
		DC = float(args.get("DC", DC))
		DPC = float(args.get("DPC", DPC))
		D2C = float(args.get("D2C", D2C))
		dC = float(args.get("dC", dC))
		dPC = float(args.get("dPC", dPC))
		d2C = float(args.get("d2C", d2C))
		FC = float(args.get("FC", FC))
		FPC = float(args.get("FPC", FPC))
		F2C = float(args.get("F2C", F2C))
		fC = float(args.get("fC", fC))
		fPC = float(args.get("fPC", fPC))
		f2C = float(args.get("f2C", f2C))
		BC = float(args.get("BC", BC))
		BPC = float(args.get("BPC", BPC))
		B2C = float(args.get("B2C", B2C))
		bC = float(args.get("bC", bC))
		bPC = float(args.get("bPC", bPC))
		b2C = float(args.get("b2C", b2C))
		RC = float(args.get("RC", RC))
		RPC = float(args.get("RPC", RPC))
		R2C = float(args.get("R2C", R2C))
		rC = float(args.get("rC", rC))
		rPC = float(args.get("rPC", rPC))
		r2C = float(args.get("r2C", r2C))
		XC = float(args.get("XC", XC))
		YC = float(args.get("YC", YC))
		ZC = float(args.get("ZC", ZC))
		XPC = float(args.get("XPC", XPC))
		YPC = float(args.get("YPC", YPC))
		ZPC = float(args.get("ZPC", ZPC))
		X2C = float(args.get("X2C", X2C))
		Y2C = float(args.get("Y2C", Y2C))
		Z2C = float(args.get("Z2C", Z2C))
		RGC = float(args.get("RGC", RGC))
		SGC = float(args.get("SGC", SGC))
		maxRots = int(float(args.get("maxRots", maxRots)))
	except:
		return "Use numbers in those text fields, retard."
		
	algg=args.get("alg", "").strip()
	algg = algg.replace("(", "")
	algg = algg.replace(")", "")
	algg = algg.replace("]", "")
	algg = algg.replace("[", "")
	algg = algg.replace("2'", "2")
	algg = algg.replace("'2", "2") #damn you bob burton!
	algg = algg.replace("  ", " ")
	alglength=len(algg.split())
	
	regexstr="^([UDFBRL]['2]? )*([UDFBRL]['2]?)?$"
	if re.match(regexstr, algg) == None and algg!="":
		return "Your alg is not well formed. It has to composed of only RUFLDB letters and have spaces in between letters! (for programmers: The regex expression is: ([UDFBRL]['2]? )*)"
	
	if alglength > 18:
		return "OK do you really expect my crappy home computer to process your " + `alglength` + " moves long algorithm?"
		
	if maxRots > 5 or (alglength > 15 and maxRots>4):
		return `maxRots` + " depth????!!! are you serious? No can do man. Seriously my poor 2 Ghz PC with 256 RAM in my living room just cant do that... im sorrey"
		
	str = str.replace("name=\"alg\"", "name=\"%s\" value=\"%s\"" % ("alg", algg))
	#now put them all into the HTML form
	moves = "UC UPC U2C uC uPC u2C DC DPC D2C dC dPC d2C FC FPC F2C fC fPC f2C BC BPC B2C bC bPC b2C RC RPC R2C rC rPC r2C XC YC ZC XPC YPC ZPC X2C Y2C Z2C RGC SGC maxRots".split()
	for move in moves:
		try:
			str = str.replace("name=\"" + move + "\"", "name=\"%s\" value=\"%.2f\"" % (move, eval(move)))
		except:
			str = str.replace("name=\"" + move + "\"", "name=\"%s\" value=\"%.2f\"" % (move, float(eval(move))))
	
	if args.has_key('alg'):
		#algorithm was supplied!
		if args['alg'] != "":
			
			isok = True
			for k in "wxyzfbrlud":
				if k in algg:
					isok = False
					break
			
			if not isok:
				str += "CUBE ROTATIONS / DOUBLE LAYER TURNS IN ALG ARE NOT YET SUPPORTED!!!"
			else:
				str += "<br>" + produceTable(algg)
	
	str += "</body></html>"
	
	return str
	
def reloadConstants():
	global UC, UPC, U2C, uC, uPC, u2C
	global DC, DPC, D2C, dC, dPC, d2C
	global FC, FPC, F2C, fC, fPC, f2C
	global BC, BPC, B2C, bC, bPC, b2C
	global RC, RPC, R2C, rC, rPC, r2C
	global XC, YC, ZC, XPC, YPC, ZPC, X2C, Y2C, Z2C
	global SGC, RGC, maxRots,lpenalty
	
	#from constants import *
	UC = 0.08 #U FLICK COST
	UPC = 0.07 #U' FLICK COST
	U2C = 0.15 #U2 FLICK COST
	RC = 0.06
	RPC = 0.06
	R2C = 0.12
	FC = 0.1
	FPC = 0.19
	F2C = 0.3
	DC = 0.12
	D2C = 0.4
	DPC = 0.15
	BC = 0.15
	B2C = 0.45
	BPC = 0.35

	uC = UC
	uPC = UPC
	u2C = U2C
	rC = RC
	rPC = RPC
	r2C = R2C
	fC = FC + 0.01
	fPC = FPC + 0.01
	f2C = F2C + 0.01
	dC = DC + 0.2
	d2C = D2C + 0.1
	dPC = DPC + 0.2
	bC = BC + 0.05
	b2C = B2C + 0.04
	bPC = BPC + 0.05

	#special costs
	SGC = 0.2 #switch grip from one hand to another cost
	RGC = 0.2 #REGRIP COST
	lpenalty = 0.05 #penalty per turn of using left hand

	#rotation costs
	YC = 0.25
	YPC = 0.25
	Y2C = 0.35
	XC = 0.25
	XPC = 0.25
	X2C = 0.4
	ZC = 0.25
	ZPC = 0.27
	Z2C = 0.35


#doesnt rly belong here but whatever
#mirror alg by F face times times. We have to mirror alg if we switched hands
def mirrorF(alg, times=1):
    if times%2 == 0: #algorithm mirror twice is just it 
        return alg
    else:
        if alg == "R": return "L'"
        if alg == "R'": return "L"
        if alg == "R2": return "L2"
        if alg == "L'": return "R"
        if alg == "L": return "R'"
        if alg == "L2": return "R2"
        
        if alg == "r": return "l'"
        if alg == "r'": return "l"
        if alg == "r2": return "l2"
        if alg == "l'": return "r"
        if alg == "l": return "r'"
        if alg == "l2": return "r2"
        
        if alg[0] == "G": return alg
        
        if alg[-1] == "'": #convert all X' to X
            return alg[:-1]
        elif alg[-1] == "2": #convert all X2 to just X2
            return alg
        else:
            return alg+"'" #convert all X to X'

class Memoize:
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
       Will only work on functions with non-mutable arguments
    """
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
        
    def __call__(self, grip, alg, c=0.0, rh=True):
        if len(alg) > 10 :
            return self.fn(grip, alg, c, rh)
        else:
            t = (grip, rh, alg)
            if not self.memo.has_key(t):
                self.memo[t] = self.fn(grip, alg, 0.0, rh) 
                
            return c + self.memo[t]


#fast version of cost, lol
#grip= 0,1,2
#alg = (A1, A2, A3, .... An)
#c = float
#rh = True/False
def fastcost(grip, alg, c=0.0, rh=True):
    if len(alg) == 0: 
        return c #base case
    
    cur = alg[0] #current move, a string
    nalg = alg[1:] #list of moves to still be done after this move
    
    if not rh: c+= lpenalty
    
    if c == 0.0: #first rotation is free for y's, because we can just AUF
        #handle cube rotations:
        #after a rotation, we can use left or right hand interchangably..we can fiddle the fingers in either way
        if cur == "y": return min(fastcostm(grip, nalg, c, rh), fastcostm(grip, nalg, c, not rh))
        if cur == "y'": return min(fastcostm(grip, nalg, c, rh), fastcostm(grip, nalg, c, not rh))
        if cur == "y2": return min(fastcostm(grip, nalg, c, rh), fastcostm(grip, nalg, c, not rh))    
    else:
        #handle cube rotations:
        #after a rotation, we can use left or right hand interchangably..we can fiddle the fingers in either way
        if cur == "y": return min(fastcostm(grip, nalg, c+YC, rh), fastcostm(grip, nalg, c+YC, not rh))
        if cur == "y'": return min(fastcostm(grip, nalg, c+YPC, rh), fastcostm(grip, nalg, c+YPC, not rh))
        if cur == "y2": return min(fastcostm(grip, nalg, c+Y2C, rh), fastcostm(grip, nalg, c+Y2C, not rh))    

    #x rotations are funky!
    if cur == "x": return fastcostm(min(2, grip+1), nalg, c+XC, rh)
    if cur == "x'": return fastcostm(max(0, grip-1), nalg, c+XPC, rh)
    if cur == "x2" and grip == 0: return fastcostm(2, nalg, c+X2C, rh)
    if cur == "x2" and grip == 2: return fastcostm(0, nalg, c+X2C, rh)
    if cur == "x2" and grip == 1: return min(fastcostm(2, nalg, c+X2C, rh), fastcostm(0, nalg, c+X2C, rh)) #can rotate either way
    #z rotations preserve grip
    if cur == "z": return fastcostm(grip, nalg, c+ZC, rh)
    if cur == "z'": return fastcostm(grip, nalg, c+ZPC, rh)    
    if cur == "z2": return fastcostm(grip, nalg, c+Z2C, rh)    

    #if we are using left hand, mirror this move to pretend we are using right hand
    #after all, using left hand is same as using right hand, just everything is mirrored in the alg
    if  not rh: cur = mirrorF(cur)
    
    #if first letter of current symbol is....
    if cur[0] == "R":
        #grip changes
        if grip == 0 and cur == "R": return fastcostm(1, nalg,c+RC, rh)
        if grip == 0 and cur == "R'": return min(fastcostm(1, alg,c+RGC, rh), fastcostm(2, alg,c+RGC, rh))
        if grip == 0 and cur == "R2": return fastcostm(2, nalg,c+R2C, rh)
        
        if grip == 1 and cur == "R": return fastcostm(2, nalg,c+RC, rh)
        if grip == 1 and cur == "R'": return fastcostm(0, nalg,c+RPC, rh)
        if grip == 1 and cur == "R2": return min(fastcostm(0, alg,c+RGC, rh), fastcostm(2, alg,c+RGC, rh))
        
        if grip == 2 and cur == "R": return min(fastcostm(0, alg,c+RGC, rh), fastcostm(1, alg,c+RGC, rh))
        if grip == 2 and cur == "R'": return fastcostm(1, nalg,c+RPC, rh)
        if grip == 2 and cur == "R2": return fastcostm(0, nalg,c+R2C, rh)
    
    elif cur[0] == "F":
        #this is an F/F' move
        if grip == 0 and cur == "F": return fastcostm(0, nalg,c+FC, rh)
        if grip == 0 and cur == "F'": return fastcostm(0, nalg,c+FPC, rh)
        if grip == 0 and cur == "F2": return fastcostm(0, nalg,c+F2C, rh)
        
        return fastcostm(0, alg,c+RGC, rh) #must regrip to 0 first otherwise
    
    elif cur[0] == "D":
        #this is D/D' move
        if cur == "D": return fastcostm(grip, nalg,c+DC, rh) #D can be done using left ring finger, so its grip-free
        if cur == "D2": return fastcostm(grip, nalg,c+D2C, rh) #D2 can as well, even though its slow as hell
        
        if grip == 0 and cur == "D'": return fastcostm(1, alg,c+RGC, rh) #must regrip to 1
        if grip == 1 and cur == "D'": return fastcostm(1, nalg,c+DPC, rh)
        if grip == 2 and cur == "D'": return fastcostm(1, alg,c+RGC, rh) #must regrip to 1
        
    elif cur[0] == "U":
        #U' moves are free
        if cur == "U'": return fastcostm(grip, nalg,c+UPC, rh) #U' can be made at any grip
        
        #otherwise its U or U2. both need grip 1
        if grip == 0: return fastcostm(1, alg,c+RGC, rh) #must regrip to 1
        if grip == 2: return fastcostm(1, alg,c+RGC, rh) #must regrip to 1
        
        if grip == 1 and cur == "U": return fastcostm(1, nalg,c+UC, rh)
        if grip == 1 and cur == "U2": return fastcostm(1, nalg,c+U2C, rh)
        
    elif cur[0] == "B":
        #must regrip to either 0 or 2 first
        if grip == 1: return min(fastcostm(0, alg, c+RGC, rh), fastcostm(2, alg, c+RGC, rh))
        
        if grip == 0 and cur == "B'": return fastcostm(0, nalg,c+BPC, rh)
        if grip == 0 and cur == "B2": return fastcostm(0, nalg,c+B2C, rh)
        if grip == 0 and cur == "B": return fastcostm(2, alg, c+RGC, rh)
        
        if grip == 2 and cur == "B": return fastcostm(2, nalg, c+BC, rh)
        if grip == 2 and cur == "B2": return fastcostm(2, nalg,c+B2C, rh)
        if grip == 2 and cur == "B'": return fastcostm(0, alg, c+RGC, rh) #could also go to left hand and do it that way? hm
    
    elif cur[0] == "L":
        #this is an L/L' move.
        #switch grip and mirror alg
        if grip == 1: return fastcostm(1, alg, c+SGC, not rh) #SWITCH HANDS WEEE
        if grip == 0 or grip == 2: return fastcostm(1, alg, c+RGC, rh) #must switch grip first to 1-grip so that we can hold the cube

    #if first letter of current symbol is....
    elif cur[0] == "r":
        #grip changes
        if grip == 0 and cur == "r": return fastcostm(1, nalg,c+rC, rh)
        if grip == 0 and cur == "r'": return min(fastcostm(1, alg,c+RGC, rh), fastcostm(2, alg,c+RGC, rh))
        if grip == 0 and cur == "r2": return fastcostm(2, nalg,c+r2C, rh)
        
        if grip == 1 and cur == "r": return fastcostm(2, nalg,c+rC, rh)
        if grip == 1 and cur == "r'": return fastcostm(0, nalg,c+rPC, rh)
        if grip == 1 and cur == "r2": return min(fastcostm(0, alg,c+RGC, rh), fastcostm(2, alg,c+RGC, rh))
        
        if grip == 2 and cur == "r": return min(fastcostm(0, alg,c+RGC, rh), fastcostm(1, alg,c+RGC, rh))
        if grip == 2 and cur == "r'": return fastcostm(1, nalg,c+rPC, rh)
        if grip == 2 and cur == "r2": return fastcostm(0, nalg,c+r2C, rh)
    
    elif cur[0] == "f":
        #this is an F/F' move
        if grip == 0 and cur == "f": return fastcostm(0, nalg,c+fC, rh)
        if grip == 0 and cur == "f'": return fastcostm(0, nalg,c+fPC, rh)
        if grip == 0 and cur == "f2": return fastcostm(0, nalg,c+f2C, rh)
        
        return fastcostm(0, alg,c+RGC, rh) #must regrip to 0 first otherwise
    
    elif cur[0] == "d":
        #this is D/D' move
        if cur == "d": return fastcostm(grip, nalg,c+dC, rh) #D can be done using left ring finger, so its grip-free
        if cur == "d2": return fastcostm(grip, nalg,c+d2C, rh) #D2 can as well, even though its slow as hell
        
        if grip == 0 and cur == "d'": return fastcostm(1, alg,c+RGC, rh) #must regrip to 1
        if grip == 1 and cur == "d'": return fastcostm(1, nalg,c+dPC, rh)
        if grip == 2 and cur == "d'": return fastcostm(1, alg,c+RGC, rh) #must regrip to 1
        
    elif cur[0] == "u":
        #U' moves are free
        if cur == "u'": return fastcostm(grip, nalg,c+uPC, rh) #U' can be made at any grip
        
        #otherwise its U or U2. both need grip 1
        if grip == 0: return fastcostm(1, alg,c+RGC, rh) #must regrip to 1
        if grip == 2: return fastcostm(1, alg,c+RGC, rh) #must regrip to 1
        
        if grip == 1 and cur == "u": return fastcostm(1, nalg,c+uC, rh)
        if grip == 1 and cur == "u2": return fastcostm(1, nalg,c+u2C, rh)
        
    elif cur[0] == "b":
        #must regrip to either 0 or 2 first
        if grip == 1: return min(fastcostm(0, alg, c+RGC, rh), fastcostm(2, alg, c+RGC, rh))
        
        if grip == 0 and cur == "b'": return fastcostm(0, nalg,c+bPC, rh)
        if grip == 0 and cur == "b2": return fastcostm(0, nalg,c+b2C, rh)
        if grip == 0 and cur == "b": return fastcostm(2, alg, c+RGC, rh)
        
        if grip == 2 and cur == "b": return fastcostm(2, nalg, c+bC, rh)
        if grip == 2 and cur == "b2": return fastcostm(2, nalg,c+b2C, rh)
        if grip == 2 and cur == "b'": return fastcostm(0, alg, c+RGC, rh) #could also go to left hand and do it that way? hm
    
    elif cur[0] == "l":
        #this is an L/L' move.
        #switch grip and mirror alg
        if grip == 1: return fastcostm(1, alg, c+SGC, not rh) #SWITCH HANDS WEEE
        if grip == 0 or grip == 2: return fastcostm(1, alg, c+RGC, rh) #must switch grip first to 1-grip so that we can hold the cube
    
    else:
        
        print "WTF UNEXPECTED LITERAL ERROR: " + `cur` + ". IGNORING LITERAL."
        return fastcostm(grip, nalg, c, rh)
    
fastcostm = fastcost #Memoize(fastcost)



#cost with that grip on alg alg (a LIST of moves), path so far is p to this point, ...
#...cost so far is cost, and we hold cube with left hand (right hand operates)
def cost(grip, alg, p="", c=0.0, rh=True):
	if len(alg) == 0: 
		return (postProcess(p), c) #base case
	
	cur = alg[0] #current move, a string
	nalg = alg[1:] #list of moves to still be done after this move

	if not rh: c += lpenalty
		
	#handle cube rotations:
	if c == 0.0: #first rotation is free for y's, because we can just AUF
	#handle cube rotations:
	#after a rotation, we can use left or right hand interchangably..we can fiddle the fingers in either way
		if cur == "y": return mintup1(cost(grip, nalg, p + "y ", c, rh), cost(grip, nalg, p + "y ! ", c, not rh))
		if cur == "y'": return mintup1(cost(grip, nalg, p + "y' ", c, rh), cost(grip, nalg, p + "y' ! ", c, not rh))
		if cur == "y2": return mintup1(cost(grip, nalg, p + "y2 ", c, rh), cost(grip, nalg, p + "y2 ! ", c, not rh))
		
	else:
		#after a rotation, we can use left or right hand interchangably..we can fiddle the fingers in either way
		if cur == "y": return mintup1(cost(grip, nalg, p + "y ", c+YC, rh), cost(grip, nalg, p + "y ! ", c+YC, not rh))
		if cur == "y'": return mintup1(cost(grip, nalg, p + "y' ", c+YPC, rh), cost(grip, nalg, p + "y' ! ", c+YPC, not rh))
		if cur == "y2": return mintup1(cost(grip, nalg, p + "y2 ", c+Y2C, rh), cost(grip, nalg, p + "y2 ! ", c+Y2C, not rh))

		#x rotations are funky!
	if cur == "x": return cost(min(2, grip+1), nalg, p + "x ", c+XC, rh)
	if cur == "x'": return cost(max(0, grip-1), nalg, p + "x' ", c+XPC, rh)
	if cur == "x2" and grip == 0: return cost(2, nalg, p+"x2 ", c+X2C, rh)
	if cur == "x2" and grip == 2: return cost(0, nalg, p+"x2 ", c+X2C, rh)
	if cur == "x2" and grip == 1: return mintup1(cost(2, nalg, p+"x2 ", c+X2C, rh), cost(0, nalg, p+"x2 ", c+X2C, rh)) #can rotate either way
	#z rotations preserve grip
	if cur == "z": return cost(grip, nalg, p+"z ", c+ZC, rh)
	if cur == "z'": return cost(grip, nalg, p+"z' ", c+ZPC, rh)
	if cur == "z2": return cost(grip, nalg, p+"z2 ", c+Z2C, rh)

	#if we are using left hand, mirror this move to pretend we are using right hand
	#after all, using left hand is same as using right hand, just everything is mirrored in the alg
	if  not rh: cur = mirrorF(cur)
	
	#if first letter of current symbol is....
	if cur[0] == "R":
		#grip changes
		if grip == 0 and cur == "R": return cost(1, nalg, p+"R ",c+RC, rh)
		if grip == 0 and cur == "R'": return mintup1(cost(1, alg,p+"G1 ",c+RGC, rh), cost(2, alg,p+"G2 ",c+RGC, rh))
		if grip == 0 and cur == "R2": return cost(2, nalg, p+"R2 ",c+R2C, rh)
		
		if grip == 1 and cur == "R": return cost(2, nalg,p+"R ",c+RC, rh)
		if grip == 1 and cur == "R'": return cost(0, nalg,p+"R' ",c+RPC, rh)
		if grip == 1 and cur == "R2": return mintup1(cost(0, alg,p+"G0 ",c+RGC, rh), cost(2, alg,p+"G2 ",c+RGC, rh))
		
		if grip == 2 and cur == "R": return mintup1(cost(0, alg,p+"G0 ",c+RGC, rh), cost(1, alg,p+"G1 ",c+RGC, rh))
		if grip == 2 and cur == "R'": return cost(1, nalg,p+"R' ",c+RPC, rh)
		if grip == 2 and cur == "R2": return cost(0, nalg,p+"R2 ",c+R2C, rh)
	
	elif cur[0] == "F":
		#this is an F/F' move
		if grip == 0 and cur == "F": return cost(0, nalg,p+"F ",c+FC, rh)
		if grip == 0 and cur == "F'": return cost(0, nalg,p+"F' ",c+FPC, rh)
		if grip == 0 and cur == "F2": return cost(0, nalg,p+"F2 ",c+F2C, rh)
		
		return cost(0, alg,p+"G0 ",c+RGC, rh) #must regrip to 0 first otherwise
	
	elif cur[0] == "D":
		#this is D/D' move
		if cur == "D": return cost(grip, nalg,p+"D ",c+DC, rh) #D can be done using left ring finger, so its grip-free
		if cur == "D2": return cost(grip, nalg,p+"D2 ",c+D2C, rh) #D2 can as well, even though its slow as hell
		
		if grip == 0 and cur == "D'": return cost(1, alg,p+"G1 ",c+RGC, rh) #must regrip to 1
		if grip == 1 and cur == "D'": return cost(1, nalg,p+"D' ",c+DPC, rh)
		if grip == 2 and cur == "D'": return cost(1, alg,p+"G1 ",c+RGC, rh) #must regrip to 1
		
	elif cur[0] == "U":
		#U' moves are free
		if cur == "U'": return cost(grip, nalg,p+"U' ",c+UPC, rh) #U' can be made at any grip
		
		#otherwise its U or U2. both need grip 1
		if grip == 0: return cost(1, alg,p+"G1 ",c+RGC, rh) #must regrip to 1
		if grip == 2: return cost(1, alg,p+"G1 ",c+RGC, rh) #must regrip to 1
		
		if grip == 1 and cur == "U": return cost(1, nalg,p+"U ",c+UC, rh)
		if grip == 1 and cur == "U2": return cost(1, nalg,p+"U2 ",c+U2C, rh)
		
	elif cur[0] == "B":
		#must regrip to either 0 or 2 first
		if grip == 1: return mintup1(cost(0, alg, p+"G0 ", c+RGC, rh), cost(2, alg, p+"G2 ", c+RGC, rh))
		
		if grip == 0 and cur == "B'": return cost(0, nalg,p+"B' ",c+BPC, rh)
		if grip == 0 and cur == "B2": return cost(0, nalg,p+"B2 ",c+B2C, rh)
		if grip == 0 and cur == "B": return cost(2, alg,p+"G2 ", c+RGC, rh)
		
		if grip == 2 and cur == "B": return cost(2, nalg,p+"B ", c+BC, rh)
		if grip == 2 and cur == "B2": return cost(2, nalg,p+"B2 ",c+B2C, rh)
		if grip == 2 and cur == "B'": return cost(0, alg,p+"G0 ", c+RGC, rh) #could also go to left hand and do it that way? hm
	
	elif cur[0] == "L":
		#this is an L/L' move.
		#switch grip and mirror alg
		if grip == 1: return cost(1, alg, p+"! ", c+SGC, not rh) #SWITCH HANDS WEEE
		if grip == 0 or grip == 2: return cost(1, alg, p+"G1 ", c+RGC, rh) #must switch grip first to 1-grip so that we can hold the cube

	#if first letter of current symbol is....
	elif cur[0] == "r":
		#grip changes
		if grip == 0 and cur == "r": return cost(1, nalg, p+"r ",c+rC, rh)
		if grip == 0 and cur == "r'": return mintup1(cost(1, alg,p+"G1 ",c+RGC, rh), cost(2, alg,p+"G2 ",c+RGC, rh))
		if grip == 0 and cur == "r2": return cost(2, nalg, p+"r2 ",c+r2C, rh)
		
		if grip == 1 and cur == "r": return cost(2, nalg,p+"r ",c+rC, rh)
		if grip == 1 and cur == "r'": return cost(0, nalg,p+"r' ",c+rPC, rh)
		if grip == 1 and cur == "r2": return mintup1(cost(0, alg,p+"G0 ",c+RGC, rh), cost(2, alg,p+"G2 ",c+RGC, rh))
		
		if grip == 2 and cur == "r": return mintup1(cost(0, alg,p+"G0 ",c+RGC, rh), cost(1, alg,p+"G1 ",c+RGC, rh))
		if grip == 2 and cur == "r'": return cost(1, nalg,p+"r' ",c+rPC, rh)
		if grip == 2 and cur == "r2": return cost(0, nalg,p+"r2 ",c+r2C, rh)
	
	elif cur[0] == "f":
		#this is an F/F' move
		if grip == 0 and cur == "f": return cost(0, nalg,p+"f ",c+fC, rh)
		if grip == 0 and cur == "f'": return cost(0, nalg,p+"f' ",c+fPC, rh)
		if grip == 0 and cur == "f2": return cost(0, nalg,p+"f2 ",c+f2C, rh)
		
		return cost(0, alg,p+"G0 ",c+RGC, rh) #must regrip to 0 first otherwise
	
	elif cur[0] == "d":
		#this is D/D' move
		if cur == "d": return cost(grip, nalg,p+"d ",c+dC, rh) #D can be done using left ring finger, so its grip-free
		if cur == "d2": return cost(grip, nalg,p+"d2 ",c+d2C, rh) #D2 can as well, even though its slow as hell
		
		if grip == 0 and cur == "d'": return cost(1, alg,p+"G1 ",c+RGC, rh) #must regrip to 1
		if grip == 1 and cur == "d'": return cost(1, nalg,p+"d' ",c+dPC, rh)
		if grip == 2 and cur == "d'": return cost(1, alg,p+"G1 ",c+RGC, rh) #must regrip to 1
		
	elif cur[0] == "u":
		#U' moves are free
		if cur == "u'": return cost(grip, nalg,p+"u' ",c+uPC, rh) #U' can be made at any grip
		
		#otherwise its U or U2. both need grip 1
		if grip == 0: return cost(1, alg,p+"G1 ",c+RGC, rh) #must regrip to 1
		if grip == 2: return cost(1, alg,p+"G1 ",c+RGC, rh) #must regrip to 1
		
		if grip == 1 and cur == "u": return cost(1, nalg,p+"u ",c+uC, rh)
		if grip == 1 and cur == "u2": return cost(1, nalg,p+"u2 ",c+u2C, rh)
		
	elif cur[0] == "b":
		#must regrip to either 0 or 2 first
		if grip == 1: return mintup1(cost(0, alg, p+"G0 ", c+RGC, rh), cost(2, alg, p+"G2 ", c+RGC, rh))
		
		if grip == 0 and cur == "b'": return cost(0, nalg,p+"b' ",c+bPC, rh)
		if grip == 0 and cur == "b2": return cost(0, nalg,p+"b2 ",c+b2C, rh)
		if grip == 0 and cur == "b": return cost(2, alg,p+"G2 ", c+RGC, rh)
		
		if grip == 2 and cur == "b": return cost(2, nalg,p+"b ", c+bC, rh)
		if grip == 2 and cur == "b2": return cost(2, nalg,p+"b2 ",c+b2C, rh)
		if grip == 2 and cur == "b'": return cost(0, alg,p+"G0 ", c+RGC, rh) #could also go to left hand and do it that way? hm
	
	elif cur[0] == "l":
		#this is an L/L' move.
		#switch grip and mirror alg
		if grip == 1: return cost(1, alg, p+"! ", c+SGC, not rh) #SWITCH HANDS WEEE
		if grip == 0 or grip == 2: return cost(1, alg, p+"G1 ", c+RGC, rh) #must switch grip first to 1-grip so that we can hold the cube
	
	else:
		print "WTF UNEXPECTED LITERAL ERROR: " + `cur` + ". IGNORING LITERAL."
		return cost(grip, nalg, p, c, rh) #! signifies hand switch
			
#reflect things after !'s to their right things.
#!'s signify a hand grip switch
#alg here is given as STRING of notation separated by spaces
def postProcess(alg):
	res=""
	parts = alg.split(" ")
	c=0
	for p in parts:
		if p == "": #can sometimes happen for some reason
			pass
		elif p == "!":
			c+=1
			res += "! "
		else:
			res += mirrorF(p, c) + " "
	return res

#cost(): method where all magic happens. This method is terribly inefficient because concatenation of strings in Python 2.4 is slow. 2.5 is better
#efficient version could be made by disregarding the path-to-solution build in the recursion.
#possibly implement this later, so that when we need to tet 10 000 ALGS, we can Fast-test them to filter out 
#the first 100 best, and then use this inefficient version on those 100 to see actually how to execute them too.

#returns the tuple with lower second argument
def mintup1(t1, t2):
	if t1[1] < t2[1]:
		return t1
	else:
		return t2
	
	
#GRIPPER. ORIGIANLLY STARTED BY BADMEPHISTO.
#Given alg, evaluate how good it is. Main method is mincost()
#All permissions granted to enchance the code

#SUPPORTS: ALGS in standard notation usisng FBRLUD
#WILL RUN if you give it MSE and fbrlud but the final costs may be skewed a little

#!!!!!!!!!DOES NOT SUPPORT CUBE ROTATIONS xyz (yet)!!!!!!!!!!!!!!

#TODO:
#add full support for M/S/E (current implementation is just a hack)
#add support for x/y/z

import operator
#from constants import *

def mincost(alg, needPath = True):
	#ex of input: (R U' R U) (R U) (R U') (R' U' R2)
	#normalize input by removing brackets and stuff
	ialg = alg.replace("(", "")
	ialg = ialg.replace(")", "")
	ialg = ialg.replace("2'", "2")
	ialg = ialg.replace("  ", " ")
	
	#for now treat double layer turns as single layer turns. Maybe more on this later maybe?
	#ialg = ialg.replace("u", "U")
	#ialg = ialg.replace("r", "R")
	#ialg = ialg.replace("d", "D")
	#ialg = ialg.replace("f", "F")
	#ialg = ialg.replace("b", "B")
	#ialg = ialg.replace("l", "L")
	
	#temporary stuff too. SE do not occur too often anyway. M is slightly of concern. Maybe add support later?
	ialg = ialg.replace("M", "R")
	ialg = ialg.replace("S", "F")
	ialg = ialg.replace("E", "D")
	
	parts = ialg.split(" ")
	parts = tuple(parts)
	
	#- print predicted time in seconds. min of all possible starting grips
	#- the operator is there so that all tuples returned are sorted by the 1st thing in the tuple (the cost)
	#  since the cost() function returns a tuple (ALG, cost)
	#- G0, G1, G2 are the 3 grips you can have on the cube with your right hand.
	#  G0 is with thumb on D, fingers on U
	#  G1 is with thumb on F, fingers on B
	#  G2 is with thumb on U, fingers on D
	if needPath:
		return sorted([cost(0, parts, "G0 "),cost(1, parts, "G1 "),cost(2, parts, "G2 ")], key=operator.itemgetter(1))[0]
	else:
		return sorted([fastcostm(0, parts),fastcostm(1, parts),fastcostm(2, parts)])[0]
	

#This file will contain methods that pimp out an algorithm:
from string import maketrans
rotations = { "x":  "LRUDBF", 
              "x2": "LRBFDU", 
              "x'": "LRDUFB", 
              "y":  "BFLRUD", 
              "y2": "RLBFUD", 
              "y'": "FBRLUD", 
              "z":  "UDFBRL", 
              "z2": "RLFBDU", 
              "z'": "DUFBLR" }
standard = "LRFBUD"
import psyco
psyco.full()

    
def cuberotation(r):    
    global rotations, standard    
    return maketrans(standard, rotations[r])

#alg: string of notation
#r: the rotation, as string
#output: string of new notation
def rotalg(alg, r):
    return alg.translate(cuberotation(r))

#example: D R2 U' R2 U R2 B2 U B2 D' R2
#         0123456789
#         z' R U2...
#first call p is 0. its the pointer
#rots is 0, meaning first call we use 0 rotations so far
def pimp(alg, p = 0, rots = 0):
    global topList, maxRots, counter

    #base case-------------------------------------------------------------
    if p >= len(alg) - 1:
        cost = mincost(alg.strip(), needPath=False) #except for last character, because it is space
        counter +=1
        
        i = len(topList) - 1
        if cost < topList[i][1]:
            #this is a good alg, insert it to the right place in the list!
            while(cost < topList[i-1][1] and i > 0):
                topList[i] = topList[i-1]
                i-=1
                
            topList[i] = (alg.strip(), cost)
        return
    #-----------------------------------------------------------------------
    
    cur = alg[p:p+2]
    #if this literal has a ' or 2 in it, then it takes up 3 spaces in the string, not just 2
    mv = 0

    if alg[p+1] == "'" or alg[p+1] == "2": 
        mv = 3
        rest = alg[p+mv:]
    else: 
        mv = 2
        rest = alg[p+mv:]

    #leave it alone
    pimp(alg, p + mv, rots)
    
    #for now i will avoid making double layer turns like z2 y2 x2... they take way too much time to do
    #i postulate that they are never useful to make
    
    if rots < maxRots:
        #or make it R or U or doubleturn
        if cur == "D ": 
            pimp(alg[:p] + "z' R " + rotalg(rest, "z'"), p+5, rots+1) #make it R
            pimp(alg[:p] + "u " + rotalg(rest, "y"), p+2, rots+1) #make it double turn (notdone)
            return
        if cur == "D'": 
            pimp(alg[:p] + "z' R' " + rotalg(rest, "z'"), p+6, rots+1)
            pimp(alg[:p] + "u' " + rotalg(rest, "y'"), p+3, rots+1)    
            return
        if cur == "D2":
            pimp(alg[:p] + "z' R2 " + rotalg(rest, "z'"), p+6, rots+1)
            pimp(alg[:p] + "u2 " + rotalg(rest, "y2"), p+3, rots+1)
            return
        
        if cur == "U ":
            pimp(alg[:p] + "z R " + rotalg(rest, "z"), p+4, rots+1)
            pimp(alg[:p] + "d " + rotalg(rest, "y'"), p+2, rots+1)
            return
        if cur == "U'":
            pimp(alg[:p] + "z R' " + rotalg(rest, "z"), p+5, rots+1)
            pimp(alg[:p] + "d' " + rotalg(rest, "y"), p+3, rots+1)
            return
        if cur == "U2":
            pimp(alg[:p] + "z R2 " + rotalg(rest, "z"), p+5, rots+1)
            pimp(alg[:p] + "d2 " + rotalg(rest, "y2"), p+3, rots+1)
            return
        
        if cur == "R ":
            pimp(alg[:p] + "z' U " + rotalg(rest, "z'"), p+5, rots+1)
            pimp(alg[:p] + "l " + rotalg(rest, "x'"), p+2, rots+1)
            return
        if cur == "R'":
            pimp(alg[:p] + "z' U' " + rotalg(rest, "z'"), p+6, rots+1)
            pimp(alg[:p] + "l' " + rotalg(rest, "x"), p+3, rots+1)
            return
        if cur == "R2":
            pimp(alg[:p] + "z' U2 " + rotalg(rest, "z'"), p+6, rots+1)
            pimp(alg[:p] + "l2 " + rotalg(rest, "x2"), p+3, rots+1)
            return
        
        if cur == "L ":
            pimp(alg[:p] + "z U " + rotalg(rest, "z"), p+4, rots+1)
            pimp(alg[:p] + "r " + rotalg(rest, "x"), p+2, rots+1)
            pimp(alg[:p] + "y2 R " + rotalg(rest, "y2"), p+5, rots+1)
            return
        if cur == "L'":
            pimp(alg[:p] + "z U' " + rotalg(rest, "z"), p+5, rots+1)
            pimp(alg[:p] + "r' " + rotalg(rest, "x'"), p+3, rots+1)
            pimp(alg[:p] + "y2 R' " + rotalg(rest, "y2"), p+6, rots+1)
            return
        if cur == "L2":
            pimp(alg[:p] + "z U2 " + rotalg(rest, "z"), p+5, rots+1)
            pimp(alg[:p] + "r2 " + rotalg(rest, "x2"), p+3, rots+1)
            pimp(alg[:p] + "y2 R2 " + rotalg(rest, "y2"), p+6, rots+1)
            return
        
        if cur == "F ":
            pimp(alg[:p] + "y' R " + rotalg(rest, "y'"), p+5, rots+1)
            pimp(alg[:p] + "x U " + rotalg(rest, "x"), p+4, rots+1)
            pimp(alg[:p] + "b " + rotalg(rest, "z'"), p+2, rots+1)
            return
        if cur == "F'":
            pimp(alg[:p] + "y' R' " + rotalg(rest, "y'"), p+6, rots+1)
            pimp(alg[:p] + "x U' " + rotalg(rest, "x"), p+5, rots+1)
            pimp(alg[:p] + "b' " + rotalg(rest, "z"), p+3, rots+1)
            return
        if cur == "F2":
            pimp(alg[:p] + "y' R2 " + rotalg(rest, "y'"), p+6, rots+1)
            pimp(alg[:p] + "x U2 " + rotalg(rest, "x"), p+5, rots+1)
            pimp(alg[:p] + "b2 " + rotalg(rest, "z2"), p+3, rots+1)
            return
        
        if cur == "B ":
            pimp(alg[:p] + "y R " + rotalg(rest, "y"), p+4, rots+1)
            pimp(alg[:p] + "x' U " + rotalg(rest, "x'"), p+5, rots+1)
            pimp(alg[:p] + "f " + rotalg(rest, "z"), p+3, rots+1)
            return
        if cur == "B'":
            pimp(alg[:p] + "y R' " + rotalg(rest, "y"), p+5, rots+1)
            pimp(alg[:p] + "x' U' " + rotalg(rest, "x'"), p+6, rots+1)
            pimp(alg[:p] + "f' " + rotalg(rest, "z'"), p+3, rots+1)                              
            return
        if cur == "B2":
            pimp(alg[:p] + "y R2 " + rotalg(rest, "y"), p+5, rots+1)
            pimp(alg[:p] + "x' U2 " + rotalg(rest, "x'"), p+6, rots+1)
            pimp(alg[:p] + "f2 " + rotalg(rest, "z2"), p+3, rots+1)
            return
        
#create the list of top results
topList = []
for i in range(0, 50): topList.append(("", "", 100))
maxRots = 2
counter = 0

def produceTable(alg):
	global topList
	
	topList = []
	for i in range(0, 50): topList.append(("", "", 100))
	pimp(alg)
	header = "<table><td>Alg</td><td>How to get there</td><td>Cost</td>"
	#str="R cost is " + `RC`
	str=""
	for j in topList:
		if j[0] != "":
			execPath, thecost = mincost(j[0], needPath=True)
			str += "<tr><td><b> %s </b></td><td><b> %s </b></td><td><b> %s </b></td></tr>" % (j[0], execPath, `j[1]`[:5])
			print j
			#write it to html file
			
	footer = "</table>"
	str = str.replace("G0", "<font color='red'>G0</font>")
	str = str.replace("G1", "<font color='red'>G1</font>")
	str = str.replace("G2", "<font color='red'>G2</font>")
	str = str.replace(" x", "<font color='blue'> x</font>")
	str = str.replace(" y", "<font color='blue'> y</font>")
	str = str.replace(" y2", "<font color='blue'> y2</font>")
	str = str.replace(" z", "<font color='blue'> z</font>")
	return header+str+footer
