import argparse
import re

YEAR = 13
COMMON_LESSONS = [["CT", "GP", "GPPW", "PE", "PT", "PW",], ["CT", "GP", "PT", "PE"]] # [J1, J2]
SUBJECTS = {
    "AEP" : "Art",
    "BI"  : "Biology",
    "CH"  : "Chemistry",
    "CLL" : "Chinese Language & Literature",
    "CP"  : "Computing",
    "CSC" : "China Studies in Chinese",
    "CSE" : "China Studies in English",
    "EC"  : "Economics",
    "EG"  : "Geography",
    "EH"  : "History",
    "EL"  : "Literature",
    "ELL" : "English Language and Linguistics",
    "GSC" : "General Studies in Chinese",
    "KI"  : "Knowledge & Inquiry",
    "MA"  : "Math",
    "MU"  : "Music",
    "PH"  : "Physics",
}

# argparse setup
parser = argparse.ArgumentParser()
parser.add_argument("query", help="anything goes")
parser.add_argument("-v", "--verbose", help="verbose output",
                    action="store_true")
args = parser.parse_args()
query = args.query.upper()

def get_timetable(ct, filter=None):
    # Fetches timetable from corresponding file and stores as a list
    # i.e. timetable[day][period][lesson][lesson name/detail]
    with open("timetables/%s.txt" % ct, "r") as f:
        timetable = [[[["", ""]] for j in range(20)] for i in range(5)]
        for lesson in f.readlines():
            lesson = lesson.split()
            if len(lesson) == 4: # change to 5 once venue is added
                day, period, subject, type = lesson
                if filter and subject not in filter:
                    continue
                else:
                    s = [subject, type]
            elif len(lesson) == 3: # change to 4 once venue is added
                day, period, subject = lesson
                if filter and subject not in filter:
                    continue
                else:
                    s = [subject, ""]
            if timetable[int(day)-1][int(period)-1] == [["", ""]]: # first lesson of a period
                timetable[int(day)-1][int(period)-1] = [s]
            else:
                timetable[int(day)-1][int(period)-1] += [s]
    return timetable

def print_legend(subjects):
    print "Legend:"
    for s in subjects:
        if s[-1] == "1":
            print "  %s\t- %s (H1)" % (s, SUBJECTS[s[:-1]])
        else:
            print "  %s\t- %s" % (s, SUBJECTS[s])

def print_timetable(timetable):
    max_concurrent_lessons = max(len(period) for day in timetable for period in day)
    if not args.verbose:
        print "┌─────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐"
        print "│     │0800│0830│0900│0930│1000│1030│1100│1130│1200│1230│1300│1330│1400│1430│1500│1530│1600│1630│1700│1730│"
        for i, day in enumerate(timetable):
            print "├─────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤"
            for lesson in range(max_concurrent_lessons):
                s = ""
                for period in day:
                    if len(period) < lesson + 1: # No concurrent lesson at given period
                        s += "    │"
                        continue
                    if period[lesson][0]: # current period not a break
                        s += period[lesson][0].center(4) + "│"
                    else:
                        s += "    │"
                if lesson == 0:
                    print "│ %s │%s" % (["MON", "TUE", "WED", "THU", "FRI"][i], s)
                else:
                    print "│     │" + s
        print "└─────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘"
    else:
        print "┌─────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐"
        print "│     │ 0800 │ 0830 │ 0900 │ 0930 │ 1000 │ 1030 │ 1100 │ 1130 │ 1200 │ 1230 │ 1300 │ 1330 │ 1400 │ 1430 │ 1500 │ 1530 │ 1600 │ 1630 │ 1700 │ 1730 │"
        for i, day in enumerate(timetable):
            print "├─────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤"
            for lesson in range(max_concurrent_lessons):
                s = ""
                for period in day:
                    if len(period) < lesson + 1: # No concurrent lesson at given period
                        s += "      │"
                        continue
                    if period[lesson][0]: # current period not a break
                        if len(period[lesson][1]):
                            s += " ".join(period[lesson]).center(6) + "│"
                        else:
                            s += period[lesson][0].center(6) + "│"
                    else:
                        s += "      │"
                if lesson == 0:
                    print "│ %s │%s" % (["MON", "TUE", "WED", "THU", "FRI"][i], s)
                else:
                    print "│     │" + s
        print "└─────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘"

if re.match(r"\d\d[AS]\d[AS]", query):
    with open("students.txt", "r") as f:
        students = [s.strip().split(",") for s in f.readlines() if query in s]
        combis = {s[3] for s in students}
        timetable = get_timetable(query)
        # print class info
        print "┌───────┐"
        print "│ %s │" % query
        print "└───────┘"
        print "%d subject combination%s found:" % (len(combis), "s"*(len(combis) > 1))
        print "".join(map(lambda x: "  "+x, sorted(combis)))
        print ""
        print_legend({y for x in combis for y in x.split()})
        print_timetable(timetable)
else:
    with open("students.txt", "r") as f:
        results = [s.strip().split(",") for s in f.readlines() if query in s]
        if results:
            # query is a name
            if len(results) > 1:
                print "%d people found with '%s':" % (len(results), query)
                print "\n".join(["\t".join(s) for s in results])
            else:
                ct, gender, name, combi = results[0]
                self_timetable = get_timetable(ct, combi.split() + COMMON_LESSONS[YEAR - int(ct[:2])])
                # print student info
                header = "│ %s (%s) of %s │" % (name, gender, ct)
                print "┌%s┐" % ("─"*(len(header)-6)) # note that vertical lines, unlike pipes, have a length of 3
                print header
                print "└%s┘" % ("─"*(len(header)-6))
                print_legend(combi.split())
                print_timetable(self_timetable)
        else:
            # query not a name
            pass
