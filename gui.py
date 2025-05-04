import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from base import *

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 Funky Tic Tac Toe 🎉")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.player = 'X'
        self.ai = 'O'
        self.player_score = 0
        self.ai_score = 0
        self.engine = TicTacToeAI()

        self.custom_font = ("Comic Sans MS", 18, "bold")
        self.title_font = ("Comic Sans MS", 28, "bold")

        self.game_mode = "AI"  # Default mode to Player vs AI
        self.show_menu()

    def show_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        title = ttk.Label(frame, text="🎮 Tic Tac Toe 🎮", font=self.title_font, bootstyle="warning")
        title.pack(pady=15)

        score_label = ttk.Label(
            frame,
            text=f"😎 Player: {self.player_score}   |   🤖 AI: {self.ai_score}",
            font=("Comic Sans MS", 16, "bold"),
            bootstyle="info"
        )
        score_label.pack(pady=10)

        play_ai_button = ttk.Button(frame, text="Play vs AI", width=25, bootstyle="success-outline", command=self.start_game_ai)
        play_ai_button.pack(pady=15, ipady=5)

        play_pvp_button = ttk.Button(frame, text="Play vs Player", width=25, bootstyle="info-outline", command=self.start_game_pvp)
        play_pvp_button.pack(pady=15, ipady=5)

        quit_button = ttk.Button(frame, text="I'm Done 😴", width=25, bootstyle="danger", command=self.root.destroy)
        quit_button.pack(pady=5, ipady=5)

    def start_game_ai(self):
        self.game_mode = "AI"
        self.start_game()

    def start_game_pvp(self):
        self.game_mode = "PVP"
        self.start_game()

    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if hasattr(self, 'overlay_frame') and self.overlay_frame.winfo_exists():
            self.overlay_frame.destroy()

        self.engine.reset_board()
        self.buttons = []

        game_frame = ttk.Frame(self.root, padding=10)
        game_frame.pack(expand=True)

        for i in range(9):
            btn = ttk.Button(
                game_frame,
                text='',
                width=8,
                style="Funky.TButton",
                command=lambda i=i: self.player_move(i)
            )
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=10, ipadx=5, ipady=20)
            self.buttons.append(btn)

        self.current_player = 'X'  # Player 1 starts

    def player_move(self, index):
        if self.engine.make_move(index, self.current_player):
            self.buttons[index].config(text=self.current_player, bootstyle='success' if self.current_player == 'X' else 'danger')

            if self.engine.check_winner(self.current_player):
                if self.current_player == 'X':
                    self.player_score += 1
                else:
                    self.ai_score += 1
                self.end_game(f"🎉 {self.current_player} wins! 🏆")
                return
            elif self.engine.is_full():
                self.end_game("It's a tie 😐")
                return

            self.switch_turns()

            # If AI mode, let AI make a move
            if self.game_mode == "AI" and self.current_player == self.ai:
                self.ai_move()

    def switch_turns(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def ai_move(self):
        move = self.engine.best_move(self.player, self.ai)
        if move is not None:
            self.engine.make_move(move, self.ai)
            self.buttons[move].config(text=self.ai, bootstyle='danger')
            if self.engine.check_winner(self.ai):
                self.ai_score += 1
                self.end_game("💀 AI wins! Try again?")
                return
            elif self.engine.is_full():
                self.end_game("It's a tie 😐")

    def end_game(self, message):
        # Disable and fade board
        for btn in self.buttons:
            btn.config(state="disabled", bootstyle="secondary")

        # Overlay result frame
        self.overlay_frame = ttk.Frame(self.root, bootstyle="dark", padding=30)
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor="center")

        result_label = ttk.Label(
            self.overlay_frame,
            text=message,
            font=("Comic Sans MS", 24, "bold"),
            bootstyle="warning"
        )
        result_label.pack(pady=15)

        play_again_btn = ttk.Button(
            self.overlay_frame,
            text="🔄 Play Again",
            width=20,
            bootstyle="success-outline",
            command=self.start_game
        )
        play_again_btn.pack(pady=10)

        quit_btn = ttk.Button(
            self.overlay_frame,
            text="❌ Quit",
            width=20,
            bootstyle="danger",
            command=self.root.destroy
        )
        quit_btn.pack()


def main():
    root = ttk.Window(themename="superhero")
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()