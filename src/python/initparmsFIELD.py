# note that the following assumes you have certain directories setup in your home folder (e.g. ~/models/<modelfiles> and ~/clusterdesc/<cluster-description>

operations = 'cifw'  # operations if transfering solutions
Lnum  =  'L93892' # 'specify project number
L2num =  'L93942'     #  specify 2nd project number (the calibrator)
L2dir  =  '/data/scratch/deane/xmm-lss/demixedCAL_amponly' #RPDpipe_3C53_86788'  # working directory
Ldir =   '/data/scratch/deane/xmm-lss/demixedFIELD_amponly' #RPDpipe_XMM_86788'   # directory where gain calibrator solutions are located
wdir = Ldir # for the moment
convertsb= True
scpMaps = True
parsetin = '~/models/3C53.model' # input parset file
parsetin_trans= '~/parsets/bbs_applysol_20130311.parset' # transfer AMP solns
subbands= 'range(390,404,12)'
print subbands
model = '~/models/3C53.model'

SetPhaseZero = True


dummymodel = '~/models/dummy.model'
rawdir = '/staging4/pipeline/'
clusterdesc = '~/clusterdesc/cep1.clusterdesc'


# diagnostics
cmdhistfile = open('cmdhist.txt','a')


# imaging parameters (note a few parameters are hardwired. see main file)
npix = 512
cellsize = '50arcsec'
robust = 0
weighting = 'briggs'
niters= '2000'  # awimager iterations
wmax = 5000

"""


operations dictionary:

t = copy
u = untar
b = bbs
d = delete
c = clip
i = image
f = covert img to fits
w = perform and write out diagnostics


v = vds (which is?)
g = gds (which is?)
s = bbst (transfer gain solutions to target field)




"""
