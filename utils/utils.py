import dlgo.game_rules_implementation.Player
import dlgo.game_rules_implementation.Point
from dlgo.game_rules_implementation import gotypes
from scipy.stats import binomtest

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' . ',
    dlgo.game_rules_implementation.Player.Player.black: ' B ',
    dlgo.game_rules_implementation.Player.Player.white: ' W ',
    }


def print_move(player, move):
    if move.is_pass:
        move_str = "passes"
    elif move.is_resign:
        move_str = "resigns"
    else:
        move_str = "%s%d" % (COLS[move.point.col - 1], move.point.row)
    print("%s %s" % (player, move_str))


def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(dlgo.game_rules_implementation.Point.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print("%s%d %s" % (bump, row, "".join(line)))
    print("    " + "  ".join(COLS[: board.num_cols]))


def probs_for_gui(move_probs, board_width, board_height):
    # CSS pentru a ajusta dimensiunea și spațiul tabelei
    css_style = """
    <style>
        table {
            width: 500px;
            height: 400px;
            border: none;

        }
        td, th {
            overflow: hidden;
            font-size: 12px; 
            width:50px;
            height:50px;
            padding: 3px;
        }

        th{ 
            color:brown;
            font-weight: bold;
        }
    </style>
    """

    # Definim headerul cu literele A-I și creăm un tabel HTML
    letters = 'ABCDEFGHIJ'[0:board_width]  # Adaptat pentru lățimea tabelei
    header = ''.join(f'<th>{letter}</th>' for letter in letters)
    header_footer = f'<tr><th></th>{header}<th></th></tr>'

    # Începem construcția tabelului HTML
    board_html = f"<html><head>{css_style}</head><body><table><tbody>"
    board_html += header_footer  # Header cu litere

    i = 0
    for row in range(board_height, 0, -1):
        row_html = f"<tr><th>{row}</th>"  # Numărul rândului la început
        for col in range(board_width):
            mi = move_probs[i] * 100
            row_html += f'<td>{mi:.2f}%</td>'
            i += 1
        row_html += f"<th>{row}</th></tr>"  # Numărul rândului la sfârșit
        board_html += row_html

    board_html += header_footer  # Footer cu litere
    board_html += "</tbody></table></body></html>"

    return board_html


print(binomtest(81, 100))