from __future__ import annotations
import argparse
from .api import fetch_bootstrap, fetch_fixtures, next_gw
from .projections import rank_players

def main() -> None:
    parser = argparse.ArgumentParser(prog="fplkit", description="FPL Toolkit CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    top = sub.add_parser("top", help="Top N por posição para a próxima GW")
    top.add_argument("--pos", required=True, choices=["GK", "DEF", "MID", "FWD"])
    top.add_argument("--n", type=int, default=10)

    args = parser.parse_args()

    if args.cmd == "top":
        bootstrap = fetch_bootstrap()
        fixtures = fetch_fixtures()
        gw = next_gw(bootstrap)
        if gw is None:
            print("Não foi possível determinar a próxima GW.")
            return
        ranks = rank_players(bootstrap, fixtures, gw, pos=args.pos, n=args.n)
        print(f"Top {args.n} {args.pos} para GW{gw}")
        for i, (name, score) in enumerate(ranks, 1):
            print(f"{i:>2}. {name:<25} {score:>6.2f}")

if __name__ == "__main__":
    main()
