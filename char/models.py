from django.db import models
from django.contrib.auth.models import User
import random


# Create your models here.
class CharBasicInfo(models.Model):
    name = models.CharField(max_length=50)
    player_name = models.CharField(max_length=50, blank=True)
    age = models.IntegerField()
    residence = models.CharField(max_length=150)
    birthplace = models.CharField(max_length=150)

    class Sex(models.TextChoices):
        Male = 'Male'
        Female = 'Female'

    gender = models.TextField(choices=Sex.choices)

    class Jobs(models.TextChoices):
        Antiquarian = "Occupation: Antiquarian. Occupational Skill Point Focus: Appraise, Art/Craft(Any), History, " \
                      "Library Use,Other Language, One interpersonal skill (Charm, Fast Talk, Intimidate, " \
                      "or Persuade), Spot Hidden, any one other Skill. Credit Rating: 30-70 "
        Author = "Occupation: Author.    Occupational Skill Point Focus: Art/Craft(Literature), History, " \
                 "Library Use, Natural world or Occult, Other language, Own language, Psychology, any one other skill. Credit " \
                 "Rating: 9-30 "
        Dilettante = "Occupation: Dilettante. Occupational Skill Point Focus: Art/Craft(Any), Fire Arms, " \
                     "Other Languages, Ride, One interpersonal skill(Charm, Fast Talk, Intimidate, or Persuade)," \
                     " Any three other skills. Credit Rating: 50-99"
        Doctor_of_Medicine = "Occupation: Doctor.    Occupation Skill Point Focus: First Aid, Other Language (Latin)" \
                             "Medicine, Psychology, Science (Biology), Science (Pharmacy), any two other skills as " \
                             "academic or personal specialties (e.g. a psychiatrist might take psychoanalysis). " \
                             "Credit Rating: 30-80"
        Journalist = "Occupation: Journalist. Occupational Skill Point Focus: Art/Craft(Photography), History, " \
                     "Library Use, Own Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade)," \
                     "Psychology, any two other skills. Credit Rating: 9-30"
        Police_Detective = "Occupation: Detective. Occupational Skill Point Focus: Art/Craft(Acting), or Disguise," \
                           "Firearms, Law, Listen, one interpersonal skill(Charm, Fast Talk, Intimidate, " \
                           "or Persuade), Psychology, Spot Hidden, any one other skill. Credit Rating: 20-50"
        Private_Investigator = "Occupation: P.I.       Occupational Skill Point Focus: Art/Craft(Photography), Disguise," \
                               "Law, Library Use, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade)" \
                               "Psychology, Spot Hidden and any one other skill(e.g. Lock Smith, Firearms) " \
                               "Credit Rating: 9-30"
        Professor = "Occupation: Professor. Occupational Skill Point Focus: Library Use, Other Language, Own Language," \
                    "Psychology, any four other skills as academic or personal specialities. Credit Rating: 20-70"
    occupation = models.TextField(choices=Jobs.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Characteristics(models.Model):
    STR = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5)
    DEX = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5)
    INT = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + 6) * 5)
    CON = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5)
    APP = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5)
    POW = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5)
    SIZ = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + 6) * 5)
    EDU = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + 6) * 5)
    LUCK = models.IntegerField(default=(random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        return self.STR, self.DEX, self.INT, self.CON, self.APP, self.POW, self.SIZ, self.EDU, self.LUCK


class BackStory(models.Model):
    class IB(models.TextChoices):
        There_is_a_higher_power_that_you_worship_and_pray_to = "There is a higher power that you worship and pray to"
        Mankind_can_do_fine_without_religions = "Mankind can do fine without religions."
        Science_has_all_the_answers_Pick_a_particular_aspect_of_interest = "Science has all the answers. Pick a " \
                                                                           "particular aspect of interest. "
        A_belief_in_fate = "A belief in fate."
        Member_of_a_society_or_secret_society = "Member of a society or secret society."
        There_is_evil_in_society_that_should_be_rooted_out = "There is evil in society that should be rooted out. " \
                                                             "What is this evil? "
        The_occult = "The occult."
        Politics = "Politics."
        Money_is_power_and_Im_going_to_get_all_I_can = "Money is power, and I'm going to get all I can."
        Campaigner_or_Activist = "Campaigner/Activist."

    class SP(models.TextChoices):
        Parent = "Parent."
        Grandparent = "Grandparent."
        Sibling = "Sibling."
        Child = "Child."
        Partner = "Partner."
        Person_who_taught_you_your_highest_occupational_skill_Identify_the_skill_and_consider_who_taught_you = "Person who taught you your highest occupational skill. Identify the skill and consider who taught you. "
        Childhood_friend = "Childhood friend."
        A_famous_person_Your_idol_or_hero_You_may_never_have_even_met = "A famous person. Your idol or hero. You may " \
                                                                        "never have even met. "
        A_fellow_investigator_in_your_game_Pick_on_or_choose_randomly = "A fellow investigator in your game. Pick on " \
                                                                        "or choose randomly. "
        A_non_player_character_in_the_game = "A non-player character in the game. Ask the Keeper to pick one for you."

    class ML(models.TextChoices):
        Your_seat_of_learning = "Your seat of learning."
        Your_hometown = "Your hometown."
        The_place_you_met_your_first_love = "The place you met your first love."
        A_place_for_quiet_contemplation = "A place for quiet contemplation."
        A_place_for_socializing = "A place for socializing."
        A_place_connected_with_your_ideology_or_belief = "A place connected with your ideology/belief."
        The_grave_of_a_significant_person = "The grave of a significant person. Who?"
        Your_family_home = "Your family home."
        The_place_you_were_happiest_in_your_life = "The place you were happiest in your life."
        Your_workplace = "Your workplace."

    class TP(models.TextChoices):
        An_item_connected_with_your_highest_skill = "An item connected with your highest skill"
        An_essential_item_for_your_occupation = "An essential item for your occupation"
        A_memento_from_you_childhood = "A memento from you childhood"
        A_memento_of_a_departed_person = 'A memento of a departed person'
        Something_given_to_you_by_your_significant_person = 'Something given to you by your significant person'
        Your_collection_What_is_it = 'Your collection. What is it'
        Something_you_found_but_you_dont_know_what_it_is_You_seek_answers = "Something you found but you dont know " \
                                                                            "what it is. You seek answers "
        A_sporting_item = 'eight'
        A_weapon = 'A weapon'
        A_pet = 'A pet'

    class TR(models.TextChoices):
        Generous = "Generous"
        Good_with_animals = " Good with animals"
        Dreamer = "Dreamer"
        Hedonist = "Hedonist"
        Gambler_and_risk_taker = "Gambler and risk taker"
        Good_cook = "Good cook"
        Ladies_man_or_seductress = "Ladies' man/seductress"
        Loyal = "Loyal."
        A_good_reputation = "A good reputation"
        Ambitious = "Ambitious"

    ideology_beliefs = models.TextField(choices=IB.choices)
    ideology_beliefs_descriptor = models.CharField(max_length=250)
    significant_people = models.TextField(choices=SP.choices)
    significant_people_descriptor = models.CharField(max_length=250)
    meaningful_locations = models.TextField(choices=ML.choices)
    meaningful_locations_descriptor = models.CharField(max_length=250)
    treasured_possessions = models.TextField(choices=TP.choices)
    treasured_possessions_descriptor = models.CharField(max_length=250)
    traits = models.TextField(choices=TR.choices)
    traits_descriptor = models.CharField(max_length=250)
    personal_description = models.CharField(max_length=300)
    injuries_scars = models.CharField(max_length=250, default='None')
    phobias_Manias = models.CharField(max_length=250, default='None')
    arcane_tomes_spells_artifacts = models.CharField(max_length=250, default='None')
    encounters_with_strange_entities = models.CharField(max_length=250, default='None')
    select_a_key_connection_from_above = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO User should probably be foreign key basic info

# TODO Note: (default=0, help_text=Text here will show up next to the field)
class Skills(models.Model):
    Accounting = models.IntegerField(default=0)
    Anthropology = models.IntegerField(default=0)
    Appraise = models.IntegerField(default=0)
    Archeology = models.IntegerField(default=0)
    Art_Craft = models.IntegerField(default=0)
    Art_Craft_Chosen = models.CharField(max_length=50, default='none')
    Charm = models.IntegerField(default=0)
    Climb = models.IntegerField(default=0)
    Credit_Rating = models.IntegerField(default=0)
    Cthulhu_Mythos = models.IntegerField(default=0)
    Disguise = models.IntegerField(default=0)
    # Dodge = models.IntegerField(default=(Characteristics.objects.get().DEX / 2))
    Dodge = models.IntegerField(default=0)
    Drive_Auto = models.IntegerField(default=0)
    Electric_Repair = models.IntegerField(default=0)
    Fast_Talk = models.IntegerField(default=0)
    Fighting = models.IntegerField(default=0)
    Handguns = models.IntegerField(default=0)
    Rifles_Shotguns = models.IntegerField(default=0)
    First_Aid = models.IntegerField(default=0)
    History = models.IntegerField(default=0)
    Intimidate = models.IntegerField(default=0)
    Jump = models.IntegerField(default=0)
    Other_Language = models.IntegerField(default=0)
    Other_Language_Chosen = models.CharField(max_length=50, default='none')
    Own_language = models.IntegerField(default=0)
    # Own_language = models.IntegerField(default=Characteristics.objects.get().EDU)
    Law = models.IntegerField(default=0)
    Library_Use = models.IntegerField(default=0)
    Listen = models.IntegerField(default=0)
    Locksmith = models.IntegerField(default=0)
    Mech_Repair = models.IntegerField(default=0)
    Medicine = models.IntegerField(default=0)
    Natural_World = models.IntegerField(default=0)
    Navigate = models.IntegerField(default=0)
    Occult = models.IntegerField(default=0)
    Op_Hv_Machine = models.IntegerField(default=0)
    Persuade = models.IntegerField(default=0)
    Pilot = models.IntegerField(default=0)
    Piloted_Vehicle = models.CharField(max_length=50, default='none')
    Psychology = models.IntegerField(default=0)
    Psychoanalysis = models.IntegerField(default=0)
    Ride = models.IntegerField(default=0)
    Science = models.IntegerField(default=0)
    Science_chosen = models.CharField(max_length=50, default='none')
    Slight_of_hand = models.IntegerField(default=0)
    Spot_hidden = models.IntegerField(default=0)
    Stealth = models.IntegerField(default=0)
    Survival = models.IntegerField(default=0)
    Swim = models.IntegerField(default=0)
    Throw = models.IntegerField(default=0)
    Track = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Equipment(models.Model):
    Equipment = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CashAndAssets(models.Model):
    Cash = models.IntegerField()
    Assets = models.IntegerField()
    Spending_level = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Weapons(models.Model):
    Hand_to_Hand_Weapon = models.CharField(max_length=100, default='None')
    Hand_to_Hand_Weapon_Damage = models.CharField(max_length=100, default='None')
    Handgun = models.CharField(max_length=100, default='None')
    Handgun_Damage = models.CharField(max_length=100, default='None')
    Shotgun = models.CharField(max_length=100, default='None')
    Shotgun_Damage = models.CharField(max_length=100, default='None')
    Rifle = models.CharField(max_length=100, default='None')
    Rifle_Damage = models.CharField(max_length=100, default='None')
    Automatic_Weapon = models.CharField(max_length=100, default='None')
    Automatic_Weapon_Damage = models.CharField(max_length=100, default='None')
    Misc = models.CharField(max_length=100, default='None')
    Misc_Damage = models.CharField(max_length=100, default='None')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #TODO note: Null set to true to see if it can be left blank

