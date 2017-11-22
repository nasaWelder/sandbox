#! /usr/bin/python
import curses
import random
import wordlist
import time

WORDS = wordlist.english
config = {"offset2":random.randint(0,len(WORDS)),
          "offset3":random.randint(0,len(WORDS)),
          "words":WORDS,
          }
          

i = random.randint(0,len(WORDS))
seed = []


def getChoices(step):
    one = wraplist(i)
    two = wraplist(i+config["offset2"])
    three = wraplist(i+config["offset3"])
    
    stdscr.addstr(1, 0, " "*100)
    stdscr.addstr(1, 0, "choose: %s\t%s\t%s" % (one,two,three))
    return one,two,three
    
def wraplist(index):
    global config
    words = config["words"]
    return words[index % len(words)]
    
def getSeed(blah):
    global i
    stdscr.clear()
    #curses.echo()
    stdscr.keypad(True)
    one,two,three = getChoices(i) 
    
    while True:
        c = stdscr.getch()
        if c == ord('1'):
            seed.append(one)
        elif c == ord('2'):
            seed.append(two)
        elif c == ord('3'):
            seed.append(three)
        elif c == ord('p'):
            stdscr.addstr(5,0,"".join([i+" " for i in seed]))
        elif c == ord('l'):
            stdscr.addstr(4,0,"# of seed words entered: %s" % len(seed))
            stdscr.refresh()
            time.sleep(1.5)
            stdscr.addstr(4,0," "*30)
            stdscr.refresh()
        elif c == ord("r"):
            i+=random.randint(0,len(config["words"]))
            one,two,three = getChoices(i)
        elif c == ord('q'):
            break  # Exit the while loop
        elif c == curses.KEY_DOWN:
            i+=1
            one,two,three = getChoices(i)
        elif c == curses.KEY_UP:
            i-=1
            one,two,three = getChoices(i)
        elif c == ord("z"):
            i+=1
            one,two,three = getChoices(i)
        elif c == ord("a"):
            i-=1
            one,two,three = getChoices(i)
        elif c == ord("x"):
            i+=random.randint(10,20)
            one,two,three = getChoices(i)
        elif c == ord("s"):
            i-=random.randint(10,20)
            one,two,three = getChoices(i)
        elif c == ord("c"):
            i+=random.randint(100,202)
            one,two,three = getChoices(i)
        elif c == ord("d"):
            i-=random.randint(100,200)
            one,two,three = getChoices(i)
        else:
            pass

    stdscr.refresh()
    if not len(seed) == 25:
        raise Exception("Invalid Seed length, must be 25 words")

stdscr = curses.initscr()
curses.wrapper(getSeed)
