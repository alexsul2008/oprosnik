
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.generic import TemplateView, ListView
from django.contrib import auth
from django.contrib.auth import authenticate, login

from django.views.generic import View
from json import dumps
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.core import serializers

from django.db.models import Count, Q, F

from questions.models import UsersAnswers, Questions, Answers, UsersAnswer, WorkPermitUsers
import random
import json

class QuestionsViewList(ListView):
    model = UsersAnswer
    template_name = 'usersanswer_list.html'

    def get_queryset(self):
        queryset = UsersAnswer.objects.filter(
            Q(user__in=self.request.GET.getlist("user"))
        )
        return queryset




@csrf_protect
# @csrf_exempt
def question_ajax(request):
    session_key = request.session.session_key
    user = request.user.username
    group_user = Group.objects.get(user=request.user).id
    # print(request.POST)
    data = {}
    if request.POST.get('correct') == '1':
        ok_vop = request.POST.get('vop')
        ok_otv = request.POST.get('otv')
        not_ok_vop = 0
        not_ok_otv = 0
    else:
        ok_vop = 0
        ok_otv = 0
        not_ok_vop = request.POST.get('vop')
        not_ok_otv = request.POST.get('otv')

    correct = request.POST.get('correct')
    vop = request.POST.get('vop')
    otv = request.POST.get('otv')

    ua = UsersAnswers.objects.create(user=user, group_user=group_user, session_key=session_key, not_ok_vop=not_ok_vop,
                                     not_ok_otv=not_ok_otv, ok_vop=ok_vop, ok_otv=ok_otv)

    new_ua = UsersAnswer.objects.create(user=user, group_user=group_user, session_key=session_key, correct=correct,
                                        vop=vop, otv=otv)
    data['ok_vop'] = ok_vop
    data['ok_otv'] = ok_otv
    data['not_ok_vop'] = not_ok_vop
    data['not_ok_otv'] = not_ok_otv


    return JsonResponse(data)


# @csrf_protect
@csrf_exempt
def next_question(request):
    massivId = request.session["listQuestionsCook"]
    total = int(request.session["total_questions"])
    counts = int(request.session["count_questions"])
    # print('count до: ', counts)
    counts += 1
    request.session["count_questions"] = counts

    data = {}
    del massivId[0]
    if len(massivId) == 0:
        data['flag'] = 1
        # user = auth.get_user(request).username
        user_id = User.objects.get(username=request.user.username).id
        # print(user_id)
        session_key = request.session.session_key
        user_work_perm = WorkPermitUsers.objects.create(user_id_id=user_id, session_key=session_key)

        # list_not_ok_questions = UsersAnswers.objects.all().filter(session_key=session_key).exclude(not_ok_vop__isnull=True).values('not_ok_vop')
        # list_not_ok_questions = UsersAnswers.objects.all().filter(session_key=session_key).exclude(not_ok_vop=0)
        # count_not_ok_questions = list_not_ok_questions.count()
        # print(session_key)
        # print(list_not_ok_questions)
        # print(count_not_ok_questions)
        #
        # data['list_not_ok_questions'] = serializers.serialize('json', list_not_ok_questions, indent=2,
        #                                                       fields=('not_ok_vop', 'not_ok_otv'))
        # # data['list_not_ok_questions'] = serializers.serialize('json', list_not_ok_questions, indent=2)
        # data['count_not_ok_questions'] = count_not_ok_questions
        # print(data)
        #
        # # list_questions = Questions.objects.filter(groups=user_groups.id, in_active = 'True').values_list('pk', flat=True).order_by('id')
        #
        # list_vop = UsersAnswer.objects.filter(session_key=session_key, correct=False).values_list('vop', 'otv')
        # print(list_vop)
        # print(list_vop.query)
        #
        # vop_not = {}
        # # id_vop = [int(i[0]) for i in list_vop]
        # # id_vop_l = list(id_vop)
        # id_vop = []
        # for i in list_vop:
        #     id_vop.append(i[0])
        #
        # print(id_vop)
        # #
        # # vop_not = Questions.objects.filter(pk__in=id_vop).all()
        # not_vop_list = Questions.objects.filter(pk__in=id_vop).all()
        #
        # data['vop'] = serializers.serialize('json', not_vop_list, indent=2, ensure_ascii=False, fields=('description'))
        # print(vop_not)
        # vop_not['otv'] = Answers.objects.filter(vop_id_id=pk)
        # print(vop_not_all.query)
        # vop_not['vop'] = Questions.objects.get(id=[list_vop[0]]).description
        # print(vop_not)
        url = '/statistics/'
        data['url'] = url
        return JsonResponse(data)
    else:
        data['flag'] = 0
        pk = massivId[0]
        # questions_list = Questions.objects.filter(id=pk)
        questions_list = Questions.objects.get(id=pk).description
        answers_list = Answers.objects.filter(vop_id_id=pk)

        try:
            last = massivId[1]
        except:
            last = massivId[0]

        request.session["listQuestionsCook"] = massivId
        # data['questions_list'] = serializers.serialize('json', questions_list, indent=2, ensure_ascii=False, fields=('description','image', 'doc_url'))
        data['questions_list'] = questions_list
        data['answers'] = serializers.serialize('json', answers_list, indent=2, ensure_ascii=False, fields=('description', 'approved'))
        data['next'] = last
        data['id'] = massivId[0]
        data['count'] = counts
        data['total'] = total

        return JsonResponse(data)


