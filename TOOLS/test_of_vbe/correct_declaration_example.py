#Tai programa, kuri is fail? analysis_of_vbe ir data_of_vbe nustato, koks kuri? tem? svoris egzamine

#VBE 2016 21.2 was cancelled as unreliable: 21.2-1 and 21.2-2 are 9.7 and 25.0 from geometrija and reikiniu sudarymas

# this is an example of row in 'analysis of vbe' file: Vektoriai (7, 16.1, 16.2)
# this is example of row in 'data of vbe' file: 18=8.2 81.4 63.9
from typing import List

class Subject:
    def __init__(self, name: str, skill: str):
        self.name = name
        self.skill = skill

class ProblemAtom:
    def __init__(self, subject: Subject, statement: str, points: int):
        self.subject = subject
        self.statement = statement
        self.points = points
        #self.solvabilities =?
        #self.recalcultion: bool =?

class Problem:
    def __init__(self, parts: List[ProblemAtom], total_points: int = 1):
        self.parts = parts
        self.total_points = total_points

class Exam:
    def __init__(self, year: int, problems: List[Problem], total_points: int = 60):
        self.year = year
        self.problems = problems
        self.total_points = total_points

class ExamSeries:
    #made with intention you can choose any subset of years you want
    def __init__(self, exams: List[Exam]):
        self.exams = exams

#exam or examseries are planned to with adding points or solvabilities for each subject
#

'''
def analyse(analysis_file, data_file, p):
    f=open(r'C:\Users\Vartotojas\Desktop\mscanvas\egzanalysis\\'+analysis_file).read().split('\n')
    PROBLEMS={} #dict of problem codes related with its numbers
    SUBJECTS={}
    NAMES={}
    for n in f:
        start,end=n.index('('), n.index(')')
        name=n[:start]
        NAMES.update({name:0})
        problems=[filter(lambda x: x<>' ',N) for N in n[start+1:end].split(',')]
        print name, problems
        for n in problems:
            if n<>'':
                PROBLEMS.update({n:int(n.split('.')[0].split('-')[0])})
                SUBJECTS.update({n:name})
    print 'PROBLEMS='
    print PROBLEMS
    print 'SUBJECTS='
    print SUBJECTS
    CDS=[]
    XDS=[]
    print set(PROBLEMS.values()), NAMES.keys()
    for n in sorted(set(PROBLEMS.values())):
        xdict={}
        for m in PROBLEMS:
             if PROBLEMS[m]==n:
                xdict.update({m:m.split('-')[0]})
        XDS.append(sorted(xdict.keys()))
        CDS.append([xdict.values().count(N) for N in sorted(set(xdict.values()))]) #e.g. by 2,3,1,1 which means 2pts for 24.1, 3pts for 24.2, 1pts for 24.3, 1pts for 24.4

    print 'CDS='
    print CDS
    print 'XDS='
    print XDS

    def calc(pts_array, p=0.5):
        #given percents of 1, 2, 3 points and so on
        #p=0 WORST CASE (0 points for B if A is not solved)
        #p=1 BEST CASE (1 point for B if A is not solved)
        #p=0.5 REAL CASE (0.5 point for B if A is not solved)
        pts_array=[1-sum(pts_array)]+pts_array
        return [sum(pts_array[i:])+p*sum(pts_array[:i][:-1]) for i in range(1, len(pts_array))]

    PTS=[[float(k)/100. for k in n.split('=')[1].split(' ') if k<>''] for n in open(r'C:\Users\Vartotojas\Desktop\mscanvas\egzanalysis\\'+data_file).read().split('\n')]
    for i in range(len(PTS)):
        if sum(CDS[i])<>len(PTS[i]):
            print 'smth is wrong in problem',i+1, CDS[i],'=', PTS[i],'+',XDS[i]
            break
        print i+1, CDS[i],'=', zip(XDS[i],[round(n,3) for n in PTS[i]])
        print 'recalculations:',
        it=0
        for n in CDS[i]:
            #Remove for check please
            if i<10:
                #ATTENTION. GUESS CASES ELIMINATED
                PTS[i][0]=max(PTS[i][0]-(1-PTS[i][0])/3.,0)
            else:
                PTS[i][it:it+n]=calc(PTS[i][it:it+n],p)
                it+=int(n)
        print zip(XDS[i],[round(n,3) for n in PTS[i]])
        print '-'*50

        for j in range(len(XDS[i])):
            #print SUBJECTS[XDS[i][j]], 'increased by', PTS[i][j]
            NAMES[SUBJECTS[XDS[i][j]]]=NAMES[SUBJECTS[XDS[i][j]]]+PTS[i][j]
    print 'final sum:', sum([sum(n) for n in CDS])

    finals=[]
    suma=0
    for n in f:
        start,end=n.index('('), n.index(')')
        name=n[:start]
        problems=[filter(lambda x: x<>' ',N) for N in n[start+1:end].split(',')]
        print name+' '*(50-len(name)), len([n for n in problems if n<>'']), NAMES[name]
        finals.append((name, len([n for n in problems if n<>'']), NAMES[name]))
        suma+=NAMES[name]
    print 'suma:'+' '*47, suma
    return finals

K=0.0
m2015=analyse('analysis_of_vbe2015.tex','data_of_vbe2015.tex',K)
m2016=analyse('analysis_of_vbe2016.tex','data_of_vbe2016.tex',K)
m2017=analyse('analysis_of_vbe2017.tex','data_of_vbe2017.tex',K)

stat=[m2015,m2016,m2017]
sortof=[]
for i in range(16):
    sortof.append((m2016[i][0], sum([n[i][1] for n in stat]), round(sum([n[i][2] for n in stat])/sum([n[i][1] for n in stat]),2)))
for n in sortof: print n
'''