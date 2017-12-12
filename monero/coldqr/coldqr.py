import pyqrcode
import argparse
import hashlib
import math
import os

parser = argparse.ArgumentParser(description='Generate bulk qr code')
parser.add_argument('msgType', choices = ["signed_tx","unsigned_tx","watch-only","public_address","raw"],
                    help='heading for qrcodes')
parser.add_argument('infile',
                    help='file to be converted to QR code batch')
parser.add_argument('--outDir', default="./",
                    help='dir to place QR code batch')




PAGE_SIZE = 1500

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def prepare_data(args):


    actualOutDir =  os.path.realpath(os.path.join(args.outDir,os.path.basename(args.infile) + ".QRbatch"))
    os.makedirs(actualOutDir) 
    
    checksum = md5(args.infile)
    print("\n\t%s md5sum:\t%s" %(args.infile,checksum))
    fsize = os.path.getsize(args.infile)
    
    
    htmlfile = open(os.path.join(actualOutDir,"all.html"), "w")
    htmlfile.write("<!DOCTYPE html>\n<html>\n<body>\n") 
    htmlfile.write('<table cellpadding="35">\n<tr><th>qrcode</th><th>file</th></tr>\n')
    
    print("\tfile size:\t\t%s bytes" % fsize)
    pages = math.ceil(float(fsize) / float(PAGE_SIZE))
    print("\t# of QR codes:\t\t%s" % pages)
    with open(args.infile) as f:
      i = 1
      while True:
        heading = args.msgType + "," + str(checksum) + "," + str(i) + "/" + str(pages) + ":"
        chunk = f.read(PAGE_SIZE)        
        if not chunk:
          print("\n\tEnd of file reached")
          print("\tOutput dir:\t\t%s"%actualOutDir)
          break
        if i>=200:
            print("file really got out of hand, exiting")
            break
        page = heading + chunk.decode().encode('ascii',errors='ignore')
        pageName = os.path.basename(args.infile) + "_" + str(checksum) + "_" + str(i) + "of" + str(int(pages)) + ".svg"
        qrPage = pyqrcode.create(page,error="L")
        #print(qrPage.terminal())
        pagePath = os.path.join(actualOutDir,pageName)
        saved = qrPage.svg(pagePath)
        htmlfile.write('<tr>\n')
        htmlfile.write('<td><img src = "' + pagePath + '" alt ="cfg" align = "left" height="500" width="500"></td><td>%s</td>\n' % pageName)
        htmlfile.write('</tr>\n')
        i+=1
    htmlfile.write('</table>\n')
    htmlfile.write("</body>\n</html>\n")
    htmlfile.close()

    
if __name__ == "__main__":
    args = parser.parse_args()
    for arg in vars(args):
        print("\t%s\t\t%s"% (arg, getattr(args, arg)))
    prepare_data(args)
