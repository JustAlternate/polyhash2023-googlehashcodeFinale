from polyparser import parse_challenge


def naive_approach_ametheo(challenge):
    solution = []
    game = parse_challenge(challenge)

    dispo = game.drones

    for w in game.warehouses:
        for nbProduit, typeProduit in enumerate(w.stock):
            for d in dispo:
                d.load(w, typeProduit, nbProduit)

    return challenge
