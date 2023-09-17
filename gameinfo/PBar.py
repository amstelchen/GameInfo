import customtkinter as ctk

G = 572.64
U = 24.99
D = 103.83
W = 12.86
O = 106.56
F = 571.98 / 1024 * 1000

height = 8

class SteamPBar():
    def __init__(self, master, G, U, D, W, O, height=8):
        #pb_Start = ctk.CTkProgressBar(master=root_tk, width=10, height=32, progress_color="#1a9fff", corner_radius=0)
        #pb_Start.set(1)
        #pb_Start.pack(side=ctk.LEFT)

        canvas_Start = ctk.CTkCanvas(root_tk, width=height // 2, height=height, borderwidth=0, highlightthickness=0, bg=None)
        # Coordinates for the arc
        coord = 0, 0, height, height
        # Create the arc with extent=150
        arc = canvas_Start.create_arc(coord, start=90, extent=180, fill="#1a9fff", outline="#1a9fff")
        canvas_Start.pack(side=ctk.LEFT)

        # 572.64 GB
        pb_Games = ctk.CTkProgressBar(master=root_tk, width=int(G), height=height, progress_color="#1a9fff", corner_radius=0)
        pb_Games.set(1)
        pb_Games.pack(side=ctk.LEFT)

        pb_Updates = ctk.CTkProgressBar(master=root_tk, width=int(U), height=height, progress_color="#ef806c", corner_radius=0)
        pb_Updates.set(1)
        pb_Updates.pack(side=ctk.LEFT)

        pb_DLC = ctk.CTkProgressBar(master=root_tk, width=round(D), height=height, progress_color="#5340a6", corner_radius=0)
        pb_DLC.set(1)
        pb_DLC.pack(side=ctk.LEFT)

        pb_Workshop = ctk.CTkProgressBar(master=root_tk, width=int(W), height=height, progress_color="#59bf40", corner_radius=0)
        pb_Workshop.set(1)
        pb_Workshop.pack(side=ctk.LEFT)

        pb_Other = ctk.CTkProgressBar(master=root_tk, width=int(O), height=height, progress_color="#ffc82c", corner_radius=0)
        pb_Other.set(1)
        pb_Other.pack(side=ctk.LEFT)

        canvas_End = ctk.CTkCanvas(root_tk, width=height // 2, height=height, borderwidth=0, highlightthickness=0, bg=None)
        # Coordinates for the arc
        coord = -height // 2, 0, height // 2, height
        # Create the arc with extent=150
        arc = canvas_End.create_arc(coord, start=270, extent=180, fill="#ffc82c", outline="#ffc82c")
        canvas_End.pack(side=ctk.LEFT)

        # progressbar.pack(padx=20, pady=10)

root_tk = ctk.CTk()
SteamPBar(root_tk, G, U, D, W, O, height=12)
root_tk.mainloop()
