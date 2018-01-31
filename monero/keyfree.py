#! /usr/bin/python

"""
copyright (c) 2017-2018 u/NASA_Welder, all rights reserved
feel free to test for your own private use. don't add to any larger projects, I'll figure that out soon, and then give this away to Monero
Monero donations: 
48Zuamrb7P5NiBHrSN4ua3JXRZyPt6XTzWLawzK9QKjTVfsc2bUr1UmYJ44sisanuCJzjBAccozckVuTLnHG24ce42Qyak6

    This prototype script is meant to be a keylogger/screenshot resistant(not fully proofed) tool for restoring wallet on monero-cli.
    Integration into monero still being studied.... I'm a mechanical engineer...
    
    Assumed use-case is on an airgapped computer or liveCD/USB where keyboard or screen are of questionable integrity.
    There is a chance someone/agency could have broken into your house and implemented a physical keylogger/screenshot
    bug on your existing peripherals(keyboard, cables, monitor)
    Also, if you are traveling and don't trust hardware you come across/buy at store, this could help.
    I'm looking for feedback on if this is useful, and if i should spend more time on it. 
    
    usage:
        for now assumes english dictionary
        randomly displays three seed words that are at fixed but random offsets from each other
        press a|z       step up/down alphabetical word list by one entry
        press s|x       step up/down alphabetical word list by random.randint(10,20) entries
        press d|c       step up/down alphabetical word list by random.randint(100,200) entries
        press 1|2|3     add corresponding word to seed list
        press l         briefly list number of words added to list (1.5 seconds)
        press q         exits program, if list is not exactly 25 words, it will raise exception
        
        Danger: press p     will display seed list to screen, don't use in real life for development only       
    


"""
import curses
import random
import wordlist
import time

WORDS = wordlist.english
config = {"offset2":random.randint(0,len(WORDS)),
          "offset3":random.randint(0,len(WORDS)),
          "offset4":random.randint(0,len(WORDS)),
          "offset5":random.randint(0,len(WORDS)),
          "offset6":random.randint(0,len(WORDS)),
          "words":WORDS,
          }
          

i = random.randint(0,len(WORDS))
seed = []


def getChoices(step):
    one = wraplist(step)
    two = wraplist(step+config["offset2"])
    three = wraplist(step+config["offset3"])
    four = wraplist(step+config["offset4"])
    five = wraplist(step+config["offset5"])
    six = wraplist(step+config["offset6"])
    
    stdscr.addstr(1, 0, " "*100)
    stdscr.addstr(0, 0, "                  1            2            3")
    stdscr.addstr(1, 0, "choose: %12s  %12s  %12s" % (one,two,three))
    stdscr.addstr(3, 0, "                  4            5            6")
    stdscr.addstr(4, 0, "        %12s  %12s  %12s" % (four,five,six))
    return one,two,three,four,five,six
    
def wraplist(index):
    global config
    words = config["words"]
    return words[index % len(words)]
    
def getSeed(blah):
    global i
    global config
    stdscr.clear()
    #curses.echo()
    stdscr.keypad(True)
    one,two,three,four,five,six = getChoices(i) 
    
    while True:
        c = stdscr.getch()
        if c == ord('1'):
            seed.append(one)
        elif c == ord('2'):
            seed.append(two)
        elif c == ord('3'):
            seed.append(three)
        elif c == ord('4'):
            seed.append(four)
        elif c == ord('5'):
            seed.append(five)
        elif c == ord('6'):
            seed.append(six)
        elif c == ord('p'):
            stdscr.addstr(6,0,"".join([x+" " for x in seed]))
        elif c == ord('l'):
            stdscr.addstr(5,0,"# of seed words entered: %s" % len(seed))
            stdscr.refresh()
            time.sleep(1.5)
            stdscr.addstr(5,0," "*30)
            stdscr.refresh()
        elif c == ord("r"):
            i+=random.randint(0,len(config["words"]))
            one,two,three,four,five,six = getChoices(i)
        elif c == ord('q'):
            break  # Exit the while loop
        elif c == curses.KEY_DOWN:
            i+=1
            one,two,three,four,five,six = getChoices(i)
        elif c == curses.KEY_UP:
            i-=1
            one,two,three,four,five,six = getChoices(i)
        elif c == ord("z"):
            i+=1
            one,two,three,four,five,six = getChoices(i)
        elif c == ord("a"):
            i-=1
            one,two,three,four,five,six = getChoices(i)
        elif c == ord("x"):
            i+=random.randint(10,20)
            one,two,three,four,five,six = getChoices(i)
        elif c == ord("s"):
            i-=random.randint(10,20)
            one,two,three,four,five,six = getChoices(i)
        elif c == ord("c"):
            i+=random.randint(100,202)
            one,two,three,four,five,six = getChoices(i)
        elif c == ord("d"):
            i-=random.randint(100,200)
            one,two,three,four,five,six = getChoices(i)
        else:
            pass

    stdscr.refresh()
    if not len(seed) == 25:
        raise Exception("Invalid Seed length, must be 25 words")

stdscr = curses.initscr()
curses.wrapper(getSeed)
