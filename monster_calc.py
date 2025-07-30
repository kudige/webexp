import argparse
import logging

logger = logging.getLogger(__name__)

# Example base attack stats for troops by type and tier.
# In a real implementation these should be replaced with accurate values.
TROOP_STATS = {
    ('ground', 10): 517,
    ('ground', 11): 682,
    ('ground', 12): 918,
    ('ground', 13): 1176,
    ('ground', 14): 1494,
    ('ground', 15): 1877,
    ('ground', 16): 2222,

    # correct values
    ('mounted', 10): 3320,
    ('mounted', 11): 4150,
    ('mounted', 12): 5187,
    ('mounted', 13): 5800,
    ('mounted', 14): 6670,
    ('mounted', 15): 7540,
    ('mounted', 16): 8780,

    ('ranged', 10): 585,
    ('ranged', 11): 780,
    ('ranged', 12): 1020,
    ('ranged', 13): 1320,
    ('ranged', 14): 1650,
    ('ranged', 15): 1980,
    ('ranged', 16): 2300,

    ('siege', 10): 1040,
    ('siege', 11): 1390,
    ('siege', 12): 1760,
    ('siege', 13): 2150,
    ('siege', 14): 2550,
    ('siege', 15): 2960,
    ('siege', 16): 3380,
}

# Monster HP (power) and default defense values (approx). The defense values
# are fictional placeholders.
MONSTER_DATA = {
    'Agalope':      {'hp': 5488952582, 'defense': 984422.0478836844},
    'Kraken':      {'hp': 1.6e9, 'defense': 2500},
    'Stymphalian Bird': {'hp': 1.1e9, 'defense': 2300},
    'King of the Vikings': {'hp': 1e9, 'defense': 2100},
    'Sphinx 1':    {'hp': 704297985,  'defense': 170559.99849695482},
    'Sphinx 2':    {'hp': 1000000000,  'defense': 196040.00578249115},
    'Sphinx 3':    {'hp': 3548891756,  'defense': 568515.9690187828},
    'Witch 1':     {'hp': 704297985,    'defense': 170559.99849695482},
    'Witch 2':     {'hp': 1869964315,  'defense': 296040.0051484122},
    'Witch 3':     {'hp': 4059876170,  'defense': 723840.0604081601},
    'Ammit':       {'hp': 800.1e6, 'defense': 1800},
    'Cerberus 1':  {'hp': 1539953030,  'defense': 165880.00432143305},
    'Cerberus 2':  {'hp': 153.4e6, 'defense': 1500},
    'Cerberus 3':  {'hp': 234.2e6, 'defense': 1600},
    'Cerberus 4':  {'hp': 694.9e6, 'defense': 1700},
    'Knight 1':	   { 'hp': 1539953030, 'defense': 165880.0},
    'Knight 2':	   { 'hp': 7547309800, 'defense': 1353581.0},
    'Hydra 1':     {'hp': 3856882361, 'defense': 687648.0095408165},
    'Hydra 2':     {'hp': 66942388250, 'defense': 1444060.0791483587},
    'Lava 1': 	   {'hp': 704297985, 'defense': 170560.00000000003},
    'Ymir 1':	   { 'hp': 599981700, 'defense': 188500.0},
    'Ymir 2':	   { 'hp': 3247900936, 'defense': 506688.0},
    'Golem 1':	   { 'hp': 404297985, 'defense': 170560.00000000003},
    'Golem 2':	   { 'hp': 1169964315, 'defense': 196040.0},
    'Golem 3':	   { 'hp': 3548891756, 'defense': 568516.0},
    'Lava 1':	   { 'hp': 404297985, 'defense': 170560.00000000003},
    'Lava 2':	   { 'hp': 1169964315, 'defense': 196040.0},
    'Lava 3':	   { 'hp': 3548891756, 'defense': 568516.0},
    'Warlord 1':   { 'hp': 704297985, 'defense': 170560.00000000003},
    'Warlord 2':   { 'hp': 1869964315, 'defense': 296040.0},
    'Warlord 3':   { 'hp': 4059876170, 'defense': 723840.0},
    'Pan Ground 1':{ 'hp': 599981700, 'defense': 188500.0},
    'Pan Ground 2':{ 'hp': 3247900936, 'defense': 506688.0},
    'Pan Ground 3':{ 'hp': 6160862088, 'defense': 1103856.0},
    'Pan Ranged 1':{ 'hp': 599981700, 'defense': 188500.0},
    'Pan Ranged 2':{ 'hp': 3247900936, 'defense': 506688.0},
    'Pan Ranged 3':{ 'hp': 6160862088, 'defense': 1103856.0},
    'Pan Mounted 1':{ 'hp': 599981700, 'defense': 188500.0},
    'Pan Mounted 2':{ 'hp': 3247900936, 'defense': 506688.0},
    'Pan Mounted 3':{ 'hp': 6160862088, 'defense': 1103856.0},
    'Desert 5':	   { 'hp': 684741775, 'defense': 203636.0},
    'Desert 6':	   { 'hp': 1074613990, 'defense': 261559.0},
    'Desert 7':	   { 'hp': 1845539262, 'defense': 353206.0},
    'Desert 8':	   { 'hp': 2646694539, 'defense': 431517.99999999994},
    'Desert 9':	   { 'hp': 7135638356, 'defense': 1722739.0},
    'Desert 10':   { 'hp': 13207792150, 'defense': 3534058.0},
    'Viking Hard 33':	   { 'hp': 0, 'defense': 0},
    'Viking Hard 34':	   { 'hp': 0, 'defense': 0},
    'Viking Hard 35':	   { 'hp': 0, 'defense': 0},
    'Viking Hard 36':	   { 'hp': 0, 'defense': 0},
    'Viking Hard 37':	   { 'hp': 0, 'defense': 0},
    'x':	   { 'hp': 0, 'defense': 0},
    'x':	   { 'hp': 0, 'defense': 0},

    # ... add additional monsters as needed
}

