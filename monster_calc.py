import argparse

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

    ('mounted', 10): 620,
    ('mounted', 11): 820,
    ('mounted', 12): 1105,
    ('mounted', 13): 1415,
    ('mounted', 14): 1730,
    ('mounted', 15): 2070,
    ('mounted', 16): 2420,

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
    'Azazel':      {'hp': 2.6e9, 'defense': 3000},
    'Kraken':      {'hp': 1.6e9, 'defense': 2500},
    'Stymphalian Bird': {'hp': 1.1e9, 'defense': 2300},
    'King of the Vikings': {'hp': 1e9, 'defense': 2100},
    'Sphinx 1':    {'hp': 12.4e6,  'defense': 1400},
    'Sphinx 2':    {'hp': 22.3e6,  'defense': 1500},
    'Sphinx 3':    {'hp': 74.5e6,  'defense': 1600},
    'Sphinx 7':    {'hp': 914.4e6, 'defense': 2000},
    'Witch 1':     {'hp': 13e6,    'defense': 1200},
    'Witch 2':     {'hp': 24.6e6,  'defense': 1300},
    'Witch 3':     {'hp': 85.6e6,  'defense': 1450},
    'Ammit':       {'hp': 800.1e6, 'defense': 1800},
    'Cerberus 1':  {'hp': 68.2e6,  'defense': 1400},
    'Cerberus 2':  {'hp': 153.4e6, 'defense': 1500},
    'Cerberus 3':  {'hp': 234.2e6, 'defense': 1600},
    'Cerberus 4':  {'hp': 694.9e6, 'defense': 1700},
    'Hydra 5':     {'hp': 678.8e6, 'defense': 1700},
    'Lava Turtle 6': {'hp': 668.1e6, 'defense': 1600},
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
    'ground':  { 'Pan (Ground)': 0.9, 'Pan (Ranged)': 4.08, 'Pan (Mounted)': 0.7 },
    'ranged':  { 'Pan (Ground)': 1.0, 'Pan (Ranged)': 1.0,  'Pan (Mounted)': 3.67 },
    'mounted': { 'Pan (Ground)': 1.4, 'Pan (Ranged)': 0.65, 'Pan (Mounted)': 0.76 },
    'siege':   { 'Pan (Ground)': 0.5, 'Pan (Ranged)': 0.5,  'Pan (Mounted)': 0.5 },
}

def calc_troop_attack(base_atk, attack_buff_pct, absolute_buff=0):
    """Compute troop attack after buffs."""
    return base_atk * (1 + attack_buff_pct / 100.0) + absolute_buff

def calc_monster_def(default_def, defense_debuff_pct):
    """Compute monster defense after debuff."""
    return default_def * (1 - defense_debuff_pct / 100.0)

def calc_damage_per_soldier(coeff, troop_atk, monster_def):
    return coeff * troop_atk * troop_atk / (troop_atk + monster_def)

def troops_needed(monster_hp, dmg_per_soldier):
    return monster_hp / dmg_per_soldier

def calculate_troops(troop_type, tier, monster_name,
                     attack_buff=0, def_debuff=0, absolute_buff=0,
                     vs_pan=False):
    """Return the number of troops needed for zero wounded."""
    base_atk = TROOP_STATS.get((troop_type, tier))
    if base_atk is None:
        raise ValueError('Unknown troop type or tier')

    monster = MONSTER_DATA[monster_name]
    coeff_table = COEFF_VS_PAN if vs_pan else COEFF_BASIC
    key = 't1-t10' if tier <= 10 else 't11-t16'
    coeff = coeff_table[troop_type][key]

    troop_attack = calc_troop_attack(base_atk, attack_buff, absolute_buff)
    monster_def = calc_monster_def(monster['defense'], def_debuff)
    dmg = calc_damage_per_soldier(coeff, troop_attack, monster_def)
    needed = troops_needed(monster['hp'], dmg)

    return int(needed)


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
    args = parser.parse_args()

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
