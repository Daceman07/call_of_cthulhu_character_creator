from django.forms import ModelForm
from .models import CharBasicInfo, Characteristics, BackStory, Skills, Equipment, CashAndAssets, Weapons


class BasicForm(ModelForm):
    class Meta:
        model = CharBasicInfo
        fields = ['name', 'player_name', 'occupation', 'age', 'gender', 'residence', 'birthplace']


class CharacteristicsForm(ModelForm):
    class Meta:
        model = Characteristics
        fields = ['STR', 'DEX', 'INT', 'CON', 'APP', 'POW', 'SIZ', 'EDU', 'LUCK']


class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = ['Accounting', 'Anthropology', 'Appraise', 'Archeology', 'Art_Craft', 'Art_Craft_Chosen', 'Charm', 'Climb',
                  'Credit_Rating', 'Cthulhu_Mythos', 'Disguise', 'Dodge', 'Drive_Auto', 'Electric_Repair', 'Fast_Talk',
                  'Fighting', 'Handguns', 'Rifles_Shotguns', 'First_Aid', 'History', 'Intimidate', 'Jump',
                  'Other_Language', 'Other_Language_Chosen', 'Own_language', 'Law', 'Library_Use', 'Listen', 'Locksmith', 'Mech_Repair',
                  'Medicine', 'Natural_World', 'Navigate', 'Occult', 'Op_Hv_Machine', 'Persuade', 'Pilot', 'Piloted_Vehicle',
                  'Psychology', 'Psychoanalysis', 'Ride', 'Science', 'Science_chosen', 'Slight_of_hand', 'Spot_hidden', 'Stealth',
                  'Survival', 'Swim', 'Throw', 'Track']


class BackStoryForm(ModelForm):
    class Meta:
        model = BackStory
        fields = ['ideology_beliefs', 'ideology_beliefs_descriptor', 'significant_people',
                  'significant_people_descriptor', 'meaningful_locations', 'meaningful_locations_descriptor',
                  'treasured_possessions', 'treasured_possessions_descriptor','select_a_key_connection_from_above',
                  'traits', 'traits_descriptor', 'personal_description', 'injuries_scars', 'phobias_Manias',
                  'arcane_tomes_spells_artifacts', 'encounters_with_strange_entities']


class WeaponsForm(ModelForm):
    class Meta:
        model = Weapons
        fields = ['Hand_to_Hand_Weapon', 'Hand_to_Hand_Weapon_Damage', 'Handgun', 'Handgun_Damage', 'Shotgun',
                  'Shotgun_Damage', 'Rifle', 'Rifle_Damage', 'Automatic_Weapon', 'Automatic_Weapon_Damage',
                  'Misc', 'Misc_Damage']

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['Equipment']


class CashForm(ModelForm):
    class Meta:
        model = CashAndAssets
        fields = ['Cash', 'Assets', 'Spending_level']

