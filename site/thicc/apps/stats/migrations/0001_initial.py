# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-24 17:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('social_django', '0008_partial_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='GmodMapStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gamemode', models.IntegerField(default=0)),
                ('playtime_nor', models.IntegerField(default=0)),
                ('playtime_adv', models.IntegerField(default=0)),
                ('playtime_exp', models.IntegerField(default=0)),
                ('restarts', models.IntegerField(blank=True, default=0)),
                ('custom', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='L4d2MapStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gamemode', models.IntegerField(default=0)),
                ('playtime', models.IntegerField(blank=True, default=0)),
                ('restarts', models.IntegerField(blank=True, default=0)),
                ('custom', models.BooleanField(default=0)),
                ('mutation', models.IntegerField(blank=True, default=0)),
                ('points', models.IntegerField(blank=True, default=0)),
                ('points_infected', models.IntegerField(blank=True, default=0)),
                ('points_survivor', models.IntegerField(blank=True, default=0)),
                ('charger_impacts', models.IntegerField(blank=True, default=0)),
                ('caralarm', models.IntegerField(blank=True, default=0)),
                ('jockey_rides', models.IntegerField(blank=True, default=0)),
                ('infected_spawn_1', models.IntegerField(blank=True, default=0)),
                ('infected_spawn_2', models.IntegerField(blank=True, default=0)),
                ('infected_spawn_3', models.IntegerField(blank=True, default=0)),
                ('infected_spawn_4', models.IntegerField(blank=True, default=0)),
                ('infected_spawn_5', models.IntegerField(blank=True, default=0)),
                ('infected_spawn_6', models.IntegerField(blank=True, default=0)),
                ('infected_spawn_8', models.IntegerField(blank=True, default=0)),
                ('infected_spitter_damage', models.IntegerField(blank=True, default=0)),
                ('infected_tank_damage', models.IntegerField(blank=True, default=0)),
                ('infected_charger_damage', models.IntegerField(blank=True, default=0)),
                ('infected_jocker_ridetime', models.IntegerField(blank=True, default=0)),
                ('infected_jocker_damage', models.IntegerField(blank=True, default=0)),
                ('infected_smoker_damage', models.IntegerField(blank=True, default=0)),
                ('infected_hunter_pounce_counter', models.IntegerField(blank=True, default=0)),
                ('infected_hunter_pounce_damage', models.IntegerField(blank=True, default=0)),
                ('infected_tanksniper', models.IntegerField(blank=True, default=0)),
                ('infected_boomer_vomits', models.IntegerField(blank=True, default=0)),
                ('infected_boomer_blinded', models.IntegerField(blank=True, default=0)),
                ('infected_win', models.IntegerField(blank=True, default=0)),
                ('survivors_win', models.IntegerField(blank=True, default=0)),
                ('survivor_kills', models.IntegerField(blank=True, default=0)),
                ('kills', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('steam64', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('l4d2_mute', models.BooleanField(default=False)),
                ('gmodzs_mute', models.BooleanField(default=False)),
                ('gmodrp_mute', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steam64', models.CharField(max_length=255)),
                ('ip', models.CharField(blank=True, default='0.0.0.0', max_length=16)),
                ('last_used_username', models.CharField(max_length=255)),
                ('last_online', models.CharField(max_length=255)),
                ('last_gamemode', models.IntegerField()),
                ('total_points', models.IntegerField(blank=True, default=0)),
                ('total_playtime', models.IntegerField(blank=True, default=0)),
                ('l4d2_points', models.IntegerField(blank=True, default=0)),
                ('l4d2_playtime', models.IntegerField(blank=True, default=0)),
                ('l4d2_points_infected', models.IntegerField(blank=True, default=0)),
                ('l4d2_points_survivor', models.IntegerField(blank=True, default=0)),
                ('l4d2_headshots', models.IntegerField(blank=True, default=0)),
                ('l4d2_kills', models.IntegerField(blank=True, default=0)),
                ('l4d2_melee_kills', models.IntegerField(blank=True, default=0)),
                ('l4d2_kills_survivor', models.IntegerField(blank=True, default=0)),
                ('l4d2_charger_impacts', models.IntegerField(blank=True, default=0)),
                ('l4d2_friendly_fire', models.IntegerField(blank=True, default=0)),
                ('l4d2_kill_infected', models.IntegerField(blank=True, default=0)),
                ('l4d2_kill_hunter', models.IntegerField(blank=True, default=0)),
                ('l4d2_kill_boomer', models.IntegerField(blank=True, default=0)),
                ('l4d2_kill_spitter', models.IntegerField(blank=True, default=0)),
                ('l4d2_kill_charger', models.IntegerField(blank=True, default=0)),
                ('l4d2_kill_jockey', models.IntegerField(blank=True, default=0)),
                ('l4d2_kill_smoker', models.IntegerField(blank=True, default=0)),
                ('l4d2_kill_tank', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_jockey_ridetime', models.FloatField(blank=True, default=0)),
                ('l4d2_infected_jockey_rides', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_boomer_vomits', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_boomer_blinded', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_hunter_pounce_damage', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_hunter_pounce_counter', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_smoker_damage', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_jockey_damage', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_charger_damage', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_tank_damage', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_tanksniper', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_spitter_damage', models.IntegerField(blank=True, default=0)),
                ('l4d2_infected_spawn_1', models.IntegerField(blank=True, default=0, verbose_name='Spawned as Smoker')),
                ('l4d2_infected_spawn_2', models.IntegerField(blank=True, default=0, verbose_name='Spawned as Boomer')),
                ('l4d2_infected_spawn_3', models.IntegerField(blank=True, default=0, verbose_name='Spawned as Hunter')),
                ('l4d2_infected_spawn_4', models.IntegerField(blank=True, default=0, verbose_name='Spawned as Spitter')),
                ('l4d2_infected_spawn_5', models.IntegerField(blank=True, default=0, verbose_name='Spawned as Jockey')),
                ('l4d2_infected_spawn_6', models.IntegerField(blank=True, default=0, verbose_name='Spawned as Charger')),
                ('l4d2_infected_spawn_8', models.IntegerField(blank=True, default=0, verbose_name='Spawned as Tank')),
                ('l4d2_award_survivor_down', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_bulldozer', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_infected_win', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_allinsafehouse', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_witchdisturb', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_rescue', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_pounce_nice', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_pounce_perfect', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_perfect_blindness', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_gascans_poured', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_upgrades_added', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_matador', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_ledgegrab', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_fincap', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_campaigns', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_medkit', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_adrenaline', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_pills', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_defib', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_protect', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_revive', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_teamkill', models.IntegerField(blank=True, default=0)),
                ('l4d2_award_scatteringram', models.IntegerField(blank=True, default=0)),
                ('gmodzs_playtime', models.IntegerField(blank=True, default=0)),
                ('gmodzs_points', models.IntegerField(blank=True, default=0)),
                ('gmodzs_kills', models.IntegerField(blank=True, default=0)),
                ('gmodzs_kills_as_human', models.IntegerField(blank=True, default=0)),
                ('gmodzs_kills_as_infected', models.IntegerField(blank=True, default=0)),
                ('gmodzs_headshots', models.IntegerField(blank=True, default=0)),
                ('gmodzs_redemptions', models.IntegerField(blank=True, default=0)),
                ('gmodzs_deaths', models.IntegerField(blank=True, default=0)),
                ('gmodrp_points', models.IntegerField(blank=True, default=0)),
                ('gmodrp_playtime', models.IntegerField(blank=True, default=0)),
                ('gmodrp_kills', models.IntegerField(blank=True, default=0)),
                ('gmodrp_deaths', models.IntegerField(blank=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('linked_steam', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_stats_object', to='social_django.UserSocialAuth')),
            ],
            options={
                'verbose_name': "Player's Stats",
                'verbose_name_plural': 'Player In Game Stats',
                'ordering': ['-total_points'],
            },
        ),
    ]