@login_required
def statistics(request):
    # user = User.objects.get(username=request.user.username)
    # # print(user.id)
    # sess_list_user = WorkPermitUsers.objects.filter(user_id_id=user.id).values('session_key')
    # print(sess_list_user.query)
    # print(sess_list_user)

    # answer_user_not_ok = []
    # data = [[], []]
    # data = []
    # i = 0
    # vop_list = {}
    # vop_ans = {}
    # list_all = {}
    # for sess in sess_list_user:
    #
    #
    #     # answer_user_not_ok.append(UsersAnswer.objects.filter(session_key=sess['session_key'], correct=False).values_list('vop', 'otv'))
    #     # answer_user_not_ok = UsersAnswer.objects.filter(session_key=sess['session_key'], correct=False).values_list('vop', flat=True)
    #     answer_user_not_ok = UsersAnswer.objects.filter(session_key=sess['session_key'], correct=False).values_list('vop', 'otv')
    #
    #     count = len(answer_user_not_ok)
    #     # print(answer_user_not_ok)
    #     # vop, otv = answer_user_not_ok
    #     # print(vop)
    #     # print(otv)
    #     # Questions.objects.get(id=[int(j[0]) for j in list(answer_user_not_ok)])
    #     ids_vop = [j[0] for j in answer_user_not_ok]
    #     ids_otv = [j[1] for j in answer_user_not_ok]
    #     print(ids_vop)
    #     # print(ids_otv)
    #
    #     # data.append(('vop', Questions.objects.filter(pk__in=ids).values('description')), ('count_vop', answers_user_not_ok.count())
    #     # data[0].append(list(Questions.objects.filter(pk__in=ids_vop).values('description')))
    #     # data[1].append(str(count))
    #
    #     vop_list = {
    #         'vop': list(Questions.objects.filter(pk__in=ids_vop).values('description')),
    #         'answ': list(ids_otv),
    #         'vop_count': str(count),
    #     }
    #     # vop_list['vop'] = list(Questions.objects.filter(pk__in=ids_vop).all())
    #     # vop_list['answ'] = ids_otv
    #     # vop_list['vop_count'] = str(count)
    #
    #     vop_ans = list(zip(vop_list['vop'], vop_list['answ']))
    #
    #     print(vop_list)
    #     # data[i] = vop_list['vop_count']
    #     # print(data[i])
    #     data.append(vop_list)
    #     # print(vop_list.items())
    #     # answers_list = Answers.objects.filter(vop_id_id=questions_list.id)
    #     # print(dict(data))
    #     # data[i] = answer_user_not_ok
    #     # for key, value in data[i].items():
    #     #     print(key, value)
    #     # data.append(answer_user_not_ok)
    #     # print(data[i])
    #     # i += 1
    # # print(list(data))
    #
    # # print(vop_ans)
    #
    # # print(list(zip(data[0], data[1])))
    #
    # # answers_user = zip(data[0], data[1])
    #
    # # data = dict(answer_user_not_ok)
    # # print(data)
    # # for answer_user in answer_user_not_ok:
    # #     data.append(answer_user)
    #
    # # for key, value in data.items():
    # #     print(key, value)
    #     # print(value)

    # nurseries = Nursery.objects.filter(title__startswith="Moscow").values_list('pk', flat=True)
    # Pet.objects.filter(nursery__in=list(nurseries))



    list_user = {}
    user = User.objects.get(username=request.user.username)
    sessions_lists_users = WorkPermitUsers.objects.filter(user_id_id=user.id).values('session_key', 'date_passage').order_by('-date_passage', '-id')

    list_quests = []

    list_quest_all = []
    j_sess = 0
    for sessions_us in sessions_lists_users:

        # nurseries = UsersAnswer.objects.filter(session_key=sessions_us['session_key'], correct=False).values_list('vop', flat=True)
        # nurseries_quest = Questions.objects.filter(id__in=list(UsersAnswer.objects.filter(session_key=sessions_us['session_key'], correct=False).values_list('vop', flat=True)))
        # #
        user_answers = UsersAnswer.objects.filter(session_key=sessions_us['session_key'], correct=False).values_list('vop', flat=True).order_by('vop')
        # user_answers_quest = Questions.objects.filter(id__in=user_answers).values_list('id', 'description').order_by('id')
        # user_answers_answers = Answers.objects.filter(vop_id_id__in=Questions.objects.filter(id__in=list(user_answers))).values_list('id', 'description', 'approved').order_by('vop_id_id', 'id')

        # print(user_answers.query)
        # print(len(user_answers))
        user_answers_quest = []
        i_us_an_ques = 0
        for i in user_answers:
            # print(i)
            # questions = list(Questions.objects.filter(id=i).values('id', 'description').order_by('id'))

            # questions += list(Answers.objects.filter(vop_id_id=i).values('id', 'description','approved').order_by('vop_id_id', 'id'))
            # user_answers_answers = []
            # user_answers_answers.append(list(Answers.objects.filter(vop_id_id=i).values('id', 'description','approved').order_by('vop_id_id', 'id')))
            question_new = Questions.objects.get(id=i)
            new_answ = Answers.objects.filter(vop_id_id=i).values('id', 'description','approved', 'vop_id').order_by('vop_id_id', 'id')
            new_user_answer = UsersAnswer.objects.filter(session_key=sessions_us['session_key'], correct=False).values_list('otv', flat=True)
            # print(question_new.id)
            list_quest_all_new = {
                'id': question_new.id,
                'otv': list(new_user_answer),
                'question_new': question_new.description,
                'new_answ': list(new_answ),
            }
            # list_quest_all.append(list_quest_all_new)


            # list_vop_answ_user = {
            #     'questions': questions,
            #     'ans': list(Answers.objects.filter(vop_id_id=i).values('id', 'description','approved', 'vop_id').order_by('vop_id_id', 'id')),
            # }
            user_answers_quest.append(list_quest_all_new)

        # print(user_answers_quest.query)
        # print(user_answers_quest)
        # print(user_answers_answers.query)
        # print(user_answers_quest)

        # print(UsersAnswer.objects.filter(session_key=sessions['session_key'], correct=False).values('vop', 'otv').annotate(cnt=Count('vop')).count())
        list_vop_count = {
            # 'count': UsersAnswer.objects.filter(session_key=sessions_us['session_key'], correct=False).count(),
            'count': len(user_answers),
            'date_passage': sessions_us['date_passage'],
            # 'vop': list(UsersAnswer.objects.filter(session_key=sessions_us['session_key'], correct=False).values('vop', 'otv')),
            # 'vop': list(Questions.objects.filter(id__in=list(UsersAnswer.objects.filter(session_key=sessions_us['session_key'], correct=False).values_list('vop', flat=True))).order_by('id')),
            'vop': user_answers_quest,
        }
        # print(list_vop_count['vop'])
        list_quests.append(list_vop_count)


    print(list_quests)


    context = {
        'user_groups': Group.objects.get(user=request.user),
        'user_stat': list_quests,
    }
    template = 'questions/statistics_questions.html'
    return render(request, template, context)



