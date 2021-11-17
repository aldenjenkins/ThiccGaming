from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from djangobb_forum.models import Profile
#from social.apps.django_app.default.models import UserSocialAuth
from django_prometheus.models import ExportModelOperationsMixin

from social_django.models import UserSocialAuth


# Base steam id as shown at https://forums.alliedmods.net/showthread.php?t=60899
steamid64ident = 76561197960265728


@python_2_unicode_compatible
class UserSettings(ExportModelOperationsMixin('userstatssettings'), models.Model):
    steam64 = models.CharField(primary_key=True, max_length=255, null=False)
    l4d2_mute = models.BooleanField(default=False)
    gmodzs_mute = models.BooleanField(default=False)
    gmodrp_mute = models.BooleanField(default=False)
    

@python_2_unicode_compatible
class L4d2MapStats(ExportModelOperationsMixin('l4d2mapstats'), models.Model):
    """
    We have a map stat model for each game because each map only
    applies to one game where a user stat object can apply to every
    game. ex. 
    * a map for l4d2 doesnt need a gmod_headshots field.
    * a map for l4d2 doesnt need a gmod_headshots field.
    """
    name = models.CharField(max_length=255)
    gamemode = models.IntegerField(default=0)
    custom = models.BooleanField(blank=True, default=0)
    playtime = models.IntegerField(blank=True, default=0)
    restarts = models.IntegerField(blank=True, default=0)
    custom = models.BooleanField(blank=True, default=0)
    mutation = models.IntegerField(blank=True, default=0)
    points = models.IntegerField(blank=True, default=0)
    points_infected = models.IntegerField(blank=True, default=0)
    points_survivor = models.IntegerField(blank=True, default=0)
    charger_impacts = models.IntegerField(blank=True, default=0)
    caralarm = models.IntegerField(blank=True, default=0)
    infected_tanksniper = models.IntegerField(blank=True, default=0)
    jockey_rides = models.IntegerField(blank=True, default=0)
    infected_spawn_1 = models.IntegerField(blank=True, default=0)
    infected_spawn_2 = models.IntegerField(blank=True, default=0)
    infected_spawn_3 = models.IntegerField(blank=True, default=0)
    infected_spawn_4 = models.IntegerField(blank=True, default=0)
    infected_spawn_5 = models.IntegerField(blank=True, default=0)
    infected_spawn_6 = models.IntegerField(blank=True, default=0)
    infected_spawn_8 = models.IntegerField(blank=True, default=0)
    infected_spitter_damage = models.IntegerField(blank=True, default=0)
    infected_tank_damage = models.IntegerField(blank=True, default=0)
    infected_charger_damage = models.IntegerField(blank=True, default=0)
    infected_jocker_ridetime = models.IntegerField(blank=True, default=0)
    infected_jocker_damage = models.IntegerField(blank=True, default=0)
    infected_smoker_damage = models.IntegerField(blank=True, default=0)
    infected_hunter_pounce_counter = models.IntegerField(blank=True, default=0)
    infected_hunter_pounce_damage = models.IntegerField(blank=True, default=0)
    infected_tanksniper = models.IntegerField(blank=True, default=0)
    infected_boomer_vomits = models.IntegerField(blank=True, default=0)
    infected_boomer_blinded = models.IntegerField(blank=True, default=0)
    infected_win = models.IntegerField(blank=True, default=0)
    survivors_win = models.IntegerField(blank=True, default=0)
    survivor_kills = models.IntegerField(blank=True, default=0)
    kills = models.IntegerField(blank=True, default=0)


@python_2_unicode_compatible
class GmodMapStats(ExportModelOperationsMixin('gmodmapstat'), models.Model):
    name = models.CharField(max_length=255)
    gamemode = models.IntegerField(default=0)
    custom = models.BooleanField(default=0)
    playtime_nor = models.IntegerField(default=0)
    playtime_adv = models.IntegerField(default=0)
    playtime_exp = models.IntegerField(default=0)
    restarts = models.IntegerField(blank=True, default=0)
    custom = models.BooleanField(default=0)


