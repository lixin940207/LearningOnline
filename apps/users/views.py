from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Course
from apps.operations.models import UserFavorite, UserMessage, Banner, UserProfile
from apps.organizations.models import CourseOrg, Teacher
from apps.users.forms import LoginForm, UploadImageForm, UserInfoForm, ChangePwdForm, RegisterPostForm


def message_nums(request):
    """
    Add media-related context variables to the context.
    """
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class MyMessageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "message"
        for message in messages:
            message.has_read = True
            message.save()

        # 对讲师数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=5, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            "current_page": current_page
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_teacher"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            org = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(org)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
            "current_page": current_page
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_org"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
            "current_page": current_page
        })


class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        # my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            # "my_courses":my_courses,
            "current_page": "mycourse"
        })


class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd1)
            user.save()
            # login(request, user)

            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        return render(request, "usercenter-info.html", {
            "current_page": "info"
        })

    def post(self, request, *args, **kwargs):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(userinfo_form.errors)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all()[:3]
        return render(request, "register.html", {
            "banners": banners,
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            nick_name = register_post_form.cleaned_data["nick_name"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个用户
            user = UserProfile(username=nick_name, nick_name=nick_name)
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "register.html", {
                "register_post_form": register_post_form
            })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        banners = Banner.objects.all()[:3]
        next = request.GET.get("next", "")
        return render(request, "login.html", {
            "next": next,
            "banners": banners,
        })

    def post(self, request, *args, **kwargs):
        # form validation
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # 使用django提供的内置方法来判断用户名和密码是否存在
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # check if user can login
                login(request, user)
                # return render(request, "index.html")
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {
                    "msg": "Username or password incorrect.",
                    "login_form": login_form
                })
        else:
            return render(request, "login.html", {"login_form": login_form})


class BehaviorView(View):
    def get(self, request, *args, **kwargs):
        articles = []
        articles.append(Article(id="introduction", title="introduction",
                                content="Thank you for giving me opportunity to interview with you today. Let me start from education, I majored at software engineering at Wuhan University and I went to France in 2016 to study Data Science at Telecom Paristech.I was passionate by computer, electronic products, games when I was young, that's why I have been always on this way to accumulate my tech stack from time to time. In the last year of master, I did an internship at Total as a data analyst, the main task is to clean and process production data and applied Machine Learning on those in order to better locate problems. After that, I went to China to work at a leading nlp AI company as an algorithm engineer, as for my daily duty, one part is researching and integrating NLP models into production, another is backend development in Python, Django, Flask, Mysql etc. Besides development work, I also participated in most stages of life cycle of a product: analyzing business requirements, POC, unit testing and integration testing, and product delivery.Outside of work, I never stayed at the comfort zone, I learned Java, Scala and big data technologies and finished a real-time processing project on my own, and I also learned some frontend technologies, and finished several Django projects from font to back on my own. Recently I passed Spark and Hadoop Developer Certificate and AWS certified developer Certificate.<sep>About my characteristics,  I am very autonomy and enjoy learning new things, back in my undergraduate years, I got national prize scholarship every year and graduated with the first place of the grade, when I applied for Telecom Paristech, I was awarded the Eiffel scholarship by French minister, of which I am the proudest and I would keep on studying and working hard all my life to be worthy of this honor. <sep>That's a simple introduction of my education, experience and myself. Thank you for your time.I'd love to learn more about the job and happy to answer any questions you may have regarding my qualification."))
        articles.append(Article(id="datagrand", title="DataGrand",
                                content="DataGrand provides b2b business to business nlp solution services, for example: information extraction, text classification, sentiment analysis etc. our clients are companies like banks, audit companies, securities companies we help them to simplify manual text reading time. Like auditors, they have tons of documents to read everyday, if models can extract the keywords for them can simplify their work.<sep>About the products, one part is that clients gave us all their data, we use the data to tune models and then integrate into the whole text processing system; another is that customer's data is confidential, so they need an auto learning platform which we integrated different machine learning and deep learning algorithms inside, and they can input their own files in the system, customize model parameters in the front end, train and predict their own models."))
        articles.append(Article(id="why-come-back", title="为什么回国又回来",
                                content="That may a long story, but I will make it short. Before I graduated from Telecom in 2018, I tried to seek job opportunities both in France and in China, and finally I got several offers, I took all factors into considerations and decided to work at DataGrand at Shanghai, and they gave me a lot opportunities to express myself and develop myself.<sep>but the last year, my boyfriend had to go back to France due to work change, I was kind of reluctant to leave so I stayed there until all the projects I participated finished, then I arrived in France on November and started job hunting in paris recently.<sep>I have signed civil solidarity pact with my boyfriend and we decided to settle down our life here. In France, both of us can have a good career development, balance our family life and work life."))
        articles.append(Article(id="recent-project", title="你领导的项目",
                                content="I would like to talk about a recent professional project"
                                        "<sep>before that, let me simply explain a little what does my previous company do."
                                        "DataGrand provides b2b nlp solution services, "
                                        "for example: information extraction, text classification, sentiment analysis "
                                        "etc. our clients are companies like banks, audit companies, securities "
                                        "companies we help them to simplify manual text reading time. Like auditors, "
                                        "they have tons of documents to read everyday, if models can extract the "
                                        "keywords for them can simplify their work.<sep>I am in charge of the project "
                                        "with a big security company. The client wanted an auto learning nlp platform "
                                        "which enable their staffs to train their own nlp models easily through a user friendly interface, (user can upload labeled data or directly label data on the interface) "
                                        "we integrated many machine learning and deep learning algorithms "
                                        "inside the system for users to select, they customize parameters on the frontend, so customers can do "
                                        "nlp analysis without writing any code or having deployment issues."
                                        "I was responsible for the application server, receives requests from font-end, does the business logic, connects with MySQL, Redis as Cache, adopted Celery and Rabbitmq as asynchronous task queue architecture."
                                        "<sep>We implemented the machine learning or deep learning algorithms in dockers "
                                        "seperately, and expose parameters in the frontend to users, that is for "
                                        "their staff who know business very well but not so skilled at development, "
                                        "so they can tune models without writing any code or deployment "
                                        "issues.<sep>This was also the first time I lead a team(there are 4 juniors "
                                        "and interns), the biggest difficulty for me is the frequent requirement changes,"
                                        "at first, "
                                        "I only communicated with my project manager, he listed the requirements that "
                                        "the clients wanted and then I reforwarded these information to my teammates "
                                        "and delegated tasks and after one sprint, we showed some results to clients, "
                                        "but clients were not very satisfied and came up with some new ideas and even "
                                        "overturned some features that he said before. Things like that happened 2 "
                                        "sprints later, I realized that maybe the communication between me and "
                                        "project manager and clients are not efficient, and sometimes clients didn't "
                                        "have a very specific and clear requirements, and they didn’t have coding "
                                        "experience, they may have some unrealistic ideas.<sep>Then I privately hold discusses a lot of times with my team, summarized several feasible solutions and thier advantages and disadvantages, time cost and machine cost"
                                        "then I went to clients' company and visited them in person"
                                        "understand what the client wanted, guide them towards the feasible solutions that we made, explain in a development perspective, "
                                        "explain some features can be easy to implement but others may need a bit more time."
                                        "finally our honest and delivery of high quality product in time won the trust and a long term collaboration with the client company. "))
        articles.append(Article(id="personal-projects", title="私人项目",
                                content="[welearning]<sep>I have developed a personal Django web system on my own.  I "
                                        "deployed it on aws, you can have a look at it through the address I noted on "
                                        "my resume.<sep>The original intention to do this project is to test my "
                                        "skills to architect a whole project from front to end and my modeling "
                                        "ability to split initial requirements to different classes and operations. "
                                        "That is an online course platform, there are four main apps: users, "
                                        "organizations and courses, and operations and use MVC pattern to implement "
                                        "logic. And on the other hand, being a backend engineer should be able to "
                                        "know the knowledge of frontend, that's a good chance for me to hand on these "
                                        "html, css, js technologies.<sep>Why online course platform?I benefit a lot "
                                        "from these online course platform, I am a person that desire to learn new "
                                        "things, thank to these online courses, I can follow the top courses from top "
                                        "universities especially when I was out of school, so I want to do a project "
                                        "of my interest domain<sep>  "
                                        "<sep>[real-time user behavior analysis]<sep>"
                                        "Considering that the tech stack of this job is more about big data, I want to talk about one of my private projects of big data"
                                        "I have learned big data at school, but after I started working, "
                                        "I have no opportunities to contact this field, but I have been always "
                                        "interested in big data, so in my private time I self learned java scala, "
                                        "hadoop, spark, kafka etc, after learned the basic theory, I decided to work "
                                        "on this realtime user behavior analysis project to string together many "
                                        "component in the Hadoop Ecosystem.First, I write a program to fake tons of "
                                        "user behaviors(click items, collect items, add coupon, buy) from different "
                                        "location via different devices. Then implemented a logserver to collect "
                                        "these user data and send them to Kafka, based on the high-throughput, "
                                        "low-latency features of Kafka, data can be in near real time be transformed "
                                        "to downstream server, that is sparkstreaming, it will do the business logic: "
                                        "calculate DAU, transaction amount, detect abuse behavior etc., "
                                        "then the results will be saved to Hbase and  Elasticsearch for further "
                                        "query.<sep>I deployed the project on Cloud, the qps is around 10k qps, "
                                        "one instance for nginx, and 3 Hadoop nodes for handling the "
                                        "requests.<sep>That is a basic logic of this project, the main mission for me "
                                        "is to better understand how works big data technologies. I found that "
                                        "joining an exam related to what I'm learning is also very practical, "
                                        "it pushes you to move forward and systematically learn knowledge of this "
                                        "field, so I signed up the Hadoop and Spark Certification Test and finally "
                                        "passes it.Although I didn't use big data as my future work, it’s always good "
                                        "to learn new things.<sep>  <sep>[比赛]<sep>That competition is hold by a "
                                        "famous Chinese Conference in the field of nlp. The mission is to xtract "
                                        "structured data from executive personnel change announcement like personnel "
                                        "name, sex, position, reason for leaving, successor name etc. the essence is "
                                        "very similar to what I did in the last job, information extraction. I "
                                        "applied our daily deep-learning networks as baseline, and did some model "
                                        "tunning, model fusing works and regular expression, we got the second prize "
                                        "in the end. <sep>The difficulties may be that participating competitions is "
                                        "not like solving real problems for clients, in competitions if we want to "
                                        "get good scores we need to fuse many many models together, during that "
                                        "period of time, we are like train models day and night, we often need to "
                                        "wake up in the midnight to check if model training succeed or fail, "
                                        "converge or not, we ate and slept together with workmates, I often miss that "
                                        "time, it’s valuable to have someone fight alongside."))

        articles.append(Article(id="about-company", title="Luko是做什么的，为什么想加入",
                                content="Luko is a company specializing in house insurance and protection and also the fastest growing insurance company in Europe. Luko wants to provide the most simple and most transparent service of assurance which reinvent the traditional assurance. Besides the very caring insurance service, luko has leveraged their product and artificial intelligence technologies, such as the smart sensor, it can analyze consummation of electricity, water etc in realtime.<sep>Why you want to join us? <sep>I want to join Luko because I believe what the company provide is meaningful to everyone, house is the most essential thing in our life, whatever what happened, Luko can provide the most reliable and fastest service. Besides the most caring insurance service, you have leveraged artificial intelligence and your product to build the strong AI powered technologies to avoid accident.I have experience in both backend development and AI, using my experience and knowledge, I can better understand the products of company and communicate well between teams, so I want to join you, I want a fast growing and Humanitarian company.<sep>Whatever I can join you or not, I will definitely consider you service and product when I am about to buy my own property."))
                                # content="Luko is a company specializing in house insurance and protection and also the fastest growing insurance company in Europe. Besides the very caring insurance service, luko has leveraged their product and artificial intelligence technologies, such as the smart sensor, it can analyze consummation of electricity, water etc in realtime.<sep>Why you want to join us? <sep>I want to join Luko because I believe what the company provide is meaningful to everyone, house is the most essential thing in our life, whatever what happened, Luko can provide the most reliable and fastest service. Besides the most caring insurance service, you have leveraged artificial intelligence and your product to build the strong AI powered technologies to avoid accident.I have experience in both backend development and AI, using my experience and knowledge, I can better understand the products of company and communicate well between teams, so I want to join you, I want a fast growing and Humanitarian company.<sep>Whatever I can join you or not, I will definitely consider you service and product when I am about to buy my own property."))
        # articles.append(Article(id="why-sa", title="为什么想做Solution Architect",
        #                         content="自己还是刚毕业没多久的人，总是有特别多感兴趣的地方和想学习的领域，从毕业以后我一直没把自己受限在一个领域里"
        #                                 "架构一直是我特别感兴趣的领域，特别是工作了一段时间以后更加深有体会，更加熟悉了成为一个优秀的架构师必须要具备的一些条件：coding，deployment，optimization,架构能力，运维devops，管理和沟通"
        #                                 "缺一不可。我自己在工作就做过很多，比如去客户现场做poc或者项目交付，数据库设计和调优，管理一个小的团队，跟客户沟通，跟其他的team沟通，包括微服务，云开发等等"
        #                                 ""))
        articles.append(Article(id="why-you", title="为什么你？",
                                content="What can you bring to the role?<sep>First, I am familiar with your tech stack: Python, Flask, AWS, MySQL, docker, CICD etc. I have experiences in both backend development and artificial intelligence fields, I know that you have applied artificial intelligence into production. I can contribute both my skills to the company. And based on my knowledge, I can collaborate very well with other teams and better understand the products of the company.<sep>Next, I worked in a startup, I am very adapted to a challenging and fast-developing environment and I enjoy working with it. I don’t mind woking in different roles, except for my development skills, I also want to contribute my business analysis skills, communications skills, leadership, autonomy, adaptability and resistance to stress, they all formed me to be a very good candidate for you."))
                                # content="What can you bring to the role?<sep>First, I am familiar with your tech stack: Python, Flask, AWS, MySQL, docker, CICD etc. I have experiences in both backend development and artificial intelligence fields, I know that you have applied artificial intelligence into production. I can contribute both my skills to the company. And based on my knowledge, I can collaborate very well with other teams and better understand the products of the company.<sep>Next, I worked in a startup, I am very adapted to a challenging and fast-developing environment and I enjoy working with it. I don’t mind woking in different roles, except for my development skills, I also want to contribute my business analysis skills, communications skills, leadership, autonomy, adaptability and resistance to stress, they all formed me to be a very good candidate for you."))

        articles.append(Article(id="strengths-faults", title="优点/缺点",
                                content="Strengths:<sep>	1. Autonomy	I really enjoy learning new things and I can "
                                        "say that I'm skilled at learning, I learn things very fast, can fit in new "
                                        "works fast	Back in my university, I got national prize scholarship every year "
                                        "and awarded the most prestigious Eiffel scholarship when I studied at France "
                                        "credit to my best academic performance at school.	<sep>	2. Strong "
                                        "Adaptability	I have been lived long-term or short-term in many cities, "
                                        "I can always adapt myself very quickly to the new environment. In my previous "
                                        "job, once I was asked to go on a business trip to another city to develop POC "
                                        "and experiments in client's company. I lived there for a month, worked and "
                                        "ate together with clients, I  didn’t feel afraid of asking questions and "
                                        "communicating with them to better understand their business need, "
                                        "my honest and problem solving skills won their trust so that after that time "
                                        "our company got the long term relationship with them.	<sep>	3. "
                                        "Committed/dedicated 	My leader and my colleagues think me as a very "
                                        "responsible and committed staff,  after finished the tasks that delegated to "
                                        "me,  I would  always love to stay at office late to think about if there can "
                                        "be any improvement or if there are any small exceptions that we didn’t take "
                                        "into consideration. 	<sep>Disadvantage:<sep>In the past, I tended to focus "
                                        "too much on details because I really want to product quality work, "
                                        "but sometimes it can cause me to lose focus of the big picture. Realizing "
                                        "that I need to strike a balance between details and finishing the task on "
                                        "time. So now, I will first finish the main functional requirements, "
                                        "then polish the project little by little."))
        articles.append(Article(id="short-long-plan", title="短期/长期计划",
                                content="Short-term<sep>Break into a company and gain as much knowledge as possible about the day-to-day responsibilities, fit in the new environment. I know that in Luko there are a lot of talented people from whom I can gain a lot tech knowledge, communication skills and problem solving skills. This is the most import short-term for me. After that, I may want to work on some other certificates that related to current work, which can help me develop better insight and knowledge.<sep>Long-term<sep>In the long term, I think long term may be 5 years, I hope to become a senior and very experienced software engineer who can contribute to the growth of the industry as well as the company, I want also to help these juniors in both career plan suggestions and technology problem solving, because along the way I walked, I have been helped by many people, I am really grateful."))
        articles.append(Article(id="difficulty", title="最大的困难，客户频繁的改需求",
                                content="The biggest difficulty during my development career life, I think that is "
                                        "frequent requirement changes, after I woked in Datagrand one year, "
                                        "I was promoted to be a team leader of a small, developemt team, there were 4 "
                                        "juniors and interns in my team, we are responsible for designing the "
                                        "application server of a nlp auto learning platform(which enable their staffs "
                                        "to train their own deep learning models easily through a user friendly "
                                        "interface, we already integrated several Machine learning and deep learning "
                                        "algorithms and let users to customize parameters on the frontend, "
                                        "so they can do nlp analysis based on their own data.<sep> at first, "
                                        "I only communicated with project manager, he listed the requirements that "
                                        "the clients want and then I reforwarded these information to my teammates "
                                        "and delegated tasks and after one sprint, we showed some results to clients, "
                                        "but clients didn’t be very satisfied and came up with some new ideas and "
                                        "overturned some features that he said before. Thing like that happened 2 or "
                                        "3 times, then I realized that maybe the communication between me and project "
                                        "manager and clients are not efficient, and sometimes clients didn’t have a "
                                        "very specific and clear requirements, and they don’t know coding, "
                                        "they may have some unrealistic ideasThen I went to clients' company and "
                                        "visited them in person, on one hand to better understand what he wants,  "
                                        "guide them in a development perspective, explain some features can be easy "
                                        "to implement but others may need a bit more time, and on the other hand "
                                        "better understand the culture, working method and environment of client "
                                        "company"))
        articles.append(Article(id="achievements", title="最大的成就，解决sql慢的问题",
                                content="Professional part<sep>When I started working at my previous company, "
                                        "once the system became slower and slower and unacceptable by our "
                                        "clientsBecause several people collaborate, the manager didn’t have time to "
                                        "code review all, when things happened, I propose to the manager to let me "
                                        "examine the performance of code, use cProfile can show how long every "
                                        "function or single code line takes, then I found that slowness mostly came "
                                        "from sql queries, I use my sql tuning and database design knowledge to optimize "
                                        "the performance, reduced 2-3x response time."
                                        "I found there is one place not reasonable in database design, for example one record in a table often need to appear together with another table that is related with it 2or3 tables far, so why we don't add a foreign key in the previous table. although it cost a little more while creating but it saves alot while selecting;"
                                        " My leader recognize me very well "
                                        "and promoted me as a small team leader after one year's work, that's the "
                                        "achievement that I am proudest of<sep>Educational part<sep>The Eiffel "
                                        "excellence scholarship by French minister, this is the most prestigious "
                                        "scholarship, only around 350 foreign students are awarded each year. This "
                                        "the biggest recognition  of my these years' study, hundreds and thousands of "
                                        "days' insisting.Several aspects： scores(gpa), separate exam for us(math, "
                                        "physics, english, programing etc), interview(express your self, communicate "
                                        "with others)"))
        articles.append(Article(id="team-role", title="团队角色",
                                content="To be honest, I don't believe in a typical division of roles in a team, "
                                        "like leaders and followers. In my opinion, feedback should flow free in all "
                                        "directions in a successful team. Each team member should not hesitate to "
                                        "share their opinions and also take a leadership role when that's the best "
                                        "thing for the team. I tries to approach my team in the same way.<sep>When I "
                                        "was the fresh in a company, expressing myself is a good chance to let others "
                                        "correcting my unrealistic thought, then I will get improved.When I led the "
                                        "small team, I should absolutely take more responsibilities than others, "
                                        "I should be sensible enough to take care of my teammates so that they wont "
                                        "get into a wrong way."))
        articles.append(Article(id="work-in-startup", title="工作给初创公司",
                                content="My only official job experience was in a startup, honestly, I really "
                                        "enjoying working there, but due to family reason I have to give it up.In "
                                        "fact, they gave me a lot of opportunities to express myself and develop "
                                        "diversely. I always think that a successful person is not just excellent in "
                                        "one aspect, for me, I'm software engineer I should not be only good at "
                                        "coding, but also communication skills, presentation skills, resistance to "
                                        "stress etc. I cultivated a lot these abilities in my past job.<sep>In "
                                        "addition, I'd love to grow with the company, startup need to grow fast, "
                                        "my innovate can always be taken into consideration.<sep>For the reasons "
                                        "above, I'd love to work in a startup"))
        articles.append(Article(id="next-role-expectation", title="下一份工作期待",
                                content="I want to be able to contribute my skills, experience the most to the next "
                                        "role, and there also need be challenges, unknown things to wait for me to "
                                        "explore. That's why I want to work in a startup, I want to grow with the "
                                        "company in a very high speed.  I enjoy challenges"))
        articles.append(Article(id="ds-se", title="DS or SE",
                                content="This is also a question I have been thinking of in the past few years, "
                                        "I think Data Science and Software Engineers can work hand-in-hand<sep>A "
                                        "typical Data Scientist will work on establishing a problem statement, "
                                        "querying data, exploratory data analysis, feature engineering, "
                                        "model building and development, and result interpretation. A Software "
                                        "Engineer may not work on all of these steps of a typical Data Science "
                                        "process, but they do touch a great amount of this work — including calling "
                                        "API data, storing it, programming enhancements, and deployment of a "
                                        "model Some skills overlapped, such as python, business analysis, "
                                        "sql etc.<sep>Currently I may focus a little bit more on development, "
                                        "because I am interested in designed high scaling system, build high "
                                        "availability infrastructure, I love these challenging works. But I won't "
                                        "lose my data science skills, I know that you company leveraged artificial "
                                        "intelligence and these smart products. So it would be easy for me to "
                                        "collaborate with other teams and better understand products of company."))
        articles.append(Article(id="other-interview", title="还有面试其他公司吗",
                                content="I'm interviewing with another high technology companies. One is in the "
                                        "middle of hiring process and another  is almost at the final step."))
        articles.append(Article(id="salary", title="薪水",
                                content="I really appreciate this opportunity, and I am flexible about it. However, based on my previous salary, my knowledge of the industry, and my understanding of this geographic area, I'd expect a salary around 50k."))
        articles.append(Article(id="visa", title="签证",
                                content="I had signed pacs with my boyfriend, he is french. Now my lawyer is applying the family visa for me, family visa is work authorized. <sep>But now due to the current isolation situation, making an appointment with the police takes a little bit long, but my laywer is sure that I can get my family visa in the end of April or at latest the beginning of May."
                                        "if it's too late for you."))
        articles.append(Article(id="interests", title="interests",
                                content="I like play badmintons in my sparse time, but now due to isolation no "
                                        "stadium open, so now I tend to paly Somatosensory games at home, "
                                        "I like making myself move, as we sit infront of computers a very long time "
                                        "everyday, it's important to exercise body in a good physical "
                                        "condition.<sep>Another I like is playing Chinese traditional instrument, "
                                        "I started to learn it since I was young then for 10 years, every weekend I "
                                        "need to attend the class kind of far from my home, rain or shine. Now "
                                        "although I didn’t live for it but it can make me calm while I am playing "
                                        "it."))
        articles.append(Article(id="integration", title="怎么integrate深度学习模型的",
                                content="Backend service:  tensorflow framework <sep>Offline, for training	• Users "
                                        "can type parameter they want at frontend, then these parameters can be send "
                                        "to backend service to train model.<sep>	• We didn’t do too much scaling on "
                                        "offline service, add GPU to accelerate offline training, increase the batch "
                                        "size, early stop mechanism etc. these are usually base on model tunning "
                                        "mechanism.<sep><sep>Online, for prediction<sep>	• simply read incoming "
                                        "messages(text) from a queue<sep>	• For scaling, This backend service split "
                                        "the long text and use Python-included multipleprocessing library to do "
                                        "preprocessing jobs parallelly, <sep>	• After preprocessing, group text "
                                        "samples into batches, use round robin to distribute these batches via celery "
                                        "to do the inference asynchronously. By increasing the number of workers can "
                                        "scaling the performance of online prediction task.<sep>	• Then after all "
                                        "batches finished, we gathered the results together and then Send result back "
                                        "via API<sep>We can't only have one algorithm, for nlp tasks, we have BILSTM, "
                                        "CNN, and svm or randomforest these machine learning algorithms can solve "
                                        "problem in some cases, and different algorithms need different environments, "
                                        "different requirements, so we need Docker to run each model in its own "
                                        "virtual environment, and these dockers need to provide a unified interface "
                                        "to front end<sep>"))
        articles.append(Article(id="explan-ml", title="解释一个ml或dl",
                                content="[lstm]<sep>A Recurrent Neural Network’s signals travel in both directions, "
                                        "creating a looped network. It considers the current input with the "
                                        "previously received inputs for generating the output of a layer and can "
                                        "memorize past data due to its internal memory.<sep>Long-Short-Term Memory ("
                                        "LSTM) is a special kind of recurrent neural network capable of learning "
                                        "long-term dependencies, remembering information for long periods as its "
                                        "default behavior. That's why LSTM can relate information even in a long "
                                        "text. In works, we use lstm to extract important information from a long "
                                        "text.<sep>There are three steps in an LSTM network:Step 1: The network "
                                        "decides what to forget and what to remember.Step 2: It selectively updates "
                                        "cell state values.Step 3: The network decides what part of the current state "
                                        "makes it to the output.<sep> <sep>[svm]<sep>Imagine there is a space where "
                                        "has a cluster of red points and a cluster of blue points. Svm is responsible "
                                        "for finding the decision boundary to separate different classes and maximize "
                                        "the margin. Margins are the distances between the line and those "
                                        "points.<sep>This is our representation in 3d or 2d sparse, and we can extend "
                                        " it to a hyper dimension, then the mission becomes to find a hyperplane, "
                                        "it can be used to solve a lot of classification problems"))
        articles.append(Article(id="agile", title="agile development",
                                content="• Product manager 设计产品一个个的backlog, 确定哪些backlog需要在当前的sprint(大概两周)完成*sprint是一个工作周期<sep>	• 召开产品backlog计划会，预估时间<sep>	• 把backlog放在redmine或者jira（project tracking software）,由team leader划分任务给每个人<sep>	• 每天举行stand up meeting ，brief introduction of daily work, difficutilies, etc<sep>	• leader随时查看burndown chart，了解进度，知道unfinished tasks 是0，这个sprint结束<sep>	• 向客户展示这个sprint的成果，拿到feedback<sep>总结会议wrap up meeting，everyone share with other the difficulties, improvements<sep>"))
        articles.append(Article(id="questions", title="questions",
                                content="It has been a so good to talk to you and you helped me to better understand the company. "
                                        "<sep>could you please tell me about a project that you are working on currently"
                                        "Is that possible for me to know the next step of the hiring process?<sep>If I am lucky enough to get to the next round, can you give my an overview of what to expect in the next round, like online coding test or system design problems?"))
        articles.append(Article(id="apsheduler", title="apsheduler",
                                content="Advanced python sheduler, light weight, let you schedule your code once or periodically and also in an asynchronize wayOne way to implement parallel tasksHere why I choose apsheduler but not multiprocessing or multithreading libraries in PythonThat's because pushing tasks to redis is a continous process, use apsheduler can set time frequency to fetch from redis, we can set a little big longer, so that can save cpu resource<sep>I also consider multithreading, redis need blpop or brpop , it waits and blocks the connection when there are no elements to pop<sep>Flask_apscheduler is under Flask extension libraries, it can better integrated with flask, 比如根据flask config to load apscheduler config， can indicated how many workers"))
        articles.append(Article(id="celery", title="celery",
                                content="Celery is an asynchronous task queue based on distributed message passing to distribute workload across machines or threads. A celery system consists of a client, a broker, and several workers.Scalable, parallelly, itergrated very well with web framework"))
        articles.append(Article(id="asyncawait", title="async await",
                                content="define a function to be async, and inside the function add some awaitable process, during this time, it can be hangedup and go to do other things.it can implement async, but cannot return instantly"))
        articles.append(Article(id="mysql", title="mysql",
                                content="How mysql store data?<sep>Basic storage structure is page, inside each pages, "
                                        "there are recordsPages are linked with each other using a double linked list, "
                                        "inside a page, records are linked into a single linked list, so when we need "
                                        "to do a simple query like select * from table where name = 'Tom' without any "
                                        "optimization, mysql will search sequentially from the first page, then inside "
                                        "the page find records one by one from the first record, if data size is big, "
                                        "query time would be very long.<sep>So why index can improve the "
                                        "performance?<sep>Index use B+ tree to store page and record informationFor "
                                        "example, parent node contains a wide range of id, and each its child node "
                                        "cover a part, so  if we need to find a specific id, we just search down the "
                                        "tree, the maximum tc is the height of the tree<sep>LOCK<sep>	• For "
                                        "update/insert/delete, inooDB will automatically add exclusive lock(prevent "
                                        "all read or write operation to the same data object); 	<sep>	• MyIsam will "
                                        "automatically add read lock when execute select operation, add write lock "
                                        "when execute insert/update/delete operation	<sep>How to master-slave "
                                        "replication?	• mysql	• 主机把所有的data changes放到binary log	• "
                                        "（binlog除了用于主从复制，还用于数据恢复）	• 从机读binlog复制在自己的relay "
                                        "log，然后在自己的机器上replay，从而实现主从复制	• binlog 保存mysql从开机到现在保存的所有data changes	• "
                                        "binlog格式		○ statement sql语句记录在binlog，比如update xxx set xxx=xx			§ "
                                        "会造成不一致，比如在语句中使用now(),rand(),uuid()		○ row 行数据("
                                        "canal只能用row，因为canal不是mysql不能执行sql语句)			§ id=1 的数据现在长什么样：name=xx, "
                                        "age=xx, city=xx			§ 直接覆盖掉			§ 比较占资源		○ "
                                        "mixed一般情况下用statement，在可能会造成不一致的情况下用row"
                                        "<sep> <sep>"
                                        "how you optimized?"
                                        "prevent scaning the whole table, add index for those column many used in where and order by clause"
                                        "<sep>prevent using !=, or, in, is null or is not null operations in where clause, mysql engine will scan the whole tale regardless of index"
                                        "<sep>for those big tables, try to first pagination before join operation"
                                        "<sep> explain select xxx to see the exuction plan of this sql"
                                        "when create table, it's better to set attribute not null, because nullable attribute need other space to store if it's null or not"
                                        "<sep> use bulk operation instead of forloop single operation"))
        articles.append(Article(id="copy", title="copy",
                                content="	• Python		○ Reference copy			§ B = a, they point to the same address in memory		○ Shallow copy, copy.copy()			§ Create a new object, but sub object wont change			§ For example nested listDeep copy, copy.deepcopy()"))
        articles.append(Article(id="cache", title="cache",
                                content="api level, the same route in 1 minuite don't need to process again; database level: redis"))
        articles.append(Article(id="redis", title="redis",
                                content="redis作为消息队列：<sep>	好处：实现简单；支持持久化，数据不会丢失；业务是一个生产者，多个消费者，后端服务开多分片	<sep>缺点：消费者消费后是否完成，比较麻烦，需要实现api回写状态；不支持分组；长时间没有消息可能会断开，逻辑上需要重试"))
        articles.append(Article(id="cap", title="cap theorem",
                                content="Consistency (all nodes see the same data even at the same time with concurrent updates )Availability (a guarantee that every request receives a response about whether it was successful or failed)Partition tolerance (the system continues to operate despite arbitrary message loss or failure of part of the system)"))
        articles.append(Article(id="REST", title="REST",
                                content="REST stands for REpresentational State Transfer. REST is web standards based architecture and uses HTTP Protocol for data communication."))
        articles.append(Article(id="g", title="flask g",
                                content="Flask’s g object is used as a global namespace for holding any data during the application context."))
        articles.append(Article(id="session", title="session",
                                content="The session object of the flask package is used to set and get session data. The session object works like a dictionary but it can also keep track modifications."
                                        "g” is data shared between different parts of the code base within one request cycle. For example, a database connection or the user that is currently logged in. While session provides you a storage place to store data for a specific browser. Which means using a specific browser, returns for more request."))
        articles.append(Article(id="wsgi", title="wsgi",
                                content="只是一种规范，描述web server如何与web application通信的规范"))
        articles.append(Article(id="CICD", title="CICD",
                                content="Continuous Integration (CI) is a development practice that requires developers to integrate code into a shared repository several times a day. Each check-in is then verified by an automated build, allowing teams to detect problems early. it often comes with unit testing"))
        articles.append(Article(id="sqlalchemy", title="sqlalchemy",
                                content="orm vs core: <sep> view data as schema or business object"
                                        "<sep> orm makes database interaction feel like python code, microservice benifits from this, allowing developers to foucs on the business logic"
                                        "<sep> core:ORM is built on top of SQLAlchemy Core, it more toward the sql level. more efficient when handling large amount of data insert"
                                        "<sep> I have done an experiment to insert a large amount of data, using bulk insert is almost 10 times faster than forloop inserting, then use sqlalchemy core is twice faster than orm bulk insert"))
        articles.append(Article(id="unit test", title="unit test",
                                content="all kinds of cases: tracking number valid and not valid, tracking in db or not,"
                                        "<sep> unit test: as the point of view of developers, test the functionalities of your code, if the result are as we expected, and we want to cover as many lines as possible"
                                        "<sep> integration test:"
                                        "<sep> e2e test: test from the end user’s experience by simulating the real user scenario,"))

        articles.append(Article(id="broswer", title="what does broswer do",
                                content="[back](#table)1. You enter a URL into a web browser2. The browser looks up the IP address for the domain name via DNS3. The browser sends a HTTP *request* to the server4. The server sends back a HTTP *response*5. The browser begins rendering the HTML6. The browser sends requests for additional objects embedded in HTML (images, css, JavaScript) and repeats steps 3-5.7. Once the page is loaded, the browser sends further async requests as needed."))

        articles.append(Article(id="threading", title="threading and multiprocessing",
                                content="process:A process is an instance of a computer program being executed.<sep>thread:Threads are components of a process, which can run in parallel.<sep>There can be multiple threads in a process, and they share the same memory space<sep>multithread: io bounded<sep>multiprocessing: cpu bounded<sep>Python has something called the Global Interpreter Lock (GIL).you can create as many threads as you like, but the GIL ensures only one of those threads will ever be executing at any given time.<sep>for multiprocessing, every process has independent GIL.<sep>我更习惯使用multiprocessing, You may notice that CPU utilization goes much higher when you are using multiprocessing compared to using multithreading"))
        articles.append(Article(id="flaskdjango", title="flask or django",
                                content="flask is more light weight with less features, allows developers to add any number of libraries or plugins for an extension, it's more flexible and easy to learn"
                                        "django is heavy-weight, it has integrated a lot of standard functionalities, developers just need to focus on business logic"))
        return render(request, "behavior-questions.html", {
            "articles": articles,
        })

class Article:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
        self.paras = content.split('<sep>')
