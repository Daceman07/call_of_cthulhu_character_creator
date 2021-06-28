import random
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import BasicForm, CharacteristicsForm, BackStoryForm, SkillsForm, EquipmentForm, CashForm, WeaponsForm
from .models import Characteristics, CharBasicInfo, Skills, Equipment, Weapons, BackStory, CashAndAssets
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .utils import render_to_pdf
from django.template.loader import get_template


def signup(request):
    if request.method == "GET":
        return render(request, 'char/signup.html', {'form': UserCreationForm})
    else:
        # Create a new user

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentchar')
            except IntegrityError:
                return render(request, 'char/signup.html', {'form': UserCreationForm, 'error': 'That user name has '
                                                                                               'already been taken. '
                                                                                               'Please try another'})

        else:
            return render(request, 'char/signup.html', {'form': UserCreationForm, 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == "GET":
        return render(request, 'char/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'char/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and '
                                                                                                  'password did not '
                                                                                                  'match'})
        else:
            login(request, user)
            return redirect('currentchar')


def home(request):
    return render(request, 'char/home.html')


@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


@login_required
def currentchar(request):
    basic_info = CharBasicInfo.objects.filter(user=request.user).delete()
    stats = Characteristics.objects.filter(user=request.user).delete()
    background = BackStory.objects.filter(user=request.user).delete()
    equipment_and_gear = Equipment.objects.filter(user=request.user).delete()
    money = CashAndAssets.objects.filter(user=request.user).delete()
    player_skills = Skills.objects.filter(user=request.user).delete()
    weapons = Weapons.objects.filter(user=request.user).delete()
    return render(request, 'char/currentchar.html')


@login_required
def createbasicinfo(request):
    if request.method == "GET":
        return render(request, 'char/createbasicinfo.html', {'form': BasicForm()})
    else:
        try:
            form = BasicForm(request.POST)
            new_basic_form = form.save(commit=False)
            new_basic_form.user = request.user
            new_basic_form.save()
            return redirect('characteristics')
        except ValueError:
            return render(request, 'char/createbasicinfo.html', {'form': BasicForm(), 'error': 'Form not filled out'})


@login_required
def characteristics(request):
    if request.method == 'GET':
        return render(request, 'char/characteristics.html', {'form': CharacteristicsForm(),

                                                             })
    else:
        try:
            form = CharacteristicsForm(request.POST)
            new_stats_from = form.save(commit=False)
            new_stats_from.user = request.user
            new_stats_from.save()
            return redirect('skills')
        except ValueError:
            return render(request, 'char/characteristics.html',
                          {'form': CharacteristicsForm(), 'error': 'Form not filled out'})


@login_required
def backstory(request):
    if request.method == "GET":
        return render(request, 'char/backstory.html', {'form': BackStoryForm()})
    else:
        try:
            form = BackStoryForm(request.POST)
            new_backstory_from = form.save(commit=False)
            new_backstory_from.user = request.user
            new_backstory_from.save()
            return redirect('equipment')
        except ValueError:
            return render(request, 'char/backstory.html',
                          {'form': BackStoryForm(), 'error': 'Form not filled out'})


@login_required
def shopping(request):
    return render(request, 'char/shopping.html')


@login_required
def skills(request):
    basic_info = CharBasicInfo.objects.filter(user=request.user)
    basic_skills = Characteristics.objects.filter(user=request.user)
    dex = basic_skills.get().DEX
    answer = round(dex / 2)
    base_skill_points = basic_skills.get().INT
    base_edu = basic_skills.get().EDU
    base_app = basic_skills.get().APP
    base_str = basic_skills.get().STR
    personal_interest_skill_points = base_skill_points * 2
    job = basic_info.get().occupation[12:23]
    points = 0
    if job == "Antiquarian":
        points = base_edu * 4
    elif job == "Author.    ":
        points = base_edu * 4
    elif job == "Dilettante.":
        points = (base_edu * 2) + (base_app * 2)
    elif job == "Doctor.    ":
        points = base_edu * 4
    elif job == "Journalist.":
        points = base_edu * 4
    elif job == "Detective. ":
        if dex >= base_str:
            points = (base_edu * 2) + (dex * 2)
        elif base_str > dex:
            points = (base_edu * 2) + (base_str * 2)
    elif job == "P.I.       ":
        if dex >= base_str:
            points = (base_edu * 2) + (dex * 2)
        elif base_str > dex:
            points = (base_edu * 2) + (base_str * 2)
    elif job == "Professor. ":
        points = base_edu * 4
    occupational_skill_points = points

    if request.method == "GET":
        return render(request, 'char/skills.html', {'form': SkillsForm(), 'info': basic_info,
                                                    'basic_skills': basic_skills, "dex": answer,
                                                    'occupational_skill_points': occupational_skill_points,
                                                    'job': job,
                                                    'personal_interest_skill_points': personal_interest_skill_points
                                                    })
    # todo remove job from return dict after trouble shooting
    else:
        try:
            form = SkillsForm(request.POST)
            new_skill_from = form.save(commit=False)
            new_skill_from.user = request.user
            new_skill_from.save()
            return redirect('backstory')
        except ValueError:
            return render(request, 'char/backstory.html',
                          {'form': SkillsForm(), 'error': 'Form not filled out'})


@login_required
def equipment(request):
    cash = 0
    assets = 0
    spending_level = 0
    CR = Skills.objects.filter(user=request.user)
    credit_rating = CR.get().Credit_Rating

    if credit_rating <= 0:
        cash += 0.50
        assets += 0
        spending_level += 0.50
    elif credit_rating in range(1, 9):
        cash += credit_rating * 1
        assets += credit_rating * 10
        spending_level += 2
    elif credit_rating in range(10, 49):
        cash += credit_rating * 2
        assets += credit_rating * 50
        spending_level += 10
    elif credit_rating in range(50, 89):
        cash += credit_rating * 5
        assets += credit_rating * 500
        spending_level += 50
    elif credit_rating in range(90, 98):
        cash += credit_rating * 20
        assets += credit_rating * 2000
        spending_level += 250
    elif credit_rating >= 99:
        cash += 50000
        assets += 5000000
        spending_level += 5000

    if request.method == "GET":
        return render(request, 'char/equipment.html', {'form': EquipmentForm(),
                                                       "CR": credit_rating,
                                                       'cashform': CashForm(),
                                                       'cash': cash,
                                                       'assets': assets,
                                                       'spending_level': spending_level,
                                                       'weapons': WeaponsForm(),
                                                       })
    else:
        try:
            form = EquipmentForm(request.POST)
            new_equipment_from = form.save(commit=False)
            new_equipment_from.user = request.user
            new_equipment_from.save()

            form2 = CashForm(request.POST)
            new_cash_from = form2.save(commit=False)
            new_cash_from.user = request.user
            new_cash_from.save()

            form3 = WeaponsForm(request.POST)
            new_weapons_form = form3.save(commit=False)
            new_weapons_form.user = request.user
            new_weapons_form.save()

            return redirect('done')
        except ValueError:
            return render(request, 'char/backstory.html',
                          {'form': SkillsForm(), 'error': 'Form not filled out'})

@login_required
def done(request):
    return render(request, 'char/done.html')

@login_required
def completed(request, *args, **kwargs):
    basic_info = CharBasicInfo.objects.filter(user=request.user)
    stats = Characteristics.objects.filter(user=request.user)
    background = BackStory.objects.filter(user=request.user)
    equipment_and_gear = Equipment.objects.filter(user=request.user)
    money = CashAndAssets.objects.filter(user=request.user)
    player_skills = Skills.objects.filter(user=request.user)
    weapons = Weapons.objects.filter(user=request.user)
    job = basic_info.get().occupation[12:23]
    luck = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
    name = basic_info.get().name

    str = stats.get().STR
    con = stats.get().CON
    siz = stats.get().SIZ
    dex = stats.get().DEX
    app = stats.get().APP
    edu = stats.get().EDU
    int = stats.get().INT
    pow = stats.get().POW
    age = basic_info.get().age

    move_with_age = 0
    if dex and str < siz:
        move_rate = 7
        if age in range(15, 39):
            move_with_age = move_rate
        elif age in range(40, 49):
            move_with_age = move_rate - 1
        elif age in range(50, 59):
            move_with_age = move_rate - 2
        elif age in range(60, 69):
            move_with_age = move_rate - 3
        elif age in range(70, 79):
            move_with_age = move_rate - 4
        elif age > 80:
            move_with_age = move_rate - 5
    elif dex or str >= siz:
        move_rate = 8
        if age in range(15, 39):
            move_with_age = move_rate
        elif age in range(40, 49):
            move_with_age = move_rate - 1
        elif age in range(50, 59):
            move_with_age = move_rate - 2
        elif age in range(60, 69):
            move_with_age = move_rate - 3
        elif age in range(70, 79):
            move_with_age = move_rate - 4
        elif age > 80:
            move_with_age = move_rate - 5
    elif dex == str == siz:
        move_rate = 8
        if age in range(15, 39):
            move_with_age = move_rate
        elif age in range(40, 49):
            move_with_age = move_rate - 1
        elif age in range(50, 59):
            move_with_age = move_rate - 2
        elif age in range(60, 69):
            move_with_age = move_rate - 3
        elif age in range(70, 79):
            move_with_age = move_rate - 4
        elif age > 80:
            move_with_age = move_rate - 5
    elif dex and str >= siz:
        move_rate = 9
        if age in range(15, 39):
            move_with_age = move_rate
        elif age in range(40, 49):
            move_with_age = move_rate - 1
        elif age in range(50, 59):
            move_with_age = move_rate - 2
        elif age in range(60, 69):
            move_with_age = move_rate - 3
        elif age in range(70, 79):
            move_with_age = move_rate - 4
        elif age > 80:
            move_with_age = move_rate - 5

    improvement_check = random.randint(1, 100)
    if age in range(15, 19):
        str = str - 5
        siz = siz - 5
        edu = edu - 5
        luck_role = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
        luck_role_2 = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
        new_luck_pool = [luck, luck_role, luck_role_2]
        new_luck_pool.sort()
        luck = new_luck_pool[-1]
    elif age in range(20, 39):
        if improvement_check > edu:
            edu = edu + random.randint(1, 10)
    elif age in range(40, 49):
        str = str - 2
        con = con - 1
        dex = dex - 2
        app = app - 5
        improvement_check1 = random.randint(1, 100)
        improvement_check2 = random.randint(1, 100)
        check_pool = [improvement_check1, improvement_check2]
        check_pool.sort()
        for item in check_pool:
            if item > edu:
                edu += random.randint(1, 10)

    elif age in range(50, 59):
        str = str - 3
        con = con - 3
        dex = dex - 4
        app = app - 10
        improvement_check1 = random.randint(1, 100)
        improvement_check2 = random.randint(1, 100)
        improvement_check3 = random.randint(1, 100)
        check_pool = [improvement_check1, improvement_check2, improvement_check3]
        check_pool.sort()
        for item in check_pool:
            if item > edu:
                edu += random.randint(1, 10)

    elif age in range(60, 69):
        str = str - 7
        con = con - 6
        dex = dex - 7
        app = app - 15
        improvement_check1 = random.randint(1, 100)
        improvement_check2 = random.randint(1, 100)
        improvement_check3 = random.randint(1, 100)
        improvement_check4 = random.randint(1, 100)
        check_pool = [improvement_check1, improvement_check2, improvement_check3, improvement_check4]
        check_pool.sort()
        for item in check_pool:
            if item > edu:
                edu += random.randint(1, 10)

    elif age in range(70, 79):
        str = str - 15
        con = con - 10
        dex = dex - 15
        app = app - 20
        improvement_check1 = random.randint(1, 100)
        improvement_check2 = random.randint(1, 100)
        improvement_check3 = random.randint(1, 100)
        improvement_check4 = random.randint(1, 100)
        check_pool = [improvement_check1, improvement_check2, improvement_check3, improvement_check4]
        check_pool.sort()
        for item in check_pool:
            if item > edu:
                edu += random.randint(1, 10)

    elif age > 80:
        str = str - 27
        con = con - 26
        dex = dex - 27
        app = app - 25
        improvement_check1 = random.randint(1, 100)
        improvement_check2 = random.randint(1, 100)
        improvement_check3 = random.randint(1, 100)
        improvement_check4 = random.randint(1, 100)
        check_pool = [improvement_check1, improvement_check2, improvement_check3, improvement_check4]
        check_pool.sort()
        for item in check_pool:
            if item > edu:
                edu += random.randint(1, 10)

    # get str % size from above filtered data
    damage_handout = ""
    build = 0
    check = str + siz
    if check in range(2, 64):
        damage_handout = '-2'
        build = -2
    elif check in range(65, 84):
        damage_handout = "-1"
        build = -1
    elif check in range(85, 124):
        damage_handout = "0"
        build = 0
    elif check in range(125, 164):
        damage_handout = "+ 1D4"
        build = 1
    elif check in range(165, 204):
        damage_handout = "+1D6"
        build = 2
    elif check in range(205, 284):
        damage_handout = "+2D6"
        build = 3
    elif check in range(285, 364):
        damage_handout = "+3D6"
        build = 4
    elif check in range(365, 444):
        damage_handout = "+4D6"
        build = 5
    elif check > 445:
        damage_handout = "+5D6"
        build = 6

    # HP have to be redone with filtered con & size
    hp = (con + siz) / 10
    magic_points = pow / 5
    sanity = pow

    half_str = str / 2
    quarter_str = half_str / 2
    half_con = con / 2
    quarter_con = half_con / 2
    half_siz = siz / 2
    quarter_siz = half_siz / 2
    half_dex = dex / 2
    quarter_dex = half_dex / 2
    half_app = app / 2
    quarter_app = half_app / 2
    half_edu = edu / 2
    quarter_edu = half_edu / 2
    half_int = int / 2
    quarter_int = half_int / 2
    half_pow = pow / 2
    quarter_pow = half_pow / 2

    accounting_is = 0
    if player_skills.get().Accounting > 0:
        accounting_is = player_skills.get().Accounting + 5
    anthropology_is = 0
    if player_skills.get().Anthropology > 0:
        anthropology_is = player_skills.get().Anthropology + 1
    appraise_is = 0
    if player_skills.get().Appraise > 0:
        appraise_is = player_skills.get().Appraise + 5
    archeology_is = 0
    if player_skills.get().Archeology > 0:
        archeology_is = player_skills.get().Archeology + 1
    art_craft_is = 0
    if player_skills.get().Art_Craft > 0:
        art_craft_is = player_skills.get().Art_Craft + 5
    art_craft_chosen_is = ''
    if player_skills.get().Art_Craft_Chosen != 'none':
        art_craft_chosen_is += player_skills.get().Art_Craft_Chosen
    elif player_skills.get().Art_Craft_Chosen == 'none':
        art_craft_chosen_is += 'none'
    charm_is = 0
    if player_skills.get().Charm > 0:
        charm_is = player_skills.get().Charm + 15
    climb_is = 0
    if player_skills.get().Climb > 0:
        climb_is = player_skills.get().Climb + 20
    credit_rating_is = player_skills.get().Credit_Rating
    cthulhu_mythos_is = player_skills.get().Cthulhu_Mythos
    disguise_is = 0
    if player_skills.get().Disguise > 0:
        disguise_is = player_skills.get().Disguise + 5
    dodge_is = player_skills.get().Dodge
    drive_auto_is = 0
    if player_skills.get().Drive_Auto > 0:
        drive_auto_is = player_skills.get().Drive_Auto + 20
    electric_repair_is = 0
    if player_skills.get().Electric_Repair > 0:
        electric_repair_is = player_skills.get().Electric_Repair + 10
    fast_talk_is = 0
    if player_skills.get().Electric_Repair > 0:
        fast_talk_is = player_skills.get().Electric_Repair + 5
    fighting_is = 0
    if player_skills.get().Fighting > 0:
        fighting_is = player_skills.get().Fighting + 25
    handguns_is = 0
    if player_skills.get().Handguns > 0:
        handguns_is = player_skills.get().Handguns + 20
    rifles_shotguns_is = 0
    if player_skills.get().Rifles_Shotguns > 0:
        rifles_shotguns_is = player_skills.get().Rifles_Shotguns + 25
    first_aid_is = 0
    if player_skills.get().First_Aid > 0:
        first_aid_is = player_skills.get().First_Aid + 30
    history_is = 0
    if player_skills.get().History > 0:
        history_is = player_skills.get().History + 5
    intimidate_is = 0
    if player_skills.get().Intimidate > 0:
        intimidate_is = player_skills.get().Intimidate + 15
    jump_is = 0
    if player_skills.get().Jump > 0:
        jump_is = player_skills.get().Jump + 20
    other_language_is = 0
    if player_skills.get().Other_Language > 0:
        other_language_is = player_skills.get().Other_Language + 1
    other_language_chosen_is = ''
    if player_skills.get().Other_Language_Chosen != 'none':
        other_language_chosen_is += player_skills.get().Other_Language_Chosen
    elif player_skills.get().Other_Language_Chosen == 'none':
        other_language_chosen_is += 'none'
    own_language_is = player_skills.get().Own_language
    law_is = 0
    if player_skills.get().Law > 0:
        law_is += player_skills.get().Law + 5
    library_use_is = 0
    if player_skills.get().Library_Use > 0:
        library_use_is = player_skills.get().Library_Use + 20
    listen_is = 0
    if player_skills.get().Listen > 0:
        listen_is = player_skills.get().Listen + 20
    locksmith_is = 0
    if player_skills.get().Locksmith > 0:
        locksmith_is = player_skills.get().Locksmith + 1
    mech_repair_is = 0
    if player_skills.get().Mech_Repair > 0:
        mech_repair_is = player_skills.get().Mech_Repair + 10
    medicine_is = 0
    if player_skills.get().Medicine > 0:
        medicine_is = player_skills.get().Medicine + 1
    natural_world_is = 0
    if player_skills.get().Natural_World > 0:
        natural_world_is = player_skills.get().Natural_World + 10
    navigate_is = 0
    if player_skills.get().Navigate > 0:
        navigate_is = player_skills.get().Navigate + 10
    occult_is = 0
    if player_skills.get().Occult > 0:
        occult_is = player_skills.get().Occult + 5
    op_hv_machine_is = 0
    if player_skills.get().Op_Hv_Machine > 0:
        op_hv_machine_is = player_skills.get().Op_Hv_Machine + 1
    persuade_is = 0
    if player_skills.get().Persuade > 0:
        persuade_is = player_skills.get().Persuade + 10
    pilot_is = 0
    if player_skills.get().Pilot > 0:
        pilot_is = player_skills.get().Pilot + 1

    piloting_is = ''
    if player_skills.get().Piloted_Vehicle != 'none':
        piloting_is += player_skills.get().Piloted_Vehicle
    elif player_skills.get().Piloted_Vehicle == 'none':
        piloting_is += 'none'

    psychology_is = 0
    if player_skills.get().Psychology > 0:
        psychology_is = player_skills.get().Psychology + 10
    psychoanalysis_is = 0
    if player_skills.get().Psychoanalysis > 0:
        psychoanalysis_is = player_skills.get().Psychoanalysis + 1
    ride_is = 0
    if player_skills.get().Ride > 0:
        ride_is = player_skills.get().Ride + 5
    science_is = 0
    if player_skills.get().Science > 0:
        science_is = player_skills.get().Science + 1
    science_chosen_is = ''
    if player_skills.get().Science_chosen != 'none':
        science_chosen_is += player_skills.get().Science_chosen
    elif player_skills.get().Science_chosen == 'none':
        science_chosen_is += 'none'
    slight_of_hand_is = 0
    if player_skills.get().Slight_of_hand > 0:
        slight_of_hand_is = player_skills.get().Slight_of_hand + 10
    spot_hidden_is = 0
    if player_skills.get().Spot_hidden > 0:
        spot_hidden_is = player_skills.get().Spot_hidden + 25
    stealth_is = 0
    if player_skills.get().Stealth > 0:
        stealth_is = player_skills.get().Stealth + 20
    survival_is = 0
    if player_skills.get().Survival > 0:
        survival_is = player_skills.get().Survival + 10
    swim_is = 0
    if player_skills.get().Swim > 0:
        swim_is = player_skills.get().Swim + 20
    throw_is = 0
    if player_skills.get().Throw > 0:
        throw_is = player_skills.get().Throw + 20
    track_is = 0
    if player_skills.get().Track > 0:
        track_is = player_skills.get().Track + 10

    dodge = dodge_is
    half_dodge = dodge / 2
    quarter_dodge = half_dodge / 2

    fighting_skill = fighting_is
    half_fighting_skill = fighting_skill / 2
    quarter_fight = half_fighting_skill / 2

    handgun_skill = handguns_is
    half_handgun_skill = handgun_skill / 2
    quarter_handgun = half_handgun_skill / 2

    long_barrel_skills = rifles_shotguns_is
    half_long_barrel_skills = long_barrel_skills / 2
    quarter_long_barrel_skills = half_long_barrel_skills / 2

    half_accounting = accounting_is / 2
    quarter_accounting = half_accounting / 2
    half_anthropology = anthropology_is / 2
    quarter_anthropology = half_anthropology / 2
    half_appraise = appraise_is / 2
    quarter_appraise = half_appraise / 2
    half_archeology = archeology_is / 2
    quarter_archeology = half_archeology / 2
    half_art_craft = art_craft_is / 2
    quarter_art_craft = half_art_craft / 2
    half_charm = charm_is / 2
    quarter_charm = half_charm / 2
    half_climb = climb_is / 2
    quarter_climb = half_climb / 2
    half_credit = credit_rating_is / 2
    quarter_credit = half_credit / 2
    half_cthulhu_mythos = cthulhu_mythos_is / 2
    quarter_cthulhu_mythos = half_cthulhu_mythos / 2
    half_disguise = disguise_is / 2
    quarter_disguise = half_disguise / 2
    half_drive = drive_auto_is / 2
    quarter_drive = half_drive / 2
    half_elec = electric_repair_is / 2
    quarter_elec = half_elec / 2
    half_fast_talk = fast_talk_is / 2
    quarter_fast_talk = half_fast_talk / 2
    half_first_aid = first_aid_is / 2
    quarter_first_aid = half_first_aid / 2
    half_history = history_is / 2
    quarter_history = half_history / 2
    half_intimidate = intimidate_is / 2
    quarter_intimidate = half_intimidate / 2
    half_jump = jump_is / 2
    quarter_jump = half_jump / 2
    half_other_language = other_language_is / 2
    quarter_other_language = half_other_language / 2
    half_own_language = own_language_is / 2
    quarter_own_language = half_own_language / 2
    half_law = law_is / 2
    quarter_law = half_law / 2
    half_library = library_use_is / 2
    quarter_library = half_library / 2
    half_listen = listen_is / 2
    quarter_listen = half_listen / 2
    half_locksmith = locksmith_is / 2
    quarter_locksmith = half_locksmith / 2
    half_mech = mech_repair_is / 2
    quarter_mech = half_mech / 2
    half_med = medicine_is / 2
    quarter_med = half_med / 2
    half_nat_world = natural_world_is / 2
    quarter_nat_world = half_nat_world / 2
    half_navigate = navigate_is / 2
    quarter_navigate = half_navigate / 2
    half_occult = occult_is / 2
    quarter_occult = half_occult / 2
    half_hv_machine = op_hv_machine_is / 2
    quarter_hv_machine = half_hv_machine / 2
    half_persuade = persuade_is / 2
    quarter_persuade = half_persuade / 2
    half_pilot = pilot_is / 2
    quarter_pilot = half_pilot / 2
    half_psych = psychology_is / 2
    quarter_psych = half_psych / 2
    half_psychoanal = psychoanalysis_is / 2
    quarter_psychoanal = half_psychoanal / 2
    half_ride = ride_is / 2
    quarter_ride = half_ride / 2
    half_science = science_is / 2
    quarter_science = half_science / 2
    half_slight_of_hand = slight_of_hand_is / 2
    quarter_slight_of_hand = half_slight_of_hand / 2
    half_spot_hidden = spot_hidden_is / 2
    quarter_spot_hidden = half_spot_hidden / 2
    half_stealth = stealth_is / 2
    quarter_stealth = half_stealth / 2
    half_survival = survival_is / 2
    quarter_survival = half_survival / 2
    half_swim = swim_is / 2
    quarter_swim = half_swim / 2
    half_throw = throw_is / 2
    quarter_throw = half_throw / 2
    half_track = track_is / 2
    quarter_track = half_track / 2

    hand_weapon = weapons.get().Hand_to_Hand_Weapon
    hand_weapon_damage = weapons.get().Hand_to_Hand_Weapon_Damage
    handgun = weapons.get().Handgun
    handgun_damage = weapons.get().Handgun_Damage
    shotgun = weapons.get().Shotgun
    shotgun_damage = weapons.get().Shotgun_Damage
    rifle = weapons.get().Rifle
    rifle_damage = weapons.get().Rifle_Damage
    automatic_weapon = weapons.get().Automatic_Weapon
    automatic_weapon_damage = weapons.get().Automatic_Weapon_Damage
    misc_weapon = weapons.get().Misc
    misc_weapon_damage = weapons.get().Misc_Damage

    template = get_template('char/completed.html')
    context = {
        "basic_info": basic_info, "stats": stats, 'hp': round(hp),
        'sanity': sanity, 'move': move_with_age, 'luck': luck,
        "str": str, 'half_str': round(half_str),
        "quorter_str": round(quarter_str),
        "con": con, 'half_con': round(half_con),
        'quarter_con': round(quarter_con),
        "siz": siz, 'half_siz': round(half_siz),
        'quarter_siz': round(quarter_siz),
        'dex': dex, 'half_dex': round(half_dex),
        'quarter_dex': round(quarter_dex),
        'app': app, 'half_app': round(half_app),
        'quarter_app': round(quarter_app),
        'edu': edu, 'half_edu': round(half_edu),
        'quarter_edu': round(quarter_edu),
        'int': int, 'half_int': round(half_int),
        'quarter_int': round(quarter_int),
        'pow': pow, 'half_pow': round(half_pow),
        "quarter_pow": round(quarter_pow),
        'backstory': background, 'damage_bonus': damage_handout,
        'build': build,
        'dodge': dodge, 'half_dodge': round(half_dodge),
        'quarter_dodge': round(quarter_dodge),
        'hand_weapon': hand_weapon,
        'hand_weapon_damage': hand_weapon_damage,
        'handgun': handgun, "handgun_damage": handgun_damage,
        "shotgun": shotgun,
        'shotgun_damage': shotgun_damage, 'rifle': rifle,
        'rifle_damage': rifle_damage,
        'automatic_weapon': automatic_weapon,
        'automatic_weapon_damage': automatic_weapon_damage,
        'misc_weapon': misc_weapon,
        'misc_weapon_damage': misc_weapon_damage,
        'fighting_skill': fighting_skill,
        'half_fighting_skill': round(half_fighting_skill),
        'quarter_fight': round(quarter_fight),
        'handgun_skill': handgun_skill,
        'half_handgun_skill': round(half_handgun_skill),
        'quarter_handgun': round(quarter_handgun),
        'long_barrel_skills': long_barrel_skills,
        'half_long_barrel_skills': round(half_long_barrel_skills),
        'quarter_long_barrel_skills': round(quarter_long_barrel_skills),
        'job': job, 'gear': equipment_and_gear, 'cash': money,
        'magic': round(magic_points), 'acc': accounting_is,
        'anthropology': anthropology_is, 'appraise': appraise_is,
        'archeology': archeology_is, 'Art': art_craft_is,
        'charm': charm_is, 'climb': climb_is, 'credit': credit_rating_is,
        'cthulu': cthulhu_mythos_is, 'disguise': disguise_is,
        'dodge_is': dodge_is, 'drive': drive_auto_is,
        'elecrepair': electric_repair_is, 'fasttalk': fast_talk_is,
        'fighting': fighting_is, 'handgun_is': handguns_is, 'longbarrel':
            rifles_shotguns_is, 'firstaid': first_aid_is,
        'history': history_is,
        'intimidate': intimidate_is, 'jump': jump_is, 'language_other':
            other_language_is, 'language_own': own_language_is,
        'law': law_is, 'library_use': library_use_is,
        'listen': listen_is,
        'locksmith': locksmith_is, 'mechrepair': mech_repair_is,
        'medicine': medicine_is, "natural_world": natural_world_is,
        'navigate': navigate_is, 'occult': occult_is,
        'op.hv.mach': op_hv_machine_is, 'persuade': persuade_is,
        'pilot': pilot_is, 'psychology': psychology_is,
        'psychoanalysis': psychoanalysis_is, 'ride': ride_is, 'science':
            science_is, 'slight_of_hand': slight_of_hand_is,
        'spot_hidden':
            spot_hidden_is, 'stealth': stealth_is,
        'survival': survival_is,
        'swim': swim_is, 'throw': throw_is, 'track': track_is,
        'half_accounting': round(half_accounting),
        'quarter_accounting': round(quarter_accounting),
        'half_anthropology':
            round(half_anthropology),
        'quarter_anthropology': round(quarter_anthropology),
        'half_appraise': round(half_appraise),
        'quarter_appraise': round(quarter_appraise),
        'half_archeology': round(half_archeology), 'quarter_archeology':
            round(quarter_archeology),
        'half_art_craft': round(half_art_craft),
        'quarter_art_craft': round(quarter_art_craft),
        'half_charm': round(half_charm),
        'quarter_charm': round(quarter_charm),
        'half_climb': round(half_climb),
        'quarter_climb': round(quarter_climb),
        'half_credit': round(half_credit),
        'quarter_credit': round(quarter_credit),
        'half_cthulhu_mythos': round(half_cthulhu_mythos),
        'quarter_cthulhu_mythos': round(quarter_cthulhu_mythos),
        'half_disguise':
            round(half_disguise),
        'quarter_disguise': round(quarter_disguise),
        'half_fist_aid': round(half_first_aid),
        'q_first_aid': round(quarter_first_aid),
        'half_history': round(half_history),
        'q_history': round(quarter_history),
        'half_intimidate': round(half_intimidate),
        'q_intimidate': round(quarter_intimidate),
        'half_jump': round(half_jump), "q_jump": round(quarter_jump),
        'half_other_language': round(half_other_language),
        'q_other_language': round(quarter_other_language),
        'half_own_language': round(half_own_language),
        'q_own_language': round(quarter_own_language),
        'half_law': round(half_law), 'q_law': round(quarter_law),
        'half_library': round(half_library),
        'q_library': round(quarter_library),
        'half_listen': round(half_listen),
        'q_listen': round(quarter_listen),
        'half_locksmith': round(half_locksmith),
        'q_locksmith': round(quarter_locksmith),
        'half_mech': round(half_mech), 'q_mech': round(quarter_mech),
        'half_med': round(half_med), 'q_med': round(quarter_med),
        'half_natch_world': round(half_nat_world),
        'q_nat_world': round(quarter_nat_world),
        'half_nav': round(half_navigate),
        'q_nav': round(quarter_navigate),
        'half_occult': round(half_occult),
        'q_occult': round(quarter_occult),
        'half_hv_mach': round(half_hv_machine),
        'q_hv_mech': round(quarter_hv_machine),
        'half_persuade': round(half_persuade),
        'q_persuade': round(quarter_persuade),
        'half_pilot': round(half_pilot), 'q_pilot': round(quarter_pilot),
        'half_psych': round(half_psych), 'q_psych': round(quarter_psych),
        'half_psychoanal': round(half_psychoanal),
        'q_psychoanal': round(quarter_psychoanal),
        'half_ride': round(half_ride), 'q_ride': round(quarter_ride),
        'half_science': round(half_science),
        'q_science': round(quarter_science),
        'half_slight_of_hand': round(half_slight_of_hand),
        'q_slight_of_hand': round(quarter_slight_of_hand),
        'half_spot_hidden': round(half_spot_hidden),
        'q_spot_hidden': round(quarter_spot_hidden),
        'half_stealth': round(half_stealth),
        'q_stealth': round(quarter_stealth),
        'half_survival': round(half_survival),
        'q_survival': round(quarter_survival),
        'half_swim': round(half_swim), 'q_swim': round(quarter_swim),
        'half_throw': round(half_throw), 'q_throw': round(quarter_throw),
        'half_track': round(half_track), 'q_track': round(quarter_track),
        'half_auto': round(half_drive), 'q_drive': round(quarter_drive),
        'half_elec': round(half_elec), 'q_elec': round(quarter_elec),
        'half_fast_talk': round(half_fast_talk),
        'q_fast_talk': round(quarter_fast_talk),
        'other_language_known': other_language_chosen_is,
        'art_chosen': art_craft_chosen_is,
        'science_chosen': science_chosen_is,
        'piloting_known': piloting_is,
    }
    # todo add force download and delete after formatting

    pdf = render_to_pdf('char/completed.html', context)

    if pdf:
        return HttpResponse(pdf,
                            content_type='application/force-download/pdf')  # content_type='application/pdf/force-download' || content_type='application/pdf'
    return HttpResponse("Not found")

# @login_required
# def completed(request):
#     basic_info = CharBasicInfo.objects.filter(user=request.user)
#     stats = Characteristics.objects.filter(user=request.user)
#     background = BackStory.objects.filter(user=request.user)
#     equipment_and_gear = Equipment.objects.filter(user=request.user)
#     money = CashAndAssets.objects.filter(user=request.user)
#     player_skills = Skills.objects.filter(user=request.user)
#     weapons = Weapons.objects.filter(user=request.user)
#     job = basic_info.get().occupation[12:23]
#     luck = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
#     name = basic_info.get().name
#
#     str = stats.get().STR
#     con = stats.get().CON
#     siz = stats.get().SIZ
#     dex = stats.get().DEX
#     app = stats.get().APP
#     edu = stats.get().EDU
#     int = stats.get().INT
#     pow = stats.get().POW
#     age = basic_info.get().age
#
#     move_with_age = 0
#     if dex and str < siz:
#         move_rate = 7
#         if age in range(15, 39):
#             move_with_age = move_rate
#         elif age in range(40, 49):
#             move_with_age = move_rate - 1
#         elif age in range(50, 59):
#             move_with_age = move_rate - 2
#         elif age in range(60, 69):
#             move_with_age = move_rate - 3
#         elif age in range(70, 79):
#             move_with_age = move_rate - 4
#         elif age > 80:
#             move_with_age = move_rate - 5
#     elif dex or str >= siz:
#         move_rate = 8
#         if age in range(15, 39):
#             move_with_age = move_rate
#         elif age in range(40, 49):
#             move_with_age = move_rate - 1
#         elif age in range(50, 59):
#             move_with_age = move_rate - 2
#         elif age in range(60, 69):
#             move_with_age = move_rate - 3
#         elif age in range(70, 79):
#             move_with_age = move_rate - 4
#         elif age > 80:
#             move_with_age = move_rate - 5
#     elif dex == str == siz:
#         move_rate = 8
#         if age in range(15, 39):
#             move_with_age = move_rate
#         elif age in range(40, 49):
#             move_with_age = move_rate - 1
#         elif age in range(50, 59):
#             move_with_age = move_rate - 2
#         elif age in range(60, 69):
#             move_with_age = move_rate - 3
#         elif age in range(70, 79):
#             move_with_age = move_rate - 4
#         elif age > 80:
#             move_with_age = move_rate - 5
#     elif dex and str >= siz:
#         move_rate = 9
#         if age in range(15, 39):
#             move_with_age = move_rate
#         elif age in range(40, 49):
#             move_with_age = move_rate - 1
#         elif age in range(50, 59):
#             move_with_age = move_rate - 2
#         elif age in range(60, 69):
#             move_with_age = move_rate - 3
#         elif age in range(70, 79):
#             move_with_age = move_rate - 4
#         elif age > 80:
#             move_with_age = move_rate - 5
#
#     improvement_check = random.randint(1, 100)
#     if age in range(15, 19):
#         str = str - 5
#         siz = siz - 5
#         edu = edu - 5
#         luck_role = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
#         luck_role_2 = (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
#         new_luck_pool = [luck, luck_role, luck_role_2]
#         new_luck_pool.sort()
#         luck = new_luck_pool[-1]
#     elif age in range(20, 39):
#         if improvement_check > edu:
#             edu = edu + random.randint(1, 10)
#     elif age in range(40, 49):
#         str = str - 2
#         con = con - 1
#         dex = dex - 2
#         app = app - 5
#         improvement_check1 = random.randint(1, 100)
#         improvement_check2 = random.randint(1, 100)
#         check_pool = [improvement_check1, improvement_check2]
#         check_pool.sort()
#         for item in check_pool:
#             if item > edu:
#                 edu += random.randint(1, 10)
#
#     elif age in range(50, 59):
#         str = str - 3
#         con = con - 3
#         dex = dex - 4
#         app = app - 10
#         improvement_check1 = random.randint(1, 100)
#         improvement_check2 = random.randint(1, 100)
#         improvement_check3 = random.randint(1, 100)
#         check_pool = [improvement_check1, improvement_check2, improvement_check3]
#         check_pool.sort()
#         for item in check_pool:
#             if item > edu:
#                 edu += random.randint(1, 10)
#
#     elif age in range(60, 69):
#         str = str - 7
#         con = con - 6
#         dex = dex - 7
#         app = app - 15
#         improvement_check1 = random.randint(1, 100)
#         improvement_check2 = random.randint(1, 100)
#         improvement_check3 = random.randint(1, 100)
#         improvement_check4 = random.randint(1, 100)
#         check_pool = [improvement_check1, improvement_check2, improvement_check3, improvement_check4]
#         check_pool.sort()
#         for item in check_pool:
#             if item > edu:
#                 edu += random.randint(1, 10)
#
#     elif age in range(70, 79):
#         str = str - 15
#         con = con - 10
#         dex = dex - 15
#         app = app - 20
#         improvement_check1 = random.randint(1, 100)
#         improvement_check2 = random.randint(1, 100)
#         improvement_check3 = random.randint(1, 100)
#         improvement_check4 = random.randint(1, 100)
#         check_pool = [improvement_check1, improvement_check2, improvement_check3, improvement_check4]
#         check_pool.sort()
#         for item in check_pool:
#             if item > edu:
#                 edu += random.randint(1, 10)
#
#     elif age > 80:
#         str = str - 27
#         con = con - 26
#         dex = dex - 27
#         app = app - 25
#         improvement_check1 = random.randint(1, 100)
#         improvement_check2 = random.randint(1, 100)
#         improvement_check3 = random.randint(1, 100)
#         improvement_check4 = random.randint(1, 100)
#         check_pool = [improvement_check1, improvement_check2, improvement_check3, improvement_check4]
#         check_pool.sort()
#         for item in check_pool:
#             if item > edu:
#                 edu += random.randint(1, 10)
#
#     # get str % size from above filtered data
#     damage_handout = ""
#     build = 0
#     check = str + siz
#     if check in range(2, 64):
#         damage_handout = '-2'
#         build = -2
#     elif check in range(65, 84):
#         damage_handout = "-1"
#         build = -1
#     elif check in range(85, 124):
#         damage_handout = "0"
#         build = 0
#     elif check in range(125, 164):
#         damage_handout = "+ 1D4"
#         build = 1
#     elif check in range(165, 204):
#         damage_handout = "+1D6"
#         build = 2
#     elif check in range(205, 284):
#         damage_handout = "+2D6"
#         build = 3
#     elif check in range(285, 364):
#         damage_handout = "+3D6"
#         build = 4
#     elif check in range(365, 444):
#         damage_handout = "+4D6"
#         build = 5
#     elif check > 445:
#         damage_handout = "+5D6"
#         build = 6
#
#     # HP have to be redone with filtered con & size
#     hp = (con + siz) / 10
#     magic_points = pow / 5
#     sanity = pow
#
#     half_str = str / 2
#     quarter_str = half_str / 2
#     half_con = con / 2
#     quarter_con = half_con / 2
#     half_siz = siz / 2
#     quarter_siz = half_siz / 2
#     half_dex = dex / 2
#     quarter_dex = half_dex / 2
#     half_app = app / 2
#     quarter_app = half_app / 2
#     half_edu = edu / 2
#     quarter_edu = half_edu / 2
#     half_int = int / 2
#     quarter_int = half_int / 2
#     half_pow = pow / 2
#     quarter_pow = half_pow / 2
#
#     accounting_is = 0
#     if player_skills.get().Accounting > 0:
#         accounting_is = player_skills.get().Accounting + 5
#     anthropology_is = 0
#     if player_skills.get().Anthropology > 0:
#         anthropology_is = player_skills.get().Anthropology + 1
#     appraise_is = 0
#     if player_skills.get().Appraise > 0:
#         appraise_is = player_skills.get().Appraise + 5
#     archeology_is = 0
#     if player_skills.get().Archeology > 0:
#         archeology_is = player_skills.get().Archeology + 1
#     art_craft_is = 0
#     if player_skills.get().Art_Craft > 0:
#         art_craft_is = player_skills.get().Art_Craft + 5
#     art_craft_chosen_is = ''
#     if player_skills.get().Art_Craft_Chosen != 'none':
#         art_craft_chosen_is += player_skills.get().Art_Craft_Chosen
#     elif player_skills.get().Art_Craft_Chosen == 'none':
#         art_craft_chosen_is += 'none'
#     charm_is = 0
#     if player_skills.get().Charm > 0:
#         charm_is = player_skills.get().Charm + 15
#     climb_is = 0
#     if player_skills.get().Climb > 0:
#         climb_is = player_skills.get().Climb + 20
#     credit_rating_is = player_skills.get().Credit_Rating
#     cthulhu_mythos_is = player_skills.get().Cthulhu_Mythos
#     disguise_is = 0
#     if player_skills.get().Disguise > 0:
#         disguise_is = player_skills.get().Disguise + 5
#     dodge_is = player_skills.get().Dodge
#     drive_auto_is = 0
#     if player_skills.get().Drive_Auto > 0:
#         drive_auto_is = player_skills.get().Drive_Auto + 20
#     electric_repair_is = 0
#     if player_skills.get().Electric_Repair > 0:
#         electric_repair_is = player_skills.get().Electric_Repair + 10
#     fast_talk_is = 0
#     if player_skills.get().Electric_Repair > 0:
#         fast_talk_is = player_skills.get().Electric_Repair + 5
#     fighting_is = 0
#     if player_skills.get().Fighting > 0:
#         fighting_is = player_skills.get().Fighting + 25
#     handguns_is = 0
#     if player_skills.get().Handguns > 0:
#         handguns_is = player_skills.get().Handguns + 20
#     rifles_shotguns_is = 0
#     if player_skills.get().Rifles_Shotguns > 0:
#         rifles_shotguns_is = player_skills.get().Rifles_Shotguns + 25
#     first_aid_is = 0
#     if player_skills.get().First_Aid > 0:
#         first_aid_is = player_skills.get().First_Aid + 30
#     history_is = 0
#     if player_skills.get().History > 0:
#         history_is = player_skills.get().History + 5
#     intimidate_is = 0
#     if player_skills.get().Intimidate > 0:
#         intimidate_is = player_skills.get().Intimidate + 15
#     jump_is = 0
#     if player_skills.get().Jump > 0:
#         jump_is = player_skills.get().Jump + 20
#     other_language_is = 0
#     if player_skills.get().Other_Language > 0:
#         other_language_is = player_skills.get().Other_Language + 1
#     other_language_chosen_is = ''
#     if player_skills.get().Other_Language_Chosen != 'none':
#         other_language_chosen_is += player_skills.get().Other_Language_Chosen
#     elif player_skills.get().Other_Language_Chosen == 'none':
#         other_language_chosen_is += 'none'
#     own_language_is = player_skills.get().Own_language
#     law_is = 0
#     if player_skills.get().Law > 0:
#         law_is += player_skills.get().Law + 5
#     library_use_is = 0
#     if player_skills.get().Library_Use > 0:
#         library_use_is = player_skills.get().Library_Use + 20
#     listen_is = 0
#     if player_skills.get().Listen > 0:
#         listen_is = player_skills.get().Listen + 20
#     locksmith_is = 0
#     if player_skills.get().Locksmith > 0:
#         locksmith_is = player_skills.get().Locksmith + 1
#     mech_repair_is = 0
#     if player_skills.get().Mech_Repair > 0:
#         mech_repair_is = player_skills.get().Mech_Repair + 10
#     medicine_is = 0
#     if player_skills.get().Medicine > 0:
#         medicine_is = player_skills.get().Medicine + 1
#     natural_world_is = 0
#     if player_skills.get().Natural_World > 0:
#         natural_world_is = player_skills.get().Natural_World + 10
#     navigate_is = 0
#     if player_skills.get().Navigate > 0:
#         navigate_is = player_skills.get().Navigate + 10
#     occult_is = 0
#     if player_skills.get().Occult > 0:
#         occult_is = player_skills.get().Occult + 5
#     op_hv_machine_is = 0
#     if player_skills.get().Op_Hv_Machine > 0:
#         op_hv_machine_is = player_skills.get().Op_Hv_Machine + 1
#     persuade_is = 0
#     if player_skills.get().Persuade > 0:
#         persuade_is = player_skills.get().Persuade + 10
#     pilot_is = 0
#     if player_skills.get().Pilot > 0:
#         pilot_is = player_skills.get().Pilot + 1
#
#     piloting_is = ''
#     if player_skills.get().Piloting != 'none':
#         piloting_is += player_skills.get().Piloting
#     elif player_skills.get().Piloting == 'none':
#         piloting_is += 'none'
#
#     psychology_is = 0
#     if player_skills.get().Psychology > 0:
#         psychology_is = player_skills.get().Psychology + 10
#     psychoanalysis_is = 0
#     if player_skills.get().Psychoanalysis > 0:
#         psychoanalysis_is = player_skills.get().Psychoanalysis + 1
#     ride_is = 0
#     if player_skills.get().Ride > 0:
#         ride_is = player_skills.get().Ride + 5
#     science_is = 0
#     if player_skills.get().Science > 0:
#         science_is = player_skills.get().Science + 1
#     science_chosen_is = ''
#     if player_skills.get().Science_chosen != 'none':
#         science_chosen_is += player_skills.get().Science_chosen
#     elif player_skills.get().Science_chosen == 'none':
#         science_chosen_is += 'none'
#     slight_of_hand_is = 0
#     if player_skills.get().Slight_of_hand > 0:
#         slight_of_hand_is = player_skills.get().Slight_of_hand + 10
#     spot_hidden_is = 0
#     if player_skills.get().Spot_hidden > 0:
#         spot_hidden_is = player_skills.get().Spot_hidden + 25
#     stealth_is = 0
#     if player_skills.get().Stealth > 0:
#         stealth_is = player_skills.get().Stealth + 20
#     survival_is = 0
#     if player_skills.get().Survival > 0:
#         survival_is = player_skills.get().Survival + 10
#     swim_is = 0
#     if player_skills.get().Swim > 0:
#         swim_is = player_skills.get().Swim + 20
#     throw_is = 0
#     if player_skills.get().Throw > 0:
#         throw_is = player_skills.get().Throw + 20
#     track_is = 0
#     if player_skills.get().Track > 0:
#         track_is = player_skills.get().Track + 10
#
#     dodge = dodge_is
#     half_dodge = dodge / 2
#     quarter_dodge = half_dodge / 2
#
#     fighting_skill = fighting_is
#     half_fighting_skill = fighting_skill / 2
#     quarter_fight = half_fighting_skill / 2
#
#     handgun_skill = handguns_is
#     half_handgun_skill = handgun_skill / 2
#     quarter_handgun = half_handgun_skill / 2
#
#     long_barrel_skills = rifles_shotguns_is
#     half_long_barrel_skills = long_barrel_skills / 2
#     quarter_long_barrel_skills = half_long_barrel_skills / 2
#
#     half_accounting = accounting_is / 2
#     quarter_accounting = half_accounting / 2
#     half_anthropology = anthropology_is / 2
#     quarter_anthropology = half_anthropology / 2
#     half_appraise = appraise_is / 2
#     quarter_appraise = half_appraise / 2
#     half_archeology = archeology_is / 2
#     quarter_archeology = half_archeology / 2
#     half_art_craft = art_craft_is / 2
#     quarter_art_craft = half_art_craft / 2
#     half_charm = charm_is / 2
#     quarter_charm = half_charm / 2
#     half_climb = climb_is / 2
#     quarter_climb = half_climb / 2
#     half_credit = credit_rating_is / 2
#     quarter_credit = half_credit / 2
#     half_cthulhu_mythos = cthulhu_mythos_is / 2
#     quarter_cthulhu_mythos = half_cthulhu_mythos / 2
#     half_disguise = disguise_is / 2
#     quarter_disguise = half_disguise / 2
#     half_drive = drive_auto_is / 2
#     quarter_drive = half_drive / 2
#     half_elec = electric_repair_is / 2
#     quarter_elec = half_elec / 2
#     half_fast_talk = fast_talk_is / 2
#     quarter_fast_talk = half_fast_talk / 2
#     half_first_aid = first_aid_is / 2
#     quarter_first_aid = half_first_aid / 2
#     half_history = history_is / 2
#     quarter_history = half_history / 2
#     half_intimidate = intimidate_is / 2
#     quarter_intimidate = half_intimidate / 2
#     half_jump = jump_is / 2
#     quarter_jump = half_jump / 2
#     half_other_language = other_language_is / 2
#     quarter_other_language = half_other_language / 2
#     half_own_language = own_language_is / 2
#     quarter_own_language = half_own_language / 2
#     half_law = law_is / 2
#     quarter_law = half_law / 2
#     half_library = library_use_is / 2
#     quarter_library = half_library / 2
#     half_listen = listen_is / 2
#     quarter_listen = half_listen / 2
#     half_locksmith = locksmith_is / 2
#     quarter_locksmith = half_locksmith / 2
#     half_mech = mech_repair_is / 2
#     quarter_mech = half_mech / 2
#     half_med = medicine_is / 2
#     quarter_med = half_med / 2
#     half_nat_world = natural_world_is / 2
#     quarter_nat_world = half_nat_world / 2
#     half_navigate = navigate_is / 2
#     quarter_navigate = half_navigate / 2
#     half_occult = occult_is / 2
#     quarter_occult = half_occult / 2
#     half_hv_machine = op_hv_machine_is / 2
#     quarter_hv_machine = half_hv_machine / 2
#     half_persuade = persuade_is / 2
#     quarter_persuade = half_persuade / 2
#     half_pilot = pilot_is / 2
#     quarter_pilot = half_pilot / 2
#     half_psych = psychology_is / 2
#     quarter_psych = half_psych / 2
#     half_psychoanal = psychoanalysis_is / 2
#     quarter_psychoanal = half_psychoanal / 2
#     half_ride = ride_is / 2
#     quarter_ride = half_ride / 2
#     half_science = science_is / 2
#     quarter_science = half_science / 2
#     half_slight_of_hand = slight_of_hand_is / 2
#     quarter_slight_of_hand = half_slight_of_hand / 2
#     half_spot_hidden = spot_hidden_is / 2
#     quarter_spot_hidden = half_spot_hidden / 2
#     half_stealth = stealth_is / 2
#     quarter_stealth = half_stealth / 2
#     half_survival = survival_is / 2
#     quarter_survival = half_survival / 2
#     half_swim = swim_is / 2
#     quarter_swim = half_swim / 2
#     half_throw = throw_is / 2
#     quarter_throw = half_throw / 2
#     half_track = track_is / 2
#     quarter_track = half_track / 2
#
#     hand_weapon = weapons.get().Hand_to_Hand_Weapon
#     hand_weapon_damage = weapons.get().Hand_to_Hand_Weapon_Damage
#     handgun = weapons.get().Handgun
#     handgun_damage = weapons.get().Handgun_Damage
#     shotgun = weapons.get().Shotgun
#     shotgun_damage = weapons.get().Shotgun_Damage
#     rifle = weapons.get().Rifle
#     rifle_damage = weapons.get().Rifle_Damage
#     automatic_weapon = weapons.get().Automatic_Weapon
#     automatic_weapon_damage = weapons.get().Automatic_Weapon_Damage
#     misc_weapon = weapons.get().Misc
#     misc_weapon_damage = weapons.get().Misc_Damage
#
#     if request.method == "GET":
#         return render(request, 'char/completed.html', {"basic_info": basic_info, "stats": stats, 'hp': round(hp),
#                                                        'sanity': sanity, 'move': move_with_age, 'luck': luck,
#                                                        "str": str, 'half_str': round(half_str),
#                                                        "quorter_str": round(quarter_str),
#                                                        "con": con, 'half_con': round(half_con),
#                                                        'quarter_con': round(quarter_con),
#                                                        "siz": siz, 'half_siz': round(half_siz),
#                                                        'quarter_siz': round(quarter_siz),
#                                                        'dex': dex, 'half_dex': round(half_dex),
#                                                        'quarter_dex': round(quarter_dex),
#                                                        'app': app, 'half_app': round(half_app),
#                                                        'quarter_app': round(quarter_app),
#                                                        'edu': edu, 'half_edu': round(half_edu),
#                                                        'quarter_edu': round(quarter_edu),
#                                                        'int': int, 'half_int': round(half_int),
#                                                        'quarter_int': round(quarter_int),
#                                                        'pow': pow, 'half_pow': round(half_pow),
#                                                        "quarter_pow": round(quarter_pow),
#                                                        'backstory': background, 'damage_bonus': damage_handout,
#                                                        'build': build,
#                                                        'dodge': dodge, 'half_dodge': round(half_dodge),
#                                                        'quarter_dodge': round(quarter_dodge),
#                                                        'hand_weapon': hand_weapon,
#                                                        'hand_weapon_damage': hand_weapon_damage,
#                                                        'handgun': handgun, "handgun_damage": handgun_damage,
#                                                        "shotgun": shotgun,
#                                                        'shotgun_damage': shotgun_damage, 'rifle': rifle,
#                                                        'rifle_damage': rifle_damage,
#                                                        'automatic_weapon': automatic_weapon,
#                                                        'automatic_weapon_damage': automatic_weapon_damage,
#                                                        'misc_weapon': misc_weapon,
#                                                        'misc_weapon_damage': misc_weapon_damage,
#                                                        'fighting_skill': fighting_skill,
#                                                        'half_fighting_skill': round(half_fighting_skill),
#                                                        'quarter_fight': round(quarter_fight),
#                                                        'handgun_skill': handgun_skill,
#                                                        'half_handgun_skill': round(half_handgun_skill),
#                                                        'quarter_handgun': round(quarter_handgun),
#                                                        'long_barrel_skills': long_barrel_skills,
#                                                        'half_long_barrel_skills': round(half_long_barrel_skills),
#                                                        'quarter_long_barrel_skills': round(quarter_long_barrel_skills),
#                                                        'job': job, 'gear': equipment_and_gear, 'cash': money,
#                                                        'magic': round(magic_points), 'acc': accounting_is,
#                                                        'anthropology': anthropology_is, 'appraise': appraise_is,
#                                                        'archeology': archeology_is, 'Art': art_craft_is,
#                                                        'charm': charm_is, 'climb': climb_is, 'credit': credit_rating_is,
#                                                        'cthulu': cthulhu_mythos_is, 'disguise': disguise_is,
#                                                        'dodge_is': dodge_is, 'drive': drive_auto_is,
#                                                        'elecrepair': electric_repair_is, 'fasttalk': fast_talk_is,
#                                                        'fighting': fighting_is, 'handgun_is': handguns_is, 'longbarrel':
#                                                            rifles_shotguns_is, 'firstaid': first_aid_is,
#                                                        'history': history_is,
#                                                        'intimidate': intimidate_is, 'jump': jump_is, 'language_other':
#                                                            other_language_is, 'language_own': own_language_is,
#                                                        'law': law_is, 'library_use': library_use_is,
#                                                        'listen': listen_is,
#                                                        'locksmith': locksmith_is, 'mechrepair': mech_repair_is,
#                                                        'medicine': medicine_is, "natural_world": natural_world_is,
#                                                        'navigate': navigate_is, 'occult': occult_is,
#                                                        'op.hv.mach': op_hv_machine_is, 'persuade': persuade_is,
#                                                        'pilot': pilot_is, 'psychology': psychology_is,
#                                                        'psychoanalysis': psychoanalysis_is, 'ride': ride_is, 'science':
#                                                            science_is, 'slight_of_hand': slight_of_hand_is,
#                                                        'spot_hidden':
#                                                            spot_hidden_is, 'stealth': stealth_is,
#                                                        'survival': survival_is,
#                                                        'swim': swim_is, 'throw': throw_is, 'track': track_is,
#                                                        'half_accounting': round(half_accounting),
#                                                        'quarter_accounting': round(quarter_accounting),
#                                                        'half_anthropology':
#                                                            round(half_anthropology),
#                                                        'quarter_anthropology': round(quarter_anthropology),
#                                                        'half_appraise': round(half_appraise),
#                                                        'quarter_appraise': round(quarter_appraise),
#                                                        'half_archeology': round(half_archeology), 'quarter_archeology':
#                                                            round(quarter_archeology),
#                                                        'half_art_craft': round(half_art_craft),
#                                                        'quarter_art_craft': round(quarter_art_craft),
#                                                        'half_charm': round(half_charm),
#                                                        'quarter_charm': round(quarter_charm),
#                                                        'half_climb': round(half_climb),
#                                                        'quarter_climb': round(quarter_climb),
#                                                        'half_credit': round(half_credit),
#                                                        'quarter_credit': round(quarter_credit),
#                                                        'half_cthulhu_mythos': round(half_cthulhu_mythos),
#                                                        'quarter_cthulhu_mythos': round(quarter_cthulhu_mythos),
#                                                        'half_disguise':
#                                                            round(half_disguise),
#                                                        'quarter_disguise': round(quarter_disguise),
#                                                        'half_fist_aid': round(half_first_aid),
#                                                        'q_first_aid': round(quarter_first_aid),
#                                                        'half_history': round(half_history),
#                                                        'q_history': round(quarter_history),
#                                                        'half_intimidate': round(half_intimidate),
#                                                        'q_intimidate': round(quarter_intimidate),
#                                                        'half_jump': round(half_jump), "q_jump": round(quarter_jump),
#                                                        'half_other_language': round(half_other_language),
#                                                        'q_other_language': round(quarter_other_language),
#                                                        'half_own_language': round(half_own_language),
#                                                        'q_own_language': round(quarter_own_language),
#                                                        'half_law': round(half_law), 'q_law': round(quarter_law),
#                                                        'half_library': round(half_library),
#                                                        'q_library': round(quarter_library),
#                                                        'half_listen': round(half_listen),
#                                                        'q_listen': round(quarter_listen),
#                                                        'half_locksmith': round(half_locksmith),
#                                                        'q_locksmith': round(quarter_locksmith),
#                                                        'half_mech': round(half_mech), 'q_mech': round(quarter_mech),
#                                                        'half_med': round(half_med), 'q_med': round(quarter_med),
#                                                        'half_natch_world': round(half_nat_world),
#                                                        'q_nat_world': round(quarter_nat_world),
#                                                        'half_nav': round(half_navigate),
#                                                        'q_nav': round(quarter_navigate),
#                                                        'half_occult': round(half_occult),
#                                                        'q_occult': round(quarter_occult),
#                                                        'half_hv_mach': round(half_hv_machine),
#                                                        'q_hv_mech': round(quarter_hv_machine),
#                                                        'half_persuade': round(half_persuade),
#                                                        'q_persuade': round(quarter_persuade),
#                                                        'half_pilot': round(half_pilot), 'q_pilot': round(quarter_pilot),
#                                                        'half_psych': round(half_psych), 'q_psych': round(quarter_psych),
#                                                        'half_psychoanal': round(half_psychoanal),
#                                                        'q_psychoanal': round(quarter_psychoanal),
#                                                        'half_ride': round(half_ride), 'q_ride': round(quarter_ride),
#                                                        'half_science': round(half_science),
#                                                        'q_science': round(quarter_science),
#                                                        'half_slight_of_hand': round(half_slight_of_hand),
#                                                        'q_slight_of_hand': round(quarter_slight_of_hand),
#                                                        'half_spot_hidden': round(half_spot_hidden),
#                                                        'q_spot_hidden': round(quarter_spot_hidden),
#                                                        'half_stealth': round(half_stealth),
#                                                        'q_stealth': round(quarter_stealth),
#                                                        'half_survival': round(half_survival),
#                                                        'q_survival': round(quarter_survival),
#                                                        'half_swim': round(half_swim), 'q_swim': round(quarter_swim),
#                                                        'half_throw': round(half_throw), 'q_throw': round(quarter_throw),
#                                                        'half_track': round(half_track), 'q_track': round(quarter_track),
#                                                        'half_auto': round(half_drive), 'q_drive': round(quarter_drive),
#                                                        'half_elec': round(half_elec), 'q_elec': round(quarter_elec),
#                                                        'half_fast_talk': round(half_fast_talk),
#                                                        'q_fast_talk': round(quarter_fast_talk),
#                                                        'other_language_known': other_language_chosen_is,
#                                                        'art_chosen': art_craft_chosen_is,
#                                                        'science_chosen': science_chosen_is,
#                                                        'piloting_known': piloting_is,
#                                                        })
#
#     else:
#         pass