def random_question(array):
    """Перемешать список"""
    random.shuffle(array)
    return array


class HomeListView(ListView):
    model = Questions
    template_name = 'home.html'
    context_object_name = 'questions_list'


@login_required
def QuestionsViews(request):
    # print(request)
    user_groups = Group.objects.get(user=request.user)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    if (user_groups.id == 1 or user_groups.id == 2):
        list_pk = Questions.objects.filter(in_active='True').values_list('pk', flat=True).order_by('id')
    else:
        list_pk = Questions.objects.filter(groups=user_groups.id, in_active='True').values_list('pk', flat=True).order_by('id')

    massiv = random_question(list(list_pk))
    # """Проверяем наличие списка ID вопросов в куки, есле нет его, то создаем"""
    if not 'listQuestionsCook' in request.session:
        request.session["listQuestionsCook"] = massiv

    if not 'total_questions' in request.session:
        request.session["total_questions"] = len(massiv)

    if not 'count_questions' in request.session:
        request.session["count_questions"] = 1

    print(request.session["listQuestionsCook"])
    print(request.session["total_questions"])
    print(request.session["count_questions"])
    #
    massiv = request.session["listQuestionsCook"]
    total_questions = request.session["total_questions"]
    count_questions = request.session["count_questions"]

    questions_list = Questions.objects.get(id=massiv[0])
    answers_list = Answers.objects.filter(vop_id_id=questions_list.id)

    username = auth.get_user(request).username

    try:
        last = massiv[1]
    except:
        last = massiv[0]

    context = {
        'list_next': last,
        'questions_list': questions_list,
        'count_questions': count_questions,
        'answers_list': answers_list,
        'total_questions': total_questions,
        'username': username,
        'user_groups': user_groups,
    }
    template = 'questions/questions_list.html'
    return render(request, template, context)




