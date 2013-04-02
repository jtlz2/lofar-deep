# note that the following assumes you have certain directories setup in your home folder (e.g. ~/models/<modelfiles> and ~/clusterdesc/<cluster-description>

operations = 'aifw'    # operations to perform (see dict below)
Lnum  =  'L93942' # 'specify project number
Ldir =   '/data/scratch/deane/xmm-lss/demixedCAL_amponly/' #RPDe_3C53_86781'
wdir = Ldir # for the moment
convertsb= False
scpMaps = True
parsetin = '/home/deane/parsets/bbs_3C53.parset' # input parset file
subbands= 'range(366,484,12)'
model = '/home/deane/models/3C53.model'

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

a = run smooth solutions.py to set phase solutions to zero (to transfer amp only)


"""