# Compatibility coefficients vs monsters
COEFF_BASIC = {
    'ground':  { 't1-t10': 1.1, 't11-t16': 1.0 },
    'ranged':  { 't1-t10': 1.2, 't11-t16': 1.0 },
    'mounted': { 't1-t10': 0.9, 't11-t16': 1.1 },
    'siege':   { 't1-t10': 1.4, 't11-t16': 0.5 },
}

COEFF_VS_PAN = {
    'ground':  { 'Pan Ground': 0.9, 'Pan Ranged': 4.08, 'Pan Mounted': 0.7 },
    'ranged':  { 'Pan Ground': 1.0, 'Pan Ranged': 1.0,  'Pan Mounted': 3.67 },
    'mounted': { 'Pan Ground': 1.4, 'Pan Ranged': 0.65, 'Pan Mounted': 0.76 },
    'siege':   { 'Pan Ground': 0.5, 'Pan Ranged': 0.5,  'Pan Mounted': 0.5 },
}

def calc_troop_attack(base_atk, attack_buff_pct, absolute_buff=0):
    """Compute troop attack after buffs."""
    result = base_atk * (1 + attack_buff_pct / 100.0) + absolute_buff
    logger.debug(
        "Troop attack: base=%s buff_pct=%s absolute_buff=%s result=%s",
        base_atk,
        attack_buff_pct,
        absolute_buff,
        result,
    )
    return result

def calc_monster_def(default_def, defense_debuff_pct):
    """Compute monster defense after debuff."""
    result = default_def * (1 - defense_debuff_pct / 100.0)
    logger.debug(
        "Monster defense: default=%s debuff_pct=%s result=%s",
        default_def,
        defense_debuff_pct,
        result,
    )
    return result

def calc_damage_per_soldier(coeff, troop_atk, monster_def):
    result = coeff * troop_atk * troop_atk / (troop_atk + monster_def)
    logger.debug(
        "Damage per soldier: coeff=%s troop_atk=%s monster_def=%s result=%s",
        coeff,
        troop_atk,
        monster_def,
        result,
    )
    return result

def troops_needed(monster_hp, dmg_per_soldier):
    result = monster_hp / dmg_per_soldier
    logger.debug(
        "Troops needed: hp=%s dmg_per_soldier=%s result=%s",
        monster_hp,
        dmg_per_soldier,
        result,
    )
    return result

def calculate_troops(troop_type, tier, monster_name,
                     attack_buff=0, def_debuff=0, absolute_buff=0,
                     vs_pan=False):
    """Return the number of troops needed for zero wounded."""
    base_atk = TROOP_STATS.get((troop_type, tier))
    if base_atk is None:
        raise ValueError('Unknown troop type or tier')

    monster = MONSTER_DATA[monster_name]
    coeff_table = COEFF_VS_PAN if vs_pan else COEFF_BASIC
    if vs_pan:
        key = monster_name[:-2]
    else:
        key = 't1-t10' if tier <= 10 else 't11-t16'
    logger.debug(
        "Coeff key %s",
        key, 
    )
    coeff = coeff_table[troop_type][key]

    logger.debug(
        "Calculating troops for type=%s tier=%s monster=%s (hp=%s defense=%s)",
        troop_type,
        tier,
        monster_name,
        monster['hp'],
        monster['defense'],
    )
    logger.debug(
        "Base attack=%s, attack_buff=%s, def_debuff=%s, absolute_buff=%s, coeff=%s",
        base_atk,
        attack_buff,
        def_debuff,
        absolute_buff,
        coeff,
    )

    troop_attack = calc_troop_attack(base_atk, attack_buff, absolute_buff)
    monster_def = calc_monster_def(monster['defense'], def_debuff)
    dmg = calc_damage_per_soldier(coeff, troop_attack, monster_def)
    needed = troops_needed(monster['hp'], dmg)

    logger.debug("Resulting troops needed (rounded) = %s", int(needed))

    return int(needed)

def reverse_mdefense(ta, damage, coeff):
    if coeff == 0:
        coeff = 1.1
    if ta == 0:
        ta = TROOP_STATS.get(('mounted', 12))
    return coeff * ta*ta / damage - ta

def main():
    parser = argparse.ArgumentParser(
        description="Calculate troops needed to kill a monster without wounded")
    parser.add_argument('troop_type', choices=['ground', 'ranged', 'mounted', 'siege'])
    parser.add_argument('tier', type=int, help='troop tier, e.g. 10 for T10')
    parser.add_argument('monster', choices=list(MONSTER_DATA))
    parser.add_argument('--attack-buff', type=float, default=0, help='attack buff percentage')
    parser.add_argument('--def-debuff', type=float, default=0, help='monster defense debuff percentage')
    parser.add_argument('--absolute-buff', type=float, default=0, help='absolute attack buff')
    parser.add_argument('--vs-pan', action='store_true', help='use VS Pan coefficients')
    parser.add_argument('--debug', action='store_true', help='enable debug logging')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    result = calculate_troops(
        args.troop_type,
        args.tier,
        args.monster,
        attack_buff=args.attack_buff,
        def_debuff=args.def_debuff,
        absolute_buff=args.absolute_buff,
        vs_pan=args.vs_pan,
    )

    print(result)

if __name__ == '__main__':
    main()
