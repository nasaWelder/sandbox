import pyqrcode

import base64
import argparse
import hashlib
import math
import os
import chardet
import zlib        

# Monero donations to nasaWelder (babysitting money, so I can code! single parent)
# 48Zuamrb7P5NiBHrSN4ua3JXRZyPt6XTzWLawzK9QKjTVfsc2bUr1UmYJ44sisanuCJzjBAccozckVuTLnHG24ce42Qyak6
def crc(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%x"%(prev & 0xFFFFFFFF)

def restricted_delay(x):
    x = float(x)
    if x <= 0.1 or x > 100.0:
        raise argparse.ArgumentTypeError("%r not in range (0.1, 100.0]"%(x,))
    return x

def send(args):
    PAGE_SIZE = args.bytes

    actualOutDir =  os.path.realpath(os.path.join(args.outDir,os.path.basename(args.infile) + ".QRbatch"))
    os.makedirs(actualOutDir) 
    
    bitPath = os.path.join(actualOutDir,'bits')
    
    with open(args.infile, "rb") as source:
        with open(bitPath, 'wb') as dest:
            dest.write(base64.b64encode(source.read()))
    
    checksum = crc(args.infile)
    print("\n\t%s crc32:\t%s" %(args.infile,checksum))
    print("\n\t%s crc32:\t%s" %(bitPath,crc(bitPath)))
    fsize = os.path.getsize(args.infile)
    htmlfile = open(os.path.join(actualOutDir,"all.html"), "w")
    htmlfile.write("<!DOCTYPE html>\n<html>\n<body>\n") 
    htmlfile.write('<table cellpadding="35">\n<tr><th>qrcode</th><th>file</th></tr>\n')
    print("Encoding:\t",chardet.detect(open(bitPath,"rb").read()))
    print("\tfile size:\t\t%s bytes" % fsize)
    pages = math.ceil(float(fsize) / float(PAGE_SIZE))
    

    
    #with open(args.infile,"rb") as f:
    with open(bitPath, 'rb') as f:
      k = 1
      while True:
        chunk = f.read(PAGE_SIZE)
        if not chunk:
          numQR = k-1
          print("\tQR codes:\t\t%s"%numQR)
          break
        if k>=200:
            print("file really got out of hand, exiting")
            break
        k+=1
    with open(bitPath, 'rb') as f:
      i = 1
      while True:
        heading = args.msgType + "," + str(checksum) + "," + str(i) + "/" + str(int(numQR)) + ":"
        chunk = f.read(PAGE_SIZE)

        #print("Encoding:\t",chardet.detect(chunk))
        if not chunk:
          numQR = i-1
          print("\n\tEnd of file reached, %s QR codes"%numQR)
          print("\tOutput dir:\t\t%s"%actualOutDir)
          break
        if i>=200:
            print("file really got out of hand, exiting")
            break
        page = heading + chunk
        pageName = os.path.basename(args.infile) + "_" + str(checksum) + "_" + str(i) + "of" + ".svg"
        qrPage = pyqrcode.create(page,error="L")
        #print(qrPage.text())
        pagePath = os.path.join(actualOutDir,pageName)
        saved = qrPage.svg(pagePath)        
        i+=1
    htmlfile = open(os.path.join(actualOutDir,"all.html"), "w")
    htmlfile.write("<!DOCTYPE html>\n<html>\n<body>\n") 
    htmlfile.write('<table cellpadding="35">\n<tr><th>qrcode</th><th>file</th></tr>\n')
    for filename in sorted(os.listdir(actualOutDir)):
        #print("filename: ", filename)
        if filename.endswith("of.svg"):
            f2 = filename[:-4] + str(numQR) + filename[-4:]
            os.rename(os.path.join(actualOutDir,filename), os.path.join(actualOutDir,f2))
            htmlfile.write('<tr>\n')
            htmlfile.write('<td><img src = "' + os.path.join(actualOutDir,f2) + '" alt ="cfg" align = "left" height="500" width="500"></td><td>%s</td>\n' % os.path.join(actualOutDir,f2))
            htmlfile.write('</tr>\n')
            
    
    htmlfile.write('</table>\n')
    htmlfile.write("</body>\n</html>\n")
    htmlfile.close()
    
    loopfile = open(os.path.join(actualOutDir,"loop.html"), "w")
    base = os.path.basename(args.infile) + "_" + str(checksum) + "_"
    last = "of" + str(numQR) + ".svg"
    firstImg = base + str(1) + last
    loopfile.write("""
<html>
<head>
</head>

<body>
<div> Directory: %(outDir)s <div>
<div> src name: %(src)s <div>
<div> src crc32: %(check)s <div>

<table cellpadding="5">\n<tr><th></th><th></th></tr>
<td><img src="%(outDir)s/%(firstImg)s" alt="ERROR in QR code processing" width="500" height="500" id="rotator"></td><td><div id="theName"></div></td></table>
<p>Monero donations to nasaWelder (babysitting money, so I can code! single parent)</p>
<p>48Zuamrb7P5NiBHrSN4ua3JXRZyPt6XTzWLawzK9QKjTVfsc2bUr1UmYJ44sisanuCJzjBAccozckVuTLnHG24ce42Qyak6</p>

<script type="text/javascript">
(function() {
    
    var rotator = document.getElementById('rotator'), //get the element
        dir = '%(outDir)s',                              //images folder
        base = '%(base)s',
        last = '%(last)s',
        delayInSeconds = %(delay)s,                           //delay in seconds
        num = 1,                                      //start number
        len = %(N)s;                                      //limit
    setInterval(function(){                           //interval changer
        rotator.src = dir + base + num+ last + '.svg';               //change picture
        rotator.alt = base + num+ last + '.svg';
        document.getElementById('theName').innerHTML = '                 ' +num + ' of ' + len  ;
        num = (num === len) ? 1 : ++num;              //reset if last image reached
    }, delayInSeconds * 1000);
}());
</script>
</body>
</html>
""" % {"outDir" : actualOutDir + "/" ,"firstImg": firstImg,"N" : numQR,"base" :base,"last":last.replace(".svg",""),"src": os.path.basename(args.infile),"check":checksum, "delay": args.delay})
    loopfile.close()
    
def stitch(args):
    actualOutDir =  os.path.realpath(os.path.join(args.outDir,os.path.basename(args.infile) + ".QRstitched"))
    os.makedirs(actualOutDir)
    stitchPath = os.path.join(actualOutDir,os.path.basename(args.infile) +".stitched")
    with open(args.infile, "rb") as source:
        with open(stitchPath, 'wb') as dest:
            dest.write(base64.b64decode(source.read()))

    print("\n\t%s crc32:\t%s" %(args.infile,crc(args.infile)))
    print("\n\t%s crc32:\t%s" %(stitchPath,crc(stitchPath)))


parser = argparse.ArgumentParser(description='Generate bulk qr code')
subparsers = parser.add_subparsers()
sendParser = subparsers.add_parser('send')
sendParser.add_argument('msgType', choices = ["signed_tx","unsigned_tx","watch-only","public_address","raw"],
                    help='heading for qrcodes')
sendParser.add_argument('infile',
                    help='file to be converted to QR code batch')
sendParser.add_argument('--delay', default="1.0", type=restricted_delay,
                    help='delay in seconds after which QR code will transition to next QR code.')
sendParser.add_argument('--bytes', default=1000, choices=xrange(50, 2500), type=int,
                    help='how many bytes to stuff in QR code.')
sendParser.add_argument('--outDir', default="./",
                    help='dir to place QR code batch')
sendParser.set_defaults(func=send)
                    
stitchParser = subparsers.add_parser("stitch")
stitchParser.add_argument('infile',
                    help='file to be converted to QR code batch')
stitchParser.add_argument('--outDir', default="./",
                    help='dir to place stitched together file')                  
stitchParser.set_defaults(func=stitch) 
    
if __name__ == "__main__":
    args = parser.parse_args()
    for arg in vars(args):
        print("\t%s\t\t%s"% (arg, getattr(args, arg)))
    args.func(args)
