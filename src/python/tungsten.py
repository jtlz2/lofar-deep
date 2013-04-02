#!/usr/bin/python

"""
Tungsten (1944) United Kingdom - carrier-borne air attack on Tirpitz
JZ, after Roger Deane, after Jonathan Zwart, after Roger Deane
2 April 2013
"""

import os,sys
import subprocess


user = os.getenv('USER')
sty = os.getenv('STY')

BASH='/bin/bash'

OK={0:'success',1:'fail',134:'WTF',-1:'minus'}

opslist=['t','u','b','v','g','s','d','c','i','f','x']
opsdict={'t':'transfer','u':'unpack','b':'bbs','d':'backup',\
            'c':'clip','i':'image','f':'fits','w':'wrap',\
            's':'bbst','v':'vds','g':'gds','x':'bdsm'}
opsmap={'transfer':'t','unpack':'u','bbs':'b','backup':'d',\
            'clip':'c','image':'i','fits':'f','wrap':'w',\
           'bbst':'s','vds':'v','gds':'g','bdsm':'x'}


print '#%s' % ''.join(['-' for i in range(79)])

#-------------------------------------------------------------------

class bcolors:
    """
    http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = "\033[1m"
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.BOLD=''



#-------------------------------------------------------------------
#http://blog.mathieu-leplatre.info/colored-output-in-console-with-python.html
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)


def printout(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)

#-------------------------------------------------------------------

def flatten(l):
   """
   http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
   """
   import collections
   for el in l:
       if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
           for sub in flatten(el):
               yield sub
       else:
           yield el


#-------------------------------------------------------------------

def fetchHistory(logf,SB):

   """
   Query progress.log and return history for this SB
   """

   #logf='progress.log'
   log=open(logf,'r')
   logs=[line.strip() for line in log.readlines()]
   log.close()

   passed=uniqf7([opsmap[line.split()[2]] for line in logs \
                 if str(SB) in line and 'success' in line])
   #print passed

   sbhistory=passed
   return sbhistory

#-------------------------------------------------------------------

def updateHistory(logfHandle,subBand,process,operation):
   """                                                                          
   """
   success=-1
   if process is not None:
       print '(pid %i)' % process.pid
       process.wait()
       success=process.poll(); pid=process.pid
   else:
       # This is a fake pass-through for when no process is actually called     
       pid=0
       success=0
   line = 'SB%03i %i %s %i %s' \
       % (subBand,pid,opsdict[operation],success,OK[success])
   logfHandle.write('%s\n'%line); logfHandle.flush()

#-------------------------------------------------------------------   

def updateHistoryOld(logfHandle,subBand,process,operation):
   """
   """
   success=-1
   print '(pid %i)' % process.pid
   process.wait()
   success=process.poll(); pid=process.pid
   line = 'SB%03i %i %s %i %s' \
       % (subBand,pid,opsdict[operation],success,OK[success])
   logfHandle.write('%s\n'%line); logfHandle.flush()

#-------------------------------------------------------------------

def uniqf7(seq):
   """
   http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
   """
   seen = set()
   seen_add = seen.add
   return [ x for x in seq if x not in seen and not seen_add(x)]

#-------------------------------------------------------------------

def fetchChannelMapping(verbose=False):
   """
   Map LOFAR SBs <-> 3C53 SBs <-> XMM-LSS SBs

   Frequencies to be added -
       see http://www.astron.nl/radio-observatory/astronomers/users/technical-information/frequency-selection/station-clocks-and-rcu

   Usage:

   lofar2beams,cal2field,field2cal,cal2lofar,field2lofar
       = tungsten.fetchChannelMapping()

   Returns the dictionaries:

   lofar2beams[lofar_chan]=(field_chan,cal_chan)
   cal2field[cal_chan]=field_chan
   field2cal[field_chan]=cal_chan
   cal2lofar[cal_chan]=lofar_chan
   field2lofar[field_chan]=lofar_chan
   
   """

   # Check (from pbworks):
   #High freq. 305  473  360  170.312 
   #Medium freq. 154  424  209  140.820 
   #Low freq. 079  400  134  126.172 

   calibrator_chans=[55, 57, 63, 66, 68, 69, 71, 72, 73, 76, 77, 79, 83, 84, 85, 86, 90, 92, 99, 100, 101, 103, 104, 107, 108, 110, 117, 119, 121, 122, 123, 126, 130, 131, 134, 136, 137, 140, 141, 145, 147, 150, 151, 156, 157, 161, 162, 168, 170, 175, 176, 178, 185, 188, 196, 197, 201, 202, 209, 213, 217, 221, 224, 230, 235, 238, 242, 246, 254, 255, 258, 259, 260, 264, 268, 269, 271, 274, 278, 279, 280, 283, 286, 291, 295, 297, 301, 306, 307, 312, 313, 314, 317, 319, 322, 323, 325, 328, 329, 332, 341, 343, 344, 346, 347, 352, 356, 360, 361, 364, 369, 371, 382, 383, 390, 398, 401, 404, 411, 412, 414, 419]

   lofar2beams={}; cal2field={}; field2cal={}; cal2lofar={}; field2lofar={}

   zero_chan=55
   num_field_chans=366
   num_total_chans=488
   for nf in range(zero_chan,zero_chan+num_total_chans):
      lofar_chan=nf
      field_chan=lofar_chan-zero_chan
      field2lofar[field_chan]=lofar_chan
      if lofar_chan in calibrator_chans:
          cal_chan=num_field_chans+calibrator_chans.index(lofar_chan)
          if verbose:
              print lofar_chan, field_chan, ' C ', cal_chan
          lofar2beams[lofar_chan]=(field_chan,cal_chan)
          cal2field[cal_chan]=field_chan
          field2cal[field_chan]=cal_chan
          cal2lofar[cal_chan]=lofar_chan
      else:
          if verbose:
              print lofar_chan, lofar_chan-zero_chan, ' - ', ' - '
          lofar2beams[lofar_chan]=(field_chan,None)
          field2cal[field_chan]=None

   return lofar2beams,cal2field,field2cal,cal2lofar,field2lofar


#-------------------------------------------------------------------

if __name__ == '__main__':

    if (len(sys.argv) < 2):
        print 'usage: %s initparmsXXXX.py \n \
        see initparmsXXXX.py to set up reduction parameters \n' % sys.argv[0]
	sys.exit(0)
    else:
        pass

    ##### import inital parameters/directory names
    target=sys.argv[1].split('.')[0].split('initparms')[1]

    if target == 'CAL':
        from initparmsCAL import *
        print Ldir
        #X = __import__(sys.argv[1])
        os.chdir(Ldir)
        print 'imported CAL parms'
        print 'Lnum',Lnum
    elif target == 'FIELD':
        from initparmsFIELD import *
        os.chdir(Ldir)
        print 'imported FIELD parms'
        print 'Lnum',Lnum


    assert(sty is not None), 'Run %s inside screen!' % sys.argv[0]
    assert(sys.argv[1] is not None), 'input initparms.py file'

    SBs=list(flatten(eval(subbands)))
    if convertsb:
        lofar2beams,cal2field,field2cal,cal2lofar,field2lofar=\
        fetchChannelMapping(verbose=False)
        print SBs
	print cal2field
	#SBs=[cal2field[sb] for sb in SBs]

#-------------------------------------------------------------------

            #ops=[op for op in list(operations) if op is not ' ' and op is not ',']
    ops=[op for op in list(operations) if op is not ' ' and op is not ',']
    opsreq=sorted([opsdict[key] for key in opsdict.keys() if key in ops])
    print 'Operations are:',opsreq

    logfile = os.path.join(wdir,'progress.log')
    log=open(logfile,'a')

    if 's' in ops:
       lofar2beams,cal2field,field2cal,cal2lofar,field2lofar\
           = fetchChannelMapping(verbose=False)
       SBs=[cal2field[sb] for sb in SBs]
       #ops=[op for op in list(operations) if op is not ' ' and op is not ',']

    # This import is slow - only do it once (move this to above)        
    if 'x' in ops:
        import lofar.bdsm as bdsm

#-------------------------------------------------------------------

# Set up MPI
    # Usage: mpirun -n 8 ./tungsten.py initparmsXXXX.py
    from mpi4py import MPI
    world=MPI.COMM_WORLD
    rank=world.rank
    size=world.size
    print 'MPI parameters are rank,size = (%i,%i)' % (rank,size)
    my_SBs=SBs[rank::size]

#-------------------------------------------------------------------

    for sb in my_SBs:
        print "Processor %d handling SB %03i" % (rank,sb)
        sbh=fetchHistory(logfile,sb)
        # Fetch tar file
        objectf=os.path.join(rawdir,\
            os.path.join(Lnum,'%s_SB%03i_uv.dppp.MS.tar'%(Lnum,sb)))
        targetf=os.path.join(wdir,\
            '%s_SB%03i_uv.dppp.MS.tar'%(Lnum,sb))
        if 't' in ops and 't' in 't':
           cmdcp = 'cp %s %s' \
               % (objectf,wdir)
           if os.path.exists(targetf):
              print '%s already exists - skipping transfer' % targetf
              continue
           print cmdcp
	   print >>cmdhistfile,cmdcp
           proc=subprocess.Popen(cmdcp,shell=True,executable=BASH,
                                 stdout=subprocess.PIPE)
           updateHistory(log,sb,proc,'t')

        # Unpack the tar file
        sbh=fetchHistory(logfile,sb)
        if 'u' in ops and 't' in sbh:
           unpackf=os.path.join(wdir,'%s_SB%03i_uv.dppp.MS.tar'%(Lnum,sb))
           # Check the data structure within the tar file
           cmddrytar = 'tar -tvf %s' % unpackf
           print >>cmdhistfile,cmddrytar
           proc=subprocess.Popen(cmddrytar,shell=True,executable=BASH,\
                                    stdout=subprocess.PIPE)
           print ('dry-run unpack')
           print '(pid %i)' % proc.pid
           while True:
              line = proc.stdout.readline()
              if 'data' in line:
                 tarform='data'
              else:
                 tarform='non'
              break
           proc.wait()

           # Now do the untar
           if tarform == 'data':
              unpackedf=os.path.join(wdir,os.path.join(os.path.join(\
                    tarform,Lnum),os.path.basename(\
                    os.path.splitext(unpackf)[0])))
              cmdtar = 'tar -xvf %s -C %s ' % (unpackf,wdir)
           elif tarform == 'non':
              unpackedf=os.path.splitext(unpackf)[0]
              projdir=os.path.join(os.path.join(wdir,'data'),Lnum)
              cmdtar = 'tar -xvf %s -C %s ' % (unpackf,projdir)

           if os.path.exists(unpackedf):
              print '%s already exists - skipping unpack' % unpackedf
              continue
           print cmdtar
           print >>cmdhistfile,cmdtar
           proc=subprocess.Popen(cmdtar,shell=True,executable=BASH,\
                                    stdout=subprocess.PIPE)
           updateHistory(log,sb,proc,'u')

           #now delete .tar file
           delcmd = 'rm -fr  ' + unpackf
           print >>cmdhistfile,delcmd
           proc=subprocess.Popen(delcmd,shell=True,executable=BASH,\
                                    stdout=subprocess.PIPE)
           print '\n \n cleaning out tar files.... \n \n'
           proc.wait()
           
    #for sb in SBs:

        filename ='%s_SB%03i_uv.dppp.MS.tar' % (Lnum,sb)
        stem=os.path.join(os.path.join(os.path.join(wdir,'data'),Lnum),filename)
        msin=os.path.join(wdir,os.path.splitext(stem)[0])

        vds = '%s.vds' % msin
        gds = '%s.gds' % msin   # these only work per SB atm

        # Set up the VDS
        sbh=fetchHistory(logfile,sb)
        if 'v' in ops:
            cmdmkvds = 'makevds %s %s' % (clusterdesc,msin)
            print cmdmkvds
            if os.path.exists(vds):
               print '%s already exists' % vds
               continue
            print >>cmdhistfile,cmdmkvds
            proc = subprocess.Popen(cmdmkvds,shell=True,executable=BASH,
                                    stdout=subprocess.PIPE)
            updateHistory(log,sb,proc,'v')

        # Set up the GDS
        sbh=fetchHistory(logfile,sb)
        if 'g' in ops and 'v' in sbh:
            cmdcombvds = 'combinevds %s %s' % (gds,vds)
            print cmdcombvds
            if os.path.exists(gds):
               print '%s already exists' % gds
               continue
            print >>cmdhistfile,cmdcombvds
            proc = subprocess.Popen(cmdcombvds,shell=True,executable=BASH,
                                    stdout=subprocess.PIPE)           
            updateHistory(log,sb,proc,'g')


        # Carry out BBS, transferring solutions from calibrator
        sbh=fetchHistory(logfile,sb)
        if 's' in ops and 'g' in sbh:
            assert(L2num is not None)         
            model=dummymodel
            bbstlogf=os.path.join(os.path.join(\
                  os.path.join(wdir,'data'),Lnum),'bbst_SB%03i.txt' % sb)
            BBS='calibrate -f -v'
            key='%s_%03i' %(Lnum,sb)
            db='ldb001'
            sb_cal=field2cal[sb]
            if sb_cal is None:
               print 'Field SB%03i has no corresponding calibrator S - skippingB' % sb
               continue
            else:
               print 'Paired field SB%03i <-> SB%03i calibrator' % (sb,sb_cal)

            cal_dir= cal_dir= os.path.join(os.path.join(L2dir,'data'),L2num) # directory of calibrator MSs. Can be same as working directory 
            field_dir= os.path.join(os.path.join(wdir,'data'),Lnum) # probably wdir
            calibrator=os.path.join(cal_dir,'%s_SB%03i_uv.dppp.MS/instrument'\
                % (L2num,sb_cal)) # actual current calibrator SB MS
	


	    if (SetPhaseZero):
 
		calibratorPhaseZero=os.path.join(cal_dir,'%s_SB%03i_uv.dppp.MS/instrumentPhaseZero'% (L2num,sb_cal))
                cmdsmo = 'python smoothcal.py %s %s'% (calibrator,calibratorPhaseZero)
            	print >>cmdhistfile, cmdsmo
            	proc = subprocess.Popen(cmdsmo,shell=True,executable=BASH,stdout=subprocess.PIPE)
		proc.wait()
	    	calibrator=os.path.join(cal_dir,'%s_SB%03i_uv.dppp.MS/instrumentPhaseZero'% (L2num,sb_cal))



            cmdcal = '%s --key %s --cluster-desc %s --db %s --db-user postgres --instrument-db %s %s %s %s %s > %s' % (BBS,key,clusterdesc,db,calibrator,gds,parsetin_trans,model,field_dir,bbstlogf)
            print cmdcal
            # Need to implement a better success check:
            if 's' in sbh:
               print 'BBS transfer already in the history log (see %s)' \
                   % bbstlogf
               continue
            print >>cmdhistfile,cmdcal
            proc = subprocess.Popen(cmdcal,shell=True,executable=BASH,
                                    stdout=subprocess.PIPE)
            updateHistory(log,sb,proc,'s')


        # Carry out BBS self-cal
        sbh=fetchHistory(logfile,sb)
        if 'b' in ops and 'u' in sbh:
            bbslogf=os.path.join(os.path.join(\
                  os.path.join(wdir,'data'),Lnum),'bbs_SB%03i.txt' % sb)
            BBS='calibrate-stand-alone -f -v'
            cmdcal = '%s %s %s %s > %s' \
                % (BBS,msin,parsetin,model,bbslogf)
            print cmdcal
            # Need to implement a better success check:
            if 'b' in sbh:
               print 'BBS already in the history log (see %s)' % bbslogf
               continue
            print >>cmdhistfile,cmdcal
            proc = subprocess.Popen(cmdcal,shell=True,executable=BASH,
                                    stdout=subprocess.PIPE)
            updateHistory(log,sb,proc,'b')

        # Backup the self-cal'ed MS
        sbh=fetchHistory(logfile,sb)
        if 'd' in ops and ('b' in sbh or 's' in sbh):
            print msin
            cmdbackup = 'cp -r %(ms)s %(ms)s.bkp' % {'ms':msin}
            print cmdbackup
            if os.path.exists('%s.bkp'%msin):
               print 'MS %(ms)s has already been backed-up to %(ms)s.bkp' \
                   % {'ms':msin}
               continue
            print >>cmdhistfile,cmdbackup
            proc = subprocess.Popen(cmdbackup,shell=True,executable=BASH,\
                                       stdout=subprocess.PIPE)
            updateHistory(log,sb,proc,'d')

        # Clip the data
        sbh=fetchHistory(logfile,sb)
        if 'c' in ops and 'd' in sbh:
            ## WHY DOESN'T THIS GIVE ANY STDOUT????
            cmdclip = 'python clipcal.py --ms=%s/' % msin
            print cmdclip
            if 'c' in sbh:
               print 'Clip already in the history log - skipping'
               continue
	    print >>cmdhistfile,cmdclip
            proc = subprocess.Popen(cmdclip,shell=True,executable=BASH,\
                                       stdout=subprocess.PIPE)
            updateHistory(log,sb,proc,'c')


        # Image the data
        sbh=fetchHistory(logfile,sb)
        assert(niters is not None)
        imgout = '%s_niter%s.img' % (msin[:-8],niters)
        if 'i' in ops and 'c' in sbh:
            imagelogfile = '%s.txt' % imgout
            imagecmd = 'source /home/tasse/jaws22/init.sh; awimager ms=%s image=%s weight=%s robust=%.1d npix=%i cellsize=%s data=CORRECTED_DATA padding=1. niter=%s stokes=I operation=mfclark oversample=5 wmax=%i cyclefactor=1.5 gain=0.1 timewindow=300 ApplyElement=0  > %s '%(msin,imgout,weighting,robust,npix,cellsize,niters,wmax,imagelogfile) 
            print imagecmd
            if os.path.exists('%s.residual'%imgout):
               print '%s.residual already exists - skipping imaging' % imgout
               continue
            print >>cmdhistfile,imagecmd
            proc = subprocess.Popen(imagecmd,shell=True,executable=BASH,\
                                       stdout=subprocess.PIPE)
            updateHistory(log,sb,proc,'i')


        # Convert the CLEANed MS image to FITS
        sbh=fetchHistory(logfile,sb)
        if 'f' in ops and 'i' in sbh:
            img2fitscmd = \
                'python img2fits.py %(im)s.restored.corr %(im)s.restored.corr.fits'\
                %{'im':imgout}
            print img2fitscmd
            if os.path.exists('%s.restored.corr.fits'%imgout): continue
            print >>cmdhistfile,img2fitscmd
            proc = subprocess.Popen(img2fitscmd,shell=True,executable=BASH,\
                                       stdout=subprocess.PIPE)
            updateHistory(log,sb,proc,'f')

        # Run PyBDSM and output maps,stats etc.                                 
        # This could be run directly on the MS.restored.corr in fact            
        if 'x' in ops and 'f' in sbh:
            if not os.path.exists('%s.restored.corr.fits'%imgout):
                print '%s.restored.corr.fits is missing!'%imgout
                continue
            do_rms_map=True
            kappa_clip=3.0
            print 'Launching PyBDSM...'
            ncores=None # i.e. auto
            clobber=True
            psf_vary_do=False
            img=bdsm.process_image('%s.restored.corr.fits'%imgout,\
                rms_map=do_rms_map,kappa_clip=kappa_clip,\
                psf_vary_do=psf_vary_do,ncores=ncores)

            img_format='fits'
            img.export_image(img_type='rms',img_format=img_format,clobber=clobber)
            img.export_image(img_type='ch0',img_format=img_format,clobber=clobber)
            try:
                img.export_image(img_type='psf_pa',img_format=img_format,clobber=clobber)
            except AttributeError:
                print 'Could not write psf_pa image for some reason..'

            catalog_type='srl'
            img.write_catalog(format='ascii',clobber=clobber,catalog_type=catalog_type)
            img.write_catalog(format='fits',clobber=clobber,catalog_type=catalog_type)

            catalog_type='gaul'
            img.write_catalog(format='ascii',clobber=clobber,catalog_type=catalog_type)
            img.write_catalog(format='fits',clobber=clobber,catalog_type=catalog_type)
            img.write_catalog(format='bbs',clobber=clobber,catalog_type=catalog_type)

            if ncores is None: ncores=8 
            lines = \
                ['==== Stats for PyBDSM run ===========================\n',
                 'File %s' % img.filename,
                 'Frequency / MHz      = %f' % (img.frequency/1.0e6),
                 'Mask present           %s' % str(img.masked),
                 'rms_map                %s' % str(do_rms_map),
                 'psf_vary               %s' % str(psf_vary_do),
                 'ncores                 %i' % ncores,
                 'Raw mean / mJy       = %f' % (1.0e3*img.raw_mean),
                 'Raw rms / mJy        = %f' % (1.0e3*img.raw_rms),
                 'kappa_clip /sigma    = %4.2f' % kappa_clip,
                 'Clipped mean / mJy   = %f' % (1.0e3*img.clipped_mean),
                 'Clipped rms / mJy    = %f' % (1.0e3*img.clipped_rms),
                 'Max value / Jy       = %f' % img.max_value,
                 '            at (x,y) = %i,%i' % img.maxpix_coord,
                 'Min value / Jy       = %f' % img.min_value,
                 '            at (x,y) = %i,%i' % img.minpix_coord,
                 '=====================================================']
            for line in lines:
                print line
            statsf='%s.stats' % imgout
            with open(statsf,'w') as stats:
                stats.writelines(['%s\n'%line for line in lines])
            updateHistory(log,sb,None,'x')


        # Check the complete history for the given SBs
        # Copy the FITS file to tarimgs/
        sbh=fetchHistory(logfile,sb)
        if 'w' in ops: # and 'i' in sbh
            for op in opslist:
                if op in sbh:
                    line = '[ ok ] SB%03i %s\n' % (sb,opsdict[op])
                    printout(line,GREEN)
                else:
                    line = '[ no ] SB%03i %s\n' % (sb,opsdict[op])
                    printout(line,RED)
            print


            #        if (scpMaps):
            
            #if True:
            #   print 'not yet implemented (%s)' % opsdict['w']
            #   continue
            #scpcmd = 'cp %s.restored.corr.fits ./tarimgs/'%imgout
            #proc = subprocess.Popen(scpcmd,shell=True,executable=BASH)
            #updateHistory(log,sb,proc,'w')

    log.close()
    cmdhistfile.close()

    #return
#------------------------------------------------------------------------------
#if __name__ == '__main__':
#   main()
    sys.exit(0)

#------------------------------------------------------------------------------