@login_required
def edit_questions(request):
    user_groups = Group.objects.get(user=request.user)
    context = {
        'list_questions': Questions.objects.all().order_by('-id'),
        'username': auth.get_user(request).username,
        'user_groups': user_groups
    }
    template = 'questions/edit_question.html'
    return render(request, template, context)


@login_required
def question_detail(request, pk):
    question = Questions.objects.get(id=pk)
    answers = Answers.objects.filter(vop_id=pk)
    return render(request, 'questions/question_detail.html', context={'question': question, 'answers': answers})


@login_required
def login(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('questions')
        else:
            form = UserCreationForm()
    return render(request, 'registration/login.html', {
        'form': form
    })

# @login_required
# def questions(request):
#     """Определяем к какой группе принадлежит User"""
#     #groups = request.user.groups.get().name
#     groupsName = Group.objects.get(user = request.user)
#     groupsId = int(groupsName.id)
#
#     list_pk = Questions.objects.filter(groups=3).values_list('pk', flat=True).order_by('?')
#
#
#     questions_list = Questions.objects.get(id = list_pk[0])
#     answers_list = Answers.objects.filter(vop_id=list_pk[0])
#
#     count_questions = len(list_pk)
#         #list_pk = Questions.objects.filter(pk).values_list('pk', flat=True)
#
#         # print(len(list_pk))
#     print(questions_list)
#
#     return render(request, "questions/questions_list.html", {
#         "questions_list": questions_list,
#         "answers_list": answers_list,
#         "count_questions": count_questions,
#         "groups": groupsName,
#     })

# @login_required
# def home(request):
#     # count = User.objects.count()
#     # groups = Group.objects.get(user = request.user)
#     #
#     # print(Group.objects.get(user = request.user))
#     #
#     # return render(request, 'home.html', {
#     #     'count': count,
#     #     'groups': groups
#     # })
#     context = {
#
#     }
#     template = 'home.html'
#     return render(request, template, context)


# Все пользователи
# print(User.objects.all().count())

# Все пользователи, которых нет в группе.
# print(User.objects.annotate(group_count=Count('groups')).filter(group_count=0).count())

# Все пользователи, которые находятся в группе.
# print(User.objects.annotate(group_count=Count('groups')).filter(group_count__gt=0).count())

#
# print(User.objects.filter(groups__in=Group.objects.all()))

# Должно быть: все пользователи, которые находятся в группе.
# Но результат другой. Я не понимаю этого.
# print(User.objects.filter(groups__in=Group.objects.all()).count())

# Все пользователи, которые находятся в группе.
# необходимо
# print(User.objects.filter(groups__in=Group.objects.all()).distinct().count())

# Все пользователи, которые находятся в группе. Без особого, аннотирование, кажется, делает это.
# print(User.objects.filter(groups__in=Group.objects.all()).annotate(Count('pk')).count())

# Все пользователи, которые не входят ни в одну группу
# print(User.objects.filter(groups__isnull=True).count())

# фильтровать модель группы для текущего зарегистрированного пользователя
# print(Group.objects.get(user = request.user))