@python_2_unicode_compatible
class UserStats(ExportModelOperationsMixin('userstats'), models.Model):
    """
    We must allow users not registered on ThiccGaming.com with their
    steam account linked to have their stats tracked.
    """
    linked_steam = models.OneToOneField(
        UserSocialAuth, related_name="my_stats_object", on_delete=models.SET_NULL,
        blank=True, null=True)
    steam64 = models.CharField(max_length=255, null=False)
    ip = models.CharField(max_length=16, blank=True, default="0.0.0.0")
    last_used_username = models.CharField(max_length=255, blank=False, null=False)
    last_online = models.CharField(max_length=255, blank=False)
    last_gamemode = models.IntegerField(blank=False)
    total_points = models.IntegerField(blank=True, default=0)
    total_playtime = models.IntegerField(blank=True, default=0)
    l4d2_points = models.IntegerField(blank=True, default=0)
    l4d2_playtime = models.IntegerField(blank=True, default=0)
    l4d2_points_infected = models.IntegerField(blank=True, default=0)
    l4d2_points_survivor = models.IntegerField(blank=True, default=0)
    l4d2_headshots = models.IntegerField(blank=True, default=0)
    l4d2_kills = models.IntegerField(blank=True, default=0)
    l4d2_melee_kills = models.IntegerField(blank=True, default=0)
    l4d2_kills_survivor = models.IntegerField(blank=True, default=0)
    l4d2_charger_impacts = models.IntegerField(blank=True, default=0)
    l4d2_friendly_fire = models.IntegerField(blank=True, default=0)
    l4d2_kill_infected = models.IntegerField(blank=True, default=0)
    l4d2_kill_hunter = models.IntegerField(blank=True, default=0)
    l4d2_kill_boomer = models.IntegerField(blank=True, default=0)
    l4d2_kill_spitter = models.IntegerField(blank=True, default=0)
    l4d2_kill_charger = models.IntegerField(blank=True, default=0)
    l4d2_kill_jockey = models.IntegerField(blank=True, default=0)
    l4d2_kill_smoker = models.IntegerField(blank=True, default=0)
    l4d2_kill_tank = models.IntegerField(blank=True, default=0)
    l4d2_infected_jockey_ridetime = models.FloatField(blank=True, default=0)
    l4d2_infected_jockey_rides = models.IntegerField(blank=True, default=0)
    l4d2_infected_boomer_vomits = models.IntegerField(blank=True, default=0)
    l4d2_infected_boomer_blinded = models.IntegerField(blank=True, default=0)
    l4d2_infected_hunter_pounce_damage = models.IntegerField(blank=True, default=0)
    l4d2_infected_hunter_pounce_counter = models.IntegerField(blank=True, default=0)
    l4d2_infected_smoker_damage = models.IntegerField(blank=True, default=0)
    l4d2_infected_jockey_damage = models.IntegerField(blank=True, default=0)
    l4d2_infected_charger_damage = models.IntegerField(blank=True, default=0)
    l4d2_infected_tank_damage = models.IntegerField(blank=True, default=0)
    l4d2_infected_tanksniper = models.IntegerField(blank=True, default=0)
    l4d2_infected_spitter_damage = models.IntegerField(blank=True, default=0)
    l4d2_infected_spawn_1 = models.IntegerField("Spawned as Smoker", blank=True, default=0)
    l4d2_infected_spawn_2 = models.IntegerField("Spawned as Boomer", blank=True, default=0)
    l4d2_infected_spawn_3 = models.IntegerField("Spawned as Hunter", blank=True, default=0)
    l4d2_infected_spawn_4 = models.IntegerField("Spawned as Spitter", blank=True, default=0)
    l4d2_infected_spawn_5 = models.IntegerField("Spawned as Jockey", blank=True, default=0)
    l4d2_infected_spawn_6 = models.IntegerField("Spawned as Charger", blank=True, default=0)
    l4d2_infected_spawn_8 = models.IntegerField("Spawned as Tank", blank=True, default=0)
    l4d2_award_survivor_down = models.IntegerField(blank=True, default=0)
    l4d2_award_bulldozer = models.IntegerField(blank=True, default=0)
    l4d2_award_infected_win = models.IntegerField(blank=True, default=0)
    l4d2_award_allinsafehouse = models.IntegerField(blank=True, default=0)
    l4d2_award_witchdisturb = models.IntegerField(blank=True, default=0)
    l4d2_award_rescue = models.IntegerField(blank=True, default=0)
    l4d2_award_pounce_nice = models.IntegerField(blank=True, default=0)
    l4d2_award_pounce_perfect = models.IntegerField(blank=True, default=0)
    l4d2_award_perfect_blindness = models.IntegerField(blank=True, default=0)
    l4d2_award_gascans_poured = models.IntegerField(blank=True, default=0)
    l4d2_award_upgrades_added = models.IntegerField(blank=True, default=0)
    l4d2_award_matador = models.IntegerField(blank=True, default=0)
    l4d2_award_ledgegrab = models.IntegerField(blank=True, default=0)
    l4d2_award_fincap = models.IntegerField(blank=True, default=0)
    l4d2_award_campaigns = models.IntegerField(blank=True, default=0)
    l4d2_award_medkit = models.IntegerField(blank=True, default=0)
    l4d2_award_adrenaline = models.IntegerField(blank=True, default=0)
    l4d2_award_pills = models.IntegerField(blank=True, default=0)
    l4d2_award_defib = models.IntegerField(blank=True, default=0)
    l4d2_award_protect = models.IntegerField(blank=True, default=0)
    l4d2_award_revive = models.IntegerField(blank=True, default=0)
    l4d2_award_scatteringram = models.IntegerField(blank=True, default=0)
    l4d2_award_teamkill = models.IntegerField(blank=True, default=0)
    l4d2_award_tankkillnodeaths = models.IntegerField(blank=True, default=0)
    l4d2_award_hunter = models.IntegerField(blank=True, default=0)
    l4d2_award_smoker = models.IntegerField(blank=True, default=0)
    l4d2_award_left4dead = models.IntegerField(blank=True, default=0)
    l4d2_award_letinsafehouse = models.IntegerField(blank=True, default=0)
    gmodzs_headshots = models.IntegerField(blank=True, default=0)
    gmodzs_playtime = models.IntegerField(blank=True, default=0)
    gmodzs_points = models.IntegerField(blank=True, default=0)
    gmodzs_kills = models.IntegerField(blank=True, default=0)
    gmodzs_kills_as_human = models.IntegerField(blank=True, default=0)
    gmodzs_kills_as_infected = models.IntegerField(blank=True, default=0)
    gmodzs_headshots = models.IntegerField(blank=True, default=0)
    gmodzs_redemptions = models.IntegerField(blank=True, default=0)
    gmodzs_deaths = models.IntegerField(blank=True, default=0)
    gmodrp_points = models.IntegerField(blank=True, default=0)
    gmodrp_playtime = models.IntegerField(blank=True, default=0)
    gmodrp_kills = models.IntegerField(blank=True, default=0)
    gmodrp_deaths = models.IntegerField(blank=True, default=0)

    class Meta: 
        ordering = ["-total_points"]
        verbose_name = "Player's Stats"
        verbose_name_plural = "Player In Game Stats"

    def steam3(self):
        difference = int(self.steam64) - steamid64ident
        Y = 0 if difference % 2 == 0 else 1
        return "[U:{}:{}]".format(Y, difference)

    def steamid(self):
        steamid = ['STEAM_0:']
        steamidacct = int(self.steam64) - steamid64ident
        steamid.append('0:') if steamidacct % 2 == 0 else steamid.append('1:')
        steamid.append(str(steamidacct // 2))
        return ''.join(steamid)

    @property
    def overall_rank(self):
        return UserStats.objects.filter(total_points__gt=self.total_points).count() + 1


    def l4d2_stats(self):
        return {
            "Points": self.l4d2_points,
            "Points Infected": self.l4d2_points_infected,
            "Points Survivor": self.l4d2_points_survivor,
            "Friendly Fires": self.l4d2_friendly_fire,
            "Team Kills": self.l4d2_award_teamkill,
            "Kills": self.l4d2_kills,
            "Kills with melee weapons": self.l4d2_melee_kills,
            "Survivors Killed": self.l4d2_kills_survivor,
            "Infected Killed": self.l4d2_kill_infected,
            "Hunters Killed": self.l4d2_kill_hunter,
            "Boomers Killed": self.l4d2_kill_boomer,
            "Spitters Killed": self.l4d2_kill_spitter,
            "Jockeys Killed": self.l4d2_kill_jockey,
            "Smokers Killed": self.l4d2_kill_smoker,
            "Damage Dealt as Jockey": self.l4d2_infected_jockey_damage,
            "Charger Impacts": self.l4d2_charger_impacts,
            "Damage Dealt as Charger": self.l4d2_infected_charger_damage,
            "Jockey Ride Time": self.l4d2_infected_jockey_ridetime,
            "Boomer Vomits": self.l4d2_infected_boomer_vomits,
            "Boomer Blinds": self.l4d2_infected_boomer_blinded,
            "Hunter Pounces": self.l4d2_infected_hunter_pounce_counter,
            "Hunter Pounce Damage": self.l4d2_infected_hunter_pounce_damage,
            "Damage Dealt as Smoker": self.l4d2_infected_smoker_damage,
            "Damage Dealt as Tank": self.l4d2_infected_tank_damage,
            "Tank Sniper": self.l4d2_infected_tanksniper,
            "Damage Dealt as Spitter": self.l4d2_infected_spitter_damage,
            "Spawns as Infected": self.l4d2_infected_spawn_1,
            "Spawns as Smoker": self.l4d2_infected_spawn_1,
            "Spawns as Boomer": self.l4d2_infected_spawn_2,
            "Spawns as Hunter": self.l4d2_infected_spawn_3,
            "Spawns as Spitter": self.l4d2_infected_spawn_4,
            "Spawns as Jockey": self.l4d2_infected_spawn_5,
            "Spawns as Charger": self.l4d2_infected_spawn_6,
            "Spawns as Tank": self.l4d2_infected_spawn_8,
            "Survivors Incapped": self.l4d2_award_survivor_down,
            "Bulldozed Survivors": self.l4d2_award_bulldozer,
            "Rounds won as Infected": self.l4d2_award_infected_win,
            "All Survivors in Safehouse as Survivor": self.l4d2_award_allinsafehouse,
            "Witches Disturbed": self.l4d2_award_witchdisturb,
            "Rescued Incapped Teammate": self.l4d2_award_rescue,
            "Nice Pounces": self.l4d2_award_pounce_nice,
            "Perfect Pounces": self.l4d2_award_pounce_perfect,
            "Perfect Blindings": self.l4d2_award_perfect_blindness,
            "Gascans Poured": self.l4d2_award_gascans_poured,
            "Upgrades Added": self.l4d2_award_upgrades_added,
            "Matador": self.l4d2_award_matador,
            "Ledge Grabs": self.l4d2_award_ledgegrab,
            "Fincaps": self.l4d2_award_upgrades_added,
            "Campaigns Completed": self.l4d2_award_campaigns,
            "Medkits Given": self.l4d2_award_medkit,
            "Adrenalines Given": self.l4d2_award_adrenaline,
            "Pills Given": self.l4d2_award_pills,
            "Defibs Given": self.l4d2_award_defib,
            "Protected Teammate": self.l4d2_award_protect,
            "Revived Teammate": self.l4d2_award_revive,
            "Scattering Ram Award": self.l4d2_award_scatteringram,
        }

    def gmodzs_stats(self):
        return {
            "Points": self.gmodzs_points,
            "Playtime": self.gmodzs_playtime,
            "Kills": self.gmodzs_kills,
            "Kills as Human": self.gmodzs_kills_as_human,
            "Kills as Infected": self.gmodzs_kills_as_infected,
            "Deaths": self.gmodzs_deaths,
            "Headshots": self.gmodzs_headshots,
            "Redemptions": self.gmodzs_redemptions,
        }
