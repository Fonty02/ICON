def prPurple(prt):
    print("\033[95m{}\033[00m".format(prt))


def prRedMoreString(prt, prt2, prt3):
    print("\033[91m{}\033[00m".format(prt), prt2, prt3)


def prGreenMoreString(prt, prt2, prt3):
    print("\n\033[92m{}\033[00m".format(prt), prt2, prt3)


def prRed(prt):
    print("\033[91m{}\033[00m".format(prt))


def prGreen(prt):
    print("\033[92m{}\033[00m".format(prt))


def prYellow(prt):
    print("\033[93m{}\033[00m".format(prt))


def autopct(pct):
    # shows only values of labers that are greater than 1%
    return ('%.2f' % pct + "%") if pct > 1 else ''