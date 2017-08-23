import random, time

print "importing snappy ...",
import snappy
print "done"
print "version =", snappy.version()

# STEP 1: SAMPLE A RANDOM PERMUTATION

def rand_perm(n):
    a = range(n)
    random.shuffle(a)
    return a

# STEP 2: GET A TRIANGULATION OF THE COMPLEMENT

def petaluma_complement(P):
    N = len(P)
    B = [(-1)**int(P[i*2%N] < P[(i+j)*2%N]) * j
         for i in range(N)
         for j in range(1,N/2)]
    M = snappy.Manifold('Braid' + str(B))
    M.dehn_fill((1,0),1)
    M = M.filled_triangulation()
    # print M.cusp_info()
    return M

# STEP 3: CHECK HYPERBOLICITY AND COMPUTE VOLUME

def analyze_complement(M, tries = 10):
    """
    returns (volume, precision, is-verified, num-shapes, solution-type)
    """
    vol = RealNumber(M.volume())
    pr = vol.precision()
    for tr in range(tries):
        hype, shapes = M.verify_hyperbolicity()
        if hype:
            break
        M.randomize()
    st = M.solution_type()
    return {"volume" : vol, 
            "precision" : pr, 
            "verified" : hype, 
            "shapes" : len(shapes), 
            "try" : tr+1, 
            "type" : st}
                
    
# REPEAT STEPS 1,2,3 MANY TIMES

def sample(petals = range(5, 11, 2), 
           batchs = [100], 
           hp = True, 
           verbose = 3,
           tries = 1,
           save = "./samples/"):
    params = [(n,m) for n in petals for m in batchs]
    for n,m in params:
        if verbose >= 1:
            print time.ctime(),"petals =", n, "samples =", m
        samples = []
        for i in range(m):
            perm = rand_perm(n)
            try:
                M = petaluma_complement(perm)
                if hp:
                    M = M.high_precision()
                res = analyze_complement(M, tries = tries)
                if verbose >= 2:
                    print perm
                    print res
                res['perm'] = perm
                samples.append(res)
            except Exception, eee:
                if verbose >= 1:
                    print eee
        if save != None:
            open(save + '/%d-%d-%d' % (n,m,int(time.time())), 'wb').write(str(samples) + '\n')
            if verbose >= 1:
                print "saved", len(samples), "samples"
                print
                
# TEST
                
TEST_CASES = [
    ("Unknot",[1,2,3,4,5], 3),
    ("Another Unknot",[9,6,11,2,4,7,10,1,5,8,3], 3),
    ("Trefoil", [1,3,5,2,4], 5),
    ("Figure-8", [1,5,3,7,2,4,6],1),
    ("Cinquefoil", [1,3,6,2,5,7,4],1),
    ("Trefoil # Trefoil", [1,3,5,2,4,13,15,12,14],1),
    ("Figure-8 # Figure-8", [1,5,3,7,2,4,6,15,13,17,12,14,16],1),
    ("Figure-8 # Trefoil", [1,5,3,7,2,4,6,13,15,12,14],1),
    ("Some Hyperbolic Knot?", [12, 9, 14, 11, 1, 6, 10, 0, 2, 13, 8, 3, 4, 16, 5, 15, 7], 10),
    ("Some Other Hyperbolic Knot?", [14, 0, 3, 6, 11, 9, 18, 12, 15, 2, 5, 1, 8, 13, 17, 4, 10, 7, 16], 10),
    ("Some Hyperbolic Knot? # Figure-8", [12, 9, 14, 11, 1, 6, 10, 0, 2, 13, 8, 3, 4, 16, 5, 15, 7, 105,103,107,102,104,106], 1),
    ("Some Hyperbolic Knot? # Some Other Hyperbolic Knot?", [12, 9, 14, 11, 1, 6, 10, 0, 2, 13, 8, 3, 4, 16, 5, 15, 7] + [114, 100, 103, 106, 111, 109, 118, 112, 115, 102, 105, 101, 108, 113, 117, 104, 110, 107, 116], 10),
    ("Some Other Hyperbolic Knot? # Figure-8", [14, 0, 3, 6, 11, 9, 18, 12, 15, 2, 5, 1, 8, 13, 17, 4, 10, 7, 16, 105,103,107,102,104,106], 1),
    ("Torus (10,11)", [0, 10, 20, 9, 19, 8, 18, 7, 17, 6, 16, 5, 15, 4, 14, 3, 13, 2, 12, 1, 11], 5),
    ]

def test(hp = True, tries = 10):
    for title,perm,times in TEST_CASES:
        print title
        print perm
        for t in range(times):            
            M = petaluma_complement(perm)
            if hp:
                M = M.high_precision()
            res = analyze_complement(M, tries)
            print res
        print
            
        
        
